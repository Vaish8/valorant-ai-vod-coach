from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.enums import EventType


class EventCreate(BaseModel):
    timestamp_seconds: int = Field(..., ge=0)
    event_type: EventType
    actor: Optional[str] = Field(default=None, max_length=100)
    target: Optional[str] = Field(default=None, max_length=100)
    location: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None
    source: str = Field(default="manual", max_length=50)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class EventResponse(BaseModel):
    id: int
    round_id: int
    timestamp_seconds: int
    event_type: EventType
    actor: Optional[str] = None
    target: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    source: str
    confidence: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)