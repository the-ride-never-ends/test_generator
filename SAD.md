# System Architecture Document - Test Generator Mk2

## Overview
The Test Generator Mk2 is a Python CLI tool that generates boilerplate code for Python tests. It takes a JSON specification of test parameters and generates test files with appropriate setup, teardown, test methods, and validation.

## Architecture

### Core Components

```
test_generator_mk2/
├── cli.py                   # Command-line interface
├── generator.py             # Core test generation logic
├── schemas/                 # Pydantic models for data validation
├── templates/               # Jinja2 templates for test files
└── utils/                   # Utility functions
```

### Processing Pipeline

The system follows a clear pipeline architecture:

1. **Input** - Parse command-line arguments and input files
2. **Validation** - Validate input against schemas
3. **Transformation** - Convert validated data into test components
4. **Generation** - Generate test code using templates
5. **Output** - Write test files to disk

```
┌─────────┐    ┌───────────┐    ┌───────────────┐    ┌────────────┐    ┌──────────┐
│  Input  ├───►│ Validation├───►│ Transformation├───►│ Generation ├───►│  Output  │
└─────────┘    └───────────┘    └───────────────┘    └────────────┘    └──────────┘
```

## Component Details

### 1. CLI Interface

The CLI component handles:
- Argument parsing
- Configuration loading
- Pipeline orchestration

```python
# cli.py
class CLI:
    def __init__(self):
        self.parser = self._create_parser()
        
    def _create_parser(self):
        # Set up argument parser
        
    def parse_args(self):
        # Parse command-line arguments
        
    def run(self):
        # Orchestrate the pipeline
```

### 2. Core Generator

The core generator handles:
- Loading test specifications
- Applying templates
- Managing the generation process

```python
# generator.py
class TestGenerator:
    def __init__(self, config):
        self.config = config
        self.template_engine = self._initialize_template_engine()
    
    def _initialize_template_engine(self):
        # Set up Jinja2 template engine
    
    def generate_test_file(self, test_params):
        # Generate test file from parameters
        
    def write_test_file(self, test_file, output_path):
        # Write test file to disk
```

### 3. Schema Models

Pydantic models for data validation:
- TestParameters - Overall test parameters
- Variable - Test variables (independent, dependent, control)
- Method - Test method steps and procedures
- Material - Test fixtures and dependencies
- Import - Import statements for test file

### 4. Templates

Jinja2 templates for different test frameworks:
- unittest_test.py.j2
- pytest_test.py.j2

### 5. Utilities

Helper functions for:
- File I/O
- String manipulation
- Path handling
- Validation

## Data Flow

1. User provides JSON file with test parameters
2. CLI parses arguments and loads JSON
3. Parameters are validated against Pydantic models
4. Generator transforms parameters into test components
5. Template engine renders test file
6. Output is written to specified location

## Error Handling

The system employs a hierarchical error handling strategy:
- Schema validation errors - Caught during validation phase
- Template rendering errors - Caught during generation phase
- File I/O errors - Caught during input/output phases

## Extension Points

The architecture allows for extension in several ways:
- New test frameworks via additional templates
- Custom validation methods via schema extensions
- Additional test components via model extensions

## Design Improvements

### Architecture Improvements

1. **Separation of Concerns**
   - Split monolithic TestGeneratorCLI class into focused components:
     - CLI module for argument handling
     - Generator module for core logic
     - Template system for output generation
   - Created clear interfaces between components

2. **Processing Pipeline**
   - Implemented a clear, linear processing flow
   - Each step has well-defined responsibilities
   - Better error propagation between components

3. **Template System**
   - Added Jinja2 template support
   - Created separate templates for different test frameworks
   - Improved code generation readability

4. **Error Handling**
   - Added proper logging instead of print statements
   - Improved validation with helpful error messages
   - Structured exception handling

### Code Quality Improvements

1. **Docstrings and Comments**
   - Added comprehensive Google-style docstrings
   - Improved method and class documentation
   - Added type hints throughout

2. **Model Consistency**
   - Standardized naming between JSON and models
   - Implemented strict validation with proper error handling
   - Improved class relationships
   - Added case-insensitive handling for enumerated types

3. **Configuration**
   - Enhanced configuration validation
   - Added support for different test frameworks
   - Simplified main entry point
   - Fixed path handling and comparison

4. **Testing**
   - Implemented proper test isolation with mocking
   - Fixed circular import issues
   - Added comprehensive validation tests
   - Achieved 100% test success rate
   - Added special handling for exception-based tests
   - Implemented variable name sanitization
   - Added automatic timestamp generation and reporting
   - Created JSON result output for test runs

### Future Enhancements

1. **Template Expansion**
   - Add support for more test frameworks
   - Create fixtures templates
   - Add parametrized test support

2. **CLI Enhancement**
   - Add interactive mode
   - Improve error messaging
   - Add debug output options

3. **Documentation Generator**
   - Generate documentation from test output
   - Create visual test reports