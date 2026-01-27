from typing import List, TYPE_CHECKING
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.models.mixin import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.features.vocabulary.models import VocabularyModel
    from app.features.mistake.models import MistakeModel
    from app.features.feedback.models import FeedbackLogModel


class UserProfileModel(Base, UUIDMixin, TimestampMixin):
    """User profile table."""

    __tablename__ = "user_profile"

    native_language: Mapped[str] = mapped_column(String(50), default="Korean")
    target_language: Mapped[str] = mapped_column(String(50), default="English")
    proficiency_level: Mapped[str] = mapped_column(String(10), default="B1")
    interests: Mapped[list] = mapped_column(JSON, default=list)

    # Relationships
    vocabularies: Mapped[List["VocabularyModel"]] = relationship(back_populates="user_profile", cascade="all, delete-orphan")
    mistakes: Mapped[List["MistakeModel"]] = relationship(back_populates="user_profile", cascade="all, delete-orphan")
    feedback_logs: Mapped[List["FeedbackLogModel"]] = relationship(back_populates="profile", cascade="all, delete-orphan")
