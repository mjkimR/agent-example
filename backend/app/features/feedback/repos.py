"""Feedback repository."""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.repos import BaseRepository
from app.features.feedback.models import FeedbackLogModel
from app.features.feedback.schemas import FeedbackCreate, FeedbackUpdate


class FeedbackRepository(BaseRepository[FeedbackLogModel, FeedbackCreate, FeedbackUpdate]):
    """Repository for feedback log operations."""

    model = FeedbackLogModel
    default_order_by_col = "timestamp"

    async def get_by_type(
        self, session: AsyncSession, feedback_type: str
    ) -> Sequence[FeedbackLogModel]:
        """Get feedback by type."""
        stmt = (
            select(self.model)
            .where(self.model.feedback_type == feedback_type)
            .order_by(self.model.timestamp.desc())
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_recent(
        self, session: AsyncSession, limit: int = 10
    ) -> Sequence[FeedbackLogModel]:
        """Get recent feedback logs."""
        stmt = (
            select(self.model)
            .order_by(self.model.timestamp.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

