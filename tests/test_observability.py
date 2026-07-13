from __future__ import annotations

import json

from coordination import verify_coordination_replay
from observability import build_replay_evidence, export_replay_evidence


def test_evidence_has_required_sections(tmp_path) -> None:
    evidence = build_replay_evidence(verify_coordination_replay())
    assert evidence["replay_summary"]["result"] == "MATCHED"
    assert len(evidence["execution_timeline"]) == 4

    output = export_replay_evidence(verify_coordination_replay(), tmp_path / "replay.json")
    assert json.loads(output.read_text(encoding="utf-8"))["format_version"] == 1
