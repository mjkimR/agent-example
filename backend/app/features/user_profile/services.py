from typing import Annotated

from fastapi import Depends
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


class UserProfileContextKwargs(BaseContextKwargs):
    pass


class UserProfileService(
    BaseGetServiceMixin[UserProfileModel, UserProfileRepository, UserProfileContextKwargs],
    BaseGetMultiServiceMixin[UserProfileModel, UserProfileRepository, UserProfileContextKwargs],
    BaseCreateServiceMixin[UserProfileModel, UserProfileRepository, UserProfileCreate, UserProfileContextKwargs],
    BaseUpdateServiceMixin[UserProfileModel, UserProfileRepository, UserProfileUpdate, UserProfileContextKwargs],
    BaseDeleteServiceMixin[UserProfileModel, UserProfileRepository, UserProfileContextKwargs],
):
    """Service for user profile operations."""
    context_model = UserProfileContextKwargs

    def __init__(
            self,
            repo: Annotated[UserProfileRepository, Depends()],
    ):
        self._repo: UserProfileRepository = repo

    @property
    def repo(self) -> UserProfileRepository:
        return self._repo

    async def get_or_create(self, session: AsyncSession) -> UserProfileModel:
        """Get existing profile or create default one."""
        return await self.repo.get_or_create(session)
