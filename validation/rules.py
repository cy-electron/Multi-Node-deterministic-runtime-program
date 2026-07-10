from __future__ import annotations

from dataclasses import dataclass, field

from events.event import ExecutionEvent
from events.log import LoggedEvent
from runtime.errors import RuntimeErrorReason
from runtime.state import NodeState
from runtime.transitions import transition
from validation.identity import validate_event_identity


@dataclass
class RuntimeValidationContext:
    seen_event_ids: set[str] = field(default_factory=set)
    seen_causal_ids: set[int] = field(default_factory=set)
    expected_sequence: int = 1


def validate_before_execution(
    item: ExecutionEvent | LoggedEvent,
    state: NodeState,
    context: RuntimeValidationContext,
) -> ExecutionEvent:
    event = item.event if isinstance(item, LoggedEvent) else item

    validate_event_identity(event)
    validate_sequence(item, context)
    validate_unique_event(event, context)
    validate_node(event, state)
    validate_causal_id(event, state, context)
    transition(state.current_state, event.action)

    context.seen_event_ids.add(event.event_id)
    context.seen_causal_ids.add(event.causal_id)
    context.expected_sequence += 1
    return event


def validate_sequence(
    item: ExecutionEvent | LoggedEvent,
    context: RuntimeValidationContext,
) -> None:
    if not isinstance(item, LoggedEvent):
        return
    if item.sequence != context.expected_sequence:
        raise RuntimeErrorReason(
            f"invalid sequence: received {item.sequence}, expected {context.expected_sequence}"
        )


def validate_unique_event(
    event: ExecutionEvent,
    context: RuntimeValidationContext,
) -> None:
    if event.event_id in context.seen_event_ids:
        raise RuntimeErrorReason(f"duplicate event_id {event.event_id}")


def validate_node(event: ExecutionEvent, state: NodeState) -> None:
    if event.node_id != state.node_id:
        raise RuntimeErrorReason(
            f"invalid node {event.node_id!r}; expected {state.node_id!r}"
        )


def validate_causal_id(
    event: ExecutionEvent,
    state: NodeState,
    context: RuntimeValidationContext,
) -> None:
    expected_causal_id = state.event_counter + 1
    if event.causal_id in context.seen_causal_ids:
        raise RuntimeErrorReason(f"duplicate causal_id {event.causal_id}")
    if event.causal_id < expected_causal_id:
        raise RuntimeErrorReason(
            f"causal_id moved backward: received {event.causal_id}, expected {expected_causal_id}"
        )
    if event.causal_id > expected_causal_id:
        raise RuntimeErrorReason(
            f"skipped causal sequence: received {event.causal_id}, expected {expected_causal_id}"
        )
