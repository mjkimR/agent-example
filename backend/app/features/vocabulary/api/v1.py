import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Body, status

from app.base.deps.params.page import PaginationParam
from app.base.exceptions.basic import NotFoundException
from app.base.schemas.paginated import PaginatedList
from app.features.vocabulary.schemas import VocabularyRead, VocabularyUpdate, VocabularyCreate
from app.features.vocabulary.usecases.crud import (
    CreateVocabularyUseCase, GetMultiVocabularyUseCase, GetVocabularyUseCase,
    UpdateVocabularyUseCase, DeleteVocabularyUseCase
)

router = APIRouter(
    prefix="/user-profiles/{user_profile_id}/vocabularies",
    tags=["Vocabularies"],
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=VocabularyRead)
async def create_vocabulary(
        use_case: Annotated[CreateVocabularyUseCase, Depends()],
        user_profile_id: uuid.UUID,
        vocabulary_in: VocabularyCreate = Body(),
):
    context = {"parent_id": user_profile_id}
    return await use_case.execute(vocabulary_in, context=context)


@router.get("", response_model=PaginatedList[VocabularyRead])
async def get_vocabularies(
        use_case: Annotated[GetMultiVocabularyUseCase, Depends()],
        user_profile_id: uuid.UUID,
        pagination: PaginationParam,
):
    context = {"parent_id": user_profile_id}
    return await use_case.execute(**pagination, context=context)


@router.get("/{vocabulary_id}", response_model=VocabularyRead)
async def get_vocabulary(
        use_case: Annotated[GetVocabularyUseCase, Depends()],
        user_profile_id: uuid.UUID,
        vocabulary_id: uuid.UUID,
):
    context = {"parent_id": user_profile_id}
    vocabulary = await use_case.execute(vocabulary_id, context=context)
    if not vocabulary:
        raise NotFoundException()
    return vocabulary


@router.put("/{vocabulary_id}", response_model=VocabularyRead)
async def update_vocabulary(
        use_case: Annotated[UpdateVocabularyUseCase, Depends()],
        user_profile_id: uuid.UUID,
        vocabulary_id: uuid.UUID,
        vocabulary_in: VocabularyUpdate,
):
    context = {"parent_id": user_profile_id}
    vocabulary = await use_case.execute(vocabulary_id, vocabulary_in, context=context)
    if not vocabulary:
        raise NotFoundException()
    return vocabulary


@router.delete("/{vocabulary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vocabulary(
        use_case: Annotated[DeleteVocabularyUseCase, Depends()],
        user_profile_id: uuid.UUID,
        vocabulary_id: uuid.UUID,
):
    context = {"parent_id": user_profile_id}
    if not await use_case.execute(vocabulary_id, context=context):
        raise NotFoundException()
