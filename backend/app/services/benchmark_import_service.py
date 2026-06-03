import csv
from pathlib import Path

from sqlalchemy.orm import Session

from app.db.models.player_benchmark_stat import PlayerBenchmarkStat


def import_player_benchmark_stats_from_csv(
    db: Session,
    csv_path: str,
) -> dict:
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    imported_rows = 0
    skipped_rows = 0

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                stat = PlayerBenchmarkStat(
                    tournament=_clean_text(row.get("Tournament")),
                    stage=_clean_text(row.get("Stage")),
                    match_type=_clean_text(row.get("Match Type")),
                    player=_required_text(row.get("Player")),
                    teams=_clean_text(row.get("Teams")),
                    agents=_clean_text(row.get("Agents")),
                    rounds_played=_to_int(row.get("Rounds Played")),
                    rating=_to_float(row.get("Rating")),
                    acs=_to_float(row.get("Average Combat Score")),
                    kd_ratio=_to_float(row.get("Kills:Deaths")),
                    kast_percent=_to_percent_float(row.get("Kill, Assist, Trade, Survive %")),
                    adr=_to_float(row.get("Average Damage Per Round")),
                    kpr=_to_float(row.get("Kills Per Round")),
                    apr=_to_float(row.get("Assists Per Round")),
                    fkpr=_to_float(row.get("First Kills Per Round")),
                    fdpr=_to_float(row.get("First Deaths Per Round")),
                    hs_percent=_to_percent_float(row.get("Headshot %")),
                    clutch_success_percent=_to_percent_float(row.get("Clutch Success %")),
                    kills=_to_int(row.get("Kills")),
                    deaths=_to_int(row.get("Deaths")),
                    assists=_to_int(row.get("Assists")),
                    first_kills=_to_int(row.get("First Kills")),
                    first_deaths=_to_int(row.get("First Deaths")),
                )

                db.add(stat)
                imported_rows += 1

            except (ValueError, TypeError):
                skipped_rows += 1

    db.commit()

    return {
        "imported_rows": imported_rows,
        "skipped_rows": skipped_rows,
        "message": "Player benchmark stats import completed.",
    }


def _clean_text(value: str | None) -> str | None:
    if value is None:
        return None

    value = value.strip()

    if not value or value == "-":
        return None

    return value


def _required_text(value: str | None) -> str:
    cleaned = _clean_text(value)

    if cleaned is None:
        raise ValueError("Required text value is missing.")

    return cleaned


def _to_float(value: str | None) -> float | None:
    cleaned = _clean_text(value)

    if cleaned is None:
        return None

    cleaned = cleaned.replace(",", "")

    return float(cleaned)


def _to_percent_float(value: str | None) -> float | None:
    cleaned = _clean_text(value)

    if cleaned is None:
        return None

    cleaned = cleaned.replace("%", "")

    return float(cleaned)


def _to_int(value: str | None) -> int | None:
    cleaned = _clean_text(value)

    if cleaned is None:
        return None

    cleaned = cleaned.replace(",", "")

    return int(float(cleaned))