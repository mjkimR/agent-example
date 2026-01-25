from datetime import datetime

from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    """Schema for creating a feedback log."""

    feedback_type: str
    content: str
    context: str | None = None
    timestamp: datetime = Field(default_factory=datetime.now)


class FeedbackUpdate(BaseModel):
    """Schema for updating a feedback log."""

    feedback_type: str | None = None
    content: str | None = None
    context: str | None = None

