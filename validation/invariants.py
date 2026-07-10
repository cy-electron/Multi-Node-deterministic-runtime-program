from __future__ import annotations

from dataclasses import dataclass

from events.event import ExecutionEvent
from runtime.errors import RuntimeErrorReason
from runtime.state import NodeState, NodeStatus


@dataclass
class RuntimeInvariantContext:
    last_sequence: int = 0


def validate_invariants(
    previous: NodeState,
    current: NodeState,
    event: ExecutionEvent,
    sequence: int,
    context: RuntimeInvariantContext,
) -> None:
    if current.event_counter <= previous.event_counter:
        raise RuntimeErrorReason("invariant failed: event_counter did not increase")
    if current.event_counter != event.causal_id:
        raise RuntimeErrorReason("invariant failed: event_counter does not match causal_id")
    if sequence <= context.last_sequence:
        raise RuntimeErrorReason("invariant failed: sequence did not increase")

    completed_reentered_processing = (
        previous.current_state == NodeStatus.COMPLETED
        and current.current_state == NodeStatus.PROCESSING
    )
    if completed_reentered_processing:
        raise RuntimeErrorReason("invariant failed: completed node re-entered processing")

    failed_became_completed = (
        previous.current_state == NodeStatus.FAILED
        and current.current_state == NodeStatus.COMPLETED
    )
    if failed_became_completed:
        raise RuntimeErrorReason("invariant failed: failed node became completed")

    context.last_sequence = sequence
