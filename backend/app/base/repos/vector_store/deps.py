from app.base.repos import VectorStorePort, ChromaVectorAdapter


def get_vector_store() -> VectorStorePort:
    return ChromaVectorAdapter()
