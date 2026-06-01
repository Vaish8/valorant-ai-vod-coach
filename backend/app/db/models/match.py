from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    map_name: Mapped[str] = mapped_column(String(100), nullable=False)
    player_agent: Mapped[str] = mapped_column(String(100), nullable=False)
    rank: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    vod_file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    video_duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    video_fps: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    video_resolution: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

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

    rounds = relationship(
        "Round",
        back_populates="match",
        cascade="all, delete-orphan",
    )

    analysis_findings = relationship(
        "AnalysisFinding",
        back_populates="match",
        cascade="all, delete-orphan",
    )