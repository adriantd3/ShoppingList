from contextvars import ContextVar, Token
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.auth.context import AuthenticatedContext

_request_context: ContextVar["AuthenticatedContext | None"] = ContextVar("request_context", default=None)


def set_request_context(context: "AuthenticatedContext") -> Token["AuthenticatedContext | None"]:
    return _request_context.set(context)


def get_request_context() -> "AuthenticatedContext":
    context = _request_context.get()
    if context is None:
        raise RuntimeError("Request context is not available")
    return context


def clear_request_context(token: Token["AuthenticatedContext | None"] | None = None) -> None:
    if token is None:
        _request_context.set(None)
        return
    _request_context.reset(token)