from collections import defaultdict
from typing import Any

from fastapi import WebSocket


class RealtimeConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, list_id: str, websocket: WebSocket) -> None:
        self._connections[list_id].add(websocket)

    async def disconnect(self, list_id: str, websocket: WebSocket) -> None:
        connections = self._connections.get(list_id)
        if not connections:
            return

        connections.discard(websocket)
        if not connections:
            self._connections.pop(list_id, None)

    async def broadcast_event(self, list_id: str, event_payload: dict[str, Any]) -> None:
        # Copy to avoid set-size mutation while broadcasting.
        listeners = list(self._connections.get(list_id, set()))
        for websocket in listeners:
            await websocket.send_json(event_payload)


connection_manager = RealtimeConnectionManager()
