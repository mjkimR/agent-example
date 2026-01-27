from typing import Annotated
from fastapi import Depends

from app.base.services.base import (
    BaseCreateServiceMixin, BaseGetServiceMixin, BaseGetMultiServiceMixin,
    BaseUpdateServiceMixin, BaseDeleteServiceMixin
)
from app.base.services.exists_check_hook import ExistsCheckHooksMixin
from app.base.services.nested_resource_hook import NestedResourceHooksMixin, NestedResourceContextKwargs
from app.features.feedback.models import FeedbackLogModel
from app.features.feedback.repos import FeedbackRepository
from app.features.feedback.schemas import FeedbackCreate, FeedbackUpdate
from app.features.user_profile.repos import UserProfileRepository


class FeedbackContextKwargs(NestedResourceContextKwargs):
    pass


class FeedbackService(
    NestedResourceHooksMixin,
    ExistsCheckHooksMixin,
    BaseCreateServiceMixin[FeedbackRepository, FeedbackLogModel, FeedbackCreate, FeedbackContextKwargs],
    BaseGetMultiServiceMixin[FeedbackRepository, FeedbackLogModel, FeedbackContextKwargs],
    BaseGetServiceMixin[FeedbackRepository, FeedbackLogModel, FeedbackContextKwargs],
    BaseUpdateServiceMixin[FeedbackRepository, FeedbackLogModel, FeedbackUpdate, FeedbackContextKwargs],
    BaseDeleteServiceMixin[FeedbackRepository, FeedbackLogModel, FeedbackContextKwargs],
):
    def __init__(
            self,
            repo: Annotated[FeedbackRepository, Depends()],
            parent_repo: Annotated[UserProfileRepository, Depends()]
    ):
        self.repo = repo
        self.context_model = FeedbackContextKwargs

        self.parent_repo = parent_repo
        self.fk_name = "user_profile_id"
