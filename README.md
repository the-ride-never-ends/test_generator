# Test Generator Mk2

A tool for generating structured Python tests from JSON specifications using a scientific approach.

## Overview

Test Generator Mk2 creates test boilerplate code with a scientific approach to testing:
- Clearly defined hypotheses
- Independent and dependent variables
- Controlled variables
- Structured validation

## Features

- Generate test files for unittest or pytest
- Define tests in a structured JSON format
- Support for variable definitions and relationships
- Template-based generation with Jinja2
- Validation of expected vs actual results
- Clean separation of concerns
- Proper logging and error handling

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
            "orientation": "Previous performance tests showed varying query performance with different connection pool sizes.",
            "purpose": "Determine the optimal connection pool size for maximum database query performance.",
            "citation_path": "path/to/citation1.md",
            "citation": "Optimize connection pool size for PostgreSQL",
            "hypothesis": "A larger connection pool will improve performance up to a certain threshold, after which contention for database resources will cause performance degradation."
        },
        "test_title": "The Effect of Connection Pool Size on Database Query Performance",
        "independent_variable": {
            "name": "Connection Pool Size",
            "description": "Number of connections maintained in the database connection pool",
            "statistical_type": "DISCRETE",
            "unit": "connections",
            "value": 10
        },
        "dependent_variable": {
            "name": "Query Response Time",
            "description": "Average time in milliseconds taken to execute a standard query",
            "statistical_type": "CONTINUOUS",
            "expected_value": {
                "value": 100.0,
                "validation_methods": [
                    {
                        "description": "Check if the response time is within expected range",
                        "name": "range",
                        "kwargs": {
                            "min": 50.0,
                            "max": 200.0
                        },
                        "steps": [
                            "Run the benchmark query",
                            "Measure the response time",
                            "Compare with expected range"
                        ]
                    }
                ]
            }
        },
        "control_variables": [
            {
                "name": "Database Size",
                "description": "Size of the test database",
                "statistical_type": "CONTINUOUS",
                "unit": "GB",
                "value": 1.0
            },
            {
                "name": "Query Complexity",
                "description": "Complexity of the test query",
                "statistical_type": "ORDINAL",
                "unit": "level",
                "value": "medium"
            }
        ],
        "test_materials": [
            {
                "name": "PostgreSQL Database",
                "description": "Test database server",
                "type": "software",
                "version": "14.1",
                "configuration": {
                    "max_connections": 100,
                    "shared_buffers": "1GB",
                    "work_mem": "64MB"
                }
            }
        ],
        "test_method": {
            "steps": [
                "Set up database with test data",
                "Configure client with specified connection pool size",
                "Run benchmark query suite 100 times",
                "Record average query response time",
                "Analyze results for statistical significance",
                "Clean up test resources"
            ],
            "data_collection": "Automated benchmark metrics with detailed timing breakdown",
            "analysis_technique": "Mean response time with 95% confidence intervals"
        },
        "imports": [
            {
                "name": "psycopg2"
            },
            {
                "name": "numpy",
                "import_funcs": ["mean", "std"]
            },
            {
                "name": "pandas"
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
- **Expected Value Validation**: Dependent variables must have validation_methods specified
- **Proper Test Isolation**: Tests use mocking to ensure proper unit testing isolation
- **Case Insensitivity**: Statistical types are handled case-insensitively (e.g., "DISCRETE" or "discrete")
- **Path Handling**: Path objects and strings are properly compared
- **Exception Testing**: Special handling for tests that expect exceptions
- **Variable Sanitization**: Converts variable names to valid Python identifiers
- **Automated Results**: Test files include JSON result generation with timestamps

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

### Adding New Templates

To add a new test framework template:

1. Create a new template file in the `templates/` directory (e.g., `pytest_test.py.j2`)
2. Update the `_get_template()` method in `generator.py`
3. Add the new framework to the valid harnesses list in `configs.py`

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