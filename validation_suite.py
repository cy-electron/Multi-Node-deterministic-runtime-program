from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from benchmark import run_benchmark


def main() -> int:
    test_run = subprocess.run([sys.executable, "-m", "pytest", "-q"], check=False)
    benchmark = run_benchmark()
    summary = {
        "pytest_exit_code": test_run.returncode,
        "benchmark": benchmark,
        "result": "PASS" if test_run.returncode == 0 and benchmark["all_hashes_identical"] else "FAIL",
    }
    destination = Path("artifacts/execution_summary.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return test_run.returncode


if __name__ == "__main__":
    raise SystemExit(main())
