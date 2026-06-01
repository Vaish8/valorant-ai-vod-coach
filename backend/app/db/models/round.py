from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Round(Base):
    __tablename__ = "rounds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    round_number: Mapped[int] = mapped_column(Integer, nullable=False)
    side: Mapped[str] = mapped_column(String(20), nullable=False)
    round_result: Mapped[str] = mapped_column(String(20), nullable=False)

    spike_planted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    site: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    start_time_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    end_time_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    match = relationship("Match", back_populates="rounds")
    events = relationship(
        "Event",
        back_populates="round",
        cascade="all, delete-orphan",
    )