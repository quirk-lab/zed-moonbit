#!/usr/bin/env python3
"""
Watch mode for zed-moonbit development.

Watches relevant project files and re-runs validation automatically.
Uses watchexec if available, otherwise falls back to a simple Python poller.

Usage:
    python3 scripts/watch.py                    # watch + validate
    python3 scripts/watch.py --open-zed         # watch + validate + open Zed
    python3 scripts/watch.py --log              # watch + validate + tail Zed log
    python3 scripts/watch.py --open-zed --log   # all together
"""

from __future__ import annotations

import os
import platform
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

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

WATCH_PATHS = [
    "languages/moonbit",
    "src/lib.rs",
    "extension.toml",
    "Cargo.toml",
]

WATCH_EXTENSIONS = ["scm", "toml", "rs"]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"


def _supports_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if platform.system() == "Windows":
        return os.environ.get("WT_SESSION") is not None
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


USE_COLOR = _supports_color()


def _c(code: str, text: str) -> str:
    if USE_COLOR:
        return f"{code}{text}{RESET}"
    return text


def info(msg: str) -> None:
    print(_c(CYAN, f"[watch] {msg}"))


def ok(msg: str) -> None:
    print(_c(GREEN, f"[watch] ✓ {msg}"))


def fail(msg: str) -> None:
    print(_c(RED, f"[watch] ✗ {msg}"), file=sys.stderr)


def warn(msg: str) -> None:
    print(_c(YELLOW, f"[watch] ⚠ {msg}"))


def python_cmd() -> str:
    if platform.system() == "Windows":
        return "python"
    return "python3"


def separator() -> None:
    width = shutil.get_terminal_size((80, 24)).columns
    print(_c(CYAN, "─" * min(width, 80)))


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def run_validation() -> bool:
    """Run query validation. Returns True on success."""
    separator()
    info("Validating Tree-sitter queries...")

    if not NODE_TYPES.exists():
        fail(f"node-types.json not found at {NODE_TYPES}")
        warn("Run grammar-setup first (just grammar-setup / make grammar-setup)")
        return False

    cmd = [python_cmd(), "scripts/validate_queries.py", str(NODE_TYPES), *SCM_FILES]
    result = subprocess.run(cmd)

    if result.returncode == 0:
        ok("All queries valid.")
        return True
    else:
        fail("Validation failed.")
        return False


# ---------------------------------------------------------------------------
# Log tailing (background thread)
# ---------------------------------------------------------------------------

def tail_log_background() -> threading.Thread | None:
    """Start tailing Zed log in a background thread. Returns the thread."""
    try:
        from scripts.zed_log import get_zed_log_path
        log_path = get_zed_log_path()
    except Exception:
        # Fall back to running as subprocess
        cmd = [python_cmd(), "scripts/zed_log.py", "--print-path"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            warn("Could not determine Zed log path.")
            return None
        log_path = Path(result.stdout.strip())

    if not log_path.exists():
        warn(f"Zed log not found at {log_path}")
        return None

    info(f"Tailing Zed log: {log_path}")

    def _tail() -> None:
        try:
            with log_path.open("r", encoding="utf-8", errors="replace") as f:
                # Seek to end
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if line:
                        sys.stdout.write(line)
                        sys.stdout.flush()
                    else:
                        time.sleep(0.5)
        except Exception:
            pass

    t = threading.Thread(target=_tail, daemon=True)
    t.start()
    return t


# ---------------------------------------------------------------------------
# Watchexec-based watcher
# ---------------------------------------------------------------------------

def has_watchexec() -> bool:
    return shutil.which("watchexec") is not None


def run_with_watchexec() -> int:
    """Launch watchexec to re-run validation on file changes."""
    cmd = [
        "watchexec",
        "--clear",
        "--restart",
        "--no-process-group",
    ]

    # Add file extension filters
    for ext in WATCH_EXTENSIONS:
        cmd.extend(["--exts", ext])

    # Add watch paths
    for p in WATCH_PATHS:
        cmd.extend(["--watch", p])

    # The command to run on changes
    cmd.extend(["--", python_cmd(), "scripts/watch.py", "--validate-only"])

    info(f"Starting watchexec: watching {', '.join(WATCH_PATHS)}")
    info("Press Ctrl+C to stop.\n")

    try:
        result = subprocess.run(cmd)
        return result.returncode
    except KeyboardInterrupt:
        return 0


# ---------------------------------------------------------------------------
# Python polling fallback
# ---------------------------------------------------------------------------

def _collect_mtimes(paths: list[str]) -> dict[str, float]:
    """Collect modification times for all watched files."""
    mtimes: dict[str, float] = {}
    for watch_path in paths:
        p = Path(watch_path)
        if p.is_file():
            try:
                mtimes[str(p)] = p.stat().st_mtime
            except OSError:
                pass
        elif p.is_dir():
            for ext in WATCH_EXTENSIONS:
                for f in p.rglob(f"*.{ext}"):
                    try:
                        mtimes[str(f)] = f.stat().st_mtime
                    except OSError:
                        pass
    return mtimes


def run_with_polling(poll_interval: float = 1.0) -> int:
    """Simple polling-based file watcher. Fallback when watchexec is missing."""
    warn("watchexec not found — using Python polling fallback.")
    warn("Install watchexec for a better experience:")
    warn("  cargo install watchexec-cli")
    warn("  brew install watchexec       (macOS)")
    warn("  scoop install watchexec      (Windows)")
    print()

    info(f"Watching {', '.join(WATCH_PATHS)} (polling every {poll_interval}s)")
    info("Press Ctrl+C to stop.\n")

    prev_mtimes = _collect_mtimes(WATCH_PATHS)

    try:
        while True:
            time.sleep(poll_interval)
            curr_mtimes = _collect_mtimes(WATCH_PATHS)

            changed = []
            for path, mtime in curr_mtimes.items():
                if path not in prev_mtimes or prev_mtimes[path] != mtime:
                    changed.append(path)

            if changed:
                for c in changed:
                    info(f"Changed: {c}")
                run_validation()

            prev_mtimes = curr_mtimes
    except KeyboardInterrupt:
        return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Watch mode for zed-moonbit development."
    )
    parser.add_argument(
        "--open-zed", action="store_true",
        help="Open the project in Zed before watching."
    )
    parser.add_argument(
        "--log", action="store_true",
        help="Tail the Zed log in the background."
    )
    parser.add_argument(
        "--validate-only", action="store_true",
        help="Run validation once and exit (used internally by watchexec)."
    )
    parser.add_argument(
        "--no-watchexec", action="store_true",
        help="Force Python polling fallback even if watchexec is available."
    )

    args = parser.parse_args()

    # Internal: just validate and exit (called by watchexec on each change)
    if args.validate_only:
        return 0 if run_validation() else 1

    # Banner
    separator()
    info("zed-moonbit development pipeline")
    separator()

    # Initial validation
    run_validation()

    # Open Zed
    if args.open_zed:
        info("Opening project in Zed...")
        try:
            subprocess.Popen(["zed", "."])
            ok("Zed launched.")
        except FileNotFoundError:
            warn("Could not find `zed` in PATH. Open the project manually.")

    # Start log tailing
    if args.log:
        tail_log_background()

    print()

    # Watch loop
    if not args.no_watchexec and has_watchexec():
        return run_with_watchexec()
    else:
        return run_with_polling()


if __name__ == "__main__":
    # Handle SIGINT gracefully
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))
    raise SystemExit(main())
