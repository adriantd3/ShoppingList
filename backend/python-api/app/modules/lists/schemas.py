from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.lists.catalogs import VALID_CATEGORIES, VALID_UNITS


class ListCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=120)


class ListUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=120)


class ListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    status: str
    owner_user_id: str
    created_at: datetime
    updated_at: datetime


class ListItemCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=120)
    quantity: Decimal = Field(gt=0)
    unit: str = Field(min_length=1, max_length=30)
    category: str = Field(min_length=1, max_length=40)
    note: str | None = Field(default=None, max_length=500)
    is_purchased: bool = False
    sort_index: int | None = Field(default=None, ge=0)

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value: str) -> str:
        normalized = value.lower().strip()
        if normalized not in VALID_UNITS:
            raise ValueError("Unsupported unit")
        return normalized

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        normalized = value.lower().strip()
        if normalized not in VALID_CATEGORIES:
            raise ValueError("Unsupported category")
        return normalized


class ListItemUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=120)
    quantity: Decimal | None = Field(default=None, gt=0)
    unit: str | None = Field(default=None, min_length=1, max_length=30)
    category: str | None = Field(default=None, min_length=1, max_length=40)
    note: str | None = Field(default=None, max_length=500)
    is_purchased: bool | None = None
    sort_index: int | None = Field(default=None, ge=0)

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.lower().strip()
        if normalized not in VALID_UNITS:
            raise ValueError("Unsupported unit")
        return normalized

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.lower().strip()
        if normalized not in VALID_CATEGORIES:
            raise ValueError("Unsupported category")
        return normalized


class ListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    list_id: str
    name: str
    quantity: Decimal
    unit: str
    category: str
    note: str | None
    is_purchased: bool
    is_template_item: bool
    sort_index: int
    updated_at: datetime
    updated_by_user_id: str


class ListResetResponse(BaseModel):
    list_id: str
    snapshot_id: str
    reset_items_count: int


class ListRestoreLatestResponse(BaseModel):
    list_id: str
    snapshot_id: str
    restored_items_count: int