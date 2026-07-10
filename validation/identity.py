from __future__ import annotations

from events.event import ExecutionEvent
from runtime.errors import RuntimeErrorReason


def validate_event_identity(event: ExecutionEvent) -> None:
    expected = ExecutionEvent.create(event.node_id, event.action, event.causal_id)
    if event.timestamp != expected.timestamp:
        raise RuntimeErrorReason(
            f"non-deterministic timestamp for causal_id {event.causal_id}"
        )
    if event.event_id != expected.event_id:
        raise RuntimeErrorReason(f"event_id mismatch for causal_id {event.causal_id}")
