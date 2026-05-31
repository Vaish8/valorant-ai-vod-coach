from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.event import Event
from app.db.models.match import Match
from app.db.models.round import Round
from app.services.statistics_service import calculate_match_statistics


def analyze_match(db: Session, match_id: int) -> dict | None:
    match = db.get(Match, match_id)

    if match is None:
        return None

    statistics = calculate_match_statistics(db=db, match_id=match_id)

    if statistics is None:
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

    findings = []

    findings.extend(_detect_repeated_first_deaths(statistics))
    findings.extend(_detect_post_plant_issues(rounds))
    findings.extend(_detect_utility_unused_in_lost_rounds(rounds, events))
    findings.extend(_detect_low_trade_support(statistics))
    findings.extend(_detect_low_round_conversion(statistics))

    return {
        "match_id": match_id,
        "total_findings": len(findings),
        "findings": findings,
    }


def _detect_repeated_first_deaths(statistics: dict) -> list[dict]:
    first_death_count = statistics["first_death_count"]

    if first_death_count >= 3:
        return [
            {
                "issue_type": "repeated_first_deaths",
                "severity": "high",
                "finding": f"Player or team recorded {first_death_count} first-death events.",
                "evidence": (
                    f"The match contains {first_death_count} first_death events. "
                    "Repeated first deaths often create early 4v5 disadvantages."
                ),
                "recommendation": (
                    "Avoid taking isolated early duels. Use teammate utility, request trade support, "
                    "or delay first contact until the team is ready to follow up."
                ),
                "confidence": 0.9,
                "round_id": None,
            }
        ]

    if first_death_count == 2:
        return [
            {
                "issue_type": "early_round_risk",
                "severity": "medium",
                "finding": "Multiple first-death events were detected.",
                "evidence": "The match contains 2 first_death events.",
                "recommendation": (
                    "Review early-round positioning and avoid dry peeking common angles without support."
                ),
                "confidence": 0.75,
                "round_id": None,
            }
        ]

    return []


def _detect_post_plant_issues(rounds: list[Round]) -> list[dict]:
    findings = []

    for round_obj in rounds:
        if round_obj.spike_planted and round_obj.round_result.lower() == "lost":
            findings.append(
                {
                    "issue_type": "post_plant_conversion_issue",
                    "severity": "high",
                    "finding": f"Round {round_obj.round_number} was lost after the spike was planted.",
                    "evidence": (
                        f"Round {round_obj.round_number} has spike_planted=true "
                        "and round_result=lost."
                    ),
                    "recommendation": (
                        "Review post-plant positioning, crossfire setup, utility usage, and whether "
                        "players over-peeked instead of playing time."
                    ),
                    "confidence": 0.85,
                    "round_id": round_obj.id,
                }
            )

    return findings


def _detect_utility_unused_in_lost_rounds(
    rounds: list[Round],
    events: list[Event],
) -> list[dict]:
    findings = []

    round_by_id = {round_obj.id: round_obj for round_obj in rounds}

    for event in events:
        if event.event_type != "utility_unused":
            continue

        round_obj = round_by_id.get(event.round_id)

        if round_obj is None:
            continue

        if round_obj.round_result.lower() == "lost":
            findings.append(
                {
                    "issue_type": "utility_unused_in_lost_round",
                    "severity": "medium",
                    "finding": (
                        f"Utility was unused in lost round {round_obj.round_number}."
                    ),
                    "evidence": (
                        f"Event '{event.event_type}' occurred in round {round_obj.round_number}: "
                        f"{event.description or 'No description provided.'}"
                    ),
                    "recommendation": (
                        "Review whether key utility could have been used before contact, during site "
                        "execution, or during retake/post-plant situations."
                    ),
                    "confidence": event.confidence,
                    "round_id": round_obj.id,
                }
            )

    return findings


def _detect_low_trade_support(statistics: dict) -> list[dict]:
    first_death_count = statistics["first_death_count"]
    trade_kill_count = statistics["trade_kill_count"]

    if first_death_count >= 2 and trade_kill_count == 0:
        return [
            {
                "issue_type": "low_trade_support",
                "severity": "high",
                "finding": "First deaths occurred without any recorded trade kills.",
                "evidence": (
                    f"The match contains {first_death_count} first_death events and "
                    f"{trade_kill_count} trade_kill events."
                ),
                "recommendation": (
                    "Improve spacing and trade positioning. If a player takes first contact, "
                    "a teammate should be close enough to punish the opponent."
                ),
                "confidence": 0.85,
                "round_id": None,
            }
        ]

    if first_death_count > trade_kill_count:
        return [
            {
                "issue_type": "possible_trade_support_gap",
                "severity": "medium",
                "finding": "First deaths outnumber trade kills.",
                "evidence": (
                    f"The match contains {first_death_count} first_death events and "
                    f"{trade_kill_count} trade_kill events."
                ),
                "recommendation": (
                    "Review rounds where first contact occurred and check whether teammates were "
                    "close enough to trade."
                ),
                "confidence": 0.7,
                "round_id": None,
            }
        ]

    return []


def _detect_low_round_conversion(statistics: dict) -> list[dict]:
    total_rounds = statistics["total_rounds"]
    overall_win_rate = statistics["overall_win_rate"]

    if total_rounds >= 5 and overall_win_rate <= 0.25:
        return [
            {
                "issue_type": "low_round_conversion",
                "severity": "high",
                "finding": "The match had a low round conversion rate.",
                "evidence": (
                    f"Overall win rate was {overall_win_rate} across {total_rounds} rounds."
                ),
                "recommendation": (
                    "Review repeated round-loss patterns, including first deaths, post-plant losses, "
                    "utility usage, and whether the team is converting advantages."
                ),
                "confidence": 0.8,
                "round_id": None,
            }
        ]

    return []