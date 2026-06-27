#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path


IGNORE = {
    "open",
    "close",
    "indent",
    "outdent",
    "item",
    "name",
}

STRING_ONLY_FILES = {
    "languages/moonbit/brackets.scm",
    "languages/moonbit/injections.scm",
}


def load_node_types(path: Path) -> set[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {entry["type"] for entry in data if isinstance(entry, dict) and "type" in entry}


def extract_candidates(text: str) -> list[str]:
    text = re.sub(r";.*", "", text)
    text = re.sub(r'"[^"]*"', "", text)

    candidates = re.findall(r"\(([A-Za-z_][A-Za-z0-9_]*)", text)
    return candidates


def validate_file(path: Path, valid_nodes: set[str]) -> list[str]:
    rel = str(path)
    if rel in STRING_ONLY_FILES:
        return []

    text = path.read_text(encoding="utf-8")
    candidates = extract_candidates(text)

    errors = []
    for node in candidates:
        if node in IGNORE:
            continue
        if node not in valid_nodes:
            errors.append(node)

    return sorted(set(errors))


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: validate_queries.py <node-types.json> <file1.scm> [file2.scm ...]")
        return 2

    node_types_path = Path(sys.argv[1])
    scm_files = [Path(p) for p in sys.argv[2:]]

    if not node_types_path.exists():
        print(f"Missing node-types file: {node_types_path}")
        return 1

    valid_nodes = load_node_types(node_types_path)

    had_errors = False
    for scm in scm_files:
        if not scm.exists():
            print(f"[ERROR] Missing file: {scm}")
            had_errors = True
            continue

        invalid = validate_file(scm, valid_nodes)
        if invalid:
            had_errors = True
            print(f"[ERROR] {scm}")
            for node in invalid:
                print(f"  - invalid node type: {node}")
        else:
            print(f"[OK] {scm}")

    return 1 if had_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())