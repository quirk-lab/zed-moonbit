use zed_extension_api::{self as zed, Result};

struct MoonBitExtension;

impl zed::Extension for MoonBitExtension {
    fn new() -> Self {
        Self
    }

    fn language_server_command(
        &mut self,
        language_server_id: &zed::LanguageServerId,
        worktree: &zed::Worktree,
    ) -> Result<zed::Command> {
        if language_server_id.as_ref() == "moonbit-lsp" {
            let path = worktree.which("moonbit-lsp");

            if let Some(path) = path {
                return Ok(zed::Command {
                    command: path,
                    args: vec![],
                    env: Default::default(),
                });
            } else {
                return Err(
                    "The binary 'moonbit-lsp' was not found in your PATH.\n\
                     Make sure you have installed it (e.g., via 'npm install -g @moonbit/moonbit-lsp') \n\
                     and verify that the installation PATH is correctly exposed to Zed's startup environment.".to_string()
                );
            }
        }

        Err(format!("Unknown language server: {}", language_server_id.as_ref()))
    }
}

zed::register_extension!(MoonBitExtension);
