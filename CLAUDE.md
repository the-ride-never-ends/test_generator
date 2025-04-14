# Test Generator Mk2 - Claude Developer Guide

This file provides guidance to Claude Code when working with the Test Generator Mk2 project.

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
   - For dependent variables: expected_value with validation_methods

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

## Common Workflows

### Generate a Test File

```python
from test_generator_mk2.cli import CLI

cli = CLI()
args_dict = cli.parse_args()
cli.validate_config(args_dict)
cli.run()
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
- All functions should have type hints
- Use snake_case for functions and variables
- Use PascalCase for classes

## Testing

### Running Tests

```bash
# Run tests with reporting
./run_tests.sh

# Run tests with reduced verbosity
./run_tests.sh -q
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