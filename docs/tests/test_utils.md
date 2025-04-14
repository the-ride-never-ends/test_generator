# test_utils.py: last updated 03:30 PM on April 14, 2025

**File Path:** `WIP/test_generator/tests/test_utils.py`

## Module Description

Tests for utility functions.

## Table of Contents

### Classes

- [`TestConvertToSnakeCase`](#testconverttosnakecase)
- [`TestConvertToPascalCase`](#testconverttopascalcase)
- [`TestLoadJsonFile`](#testloadjsonfile)

## Classes

## `TestConvertToSnakeCase`

```python
class TestConvertToSnakeCase(unittest.TestCase)
```

Test case for convert_to_snake_case function.

**Methods:**

- [`test_convert_already_snake_case`](#test_convert_already_snake_case)
- [`test_convert_multiple_spaces`](#test_convert_multiple_spaces)
- [`test_convert_single_word`](#test_convert_single_word)
- [`test_convert_space_separated`](#test_convert_space_separated)

### `test_convert_already_snake_case`

```python
def test_convert_already_snake_case(self)
```

Test converting already snake_case string.

### `test_convert_multiple_spaces`

```python
def test_convert_multiple_spaces(self)
```

Test converting string with multiple spaces.

### `test_convert_single_word`

```python
def test_convert_single_word(self)
```

Test converting single word.

### `test_convert_space_separated`

```python
def test_convert_space_separated(self)
```

Test converting space-separated words.

## `TestConvertToPascalCase`

```python
class TestConvertToPascalCase(unittest.TestCase)
```

Test case for convert_to_pascal_case function.

**Methods:**

- [`test_convert_already_pascal_case`](#test_convert_already_pascal_case)
- [`test_convert_kebab_case`](#test_convert_kebab_case)
- [`test_convert_mixed_case`](#test_convert_mixed_case)
- [`test_convert_single_word`](#test_convert_single_word)
- [`test_convert_snake_case`](#test_convert_snake_case)
- [`test_convert_space_separated`](#test_convert_space_separated)

### `test_convert_already_pascal_case`

```python
def test_convert_already_pascal_case(self)
```

Test converting already PascalCase string.

### `test_convert_kebab_case`

```python
def test_convert_kebab_case(self)
```

Test converting kebab-case string.

### `test_convert_mixed_case`

```python
def test_convert_mixed_case(self)
```

Test converting mixed case string.

### `test_convert_single_word`

```python
def test_convert_single_word(self)
```

Test converting single word.

### `test_convert_snake_case`

```python
def test_convert_snake_case(self)
```

Test converting snake_case string.

### `test_convert_space_separated`

```python
def test_convert_space_separated(self)
```

Test converting space-separated words.

## `TestLoadJsonFile`

```python
class TestLoadJsonFile(unittest.TestCase)
```

Test case for load_json_file function.

**Methods:**

- [`setUp`](#setup)
- [`tearDown`](#teardown)
- [`test_load_invalid_json`](#test_load_invalid_json)
- [`test_load_nonexistent_file`](#test_load_nonexistent_file)
- [`test_load_valid_json`](#test_load_valid_json)

### `setUp`

```python
def setUp(self)
```

Set up test environment.

### `tearDown`

```python
def tearDown(self)
```

Clean up temporary files.

### `test_load_invalid_json`

```python
def test_load_invalid_json(self)
```

Test loading invalid JSON file.

### `test_load_nonexistent_file`

```python
def test_load_nonexistent_file(self)
```

Test loading non-existent file.

### `test_load_valid_json`

```python
def test_load_valid_json(self)
```

Test loading valid JSON file.
