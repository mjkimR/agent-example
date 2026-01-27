from typing import Annotated
from fastapi import Depends

from app.base.services.base import (
    BaseCreateServiceMixin, BaseGetServiceMixin, BaseGetMultiServiceMixin,
    BaseUpdateServiceMixin, BaseDeleteServiceMixin
)
from app.base.services.exists_check_hook import ExistsCheckHooksMixin
from app.base.services.nested_resource_hook import NestedResourceHooksMixin, NestedResourceContextKwargs
from app.base.repos import VectorStorePort
from app.features.mistake.models import MistakeModel
from app.features.mistake.repos import MistakeRepository
from app.features.mistake.schemas import MistakeCreate, MistakeUpdate
from app.features.user_profile.repos import UserProfileRepository
from app.base.deps import get_vector_store


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
    def __init__(
            self,
            repo: Annotated[MistakeRepository, Depends()],
            parent_repo: Annotated[UserProfileRepository, Depends()],
            vector_store: Annotated[VectorStorePort, Depends(get_vector_store)],
    ):
        self.repo = repo
        self.context_model = MistakeContextKwargs

        self.parent_repo = parent_repo
        self.fk_name = "user_profile_id"
        self.vector_store = vector_store
