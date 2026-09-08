#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
python "$HERE/tests/test_benchmark.py"
python "$HERE/tests/test_conformance.py"
python "$HERE/tests/test_holdout_protocol.py"
python "$HERE/tests/test_holdout_single_analyst.py"
python "$HERE/tests/test_v3_release.py"
python "$HERE/tests/test_v3_provenance.py"
python "$HERE/validator/check_conformance_pairs.py" --pairs "$HERE/data/rank_gate_conformance_pairs_11.csv"
python "$HERE/validator/rank_gate_validator.py" \
  --cases "$HERE/data/baseline_case_inputs.csv" \
  --safeguards "$HERE/data/baseline_mandatory_inputs.csv" \
  --out "$HERE/data/_reproduced_baseline_validation.csv"
python "$HERE/validator/rank_gate_validator.py" \
  --cases "$HERE/data/holdout_case_inputs_single_analyst.csv" \
  --safeguards "$HERE/data/holdout_mandatory_gate_rows.csv" \
  --out "$HERE/data/_reproduced_holdout_validation.csv" \
  --h 0.10 --lambda-risk 0.75
python "$HERE/validator/generate_gap_certificates.py" \
  --safeguards "$HERE/data/mandatory_safeguards_46.csv" \
  --item-out "$HERE/data/_reproduced_missing_evidence_certificates.csv" \
  --case-out "$HERE/data/_reproduced_case_gap_summary.csv"
python "$HERE/validator/rank_gate_validator.py" \
  --cases "$HERE/examples/minimal_dossier/criteria.csv" \
  --safeguards "$HERE/examples/minimal_dossier/mandatory_safeguards.csv" \
  --out "$HERE/examples/minimal_dossier/results.csv"
python "$HERE/benchmark/score_submission.py" \
  --submission "$HERE/benchmark/EXAMPLE_PERFECT_SUBMISSION.csv" \
  --root "$HERE" \
  --out-json "$HERE/benchmark/_example_submission_score.json"
echo "PAPER3_RANK_GATE_BENCHMARK_V3_DOI_READY: PASS"
