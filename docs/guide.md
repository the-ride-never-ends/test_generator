# Test Generator Mk2 Documentation Guide

This guide provides an overview of the Test Generator Mk2 documentation.

## Documentation Structure

The documentation is organized according to the project's structure:

- Core modules are in the root directory
- Schema models are in the `schemas/` directory
- Test files are in the `tests/` directory
- Utility functions are in the `utils/common/` directory

## Key Components

### Core Modules

- **[CLI](cli.md)**: Command-line interface for the Test Generator
- **[Generator](generator.md)**: Core test generation logic
- **[Configs](configs.md)**: Configuration validation
- **[Main](main.md)**: Main entry point
- **[Run Tests](run_tests.md)**: Test runner with report generation
- **[View Report](view_report.md)**: Test report viewer

### Schema Models

- **[Variable](schemas/variable.md)**: Defines test variables (independent, dependent, control)
- **[Method](schemas/method.md)**: Defines test method steps and procedures
- **[Material](schemas/material.md)**: Defines test fixtures and dependencies
- **[Expected Value](schemas/expected_value.md)**: Defines validation methods for expected values
- **[Imports](schemas/imports.md)**: Defines import statements
- **[Test Title](schemas/test_title.md)**: Defines test title
- **[Statistical Type](schemas/statistical_type.md)**: Defines statistical types for variables

### Utility Functions

- **[Convert to Snake Case](utils/common/convert_to_snake_case.md)**: Converts strings to snake_case
- **[Convert to Pascal Case](utils/common/convert_to_pascal_case.md)**: Converts strings to PascalCase
- **[Load JSON File](utils/common/load_json_file.md)**: Loads JSON data from a file

### Tests

- **[Test Configuration](tests/test_configs.md)**: Tests for configuration validation
- **[Test CLI](tests/test_cli.md)**: Tests for the command-line interface
- **[Test Generator](tests/test_generator.md)**: Tests for the generator module
- **[Test Utils](tests/test_utils.md)**: Tests for utility functions
- **[Test Integration](tests/test_integration.md)**: End-to-end integration tests

## Main Concepts

### Scientific Approach to Testing

Test Generator Mk2 uses a scientific approach to testing with:

- **Hypothesis**: Clear statement of what is being tested
- **Independent Variables**: Factors being manipulated in the test
- **Dependent Variables**: Measurements taken in response to the independent variable
- **Control Variables**: Factors kept constant during the test
- **Expected Values**: Predictions about the results
- **Validation Methods**: Techniques for verifying results

### Pipeline Architecture

The tool follows a pipeline architecture:

1. **Input**: Parse command-line arguments and JSON test parameters
2. **Validation**: Validate inputs using Pydantic models
3. **Generation**: Process parameters and generate test code
4. **Templates**: Apply templates for different test frameworks
5. **Output**: Write test files to disk

### Test Reporting

The tool provides a comprehensive test reporting system:

- JSON and Markdown report formats
- Historical test records with timestamps
- Detailed test results with failure information
- Customizable detail levels

## Navigation

For a complete list of all files and their documentation, see the [auto-generated index](index.md).

---

*Note: This guide is maintained separately from the auto-generated documentation and won't be overwritten when documentation is regenerated.*