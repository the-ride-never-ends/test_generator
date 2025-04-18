# Test Generator - Claude Developer Guide

This file provides guidance to Claude Code when working with the Test Generator project.

## Development Status - IMPORTANT

As of April 17, 2025, I have implemented the following features from Phase 2 and Phase 4 of the TODO list:

1. Added support for parametrized tests:
   - Enhanced Variable schema with 'values' array for parameter sets
   - Added ParameterValue and ParameterExpectedValue classes
   - Added automatic detection of parametrized test data in templates
   - Updated test templates to support both pytest parametrize and unittest subTest

2. Added debug mode with enhanced output:
   - Added debug flag to CLI arguments
   - Added debug mode to Configs model
   - Added detailed logging throughout the generator
   - Added JSON data structure debug output

3. Added conditional test generation:
   - Added condition expressions to validation procedures
   - Added test_params support for conditional inclusion
   - Updated CLI to handle conditional test parameters as JSON

4. Added code quality tooling:
   - Implemented mypy type checking with configuration file
   - Added flake8 linting with appropriate configuration
   - Enhanced run_tests.sh to support type checking and linting options
   - Updated README.md with documentation for running linting and type checking

All test failures have been fixed! We now have a 100% test pass rate (101/101 tests passing). The issues in test_debug_mode.py and test_discovery_features.py have been resolved. 

Next steps would be:
1. Implement pre-commit hooks for automatic linting and type checking
2. Package for distribution with proper versioning
3. Create visual reports of test results and coverage

## Core Components

- **CLI Module**: Handles command-line arguments and orchestration
- **Generator Module**: Core test generation logic
- **Schemas**: Pydantic models for data validation
- **Templates**: Jinja2 templates for test files

## Validation Requirements

The system enforces strict validation to ensure high-quality test generation:

1. **Variables (independent, dependent, control)** must include:
   - name (string)
   - description (string)
   - statistical_type (must be one of: nominal, ordinal, continuous, discrete - case insensitive)
   - unit (string)
   - For dependent variables: expected_value with validation_procedures
   - For parametrized tests: values array with parameter sets

2. **Path Handling**:
   - Paths are properly compared regardless of object type (Path vs string)
   - Default paths are normalized (e.g., "tests" instead of "./tests")
   - Output directories are created automatically if they don't exist

3. **Test Case Isolation**:
   - Unit tests use proper mocking to isolate components
   - Integration tests include all required fields

4. **Generated Test Features**:
   - Automatic sanitization of variable names to valid Python identifiers
   - Special handling for exception-based tests
   - Timestamped documentation in generated files
   - JSON result generation with automatic test execution
   - Proper docstring format with full test documentation
   - Support for parametrized tests with multiple input/output values
   - Conditional test generation based on parameters
   - Debug output and enhanced logging

## Common Workflows

### Generate a Test File - API

```python
from test_generator_mk2.cli import CLI

cli = CLI()
args_dict = cli.parse_args()
cli.validate_config(args_dict)
cli.run()
```

### Command Line Usage

```bash
# Basic test generation
python -m test_generator_mk2 --name "Example Test" --description "Test Description" --test_parameter_json params.json

# Generate with fixtures
python -m test_generator_mk2 --name "Fixture Test" --test_parameter_json params.json --has-fixtures

# Generate parametrized test
python -m test_generator_mk2 --name "Parametrized Test" --test_parameter_json params.json --parametrized

# Generate with debug output
python -m test_generator_mk2 --name "Debug Test" --test_parameter_json params.json --debug

# Generate conditional test
python -m test_generator_mk2 --name "Conditional Test" --test_parameter_json params.json --test-params '{"input_type": "string"}'
```

### Add a New Schema

1. Create a new schema file in the `schemas/` directory
2. Add Pydantic model with proper validation
3. Import and use the schema in the generator module

### Add a New Template

1. Create a new template file in the `templates/` directory
2. Update the `_get_template()` method in `generator.py`
3. Add fallback inline template in the generator module

## Code Guidelines

- Follow Google style docstrings for all public APIs
- All functions must have type hints
- Use snake_case for functions and variables
- Use PascalCase for classes
- Use ALL_CAPS for constants and global variables

## CRITICAL CODE WRITING AND MODIFICATION RULES

1. NEVER replace or bypass code with placeholder comments (e.g. "in a real implementation", "For now, we'll just...", "For simplicity...", "Fallback in case...), "simplified" or partial implementations, or any other placeholder, until you explicitly ask and are given permission to do so.
2. If you are given permission for the placeholder, add TODO comments that MUST include:
- What exactly is missing or bypassed
- Why it's temporarily omitted
- How it should be implemented when completed
The TODO must appear in:
- Inline code comments above the placeholder
- The function/class docstring
- A dedicated TODO.md file in the repository root
3. ALWAYS assume code needs to be fully implemented unless explicitly stated otherwise e.g. If a comment says "verify that x equals 2", the code at runtime better actually verify that x equals 2.
4. Remember, your job is to implement and fix the code so that it runs successfully, not fake it or pretend it works for the purpose of it passing tests or for your convenience.
5. NEVER make special exceptions in code to handle test cases. Tests should verify the actual behavior of the code, not the other way around. If tests are failing, either fix the code to work correctly or update the tests to match the intended behavior. DO NOT add conditionals, special cases, or workarounds in the core code that only exist to make tests pass.

## Testing

### Running Tests

```bash
# Run tests with reporting
./run_tests.sh

# Run tests with reduced verbosity
./run_tests.sh -q

# Run tests with type checking and linting
./run_tests.sh --check-all      # Run tests + mypy + flake8
./run_tests.sh --mypy           # Run tests + mypy type checking
./run_tests.sh --flake8         # Run tests + flake8 linting
./run_tests.sh --lint-only      # Only run mypy + flake8 (no tests)
```

### Test Report System

The project includes a comprehensive test reporting system:

```python
# Programmatic use of the test reporting
from run_tests import TestDiscoverer
from pathlib import Path

# Run tests and generate reports
test_dir = Path("tests")
discoverer = TestDiscoverer(test_dir)
success, results = discoverer.run_tests()
```

### Report Formats

- JSON reports include full test details and structured data
- Markdown reports are human-readable summaries with failure details
- Historical reports are stored with timestamps in test_reports/
- latest_report.json and latest_report.md always point to most recent run

Always add tests for new features and maintain >90% test coverage.

## Dependency Management

- Add new dependencies to `requirements.txt`
- Prefer standard library when possible
- Always pin version numbers

## Available Tools

### Documentation Generator

#### Overview

Documentation Generator automatically extracts code structure, docstrings, and type annotations from Python source code to produce comprehensive documentation in Markdown format. It supports multiple docstring styles (Google, NumPy, and reStructuredText) and preserves type hints from source code annotations. The tool can now generate comprehensive class inheritance documentation with method override detection and inheritance diagrams.

#### Current Filepath to README.md
'/home/kylerose1946/claudes_toolbox/documentation_generator/README.md'