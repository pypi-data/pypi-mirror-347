from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from typing import (
    Any,
    Optional,
    Iterable,
    Sequence,
    Iterator,
    Dict,
    Union,
)

import logging
from itertools import cycle
import json
from jinja2 import Template
import textwrap
import uuid

logger = logging.getLogger(__name__)

IMPORT_ERROR_MESSAGE = """
Error: Gel Python package is not installed.
Please install it using 'pip install gel'.
"""

NO_PROJECT_MESSAGE = """
Error: it appears that the Gel project has not been initialized.
If that's the case, please run 'gel project init' to get started.
"""

MISSING_RECORD_TYPE_TEMPLATE = """
Error: Record type {{record_type}} is missing from the Gel schema.

In order to use the LangChain integration, ensure you put the following in dbschema/default.gel:

    using extension pgvector;
                                        
    module default {
        scalar type EmbeddingVector extending ext::pgvector::vector<1536>;

        type {{record_type}} {
            required collection: str;
            text: str;
            embedding: EmbeddingVector; 
            external_id: str {
                constraint exclusive;
            };
            metadata: json;

            index ext::pgvector::hnsw_cosine(m := 16, ef_construction := 128)
                on (.embedding)
        } 
    }

Remember that you also need to run a migration:
    
    $ gel migration create
    $ gel migrate

"""

try:
    import gel
except ImportError as e:
    logger.error(IMPORT_ERROR_MESSAGE)
    raise e


def format_query(text: str) -> Template:
    return Template(textwrap.dedent(text.strip()))


COSINE_SIMILARITY_QUERY = format_query(
    """
    with collection_records := (select {{record_type}} filter .collection = <str>$collection_name)
    select collection_records {
        external_id, 
        text,
        embedding,
        metadata,
        cosine_similarity := 1 - ext::pgvector::cosine_distance(
            .embedding, <ext::pgvector::vector>$query_embedding),
    }
    {{filter_clause}}
    order by .cosine_similarity desc empty last
    limit <optional int64>$limit;
    """
)

SELECT_BY_DOC_ID_QUERY = format_query(
    """
    select {{record_type}} {
        external_id,
        text,
        embedding,
        metadata, 
    }
    filter .external_id in array_unpack(<array<str>>$external_ids);
    """
)

INSERT_QUERY = format_query(
    """
    select (
        insert {{record_type}} {
            collection := <str>$collection_name,
            external_id := <optional str>$external_id,
            text := <str>$text,
            embedding := <ext::pgvector::vector>$embedding,
            metadata := <json>$metadata,
        } unless conflict on .external_id else (
            update {{record_type}} set {
                collection := <str>$collection_name,
                text := <str>$text,
                embedding := <ext::pgvector::vector>$embedding,
                metadata := <json>$metadata,
            }
        )
    ) { external_id }
    """
)

DELETE_BY_IDS_QUERY = format_query(
    """
    with collection_records := (select {{record_type}} filter .collection = <str>$collection_name)
    delete {{record_type}} 
    filter .external_id in array_unpack(<array<str>>$external_ids);
    """
)

DELETE_ALL_QUERY = format_query(
    """
    delete {{record_type}}
    filter .collection = <str>$collection_name;
    """
)


FILTER_OPS = {
    # logical
    "$and": "and",
    "$or": "or",
    # array
    "$in": "in",
    "$nin": "not in",
    # comparison
    "$eq": "=",
    "$ne": "!=",
    "$lt": "<",
    "$lte": "<=",
    "$gt": ">",
    "$gte": ">=",
    "$like": "like",
    "$ilike": "ilike",
    # not implemented
    "$between": None,
}


def filter_to_edgeql(filter: Union[dict, str, int, float]) -> str:
    if isinstance(filter, str) or isinstance(filter, int) or isinstance(filter, float):
        formatted_filter = f'"{filter}"' if isinstance(filter, str) else str(filter)
        return f" = {formatted_filter}"

    assert isinstance(filter, dict), (
        f"Expected a dict of operands but got: {type(filter)}: {filter}"
    )

    # Handle $and and $or operators at the top level
    if "$and" in filter:
        assert isinstance(filter["$and"], list), (
            f"Expected a list of dicts for $and operator but got: {type(filter['$and'])}"
        )
        filter_clause = " and ".join(filter_to_edgeql(item) for item in filter["$and"])
        return f"({filter_clause})"

    if "$or" in filter:
        assert isinstance(filter["$or"], list), (
            f"Expected a list of dicts for $or operator but got: {type(filter['$or'])}"
        )
        filter_clause = " or ".join(filter_to_edgeql(item) for item in filter["$or"])
        return f"({filter_clause})"

    # Handle field-level operators
    field_filters = []
    for field, value in filter.items():
        if isinstance(value, dict):
            # Handle operators like $in, $nin, $eq, etc.
            for op, op_value in value.items():
                if op in {"$in", "$nin"}:
                    assert isinstance(op_value, (list, tuple)), (
                        f"Expected a list or tuple for {op} operator but got: {type(op_value)}"
                    )
                    field_filters.append(
                        f'<str>json_get(.metadata, "{field}") {FILTER_OPS[op]} array_unpack({op_value})'
                    )

                elif op in {
                    "$eq",
                    "$ne",
                    "$lt",
                    "$lte",
                    "$gt",
                    "$gte",
                    "$like",
                    "$ilike",
                }:
                    formatted_value = (
                        f'"{op_value}"' if isinstance(op_value, str) else str(op_value)
                    )
                    field_filters.append(
                        f'<str>json_get(.metadata, "{field}") {FILTER_OPS[op]} {formatted_value}'
                    )

                elif op == "$between":
                    raise NotImplementedError(f"Operator {op} is not implemented")

                else:
                    assert not op.startswith("$"), f"Unsupported operator: {op}"
        else:
            # Simple equality case
            formatted_value = f'"{value}"' if isinstance(value, str) else str(value)
            field_filters.append(
                f'<str>json_get(.metadata, "{field}") = {formatted_value}'
            )

    if not field_filters:
        raise ValueError(f"Invalid filter format: {filter}")

    # If there are multiple field filters, combine them with "and"
    if len(field_filters) > 1:
        return f"({' and '.join(field_filters)})"
    return field_filters[0]


class GelVectorStore(VectorStore):
    def __init__(
        self,
        embeddings: Embeddings,
        collection_name: str = "default",
        record_type: str = "Record",
    ):
        self._embeddings = embeddings
        self.collection_name = collection_name
        self.record_type = record_type

        self._sync_client = None
        self._async_client = None

    def get_sync_client(self):
        if self._async_client is not None:
            raise RuntimeError("GelVectorStore has already been used in async mode. "
                               "If you were intentionally trying to use different IO modes at the same time, "
                               "please create a new instance instead.")
        if self._sync_client is None:
            self._sync_client = gel.create_client()

            try:
                self._sync_client.ensure_connected()
            except gel.errors.ClientConnectionError as e:
                logger.error(NO_PROJECT_MESSAGE)
                raise e

            try:
                self._sync_client.query(f"select {self.record_type};")
            except gel.errors.InvalidReferenceError as e:
                logger.error(
                    Template(MISSING_RECORD_TYPE_TEMPLATE).render(record_type=self.record_type)
                )
                raise e

        return self._sync_client

    async def get_async_client(self):
        if self._sync_client is not None:
            raise RuntimeError("GelVectorStore has already been used in sync mode. "
                               "If you were intentionally trying to use different IO modes at the same time, "
                               "please create a new instance instead.")
        if self._async_client is None:
            self._async_client = gel.create_async_client()

            try:
                await self._async_client.ensure_connected()
            except gel.errors.ClientConnectionError as e:
                logger.error(NO_PROJECT_MESSAGE)
                raise e

            try:
                await self._async_client.query(f"select {self.record_type};")
            except gel.errors.InvalidReferenceError as e:
                logger.error(
                    Template(MISSING_RECORD_TYPE_TEMPLATE).render(record_type=self.record_type)
                )
                raise e

        return self._async_client

    @property
    def embeddings(self) -> Optional[Embeddings]:
        """Access the query embedding object if available."""
        return self._embeddings

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[list[dict]] = None,
        *,
        ids: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> list[str]:
        """Run more texts through the embeddings and add to the vectorstore.

        Args:
            texts: Iterable of strings to add to the vectorstore.
            metadatas: Optional list of metadatas associated with the texts.
            ids: Optional list of IDs associated with the texts.
            **kwargs: vectorstore specific parameters.
                One of the kwargs should be `ids` which is a list of ids
                associated with the texts.

        Returns:
            List of ids from adding the texts into the vectorstore.

        Raises:
            ValueError: If the number of metadatas does not match the number of texts.
            ValueError: If the number of ids does not match the number of texts.
        """

        client = self.get_sync_client()

        texts_: Sequence[str] = (
            texts if isinstance(texts, (list, tuple)) else list(texts)
        )
        if metadatas and len(metadatas) != len(texts_):
            msg = (
                "The number of metadatas must match the number of texts."
                f"Got {len(metadatas)} metadatas and {len(texts_)} texts."
            )
            raise ValueError(msg)
        metadatas_ = iter(metadatas) if metadatas else cycle([{}])

        if ids:
            ids_ = [id_ or str(uuid.uuid4()) for id_ in ids]
        else:
            ids_ = [str(uuid.uuid4()) for _ in texts_]

        inserted_ids = []
        for text, metadata_, id_ in zip(texts, metadatas_, ids_):
            embedding = self.embeddings.embed_query(text)
            result = client.query(
                INSERT_QUERY.render(record_type=self.record_type),
                collection_name=self.collection_name,
                external_id=id_,
                text=text,
                embedding=embedding,
                metadata=json.dumps(metadata_),
            )
            inserted_ids.append(result[0].external_id)

        return inserted_ids

    async def aadd_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[list[dict]] = None,
        *,
        ids: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> list[str]:
        client = await self.get_async_client()

        texts_: Sequence[str] = (
            texts if isinstance(texts, (list, tuple)) else list(texts)
        )
        if metadatas and len(metadatas) != len(texts_):
            msg = (
                "The number of metadatas must match the number of texts."
                f"Got {len(metadatas)} metadatas and {len(texts_)} texts."
            )
            raise ValueError(msg)
        metadatas_ = iter(metadatas) if metadatas else cycle([{}])

        if ids:
            ids_ = [id_ or str(uuid.uuid4()) for id_ in ids]
        else:
            ids_ = [str(uuid.uuid4()) for _ in texts_]

        inserted_ids = []
        for text, metadata_, id_ in zip(texts, metadatas_, ids_):
            embedding = await self.embeddings.aembed_query(text)
            result = await client.query(
                INSERT_QUERY.render(record_type=self.record_type),
                collection_name=self.collection_name,
                external_id=id_,
                text=text,
                embedding=embedding,
                metadata=json.dumps(metadata_),
            )
            inserted_ids.append(result[0].external_id)

        return inserted_ids

    def delete(self, ids: Optional[list[str]] = None, **kwargs: Any) -> Optional[bool]:
        """Delete by vector ID or other criteria.

        Args:
            ids: List of ids to delete. If None, delete all. Default is None.
            **kwargs: Other keyword arguments that subclasses might use.

        Returns:
            Optional[bool]: True if deletion is successful,
            False otherwise, None if not implemented.
        """
        client = self.get_sync_client()

        if ids:
            result = client.query(
                DELETE_BY_IDS_QUERY.render(record_type=self.record_type),
                collection_name=self.collection_name,
                external_ids=ids,
            )
        else:
            result = client.query(
                DELETE_ALL_QUERY.render(record_type=self.record_type),
                collection_name=self.collection_name,
            )

    async def adelete(
        self, ids: Optional[list[str]] = None, **kwargs: Any
    ) -> Optional[bool]:
        client = await self.get_async_client()

        if ids:
            result = await client.query(
                DELETE_BY_IDS_QUERY.render(record_type=self.record_type),
                collection_name=self.collection_name,
                external_ids=ids,
            )
        else:
            result = await client.query(
                DELETE_ALL_QUERY.render(record_type=self.record_type),
                collection_name=self.collection_name,
            )

    def get_by_ids(self, ids: Sequence[str]) -> list[Document]:
        """Get documents by their IDs.

        The returned documents are expected to have the ID field set to the ID of the
        document in the vector store.

        Fewer documents may be returned than requested if some IDs are not found or
        if there are duplicated IDs.

        Users should not assume that the order of the returned documents matches
        the order of the input IDs. Instead, users should rely on the ID field of the
        returned documents.

        This method should **NOT** raise exceptions if no documents are found for
        some IDs.

        Args:
            ids: List of ids to retrieve.

        Returns:
            List of Documents.

        .. versionadded:: 0.2.11
        """
        client = self.get_sync_client()

        results = client.query(
            SELECT_BY_DOC_ID_QUERY.render(record_type=self.record_type),
            external_ids=ids,
        )
        documents = [
            Document(
                id=result.external_id,
                page_content=result.text,
                metadata=json.loads(result.metadata),
            )
            for result in results
        ]

        return sorted(documents, key=lambda x: ids.index(x.id))

    async def aget_by_ids(self, ids: Sequence[str]) -> list[Document]:
        client = await self.get_async_client()

        results = await client.query(
            SELECT_BY_DOC_ID_QUERY.render(record_type=self.record_type),
            external_ids=ids,
        )
        documents = [
            Document(
                id=result.external_id,
                page_content=result.text,
                metadata=json.loads(result.metadata),
            )
            for result in results
        ]

        return sorted(documents, key=lambda x: ids.index(x.id))

    def _search(
        self,
        embedding: list[float],
        k: int = 4,
        filter: Optional[dict] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        filter_clause = "filter " + filter_to_edgeql(filter) if filter else ""

        client = self.get_sync_client()

        results = client.query(
            COSINE_SIMILARITY_QUERY.render(
                record_type=self.record_type, filter_clause=filter_clause
            ),
            query_embedding=embedding,
            collection_name=self.collection_name,
            limit=k,
        )
        return results

    async def _asearch(
        self,
        embedding: list[float],
        k: int = 4,
        filter: Optional[dict] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        filter_clause = "filter " + filter_to_edgeql(filter) if filter else ""

        client = await self.get_async_client()

        results = await client.query(
            COSINE_SIMILARITY_QUERY.render(
                record_type=self.record_type, filter_clause=filter_clause
            ),
            query_embedding=embedding,
            collection_name=self.collection_name,
            limit=k,
        )
        return results

    def similarity_search(
        self, query: str, k: int = 4, filter: Optional[dict] = None, **kwargs: Any
    ) -> list[Document]:
        """Return docs most similar to query.

        Args:
            query: Input text.
            k: Number of Documents to return. Defaults to 4.
            **kwargs: Arguments to pass to the search method.

        Returns:
            List of Documents most similar to the query.
        """
        query_embedding = self.embeddings.embed_query(query)
        results = self._search(query_embedding, k, filter)
        return [
            Document(
                id=result.external_id,
                page_content=result.text,
                metadata=json.loads(result.metadata),
            )
            for result in results
        ]

    async def asimilarity_search(
        self, query: str, k: int = 4, filter: Optional[dict] = None, **kwargs: Any
    ) -> list[Document]:
        query_embedding = await self.embeddings.aembed_query(query)
        results = await self._asearch(query_embedding, k, filter)
        return [
            Document(
                id=result.external_id,
                page_content=result.text,
                metadata=json.loads(result.metadata),
            )
            for result in results
        ]

    def similarity_search_with_score(
        self, query: str, k: int = 4, filter: Optional[dict] = None, **kwargs: Any
    ) -> list[tuple[Document, float]]:
        """Run similarity search with distance.

        Args:
            *args: Arguments to pass to the search method.
            **kwargs: Arguments to pass to the search method.

        Returns:
            List of Tuples of (doc, similarity_score).
        """
        query_embedding = self.embeddings.embed_query(query)
        results = self._search(query_embedding, k, filter)
        return [
            (
                Document(
                    id=result.external_id,
                    page_content=result.text,
                    metadata=json.loads(result.metadata),
                ),
                result.cosine_similarity,
            )
            for result in results
        ]

    async def asimilarity_search_with_score(
        self, query: str, k: int = 4, filter: Optional[dict] = None, **kwargs: Any
    ) -> list[tuple[Document, float]]:
        query_embedding = await self.embeddings.aembed_query(query)
        results = await self._asearch(query_embedding, k, filter)
        return [
            (
                Document(
                    id=result.external_id,
                    page_content=result.text,
                    metadata=json.loads(result.metadata),
                ),
                result.cosine_similarity,
            )
            for result in results
        ]

    def similarity_search_by_vector(
        self,
        embedding: list[float],
        k: int = 4,
        filter: Optional[dict] = None,
    ) -> list[Document]:
        """Return docs most similar to embedding vector.

        Args:
            embedding: Embedding to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            **kwargs: Arguments to pass to the search method.

        Returns:
            List of Documents most similar to the query vector.
        """
        results = self._search(embedding, k, filter)
        return [
            Document(
                id=result.external_id,
                page_content=result.text,
                metadata=json.loads(result.metadata),
            )
            for result in results
        ]

    async def asimilarity_search_by_vector(
        self,
        embedding: list[float],
        k: int = 4,
        filter: Optional[dict] = None,
    ) -> list[Document]:
        results = await self._asearch(embedding, k, filter)
        return [
            Document(
                id=result.external_id,
                page_content=result.text,
                metadata=json.loads(result.metadata),
            )
            for result in results
        ]

    @classmethod
    def from_texts(
        cls,
        texts: list[str],
        embedding: Embeddings,
        metadatas: Optional[list[dict]] = None,
        *,
        ids: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> "GelVectorStore":
        """Return VectorStore initialized from texts and embeddings.

        Args:
            texts: Texts to add to the vectorstore.
            embedding: Embedding function to use.
            metadatas: Optional list of metadatas associated with the texts.
                Default is None.
            ids: Optional list of IDs associated with the texts.
            kwargs: Additional keyword arguments.

        Returns:
            VectorStore: VectorStore initialized from texts and embeddings.
        """
        store = cls(embedding)
        store.add_texts(texts, metadatas, ids=ids)
        return store

    @classmethod
    async def afrom_texts(
        cls,
        texts: list[str],
        embedding: Embeddings,
        metadatas: Optional[list[dict]] = None,
        *,
        ids: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> "GelVectorStore":
        store = cls(embedding, use_async=True)
        await store.aadd_texts(texts, metadatas, ids=ids)
        return store
