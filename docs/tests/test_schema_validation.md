# test_schema_validation.py: last updated 09:35 AM on April 17, 2025

**File Path:** `WIP/test_generator/tests/test_schema_validation.py`

## Module Description

Comprehensive tests for schema validation methods.

## Table of Contents

### Classes

- [`TestValidationProcedures`](#testvalidationprocedures)
- [`TestExpectedValue`](#testexpectedvalue)
- [`TestVariableValidation`](#testvariablevalidation)
- [`TestMaterial`](#testmaterial)
- [`TestMethod`](#testmethod)
- [`TestImports`](#testimports)
- [`TestTestTitle`](#testtesttitle)

## Classes

## `TestValidationProcedures`

```python
class TestValidationProcedures(unittest.TestCase)
```

Test the ValidationProcedure schema class.

**Methods:**

- [`test_validation_procedure_creation`](#test_validation_procedure_creation)
- [`test_validation_procedure_optional_fields`](#test_validation_procedure_optional_fields)

### `test_validation_procedure_creation`

```python
def test_validation_procedure_creation(self)
```

Test creating a validation procedure.

### `test_validation_procedure_optional_fields`

```python
def test_validation_procedure_optional_fields(self)
```

Test creating a validation procedure with optional fields omitted.

## `TestExpectedValue`

```python
class TestExpectedValue(unittest.TestCase)
```

Test the ExpectedValue schema class.

**Methods:**

- [`test_expected_value_creation`](#test_expected_value_creation)
- [`test_expected_value_multiple_procedures`](#test_expected_value_multiple_procedures)

### `test_expected_value_creation`

```python
def test_expected_value_creation(self)
```

Test creating an expected value.

### `test_expected_value_multiple_procedures`

```python
def test_expected_value_multiple_procedures(self)
```

Test creating an expected value with multiple validation procedures.

## `TestVariableValidation`

```python
class TestVariableValidation(unittest.TestCase)
```

Test the Variable schema class with comprehensive validation testing.

**Methods:**

- [`test_name_in_python_property`](#test_name_in_python_property)
- [`test_type_in_python_property`](#test_type_in_python_property)
- [`test_variable_creation_continuous`](#test_variable_creation_continuous)
- [`test_variable_creation_discrete`](#test_variable_creation_discrete)
- [`test_variable_creation_nominal`](#test_variable_creation_nominal)
- [`test_variable_creation_ordinal`](#test_variable_creation_ordinal)
- [`test_variable_with_expected_value`](#test_variable_with_expected_value)

### `test_name_in_python_property`

```python
def test_name_in_python_property(self)
```

Test the name_in_python property of Variable.

### `test_type_in_python_property`

```python
def test_type_in_python_property(self)
```

Test the type_in_python property of Variable.

### `test_variable_creation_continuous`

```python
def test_variable_creation_continuous(self)
```

Test creating a continuous variable.

### `test_variable_creation_discrete`

```python
def test_variable_creation_discrete(self)
```

Test creating a discrete variable.

### `test_variable_creation_nominal`

```python
def test_variable_creation_nominal(self)
```

Test creating a nominal variable.

### `test_variable_creation_ordinal`

```python
def test_variable_creation_ordinal(self)
```

Test creating an ordinal variable.

### `test_variable_with_expected_value`

```python
def test_variable_with_expected_value(self)
```

Test creating a variable with an expected value.

## `TestMaterial`

```python
class TestMaterial(unittest.TestCase)
```

Test the Material schema class.

**Methods:**

- [`test_material_creation`](#test_material_creation)
- [`test_material_optional_fields`](#test_material_optional_fields)

### `test_material_creation`

```python
def test_material_creation(self)
```

Test creating a material.

### `test_material_optional_fields`

```python
def test_material_optional_fields(self)
```

Test creating a material with optional fields omitted.

## `TestMethod`

```python
class TestMethod(unittest.TestCase)
```

Test the Method schema class.

**Methods:**

- [`test_method_creation`](#test_method_creation)

### `test_method_creation`

```python
def test_method_creation(self)
```

Test creating a method.

## `TestImports`

```python
class TestImports(unittest.TestCase)
```

Test the Imports schema class.

**Methods:**

- [`test_import_creation`](#test_import_creation)
- [`test_import_with_functions`](#test_import_with_functions)

### `test_import_creation`

```python
def test_import_creation(self)
```

Test creating an import.

### `test_import_with_functions`

```python
def test_import_with_functions(self)
```

Test creating an import with functions.

## `TestTestTitle`

```python
class TestTestTitle(unittest.TestCase)
```

Test the TestTitle schema class.

**Methods:**

- [`test_test_title`](#test_test_title)
- [`test_test_title_default`](#test_test_title_default)
- [`test_test_title_model_validator`](#test_test_title_model_validator)

### `test_test_title`

```python
def test_test_title(self)
```

Test creating a test title.

### `test_test_title_default`

```python
def test_test_title_default(self)
```

Test creating a test title with the default value.

### `test_test_title_model_validator`

```python
def test_test_title_model_validator(self)
```

Test that the model validator converts to PascalCase.
