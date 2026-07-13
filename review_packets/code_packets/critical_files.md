# Review-Critical Code Packets

## `coordination/coordinator.py`

- **Purpose:** accepts bounded immutable messages and delivers them in one canonical order.
- **Reason modified:** adds local multi-node coordination while excluding networking and concurrency.
- **Integration impact:** every coordinated scenario uses this class; its delivery records feed JSON evidence and replay verification.

## `runtime/node.py`

- **Purpose:** owns one node's runtime state, execution history, deterministic state hash, trace, and replay history.
- **Reason modified:** supplies the independent runtime participant required for coordination.
- **Integration impact:** the coordinator only changes a target through this history-verified node boundary.

## `coordination/scenarios.py`

- **Purpose:** defines the four-node ring and verifies reconstruction from reversed enqueue order.
- **Reason modified:** provides an executable proof of node-to-node communication, ordering, replay safety, and convergence.
- **Integration impact:** used by the main program, benchmark, tests, and evidence exporter.

## `observability/reports.py`

- **Purpose:** constructs canonical audit logs, timeline, runtime summary, replay report, and replay summary JSON.
- **Reason modified:** makes deterministic execution reviewable without reading internal objects.
- **Integration impact:** `main.py` exports the report and the capture script preserves it in this packet.

## `runtime/executor.py`

- **Purpose:** applies validated events and records immutable execution snapshots.
- **Reason modified:** retained as the core single-node replay primitive used by each independent node.
- **Integration impact:** a coordinator delivery cannot update node state without this validation/invariant boundary.
