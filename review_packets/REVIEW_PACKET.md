# REVIEW_PACKET

## Entry Point

Run this command from the project root:

```powershell
python main.py
```

It prints the full runtime proof: event log, original execution, replay, failure
cases, repeated hash proof, and stress validation.

## Core Execution Flow

1. A deterministic event is created with `ExecutionEvent.create()`.
2. The event is added to `ExecutionLog`, which gives it the next sequence number.
3. `execute_with_trace()` validates the event before changing state.
4. The runtime applies the transition and checks invariants.
5. A state hash is stored for that step.
6. `replay_verified()` replays the same log and compares each stored hash.

The runtime stops as soon as validation, invariants, or replay verification fail.

## Three Critical Files

- `runtime/executor.py`: runs validated events and records state snapshots.
- `validation/rules.py`: keeps validation separate from execution.
- `replay/engine.py`: verifies replay output against the original trace.

## Execution Example

The normal run is small on purpose:

1. Sequence `1`: `START`, `causal_id = 1`, `IDLE -> PROCESSING`.
2. Sequence `2`: `COMPLETE`, `causal_id = 2`, `PROCESSING -> COMPLETED`.

Final state hash:

```text
a64d5a8ab6ceabed3fa828db7d3b79cf7faf4c72dad1a3d662d1ba83d3d0bff4
```

## Replay Example

Replay uses the same immutable log and compares every intermediate state hash.
The expected result is:

```text
matches_original: True
```

## Failure Scenarios

The runtime rejects:

- duplicate events
- duplicate causal ids
- out-of-order events
- missing events
- illegal transitions
- invalid nodes
- tampered timestamps
- tampered event ids
- replay hash mismatches

Each failure prints a reason and halts.

## Determinism Proof

The project replays the same log five times. All five runs produce the same
final hash:

```text
all_hashes_identical: True
```

## Invariant Proof

The runtime checks these rules while executing:

- event counters must increase
- sequence numbers must increase
- completed nodes cannot go back to processing
- failed nodes cannot become completed

If any rule is broken, execution stops.

## Files Added

- `.gitignore`
- `events/`
- `hashing/`
- `replay/`
- `runtime/`
- `validation/`
- `stress.py`
- `review_packets/`

## Files Modified

- `main.py`
- `README.md`
- `REVIEW_PACKET.md`

## Files Untouched

No networking, database, API, UI, or distributed runtime code was added.

## Known Limits

- Single-node runtime model.
- In-memory event log.
- No persistence.
- No distributed transport.
- Evidence is text-based because the project runs in the terminal.

## Evidence Index

- `review_packets/evidence/terminal_output.txt`
- `review_packets/evidence/deterministic_hashes.txt`
- `review_packets/evidence/failure_cases.txt`
- `review_packets/code_packets/critical_files.md`
