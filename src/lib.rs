use zed::settings::LspSettings;
use zed_extension_api::{self as zed, serde_json, Result};

struct MoonBitExtension;

impl zed::Extension for MoonBitExtension {
    fn new() -> Self {
        Self
    }

    fn language_server_command(
        &mut self,
        _language_server_id: &zed::LanguageServerId,
        worktree: &zed::Worktree,
    ) -> Result<zed::Command> {
        let moon = worktree.which("moon").ok_or_else(|| {
            "MoonBit toolchain not found. Install or update MoonBit and ensure `moon` is available in PATH."
                .to_string()
        })?;

        Ok(zed::Command {
            command: moon,
            args: vec!["lsp".to_string()],
            env: worktree.shell_env(),
        })
    }

    fn language_server_workspace_configuration(
        &mut self,
        _language_server_id: &zed::LanguageServerId,
        worktree: &zed::Worktree,
    ) -> Result<Option<serde_json::Value>> {
        let settings = LspSettings::for_worktree("moonbit", worktree)
            .ok()
            .and_then(|lsp_settings| lsp_settings.settings.clone())
            .unwrap_or_default();

        Ok(Some(serde_json::json!({
            "moonbit": settings
        })))
    }
}

zed::register_extension!(MoonBitExtension);