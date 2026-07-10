# Critical Source Files

## runtime/executor.py

Purpose: applies events after validation and records execution snapshots.

Reason for modification: execution needed traceable intermediate hashes and invariant checks while keeping mutation logic small.

## validation/rules.py

Purpose: validates event identity, sequence, duplicates, causal order, node ownership, and legal transitions before execution.

Reason for modification: validation must remain independent from execution.

## replay/engine.py

Purpose: replays event history and compares every replay snapshot against the original execution trace.

Reason for modification: replay must stop immediately on the first divergence.
