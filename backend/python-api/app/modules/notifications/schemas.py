from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    email: str
    display_name: str
    is_active: bool


class ProfileUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    display_name: str = Field(min_length=1, max_length=80)


class NotificationPreferencesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    list_change_push_enabled: bool
    updated_at: datetime


class NotificationPreferencesUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    list_change_push_enabled: bool


class DevicePushTokenRegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    platform: Literal["ios", "android"]
    push_token: str = Field(min_length=20, max_length=255)


class DevicePushTokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    platform: str
    push_token: str
    last_seen_at: datetime
    created_at: datetime
