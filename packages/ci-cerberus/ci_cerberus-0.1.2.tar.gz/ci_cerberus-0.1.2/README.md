# CI Cerberus

CI Cerberus is a security tool that scans GitHub workflows for known vulnerable actions using the NIST National Vulnerability Database (NVD) API.

## Installation

```bash
pip install ci-cerberus
```

## Usage

```bash
ci-cerberus [options] <path-to-workflow>
```

For example:
```bash
ci-cerberus .github/workflows/build.yml
```

## Features

- Scans GitHub Actions workflows for security vulnerabilities
- Uses NIST's National Vulnerability Database (NVD) API for up-to-date vulnerability information
- Easy to integrate into your CI/CD pipeline
- Supports local workflow file scanning

## Requirements

- Python 3.8 or higher
- Internet connection (for NVD API access)

## Contributing

### Environment Setup

#### Pre-Commit Hooks
This project makes use of pre-commit hooks in order to maintain a consistent codebase regardless of personal opinion or preferred coding style.

To do this, the following tools are run in a pre-commit hook:
1. Black
2. ISort
3. flake8

To set up the development environment:

```bash
pip install -e ".[dev]"
pre-commit install
```

## License

[License details here]

## Author

Gavin Roderick (gavin.roderick@pm.me)
