# Review Packet — Multi-Node Deterministic Runtime Coordination

## Entry Point

`python main.py`

## Backend Entry

`main.main()` constructs the original replay-safe event log, runs the
coordinated four-node demonstration, and exports `artifacts/replay_evidence.json`.

## Startup Path

`main.py` → `coordination.verify_coordination_replay()` →
`DeterministicCoordinator.deliver_all()` → `RuntimeNode.accept()` →
`execute_with_trace()` → validation, transitions, snapshots, hashes.

## Three Critical Files

1. `coordination/coordinator.py`: bounded canonical message delivery.
2. `runtime/node.py`: independent node-owned state/history/replay handling.
3. `coordination/scenarios.py`: repeatable four-node execution and replay proof.

## Runtime Flow

Immutable messages enter one local coordinator. It rejects unknown nodes,
duplicates, and capacity overflow, then serially sorts messages by logical
clock/source/target/ID. Each delivery becomes a target-node event. The target
replays its complete local history before replacing its state and recording a
snapshot hash.

## Replay Flow

Each node replays its immutable local event history and checks every snapshot.
The coordinator is independently rebuilt from the same messages in reverse
enqueue order. Delivery records and final coordinated state hash must match.

## Coordination Flow

The default ring is alpha→bravo, bravo→charlie, charlie→delta,
delta→alpha. It is enqueued in a non-canonical order and delivered in logical
clock order. All four nodes independently reach `PROCESSING`.

## JSON Example

```json
{
  "replay_summary": {
    "delivery_count": 4,
    "result": "MATCHED"
  }
}
```

The complete reproducible export is `artifacts/replay_evidence.json`; the
evidence capture script copies it into this packet.

## Files Added

- `coordination/`, `observability/`, `runtime/node.py`
- `tests/`, `benchmark.py`, `validation_suite.py`
- `requirements-dev.txt`, `scripts/run_validation.ps1`
- `scripts/capture_evidence.ps1`

## Files Modified

- `main.py`, `README.md`, `.gitignore`, `runtime/__init__.py`
- `review_packets/REVIEW_PACKET.md`

## Files Untouched

No network clients, API routes, databases, cloud configuration, consensus
algorithms, UI code, or quantum algorithms were introduced.

## Failure Cases

- queue capacity overflow, duplicate message ID, unknown node
- duplicate/invalid/tampered events, causal gaps, invalid transitions
- replay snapshot mismatch and coordinated replay history mismatch

## Evidence Index

- `evidence/terminal_execution.txt`: full runnable-program transcript
- `evidence/replay_evidence.json`: JSON audit export
- `evidence/pytest_execution.txt`: pytest result
- `evidence/coverage_report.txt`: coverage report
- `evidence/benchmark_output.txt`: repeatability benchmark
- `evidence/project_structure.txt`: repository tree
- `evidence/SCREENSHOT_CAPTURE.md`: repeatable screenshot checklist

Run `powershell -ExecutionPolicy Bypass -File scripts/capture_evidence.ps1`
to refresh every text/JSON artifact before the review. The checklist identifies
the terminal windows to capture during a live review; screenshots are not
fabricated by this repository.

## Known Limitations

The model is local, batch-based, in-memory, and serial. History rebuilds are
easy to audit but not designed for large logs. It proves deterministic
coordination rather than real distributed fault tolerance.

## Future Work

Add deterministic snapshots, generated-message scheduling, property tests,
and a versioned replay import format while retaining the local replay oracle.
