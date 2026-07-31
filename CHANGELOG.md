# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-07-31

### Changed

- Replaced the npm-based `@moonbit/moonbit-lsp` integration with the native MoonBit language server provided by `moon lsp`.
- Updated the pinned upstream `tree-sitter-moonbit` grammar revision.
- Simplified the Rust extension implementation by delegating language-server installation and updates to the MoonBit toolchain.
- Updated the README to document the native MoonBit toolchain requirement and the official `quirk-lab/zed-moonbit` repository.
- Renamed and updated the syntax fixture to track features supported by the pinned upstream grammar.

### Removed

- Removed automatic installation and update checks for `@moonbit/moonbit-lsp`.
- Removed the runtime dependency on Node.js and npm.
- Removed the extension-managed language-server cache and installation status handling.

### Fixed

- Preserved forwarding of MoonBit workspace LSP settings when using the native language server.

## [0.1.7] - 2026-07-01

### Fixed

- Restored automatic installation of the MoonBit language server.
- Restored workspace configuration forwarding for MoonBit LSP settings.
- Restored the `moonbit` language server ID for compatibility with existing Zed settings.

## [0.1.6] - 2026-06-14

### Changed

- Updated the Tree-sitter grammar pin for MoonBit 0.10 syntax.
- Added highlighting for trait and impl method names and the `<+` and `<?` operators.

### Added

- Added a MoonBit 0.10 syntax fixture and fixture parsing command.

## [0.1.0] - 2024-XX-XX

### Added

- Added base project structure.
- Initial LSP integration with `moonbit-lsp`.
- Language configuration for MoonBit files (`.mbt`).
- Initial Tree-sitter queries for highlighting, brackets, indentation, and outline support.
- Initial documentation for open-source standards.