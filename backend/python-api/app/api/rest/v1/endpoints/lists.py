import json
from typing import Any, cast

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.encoders import jsonable_encoder

from app.api.dependencies import DbSession
from app.core.idempotency import IdempotencyPrecheck, persist_mutation_idempotency, prepare_mutation_idempotency
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import UserPrincipal
from app.modules.lists.schemas import (
    ListCreateRequest,
    ListItemCreateRequest,
    ListItemResponse,
    ListItemUpdateRequest,
    ListResponse,
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
    update_item_for_user,
    update_list_for_user,
)

router = APIRouter(prefix="/lists", tags=["lists"])


async def _prepare_idempotency(
    request: Request,
    db: DbSession,
    principal: UserPrincipal,
) -> IdempotencyPrecheck:
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
    db: DbSession,
    precheck: IdempotencyPrecheck,
    *,
    status_code: int,
    response_body: dict[str, Any] | list[Any] | None,
) -> Response | None:
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
async def get_lists(db: DbSession, principal: UserPrincipal = Depends(get_current_user)) -> list[ListResponse]:
    return await list_lists_for_user(db, principal)


@router.post("", response_model=ListResponse, status_code=status.HTTP_201_CREATED)
async def create_list(
    request: Request,
    payload: ListCreateRequest,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> ListResponse | Response:
    precheck = await _prepare_idempotency(request, db, principal)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    created = await create_list_for_user(db, principal, payload)
    replay = await _persist_idempotency(
        db,
        precheck,
        status_code=status.HTTP_201_CREATED,
        response_body=_as_response_body(created),
    )
    if replay is not None:
        return replay
    return created


@router.get("/{list_id}", response_model=ListResponse)
async def get_list(list_id: str, db: DbSession, principal: UserPrincipal = Depends(get_current_user)) -> ListResponse:
    return await get_list_for_user(db, principal, list_id)


@router.patch("/{list_id}", response_model=ListResponse)
async def patch_list(
    request: Request,
    list_id: str,
    payload: ListUpdateRequest,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> ListResponse | Response:
    precheck = await _prepare_idempotency(request, db, principal)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    updated = await update_list_for_user(db, principal, list_id, payload)
    replay = await _persist_idempotency(
        db,
        precheck,
        status_code=status.HTTP_200_OK,
        response_body=_as_response_body(updated),
    )
    if replay is not None:
        return replay
    return updated


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_list(request: Request, list_id: str, db: DbSession, principal: UserPrincipal = Depends(get_current_user)) -> Response:
    precheck = await _prepare_idempotency(request, db, principal)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    await delete_list_for_user(db, principal, list_id)
    replay = await _persist_idempotency(
        db,
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
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> list[ListItemResponse]:
    return await list_items_for_user(db, principal, list_id)


@router.post("/{list_id}/items", response_model=ListItemResponse, status_code=status.HTTP_201_CREATED)
async def create_list_item(
    request: Request,
    list_id: str,
    payload: ListItemCreateRequest,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> ListItemResponse | Response:
    precheck = await _prepare_idempotency(request, db, principal)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    created = await create_item_for_user(db, principal, list_id, payload)
    replay = await _persist_idempotency(
        db,
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
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> ListItemResponse | Response:
    precheck = await _prepare_idempotency(request, db, principal)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    updated = await update_item_for_user(db, principal, list_id, item_id, payload)
    replay = await _persist_idempotency(
        db,
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
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> Response:
    precheck = await _prepare_idempotency(request, db, principal)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    await delete_item_for_user(db, principal, list_id, item_id)
    replay = await _persist_idempotency(
        db,
        precheck,
        status_code=status.HTTP_204_NO_CONTENT,
        response_body=None,
    )
    if replay is not None:
        return replay
    return Response(status_code=status.HTTP_204_NO_CONTENT)