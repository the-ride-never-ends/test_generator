# Test Generator Mk2

A tool for generating structured Python tests from JSON specifications using a scientific approach.

## Overview

Test Generator Mk2 creates test boilerplate code with a scientific approach to testing:
- Clearly defined hypotheses
- Independent and dependent variables
- Controlled variables
- Structured validation

## Features

- Generate test files for unittest or pytest with framework-specific optimizations
- Define tests in a structured JSON format
- Support for variable definitions and relationships
- Template-based generation with Jinja2
- Validation of expected vs actual results
- Clean separation of concerns
- Proper logging and error handling
- Comprehensive test result capturing and reporting
- Plugin-based approach for pytest integration
- Automated JSON result generation

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd claudes_toolbox/WIP/test_generator_mk2

# Install dependencies
pip install -r requirements.txt
```

## Command-line Usage

```bash
python -m test_generator_mk2 \
  --name "Connection Pool Performance" \
  --description "Tests the impact of connection pool size on query performance" \
  --test_parameter_json path/to/parameters.json \
  --output_dir ./tests \
  --harness unittest
```

### Command-line Options

- `--name`: Name of the test to generate (required)
- `--description`: A short description of the test
- `--test_parameter_json`: Path to the JSON file used to define the test (required)
- `--output_dir`: Path to output directory for tests (default: ./tests)
- `--verbose`: Enable verbose output (default: true)
- `--harness`: Which python testing harness to use (default: unittest)
- `--has-fixtures`: Whether a test needs fixtures in order to run (default: false)
- `--docstring-style`: Docstring style to parse (default: google)

## Architecture

The system follows a pipeline architecture:

1. **CLI** - Handles command-line arguments and orchestration
2. **Configuration** - Validates inputs with Pydantic models
3. **Generator** - Processes JSON input and applies templates
4. **Templates** - Jinja2 templates for different test frameworks
5. **Output** - Writes generated test files to disk

See the [System Architecture Document](./SAD.md) for more details.

## Test Parameter JSON Format

The test parameter JSON file defines all aspects of the test in a scientific structure:

| Component | Description |
|-----------|-------------|
| Test title | The title of the test experiment |
| Background | Context, purpose, and hypothesis |
| Independent variable | The variable you're manipulating in the test |
| Dependent variable | The variable you're measuring in response |
| Control variables | Variables kept constant during the test |
| Test materials | Software, hardware, and configurations used |
| Test method | Steps to execute the test and analyze results |
| Imports | Libraries needed for the test |

Here's the structure from `_test_file_parameters_template.json`:

```json
{
    "test_file_parameters": {
        "background": {
            "orientation": "Division by zero is undefined and throws exceptions in most programming languages.",
            "purpose": "Test the behavior of division by zero in polynomial multiplication operations.",
            "citation_path": "path/to/citation1.md",
            "citation": "Mathematics for Computer Science",
            "hypothesis": "Division by zero will raise a ZeroDivisionError exception and prevent the completion of polynomial multiplication."
        },
        "test_title": "The Effects of Division by Zero on Polynomial Multiplication",
        "independent_variable": {
            "name": "Divisor Value",
            "description": "The value used as a divisor in the polynomial operation",
            "statistical_type": "discrete",
            "unit": "integer",
            "value": 0
        },
        "dependent_variable": {
            "name": "Calculation Result",
            "description": "Whether the calculation completes successfully or raises an exception",
            "statistical_type": "nominal",
            "unit": "result",
            "expected_value": {
                "value": "ZeroDivisionError",
                "validation_procedures": [
                    {
                        "description": "Check if the ZeroDivisionError exception is raised",
                        "name": "exception_zero_division_error",
                        "kwargs": {
                            "exception_type": "ZeroDivisionError"
                        },
                        "steps": [
                            "Create two polynomial objects",
                            "Attempt to divide the first polynomial by zero",
                            "Multiply the result with the second polynomial",
                            "Verify that a ZeroDivisionError is raised"
                        ]
                    }
                ]
            }
        },
        "control_variables": [
            {
                "name": "Polynomial Degree",
                "description": "The degree of the polynomials being multiplied",
                "statistical_type": "discrete",
                "unit": "degree",
                "value": 2
            },
            {
                "name": "Coefficient Range",
                "description": "The range of values for polynomial coefficients",
                "statistical_type": "discrete",
                "unit": "range",
                "value": 10
            }
        ],
        "test_materials": [
            {
                "description": "Mathematical library for polynomial operations",
                "name": "NumPy",
                "type": "library",
                "version": "1.24.0",
                "configuration": {
                    "random_seed": 42
                }
            }
        ],
        "test_procedure": {
            "data_collection": "Exception type and message",
            "analysis_technique": "Exception analysis and verification",
            "steps": [
                "Import required libraries (numpy)",
                "Create two random polynomials with degree 2",
                "Attempt to calculate: (polynomial1 / 0) * polynomial2",
                "Verify that ZeroDivisionError is raised",
                "Record the exception details"
            ]
        },
        "imports": [
            {
                "name": "numpy"
            },
            {
                "name": "unittest"
            }
        ]
    }
}
```

## Development

### Running Tests

```bash
# Easy way: run with reporting
./run_tests.sh

# Alternative: manual test execution
python -m unittest discover tests

# Run a specific test
python -m unittest tests.test_configs
```

### Test Validation

The test system implements strict validation for all components:

- **Variable Validation**: All variables require proper statistical_type, unit, and other required fields
- **Expected Value Validation**: Dependent variables must have validation_procedures specified
- **Proper Test Isolation**: Tests use mocking to ensure proper unit testing isolation
- **Case Insensitivity**: Statistical types are handled case-insensitively (e.g., "DISCRETE" or "discrete")
- **Path Handling**: Path objects and strings are properly compared
- **Exception Testing**: Special handling for tests that expect exceptions with detailed capturing
- **Variable Sanitization**: Converts variable names to valid Python identifiers
- **Automated Results**: Test files include JSON result generation with timestamps
- **Test Reporting**: Comprehensive test result capture including error messages and outcomes
- **Framework Support**: Both unittest and pytest frameworks with proper test fixtures and plugins

### Test Reporting

The test runner automatically generates reports in both JSON and Markdown formats:

```bash
# Run tests and generate reports
./run_tests.sh

# View the latest report with different detail levels
python view_report.py
python view_report.py --format details
python view_report.py --format full

# View a specific report
python view_report.py test_reports/test_report_20250413_120000.json
```

Reports are stored in the `test_reports/` directory:
- `latest_report.json` - Always contains the most recent report (JSON)
- `latest_report.md` - Always contains the most recent report (Markdown)
- `test_report_TIMESTAMP.json` - Historical reports (JSON)
- `test_report_TIMESTAMP.md` - Historical reports (Markdown)

In addition, generated test files automatically produce their own JSON result files when executed:

```json
{
  "test_title": "The Effects of Division by Zero on Polynomial Multiplication",
  "test_function": "test_divisionbyzerotest",
  "hypothesis": "Division by zero will raise a ZeroDivisionError exception...",
  "independent_variable": {
    "name": "Divisor Value",
    "value": "0"
  },
  "dependent_variable": {
    "name": "Calculation Result",
    "expected": "ZeroDivisionError",
    "actual": "Raised expected ZeroDivisionError"
  },
  "timestamp": "20250415_144710",
  "generated_on": "20250415_144710",
  "outcome": "passed"
}
```

These result files include:
- Test metadata (title, function name, hypothesis)
- Variable definitions with expected and actual values
- Test outcome (passed, failed, skipped)
- Error details (for failed tests)
- Timestamps for test execution

### Adding New Templates

To add a new test framework template:

1. Create a new template file in the `templates/` directory (e.g., `pytest_test.py.j2`)
2. Update the `_get_template()` method in `generator.py`
3. Add the new framework to the valid harnesses list in `configs.py`

#### Template Structure Requirements

Templates must follow a standard structure to ensure proper test generation:

- **Variable Definitions**: Include sections for independent, dependent, and control variables
- **Test Implementation**: Use NotImplementedError with descriptive messages for placeholder code
- **Result Reporting**: Include JSON result generation with test status capture
- **Framework Integration**: Use framework-specific features (e.g., plugins for pytest)

For framework-specific features:
- **unittest**: Use TestCase.setUp, tearDown, and assertion methods
- **pytest**: Implement test fixtures and plugins for result collection

### Project Structure

```
test_generator_mk2/
├── cli.py                   # Command-line interface
├── configs.py               # Configuration validation
├── generator.py             # Core generation logic
├── main.py                  # Main entry point
├── schemas/                 # Pydantic models
├── templates/               # Jinja2 templates
├── tests/                   # Unit tests
└── utils/                   # Utility functions
```

## Roadmap

See the [TODO.md](./TODO.md) file for planned enhancements and the [CHANGELOG.md](./CHANGELOG.md) for recent updates.