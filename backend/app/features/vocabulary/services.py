from typing import Annotated
from fastapi import Depends

from app.base.services.base import (
    BaseCreateServiceMixin, BaseGetServiceMixin, BaseGetMultiServiceMixin,
    BaseUpdateServiceMixin, BaseDeleteServiceMixin
)
from app.base.services.exists_check_hook import ExistsCheckHooksMixin
from app.base.services.nested_resource_hook import NestedResourceHooksMixin, NestedResourceContextKwargs
from app.features.vocabulary.models import VocabularyModel
from app.features.vocabulary.repos import VocabularyRepository
from app.features.vocabulary.schemas import VocabularyCreate, VocabularyUpdate
from app.features.user_profile.repos import UserProfileRepository


class VocabularyContextKwargs(NestedResourceContextKwargs):
    pass


class VocabularyService(
    NestedResourceHooksMixin,
    ExistsCheckHooksMixin,
    BaseCreateServiceMixin[VocabularyRepository, VocabularyModel, VocabularyCreate, VocabularyContextKwargs],
    BaseGetMultiServiceMixin[VocabularyRepository, VocabularyModel, VocabularyContextKwargs],
    BaseGetServiceMixin[VocabularyRepository, VocabularyModel, VocabularyContextKwargs],
    BaseUpdateServiceMixin[VocabularyRepository, VocabularyModel, VocabularyUpdate, VocabularyContextKwargs],
    BaseDeleteServiceMixin[VocabularyRepository, VocabularyModel, VocabularyContextKwargs],
):
    context_model = VocabularyContextKwargs
    fk_name = "user_profile_id"

    def __init__(
            self,
            repo: Annotated[VocabularyRepository, Depends()],
            parent_repo: Annotated[UserProfileRepository, Depends()],
    ):
        self._repo = repo
        self._parent_repo = parent_repo

    @property
    def repo(self) -> VocabularyRepository:
        return self._repo

    @property
    def parent_repo(self) -> UserProfileRepository:
        return self._parent_repo
