from enum import StrEnum
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.domain_errors import DomainError


class ErrorCode(StrEnum):
    AUTH_INVALID_CREDENTIALS = "AUTH_INVALID_CREDENTIALS"
    AUTH_EMAIL_NOT_VERIFIED = "AUTH_EMAIL_NOT_VERIFIED"
    AUTH_TOKEN_INVALID = "AUTH_TOKEN_INVALID"
    AUTH_SERVICE_UNAVAILABLE = "AUTH_SERVICE_UNAVAILABLE"
    FORBIDDEN_LIST_ACCESS = "FORBIDDEN_LIST_ACCESS"
    LIST_NOT_FOUND = "LIST_NOT_FOUND"
    ITEM_NOT_FOUND = "ITEM_NOT_FOUND"
    SHARE_LINK_EXPIRED = "SHARE_LINK_EXPIRED"
    SHARE_LINK_REVOKED = "SHARE_LINK_REVOKED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    REQUEST_TOO_LARGE = "REQUEST_TOO_LARGE"
    UNSUPPORTED_MEDIA_TYPE = "UNSUPPORTED_MEDIA_TYPE"
    IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_PAYLOAD = "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_PAYLOAD"
    CONFLICT_LAST_WRITE_WINS_SUPERSEDED = "CONFLICT_LAST_WRITE_WINS_SUPERSEDED"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ErrorPayload(BaseModel):
    code: str
    message: str
    details: dict[str, Any]
    trace_id: str


class ErrorEnvelope(BaseModel):
    error: ErrorPayload


class ApiError(Exception):
    def __init__(
        self,
        *,
        code: ErrorCode,
        message: str,
        status_code: int,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}


def _get_trace_id(request: Request) -> str:
    trace_id = getattr(request.state, "trace_id", None)
    if not trace_id:
        trace_id = str(uuid4())
        request.state.trace_id = trace_id
    return trace_id


def _safe_internal_message() -> str:
    settings = get_settings()
    if settings.app_env == "production":
        return "Internal server error"
    return "Unhandled server exception"


def build_error_response(
    request: Request,
    *,
    code: ErrorCode,
    message: str,
    status_code: int,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    trace_id = _get_trace_id(request)
    payload = ErrorEnvelope(
        error=ErrorPayload(
            code=code,
            message=message,
            details=details or {},
            trace_id=trace_id,
        )
    )
    response = JSONResponse(status_code=status_code, content=payload.model_dump())
    response.headers["X-Trace-Id"] = trace_id
    return response


def install_exception_handlers(app: FastAPI) -> None:
    domain_status_map: dict[ErrorCode, int] = {
        ErrorCode.AUTH_INVALID_CREDENTIALS: status.HTTP_401_UNAUTHORIZED,
        ErrorCode.AUTH_TOKEN_INVALID: status.HTTP_401_UNAUTHORIZED,
        ErrorCode.AUTH_SERVICE_UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,
    }

    @app.exception_handler(DomainError)
    async def handle_domain_error(request: Request, exc: DomainError) -> JSONResponse:
        code = ErrorCode(exc.code) if exc.code in ErrorCode._value2member_map_ else ErrorCode.INTERNAL_ERROR
        status_code = domain_status_map.get(code, status.HTTP_400_BAD_REQUEST)
        if code == ErrorCode.INTERNAL_ERROR:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_error_response(
            request,
            code=code,
            message=exc.message,
            status_code=status_code,
            details=exc.details,
        )

    @app.exception_handler(ApiError)
    async def handle_api_error(request: Request, exc: ApiError) -> JSONResponse:
        return build_error_response(
            request,
            code=exc.code,
            message=exc.message,
            status_code=exc.status_code,
            details=exc.details,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        return build_error_response(
            request,
            code=ErrorCode.VALIDATION_ERROR,
            message="Validation failed",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"errors": jsonable_encoder(exc.errors())},
        )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
        code_map: dict[int, ErrorCode] = {
            status.HTTP_401_UNAUTHORIZED: ErrorCode.AUTH_TOKEN_INVALID,
            status.HTTP_403_FORBIDDEN: ErrorCode.FORBIDDEN_LIST_ACCESS,
            status.HTTP_404_NOT_FOUND: ErrorCode.LIST_NOT_FOUND,
        }
        code = code_map.get(exc.status_code, ErrorCode.INTERNAL_ERROR)
        message = str(exc.detail) if isinstance(exc.detail, str) else "Request failed"
        if code == ErrorCode.INTERNAL_ERROR:
            message = _safe_internal_message()
        return build_error_response(
            request,
            code=code,
            message=message,
            status_code=exc.status_code,
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, _: Exception) -> JSONResponse:
        return build_error_response(
            request,
            code=ErrorCode.INTERNAL_ERROR,
            message=_safe_internal_message(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
