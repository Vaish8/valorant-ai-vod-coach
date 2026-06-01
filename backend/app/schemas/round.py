from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.enums import RoundResult, RoundSide


class RoundCreate(BaseModel):
    round_number: int = Field(..., ge=1, le=30)
    side: RoundSide
    round_result: RoundResult
    spike_planted: bool = False
    site: Optional[str] = Field(default=None, max_length=10)
    start_time_seconds: Optional[int] = Field(default=None, ge=0)
    end_time_seconds: Optional[int] = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_round_timestamps(self):
        if (
            self.start_time_seconds is not None
            and self.end_time_seconds is not None
            and self.end_time_seconds < self.start_time_seconds
        ):
            raise ValueError(
                "end_time_seconds must be greater than or equal to start_time_seconds"
            )

        return self


class RoundResponse(BaseModel):
    id: int
    match_id: int
    round_number: int
    side: RoundSide
    round_result: RoundResult
    spike_planted: bool
    site: Optional[str] = None
    start_time_seconds: Optional[int] = None
    end_time_seconds: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)