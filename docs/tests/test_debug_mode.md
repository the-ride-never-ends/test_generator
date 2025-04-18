# test_debug_mode.py: last updated 06:01 PM on April 17, 2025

**File Path:** `/home/kylerose1946/claudes_toolbox/WIP/test_generator/tests/test_debug_mode.py`

## Module Description

Tests for debug mode with enhanced output.

## Table of Contents

### Classes

- [`TestDebugMode`](#testdebugmode)

## Classes

## `TestDebugMode`

```python
class TestDebugMode(unittest.TestCase)
```

Tests for debug mode with enhanced output.

**Methods:**

- [`setUp`](#setup)
- [`tearDown`](#teardown)
- [`test_debug_cli_argument`](#test_debug_cli_argument)
- [`test_debug_flag_in_config`](#test_debug_flag_in_config)
- [`test_debug_flag_propagation`](#test_debug_flag_propagation)
- [`test_debug_json_dump`](#test_debug_json_dump)
- [`test_debug_logging_level`](#test_debug_logging_level)
- [`test_debug_mode_exception_handling`](#test_debug_mode_exception_handling)
- [`test_debug_output_in_generation`](#test_debug_output_in_generation)
- [`test_normal_logging_level`](#test_normal_logging_level)
- [`test_normal_mode_exception_handling`](#test_normal_mode_exception_handling)

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

### `test_debug_cli_argument`

```python
def test_debug_cli_argument(self, mock_add_argument)
```

Test debug CLI argument is properly added.

### `test_debug_flag_in_config`

```python
def test_debug_flag_in_config(self, mock_validate)
```

Test debug flag is properly added to the configuration.

### `test_debug_flag_propagation`

```python
def test_debug_flag_propagation(self, mock_parse_args)
```

Test debug flag is properly propagated through the system.

### `test_debug_json_dump`

```python
def test_debug_json_dump(self)
```

Test debug dump of JSON data.

### `test_debug_logging_level`

```python
def test_debug_logging_level(self, mock_get_logger)
```

Test setting logging level based on debug flag.

### `test_debug_mode_exception_handling`

```python
def test_debug_mode_exception_handling(self, mock_print_exc)
```

Test exception handling in debug mode.

### `test_debug_output_in_generation`

```python
def test_debug_output_in_generation(self, mock_render, mock_get_template)
```

Test debug output during test generation.

### `test_normal_logging_level`

```python
def test_normal_logging_level(self, mock_get_logger)
```

Test setting logging level without debug flag.

### `test_normal_mode_exception_handling`

```python
def test_normal_mode_exception_handling(self, mock_print_exc)
```

Test exception handling without debug mode.
