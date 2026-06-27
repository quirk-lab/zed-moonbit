# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.7] - 2026-06-27
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
- Initial Tree-sitter queries (highlights, brackets, indents, outline).
- Initial documentation for open-source standards.
