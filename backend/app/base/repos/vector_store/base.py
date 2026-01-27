from typing import Annotated

from fastapi import Depends

from app.base.repos.vector_store import VectorStorePort, get_vector_store


class BaseVectorStoreRepository:
    def __init__(
            self,
            vector_store: Annotated[VectorStorePort, Depends(get_vector_store)]
    ):
        self.vector_store = vector_store
