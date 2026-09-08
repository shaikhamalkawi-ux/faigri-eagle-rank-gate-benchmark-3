#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-$HERE/FAIGRI_EAGLE_PAPER3_RANK_GATE_BENCHMARK_V3_GITHUB_PUBLIC_SNAPSHOT_20260908.tar.xz}"
cat \
  "$HERE/base64/part_00.b64" \
  "$HERE/base64/part_01.b64" \
  "$HERE/base64/part_02.b64" \
  "$HERE/base64/part_03.b64" \
  "$HERE/base64/part_04.b64" \
  | base64 -d > "$OUT"
EXPECTED="a170e43efb3cc193ca6ce031c4a2d76f2a6a26520bd48062a69b043ca965717b"
ACTUAL="$(sha256sum "$OUT" | awk '{print $1}')"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "SNAPSHOT_SHA256: FAIL expected=$EXPECTED actual=$ACTUAL" >&2
  exit 1
fi
xz -t "$OUT"
echo "SNAPSHOT_SHA256: PASS $ACTUAL"
echo "SNAPSHOT_XZ_TEST: PASS"
echo "SNAPSHOT_RECONSTRUCT: PASS"
