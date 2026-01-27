from typing import Annotated

from fastapi import Depends

from app.base.usecases.base import BaseUseCase
from app.base.usecases.crud import (
    BaseGetUseCase,
    BaseGetMultiUseCase,
    BaseCreateUseCase,
    BaseUpdateUseCase,
    BaseDeleteUseCase,
)
from app.core.database.transaction import AsyncTransaction
from app.features.user_profile.models import UserProfileModel
from app.features.user_profile.schemas import UserProfileCreate, UserProfileUpdate
from app.features.user_profile.services import UserProfileService, UserProfileContextKwargs


class GetUserProfileUseCase(BaseGetUseCase[UserProfileService, UserProfileModel, UserProfileContextKwargs]):
    def __init__(self, service: Annotated[UserProfileService, Depends()]):
        super().__init__(service)


class GetUserProfileListUseCase(BaseGetMultiUseCase[UserProfileService, UserProfileModel, UserProfileContextKwargs]):
    def __init__(self, service: Annotated[UserProfileService, Depends()]):
        super().__init__(service)


class CreateUserProfileUseCase(BaseCreateUseCase[UserProfileService, UserProfileModel, UserProfileCreate, UserProfileContextKwargs]):
    def __init__(self, service: Annotated[UserProfileService, Depends()]):
        super().__init__(service)


class UpdateUserProfileUseCase(BaseUpdateUseCase[UserProfileService, UserProfileModel, UserProfileUpdate, UserProfileContextKwargs]):
    def __init__(self, service: Annotated[UserProfileService, Depends()]):
        super().__init__(service)


class DeleteUserProfileUseCase(BaseDeleteUseCase[UserProfileService, UserProfileModel, UserProfileContextKwargs]):
    def __init__(self, service: Annotated[UserProfileService, Depends()]):
        super().__init__(service)


class GetOrCreateUserProfileUseCase(BaseUseCase):
    """Use case for getting or creating the user profile."""

    def __init__(self, service: Annotated[UserProfileService, Depends()]):
        self.service = service

    async def execute(self) -> UserProfileModel:
        async with AsyncTransaction() as session:
            return await self.service.get_or_create(session)
