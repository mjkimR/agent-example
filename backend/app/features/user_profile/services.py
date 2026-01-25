from sqlalchemy.ext.asyncio import AsyncSession

from app.base.services.base import (
    BaseCreateServiceMixin,
    BaseGetServiceMixin,
    BaseGetMultiServiceMixin,
    BaseUpdateServiceMixin,
    BaseDeleteServiceMixin,
    BaseContextKwargs,
)
from app.features.user_profile.models import UserProfileModel
from app.features.user_profile.repos import UserProfileRepository
from app.features.user_profile.schemas import UserProfileCreate, UserProfileUpdate


class UserProfileService(
    BaseGetServiceMixin[UserProfileModel, UserProfileRepository, BaseContextKwargs],
    BaseGetMultiServiceMixin[UserProfileModel, UserProfileRepository, BaseContextKwargs],
    BaseCreateServiceMixin[UserProfileModel, UserProfileRepository, UserProfileCreate, BaseContextKwargs],
    BaseUpdateServiceMixin[UserProfileModel, UserProfileRepository, UserProfileUpdate, BaseContextKwargs],
    BaseDeleteServiceMixin[UserProfileModel, UserProfileRepository, BaseContextKwargs],
):
    """Service for user profile operations."""

    def __init__(self):
        self.repo = UserProfileRepository()

    async def get_or_create(self, session: AsyncSession) -> UserProfileModel:
        """Get existing profile or create default one."""
        return await self.repo.get_or_create(session)

