import datetime
import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.models import Base, UUIDMixin

if TYPE_CHECKING:
    from app.features.vocabulary.models import VocabularyModel


class MistakeModel(Base, UUIDMixin):
    """Mistakes table."""

    __tablename__ = "mistakes"

    original_sentence: Mapped[str] = mapped_column(Text)
    corrected_sentence: Mapped[str] = mapped_column(Text)
    error_type: Mapped[str] = mapped_column(String(100), index=True)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    vocabulary_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("vocabulary.id"), nullable=True
    )
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now
    )

    # Relationships
    vocabulary: Mapped[Optional["VocabularyModel"]] = relationship(back_populates="mistakes")
