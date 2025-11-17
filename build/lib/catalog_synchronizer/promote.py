# src/catalog_synchronizer/promote.py

from __future__ import annotations
import logging

log = logging.getLogger(__name__)


def run_promote(
    *,
    owner: str,
    token: str,
    api_base: str,
    from_branch: str,
    to_branch: str,
) -> None:
    """
    Promote content from sandbox (from_branch) to main (to_branch).
    """
    log.info(
        "Running promote: owner=%s from=%s to=%s api_base=%s",
        owner, from_branch, to_branch, api_base
    )
    # TODO: your real promotion logic:
    # - compare / merge configs
    # - update state