from __future__ import annotations

from dataclasses import dataclass, field

from events.log import LoggedEvent
from replay import replay_verified
from runtime.executor import ExecutionSnapshot, execute_with_trace
from runtime.state import NodeState


@dataclass
class RuntimeNode:
    """An independent, in-memory deterministic runtime participant."""

    node_id: str
    state: NodeState = field(init=False)
    execution_history: list[LoggedEvent] = field(default_factory=list)
    execution_trace: tuple[ExecutionSnapshot, ...] = field(default=(), init=False)
    replay_history: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.state = NodeState.initial(self.node_id)

    @property
    def state_hash(self) -> str:
        return self.state.hash()

    def accept(self, entry: LoggedEvent) -> ExecutionSnapshot:
        """Safely accept one delivery.

        The node does not mutate its state event-by-event in place.  Instead it
        executes a *candidate* full history from a clean initial state.  If
        validation succeeds, the candidate becomes the new visible state.  This
        makes a rejected delivery unable to leave a partially updated node.
        """
        candidate_history = (*self.execution_history, entry)
        state, trace = execute_with_trace(NodeState.initial(self.node_id), candidate_history)
        self.execution_history.append(entry)
        self.state = state
        self.execution_trace = trace
        return trace[-1]

    def replay(self) -> NodeState:
        # Compare every replay snapshot with `execution_trace`, not just the
        # final state.  A matching final hash alone could hide an earlier error.
        replayed = replay_verified(self.execution_history, self.node_id, self.execution_trace)
        replay_hash = replayed.hash()
        self.replay_history.append(replay_hash)
        return replayed

    def summary(self) -> dict[str, object]:
        return {
            "node_id": self.node_id,
            "runtime_state": self.state.canonical(),
            "execution_history_length": len(self.execution_history),
            "deterministic_state_hash": self.state_hash,
            "replay_history": list(self.replay_history),
        }
