# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1] - 2025-05-03
### Added
- Initial release of **IOACollector**, a CLI tool for managing CrowdStrike IOA rules via API.
- Support for two primary operations:
  - `create`: Generate and enable new IOA rules using templates and provided indicators.
  - `delete`: Disable and remove existing IOA rules by ID.
- Built-in template rendering with Jinja2 and YAML serialization support.
- Dry-run mode to safely preview payloads before submission.
- Credential management with environment variable configuration using `.env` file.
- Automatic retry logic for robust API communication.
- CLI argument parsing tailored to each mode (`create`, `delete`).
- Fully documented and modular Python codebase with reusable classes:
  - `APIClient` for authenticated API communication.
  - `IOA` for managing IOA-specific operations.
  - `EnvironmentManager` for handling API credentials.
  - `LoadTemplate` and `RenderedTemplate` for managing rule templates.

### Notes
- This is the first official and production-ready release.
- Designed for security analysts and DevSecOps engineers automating IOA rule operations in CrowdStrike Falcon.