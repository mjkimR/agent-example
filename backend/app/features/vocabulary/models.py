"""Vocabulary model."""

import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Text, Integer, Float, DateTime, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.models import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.features.mistake.models import MistakeModel


class VocabularyModel(Base, UUIDMixin, TimestampMixin):
    """Vocabulary table."""

    __tablename__ = "vocabulary"

    item: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    meaning: Mapped[str] = mapped_column(Text)
    word_type: Mapped[str] = mapped_column(String(50), default="other")
    example_sentence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # SM-2 SRS fields
    mastery_level: Mapped[int] = mapped_column(Integer, default=0)
    easiness_factor: Mapped[float] = mapped_column(Float, default=2.5)
    repetition_count: Mapped[int] = mapped_column(Integer, default=0)
    interval_days: Mapped[int] = mapped_column(Integer, default=0)

    last_reviewed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    next_review_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

    context_history: Mapped[list] = mapped_column(JSON, default=list)

    # Relationships
    mistakes: Mapped[list["MistakeModel"]] = relationship(back_populates="vocabulary")

    __table_args__ = (
        Index("idx_vocabulary_mastery", "mastery_level"),
    )

