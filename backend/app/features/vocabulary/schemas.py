"""Vocabulary schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class VocabularyCreate(BaseModel):
    """Schema for creating a vocabulary item."""

    item: str
    meaning: str
    word_type: str = Field(default="other")
    example_sentence: str | None = None
    mastery_level: int = Field(default=0)
    easiness_factor: float = Field(default=2.5)
    repetition_count: int = Field(default=0)
    interval_days: int = Field(default=0)
    last_reviewed_at: datetime | None = None
    next_review_at: datetime | None = None
    context_history: list[dict[str, Any]] = Field(default_factory=list)


class VocabularyUpdate(BaseModel):
    """Schema for updating a vocabulary item."""

    item: str | None = None
    meaning: str | None = None
    word_type: str | None = None
    example_sentence: str | None = None
    mastery_level: int | None = None
    easiness_factor: float | None = None
    repetition_count: int | None = None
    interval_days: int | None = None
    last_reviewed_at: datetime | None = None
    next_review_at: datetime | None = None
    context_history: list[dict[str, Any]] | None = None

