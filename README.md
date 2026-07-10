# Deterministic Runtime Simulation

Small Python implementation for the replay-safe deterministic runtime task.

It models one node, applies ordered events, records immutable execution history,
replays the log, checks the final state hash, and shows divergence cases.

```powershell
python main.py
```

## Files

- `runtime/`: state model, transition executor, errors, and serialization.
- `events/`: immutable event contract and append-only execution log.
- `replay/`: replay entry point.
- `validation/`: event identity checks kept separate from execution.
- `hashing/`: stable JSON/SHA-256 hashing helper.
- `main.py`: runs the example, replay, failure checks, and hash proof.
- `REVIEW_PACKET.md`: short explanation of the build.

No external packages are needed.
