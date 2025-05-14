# CodeQA

A code quality metrics tracking tool for Python projects, focusing on:

- Lines of code statistics
- Linting issues (using Ruff)
- Cyclomatic complexity (using Radon)
- Maintainability index (using Radon)

## Installation

```bash
pip install codeqa
```

## Quick Start

1. Initialize code quality tracking in your project:

```bash
codeqa init
```

2. Create a code quality snapshot:

```bash
codeqa snapshot
```

3. View the generated CODE_METRICS.md file for detailed metrics.

## Features

- Track code quality metrics over time
- Generate formatted Markdown reports
- Compare snapshots to identify trends
- Highlight critical issues to address
- Configurable for different project structures

## Commands

- `codeqa init` - Initialize code quality tracking in your project
- `codeqa snapshot` - Create a new code quality snapshot
- `codeqa list` - List all available snapshots
- `codeqa compare` - Compare two snapshots to see trends
- `codeqa report` - Generate a standalone report from a snapshot

## Configuration

The tool uses a `codeqa.json` configuration file to determine which directories to analyze, focusing only on code maintained by your team.

Example configuration:

```json
{
  "include_paths": ["src", "tests"],
  "exclude_patterns": ["venv", "site-packages", "__pycache__", ".pyc"]
}
```

## GitHub Actions Integration

Add this to your GitHub Actions workflow to automatically track code quality metrics:

```yaml
name: Code Quality Metrics

on:
  push:
    branches: [ main ]

jobs:
  code-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install codeqa
      - name: Generate code quality snapshot
        run: codeqa snapshot
      - name: Commit updated CODE_METRICS.md
        uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: "Update code quality metrics"
          file_pattern: CODE_METRICS.md generated/metrics/*
```

## License

MIT