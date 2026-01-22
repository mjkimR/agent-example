"""Mistake repository."""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.repos import BaseRepository
from app.features.mistake.models import MistakeModel
from app.features.mistake.schemas import MistakeCreate, MistakeUpdate


class MistakeRepository(BaseRepository[MistakeModel, MistakeCreate, MistakeUpdate]):
    """Repository for mistake operations."""

    model = MistakeModel
    default_order_by_col = "timestamp"

    async def get_by_error_type(
        self, session: AsyncSession, error_type: str
    ) -> Sequence[MistakeModel]:
        """Get mistakes by error type."""
        stmt = (
            select(self.model)
            .where(self.model.error_type == error_type)
            .order_by(self.model.timestamp.desc())
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_recent(
        self, session: AsyncSession, limit: int = 10
    ) -> Sequence[MistakeModel]:
        """Get recent mistakes."""
        stmt = (
            select(self.model)
            .order_by(self.model.timestamp.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_by_vocabulary_id(
        self, session: AsyncSession, vocabulary_id
    ) -> Sequence[MistakeModel]:
        """Get mistakes related to a vocabulary item."""
        stmt = (
            select(self.model)
            .where(self.model.vocabulary_id == vocabulary_id)
            .order_by(self.model.timestamp.desc())
        )
        result = await session.execute(stmt)
        return result.scalars().all()

