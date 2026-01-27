import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.base.schemas.mixin import UUIDSchemaMixin, TimestampSchemaMixin


class MistakeCreate(BaseModel):
    """Schema for creating a mistake record."""

    original_sentence: str
    corrected_sentence: str
    error_type: str
    explanation: str | None = None
    vocabulary_id: uuid.UUID | None = None
    timestamp: datetime = Field(default_factory=datetime.now)


class MistakeUpdate(BaseModel):
    """Schema for updating a mistake record."""

    original_sentence: str | None = None
    corrected_sentence: str | None = None
    error_type: str | None = None
    explanation: str | None = None
    vocabulary_id: uuid.UUID | None = None


class MistakeRead(UUIDSchemaMixin, TimestampSchemaMixin, BaseModel):
    """Schema for reading a mistake record."""

    feedback_type: str
    content: str
    context: str | None = None

    class Config:
        orm_mode = True
