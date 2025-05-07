# IOACollector - CrowdStrike IOA Rule Automation

## Overview

**IOACollector** is a command-line tool for automating the creation, management, and deletion of **Indicators of Attack (IOA)** rules in **CrowdStrike Falcon**. Designed for incident response workflows, this tool accelerates rule management by interacting with the CrowdStrike API using structured templates and secure authentication.

## Features

- **Secure Authentication** using `.env` stored credentials (no hardcoded secrets).
- **Dry-run mode** to preview payloads before execution.
- **Template-based Rule Creation** using Jinja2 and YAML.
- **Clean and Modular CLI** for easy integration into automated workflows.
- **Retry Logic** for robust API calls in unstable environments.

## CLI Commands

Once installed, the following commands will be available globally:

- `ioacollector-add`: Create and enable a new IOA rule.
- `ioacollector-delete`: Disable and delete an existing IOA rule.
- `ioacollector-config`: Configure your API credentials (CLIENT_ID and CLIENT_SECRET).

## Installation

Install the package from PyPI:

```bash
pip install ioacollector
```

Check if the commands are available:

```bash
ioacollector-add --help
ioacollector-delete --help
ioacollector-config --help
```

### Development Setup

If you'd like to contribute or modify the project, you can easily set up a local development environment by cloning the repository and installing the package in "editable" mode:

```bash
git clone https://github.com/yourusername/ioacollector.git
cd ioacollector
pip3 install -e .
```

This will install the package and allow you to make changes to the source code locally without needing to reinstall the package after each change.

---

## Usage

### Configure API Credentials (Run once)

```bash
ioacollector-config
```

This will store your `CLIENT_ID` and `CLIENT_SECRET` in a local `.env` file.

---

### Create an IOA Rule

```bash
ioacollector-add --rulegroup-id <RULEGROUP_ID> --data <IP_OR_DOMAIN>
```

### Delete an IOA Rule

```bash
ioacollector-delete --rulegroup-id <RULEGROUP_ID> --rule-id <RULE_ID>
```

### Dry-Run Example

```bash
ioacollector-add --rulegroup-id abc123 --data 1.2.3.4 --dry-run
```

---

## Requirements

- Python 3.8+
- CrowdStrike account with access to IOA API
- Dependencies: `requests`, `python-dotenv`, `jinja2`, `pyyaml`, `validators`

The requirements will be automatically installed while installing the package.

## Author

John Requejo

## Creation Date

2025/05/03

## License

This project is open source under the [MIT License](LICENSE).

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for a complete list of updates and release history.