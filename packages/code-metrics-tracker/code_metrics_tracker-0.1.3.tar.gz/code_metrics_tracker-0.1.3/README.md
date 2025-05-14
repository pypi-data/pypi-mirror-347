# Code Metrics Tracker

[![PyPI Version](https://img.shields.io/pypi/v/code-metrics-tracker.svg)](https://pypi.org/project/code-metrics-tracker/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/code-metrics-tracker.svg)](https://pypi.org/project/code-metrics-tracker/)

A powerful code quality metrics tracking tool for Python projects that helps teams monitor and improve their codebase over time. Code Metrics Tracker leverages three specialized tools to provide comprehensive analysis:

- **cloc**: Counts lines of code, comments, and blank lines across programming languages
- **Ruff**: Identifies linting issues, code style violations, and potential bugs with fast performance
- **Radon**: Analyzes code complexity (cyclomatic complexity) and maintainability

The tracker generates detailed reports focusing on:

- **Lines of code statistics**: Track code volume and distribution by language
- **Linting issues**: Detect and monitor code style, potential bugs, and anti-patterns
- **Cyclomatic complexity**: Identify complex functions and methods that need refactoring
- **Maintainability index**: Measure how maintainable your code is over time

Results are stored in two complementary formats:
1. **JSON snapshots**: Detailed metrics data stored in versioned JSON files for programmatic analysis
2. **Markdown reports**: Human-readable CODE_METRICS.md file that tracks metrics over time with trend indicators

Perfect for teams that want to:
- Track code quality trends over time
- Identify problematic areas in the codebase
- Make data-driven refactoring decisions
- Establish quality standards with measurable metrics
- Integrate metrics tracking into CI/CD pipelines

## Installation

### Install from PyPI

```bash
pip install code-metrics-tracker
```

### Install Required Dependencies

The tool relies on three external tools that need to be installed separately:

#### 1. Install cloc

```bash
# macOS
brew install cloc

# Ubuntu/Debian
sudo apt-get install cloc

# Windows
choco install cloc
```

#### 2. Install Ruff and Radon

These are automatically installed as dependencies when you install code-metrics-tracker, but you can also install them directly:

```bash
pip install ruff radon
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

### Command Overview

- `codeqa init` - Initialize code quality tracking in your project
- `codeqa snapshot` - Create a new code quality snapshot and update CODE_METRICS.md
- `codeqa list` - List all available snapshots
- `codeqa compare` - Compare two snapshots to see trends
- `codeqa report` - Generate a standalone report from a snapshot

### Detailed Usage Examples

#### Initialize a Project

The `init` command sets up your project for code quality tracking by:
- Creating a configuration file (`codeqa.json`)
- Creating a metrics storage directory
- Adding a CODE_METRICS.md file if it doesn't exist

```bash
# Basic initialization with default settings
codeqa init

# After initialization, you can edit codeqa.json to customize
# which directories to include/exclude
```

#### Create Metrics Snapshots

The `snapshot` command analyzes your codebase and:
- Runs code statistics with cloc
- Performs linting checks with Ruff
- Analyzes complexity and maintainability with Radon
- Updates CODE_METRICS.md with the latest metrics
- Stores detailed metrics data as a JSON file

```bash
# Create a snapshot with default settings
codeqa snapshot

# Create a snapshot with a custom report title
codeqa snapshot --title "Post-Refactoring Metrics"
```

#### List Available Snapshots

The `list` command shows all available snapshots:

```bash
# List all snapshots with their dates and filenames
codeqa list
```

Example output:
```
Available snapshots:
- May 13, 2025 (metrics_20250513_164444.json)
- April 19, 2025 (metrics_20250419_150845.json)
- April 18, 2025 (metrics_20250418_183327.json)
```

#### Compare Snapshots

The `compare` command allows you to track changes between two snapshots:

```bash
# Compare by using snapshot filenames
codeqa compare --first generated/metrics/metrics_20250418_183327.json --second generated/metrics/metrics_20250513_164444.json

# Compare and save the report to a file
codeqa compare --first generated/metrics/metrics_20250418_183327.json --second generated/metrics/metrics_20250513_164444.json --output comparison_report.md

# Compare using indexes from the list command (1-based)
codeqa compare --first 2 --second 1 --output comparison_report.md
```

The comparison report highlights:
- Changes in lines of code
- Changes in linting issues
- Changes in complex functions
- Changes in maintainability
- Trend analysis with percentage changes

#### Generate Standalone Reports

The `report` command generates a standalone report from a specific snapshot:

```bash
# Generate a report from a specific snapshot
codeqa report --snapshot generated/metrics/metrics_20250513_164444.json

# Save the report to a specific file
codeqa report --snapshot generated/metrics/metrics_20250513_164444.json --output quality_report.md

# Generate a report using the snapshot index from the list command (1-based)
codeqa report --snapshot 1 --output quality_report.md
```

The standalone report includes:
- Summary statistics
- Code distribution by language
- Top complex files and functions
- Files with linting issues
- Files with low maintainability

## Output Formats

### CODE_METRICS.md

The main output file is `CODE_METRICS.md`, which contains:

- A header section explaining the metrics
- Historical snapshots with dates
- Summary statistics for each snapshot
- Code statistics by language
- Lists of complex files and functions
- Files with linting issues
- Files with low maintainability
- Trend analysis compared to the previous snapshot
- Analysis of critical issues to address

#### Sample CODE_METRICS.md Excerpt

```markdown
# Code Quality Metrics

This file tracks code quality metrics over time to help monitor and improve our codebase.

## Metrics Definitions

### Ruff Metrics
- **Issues Count**: Total number of linting issues detected by Ruff
- **Issues by Type**: Distribution of error types (unused imports, undefined names, etc.)

### Radon Complexity Metrics (CC)
- **A**: CC score 1-5 (low complexity)
- **B**: CC score 6-10 (moderate complexity)
- **C**: CC score 11-20 (high complexity)
- **D**: CC score 21-30 (very high complexity)
- **E**: CC score 31-40 (extremely high complexity)
- **F**: CC score 41+ (alarming complexity)

## Historical Snapshots

### May 13, 2025

#### Summary

| Metric | Value | 
|--------|-------|
| Lines of Code | 123,739 |
| Files | 699 |
| Comments | 35,493 |
| Linting Issues | 376 |
| Cyclomatic Complexity | A:751 B:102 C:253 D:8 E:3 F:346 |
| Maintainability Index | A:215 B:1 C:3 |

#### Analysis
- Critical issues to address:
  - 376 linting issues
  - 610 high complexity functions
  - 3 files with low maintainability
```

### Comparison Reports

Comparison reports highlight changes between snapshots:

```markdown
## Comparison: April 19, 2025 vs May 13, 2025

### Summary

| Metric | April 19, 2025 | May 13, 2025 | Change |
|--------|---------|---------|--------|
| Lines of Code | 26,423 | 123,739 | ↑ 97316 (368.3%) |
| Linting Issues | 296 | 376 | ↑ 80 (27.0%) |
| Complex Functions (C-F) | 474 | 610 | ↑ 136 (28.7%) |
| Low Maintainability Files | 3 | 3 | ↑ 0 (0.0%) |

### Analysis

- Code Size: Increased by 97,316 lines
- Code Quality: Mixed changes
- Most Significant Change: Complex Functions
```

### JSON Data Files

Each snapshot also produces a detailed JSON file containing:

- Complete metrics data
- Timestamp information
- Raw data from all tools (cloc, Ruff, Radon)
- Detailed breakdowns by file and function
- Language statistics

These JSON files can be used for:
- Custom analysis scripts
- Integration with other tools
- Historical data processing
- Visualization dashboards

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
      - name: Install cloc
        run: sudo apt-get install -y cloc
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install code-metrics-tracker
      - name: Generate code quality snapshot
        run: codeqa snapshot
      - name: Commit updated CODE_METRICS.md
        uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: "Update code quality metrics"
          file_pattern: CODE_METRICS.md generated/metrics/*
```

## Development Guide

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/AgileWorksZA/codeqa.git
cd codeqa
```

2. Install in development mode:
```bash
pip install -e .
```

3. Install development dependencies:
```bash
pip install build twine
```

### Creating a New Release

1. Update version numbers in both files:
   - `setup.py` - Update the `version` parameter
   - `codeqa/__init__.py` - Update the `__version__` variable

2. Update the README.md with any new features or changes

3. Build the package:
```bash
rm -rf dist/ build/ *.egg-info/
python -m build
```

4. Test the package locally:
```bash
pip install dist/*.whl
```

### Publishing to PyPI

1. Install publishing tools if you haven't already:
```bash
pip install twine
```

2. Create a `.pypirc` file in your home directory with your PyPI credentials:
```ini
[pypi]
username = your_username
password = your_password
```

3. Upload to PyPI:
```bash
python -m twine upload dist/*
```

4. Alternatively, use a token for authentication:
```bash
python -m twine upload --username __token__ --password your-pypi-token dist/*
```

5. Verify the package is available on PyPI:
https://pypi.org/project/code-metrics-tracker/

## Common Workflows and Use Cases

### 1. Initial Code Quality Baseline

When starting to monitor a project, first create a baseline:

```bash
# Set up code quality tracking
codeqa init

# Edit codeqa.json to include your relevant code paths
# e.g., {"include_paths": ["src", "lib", "tests"], "exclude_patterns": ["venv", "node_modules"]}

# Create initial baseline snapshot
codeqa snapshot
```

### 2. Regular Quality Monitoring

Integrate into your development workflow:

```bash
# Before starting work (to see current state)
git pull
codeqa list  # Check latest snapshot date

# After significant changes (to track progress)
codeqa snapshot
git add CODE_METRICS.md generated/metrics
git commit -m "Update code quality metrics"
```

### 3. Pre-Release Quality Check

Before releasing a new version:

```bash
# Create a pre-release snapshot
codeqa snapshot --title "Pre-release v1.2.0"

# Compare with the previous snapshot
codeqa list  # Note the snapshot indexes
codeqa compare --first 2 --second 1 --output release_quality_report.md

# Review the report and address critical issues before release
```

### 4. Refactoring Impact Analysis

Measure the impact of refactoring efforts:

```bash
# Create pre-refactoring snapshot
codeqa snapshot --title "Pre-refactoring"

# (Perform your refactoring work)

# Create post-refactoring snapshot
codeqa snapshot --title "Post-refactoring"

# Compare the snapshots
codeqa list
codeqa compare --first 2 --second 1 --output refactoring_impact.md
```

### 5. Team Code Quality Review

Regular team review of code quality:

```bash
# Generate the latest snapshot
codeqa snapshot

# Generate a standalone report for the meeting
codeqa report --snapshot 1 --output team_review.md

# During the meeting, focus on:
# - Top complex functions that need refactoring
# - Linting issues to address
# - Files with low maintainability
# - Trends compared to previous review
```

### Committing Changes to GitHub

1. Add and commit your changes:
```bash
git add .
git commit -m "Release version X.Y.Z with [brief description]"
```

2. Push to GitHub:
```bash
git push origin main
```

3. Create a GitHub release:
   - Go to the repository's Releases page
   - Click "Draft a new release"
   - Tag version: vX.Y.Z
   - Title: Version X.Y.Z
   - Description: Add release notes
   - Publish release

## License

MIT