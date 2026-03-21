from typing import Any

DEFAULT_DOMAIN_MESSAGES: dict[str, str] = {
    "AUTH_INVALID_CREDENTIALS": "Invalid credentials",
    "AUTH_TOKEN_INVALID": "Invalid or missing authentication token",
    "AUTH_SERVICE_UNAVAILABLE": "Authentication service temporarily unavailable",
}


class DomainError(Exception):
    def __init__(
        self,
        *,
        code: str,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        resolved_message = message or DEFAULT_DOMAIN_MESSAGES.get(code, "Domain operation failed")
        super().__init__(resolved_message)
        self.code = code
        self.message = resolved_message
        self.details = details or {}


class InvalidCredentialsError(DomainError):
    def __init__(self) -> None:
        super().__init__(code="AUTH_INVALID_CREDENTIALS")


class InvalidTokenError(DomainError):
    def __init__(self) -> None:
        super().__init__(code="AUTH_TOKEN_INVALID")


class AuthenticationServiceUnavailableError(DomainError):
    def __init__(self) -> None:
        super().__init__(code="AUTH_SERVICE_UNAVAILABLE")