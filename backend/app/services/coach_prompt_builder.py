from sqlalchemy.orm import Session

from app.db.models.match import Match
from app.services.analysis_service import get_saved_analysis_findings
from app.services.statistics_service import calculate_match_statistics


def build_coach_prompt(
    db: Session,
    match_id: int,
) -> dict | None:
    match = db.get(Match, match_id)

    if match is None:
        return None

    statistics = calculate_match_statistics(db=db, match_id=match_id)
    saved_analysis = get_saved_analysis_findings(db=db, match_id=match_id)

    if statistics is None or saved_analysis is None:
        return None

    findings = saved_analysis["findings"]

    prompt = _build_prompt_text(
        match=match,
        statistics=statistics,
        findings=findings,
    )

    return {
        "match_id": match_id,
        "prompt_type": "evidence_grounded_coaching_prompt",
        "prompt": prompt,
    }


def _build_prompt_text(
    match: Match,
    statistics: dict,
    findings: list,
) -> str:
    findings_text = _format_findings(findings)

    return f"""
You are an expert Valorant coach and esports analyst.

Your task is to generate a coaching summary for a player based ONLY on the structured evidence provided below.

Do not invent facts.
Do not assume events that are not present.
Do not mention video details unless they are explicitly provided.
If evidence is limited, clearly say that the analysis is based on available structured events only.

MATCH CONTEXT
- Match ID: {match.id}
- Title: {match.title}
- Map: {match.map_name}
- Player Agent: {match.player_agent}
- Rank: {match.rank or "Unknown"}

MATCH STATISTICS
- Total rounds tracked: {statistics["total_rounds"]}
- Rounds won: {statistics["rounds_won"]}
- Rounds lost: {statistics["rounds_lost"]}
- Overall win rate: {statistics["overall_win_rate"]}
- Attack rounds: {statistics["attack_rounds"]}
- Defense rounds: {statistics["defense_rounds"]}
- Attack win rate: {statistics["attack_win_rate"]}
- Defense win rate: {statistics["defense_win_rate"]}
- Spike plants: {statistics["spike_plants"]}
- Post-plant losses: {statistics["post_plant_losses"]}
- Total gameplay events: {statistics["total_events"]}
- First-death events: {statistics["first_death_count"]}
- Utility-unused events: {statistics["utility_unused_count"]}
- Trade-kill events: {statistics["trade_kill_count"]}

TACTICAL FINDINGS
{findings_text}

OUTPUT REQUIREMENTS
Write the coaching response using this structure:

1. Overall Match Summary
   - 3 to 5 sentences explaining the main performance pattern.

2. Top 3 Issues
   - List the top issues based on the evidence.
   - For each issue, include the evidence that supports it.

3. Practical Improvement Plan
   - Give specific practice actions the player can take.
   - Avoid generic advice like "play better" or "improve positioning" unless supported by evidence.

4. Confidence and Limitations
   - Explain what the system can confidently say.
   - Mention any limits caused by missing video data or manually entered events.

STYLE
- Be direct, practical, and coach-like.
- Use simple language.
- Do not be motivational or vague.
- Ground every claim in the evidence above.
""".strip()


def _format_findings(findings: list) -> str:
    if not findings:
        return (
            "- No saved tactical findings were available. "
            "The coaching summary should state that more structured event data is needed."
        )

    formatted_findings = []

    for index, finding in enumerate(findings, start=1):
        formatted_findings.append(
            "\n".join(
                [
                    f"{index}. Issue Type: {finding.issue_type}",
                    f"   Severity: {finding.severity}",
                    f"   Finding: {finding.finding}",
                    f"   Evidence: {finding.evidence}",
                    f"   Recommendation: {finding.recommendation}",
                    f"   Confidence: {finding.confidence}",
                    f"   Round ID: {finding.round_id if finding.round_id is not None else 'Match-level'}",
                ]
            )
        )

    return "\n\n".join(formatted_findings)