from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from threading import Lock
from time import monotonic

from fastapi import Request

from app.core.config import get_settings
from app.core.errors import ApiError, ErrorCode


@dataclass
class RateLimitRule:
    scope: str
    limit: int
    window_seconds: int


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._events: dict[str, deque[float]] = {}
        self._lock = Lock()

    def reset(self) -> None:
        with self._lock:
            self._events.clear()

    def allow(self, *, key: str, limit: int, window_seconds: int) -> bool:
        now = monotonic()
        threshold = now - window_seconds

        with self._lock:
            bucket = self._events.setdefault(key, deque())
            while bucket and bucket[0] <= threshold:
                bucket.popleft()

            if len(bucket) >= limit:
                return False

            bucket.append(now)
            return True


rate_limiter = InMemoryRateLimiter()


def _client_identifier(request: Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",", maxsplit=1)[0].strip()

    if request.client is None or request.client.host is None:
        return "unknown"
    return request.client.host


def _enforce_rule(request: Request, rule: RateLimitRule) -> None:
    client = _client_identifier(request)
    key = f"{rule.scope}:{client}"

    if not rate_limiter.allow(key=key, limit=rule.limit, window_seconds=rule.window_seconds):
        raise ApiError(
            code=ErrorCode.RATE_LIMIT_EXCEEDED,
            message="Too many requests",
            status_code=429,
            details={"scope": rule.scope, "limit": rule.limit, "window_seconds": rule.window_seconds},
        )


def auth_rate_limit_dependency() -> Callable[[Request], None]:
    settings = get_settings()
    rule = RateLimitRule(scope="auth", limit=settings.auth_rate_limit_per_minute, window_seconds=60)

    def _dependency(request: Request) -> None:
        _enforce_rule(request, rule)

    return _dependency


def share_link_rate_limit_dependency() -> Callable[[Request], None]:
    settings = get_settings()
    rule = RateLimitRule(scope="share-link", limit=settings.share_link_rate_limit_per_minute, window_seconds=60)

    def _dependency(request: Request) -> None:
        _enforce_rule(request, rule)

    return _dependency
