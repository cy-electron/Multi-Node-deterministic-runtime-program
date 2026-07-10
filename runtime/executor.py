from __future__ import annotations

from collections.abc import Iterable

from events.event import ExecutionEvent
from runtime.errors import RuntimeErrorReason
from runtime.state import Action, NodeState, NodeStatus
from validation import validate_event_identity


def apply_event(event: ExecutionEvent, state: NodeState) -> NodeState:
    validate_event_identity(event)

    if event.node_id != state.node_id:
        raise RuntimeErrorReason(
            f"event node {event.node_id!r} does not match state node {state.node_id!r}"
        )

    expected_causal_id = state.event_counter + 1
    if event.causal_id < expected_causal_id:
        raise RuntimeErrorReason(
            f"duplicate causal_id {event.causal_id}; expected {expected_causal_id}"
        )
    if event.causal_id > expected_causal_id:
        raise RuntimeErrorReason(
            f"skipped causal sequence: received {event.causal_id}, expected {expected_causal_id}"
        )

    next_status = transition(state.current_state, event.action)
    return NodeState(
        node_id=state.node_id,
        current_state=next_status,
        state_version=state.state_version + 1,
        event_counter=event.causal_id,
    )


def transition(current: NodeStatus, action: Action) -> NodeStatus:
    allowed = {
        (NodeStatus.IDLE, Action.START): NodeStatus.PROCESSING,
        (NodeStatus.PROCESSING, Action.COMPLETE): NodeStatus.COMPLETED,
        (NodeStatus.PROCESSING, Action.FAIL): NodeStatus.FAILED,
    }
    try:
        return allowed[(current, action)]
    except KeyError as exc:
        raise RuntimeErrorReason(
            f"invalid transition: {current.value} + {action.value}"
        ) from exc


def execute_events(initial_state: NodeState, event_log: Iterable[ExecutionEvent]) -> NodeState:
    state = initial_state
    for event in event_log:
        state = apply_event(event, state)
    return state
