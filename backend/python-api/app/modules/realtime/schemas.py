from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RealtimeEventEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str
    event_type: str
    list_id: str
    occurred_at: datetime
    actor_user_id: str
    payload: dict[str, Any] = Field(default_factory=dict)
    version: int = 1
