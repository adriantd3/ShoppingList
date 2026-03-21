import json
from typing import Any, cast

from fastapi import APIRouter, Request, Response, status
from fastapi.encoders import jsonable_encoder

from app.core.idempotency import IdempotencyPrecheck, persist_mutation_idempotency, prepare_mutation_idempotency
from app.core.request_context import get_request_context
from app.modules.auth.context import AuthenticatedContextDep
from app.modules.lists.schemas import (
    ListCreateRequest,
    ListItemCreateRequest,
    ListItemResponse,
    ListItemUpdateRequest,
    ListResetResponse,
    ListResponse,
    ListRestoreLatestResponse,
    ListUpdateRequest,
)
from app.modules.lists.service import (
    create_item_for_user,
    create_list_for_user,
    delete_item_for_user,
    delete_list_for_user,
    get_list_for_user,
    list_items_for_user,
    list_lists_for_user,
    reset_list_for_user,
    restore_latest_for_user,
    update_item_for_user,
    update_list_for_user,
)

router = APIRouter(prefix="/lists", tags=["lists"])


async def _prepare_idempotency(
    request: Request,
) -> IdempotencyPrecheck:
    context = get_request_context()
    db = context.db
    principal = context.principal
    payload_bytes = await request.body()
    return await prepare_mutation_idempotency(
        db,
        user_id=principal.user_id,
        request_method=request.method,
        request_path=request.url.path,
        idempotency_key=request.headers.get("Idempotency-Key"),
        payload_bytes=payload_bytes,
    )


async def _persist_idempotency(
    precheck: IdempotencyPrecheck,
    *,
    status_code: int,
    response_body: dict[str, Any] | list[Any] | None,
) -> Response | None:
    context = get_request_context()
    db = context.db
    replay = await persist_mutation_idempotency(
        db,
        context=precheck.context,
        response_status_code=status_code,
        response_body=response_body,
    )
    if replay is None:
        return None
    return replay.to_http_response()


def _as_response_body(payload: Any) -> dict[str, Any] | list[Any] | None:
    if payload is None:
        return None

    # Keep replay payload as close as possible to FastAPI's serialized response output.
    if hasattr(payload, "model_dump_json"):
        return cast(dict[str, Any] | list[Any] | None, json.loads(payload.model_dump_json()))

    encoded = jsonable_encoder(payload)
    if isinstance(encoded, dict):
        return encoded
    if isinstance(encoded, list):
        return encoded
    return None


@router.get("", response_model=list[ListResponse])
async def get_lists(_: AuthenticatedContextDep) -> list[ListResponse]:
    return await list_lists_for_user()


@router.post("", response_model=ListResponse, status_code=status.HTTP_201_CREATED)
async def create_list(
    request: Request,
    payload: ListCreateRequest,
    _: AuthenticatedContextDep,
) -> ListResponse | Response:
    precheck = await _prepare_idempotency(request)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    created = await create_list_for_user(payload)
    replay = await _persist_idempotency(
        precheck,
        status_code=status.HTTP_201_CREATED,
        response_body=_as_response_body(created),
    )
    if replay is not None:
        return replay
    return created


@router.get("/{list_id}", response_model=ListResponse)
async def get_list(list_id: str, _: AuthenticatedContextDep) -> ListResponse:
    return await get_list_for_user(list_id)


@router.patch("/{list_id}", response_model=ListResponse)
async def patch_list(
    request: Request,
    list_id: str,
    payload: ListUpdateRequest,
    _: AuthenticatedContextDep,
) -> ListResponse | Response:
    precheck = await _prepare_idempotency(request)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    updated = await update_list_for_user(list_id, payload)
    replay = await _persist_idempotency(
        precheck,
        status_code=status.HTTP_200_OK,
        response_body=_as_response_body(updated),
    )
    if replay is not None:
        return replay
    return updated


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_list(request: Request, list_id: str, _: AuthenticatedContextDep) -> Response:
    precheck = await _prepare_idempotency(request)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    await delete_list_for_user(list_id)
    replay = await _persist_idempotency(
        precheck,
        status_code=status.HTTP_204_NO_CONTENT,
        response_body=None,
    )
    if replay is not None:
        return replay
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{list_id}/items", response_model=list[ListItemResponse])
async def get_list_items(
    list_id: str,
    _: AuthenticatedContextDep,
) -> list[ListItemResponse]:
    return await list_items_for_user(list_id)


@router.post("/{list_id}/items", response_model=ListItemResponse, status_code=status.HTTP_201_CREATED)
async def create_list_item(
    request: Request,
    list_id: str,
    payload: ListItemCreateRequest,
    _: AuthenticatedContextDep,
) -> ListItemResponse | Response:
    precheck = await _prepare_idempotency(request)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    created = await create_item_for_user(list_id, payload)
    replay = await _persist_idempotency(
        precheck,
        status_code=status.HTTP_201_CREATED,
        response_body=_as_response_body(created),
    )
    if replay is not None:
        return replay
    return created


@router.patch("/{list_id}/items/{item_id}", response_model=ListItemResponse)
async def patch_list_item(
    request: Request,
    list_id: str,
    item_id: str,
    payload: ListItemUpdateRequest,
    _: AuthenticatedContextDep,
) -> ListItemResponse | Response:
    precheck = await _prepare_idempotency(request)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    updated = await update_item_for_user(list_id, item_id, payload)
    replay = await _persist_idempotency(
        precheck,
        status_code=status.HTTP_200_OK,
        response_body=_as_response_body(updated),
    )
    if replay is not None:
        return replay
    return updated


@router.delete("/{list_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_list_item(
    request: Request,
    list_id: str,
    item_id: str,
    _: AuthenticatedContextDep,
) -> Response:
    precheck = await _prepare_idempotency(request)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    await delete_item_for_user(list_id, item_id)
    replay = await _persist_idempotency(
        precheck,
        status_code=status.HTTP_204_NO_CONTENT,
        response_body=None,
    )
    if replay is not None:
        return replay
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{list_id}/reset", response_model=ListResetResponse)
async def reset_list(
    request: Request,
    list_id: str,
    _: AuthenticatedContextDep,
) -> ListResetResponse | Response:
    precheck = await _prepare_idempotency(request)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    reset_result = await reset_list_for_user(list_id)
    replay = await _persist_idempotency(
        precheck,
        status_code=status.HTTP_200_OK,
        response_body=_as_response_body(reset_result),
    )
    if replay is not None:
        return replay
    return reset_result


@router.post("/{list_id}/restore-latest", response_model=ListRestoreLatestResponse)
async def restore_latest(
    request: Request,
    list_id: str,
    _: AuthenticatedContextDep,
) -> ListRestoreLatestResponse | Response:
    precheck = await _prepare_idempotency(request)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    restore_result = await restore_latest_for_user(list_id)
    replay = await _persist_idempotency(
        precheck,
        status_code=status.HTTP_200_OK,
        response_body=_as_response_body(restore_result),
    )
    if replay is not None:
        return replay
    return restore_result