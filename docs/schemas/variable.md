# variable.py: last updated 07:08 PM on April 13, 2025

**File Path:** `/home/kylerose1946/claudes_toolbox/WIP/test_generator_mk2/schemas/variable.py`

## Table of Contents

### Functions

- [`_get_python_type_from_statistical_type`](#_get_python_type_from_statistical_type)

### Classes

- [`Variable`](#variable)

## Functions

## `_get_python_type_from_statistical_type`

```python
def _get_python_type_from_statistical_type(statistical_type)
```

Returns the python type of the variable based on the statistical type.

## Classes

## `Variable`

```python
class Variable(BaseModel)
```

A variable is any characteristic, number, or quantity that can be measured or counted.
Age, sex, business income and expenses, country of birth, capital expenditure, class grades, eye color 
and vehicle type are examples of variables. It is called a variable because the value may vary between data units in a population, 
and may change in value over time.

For example, 'income' is a variable that can vary between data units in a population 
(i.e. the people or businesses being studied may not have the same incomes) and can also 
vary over time for each data unit (i.e. income can go up or down).

**Methods:**

- [`name_in_python`](#variable_name_in_python) (property)
- [`reject_null`](#variable_reject_null) (property)
- [`type_in_python`](#variable_type_in_python) (property)

### `name_in_python`

```python
def name_in_python(self)
```

Returns the name of the variable in python.
This is used to determine how to handle the variable in code.

### `reject_null`

```python
def reject_null(self)
```

### `type_in_python`

```python
def type_in_python(self)
```

Returns the python type of the variable. 
This is used to determine how to handle the variable in code.
