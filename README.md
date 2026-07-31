[![CI](https://github.com/quirk-lab/zed-moonbit/actions/workflows/ci.yml/badge.svg)](https://github.com/quirk-lab/zed-moonbit/actions/workflows/ci.yml)

# MoonBit for Zed

Official MoonBit language support for the Zed editor.

This extension provides Tree-sitter-based syntax highlighting together with the native MoonBit Language Server (`moon lsp`).

---

## Features

- Tree-sitter syntax highlighting
- Partial MoonBit 0.10.4 syntax support (literal Iterators and Bytes interpolation are locked by `tree-sitter-moonbit` current support)
- Native MoonBit LSP integration (`moon lsp`)
- Outline support
- Bracket matching
- Indentation support

---

## Status

Functional and actively maintained.

The extension intentionally keeps its Rust implementation minimal and delegates language intelligence to the official MoonBit Language Server while following the upstream Tree-sitter grammar.

The extension tracks the upstream MoonBit Tree-sitter grammar and native MoonBit language server.

Syntax support is limited by the currently pinned upstream grammar revision and may not yet cover every feature introduced in the latest MoonBit release.

---

## Requirements

- Zed Editor
- MoonBit 0.10.4 or newer

Verify your installation:

```sh
moon version
```

The language server is included with the MoonBit toolchain:

```sh
moon lsp
```

No separate npm package is required.

---

## Installation (Development)

Clone the repository:

```sh
git clone https://github.com/quirk-lab/zed-moonbit
cd zed-moonbit
```

Then in Zed:

- Open the Command Palette
- Run:

```
zed: install dev extension
```

Official releases are available from:

https://github.com/quirk-lab/zed-moonbit/releases

---

## Optional: associate `moon.pkg` with MoonBit

Since `moon.pkg` is a MoonBit package manifest rather than a source file, you may want to associate it manually:

```json
{
  "file_types": {
    "MoonBit": ["moon.pkg"]
  }
}
```

Zed currently cannot associate languages with exact filenames automatically.

---

## Development

Using Just:

```sh
just dev
just validate-queries
just test-syntax
just zed-log
```

Using Make:

```sh
make dev
make validate-queries
make test-syntax
make zed-log
```

Windows:

```powershell
pwsh -File scripts/dev.ps1
```

---

## Tree-sitter Development

Tree-sitter queries live in:

```text
languages/moonbit/
```

Always validate queries after making changes:

```sh
just validate-queries
```

or

```sh
make validate-queries
```

Never guess node names.

---

## Debugging

Print the Zed log path:

```sh
just zed-log-path
```

Tail logs:

```sh
just zed-log
```

If you encounter errors such as:

```text
Invalid node type "..."
```

verify the syntax tree using:

```sh
tree-sitter parse example.mbt
```

and compare it with:

```text
src/node-types.json
```

---

## Project Structure

```text
src/lib.rs              Rust extension entry point
extension.toml          Extension manifest
languages/moonbit/      Tree-sitter configuration and queries
scripts/                Development utilities
```

---

## Design Principles

- Thin extension
- Native MoonBit tooling
- Upstream-first grammar
- Minimal, maintainable queries
- Validate before testing

---

## Roadmap

- Improve query coverage
- Refine outline support
- Improve indentation rules
- Track new MoonBit language releases

---

## Contributing

Small, focused pull requests are preferred.

Before opening a PR, always run:

```sh
just validate-queries
```

---

## Troubleshooting

### Error: `failed to compile grammar 'moonbit'`

This is usually caused by a corrupted local Tree-sitter grammar cache.

To fix:

1. Close Zed.
2. Delete the local `grammars/moonbit` directory (or the entire `grammars` directory).
3. Restart Zed.
4. Reinstall the extension.

This is a local cache issue rather than an extension bug.

---

## License

MIT