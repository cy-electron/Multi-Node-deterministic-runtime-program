from __future__ import annotations

import json
from pathlib import Path

from coordination import verify_coordination_replay
from observability import build_replay_evidence, export_replay_evidence


def test_evidence_has_required_sections() -> None:
    evidence = build_replay_evidence(verify_coordination_replay())
    assert evidence["replay_summary"]["result"] == "MATCHED"
    assert len(evidence["execution_timeline"]) == 4

    # Keep this small generated check in the same writable artifacts location
    # used by the application. Avoid pytest's OS temporary directory because
    # it is commonly access-restricted on managed Windows machines.
    output = export_replay_evidence(
        verify_coordination_replay(), Path("artifacts/test_replay_evidence.json")
    )
    assert json.loads(output.read_text(encoding="utf-8"))["format_version"] == 1
