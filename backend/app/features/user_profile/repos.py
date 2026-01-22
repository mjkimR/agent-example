"""User profile repository."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.repos import BaseRepository
from app.features.user_profile.models import UserProfileModel
from app.features.user_profile.schemas import UserProfileCreate, UserProfileUpdate


class UserProfileRepository(BaseRepository[UserProfileModel, UserProfileCreate, UserProfileUpdate]):
    """Repository for user profile operations."""

    model = UserProfileModel
    default_order_by_col = "created_at"

    async def get_first(self, session: AsyncSession) -> Optional[UserProfileModel]:
        """Get the first user profile (single user system)."""
        stmt = select(self.model).limit(1)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_or_create(self, session: AsyncSession) -> UserProfileModel:
        """Get existing profile or create default one."""
        profile = await self.get_first(session)
        if profile:
            return profile

        # Create default profile
        default_profile = UserProfileCreate()
        return await self.create(session, default_profile)
