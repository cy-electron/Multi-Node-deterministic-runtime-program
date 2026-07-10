from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from hashing import stable_hash


class NodeStatus(str, Enum):
    IDLE = "IDLE"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Action(str, Enum):
    START = "START"
    COMPLETE = "COMPLETE"
    FAIL = "FAIL"


@dataclass(frozen=True)
class NodeState:
    node_id: str
    current_state: NodeStatus
    state_version: int
    event_counter: int

    @classmethod
    def initial(cls, node_id: str) -> "NodeState":
        return cls(
            node_id=node_id,
            current_state=NodeStatus.IDLE,
            state_version=0,
            event_counter=0,
        )

    def canonical(self) -> dict[str, object]:
        return {
            "node_id": self.node_id,
            "current_state": self.current_state.value,
            "state_version": self.state_version,
            "event_counter": self.event_counter,
        }

    def hash(self) -> str:
        return stable_hash(self.canonical())
