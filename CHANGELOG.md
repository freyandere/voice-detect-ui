# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-07-05

### Added

- Initial project structure and onboarding.
- Gradio-based web UI with EN/RU localization.
- Model loader for HuggingFace GGUF models.
- Audio preprocessing (resampling to 16kHz).
- Stub prediction functions for age/gender, emotion, speaker verification.
- Multi-language support (English, Russian).
- OLED-themed UI with real-time visualizations.
- Comprehensive documentation: README, ARCHITECTURE, QUICKSTART, PERFORMANCE, TROUBLESHOOTING.
- `.hermes.md` AI development guide.
- Python packaging with `pyproject.toml`.
- `.gitignore` with Python/IDE/OS patterns.
- Test suite with unit and integration tests.

### Changed

- None (initial release).

### Security

- Local-first processing: no external API calls.
- No code execution from user uploads.
