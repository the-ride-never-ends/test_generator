# test_variable.py: last updated 02:01 PM on April 15, 2025

**File Path:** `WIP/test_generator/tests/test_variable.py`

## Table of Contents

### Classes

- [`TestGetPythonType`](#testgetpythontype)
- [`TestVariableProperties`](#testvariableproperties)

## Classes

## `TestGetPythonType`

```python
class TestGetPythonType(unittest.TestCase)
```

Test the _get_python_type_from_statistical_type function.

**Methods:**

- [`test_continuous_type`](#test_continuous_type)
- [`test_discrete_type`](#test_discrete_type)
- [`test_invalid_type`](#test_invalid_type)
- [`test_nominal_type`](#test_nominal_type)
- [`test_ordinal_type`](#test_ordinal_type)

### `test_continuous_type`

```python
def test_continuous_type(self)
```

Test that CONTINUOUS returns float type.

### `test_discrete_type`

```python
def test_discrete_type(self)
```

Test that DISCRETE returns int type.

### `test_invalid_type`

```python
def test_invalid_type(self)
```

Test that a non-StatisticalType value raises ValueError.

### `test_nominal_type`

```python
def test_nominal_type(self)
```

Test that NOMINAL returns str type.

### `test_ordinal_type`

```python
def test_ordinal_type(self)
```

Test that ORDINAL returns str type.

## `TestVariableProperties`

```python
class TestVariableProperties(unittest.TestCase)
```

Test the properties of the Variable class.

**Methods:**

- [`setUp`](#setup)
- [`test_name_in_python`](#test_name_in_python)
- [`test_reject_null_with_expected`](#test_reject_null_with_expected)
- [`test_reject_null_without_expected`](#test_reject_null_without_expected)
- [`test_type_in_python`](#test_type_in_python)

### `setUp`

```python
def setUp(self)
```

Set up test variables.

### `test_name_in_python`

```python
def test_name_in_python(self)
```

Test the name_in_python property.

### `test_reject_null_with_expected`

```python
def test_reject_null_with_expected(self)
```

Test reject_null property when expected_value is set.

### `test_reject_null_without_expected`

```python
def test_reject_null_without_expected(self)
```

Test reject_null property when expected_value is not set.

### `test_type_in_python`

```python
def test_type_in_python(self)
```

Test the type_in_python property.
