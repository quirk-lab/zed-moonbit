#!/usr/bin/env python3
"""
Dev entry point for zed-moonbit.

Validates queries and optionally opens Zed.
Use --watch to enter watch mode (continuous validation on file changes).
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path


GRAMMAR_COMMIT = os.environ.get(
    "GRAMMAR_COMMIT",
    "c76eb43a7ea35de24eec13dee1fe22fadb2533d7",
)

TREE_SITTER_DIR = Path(os.environ.get("TREE_SITTER_DIR", "../tree-sitter-moonbit"))
NODE_TYPES = TREE_SITTER_DIR / "src" / "node-types.json"

SCM_FILES = [
    "languages/moonbit/highlights.scm",
    "languages/moonbit/outline.scm",
    "languages/moonbit/indents.scm",
    "languages/moonbit/brackets.scm",
    "languages/moonbit/injections.scm",
]


def run(cmd: list[str], check: bool = True) -> int:
    print("+", " ".join(cmd))
    result = subprocess.run(cmd)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result.returncode


def ensure_node_types() -> None:
    if NODE_TYPES.exists():
        return

    print(f"Missing {NODE_TYPES}", file=sys.stderr)
    print("Run grammar setup first.", file=sys.stderr)
    print("Suggested command:", file=sys.stderr)
    print("  just grammar-setup", file=sys.stderr)
    print("or", file=sys.stderr)
    print("  make grammar-setup", file=sys.stderr)
    raise SystemExit(1)


def python_cmd() -> str:
    if platform.system() == "Windows":
        return "python"
    return "python3"


def open_zed(project_dir: Path) -> None:
    try:
        run(["zed", str(project_dir)], check=True)
    except FileNotFoundError:
        print("Could not find `zed` in PATH.", file=sys.stderr)
        print("Open the project manually in Zed.", file=sys.stderr)
        raise SystemExit(1)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="zed-moonbit dev workflow.")
    parser.add_argument(
        "--watch", action="store_true",
        help="Enter watch mode after initial validation."
    )
    parser.add_argument(
        "--log", action="store_true",
        help="Tail Zed log (in watch mode, runs in background)."
    )
    args = parser.parse_args()

    # If --watch, delegate to watch.py with appropriate flags
    if args.watch:
        cmd = [python_cmd(), "scripts/watch.py", "--open-zed"]
        if args.log:
            cmd.append("--log")
        return subprocess.run(cmd).returncode

    # Standard dev flow
    project_dir = Path.cwd()

    ensure_node_types()

    print("Validating Tree-sitter queries...")
    run([python_cmd(), "scripts/validate_queries.py", str(NODE_TYPES), *SCM_FILES])

    print("\nZed log path:")
    run([python_cmd(), "scripts/zed_log.py", "--print-path"])

    print("\nOpening project in Zed...")
    open_zed(project_dir)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
