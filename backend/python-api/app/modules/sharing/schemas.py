from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ShareLinkIssueRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expires_in_minutes: int = Field(default=1440, ge=5, le=10080)


class ShareLinkConsumeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    token: str = Field(min_length=20, max_length=255)

    @field_validator("token")
    @classmethod
    def strip_token(cls, value: str) -> str:
        return value.strip()


class ShareLinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    list_id: str
    expires_at: datetime
    revoked_at: datetime | None
    revoked_by_user_id: str | None
    created_by_user_id: str
    created_at: datetime


class ShareLinkIssueResponse(BaseModel):
    link: ShareLinkResponse
    token: str


class ShareLinkConsumeResponse(BaseModel):
    list_id: str
    membership_role: str


def calculate_expiration(expires_in_minutes: int) -> datetime:
    return datetime.now(UTC) + timedelta(minutes=expires_in_minutes)
