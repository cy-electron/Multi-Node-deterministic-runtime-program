from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter

from coordination import verify_coordination_replay


def run_benchmark(iterations: int = 100) -> dict[str, object]:
    started = perf_counter()
    hashes = [verify_coordination_replay().result.coordinated_state_hash for _ in range(iterations)]
    elapsed_seconds = perf_counter() - started
    return {
        "iterations": iterations,
        "elapsed_seconds": round(elapsed_seconds, 6),
        "operations_per_second": round(iterations / elapsed_seconds, 2),
        "all_hashes_identical": len(set(hashes)) == 1,
        "coordinated_state_hash": hashes[0],
    }


def main() -> int:
    result = run_benchmark()
    destination = Path("artifacts/benchmark.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    print(f"benchmark_output: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
