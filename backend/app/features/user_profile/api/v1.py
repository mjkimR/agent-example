from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, Depends

from app.features.user_profile.schemas import UserProfileCreate, UserProfileUpdate
from app.features.user_profile.usecase import (
    GetUserProfileUseCase,
    GetUserProfileListUseCase,
    CreateUserProfileUseCase,
    UpdateUserProfileUseCase,
    DeleteUserProfileUseCase,
    GetOrCreateUserProfileUseCase,
)

router = APIRouter(prefix="/user-profiles", tags=["user-profiles"])


@router.get("")
async def get_user_profiles(
        use_case: Annotated[GetUserProfileListUseCase, Depends()],
        offset: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
):
    """Get list of user profiles."""
    return await use_case.execute(offset=offset, limit=limit)


@router.get("/me")
async def get_or_create_user_profile(
        use_case: Annotated[GetOrCreateUserProfileUseCase, Depends()],
):
    """Get or create the current user profile (single user system)."""
    return await use_case.execute()


@router.get("/{profile_id}")
async def get_user_profile(
        use_case: Annotated[GetUserProfileUseCase, Depends()],
        profile_id: UUID,
):
    """Get a user profile by ID."""
    return await use_case.execute(profile_id)


@router.post("", status_code=201)
async def create_user_profile(
        use_case: Annotated[CreateUserProfileUseCase, Depends()],
        data: UserProfileCreate,
):
    """Create a new user profile."""
    return await use_case.execute(data)


@router.patch("/{profile_id}")
async def update_user_profile(
        use_case: Annotated[UpdateUserProfileUseCase, Depends()],
        profile_id: UUID,
        data: UserProfileUpdate,
):
    """Update a user profile."""
    return await use_case.execute(profile_id, data)


@router.delete("/{profile_id}", status_code=204)
async def delete_user_profile(
        use_case: Annotated[DeleteUserProfileUseCase, Depends()],
        profile_id: UUID,
):
    """Delete a user profile."""
    await use_case.execute(profile_id)
