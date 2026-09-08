# FAIGRI/EAGLE Rank–Gate Benchmark V3

**Status:** Public benchmark-development repository; DOI release pending.  
**Scientific baseline:** ITT 2026 Paper 3 R7 development set unchanged.  
**Prospective extension:** 15 frozen institution–system deployments, coded once by ChatGPT under a protocol amendment made after substantive rules were frozen and before holdout outcomes were written.

## Why this benchmark exists

Relative ranking and mandatory documentary clearance are different decision objects. A high-ranked AI procurement/deployment dossier may still lack mandatory public evidence. This release makes that distinction reusable through observed cases, a prospective holdout, matched-pair conformance tests, an executable validator, schemas, provenance, and benchmark scoring utilities.

## Evidence included

- **11 locked development cases:** 2 Documented / 9 Hold.
- **15 frozen prospective holdout cases:** 4 Documented / 11 Hold.
- **26 observed cases total** in `data/observed_cases_26.csv`.
- **107 applicable mandatory documentary rows** in `data/observed_mandatory_rows_107.csv`.
- **11 matched rank–gate pairs:** 1 observed pair plus 10 explicitly synthetic counterfactual software tests.
- Missing-evidence certificates and source provenance.

The two observed splits remain analytically separate; do not pool them for vector-normalized TOPSIS ranking.

## One-command verification

```bash
python -m pip install -r requirements.txt
bash run_all.sh
```

A successful run ends with:

```text
PAPER3_RANK_GATE_BENCHMARK_V3_DOI_READY: PASS
```

## Reuse tasks

See `benchmark/BENCHMARK_TASKS_AND_METRICS.md`.

1. rank-only matched-pair invariance;
2. documentary gate reproduction;
3. missing-safeguard localization;
4. split-wise ranking reproduction.

## Minimal example

```bash
python validator/rank_gate_validator.py \
  --cases examples/minimal_dossier/criteria.csv \
  --safeguards examples/minimal_dossier/mandatory_safeguards.csv \
  --out examples/minimal_dossier/results.csv
```

## Key files

- `benchmark/BENCHMARK_SPECIFICATION.json`
- `metadata/DATA_DICTIONARY.csv`
- `data/observed_cases_26.csv`
- `data/observed_mandatory_rows_107.csv`
- `data/benchmark_split_manifest.csv`
- `data/rank_gate_conformance_pairs_11.csv`
- `benchmark/score_submission.py`
- `validator/rank_gate_validator.py`
- `source_provenance/holdout/holdout_source_evidence_ledger.csv`
- `source_provenance/holdout/holdout_criterion_evidence_ledger.csv`

## Scientific boundary

This is not a legal-compliance engine, safety certification, prevalence estimator, or product leaderboard. `Hold` means mandatory qualifying public evidence was not located/admitted under the stated rule. The 15-case holdout is single-analyst and is not an independent-coder validation.

## Public release boundary

This GitHub repository is publicly accessible at the author team’s direction. No reuse license has yet been selected, so no permission beyond applicable law is granted by this repository. Third-party source materials are not redistributed. A versioned DOI release and explicit code/data licenses remain pending.
