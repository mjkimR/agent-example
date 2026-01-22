"""Session model."""

import datetime
from typing import Optional

from sqlalchemy import String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.base.models import Base, UUIDMixin


class SessionModel(Base, UUIDMixin):
    """Sessions table."""

    __tablename__ = "sessions"

    session_type: Mapped[str] = mapped_column(String(50), index=True)
    started_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now
    )
    ended_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    logs: Mapped[list] = mapped_column(JSON, default=list)

