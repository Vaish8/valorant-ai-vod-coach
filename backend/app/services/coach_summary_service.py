from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.analysis_finding import AnalysisFinding
from app.db.models.coach_summary import CoachSummary
from app.db.models.match import Match
from app.services.analysis_service import get_saved_analysis_findings
from app.services.statistics_service import calculate_match_statistics


def generate_and_save_coach_summary(
    db: Session,
    match_id: int,
) -> CoachSummary | None:
    match = db.get(Match, match_id)

    if match is None:
        return None

    statistics = calculate_match_statistics(db=db, match_id=match_id)
    saved_analysis = get_saved_analysis_findings(db=db, match_id=match_id)

    if statistics is None or saved_analysis is None:
        return None

    findings = list(saved_analysis["findings"])

    if not findings:
        overall_summary = (
            "No major tactical issues were detected from the currently saved analysis findings. "
            "Add more structured round and event data, then run analysis again for better coaching output."
        )
        primary_issue = "insufficient_evidence"
        key_evidence = "No saved tactical findings were available for this match."
        practice_recommendation = (
            "Record more structured events such as first deaths, utility usage, trades, spike plants, "
            "and post-plant outcomes before generating a coaching summary."
        )
    else:
        highest_priority_finding = _select_highest_priority_finding(findings)

        overall_summary = _build_overall_summary(
            statistics=statistics,
            findings=findings,
            highest_priority_finding=highest_priority_finding,
        )

        primary_issue = highest_priority_finding.issue_type
        key_evidence = highest_priority_finding.evidence
        practice_recommendation = highest_priority_finding.recommendation

    existing_summary = _get_existing_summary(db=db, match_id=match_id)

    if existing_summary is not None:
        existing_summary.overall_summary = overall_summary
        existing_summary.primary_issue = primary_issue
        existing_summary.key_evidence = key_evidence
        existing_summary.practice_recommendation = practice_recommendation
        existing_summary.source = "mock_coach"

        db.commit()
        db.refresh(existing_summary)

        return existing_summary

    summary = CoachSummary(
        match_id=match_id,
        overall_summary=overall_summary,
        primary_issue=primary_issue,
        key_evidence=key_evidence,
        practice_recommendation=practice_recommendation,
        source="mock_coach",
    )

    db.add(summary)
    db.commit()
    db.refresh(summary)

    return summary


def get_coach_summary(
    db: Session,
    match_id: int,
) -> CoachSummary | None:
    match = db.get(Match, match_id)

    if match is None:
        return None

    return _get_existing_summary(db=db, match_id=match_id)


def _get_existing_summary(
    db: Session,
    match_id: int,
) -> CoachSummary | None:
    statement = select(CoachSummary).where(CoachSummary.match_id == match_id)
    return db.scalars(statement).first()


def _select_highest_priority_finding(
    findings: list[AnalysisFinding],
) -> AnalysisFinding:
    severity_priority = {
        "high": 3,
        "medium": 2,
        "low": 1,
    }

    return max(
        findings,
        key=lambda finding: (
            severity_priority.get(finding.severity, 0),
            finding.confidence,
        ),
    )


def _build_overall_summary(
    statistics: dict,
    findings: list[AnalysisFinding],
    highest_priority_finding: AnalysisFinding,
) -> str:
    total_rounds = statistics["total_rounds"]
    overall_win_rate = statistics["overall_win_rate"]
    first_death_count = statistics["first_death_count"]
    utility_unused_count = statistics["utility_unused_count"]
    trade_kill_count = statistics["trade_kill_count"]
    post_plant_losses = statistics["post_plant_losses"]

    return (
        f"This match contains {len(findings)} tactical findings across {total_rounds} tracked rounds. "
        f"The overall round win rate was {overall_win_rate}. "
        f"The most important issue detected was '{highest_priority_finding.issue_type}', supported by this evidence: "
        f"{highest_priority_finding.evidence} "
        f"Key supporting metrics include {first_death_count} first-death events, "
        f"{utility_unused_count} utility-unused events, {trade_kill_count} trade-kill events, "
        f"and {post_plant_losses} post-plant losses. "
        f"The immediate coaching focus should be: {highest_priority_finding.recommendation}"
    )