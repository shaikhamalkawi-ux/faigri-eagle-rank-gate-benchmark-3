# Paper 3 ITT 2026 R8 - frozen paper-specific replay

This directory reproduces the **11-case conference paper only**. It does not pool the later 15-case holdout benchmark with the conference sample.

The R8 correction aligns the crisp and fuzzy comparisons: crisp TOPSIS uses `P,F,T,H,L` as benefit criteria and `r` as a cost criterion with vector normalization and equal `1/6` comparator weights. The fuzzy sensitivity uses the same inputs, normalizers, weights, and ideal points; only the five documentary criteria are fuzzified, while `r` remains degenerate. The construction recovers crisp TOPSIS exactly at `h=0`.

Run from this directory:

```bash
python -m pip install -r requirements.txt
python reproduce_ITT2026_results.py
```

Expected final line:

```text
PAPER3_ITT2026_R8_REPRODUCTION: PASS
```

The replay script automatically reconstructs the repository's hash-verified frozen benchmark snapshot when the underlying baseline tables are not exposed directly at repository root. It then reads the 11 frozen case inputs and 46 public mandatory-safeguard rows, adds the four protocol stress-test rows stored here, and reproduces the R8 paper tables and figure.
