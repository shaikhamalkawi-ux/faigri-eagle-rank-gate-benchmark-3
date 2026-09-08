# Benchmark tasks and metrics

The benchmark tests architectural separation between **relative ranking** and **mandatory documentary clearance**. It is not a predictive legal-compliance benchmark.

## Task A — rank-only matched-pair invariance

Input: `data/rank_gate_conformance_pairs_11.csv`.

Each matched pair has identical `(P,F,T,H,L,r)` ranking inputs and opposite documentary gate states. A procedure advertised as **rank-only** should therefore return the same ranking score for both members of each pair.

Report:
- `pair_invariance_pass_rate`: fraction of pairs with absolute rank-score difference <= declared tolerance;
- `pair_max_abs_rank_delta`: maximum within-pair absolute rank-score difference.

Expected for the bundled rank-only baselines: 1.000 pass rate and 0 maximum delta.

## Task B — documentary gate reproduction

Input: mandatory safeguard rows. For each case, compute `Documented` iff every applicable `m_ij=1`; otherwise return `Hold`.

Report exact gate accuracy. The bundled validator must score 1.000 because the Boolean gate is deterministic.

## Task C — missing-safeguard localization

For each Hold case, return the exact set of mandatory safeguards with `m_ij=0`.

Report exact-set accuracy and macro Jaccard similarity. This task evaluates whether a tool exposes *why* a dossier is on Hold rather than collapsing missing evidence into a single score.

## Task D — split-wise ranking reproduction

Use the provided development and prospective-holdout case files separately. Reconstruct equal-weight crisp TOPSIS and the frozen fuzzy/risk-adjusted baselines. Do not pool the two splits for ranking because vector-normalized TOPSIS is set-dependent.

## Interpretation boundary

A high ranking score does not imply documentary gate passage. A Hold result means only that required qualifying public evidence was not located/admitted under the benchmark rule. It does not establish legal non-compliance, unsafe operation, product defect, or absence of an internal control.
