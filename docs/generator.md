# generator.py: last updated 07:08 PM on April 13, 2025

**File Path:** `/home/kylerose1946/claudes_toolbox/WIP/test_generator_mk2/generator.py`

## Module Description

Core test generation logic for Test Generator Mk2.

## Table of Contents

### Classes

- [`TestFileParameters`](#testfileparameters)
- [`TestGenerator`](#testgenerator)

## Classes

## `TestFileParameters`

```python
class TestFileParameters(object)
```

Container for all test file parameters.

This class handles loading, validating, and transforming the test parameters
from JSON into usable Python objects.

**Constructor Parameters:**

- `json_data` (`Dict[(str, Any)]`): Dictionary of test file parameters

**Methods:**

- [`_parse_background`](#testfileparameters__parse_background)
- [`_parse_control_variables`](#testfileparameters__parse_control_variables)
- [`_parse_imports`](#testfileparameters__parse_imports)
- [`_parse_materials`](#testfileparameters__parse_materials)
- [`_parse_test_method`](#testfileparameters__parse_test_method)
- [`_parse_test_title`](#testfileparameters__parse_test_title)
- [`_parse_variable`](#testfileparameters__parse_variable)

### `_parse_background`

```python
def _parse_background(self)
```

Parse and validate the background information.

### `_parse_control_variables`

```python
def _parse_control_variables(self)
```

Parse and validate control variables.

### `_parse_imports`

```python
def _parse_imports(self)
```

Parse and validate imports.

### `_parse_materials`

```python
def _parse_materials(self)
```

Parse and validate test materials.

### `_parse_test_method`

```python
def _parse_test_method(self)
```

Parse and validate the test method.

### `_parse_test_title`

```python
def _parse_test_title(self)
```

Parse and validate the test title.

### `_parse_variable`

```python
def _parse_variable(self, var_type)
```

Parse and validate a variable (independent or dependent).

**Parameters:**

- `var_type` (`str`): Type of variable (independent_variable or dependent_variable)

**Returns:**

- `Variable`: Validated variable object

## `TestGenerator`

```python
class TestGenerator(object)
```

Core test generation logic.

This class handles loading test specifications, applying templates,
and managing the generation process.

**Constructor Parameters:**

- `config` (`Configs`): Configuration object

**Methods:**

- [`_get_template`](#testgenerator__get_template)
- [`_initialize_template_engine`](#testgenerator__initialize_template_engine)
- [`_load_json_file`](#testgenerator__load_json_file)
- [`_parse_test_parameters`](#testgenerator__parse_test_parameters)
- [`_render_template`](#testgenerator__render_template)
- [`generate_test_file`](#testgenerator_generate_test_file)
- [`write_test_file`](#testgenerator_write_test_file)

### `_get_template`

```python
def _get_template(self)
```

Get the appropriate template for the test framework.

**Returns:**

- `Union[(str, None)]`: Template string or None if template engine is not available

### `_initialize_template_engine`

```python
def _initialize_template_engine(self)
```

Initialize the Jinja2 template engine.

**Returns:**

- `Environment`: Configured Jinja2 environment

### `_load_json_file`

```python
def _load_json_file(self)
```

Load and parse the JSON file with test parameters.

**Returns:**

- `Dict[(str, Any)]`: Parsed JSON data

### `_parse_test_parameters`

```python
def _parse_test_parameters(self, json_data)
```

Parse and validate test parameters from JSON data.

**Parameters:**

- `json_data` (`Dict[(str, Any)]`): Dictionary with JSON data

**Returns:**

- `TestFileParameters`: Validated parameters

### `_render_template`

```python
def _render_template(self, template)
```

Render the template with test parameters.

**Parameters:**

- `template` (`str`): Template string or Jinja2 template

**Returns:**

- `str`: Rendered test file

### `generate_test_file`

```python
def generate_test_file(self)
```

Generate a test file based on JSON input.

**Returns:**

- `str`: Generated test file content

### `write_test_file`

```python
def write_test_file(self, content)
```

Write the generated test file to disk.

**Parameters:**

- `content` (`str`): Test file content

**Returns:**

- `Path`: Path to the output file
