from __future__ import annotations

from collections.abc import Iterable

from events.event import ExecutionEvent
from events.log import LoggedEvent
from runtime.errors import RuntimeErrorReason
from runtime.executor import ExecutionSnapshot, execute_events, execute_with_trace
from runtime.state import NodeState


def replay_events(event_log: Iterable[ExecutionEvent | LoggedEvent], node_id: str) -> NodeState:
    return execute_events(NodeState.initial(node_id), event_log)


def replay_verified(
    event_log: Iterable[ExecutionEvent | LoggedEvent],
    node_id: str,
    original_trace: Iterable[ExecutionSnapshot],
) -> NodeState:
    replayed_state, replay_trace = execute_with_trace(NodeState.initial(node_id), event_log)
    expected_trace = tuple(original_trace)

    if len(replay_trace) != len(expected_trace):
        raise RuntimeErrorReason(
            f"replay length mismatch: received {len(replay_trace)}, expected {len(expected_trace)}"
        )

    for replayed, expected in zip(replay_trace, expected_trace):
        if replayed.sequence != expected.sequence:
            raise RuntimeErrorReason(
                f"replay sequence mismatch: received {replayed.sequence}, expected {expected.sequence}"
            )
        if replayed.event_id != expected.event_id:
            raise RuntimeErrorReason(
                f"replay event mismatch at sequence {expected.sequence}"
            )
        if replayed.state_hash != expected.state_hash:
            raise RuntimeErrorReason(
                f"replay hash mismatch at sequence {expected.sequence}"
            )

    return replayed_state
