# generator.py: last updated 11:35 PM on April 17, 2025

**File Path:** `WIP/test_generator/generator.py`

## Module Description

Core test generation logic for Test Generator.

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

- [`_parse_background`](#_parse_background)
- [`_parse_control_variables`](#_parse_control_variables)
- [`_parse_imports`](#_parse_imports)
- [`_parse_materials`](#_parse_materials)
- [`_parse_test_method`](#_parse_test_method)
- [`_parse_test_title`](#_parse_test_title)
- [`_parse_variable`](#_parse_variable)

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

- [`_get_template`](#_get_template)
- [`_initialize_template_engine`](#_initialize_template_engine)
- [`_load_json_file`](#_load_json_file)
- [`_parse_test_parameters`](#_parse_test_parameters)
- [`_render_template`](#_render_template)
- [`generate_test_file`](#generate_test_file)
- [`write_test_file`](#write_test_file)

### `_get_template`

```python
def _get_template(self)
```

Get the appropriate template for the test framework.

**Returns:**

- `Union[(Template, str)]`: Template object or string template if engine not available

### `_initialize_template_engine`

```python
def _initialize_template_engine(self)
```

Initialize the Jinja2 template engine.

**Returns:**

- `Optional[Environment]`: Configured Jinja2 environment or None if no templates found

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

- `template` (`Union[(Template, str)]`): Template object or string template

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
