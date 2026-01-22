"""Session schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    """Schema for creating a session."""

    session_type: str
    started_at: datetime = Field(default_factory=datetime.now)
    ended_at: datetime | None = None
    logs: list[dict[str, Any]] = Field(default_factory=list)


class SessionUpdate(BaseModel):
    """Schema for updating a session."""

    session_type: str | None = None
    ended_at: datetime | None = None
    logs: list[dict[str, Any]] | None = None

