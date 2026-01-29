from abc import abstractmethod

from langchain_core.vectorstores import VectorStore
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.repos.base import CreateSchemaType
from app.base.services.base import BaseCreateHooks, BaseUpdateHooks, BaseDeleteHooks, TContextKwargs


class VectorStoreHookMixin(
    BaseCreateHooks,
    BaseUpdateHooks,
    BaseDeleteHooks,
):
    @property
    @abstractmethod
    def vector_store(self) -> VectorStore:
        """Vector store instance associated with the service."""
        pass

    async def _context_create(self, session: AsyncSession, obj_data: CreateSchemaType, context: TContextKwargs):
        async with super()._context_create(session, obj_data, context):
            # Vector store 생성 로직 추가 가능
            yield


class SearchServiceMixin:
    pass
