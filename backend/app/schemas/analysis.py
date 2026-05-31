from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AnalysisFinding(BaseModel):
    issue_type: str
    severity: str
    finding: str
    evidence: str
    recommendation: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    round_id: Optional[int] = None


class AnalysisFindingResponse(BaseModel):
    id: int
    match_id: int
    round_id: Optional[int] = None
    issue_type: str
    severity: str
    finding: str
    evidence: str
    recommendation: str
    confidence: float
    source: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MatchAnalysisResponse(BaseModel):
    match_id: int
    total_findings: int
    findings: List[AnalysisFinding]


class PersistedMatchAnalysisResponse(BaseModel):
    match_id: int
    total_findings: int
    findings: List[AnalysisFindingResponse]