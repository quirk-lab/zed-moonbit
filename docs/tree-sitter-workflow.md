# Tree-sitter Query Development Workflow

This document describes the workflow for developing and validating Tree-sitter queries in `zed-moonbit`.

---

## Why this matters

If you use invalid node types, Zed will fail:

```text
Error loading highlights query
Invalid node type "..."
```

Never guess node names.

---

## Prerequisites

You need:

- tree-sitter-cli
- jq
- Python 3.x
- MoonBit tree-sitter grammar

Install:

```bash
cargo install --locked tree-sitter-cli
```

or

```bash
npm install -g tree-sitter-cli
```

macOS jq:

```bash
brew install jq
```

---

## Grammar version

Check `extension.toml`:

```toml
rev = "c76eb43a7ea35de24eec13dee1fe22fadb2533d7"
```

Always match this version.

---

## Workflow

1. Inspect node types
2. Inspect AST
3. Write minimal queries
4. Validate
5. Only then open Zed

---

## Clone grammar

```bash
git clone https://github.com/moonbitlang/tree-sitter-moonbit
cd tree-sitter-moonbit
git checkout c76eb43a7ea35de24eec13dee1fe22fadb2533d7
```

---

## Inspect node types

```bash
jq -r '.[].type' src/node-types.json | sort -u
```

Filter:

```bash
jq -r '.[].type' src/node-types.json | grep literal
jq -r '.[].type' src/node-types.json | grep definition
```

Rule:

If it's not in node-types.json → don't use it.

---

## Inspect AST

```bash
tree-sitter parse file.mbt
```

Wrong:

```scheme
(function_item) @item
```

Correct:

```scheme
(function_definition) @item
```

---

## Minimal queries

Start with:

```scheme
(type_identifier) @type
(identifier) @variable
(integer_literal) @number
(string_literal) @string
(comment) @comment
```

---

## Validate queries

Setup:

```bash
make grammar-setup
```

or

```bash
just grammar-setup
```

Validate:

```bash
make validate-queries
```

or

```bash
just validate-queries
```

---

## Logs

Path:

```bash
just zed-log-path
```

Tail:

```bash
just zed-log
```

---

## Dev command

```bash
just dev
```

or

```bash
make dev
```

---

## Windows

```powershell
pwsh -File scripts/dev.ps1
```

Logs:

```bash
python scripts/zed_log.py --tail
```

---

## Safe patterns

```scheme
(identifier)
(type_identifier)
(integer_literal)
(comment)
```

---

## Dangerous patterns

```scheme
(number_literal)
(primitive_type)
(function_item)
```

---

## Outline baseline

```scheme
(function_definition)
(struct_definition)
(enum_definition)
(trait_definition)
(impl_definition)
```

---

## Indents baseline

```scheme
(block_expression)
(array_expression)
(tuple_expression)
```

---

## Rules

- never guess node names
- validate before testing
- keep queries minimal
- fix errors immediately

---

## Dev commands summary

macOS/Linux:

```bash
just dev
just zed-log # via a secondary terminal window/panel

# or to work in watch mode
just watch
just watch-log
```

Make:

```bash
make dev
make zed-log # via a secondary terminal window/panel

# or to work in watch mode
make watch
make watch-log
```

Windows:

```powershell
pwsh -File scripts/dev.ps1
python scripts/zed_log.py --tail # via a secondary terminal window/panel

# or to work in watch mode
pwsh -File scripts/dev.ps1 -Watch
pwsh -File scripts/dev.ps1 -Watch -Log
```

---

## Publish-ready checklist

- no invalid queries
- grammar pinned
- clean README
- working LSP
- tested on real files
- versioned (SemVer)

---

## Final principle

A simple valid query > complex broken query
