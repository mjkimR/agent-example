from typing import Annotated
from fastapi import Depends

from app.features.feedback.models import FeedbackLogModel
from app.features.feedback.schemas import FeedbackCreate, FeedbackUpdate
from app.features.feedback.services import FeedbackService, FeedbackContextKwargs
from app.base.usecases.crud import (
    BaseGetUseCase,
    BaseGetMultiUseCase,
    BaseCreateUseCase,
    BaseUpdateUseCase,
    BaseDeleteUseCase
)


class GetFeedbackUseCase(BaseGetUseCase[FeedbackService, FeedbackLogModel, FeedbackContextKwargs]):
    def __init__(self, service: Annotated[FeedbackService, Depends()]) -> None:
        super().__init__(service)


class GetMultiFeedbackUseCase(BaseGetMultiUseCase[FeedbackService, FeedbackLogModel, FeedbackContextKwargs]):
    def __init__(self, service: Annotated[FeedbackService, Depends()]) -> None:
        super().__init__(service)


class CreateFeedbackUseCase(BaseCreateUseCase[FeedbackService, FeedbackLogModel, FeedbackCreate, FeedbackContextKwargs]):
    def __init__(self, service: Annotated[FeedbackService, Depends()]) -> None:
        super().__init__(service)


class UpdateFeedbackUseCase(BaseUpdateUseCase[FeedbackService, FeedbackLogModel, FeedbackUpdate, FeedbackContextKwargs]):
    def __init__(self, service: Annotated[FeedbackService, Depends()]) -> None:
        super().__init__(service)


class DeleteFeedbackUseCase(BaseDeleteUseCase[FeedbackService, FeedbackLogModel, FeedbackContextKwargs]):
    def __init__(self, service: Annotated[FeedbackService, Depends()]) -> None:
        super().__init__(service)
