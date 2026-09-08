# FAIGRI/EAGLE Rank–Gate Benchmark V3

[![benchmark-ci](https://github.com/shaikhamalkawi-ux/faigri-eagle-rank-gate-benchmark-3/actions/workflows/ci.yml/badge.svg)](https://github.com/shaikhamalkawi-ux/faigri-eagle-rank-gate-benchmark-3/actions/workflows/ci.yml)

**Status:** Active public GitHub benchmark repository.  
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

## ITT 2026 Paper 3 frozen replay

The conference-paper calculation is isolated in [`paper3_itt2026_r8/`](paper3_itt2026_r8/). It reproduces the **11-case paper only** and does not pool the later 15-case holdout into its TOPSIS normalizers, correlations, gate counts, or figure. R8 aligns the crisp and fuzzy comparison on the same six inputs, normalizers, equal comparator weights, and ideal points; only the five documentary scores are fuzzified, while risk remains degenerate. The replay verifies exact crisp recovery at `h=0` and the reported R8 sensitivity results.

From that directory:

```bash
python -m pip install -r requirements.txt
python reproduce_ITT2026_results.py
```

Expected final line:

```text
PAPER3_ITT2026_R8_REPRODUCTION: PASS
```

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

The historical PASS token is retained for byte-stable reproducibility naming; GitHub is the active public dissemination endpoint and no DOI deposit is planned at this stage.

GitHub Actions reconstructs this same hash-verified snapshot and runs the same suite on every push/pull request. The public-mirror verification run completed successfully on 2026-09-08.

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
- `paper3_itt2026_r8/reproduce_ITT2026_results.py`
- `release/reconstruct_snapshot.sh`
- `release/SNAPSHOT_SHA256.txt`
- `release/BASE64_PARTS_MANIFEST.txt`
- `CITATION.cff`
- `LICENSES.md`

## Licensing

- **Code:** MIT License — see `LICENSE_CODE_MIT.txt`.
- **Original benchmark data, documentation, tables, figures, schemas/specifications and derived non-code artifacts:** CC BY 4.0 — see `LICENSE_DATA_DOCS_FIGURES_CC_BY_4.0.md`.
- **Third-party sources:** not redistributed or relicensed; rights remain with the original rights holders.

See `LICENSES.md` for the artifact-level license map.

## Citation

Use `CITATION.cff` for repository citation and cite the corresponding paper where appropriate. The canonical repository URL is:

https://github.com/shaikhamalkawi-ux/faigri-eagle-rank-gate-benchmark-3

## Scientific boundary

This is not a legal-compliance engine, safety certification, prevalence estimator, or product leaderboard. `Hold` means mandatory qualifying public evidence was not located/admitted under the stated rule. The 15-case holdout is single-analyst and is not an independent-coder validation.

## Public release boundary

This GitHub repository is the active public benchmark endpoint selected by the author team. Reuse is governed by the MIT and CC BY 4.0 licenses described above. Third-party source materials are not redistributed or relicensed.
