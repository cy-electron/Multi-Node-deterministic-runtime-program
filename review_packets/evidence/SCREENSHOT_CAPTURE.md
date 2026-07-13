# Screenshot Capture Checklist

Run `powershell -ExecutionPolicy Bypass -File scripts/capture_evidence.ps1`.
Capture the terminal after each labelled command/output below and save the image
beside the generated evidence with the matching stem.

1. `terminal_execution.txt` — `python main.py`, including coordinated timeline.
2. `replay_evidence.json` — JSON export opened in an editor or terminal.
3. `pytest_execution.txt` — `pytest` pass output.
4. `coverage_report.txt` — coverage table.
5. `benchmark_output.txt` — repeatability benchmark with one final hash.
6. `project_structure.txt` — repository structure listing.

The committed text and JSON files are the source evidence. Capture images from
the actual local review environment so they reflect the machine and command
output being demonstrated.
