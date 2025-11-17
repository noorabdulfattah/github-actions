#!/usr/bin/env bash
set -euo pipefail

BRANCH="${CATALOG_BRANCH:-unknown}"

echo "Running catalog-sync pull for $BRANCH ..."
catalog-sync pull --from "$BRANCH"

if [[ "$BRANCH" == "catalog-sandbox" ]]; then
  echo "Running promotion from sandbox to main..."
  catalog-sync promote --from "catalog-sandbox" --to "main"
fi