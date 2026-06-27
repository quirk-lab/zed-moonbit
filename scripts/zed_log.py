#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import platform
import sys
import time
from pathlib import Path


def get_zed_log_path() -> Path:
    system = platform.system()

    if system == "Darwin":
        return Path.home() / "Library" / "Logs" / "Zed" / "Zed.log"

    if system == "Linux":
        return Path.home() / ".local" / "state" / "zed" / "logs" / "Zed.log"

    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA is not set.")
        return Path(appdata) / "Zed" / "logs" / "Zed.log"

    raise RuntimeError(f"Unsupported operating system: {system}")


def print_path() -> int:
    print(get_zed_log_path())
    return 0


def tail_file(path: Path, lines: int = 100) -> int:
    if not path.exists():
        print(f"Log file not found: {path}", file=sys.stderr)
        return 1

    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            content = f.readlines()
            for line in content[-lines:]:
                print(line, end="")

            while True:
                where = f.tell()
                line = f.readline()
                if line:
                    print(line, end="")
                else:
                    time.sleep(0.5)
                    f.seek(where)
    except KeyboardInterrupt:
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Read or tail Zed logs.")
    parser.add_argument("--print-path", action="store_true", help="Print the Zed log path.")
    parser.add_argument("--tail", action="store_true", help="Tail the Zed log.")
    parser.add_argument("--lines", type=int, default=100, help="Number of lines to show before tailing.")

    args = parser.parse_args()

    if args.print_path:
        return print_path()

    if args.tail:
        return tail_file(get_zed_log_path(), lines=args.lines)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())