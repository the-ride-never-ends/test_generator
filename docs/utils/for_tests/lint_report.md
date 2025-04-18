# lint_report.py: last updated 11:35 PM on April 17, 2025

**File Path:** `WIP/test_generator/utils/for_tests/lint_report.py`

## Module Description

Script to generate reports for mypy and flake8 linting.

## Table of Contents

### Functions

- [`load_gitignore_patterns`](#load_gitignore_patterns)
- [`should_ignore_file`](#should_ignore_file)
- [`run_linting`](#run_linting)

### Classes

- [`LintResultCollector`](#lintresultcollector)

## Functions

## `load_gitignore_patterns`

```python
def load_gitignore_patterns(gitignore_path)
```

Load patterns from a gitignore file.

**Parameters:**

- `gitignore_path` (`Path`): Path to the gitignore file

**Returns:**

- `Optional[pathspec.PathSpec]`: PathSpec object or None if file doesn't exist

## `should_ignore_file`

```python
def should_ignore_file(file_path, spec)
```

Check if a file should be ignored based on gitignore patterns.

**Parameters:**

- `file_path` (`str`): The file path to check

- `spec` (`Optional[pathspec.PathSpec]`): The PathSpec object with gitignore patterns

**Returns:**

- `bool`: True if the file should be ignored, False otherwise

## `run_linting`

```python
def run_linting(respect_gitignore=False)
```

Run linting and generate reports.

**Parameters:**

- `respect_gitignore` (`bool`): Whether to respect gitignore patterns

**Returns:**

- `Tuple[(bool, Dict[(str, Any)])]`: Tuple of success status and lint results dictionary

## Classes

## `LintResultCollector`

```python
class LintResultCollector(object)
```

Collects and formats linting results for reporting.

**Methods:**

- [`collect_flake8_results`](#collect_flake8_results)
- [`collect_mypy_results`](#collect_mypy_results)
- [`generate_json_report`](#generate_json_report)
- [`generate_markdown_report`](#generate_markdown_report)
- [`update_overall_status`](#update_overall_status)

### `collect_flake8_results`

```python
def collect_flake8_results(self, output)
```

Collect results from flake8 output.

**Parameters:**

- `output` (`str`): Output from flake8 command

**Returns:**

- `Tuple[(bool, int)]`: Tuple of success status and error count

### `collect_mypy_results`

```python
def collect_mypy_results(self, output)
```

Collect results from mypy output.

**Parameters:**

- `output` (`str`): Output from mypy command

**Returns:**

- `Tuple[(bool, int)]`: Tuple of success status and error count

### `generate_json_report`

```python
def generate_json_report(self, output_path)
```

Generate a JSON report of the linting results.

**Parameters:**

- `output_path` (`Path`): Path to write the report to

### `generate_markdown_report`

```python
def generate_markdown_report(self, output_path)
```

Generate a Markdown report of the linting results.

**Parameters:**

- `output_path` (`Path`): Path to write the report to

### `update_overall_status`

```python
def update_overall_status(self)
```

Update the overall status based on mypy and flake8 statuses.
