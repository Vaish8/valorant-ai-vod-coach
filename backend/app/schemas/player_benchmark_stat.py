from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PlayerBenchmarkStatResponse(BaseModel):
    id: int
    tournament: str | None
    stage: str | None
    match_type: str | None
    player: str
    teams: str | None
    agents: str | None
    rounds_played: int | None
    rating: float | None
    acs: float | None
    kd_ratio: float | None
    kast_percent: float | None
    adr: float | None
    kpr: float | None
    apr: float | None
    fkpr: float | None
    fdpr: float | None
    hs_percent: float | None
    clutch_success_percent: float | None
    kills: int | None
    deaths: int | None
    assists: int | None
    first_kills: int | None
    first_deaths: int | None
    imported_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BenchmarkImportResponse(BaseModel):
    imported_rows: int
    skipped_rows: int
    message: str