from typing import Annotated
from fastapi import Depends

from app.features.vocabulary.models import VocabularyModel
from app.features.vocabulary.schemas import VocabularyCreate, VocabularyUpdate
from app.features.vocabulary.services import VocabularyService, VocabularyContextKwargs
from app.base.usecases.crud import (
    BaseGetUseCase,
    BaseGetMultiUseCase,
    BaseCreateUseCase,
    BaseUpdateUseCase,
    BaseDeleteUseCase
)


class GetVocabularyUseCase(BaseGetUseCase[VocabularyService, VocabularyModel, VocabularyContextKwargs]):
    def __init__(self, service: Annotated[VocabularyService, Depends()]) -> None:
        super().__init__(service)


class GetMultiVocabularyUseCase(BaseGetMultiUseCase[VocabularyService, VocabularyModel, VocabularyContextKwargs]):
    def __init__(self, service: Annotated[VocabularyService, Depends()]) -> None:
        super().__init__(service)


class CreateVocabularyUseCase(BaseCreateUseCase[VocabularyService, VocabularyModel, VocabularyCreate, VocabularyContextKwargs]):
    def __init__(self, service: Annotated[VocabularyService, Depends()]) -> None:
        super().__init__(service)


class UpdateVocabularyUseCase(BaseUpdateUseCase[VocabularyService, VocabularyModel, VocabularyUpdate, VocabularyContextKwargs]):
    def __init__(self, service: Annotated[VocabularyService, Depends()]) -> None:
        super().__init__(service)


class DeleteVocabularyUseCase(BaseDeleteUseCase[VocabularyService, VocabularyModel, VocabularyContextKwargs]):
    def __init__(self, service: Annotated[VocabularyService, Depends()]) -> None:
        super().__init__(service)
