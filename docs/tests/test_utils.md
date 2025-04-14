# test_utils.py: last updated 07:08 PM on April 13, 2025

**File Path:** `/home/kylerose1946/claudes_toolbox/WIP/test_generator_mk2/tests/test_utils.py`

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

- [`test_convert_already_snake_case`](#testconverttosnakecase_test_convert_already_snake_case)
- [`test_convert_multiple_spaces`](#testconverttosnakecase_test_convert_multiple_spaces)
- [`test_convert_single_word`](#testconverttosnakecase_test_convert_single_word)
- [`test_convert_space_separated`](#testconverttosnakecase_test_convert_space_separated)

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

- [`test_convert_already_pascal_case`](#testconverttopascalcase_test_convert_already_pascal_case)
- [`test_convert_kebab_case`](#testconverttopascalcase_test_convert_kebab_case)
- [`test_convert_mixed_case`](#testconverttopascalcase_test_convert_mixed_case)
- [`test_convert_single_word`](#testconverttopascalcase_test_convert_single_word)
- [`test_convert_snake_case`](#testconverttopascalcase_test_convert_snake_case)
- [`test_convert_space_separated`](#testconverttopascalcase_test_convert_space_separated)

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

- [`setUp`](#testloadjsonfile_setup)
- [`tearDown`](#testloadjsonfile_teardown)
- [`test_load_invalid_json`](#testloadjsonfile_test_load_invalid_json)
- [`test_load_nonexistent_file`](#testloadjsonfile_test_load_nonexistent_file)
- [`test_load_valid_json`](#testloadjsonfile_test_load_valid_json)

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
