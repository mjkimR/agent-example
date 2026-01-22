"""Session repository."""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.repos import BaseRepository
from app.features.session.models import SessionModel
from app.features.session.schemas import SessionCreate, SessionUpdate


class SessionRepository(BaseRepository[SessionModel, SessionCreate, SessionUpdate]):
    """Repository for session operations."""

    model = SessionModel
    default_order_by_col = "started_at"

    async def get_by_session_type(
        self, session: AsyncSession, session_type: str
    ) -> Sequence[SessionModel]:
        """Get sessions by type."""
        stmt = (
            select(self.model)
            .where(self.model.session_type == session_type)
            .order_by(self.model.started_at.desc())
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_active_sessions(self, session: AsyncSession) -> Sequence[SessionModel]:
        """Get sessions that haven't ended yet."""
        stmt = (
            select(self.model)
            .where(self.model.ended_at.is_(None))
            .order_by(self.model.started_at.desc())
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_recent(
        self, session: AsyncSession, limit: int = 10
    ) -> Sequence[SessionModel]:
        """Get recent sessions."""
        stmt = (
            select(self.model)
            .order_by(self.model.started_at.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

