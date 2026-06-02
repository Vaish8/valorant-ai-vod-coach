from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CoachSummaryResponse(BaseModel):
    id: int
    match_id: int
    overall_summary: str
    primary_issue: str
    key_evidence: str
    practice_recommendation: str
    source: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)