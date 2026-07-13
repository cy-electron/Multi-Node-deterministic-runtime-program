from __future__ import annotations

from events import ExecutionEvent
from events.log import LoggedEvent
from runtime import Action, RuntimeNode


def test_node_keeps_history_hash_and_replay_history() -> None:
    node = RuntimeNode("node-test")
    node.accept(LoggedEvent(1, ExecutionEvent.create("node-test", Action.START, 1)))
    replayed = node.replay()

    assert replayed.hash() == node.state_hash
    assert len(node.execution_history) == 1
    assert node.replay_history == [node.state_hash]
