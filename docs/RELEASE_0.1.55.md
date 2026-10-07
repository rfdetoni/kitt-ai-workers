# kitt-ai-workers 0.1.55 — Local-only STT fallback

The openai-whisper fallback resolves an existing checkpoint path when local_files_only is enabled and fails before invoking its download-capable loader when absent. CPU retries preserve the faster-whisper local-only and worker/thread options. Workers, Evals and Evolution align their Agent and Protocol locks with this ecosystem release.

## Verification

Regression checks cover the concrete bugs fixed by this release. Native changes are validated with Rust formatting, Clippy, workspace tests and a Python 3.14 wheel integration. Live provider accounts and STT model inference are not part of these local checks.
