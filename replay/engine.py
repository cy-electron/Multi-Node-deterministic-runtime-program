from __future__ import annotations

from collections.abc import Iterable

from events.event import ExecutionEvent
from runtime.executor import execute_events
from runtime.state import NodeState


def replay_events(event_log: Iterable[ExecutionEvent], node_id: str) -> NodeState:
    return execute_events(NodeState.initial(node_id), event_log)
