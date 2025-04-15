# Test Generator - Claude Developer Guide

This file provides guidance to Claude Code when working with the Test Generator project.

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
- All functions must have type hints
- Use snake_case for functions and variables
- Use PascalCase for classes
- Use ALL_CAPS for constants and global variables

## CRITICAL CODE WRITING AND MODIFICATION RULES

1. NEVER replace or bypass code with placeholder comments (e.g. "in a real implementation", "For now, we'll just...", "For simplicity..."), "simplified" or partial implementations, or any other placeholder, until you explicitly ask and are given permission to do so.
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