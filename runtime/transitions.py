from __future__ import annotations

from runtime.errors import RuntimeErrorReason
from runtime.state import Action, NodeStatus


ALLOWED_TRANSITIONS = {
    (NodeStatus.IDLE, Action.START): NodeStatus.PROCESSING,
    (NodeStatus.PROCESSING, Action.COMPLETE): NodeStatus.COMPLETED,
    (NodeStatus.PROCESSING, Action.FAIL): NodeStatus.FAILED,
}


def transition(current: NodeStatus, action: Action) -> NodeStatus:
    try:
        return ALLOWED_TRANSITIONS[(current, action)]
    except KeyError as exc:
        raise RuntimeErrorReason(
            f"invalid transition: {current.value} + {action.value}"
        ) from exc
