# view_report.py: last updated 02:01 PM on April 15, 2025

**File Path:** `WIP/test_generator/utils/for_tests/view_report.py`

## Module Description

Simple viewer for test reports.

## Table of Contents

### Functions

- [`print_color`](#print_color)
- [`view_report`](#view_report)
- [`_display_json_report`](#_display_json_report)
- [`_display_markdown_report`](#_display_markdown_report)
- [`main`](#main)

## Functions

## `print_color`

```python
def print_color(text, color=None)
```

Print colored text.

## `view_report`

```python
def view_report(report_path, format_type='summary')
```

View a test report file.

**Parameters:**

- `report_path` (`Any`): Path to the report file

- `format_type` (`Any`): Type of report to show (summary, details, full)

## `_display_json_report`

```python
def _display_json_report(report, format_type)
```

Display a JSON report.

## `_display_markdown_report`

```python
def _display_markdown_report(report_path)
```

Display a Markdown report.

## `main`

```python
def main()
```

Main entry point.
