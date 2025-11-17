#!/usr/bin/env bash
set -euo pipefail

echo "Running catalog-sync push..."
catalog-sync push --env "${ENVIRONMENT:-prod}"
