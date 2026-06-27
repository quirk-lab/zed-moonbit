# Contributing to zed-moonbit

Thank you for your interest in contributing to `zed-moonbit`.

This project aims to stay small, maintainable, and technically correct. Contributions are welcome, but they should remain focused, easy to review, and aligned with the MoonBit Tree-sitter grammar and Zed extension behavior.

---

## Before You Start

Before writing code:

1. Check if an issue already exists
2. Open an issue for bugs or feature proposals
3. Wait for feedback before large changes

Small fixes can be submitted directly.

---

## Development Process

### 1. Fork the repository

Fork the repo on GitHub.

### 2. Clone your fork

```bash
git clone https://github.com/<your-username>/zed-moonbit
cd zed-moonbit
```

### 3. Create a branch

```bash
git checkout -b fix/highlights-node
git checkout -b feat/outline-support
```

Use clear, short names.

---

## Making Changes

### Keep changes small

Good PRs:
- fix one invalid node
- improve one `.scm` file
- update one part of docs

Avoid mixing unrelated changes.

---

## Validation (MANDATORY)

Before opening a PR:

Using Just:

```bash
just validate-queries
```

Using Make:

```bash
make validate-queries
```

If Rust code changed:

```bash
cargo check
```

---

## Test in Zed

Run:

```bash
just dev
```

or:

```bash
make dev
```

Windows:

```powershell
pwsh -File scripts/dev.ps1
```

Check logs:

```bash
just zed-log
```

---

## Tree-sitter Rules

- NEVER guess node names
- ALWAYS check:
  - `tree-sitter parse`
  - `node-types.json`
- keep queries minimal
- prefer correctness over coverage

---

## Documentation

Update docs if you change:

- workflow
- commands
- features

Files:

- `README.md`
- `docs/tree-sitter-workflow.md`

---

## CHANGELOG

Update `CHANGELOG.md` if your change is user-visible.

Examples:

- new highlighting support
- outline improvements
- breaking query changes

---

## Pull Request

When ready:

1. Push branch
2. Open PR
3. Describe:
   - what changed
   - why
   - how it was tested

Keep PRs easy to review.

---

## Code Style

### Rust

- simple, linear code
- no overengineering
- comment only when needed

### Tree-sitter

- minimal queries
- no speculative nodes

---

## Final Rule

> A small correct PR is better than a large broken one.