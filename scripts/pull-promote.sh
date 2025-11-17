#!/usr/bin/env bash
set -euo pipefail

BRANCH="${CATALOG_BRANCH:-unknown}"

echo "Running catalog-sync pull for $BRANCH ..."
catalog-sync pull --branch "$BRANCH"

if [[ "$BRANCH" == "catalog-sandbox" ]]; then
  echo "Running promotion from sandbox to main..."
  catalog-sync promote --from-branch "catalog-sandbox" --to-branch "catalog-main"
fi