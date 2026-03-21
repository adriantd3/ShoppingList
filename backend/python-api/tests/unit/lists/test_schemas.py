from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.modules.lists.schemas import ListItemCreateRequest, ListItemUpdateRequest


def test_list_item_create_request_normalizes_unit_and_category() -> None:
    payload = ListItemCreateRequest(
        name="Milk",
        quantity=Decimal("1.0"),
        unit=" L ",
        category=" DAIRY ",
        is_purchased=False,
    )

    assert payload.unit == "l"
    assert payload.category == "dairy"


def test_list_item_create_request_rejects_invalid_unit() -> None:
    with pytest.raises(ValidationError):
        ListItemCreateRequest(
            name="Flour",
            quantity=Decimal("2"),
            unit="invalid-unit",
            category="pantry",
            is_purchased=False,
        )


def test_list_item_update_request_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        ListItemUpdateRequest.model_validate({"is_template_item": True})
