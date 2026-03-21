from fastapi import WebSocket

from app.core.errors import ApiError, ErrorCode
from app.core.security import decode_access_token


def extract_bearer_token(websocket: WebSocket) -> str:
    header_value = websocket.headers.get("authorization", "")
    if header_value.lower().startswith("bearer "):
        return header_value[7:].strip()

    query_token = websocket.query_params.get("token")
    if query_token:
        return query_token

    raise ApiError(
        code=ErrorCode.AUTH_TOKEN_INVALID,
        message="Missing websocket bearer token",
        status_code=401,
    )


def get_websocket_subject(websocket: WebSocket) -> str:
    token = extract_bearer_token(websocket)
    payload = decode_access_token(token)
    return payload.sub
