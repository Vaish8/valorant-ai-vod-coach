from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PlayerBenchmarkStat(Base):
    __tablename__ = "player_benchmark_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    tournament: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stage: Mapped[str | None] = mapped_column(String(255), nullable=True)
    match_type: Mapped[str | None] = mapped_column(String(100), nullable=True)

    player: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    teams: Mapped[str | None] = mapped_column(String(255), nullable=True)
    agents: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    rounds_played: Mapped[int | None] = mapped_column(Integer, nullable=True)

    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    acs: Mapped[float | None] = mapped_column(Float, nullable=True)
    kd_ratio: Mapped[float | None] = mapped_column(Float, nullable=True)
    kast_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    adr: Mapped[float | None] = mapped_column(Float, nullable=True)
    kpr: Mapped[float | None] = mapped_column(Float, nullable=True)
    apr: Mapped[float | None] = mapped_column(Float, nullable=True)
    fkpr: Mapped[float | None] = mapped_column(Float, nullable=True)
    fdpr: Mapped[float | None] = mapped_column(Float, nullable=True)
    hs_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    clutch_success_percent: Mapped[float | None] = mapped_column(Float, nullable=True)

    kills: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deaths: Mapped[int | None] = mapped_column(Integer, nullable=True)
    assists: Mapped[int | None] = mapped_column(Integer, nullable=True)
    first_kills: Mapped[int | None] = mapped_column(Integer, nullable=True)
    first_deaths: Mapped[int | None] = mapped_column(Integer, nullable=True)

    imported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )