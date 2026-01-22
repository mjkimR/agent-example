"""User profile service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.base.services.basic import (
    BasicCreateServiceMixin,
    BasicGetServiceMixin,
    BasicGetMultiServiceMixin,
    BasicUpdateServiceMixin,
    BasicDeleteServiceMixin,
)
from app.features.user_profile.models import UserProfileModel
from app.features.user_profile.repos import UserProfileRepository
from app.features.user_profile.schemas import UserProfileCreate, UserProfileUpdate


class UserProfileService(
    BasicCreateServiceMixin[UserProfileRepository, UserProfileModel, UserProfileCreate],
    BasicGetServiceMixin[UserProfileRepository, UserProfileModel],
    BasicGetMultiServiceMixin[UserProfileRepository, UserProfileModel],
    BasicUpdateServiceMixin[UserProfileRepository, UserProfileModel, UserProfileUpdate],
    BasicDeleteServiceMixin[UserProfileRepository, UserProfileModel],
):
    """Service for user profile operations."""

    def __init__(self):
        self.repo = UserProfileRepository()

    async def get_or_create(self, session: AsyncSession) -> UserProfileModel:
        """Get existing profile or create default one."""
        return await self.repo.get_or_create(session)

