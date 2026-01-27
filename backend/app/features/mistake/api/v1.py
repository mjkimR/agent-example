import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Body, status

from app.base.deps.params.page import PaginationParam
from app.base.exceptions.basic import NotFoundException
from app.base.schemas.paginated import PaginatedList
from app.features.mistake.schemas import MistakeRead, MistakeUpdate, MistakeCreate
from app.features.mistake.usecases.crud import (
    CreateMistakeUseCase, GetMultiMistakeUseCase, GetMistakeUseCase,
    UpdateMistakeUseCase, DeleteMistakeUseCase
)

router = APIRouter(
    prefix="/user-profiles/{user_profile_id}/vocabularies",
    tags=["Vocabularies"],
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=MistakeRead)
async def create_mistake(
        use_case: Annotated[CreateMistakeUseCase, Depends()],
        user_profile_id: uuid.UUID,
        mistake_in: MistakeCreate = Body(),
):
    context = {"parent_id": user_profile_id}
    return await use_case.execute(mistake_in, context=context)


@router.get("", response_model=PaginatedList[MistakeRead])
async def get_vocabularies(
        use_case: Annotated[GetMultiMistakeUseCase, Depends()],
        user_profile_id: uuid.UUID,
        pagination: PaginationParam,
):
    context = {"parent_id": user_profile_id}
    return await use_case.execute(**pagination, context=context)


@router.get("/{mistake_id}", response_model=MistakeRead)
async def get_mistake(
        use_case: Annotated[GetMistakeUseCase, Depends()],
        user_profile_id: uuid.UUID,
        mistake_id: uuid.UUID,
):
    context = {"parent_id": user_profile_id}
    mistake = await use_case.execute(mistake_id, context=context)
    if not mistake:
        raise NotFoundException()
    return mistake


@router.put("/{mistake_id}", response_model=MistakeRead)
async def update_mistake(
        use_case: Annotated[UpdateMistakeUseCase, Depends()],
        user_profile_id: uuid.UUID,
        mistake_id: uuid.UUID,
        mistake_in: MistakeUpdate,
):
    context = {"parent_id": user_profile_id}
    mistake = await use_case.execute(mistake_id, mistake_in, context=context)
    if not mistake:
        raise NotFoundException()
    return mistake


@router.delete("/{mistake_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mistake(
        use_case: Annotated[DeleteMistakeUseCase, Depends()],
        user_profile_id: uuid.UUID,
        mistake_id: uuid.UUID,
):
    context = {"parent_id": user_profile_id}
    if not await use_case.execute(mistake_id, context=context):
        raise NotFoundException()
