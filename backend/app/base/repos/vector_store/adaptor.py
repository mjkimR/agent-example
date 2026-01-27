from abc import ABC, abstractmethod
from typing import Optional, Any

from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection
from pydantic import BaseModel, Field
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import get_app_settings


class VectorDBContext(BaseModel):
    """Context for vector database operations."""

    db_name: str = Field(description="Database name for the vector store.")
    field_name: Optional[str] = Field(description="Field name associated with the embeddings.")
    partition_key: Optional[str] = Field(default=None, description="Partition key for the collection.")
    collection_keys: Optional[dict[str, Any]] = Field(default=None, description="Keys used for generating collection names.")
    meta: Optional[dict[str, Any]] = Field(default=None, description="Additional metadata for the context.")


class EmbeddingVector(BaseModel):
    """Model for embedding vectors with optional metadata."""
    field: str = Field(description="Field name for the embedding.")
    embedding: list[float] = Field(description="The embedding vector.")


class EmbeddingItem(BaseModel):
    """Base model for embedding items."""
    id: str
    text: Optional[str] = None
    embedding: list[EmbeddingVector]
    metadata: Optional[dict] = None


class SimilarResult(BaseModel):
    page_content: Optional[str] = None
    metadata: Optional[dict] = None
    id: Optional[str] = None
    distance: Optional[float] = None


class VectorStorePort(ABC):
    """Vector store port interface."""

    @abstractmethod
    def add_item(self, ctx: VectorDBContext, item: EmbeddingItem) -> None:
        pass

    @abstractmethod
    def add_items(self, ctx: VectorDBContext, items: list[EmbeddingItem]) -> None:
        pass

    @abstractmethod
    def find_similar_items(
            self,
            ctx: VectorDBContext,
            embedding: list[float],
            n_results: int = 5,
            where_filter: Optional[dict] = None,
    ) -> list[SimilarResult]:
        pass

    @abstractmethod
    def delete_item(
            self,
            ctx: VectorDBContext,
            item_id: str,
            collection: str
    ) -> None:
        pass

    @abstractmethod
    def delete_items_by_metadata(
            self,
            ctx: VectorDBContext,
            collection: str,
            where: dict
    ) -> None:
        pass

class ChromaContext(VectorDBContext):
    """ChromaDB specific context."""
    pass


class ChromaVectorAdapter(VectorStorePort):
    """ChromaDB vector store adapter."""

    # Class-level caches for clients and collections by persist_path
    _clients: dict[str, ClientAPI] = {}
    _collections_cache: dict[str, dict[str, Collection]] = {}

    def __init__(self, persist_path: str = None):
        app_settings = get_app_settings()
        self.persist_path = persist_path or str(app_settings.chroma_path)

        # Get or create client for this path
        if self.persist_path not in self.__class__._clients:
            self.__class__._clients[self.persist_path] = chromadb.PersistentClient(
                path=self.persist_path,
                settings=ChromaSettings(anonymized_telemetry=False),
            )
        self.client = self.__class__._clients[self.persist_path]

        # Ensure collections cache for this path exists
        if self.persist_path not in self.__class__._collections_cache:
            self.__class__._collections_cache[self.persist_path] = {}

    def _get_collection(self, ctx: VectorDBContext) -> Collection:
        """Get or create collection."""
        name = self.get_collection_name(ctx)
        if name not in self.__class__._collections_cache[self.persist_path]:
            self.__class__._collections_cache[self.persist_path][name] = self.client.get_or_create_collection(
                name=name,
                metadata={"description": f"Embeddings for {name}"},
            )
        return self.__class__._collections_cache[self.persist_path][name]

    def get_collection_name(self, ctx: VectorDBContext) -> str:
        if ctx.partition_key:
            raise ValueError("ChromaVectorAdapter does not support partition_key in collection names.")
        if not ctx.field_name:
            raise ValueError("field_name is required in VectorDBContext for collection naming.")
        data = [ctx.db_name, ctx.field_name]
        if ctx.collection_keys:
            for key in sorted(ctx.collection_keys.keys()):
                data.append(str(ctx.collection_keys[key]))
        return "_".join(data)

    def add_item(self, ctx: VectorDBContext, item: EmbeddingItem) -> None:
        """Add an embedding item."""
        for embed_vector in item.embedding:
            collection = self._get_collection(ctx)
            collection.add(
                ids=[item.id],
                embeddings=[embed_vector.embedding],
                documents=[item.text],
                metadatas=[item.metadata or {}],
            )

    def add_items(self, ctx: VectorDBContext, items: list[EmbeddingItem]) -> None:
        """Add multiple embedding items.

        TODO: Batch size control
        """
        if not items:
            return
        embeddings = {}
        raise NotImplementedError
        # collection_name = items[0].collection
        # collection = self._get_collection(collection_name)
        # ids = [item.id for item in items]
        # embeddings = [item.embedding for item in items]
        # documents = [item.text for item in items]
        # metadatas = [item.metadata or {} for item in items]
        # collection.add(
        #     ids=ids,
        #     embeddings=embeddings,
        #     documents=documents,
        #     metadatas=metadatas,
        # )

    def find_similar_items(
            self,
            ctx: VectorDBContext,
            embedding: list[float],
            n_results: int = 5,
            where_filter: Optional[dict] = None,
    ) -> list[SimilarResult]:
        """Find similar items by embedding."""
        coll = self._get_collection(ctx)
        results = coll.query(
            query_embeddings=[embedding],
            n_results=n_results,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        similar = []
        if results["ids"] and results["ids"][0]:
            for i, id_ in enumerate(results["ids"][0]):
                similar.append(SimilarResult(
                    id=id_,
                    page_content=results["documents"][0][i] if results["documents"] else None,
                    metadata=results["metadatas"][0][i] if results["metadatas"] else None,
                    distance=results["distances"][0][i] if results["distances"] else None,
                ))
        return similar

    def delete_item(self, ctx: VectorDBContext, item_id: str, collection: str) -> None:
        """Delete an embedding item."""
        coll = self._get_collection(ctx)
        coll.delete(ids=[item_id])

    def delete_items_by_metadata(self, ctx: VectorDBContext, collection: str, where: dict) -> None:
        """Delete items by metadata filter."""
        coll = self._get_collection(ctx)
        results = coll.get(where=where, include=[])
        if results["ids"]:
            coll.delete(ids=results["ids"])
