from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.api.rest.router import router as api_router
from app.api.ws.router import router as ws_router
from app.core.config import get_settings
from app.core.errors import ErrorCode, build_error_response, install_exception_handlers
from app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    docs_enabled = settings.enable_docs and settings.app_env != "production"
    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
        docs_url="/docs" if docs_enabled else None,
        redoc_url="/redoc" if docs_enabled else None,
        openapi_url="/openapi.json" if docs_enabled else None,
        lifespan=lifespan,
    )

    install_exception_handlers(app)

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.trusted_hosts)

    cors_allow_origins = settings.cors_allow_origins
    if settings.app_env != "production" and not cors_allow_origins:
        cors_allow_origins = ["*"]

    if cors_allow_origins:
        allow_credentials = "*" not in cors_allow_origins
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_allow_origins,
            allow_credentials=allow_credentials,
            allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
            allow_headers=["Authorization", "Content-Type", "Idempotency-Key"],
        )

    @app.middleware("http")
    async def enforce_request_guards(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        content_length_header = request.headers.get("content-length")
        content_length = 0
        if content_length_header is not None:
            try:
                content_length = int(content_length_header)
            except ValueError:
                content_length = 0

            if content_length > settings.max_request_body_bytes:
                return build_error_response(
                    request,
                    code=ErrorCode.REQUEST_TOO_LARGE,
                    message="Request body is too large",
                    status_code=413,
                    details={"max_bytes": settings.max_request_body_bytes},
                )

        if (
            settings.enforce_json_content_type
            and request.url.path.startswith("/api/")
            and request.method in {"POST", "PUT", "PATCH"}
        ):
            has_request_body = content_length > 0 or request.headers.get("transfer-encoding") is not None
            content_type = request.headers.get("content-type", "")
            if has_request_body and not content_type.lower().startswith("application/json"):
                return build_error_response(
                    request,
                    code=ErrorCode.UNSUPPORTED_MEDIA_TYPE,
                    message="Content-Type must be application/json",
                    status_code=415,
                )

        return await call_next(request)

    @app.middleware("http")
    async def attach_trace_id(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        trace_id = request.headers.get("X-Trace-Id") or str(uuid4())
        request.state.trace_id = trace_id
        response = await call_next(request)
        response.headers["X-Trace-Id"] = trace_id
        return response

    @app.middleware("http")
    async def attach_security_headers(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        response.headers.setdefault("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
        if settings.app_env == "production":
            response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        return response

    app.include_router(api_router, prefix="/api")
    app.include_router(ws_router, prefix="/api")
    return app


app = create_app()
