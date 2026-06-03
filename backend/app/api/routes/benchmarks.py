from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.player_benchmark_stat import PlayerBenchmarkStat
from app.db.session import get_db
from app.schemas.player_benchmark_stat import (
    AgentBenchmarkResponse,
    BenchmarkImportResponse,
)
from app.services.benchmark_import_service import (
    import_player_benchmark_stats_from_csv,
)
from app.services.benchmark_service import get_agent_benchmark

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

@router.get(
    "/agents/{agent_name}",
    response_model=AgentBenchmarkResponse,
)
def get_agent_benchmark_stats(
    agent_name: str,
    db: Session = Depends(get_db),
):
    benchmark = get_agent_benchmark(
        db=db,
        agent_name=agent_name,
    )

    if benchmark is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No benchmark stats found for agent '{agent_name}'",
        )

    return benchmark

@router.delete("/player-stats")
def delete_player_stats(
    db: Session = Depends(get_db),
):
    deleted_rows = db.query(PlayerBenchmarkStat).delete()
    db.commit()

    return {
        "deleted_rows": deleted_rows,
        "message": "Player benchmark stats deleted.",
    }