#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path

TEST_FILES_DIR = Path("tests")
TREE_SITTER_DIR = Path(os.environ.get("TREE_SITTER_DIR", "../tree-sitter-moonbit"))

def run_parse(file_path):
    try:
        subprocess.run(
            ["tree-sitter", "parse", str(file_path.resolve())],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=TREE_SITTER_DIR,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    if not TEST_FILES_DIR.exists():
        print("No tests directory found.")
        return 0

    failures = 0

    for file in TEST_FILES_DIR.glob("*.mbt"):
        ok = run_parse(file)
        if not ok:
            print(f"Failed parsing: {file}")
            failures += 1

    if failures > 0:
        print(f"{failures} parsing failures")
        return 1

    print("All test files parsed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())
