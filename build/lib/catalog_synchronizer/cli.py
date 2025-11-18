# src/catalog_synchronizer/cli.py

from __future__ import annotations
import argparse
import logging
import os

from .pull import main as pull_mod
from .push import main as push_mod
from .promote import main as promote_mod


def _env_or_default(name: str, default: str | None = None, required: bool = False) -> str:
    variable = os.getenv(name, default)
    if required and not variable:
        raise SystemExit(f"Missing required env var: {name}")
    return variable


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="catalog-sync",
        description="Synchronize data catalog projects/configs.",
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
        help="Auth token (default: DW_AUTH_TOKEN env).",
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
        or _env_or_default("DW_AUTH_TOKEN", required=True)
    )

    if args.command == "pull":
        pull_mod(
            owner=args.from_catalog or owner,
            token=token,
            api_base=api_base,
        )

    elif args.command == "promote":
        promote_mod(
            owner=args.from_catalog or owner,
            token=token,
            api_base=api_base,
            target=args.to_catalog,
        )

    elif args.command == "push":
        push_mod(
            owner=args.to_catalog or owner,
            token=token,
            api_base=api_base,
        )

    else:
        parser.error(f"Unknown command: {args.command}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
