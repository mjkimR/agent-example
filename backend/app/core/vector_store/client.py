from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.vectorstores import VectorStore

from app.base.ai_models.factory import AIModelFactory
from app.base.ai_models.schemas import AIModelType

"""
Draft code for vector store retrieval.

TODO:
get_vector_store_client -> lifespan or singleton / dependency injection
get_vector_store -> make class for caching via collection_name + embedding_model (small maxsize: 4-8)
"""


def get_vector_store_client():
    client = QdrantClient(":memory:")
    return client


def get_vector_store(collection_name: str, embedding_model: str) -> VectorStore:
    client = get_vector_store_client()
    embeddings = AIModelFactory().get_model(
        embedding_model, model_type=AIModelType.EMBEDDING
    )
    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )
