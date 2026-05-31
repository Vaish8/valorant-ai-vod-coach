from typing import List, Optional

from pydantic import BaseModel, Field


class AnalysisFinding(BaseModel):
    issue_type: str
    severity: str
    finding: str
    evidence: str
    recommendation: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    round_id: Optional[int] = None


class MatchAnalysisResponse(BaseModel):
    match_id: int
    total_findings: int
    findings: List[AnalysisFinding]