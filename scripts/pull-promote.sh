#!/usr/bin/env bash
set -euo pipefail

BRANCH="${CATALOG_BRANCH:-unknown}"

echo "=== pull-promote.sh ==="
echo "Branch         : $BRANCH"
echo "DW_OWNER       : ${DW_OWNER:-}"
echo "API_BASE       : ${API_BASE:-}"
echo "CATALOG_TOKEN? : ${CATALOG_TOKEN:+yes}"

mkdir -p tests/output
TS="$(date -u +'%Y%m%d-%H%M%S')"
OUT_FILE="tests/output/testfile_${BRANCH}_${TS}.txt"

{
  echo "Simulated pull for branch: $BRANCH"
  echo "DW_OWNER=$DW_OWNER"
  echo "API_BASE=${API_BASE:-}"
  echo "CATALOG_TOKEN set: ${CATALOG_TOKEN:+yes}"
  echo "Generated at (UTC): $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
} > "$OUT_FILE"

# Sandbox-specific promotion behavior
if [[ "$BRANCH" == "catalog-sandbox" ]]; then
  echo "Running sandbox promotion logic..."
  echo "Contents are promoted." | tee -a "$OUT_FILE"
fi

echo "Output file: $OUT_FILE"