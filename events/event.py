from __future__ import annotations

from dataclasses import dataclass

from hashing import stable_hash
from runtime.state import Action


@dataclass(frozen=True)
class ExecutionEvent:
    event_id: str
    node_id: str
    action: Action
    timestamp: int
    causal_id: int

    @classmethod
    def create(cls, node_id: str, action: Action | str, causal_id: int) -> "ExecutionEvent":
        action_value = Action(action)
        timestamp = deterministic_timestamp(causal_id)
        event_id = stable_hash(
            {
                "node_id": node_id,
                "action": action_value.value,
                "timestamp": timestamp,
                "causal_id": causal_id,
            }
        )
        return cls(
            event_id=event_id,
            node_id=node_id,
            action=action_value,
            timestamp=timestamp,
            causal_id=causal_id,
        )

    def canonical(self) -> dict[str, object]:
        return {
            "event_id": self.event_id,
            "node_id": self.node_id,
            "action": self.action.value,
            "timestamp": self.timestamp,
            "causal_id": self.causal_id,
        }


def deterministic_timestamp(causal_id: int) -> int:
    if causal_id <= 0:
        raise ValueError("causal_id must be positive")
    return 1_000_000 + causal_id
