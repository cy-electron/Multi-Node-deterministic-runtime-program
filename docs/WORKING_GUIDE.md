# How the Deterministic Runtime Works

This guide is intended for a human reviewer who wants to understand the project
without reading every source file first.

## The Short Version

`main.py` runs two related demonstrations:

1. The original single-node event log proves that one node can execute and
   replay a small event history safely.
2. The coordinated example proves that four separate nodes can receive local
   messages in a deterministic order and reproduce the same result later.

There is no server, network, database, thread, or hidden background process.
Everything happens serially in one Python process, which is exactly why the
result can be replayed reliably.

## What Happens When You Run `python main.py`

1. `build_valid_event_log()` creates `START` then `COMPLETE` for the original
   single node.
2. `execute_with_trace()` validates each event, changes the node state, and
   records a hash after every change.
3. `replay_verified()` starts from a clean node and repeats the same events. It
   compares each sequence number, event ID, and state hash with the first run.
4. The program deliberately tries invalid logs—duplicates, ordering gaps,
   tampering, and bad transitions—to show that the runtime stops safely.
5. `verify_coordination_replay()` runs four node-to-node messages through the
   coordinator, then reconstructs the same work from reversed enqueue order.
6. `export_replay_evidence()` writes the audit, timeline, summaries, and replay
   result to `artifacts/replay_evidence.json`.

## A Concrete Four-Node Example

The demonstration creates this ring:

```text
alpha ──START──> bravo ──START──> charlie ──START──> delta
  ^                                                       |
  └──────────────────────── START ────────────────────────┘
```

The messages are deliberately added in an unsorted order. Before delivery,
`DeterministicCoordinator` sorts them with this key:

```text
(logical_clock, source_node_id, target_node_id, message_id)
```

That means two executions with different enqueue/arrival order still deliver
the same messages in the same order. Each target node receives one `START`
event and independently becomes `PROCESSING`.

## Where the Important Data Lives

During a run, each `RuntimeNode` retains:

| Data | Meaning |
| --- | --- |
| `state` | Current state of that one node. |
| `execution_history` | Accepted local events, in node sequence order. |
| `execution_trace` | Snapshot and hash after each local event. |
| `replay_history` | Hashes of successful replay checks. |

The coordinator retains `delivery_history`, which states which message was
delivered, in which global delivery position, and the target's resulting hash.

These are intentionally in-memory structures. The assignment does not request
a database or long-term runtime persistence. The reviewable output is exported
as JSON at the end of the run.

## Why Rebuild History Instead of Updating State Directly?

When a node receives a message, `RuntimeNode.accept()` builds a candidate
history: its existing entries plus the new entry. It runs that candidate from a
fresh `IDLE` state. Only after every validation and invariant check succeeds
does it replace the node's visible state and history.

This is easy to explain in a review: invalid input cannot leave half-applied
state behind, and replay is simply the same calculation performed again.

## Files Worth Reading First

1. `main.py` — readable entry point and demonstration output.
2. `coordination/scenarios.py` — exact four-node scenario and replay proof.
3. `coordination/coordinator.py` — bounded ordering and delivery rule.
4. `runtime/node.py` — one node's state/history/replay boundary.
5. `runtime/executor.py` and `validation/rules.py` — validation and state
   transition mechanics.
6. `observability/reports.py` — JSON review evidence.

## How to Demonstrate It Live

```powershell
python main.py
python -m pytest -q
Get-Content artifacts/replay_evidence.json
```

Point out `coordination_replay_verified: True`, the four ordered delivery
records, and `all_hashes_identical: True`. Then show the pytest result and JSON
export. Those three outputs demonstrate determinism, replay safety, and
observable evidence without requiring external infrastructure.
