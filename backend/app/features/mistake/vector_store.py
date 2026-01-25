from typing import Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

from common.config import settings


class VectorStore:
    """ChromaDB vector store manager."""

    def __init__(self, persist_path: str = None):
        self.persist_path = persist_path or str(settings.chroma_path)
        settings.ensure_dirs()

        self.client = chromadb.PersistentClient(
            path=self.persist_path,
            settings=ChromaSettings(anonymized_telemetry=False),
        )

        # Collections
        self._mistakes_collection = None
        self._vocab_context_collection = None

    @property
    def mistakes_collection(self):
        """Get or create mistakes collection for error pattern analysis."""
        if self._mistakes_collection is None:
            self._mistakes_collection = self.client.get_or_create_collection(
                name="mistakes",
                metadata={"description": "Mistake embeddings for pattern analysis"},
            )
        return self._mistakes_collection

    @property
    def vocab_context_collection(self):
        """Get or create vocabulary context collection."""
        if self._vocab_context_collection is None:
            self._vocab_context_collection = self.client.get_or_create_collection(
                name="vocab_contexts",
                metadata={"description": "Vocabulary usage context embeddings"},
            )
        return self._vocab_context_collection

    def add_mistake(
        self,
        mistake_id: int,
        text: str,
        embedding: list[float],
        error_type: str,
        metadata: Optional[dict] = None,
    ) -> None:
        """Add a mistake embedding for pattern analysis."""
        doc_metadata = {"error_type": error_type}
        if metadata:
            doc_metadata.update(metadata)

        self.mistakes_collection.add(
            ids=[str(mistake_id)],
            embeddings=[embedding],
            documents=[text],
            metadatas=[doc_metadata],
        )

    def find_similar_mistakes(
        self,
        embedding: list[float],
        n_results: int = 5,
        error_type_filter: Optional[str] = None,
    ) -> list[dict]:
        """Find similar mistakes by embedding."""
        where_filter = {"error_type": error_type_filter} if error_type_filter else None

        results = self.mistakes_collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        similar = []
        if results["ids"] and results["ids"][0]:
            for i, id_ in enumerate(results["ids"][0]):
                similar.append({
                    "id": int(id_),
                    "document": results["documents"][0][i] if results["documents"] else None,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else None,
                    "distance": results["distances"][0][i] if results["distances"] else None,
                })
        return similar

    def add_vocab_context(
        self,
        vocab_id: int,
        context_index: int,
        text: str,
        embedding: list[float],
        metadata: Optional[dict] = None,
    ) -> None:
        """Add a vocabulary context embedding."""
        doc_id = f"{vocab_id}_{context_index}"
        doc_metadata = {"vocab_id": vocab_id}
        if metadata:
            doc_metadata.update(metadata)

        self.vocab_context_collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[doc_metadata],
        )

    def find_similar_contexts(
        self,
        embedding: list[float],
        n_results: int = 5,
    ) -> list[dict]:
        """Find similar vocabulary contexts by embedding."""
        results = self.vocab_context_collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        similar = []
        if results["ids"] and results["ids"][0]:
            for i, id_ in enumerate(results["ids"][0]):
                similar.append({
                    "id": id_,
                    "document": results["documents"][0][i] if results["documents"] else None,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else None,
                    "distance": results["distances"][0][i] if results["distances"] else None,
                })
        return similar

    def delete_mistake(self, mistake_id: int) -> None:
        """Delete a mistake embedding."""
        self.mistakes_collection.delete(ids=[str(mistake_id)])

    def delete_vocab_contexts(self, vocab_id: int) -> None:
        """Delete all context embeddings for a vocabulary item."""
        # Get all contexts for this vocab
        results = self.vocab_context_collection.get(
            where={"vocab_id": vocab_id},
            include=[],
        )
        if results["ids"]:
            self.vocab_context_collection.delete(ids=results["ids"])
