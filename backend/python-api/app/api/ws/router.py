from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.api.dependencies import DbSession
from app.api.ws.auth import get_websocket_subject
from app.modules.lists.repository import get_membership_role
from app.modules.realtime.manager import connection_manager

router = APIRouter()


@router.websocket("/v1/ws/lists/{list_id}")
async def list_events_channel(websocket: WebSocket, list_id: str, db: DbSession) -> None:
    try:
        user_id = get_websocket_subject(websocket)
    except Exception:
        await websocket.close(code=4401)
        return

    membership_role = await get_membership_role(db, list_id=list_id, user_id=user_id)
    if membership_role is None:
        await websocket.close(code=4403)
        return

    await websocket.accept()
    await connection_manager.connect(list_id, websocket)
    try:
        while True:
            # Keep the channel open; client-side pings are ignored.
            await websocket.receive_text()
    except WebSocketDisconnect:
        await connection_manager.disconnect(list_id, websocket)
