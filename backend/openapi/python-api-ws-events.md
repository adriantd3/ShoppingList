# Python API WebSocket Event Catalog (MVP)

Channel endpoint: `GET /api/v1/ws/lists/{list_id}?token=<bearer-or-query-token>`

## Connection Contract
- Authentication: bearer token required (header or query token accepted by WS auth helper).
- Authorization: user must be list member.
- Rejection codes:
  - `4401` when token is missing/invalid.
  - `4403` when authenticated user is not a list member.

## Event Envelope (version 1)

```json
{
  "event_id": "uuid",
  "event_type": "list.item.updated",
  "list_id": "uuid",
  "occurred_at": "2026-03-21T12:00:00Z",
  "actor_user_id": "uuid",
  "payload": {},
  "version": 1
}
```

Required fields:
- `event_id` (string)
- `event_type` (string)
- `list_id` (string)
- `occurred_at` (ISO-8601 datetime)
- `actor_user_id` (string)
- `payload` (object)
- `version` (integer)

## Event Types
- `list.item.created`
- `list.item.updated`
- `list.item.deleted`
- `list.item.purchased_toggled`
- `list.reset.performed`
- `list.restore.performed`
- `list.member.joined`
- `list.member.left`

## Versioning Policy
- Envelope `version` starts at `1`.
- Additive payload fields are backward-compatible.
- Breaking changes require version increment and dual-support transition window.

## Consumer Notes
- Clients should treat unknown fields as forward-compatible.
- Clients should apply last-write-wins semantics using server event ordering and timestamps.
- Reconnect flows should re-sync state from REST if any event gap is suspected.
