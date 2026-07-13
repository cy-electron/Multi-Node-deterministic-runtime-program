$ErrorActionPreference = 'Stop'
python -m coverage run -m pytest -q
python -m coverage html -d artifacts/coverage_html
python -m coverage report | Tee-Object -FilePath artifacts/coverage_report.txt
python benchmark.py | Tee-Object -FilePath artifacts/benchmark_output.txt
python validation_suite.py | Tee-Object -FilePath artifacts/execution_summary.txt
