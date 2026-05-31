from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models.analysis_finding import AnalysisFinding
from app.db.models.match import Match
from app.services.rule_engine import analyze_match


def run_and_save_analysis(db: Session, match_id: int) -> dict | None:
    match = db.get(Match, match_id)

    if match is None:
        return None

    analysis = analyze_match(db=db, match_id=match_id)

    if analysis is None:
        return None

    # Replace old analysis findings so each analysis run reflects the latest match data.
    delete_statement = delete(AnalysisFinding).where(
        AnalysisFinding.match_id == match_id
    )
    db.execute(delete_statement)

    saved_findings = []

    for finding in analysis["findings"]:
        finding_obj = AnalysisFinding(
            match_id=match_id,
            round_id=finding.get("round_id"),
            issue_type=finding["issue_type"],
            severity=finding["severity"],
            finding=finding["finding"],
            evidence=finding["evidence"],
            recommendation=finding["recommendation"],
            confidence=finding["confidence"],
            source="rule_engine",
        )

        db.add(finding_obj)
        saved_findings.append(finding_obj)

    db.commit()

    for finding_obj in saved_findings:
        db.refresh(finding_obj)

    return {
        "match_id": match_id,
        "total_findings": len(saved_findings),
        "findings": saved_findings,
    }


def get_saved_analysis_findings(
    db: Session,
    match_id: int,
) -> dict | None:
    match = db.get(Match, match_id)

    if match is None:
        return None

    statement = (
        select(AnalysisFinding)
        .where(AnalysisFinding.match_id == match_id)
        .order_by(
            AnalysisFinding.created_at.desc(),
            AnalysisFinding.id.asc(),
        )
    )

    findings: Sequence[AnalysisFinding] = db.scalars(statement).all()

    return {
        "match_id": match_id,
        "total_findings": len(findings),
        "findings": findings,
    }