import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.models.mixin import Base, UUIDMixin

if TYPE_CHECKING:
    from app.features.user_profile.models import UserProfileModel


class FeedbackLogModel(Base, UUIDMixin):
    """Feedback logs table."""

    __tablename__ = "feedback_logs"

    feedback_type: Mapped[str] = mapped_column(String(50), index=True)
    content: Mapped[str] = mapped_column(Text)
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now
    )
    profile_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    profile: Mapped["UserProfileModel"] = relationship(back_populates="feedback_logs")
