# src/catalog_synchronizer/cli.py

from __future__ import annotations
import argparse
import logging
import os

from . import pull as pull_mod
from . import push as push_mod
from . import promote as promote_mod


def _env_or_default(name: str, default: str | None = None, required: bool = False) -> str:
    v = os.getenv(name, default)
    if required and not v:
        raise SystemExit(f"Missing required env var: {name}")
    return v


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="catalog-sync",
        description="Synchronize data.world catalog projects/configs.",
    )

    # Global options (can override env)
    parser.add_argument(
        "--owner",
        default=None,
        help="DW owner/organization (default: DW_OWNER env).",
    )
    parser.add_argument(
        "--api-base",
        default=None,
        help="API base URL (default: API_BASE env).",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="Auth token (default: CATALOG_TOKEN or DW_AUTH_TOKEN env).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v, -vv).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # pull
    pull_p = subparsers.add_parser(
        "pull",
        help="Pull projects/files from data catalog into the repo.",
    )
    pull_p.add_argument(
        "--from",
        dest="from_catalog",
        required=True,
        help="Source catalog/org name (e.g., catalog-sandbox, main).",
    )

    # promote
    promote_p = subparsers.add_parser(
        "promote",
        help="Promote content from sandbox catalog to main catalog.",
    )
    promote_p.add_argument(
        "--from",
        dest="from_catalog",
        required=True,
        help="Source catalog (e.g., catalog-sandbox).",
    )
    promote_p.add_argument(
        "--to",
        dest="to_catalog",
        required=True,
        help="Target catalog (e.g., main).",
    )

    # push
    push_p = subparsers.add_parser(
        "push",
        help="Push promoted projects to the target catalog",
    )
    push_p.add_argument(
        "--to",
        dest="to_catalog",
        required=True,
        help="Target catalog (e.g., main).",
    )

    return parser


def configure_logging(verbosity: int) -> None:
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    configure_logging(args.verbose)

    owner = args.owner or _env_or_default("DW_OWNER", required=True)
    api_base = args.api_base or _env_or_default("API_BASE", required=True)
    token = (
        args.token
        or os.getenv("CATALOG_TOKEN")
        or _env_or_default("DW_AUTH_TOKEN", required=True)
    )

    if args.command == "pull":
        # here we interpret "from_catalog" as the catalog/branch to pull from
        pull_mod.run_pull(
            owner=owner,
            token=token,
            api_base=api_base,
            branch=args.from_catalog,
        )

    elif args.command == "promote":
        promote_mod.run_promote(
            owner=owner,
            token=token,
            api_base=api_base,
            from_branch=args.from_catalog,
            to_branch=args.to_catalog,
        )

    elif args.command == "push":
        # adjust signature if your run_push expects a target catalog
        push_mod.run_push(
            owner=owner,
            token=token,
            api_base=api_base,
            # e.g., target_catalog=args.to_catalog
        )

    else:
        parser.error(f"Unknown command: {args.command}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())