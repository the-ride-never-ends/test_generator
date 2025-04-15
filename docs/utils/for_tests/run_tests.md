# run_tests.py: last updated 03:56 PM on April 15, 2025

**File Path:** `/home/kylerose1946/claudes_toolbox/WIP/test_generator/utils/for_tests/run_tests.py`

## Module Description

Script to run all tests for Test Generator and generate reports.

## Table of Contents

### Classes

- [`TestResultCollector`](#testresultcollector)
- [`TestDiscoverer`](#testdiscoverer)

## Classes

## `TestResultCollector`

```python
class TestResultCollector(object)
```

Collects and formats test results for reporting.

**Methods:**

- [`_extract_message`](#_extract_message)
- [`collect_results`](#collect_results)
- [`generate_json_report`](#generate_json_report)
- [`generate_markdown_report`](#generate_markdown_report)

### `_extract_message`

```python
def _extract_message(self, traceback)
```

Extract the error message from a traceback.

### `collect_results`

```python
def collect_results(self, result)
```

Collect results from a TestResult object.

**Parameters:**

- `result` (`unittest.TestResult`): TestResult object from the test run

### `generate_json_report`

```python
def generate_json_report(self, output_path)
```

Generate a JSON report of the test results.

**Parameters:**

- `output_path` (`Path`): Path to write the report to

### `generate_markdown_report`

```python
def generate_markdown_report(self, output_path)
```

Generate a Markdown report of the test results.

**Parameters:**

- `output_path` (`Path`): Path to write the report to

## `TestDiscoverer`

```python
class TestDiscoverer(object)
```

Discovers and runs tests, then generates reports.

**Constructor Parameters:**

- `test_dir` (`Path`): Directory to look for tests in
- `verbosity` (`int`): Verbosity level for test output

**Methods:**

- [`run_tests`](#run_tests)

### `run_tests`

```python
def run_tests(self)
```

Discover and run tests, then return the results.

**Returns:**

- `Tuple[(bool, Dict[(str, Any)])]`: Tuple containing success status and test results
