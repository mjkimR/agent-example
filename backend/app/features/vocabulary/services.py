from typing import Annotated
from fastapi import Depends

from app.base.services.base import (
    BaseCreateServiceMixin, BaseGetServiceMixin, BaseGetMultiServiceMixin,
    BaseUpdateServiceMixin, BaseDeleteServiceMixin
)
from app.base.services.exists_check_hook import ExistsCheckHooksMixin
from app.base.services.nested_resource_hook import NestedResourceHooksMixin, NestedResourceContextKwargs
from app.base.repos import VectorStorePort
from app.features.vocabulary.models import VocabularyModel
from app.features.vocabulary.repos import VocabularyRepository
from app.features.vocabulary.schemas import VocabularyCreate, VocabularyUpdate
from app.features.user_profile.repos import UserProfileRepository
from app.base.deps import get_vector_store


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
    def __init__(
            self,
            repo: Annotated[VocabularyRepository, Depends()],
            parent_repo: Annotated[UserProfileRepository, Depends()],
            vector_store: Annotated[VectorStorePort, Depends(get_vector_store)],
    ):
        self.repo = repo
        self.context_model = VocabularyContextKwargs

        self.parent_repo = parent_repo
        self.fk_name = "user_profile_id"
        self.vector_store = vector_store
