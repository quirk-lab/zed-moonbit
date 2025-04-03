use zed::settings::LspSettings;
use zed_extension_api::{self as zed, Result};

struct MoonBitBinary {
    pub path: String,
    pub args: Option<Vec<String>>,
}

struct MoonBitExtension;

impl MoonBitExtension {
    fn language_server_binary(
        &mut self,
        _language_server_id: &zed::LanguageServerId,
        worktree: &zed::Worktree,
    ) -> Result<MoonBitBinary> {
        let binary_settings = LspSettings::for_worktree("moonbit", worktree)
            .ok()
            .and_then(|lsp_settings| lsp_settings.binary);
        let binary_args = binary_settings
            .as_ref()
            .and_then(|binary_settings| binary_settings.arguments.clone());

        if let Some(path) = binary_settings.and_then(|binary_settings| binary_settings.path) {
            return Ok(MoonBitBinary {
                path,
                args: binary_args,
            });
        }

        if let Some(path) = worktree.which("moonbit") {
            return Ok(MoonBitBinary {
                path,
                args: binary_args,
            });
        }

        Err(
            "moonbit must be installed from https://www.moonbitlang.com/download#moonbit-cli-tools or pointed to by the LSP binary settings"
                .to_string(),
        )
    }
}

impl zed::Extension for MoonBitExtension {
    fn new() -> Self {
        Self
    }

    fn language_server_command(
        &mut self,
        language_server_id: &zed::LanguageServerId,
        worktree: &zed::Worktree,
    ) -> Result<zed::Command> {
        let dart_binary = self.language_server_binary(language_server_id, worktree)?;

        Ok(zed::Command {
            command: dart_binary.path,
            args: dart_binary.args.unwrap_or_else(|| {
                vec!["language-server".to_string(), "--protocol=lsp".to_string()]
            }),
            env: Default::default(),
        })
    }
}

zed::register_extension!(MoonBitExtension);
