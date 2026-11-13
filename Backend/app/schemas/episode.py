from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class EpisodeResponse(BaseModel):
    id: UUID
    briefing_id: UUID
    user_id: UUID
    title: Optional[str] = None
    script: Optional[str] = None
    audio_url: Optional[str] = None
    status: str
    error_message: Optional[str] = None