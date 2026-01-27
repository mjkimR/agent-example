from typing import Annotated
from fastapi import Depends

from app.features.mistake.models import MistakeModel
from app.features.mistake.schemas import MistakeCreate, MistakeUpdate
from app.features.mistake.services import MistakeService, MistakeContextKwargs
from app.base.usecases.crud import (
    BaseGetUseCase,
    BaseGetMultiUseCase,
    BaseCreateUseCase,
    BaseUpdateUseCase,
    BaseDeleteUseCase
)


class GetMistakeUseCase(BaseGetUseCase[MistakeService, MistakeModel, MistakeContextKwargs]):
    def __init__(self, service: Annotated[MistakeService, Depends()]) -> None:
        super().__init__(service)


class GetMultiMistakeUseCase(BaseGetMultiUseCase[MistakeService, MistakeModel, MistakeContextKwargs]):
    def __init__(self, service: Annotated[MistakeService, Depends()]) -> None:
        super().__init__(service)


class CreateMistakeUseCase(BaseCreateUseCase[MistakeService, MistakeModel, MistakeCreate, MistakeContextKwargs]):
    def __init__(self, service: Annotated[MistakeService, Depends()]) -> None:
        super().__init__(service)


class UpdateMistakeUseCase(BaseUpdateUseCase[MistakeService, MistakeModel, MistakeUpdate, MistakeContextKwargs]):
    def __init__(self, service: Annotated[MistakeService, Depends()]) -> None:
        super().__init__(service)


class DeleteMistakeUseCase(BaseDeleteUseCase[MistakeService, MistakeModel, MistakeContextKwargs]):
    def __init__(self, service: Annotated[MistakeService, Depends()]) -> None:
        super().__init__(service)
