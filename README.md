[![CI](https://github.com/Metalymph/zed-moonbit/actions/workflows/ci.yml/badge.svg)](https://github.com/Metalymph/zed-moonbit/actions/workflows/ci.yml)

# MoonBit Community

MoonBit language support for the Zed editor.

This extension provides Tree-sitter-based syntax highlighting and integrates the MoonBit Language Server (`moonbit-lsp`).

---

## Features

- Syntax highlighting (Tree-sitter)
- MoonBit 0.10 grammar and syntax coverage
- LSP integration (`moonbit-lsp`)
- Outline support (basic)
- Brackets + indentation

---

## Status

Early-stage but functional.

The main focus is correctness of Tree-sitter queries. Coverage is intentionally minimal and will evolve with the upstream MoonBit grammar.

---

## Requirements

- Zed Editor
- `moonbit-lsp` in PATH
- Rust toolchain (for dev only)

Install LSP:

```
npm install -g @moonbit/moonbit-lsp
```

Verify:

```
which moonbit-lsp
```

---

## Installation (Dev)

Clone:

```
git clone https://github.com/Metalymph/zed-moonbit
cd zed-moonbit
```

In Zed:

- open command palette
- run: `zed: install dev extension`

### Note: For the official releases look at [Releases](https://github.com/Metalymph/zed-moonbit/releases).

## Optional: associate `moon.pkg` with MoonBit

Since `moon.pkg` is a MoonBit package manifest rather than a `.mbt` source file, you may want to associate it manually in Zed settings:

```json
{
  "file_types": {
    "MoonBit": ["moon.pkg"]
  }
}
```

Zed currently does not support matching exact filenames in language extensions,
so this must be configured manually.

---

## Development Workflow

### Core commands

Using Just:

```
just dev
just validate-queries
just test-syntax
just zed-log
```

Using Make:

```
make dev
make validate-queries
make test-syntax
make zed-log
```

Windows (PowerShell):

```
pwsh -File scripts/dev.ps1
```

---

### What `dev` does

- validates Tree-sitter queries
- prints Zed log path
- opens project in Zed

---

## Tree-sitter Development

All syntax behavior is driven by:

```
languages/moonbit/*.scm
```

You **must not guess node names**.

Use:

```
make validate-queries
```

or:

```
just validate-queries
```

If queries are invalid, Zed will fail to load the language.

---

## Debugging

Show log path:

```
just zed-log-path
```

Tail logs:

```
just zed-log
```

Common error:

```
Invalid node type "..."
```

Fix by checking:

```
tree-sitter parse file.mbt
```

and:

```
src/node-types.json
```

---

## Project Structure

```
src/lib.rs                -> Rust extension entry point
extension.toml           -> extension manifest
languages/moonbit/       -> Tree-sitter config + queries
scripts/                 -> validation + dev tools
```

---

## Design Principles

- minimal queries > complex broken queries
- no guessed AST nodes
- validate before testing
- keep extension logic thin (LSP does the heavy work)

---

## Roadmap

- improve query coverage
- refine outline support
- stabilize indentation rules
- prepare for extension registry release

---

## Contributing

Small, focused changes only.

Before opening a PR:

```
make validate-queries
```

---

## Troubleshooting

Generally speaking, if you meet any problem, open an issue on GitHub.

### Error: `failed to compile grammar 'moonbit'`

If you see this error while installing the extension, it may be caused by a corrupted or conflicting local grammar cache in Zed.

Zed clones the Tree-sitter grammar into a local `grammars/moonbit` directory. If that folder already exists but is not a valid Git repository (or does not match the expected remote), installation can fail.

**Fix:**

1. Locate Zed’s extensions/grammars directory (depends on your OS).
2. Delete the `grammars` folder (or at least `grammars/moonbit`).
3. Restart Zed.
4. Reinstall the extension.

This is a local state issue and not a problem with the extension itself.

---

## License

MIT
