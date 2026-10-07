# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-10-07

### Added
- **Production Modular Architecture**: Refactored monolithic implementation into clean `role_recommendation` package with separate modules (`data`, `models`, `recommender`, `evaluation`, `cli`, `synthesize`).
- **Modern Packaging Standard**: Added `pyproject.toml` with setuptools build-backend and PEP 621 metadata.
- **Unified Command-Line Interface**: Introduced `role-recommendation` CLI with subcommands: `stats`, `mine`, `evaluate`, `synthesize`.
- **Comprehensive Test Suite**: 23 unit and integration test cases covering TF-IDF models, cosine distance, statistical confirmation, role clustering, and CLI invocations.
- **Open-Source Infrastructure**: Added `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, Pull Request template, and structured GitHub Issue templates.
- **Continuous Integration**: Configured automated GitHub Actions workflows for dependency graph generation and multi-platform test verification.

### Changed
- Replaced runtime dynamic pip installs with declarative package dependencies.
- Standardized logging using Python's standard `logging` library instead of raw prints.
- Ensured deterministic evaluation with reproducible random seeds (`random_state=42`).
