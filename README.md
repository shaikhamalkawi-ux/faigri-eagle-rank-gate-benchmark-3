# FAIGRI/EAGLE Rank–Gate Benchmark V3

[![benchmark-ci](https://github.com/shaikhamalkawi-ux/faigri-eagle-rank-gate-benchmark-3/actions/workflows/ci.yml/badge.svg)](https://github.com/shaikhamalkawi-ux/faigri-eagle-rank-gate-benchmark-3/actions/workflows/ci.yml)

**Status:** Public benchmark-development repository; DOI release pending.  
**Scientific baseline:** ITT 2026 Paper 3 R7 development set unchanged.  
**Prospective extension:** 15 frozen institution–system deployments, coded once by ChatGPT under a protocol amendment made after substantive rules were frozen and before holdout outcomes were written.

## Why this benchmark exists

Relative ranking and mandatory documentary clearance are different decision objects. A high-ranked AI procurement/deployment dossier may still lack mandatory public evidence. This release makes that distinction reusable through observed cases, a prospective holdout, matched-pair conformance tests, an executable validator, schemas, provenance, and benchmark scoring utilities.

## Evidence included

- **11 locked development cases:** 2 Documented / 9 Hold.
- **15 frozen prospective holdout cases:** 4 Documented / 11 Hold.
- **26 observed cases total** in `data/observed_cases_26.csv`.
- **107 applicable mandatory documentary rows** in the complete snapshot archive.
- **11 matched rank–gate pairs:** 1 observed pair plus 10 explicitly synthetic counterfactual software tests.
- Missing-evidence certificates and source provenance are included in the complete snapshot archive.

The two observed splits remain analytically separate; do not pool them for vector-normalized TOPSIS ranking.

## Complete public snapshot

Because direct binary upload through the connected workflow corrupted the compressed archive, the exact complete V3 snapshot is stored losslessly as five Base64 text parts under `release/base64/`. Reconstruct it with:

```bash
bash release/reconstruct_snapshot.sh /tmp/FAIGRI_EAGLE_PAPER3_RANK_GATE_BENCHMARK_V3.tar.xz
mkdir -p /tmp/faigri_rank_gate_v3
tar -xJf /tmp/FAIGRI_EAGLE_PAPER3_RANK_GATE_BENCHMARK_V3.tar.xz -C /tmp/faigri_rank_gate_v3
```

The reconstruction script verifies the archive before returning success.

Expected SHA-256:

`a170e43efb3cc193ca6ce031c4a2d76f2a6a26520bd48062a69b043ca965717b`

The archive contains the full V3 data, protocol, provenance, validator, benchmark scoring, schemas, tests, examples, metadata, and documentation tree. Key reusable tables are also exposed directly in the repository.

## One-command verification

After extracting the complete snapshot:

```bash
cd /tmp/faigri_rank_gate_v3
python -m pip install -r requirements.txt
bash run_all.sh
```

A successful run ends with:

```text
PAPER3_RANK_GATE_BENCHMARK_V3_DOI_READY: PASS
```

GitHub Actions reconstructs this same hash-verified snapshot and runs the same suite on every push/pull request. The final public-mirror verification run completed successfully on 2026-09-08.

## Reuse tasks

See `benchmark/BENCHMARK_TASKS_AND_METRICS.md`.

1. rank-only matched-pair invariance;
2. documentary gate reproduction;
3. missing-safeguard localization;
4. split-wise ranking reproduction.

## Key files

- `benchmark/BENCHMARK_SPECIFICATION.json`
- `data/observed_cases_26.csv`
- `data/benchmark_split_manifest.csv`
- `benchmark/GROUND_TRUTH_GATE_AND_MISSING.csv`
- `benchmark/SUBMISSION_TEMPLATE.csv`
- `release/reconstruct_snapshot.sh`
- `release/SNAPSHOT_SHA256.txt`
- `release/BASE64_PARTS_MANIFEST.txt`
- `CITATION.cff`

## Scientific boundary

This is not a legal-compliance engine, safety certification, prevalence estimator, or product leaderboard. `Hold` means mandatory qualifying public evidence was not located/admitted under the stated rule. The 15-case holdout is single-analyst and is not an independent-coder validation.

## Public release boundary

This GitHub repository is publicly accessible at the author team’s direction. No reuse license has yet been selected, so no permission beyond applicable law is granted by this repository. Third-party source materials are not redistributed. A versioned DOI release and explicit code/data licenses remain pending.
