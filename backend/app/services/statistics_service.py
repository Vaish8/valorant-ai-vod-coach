from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.event import Event
from app.db.models.match import Match
from app.db.models.round import Round


def _safe_rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0

    return round(numerator / denominator, 2)


def calculate_match_statistics(db: Session, match_id: int) -> dict | None:
    match = db.get(Match, match_id)

    if match is None:
        return None

    rounds_statement = (
        select(Round)
        .where(Round.match_id == match_id)
        .order_by(Round.round_number.asc())
    )
    rounds = list(db.scalars(rounds_statement).all())

    round_ids = [round_obj.id for round_obj in rounds]

    if round_ids:
        events_statement = (
            select(Event)
            .where(Event.round_id.in_(round_ids))
            .order_by(Event.timestamp_seconds.asc())
        )
        events = list(db.scalars(events_statement).all())
    else:
        events = []

    total_rounds = len(rounds)

    rounds_won = sum(
        1 for round_obj in rounds
        if round_obj.round_result.lower() == "won"
    )

    rounds_lost = sum(
        1 for round_obj in rounds
        if round_obj.round_result.lower() == "lost"
    )

    attack_rounds = [
        round_obj for round_obj in rounds
        if round_obj.side.lower() == "attack"
    ]

    defense_rounds = [
        round_obj for round_obj in rounds
        if round_obj.side.lower() == "defense"
    ]

    attack_rounds_won = sum(
        1 for round_obj in attack_rounds
        if round_obj.round_result.lower() == "won"
    )

    defense_rounds_won = sum(
        1 for round_obj in defense_rounds
        if round_obj.round_result.lower() == "won"
    )

    spike_plants = sum(
        1 for round_obj in rounds
        if round_obj.spike_planted
    )

    post_plant_losses = sum(
        1 for round_obj in rounds
        if round_obj.spike_planted and round_obj.round_result.lower() == "lost"
    )

    event_counter = Counter(event.event_type for event in events)
    event_counts_by_type = dict(event_counter)

    first_death_count = event_counts_by_type.get("first_death", 0)
    utility_unused_count = event_counts_by_type.get("utility_unused", 0)
    trade_kill_count = event_counts_by_type.get("trade_kill", 0)

    return {
        "match_id": match_id,
        "total_rounds": total_rounds,
        "rounds_won": rounds_won,
        "rounds_lost": rounds_lost,
        "attack_rounds": len(attack_rounds),
        "defense_rounds": len(defense_rounds),
        "attack_rounds_won": attack_rounds_won,
        "defense_rounds_won": defense_rounds_won,
        "attack_win_rate": _safe_rate(attack_rounds_won, len(attack_rounds)),
        "defense_win_rate": _safe_rate(defense_rounds_won, len(defense_rounds)),
        "overall_win_rate": _safe_rate(rounds_won, total_rounds),
        "spike_plants": spike_plants,
        "post_plant_losses": post_plant_losses,
        "total_events": len(events),
        "event_counts_by_type": event_counts_by_type,
        "first_death_count": first_death_count,
        "utility_unused_count": utility_unused_count,
        "trade_kill_count": trade_kill_count,
    }