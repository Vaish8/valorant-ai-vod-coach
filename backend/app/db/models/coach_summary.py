from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CoachSummary(Base):
    __tablename__ = "coach_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True,
    )

    overall_summary: Mapped[str] = mapped_column(Text, nullable=False)
    primary_issue: Mapped[str] = mapped_column(String(100), nullable=False)
    key_evidence: Mapped[str] = mapped_column(Text, nullable=False)
    practice_recommendation: Mapped[str] = mapped_column(Text, nullable=False)

    source: Mapped[str] = mapped_column(
        String(50),
        default="mock_coach",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    match = relationship("Match", back_populates="coach_summary")