import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Body, status

from app.base.deps.params.page import PaginationParam
from app.base.exceptions.basic import NotFoundException
from app.base.schemas.paginated import PaginatedList
from app.features.feedback.schemas import FeedbackRead, FeedbackUpdate, FeedbackCreate
from app.features.feedback.usecases.crud import (
    CreateFeedbackUseCase, GetMultiFeedbackUseCase, GetFeedbackUseCase,
    UpdateFeedbackUseCase, DeleteFeedbackUseCase
)

router = APIRouter(
    prefix="/user-profiles/{user_profile_id}/vocabularies",
    tags=["Vocabularies"],
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=FeedbackRead)
async def create_feedback(
        use_case: Annotated[CreateFeedbackUseCase, Depends()],
        user_profile_id: uuid.UUID,
        feedback_in: FeedbackCreate = Body(),
):
    context = {"parent_id": user_profile_id}
    return await use_case.execute(feedback_in, context=context)


@router.get("", response_model=PaginatedList[FeedbackRead])
async def get_vocabularies(
        use_case: Annotated[GetMultiFeedbackUseCase, Depends()],
        user_profile_id: uuid.UUID,
        pagination: PaginationParam,
):
    context = {"parent_id": user_profile_id}
    return await use_case.execute(**pagination, context=context)


@router.get("/{feedback_id}", response_model=FeedbackRead)
async def get_feedback(
        use_case: Annotated[GetFeedbackUseCase, Depends()],
        user_profile_id: uuid.UUID,
        feedback_id: uuid.UUID,
):
    context = {"parent_id": user_profile_id}
    feedback = await use_case.execute(feedback_id, context=context)
    if not feedback:
        raise NotFoundException()
    return feedback


@router.put("/{feedback_id}", response_model=FeedbackRead)
async def update_feedback(
        use_case: Annotated[UpdateFeedbackUseCase, Depends()],
        user_profile_id: uuid.UUID,
        feedback_id: uuid.UUID,
        feedback_in: FeedbackUpdate,
):
    context = {"parent_id": user_profile_id}
    feedback = await use_case.execute(feedback_id, feedback_in, context=context)
    if not feedback:
        raise NotFoundException()
    return feedback


@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feedback(
        use_case: Annotated[DeleteFeedbackUseCase, Depends()],
        user_profile_id: uuid.UUID,
        feedback_id: uuid.UUID,
):
    context = {"parent_id": user_profile_id}
    if not await use_case.execute(feedback_id, context=context):
        raise NotFoundException()
