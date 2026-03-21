from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import DbSession
from app.core.request_context import clear_request_context, set_request_context
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import UserPrincipal


@dataclass(frozen=True)
class AuthenticatedContext:
    db: AsyncSession
    principal: UserPrincipal


async def get_authenticated_context(
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> AsyncGenerator[AuthenticatedContext, None]:
    context = AuthenticatedContext(db=db, principal=principal)
    token = set_request_context(context)
    try:
        yield context
    finally:
        clear_request_context(token)


AuthenticatedContextDep = Annotated[AuthenticatedContext, Depends(get_authenticated_context)]