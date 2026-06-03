from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.player_benchmark_stat import PlayerBenchmarkStat
from app.db.session import get_db
from app.schemas.player_benchmark_stat import BenchmarkImportResponse
from app.services.benchmark_import_service import (
    import_player_benchmark_stats_from_csv,
)

router = APIRouter(prefix="/benchmarks", tags=["Benchmarks"])


@router.post(
    "/import-player-stats",
    response_model=BenchmarkImportResponse,
)
def import_player_stats(
    db: Session = Depends(get_db),
):
    project_root = Path(__file__).resolve().parents[4]
    csv_path = project_root / "sample_data" / "benchmarks" / "players_stats.csv"

    try:
        result = import_player_benchmark_stats_from_csv(
            db=db,
            csv_path=str(csv_path),
        )
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return result


@router.get("/player-stats/count")
def get_player_stats_count(
    db: Session = Depends(get_db),
):
    statement = select(func.count()).select_from(PlayerBenchmarkStat)
    count = db.scalar(statement)

    return {
        "total_rows": count,
    }