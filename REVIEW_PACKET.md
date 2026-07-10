# REVIEW_PACKET

## Entry Point

Run the project from this folder:

```powershell
python main.py
```

The command prints the event log, original execution, replay result, failure
cases, determinism proof, and stress validation summary.

## Core Flow

1. `ExecutionEvent.create()` builds an event from deterministic inputs.
2. `ExecutionLog.append()` stores the event and assigns the next sequence number.
3. `execute_with_trace()` validates the event, applies it, checks invariants, and records the new state hash.
4. `replay_verified()` runs the same history again and compares every replayed state hash with the original trace.

If anything is invalid, the runtime raises `RuntimeErrorReason` and stops.

## Critical Files

- `runtime/executor.py`: applies validated events and records state snapshots.
- `validation/rules.py`: checks identity, sequence, duplicates, causal order, node id, and legal transition.
- `replay/engine.py`: replays the log and stops on the first mismatch.

## Execution Example

The default valid run has two events:

1. `START` with `causal_id = 1`: `IDLE -> PROCESSING`.
2. `COMPLETE` with `causal_id = 2`: `PROCESSING -> COMPLETED`.

The original final hash and replay final hash are the same:

```text
a64d5a8ab6ceabed3fa828db7d3b79cf7faf4c72dad1a3d662d1ba83d3d0bff4
```

## Replay Example

Replay uses the immutable log entries and the trace from the original execution.
The output includes:

```text
matches_original: True
```

## Failure Scenarios

The program demonstrates these failures:

- duplicate event
- duplicate causal id
- out-of-order event
- missing event
- illegal transition
- invalid node
- tampered timestamp
- tampered event id
- replay hash mismatch

Each case prints `halted: True` with the reason.

## Determinism Proof

The same event log is replayed five times. Every run gives the same hash:

```text
all_hashes_identical: True
```

## Invariant Proof

The runtime checks that counters and sequence numbers only move forward. It also
prevents terminal states from moving into invalid states. If an invariant fails,
execution stops.

## Known Limits

- Single-node runtime only.
- In-memory event log only.
- No persistence layer.
- No network or distributed coordination.
- No external dependencies.
