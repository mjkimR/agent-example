"""User profile CRUD use cases."""

from uuid import UUID
from typing import Optional

from app.base.usecase.base import BaseUseCase
from app.base.usecase.crud import (
    BaseGetUseCase,
    BaseGetMultiUseCase,
    BaseCreateUseCase,
    BaseUpdateUseCase,
    BaseDeleteUseCase,
)
from app.base.schemas.paginated import PaginatedList
from app.core.transaction import AsyncTransaction
from app.features.user_profile.models import UserProfileModel
from app.features.user_profile.schemas import UserProfileCreate, UserProfileUpdate
from app.features.user_profile.services import UserProfileService


class GetUserProfileUseCase(BaseGetUseCase[UserProfileService, UserProfileModel]):
    """Use case for getting a user profile by ID."""

    def __init__(self):
        super().__init__(UserProfileService())


class GetUserProfileListUseCase(BaseGetMultiUseCase[UserProfileService, UserProfileModel]):
    """Use case for getting a list of user profiles."""

    def __init__(self):
        super().__init__(UserProfileService())


class CreateUserProfileUseCase(BaseCreateUseCase[UserProfileService, UserProfileModel, UserProfileCreate]):
    """Use case for creating a user profile."""

    def __init__(self):
        super().__init__(UserProfileService())


class UpdateUserProfileUseCase(BaseUpdateUseCase[UserProfileService, UserProfileModel, UserProfileUpdate]):
    """Use case for updating a user profile."""

    def __init__(self):
        super().__init__(UserProfileService())


class DeleteUserProfileUseCase(BaseDeleteUseCase[UserProfileService, UserProfileModel]):
    """Use case for deleting a user profile."""

    def __init__(self):
        super().__init__(UserProfileService())


class GetOrCreateUserProfileUseCase(BaseUseCase):
    """Use case for getting or creating the user profile."""

    def __init__(self):
        self.service = UserProfileService()

    async def execute(self) -> UserProfileModel:
        async with AsyncTransaction() as session:
            return await self.service.get_or_create(session)

