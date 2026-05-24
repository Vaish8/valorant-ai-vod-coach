from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MatchCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    map_name: str = Field(..., min_length=2, max_length=100)
    player_agent: str = Field(..., min_length=2, max_length=100)
    rank: Optional[str] = Field(default=None, max_length=100)


class MatchResponse(BaseModel):
    id: int
    title: str
    map_name: str
    player_agent: str
    rank: Optional[str] = None
    vod_file_path: Optional[str] = None
    video_duration_seconds: Optional[float] = None
    video_fps: Optional[float] = None
    video_resolution: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)