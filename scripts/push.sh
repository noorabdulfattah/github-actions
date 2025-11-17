#!/usr/bin/env bash
set -euo pipefail

echo "=== push.sh ==="
echo "DW_OWNER       : ${DW_OWNER:-}"
echo "API_BASE       : ${API_BASE:-}"
echo "CATALOG_TOKEN? : ${CATALOG_TOKEN:+yes}"
echo "ENVIRONMENT    : ${ENVIRONMENT:-}"

mkdir -p tests/push-output
TS="$(date -u +'%Y%m%d-%H%M%S')"
OUT_FILE="tests/push-output/push_run_${TS}.txt"

{
  echo "Simulated push for DW_OWNER=$DW_OWNER"
  echo "API_BASE=${API_BASE:-}"
  echo "CATALOG_TOKEN set: ${CATALOG_TOKEN:+yes}"
  echo "ENVIRONMENT=${ENVIRONMENT:-}"
  echo "Generated at (UTC): $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
} > "$OUT_FILE"

echo "Push output file: $OUT_FILE"