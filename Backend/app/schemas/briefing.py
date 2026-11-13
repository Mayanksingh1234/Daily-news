from datetime import time
from typing import Optional

from pydantic import BaseModel, Field


class BriefingCreate(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    scheduled_time: time
    timezone: str = "Asia/Kolkata"


class BriefingUpdate(BaseModel):
    topic: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
    )
    scheduled_time: Optional[time] = None
    timezone: Optional[str] = None
    active: Optional[bool] = None