from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.repos.base import BaseRepository
from app.features.vocabulary.models import VocabularyModel
from app.features.vocabulary.schemas import VocabularyCreate, VocabularyUpdate


class VocabularyRepository(BaseRepository[VocabularyModel, VocabularyCreate, VocabularyUpdate]):
    """Repository for vocabulary operations."""

    model = VocabularyModel
    default_order_by_col = "created_at"

    async def get_by_item(self, session: AsyncSession, item: str) -> VocabularyModel | None:
        """Get vocabulary by word/phrase."""
        stmt = select(self.model).where(self.model.item == item)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_due_for_review(self, session: AsyncSession, limit: int = 20) -> Sequence[VocabularyModel]:
        """Get vocabulary items due for review."""
        now = datetime.now(timezone.utc)
        stmt = (
            select(self.model)
            .where(
                or_(
                    self.model.next_review_at.is_(None),
                    self.model.next_review_at <= now
                )
            )
            .order_by(self.model.next_review_at.asc().nullsfirst())
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def search(self, session: AsyncSession, query: str) -> Sequence[VocabularyModel]:
        """Search vocabulary by item or meaning."""
        stmt = (
            select(self.model)
            .where(
                or_(
                    self.model.item.contains(query),
                    self.model.meaning.contains(query)
                )
            )
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_by_mastery_level(
        self, session: AsyncSession, mastery_level: int
    ) -> Sequence[VocabularyModel]:
        """Get vocabulary items by mastery level."""
        stmt = select(self.model).where(self.model.mastery_level == mastery_level)
        result = await session.execute(stmt)
        return result.scalars().all()

