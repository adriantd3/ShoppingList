import json
from collections.abc import Awaitable, Callable
from typing import Any, cast

from fastapi import APIRouter, Request, Response, status
from fastapi.encoders import jsonable_encoder

from app.core.idempotency import IdempotencyPrecheck, persist_mutation_idempotency, prepare_mutation_idempotency
from app.modules.auth.context import AuthenticatedContext, AuthenticatedContextDep
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
    context: AuthenticatedContext,
) -> IdempotencyPrecheck:
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
    context: AuthenticatedContext,
    precheck: IdempotencyPrecheck,
    *,
    status_code: int,
    response_body: dict[str, Any] | list[Any] | None,
) -> Response | None:
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


async def _run_idempotent_mutation(
    *,
    request: Request,
    context: AuthenticatedContext,
    status_code: int,
    operation: Callable[[], Awaitable[Any | None]],
) -> Any | Response:
    precheck = await _prepare_idempotency(request, context)
    if precheck.replay is not None:
        return precheck.replay.to_http_response()

    result = await operation()
    replay = await _persist_idempotency(
        context,
        precheck,
        status_code=status_code,
        response_body=_as_response_body(result),
    )
    if replay is not None:
        return replay
    return result


@router.get("", response_model=list[ListResponse])
async def get_lists(context: AuthenticatedContextDep) -> list[ListResponse]:
    return await list_lists_for_user(db=context.db, principal=context.principal)


@router.post("", response_model=ListResponse, status_code=status.HTTP_201_CREATED)
async def create_list(
    request: Request,
    payload: ListCreateRequest,
    context: AuthenticatedContextDep,
) -> ListResponse | Response:
    async def _operation() -> ListResponse:
        return await create_list_for_user(db=context.db, principal=context.principal, payload=payload)

    return cast(
        ListResponse | Response,
        await _run_idempotent_mutation(
            request=request,
            context=context,
            status_code=status.HTTP_201_CREATED,
            operation=_operation,
        ),
    )


@router.get("/{list_id}", response_model=ListResponse)
async def get_list(list_id: str, context: AuthenticatedContextDep) -> ListResponse:
    return await get_list_for_user(db=context.db, principal=context.principal, list_id=list_id)


@router.patch("/{list_id}", response_model=ListResponse)
async def patch_list(
    request: Request,
    list_id: str,
    payload: ListUpdateRequest,
    context: AuthenticatedContextDep,
) -> ListResponse | Response:
    async def _operation() -> ListResponse:
        return await update_list_for_user(
            db=context.db,
            principal=context.principal,
            list_id=list_id,
            payload=payload,
        )

    return cast(
        ListResponse | Response,
        await _run_idempotent_mutation(
            request=request,
            context=context,
            status_code=status.HTTP_200_OK,
            operation=_operation,
        ),
    )


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_list(request: Request, list_id: str, context: AuthenticatedContextDep) -> Response:
    async def _operation() -> None:
        await delete_list_for_user(db=context.db, principal=context.principal, list_id=list_id)
        return None

    result = await _run_idempotent_mutation(
        request=request,
        context=context,
        status_code=status.HTTP_204_NO_CONTENT,
        operation=_operation,
    )
    if isinstance(result, Response):
        return result
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{list_id}/items", response_model=list[ListItemResponse])
async def get_list_items(
    list_id: str,
    context: AuthenticatedContextDep,
) -> list[ListItemResponse]:
    return await list_items_for_user(db=context.db, principal=context.principal, list_id=list_id)


@router.post("/{list_id}/items", response_model=ListItemResponse, status_code=status.HTTP_201_CREATED)
async def create_list_item(
    request: Request,
    list_id: str,
    payload: ListItemCreateRequest,
    context: AuthenticatedContextDep,
) -> ListItemResponse | Response:
    async def _operation() -> ListItemResponse:
        return await create_item_for_user(
            db=context.db,
            principal=context.principal,
            list_id=list_id,
            payload=payload,
        )

    return cast(
        ListItemResponse | Response,
        await _run_idempotent_mutation(
            request=request,
            context=context,
            status_code=status.HTTP_201_CREATED,
            operation=_operation,
        ),
    )


@router.patch("/{list_id}/items/{item_id}", response_model=ListItemResponse)
async def patch_list_item(
    request: Request,
    list_id: str,
    item_id: str,
    payload: ListItemUpdateRequest,
    context: AuthenticatedContextDep,
) -> ListItemResponse | Response:
    async def _operation() -> ListItemResponse:
        return await update_item_for_user(
            db=context.db,
            principal=context.principal,
            list_id=list_id,
            item_id=item_id,
            payload=payload,
        )

    return cast(
        ListItemResponse | Response,
        await _run_idempotent_mutation(
            request=request,
            context=context,
            status_code=status.HTTP_200_OK,
            operation=_operation,
        ),
    )


@router.delete("/{list_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_list_item(
    request: Request,
    list_id: str,
    item_id: str,
    context: AuthenticatedContextDep,
) -> Response:
    async def _operation() -> None:
        await delete_item_for_user(
            db=context.db,
            principal=context.principal,
            list_id=list_id,
            item_id=item_id,
        )
        return None

    result = await _run_idempotent_mutation(
        request=request,
        context=context,
        status_code=status.HTTP_204_NO_CONTENT,
        operation=_operation,
    )
    if isinstance(result, Response):
        return result
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{list_id}/reset", response_model=ListResetResponse)
async def reset_list(
    request: Request,
    list_id: str,
    context: AuthenticatedContextDep,
) -> ListResetResponse | Response:
    async def _operation() -> ListResetResponse:
        return await reset_list_for_user(db=context.db, principal=context.principal, list_id=list_id)

    return cast(
        ListResetResponse | Response,
        await _run_idempotent_mutation(
            request=request,
            context=context,
            status_code=status.HTTP_200_OK,
            operation=_operation,
        ),
    )


@router.post("/{list_id}/restore-latest", response_model=ListRestoreLatestResponse)
async def restore_latest(
    request: Request,
    list_id: str,
    context: AuthenticatedContextDep,
) -> ListRestoreLatestResponse | Response:
    async def _operation() -> ListRestoreLatestResponse:
        return await restore_latest_for_user(db=context.db, principal=context.principal, list_id=list_id)

    return cast(
        ListRestoreLatestResponse | Response,
        await _run_idempotent_mutation(
            request=request,
            context=context,
            status_code=status.HTTP_200_OK,
            operation=_operation,
        ),
    )
