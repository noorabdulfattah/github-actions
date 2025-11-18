#!/usr/bin/env bash
set -euo pipefail

DW_OWNER="${DW_OWNER:-unknown}"

echo "Running catalog-sync pull for $DW_OWNER ..."
catalog-sync pull --from "$DW_OWNER"

if [[ "$DW_OWNER" == "catalog-sandbox" ]]; then
  echo "Running promotion from sandbox to main..."
  catalog-sync promote --from "catalog-sandbox" --to "main"
fi