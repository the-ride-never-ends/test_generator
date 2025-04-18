# fix_whitespace.py: last updated 11:35 PM on April 17, 2025

**File Path:** `WIP/test_generator/utils/for_tests/fix_whitespace.py`

## Module Description

Script to automatically fix common whitespace issues in Python files.

## Table of Contents

### Functions

- [`clean_whitespace_in_blank_lines`](#clean_whitespace_in_blank_lines)
- [`fix_trailing_whitespace`](#fix_trailing_whitespace)
- [`ensure_newline_at_end_of_file`](#ensure_newline_at_end_of_file)
- [`find_files`](#find_files)
- [`fix_files`](#fix_files)
- [`main`](#main)

## Functions

## `clean_whitespace_in_blank_lines`

```python
def clean_whitespace_in_blank_lines(file_path)
```

Clean whitespace in blank lines in a file.

**Parameters:**

- `file_path` (`str`): Path to the file to clean

**Returns:**

- `int`: Number of lines fixed

## `fix_trailing_whitespace`

```python
def fix_trailing_whitespace(file_path)
```

Fix trailing whitespace in a file.

**Parameters:**

- `file_path` (`str`): Path to the file to fix

**Returns:**

- `int`: Number of lines fixed

## `ensure_newline_at_end_of_file`

```python
def ensure_newline_at_end_of_file(file_path)
```

Ensure file ends with a newline.

**Parameters:**

- `file_path` (`str`): Path to the file to fix

**Returns:**

- `int`: 1 if fixed, 0 if already correct

## `find_files`

```python
def find_files(patterns, exclude_dirs=None)
```

Find files matching the given patterns.

**Parameters:**

- `patterns` (`List[str]`): List of file patterns (e.g. ["*.py"])

- `exclude_dirs` (`Optional[List[str]]`): List of directory patterns to exclude

**Returns:**

- `List[str]`: List of file paths

## `fix_files`

```python
def fix_files(file_paths, fix_blank=True, fix_trailing=True, fix_newlines=True, verbose=False)
```

Fix issues in the given files.

**Parameters:**

- `file_paths` (`List[str]`): List of file paths to fix

- `fix_blank` (`bool`): Whether to fix blank lines with whitespace

- `fix_trailing` (`bool`): Whether to fix trailing whitespace

- `fix_newlines` (`bool`): Whether to ensure files end with a newline

- `verbose` (`bool`): Whether to print details about each file

**Returns:**

- `Tuple[(int, int, int, int)]`: Tuple of (number of files fixed, blank line fixes, trailing whitespace fixes, newline fixes)

## `main`

```python
def main()
```

Main entry point for the script.
