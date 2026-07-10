from __future__ import annotations

from dataclasses import asdict
from collections.abc import Iterable

from events.event import ExecutionEvent
from events.log import ExecutionLog
from runtime.state import NodeState


def event_log_as_dicts(event_log: ExecutionLog | Iterable[ExecutionEvent]) -> list[dict[str, object]]:
    if isinstance(event_log, ExecutionLog):
        return event_log.canonical()
    return [event.canonical() for event in event_log]


def state_as_dict(state: NodeState) -> dict[str, object]:
    data = asdict(state)
    data["current_state"] = state.current_state.value
    return data
