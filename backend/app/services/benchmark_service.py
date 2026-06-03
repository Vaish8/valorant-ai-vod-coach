from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.player_benchmark_stat import PlayerBenchmarkStat


def get_agent_benchmark(
    db: Session,
    agent_name: str,
) -> dict | None:
    normalized_agent = agent_name.strip()

    if not normalized_agent:
        return None

    statement = (
        select(
            func.count(PlayerBenchmarkStat.id).label("sample_size"),
            func.avg(PlayerBenchmarkStat.rating).label("average_rating"),
            func.avg(PlayerBenchmarkStat.acs).label("average_acs"),
            func.avg(PlayerBenchmarkStat.kd_ratio).label("average_kd_ratio"),
            func.avg(PlayerBenchmarkStat.kast_percent).label("average_kast_percent"),
            func.avg(PlayerBenchmarkStat.adr).label("average_adr"),
            func.avg(PlayerBenchmarkStat.kpr).label("average_kpr"),
            func.avg(PlayerBenchmarkStat.apr).label("average_apr"),
            func.avg(PlayerBenchmarkStat.fkpr).label("average_fkpr"),
            func.avg(PlayerBenchmarkStat.fdpr).label("average_fdpr"),
            func.avg(PlayerBenchmarkStat.hs_percent).label("average_hs_percent"),
            func.avg(PlayerBenchmarkStat.clutch_success_percent).label(
                "average_clutch_success_percent"
            ),
        )
        .where(func.lower(PlayerBenchmarkStat.agents) == normalized_agent.lower())
    )

    result = db.execute(statement).mappings().first()

    if result is None:
        return None

    sample_size = result["sample_size"]

    if sample_size == 0:
        return None

    return {
        "agent": normalized_agent,
        "sample_size": sample_size,
        "average_rating": _round_optional(result["average_rating"]),
        "average_acs": _round_optional(result["average_acs"]),
        "average_kd_ratio": _round_optional(result["average_kd_ratio"]),
        "average_kast_percent": _round_optional(result["average_kast_percent"]),
        "average_adr": _round_optional(result["average_adr"]),
        "average_kpr": _round_optional(result["average_kpr"]),
        "average_apr": _round_optional(result["average_apr"]),
        "average_fkpr": _round_optional(result["average_fkpr"]),
        "average_fdpr": _round_optional(result["average_fdpr"]),
        "average_hs_percent": _round_optional(result["average_hs_percent"]),
        "average_clutch_success_percent": _round_optional(
            result["average_clutch_success_percent"]
        ),
    }


def _round_optional(value: float | None) -> float | None:
    if value is None:
        return None

    return round(float(value), 2)