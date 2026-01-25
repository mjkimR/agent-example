from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.base.models import Base, UUIDMixin, TimestampMixin


class UserProfileModel(Base, UUIDMixin, TimestampMixin):
    """User profile table."""

    __tablename__ = "user_profile"

    native_language: Mapped[str] = mapped_column(String(50), default="Korean")
    target_language: Mapped[str] = mapped_column(String(50), default="English")
    proficiency_level: Mapped[str] = mapped_column(String(10), default="B1")
    interests: Mapped[list] = mapped_column(JSON, default=list)

