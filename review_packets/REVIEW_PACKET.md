# REVIEW_PACKET

## Entry Point

Run from the project root:

```powershell
python main.py
```

## Core Execution Flow

1. `ExecutionLog.append()` assigns deterministic sequence numbers and preserves insertion order.
2. `execute_with_trace()` validates each event before execution, applies the transition, checks invariants, and records the intermediate state hash.
3. `replay_verified()` replays the complete history and compares every replay snapshot with the original trace.
4. Runtime halts immediately on validation, invariant, or replay divergence failure.

## Maximum Three Critical Files

- `runtime/executor.py`: applies validated events and records execution snapshots.
- `validation/rules.py`: owns pre-execution validation boundaries.
- `replay/engine.py`: owns replay and intermediate hash verification.

## Execution Example

The valid default log is:

1. Sequence `1`: `START`, `causal_id = 1`, `IDLE -> PROCESSING`.
2. Sequence `2`: `COMPLETE`, `causal_id = 2`, `PROCESSING -> COMPLETED`.

Final state hash:

```text
a64d5a8ab6ceabed3fa828db7d3b79cf7faf4c72dad1a3d662d1ba83d3d0bff4
```

## Replay Example

Replay uses the same immutable log entries and original execution trace. The replay hash matches the original final hash exactly.

```text
matches_original: True
```

## Failure Scenarios

- Duplicate event: halted by duplicate `event_id`.
- Ordering failure: halted when causal sequence starts at `2` instead of `1`.
- Illegal transition: halted on invalid state/action pair.
- Invalid node: halted when event node does not match runtime node.
- Missing event: halted when causal sequence jumps from `1` to `3`.
- Replay mismatch: halted when an intermediate replay hash differs.

## Determinism Proof

The same immutable log is replayed five times. Every run produces the same final hash.

```text
all_hashes_identical: True
```

## Invariant Proof

Runtime invariant checks halt execution when:

- `event_counter` does not increase.
- sequence numbers do not increase.
- a completed node re-enters processing.
- a failed node becomes completed.

Terminal-state protections are also covered by the transition validator.

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

- No networking, API, database, UI, or distributed runtime files were added.
- No external dependencies were introduced.

## Known Limitations

- Single-node runtime model.
- In-memory execution log.
- No persistence, network transport, or consensus layer.
- Review evidence is terminal/text evidence because this is a CLI-only project.

## Evidence Index

- `review_packets/evidence/terminal_output.txt`
- `review_packets/evidence/deterministic_hashes.txt`
- `review_packets/evidence/failure_cases.txt`
- `review_packets/code_packets/critical_files.md`
