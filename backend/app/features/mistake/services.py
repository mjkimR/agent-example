from typing import Annotated
from fastapi import Depends

from app.base.services.base import (
    BaseCreateServiceMixin, BaseGetServiceMixin, BaseGetMultiServiceMixin,
    BaseUpdateServiceMixin, BaseDeleteServiceMixin
)
from app.base.services.exists_check_hook import ExistsCheckHooksMixin
from app.base.services.nested_resource_hook import NestedResourceHooksMixin, NestedResourceContextKwargs
from app.features.mistake.models import MistakeModel
from app.features.mistake.repos import MistakeRepository
from app.features.mistake.schemas import MistakeCreate, MistakeUpdate
from app.features.user_profile.repos import UserProfileRepository


class MistakeContextKwargs(NestedResourceContextKwargs):
    pass


class MistakeService(
    NestedResourceHooksMixin,
    ExistsCheckHooksMixin,
    BaseCreateServiceMixin[MistakeRepository, MistakeModel, MistakeCreate, MistakeContextKwargs],
    BaseGetMultiServiceMixin[MistakeRepository, MistakeModel, MistakeContextKwargs],
    BaseGetServiceMixin[MistakeRepository, MistakeModel, MistakeContextKwargs],
    BaseUpdateServiceMixin[MistakeRepository, MistakeModel, MistakeUpdate, MistakeContextKwargs],
    BaseDeleteServiceMixin[MistakeRepository, MistakeModel, MistakeContextKwargs],
):
    context_model = MistakeContextKwargs
    fk_name = "user_profile_id"

    def __init__(
            self,
            repo: Annotated[MistakeRepository, Depends()],
            parent_repo: Annotated[UserProfileRepository, Depends()],
    ):
        self._repo = repo
        self._parent_repo = parent_repo

    @property
    def repo(self) -> MistakeRepository:
        return self._repo

    @property
    def parent_repo(self) -> UserProfileRepository:
        return self._parent_repo
