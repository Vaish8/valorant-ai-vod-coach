from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RoundCreate(BaseModel):
    round_number: int = Field(..., ge=1, le=30)
    side: str = Field(..., min_length=3, max_length=20)
    round_result: str = Field(..., min_length=3, max_length=20)
    spike_planted: bool = False
    site: Optional[str] = Field(default=None, max_length=10)
    start_time_seconds: Optional[int] = Field(default=None, ge=0)
    end_time_seconds: Optional[int] = Field(default=None, ge=0)


class RoundResponse(BaseModel):
    id: int
    match_id: int
    round_number: int
    side: str
    round_result: str
    spike_planted: bool
    site: Optional[str] = None
    start_time_seconds: Optional[int] = None
    end_time_seconds: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
