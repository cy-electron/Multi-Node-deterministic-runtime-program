from __future__ import annotations

from dataclasses import replace

import pytest

from coordination import DeterministicCoordinator, RuntimeMessage, verify_coordination_replay
from coordination.scenarios import build_demo_messages, execute_coordination
from runtime import Action, RuntimeErrorReason


def test_coordination_replay_converges() -> None:
    verification = verify_coordination_replay()
    assert verification.replay_verified is True
    assert len(verification.result.deliveries) == 4
    assert len(verification.node_replay_hashes) == 4


def test_delivery_order_is_independent_of_enqueue_order() -> None:
    _, first = execute_coordination(build_demo_messages())
    _, second = execute_coordination(tuple(reversed(build_demo_messages())))
    assert first == second


def test_messages_are_immutable() -> None:
    message = build_demo_messages()[0]
    with pytest.raises(AttributeError):
        message.logical_clock = 99  # type: ignore[misc]


def test_queue_capacity_halts_execution() -> None:
    coordinator = DeterministicCoordinator(("a", "b", "c"), max_messages=1)
    coordinator.enqueue(RuntimeMessage.create("a", "b", Action.START, 1, 1))
    with pytest.raises(RuntimeErrorReason, match="capacity"):
        coordinator.enqueue(RuntimeMessage.create("b", "c", Action.START, 1, 2))


def test_unknown_target_halts_execution() -> None:
    coordinator = DeterministicCoordinator(("a", "b", "c"))
    with pytest.raises(RuntimeErrorReason, match="unknown"):
        coordinator.enqueue(RuntimeMessage.create("a", "missing", Action.START, 1, 1))


def test_tampered_message_id_is_not_duplicate_safe() -> None:
    coordinator = DeterministicCoordinator(("a", "b", "c"))
    message = RuntimeMessage.create("a", "b", Action.START, 1, 1)
    coordinator.enqueue(message)
    with pytest.raises(RuntimeErrorReason, match="duplicate"):
        coordinator.enqueue(replace(message))
