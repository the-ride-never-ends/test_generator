# cli.py: last updated 02:01 PM on April 15, 2025

**File Path:** `WIP/test_generator/cli.py`

## Module Description

Command-line interface for the Test Generator Mk2.

## Table of Contents

### Functions

- [`main`](#main)

### Classes

- [`CLI`](#cli)

## Functions

## `main`

```python
def main()
```

Main entry point for the CLI.

**Returns:**

- `int`: Exit code

## Classes

## `CLI`

```python
class CLI(object)
```

Command-line interface for the Test Generator Mk2.

Handles command-line arguments, configuration loading, and pipeline orchestration.

**Methods:**

- [`_create_parser`](#_create_parser)
- [`parse_args`](#parse_args)
- [`run`](#run)
- [`validate_config`](#validate_config)

### `_create_parser`

```python
def _create_parser(self)
```

Create the argument parser for the CLI.

**Returns:**

- `argparse.ArgumentParser`: Configured argument parser

### `parse_args`

```python
def parse_args(self, args=None)
```

Parse command-line arguments.

**Parameters:**

- `args` (`Optional[list[str]]`): Command-line arguments (uses sys.argv if None)

**Returns:**

- `Dict[(str, Any)]`: Dictionary of parsed arguments

### `run`

```python
def run(self)
```

Run the test generator pipeline.

**Returns:**

- `int`: Exit code (0 for success, non-zero for errors)

### `validate_config`

```python
def validate_config(self, args_dict)
```

Validate configuration using Pydantic models.

**Parameters:**

- `args_dict` (`Dict[(str, Any)]`): Dictionary of arguments to validate

**Returns:**

- `bool`: True if validation passed, False otherwise
