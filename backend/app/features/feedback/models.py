"""Feedback log model."""

import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.base.models import Base, UUIDMixin


class FeedbackLogModel(Base, UUIDMixin):
    """Feedback logs table."""

    __tablename__ = "feedback_logs"

    feedback_type: Mapped[str] = mapped_column(String(50), index=True)
    content: Mapped[str] = mapped_column(Text)
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now
    )

