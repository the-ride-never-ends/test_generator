# test_fix_whitespace.py: last updated 11:35 PM on April 17, 2025

**File Path:** `WIP/test_generator/tests/test_fix_whitespace.py`

## Module Description

Tests for the fix_whitespace script.

## Table of Contents

### Classes

- [`TestFixWhitespace`](#testfixwhitespace)

## Classes

## `TestFixWhitespace`

```python
class TestFixWhitespace(unittest.TestCase)
```

Test case for the fix_whitespace script.

**Methods:**

- [`setUp`](#setup)
- [`tearDown`](#teardown)
- [`test_clean_whitespace_in_blank_lines`](#test_clean_whitespace_in_blank_lines)
- [`test_ensure_newline_at_end_of_file`](#test_ensure_newline_at_end_of_file)
- [`test_find_files`](#test_find_files)
- [`test_fix_files`](#test_fix_files)
- [`test_fix_trailing_whitespace`](#test_fix_trailing_whitespace)

### `setUp`

```python
def setUp(self)
```

Set up the test environment.

### `tearDown`

```python
def tearDown(self)
```

Clean up the test environment.

### `test_clean_whitespace_in_blank_lines`

```python
def test_clean_whitespace_in_blank_lines(self)
```

Test cleaning whitespace in blank lines.

### `test_ensure_newline_at_end_of_file`

```python
def test_ensure_newline_at_end_of_file(self)
```

Test ensuring file ends with a newline.

### `test_find_files`

```python
def test_find_files(self)
```

Test finding files matching patterns.

### `test_fix_files`

```python
def test_fix_files(self)
```

Test fixing multiple files at once.

### `test_fix_trailing_whitespace`

```python
def test_fix_trailing_whitespace(self)
```

Test fixing trailing whitespace.
