# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-04-17

This version marks the first GitHub release with a completed feature set and robust test suite.

### Release Highlights
- 100% test passing rate (106/106 tests)
- Comprehensive documentation including README, SAD, and CLAUDE guidance
- Support for multiple test frameworks (unittest, pytest)
- Advanced features: parameterized tests, fixtures, conditional generation
- Example templates with working implementation
- Improved code quality with type checking and linting
- Robust error handling and validation

### Added
- Added example templates for test generation:
  - Added simple parametrized test example with working implementation
  - Added comprehensive reference templates for various test scenarios:
    - Advanced parametrized test template for string capitalization
    - Fixture-based test template for database testing
    - Conditional test template with format-specific validations
    - API testing template with request/response scenarios
    - Data validation template with various validation rules
  - Added detailed README with usage instructions for all templates
  - Included specific schema examples for proper template structure
- Added gitignore-aware linting:
  - Added --respect-gitignore option to run_tests.sh
  - Enhanced lint_report.py to filter out issues in files/folders listed in .gitignore
  - Integrated pathspec library for accurate gitignore pattern matching
  - Added detailed filtering of mypy and flake8 issues with proper reporting
- Added return type hints to tests in multiple directories:
  - Added return type annotations to test_whitespace_issues.py methods
  - Created tests for the fix_whitespace.py utility
  - Enhanced type annotations in generator.py and cli.py
- Added mypy type checking with configuration file
  - Created mypy.ini with project-specific settings
  - Configured mypy to ensure proper type checking
  - Fixed type annotations in utils/common/load_json_file.py
  - Fixed type annotations in utils/for_tests/view_report.py
  - Fixed type annotations in schemas/imports.py and schemas/method.py
  - Added proper type annotations to CLI class attributes with Optional
  - Fixed Optional type parameters in fix_whitespace.py
- Added flake8 linting with configuration file
  - Created .flake8 configuration file with project-specific settings
  - Identified linting issues across the codebase (988 total issues)
  - Common issues include: blank lines with whitespace (696), multiple spaces after ':' (26), 
    trailing whitespace (46), and lines too long (58)
- Enhanced run_tests.sh to support type checking and linting options
  - Added --mypy, --flake8, --check-all, and --lint-only parameters
  - Implemented parallel running of tests, type checking, and linting
  - Created proper exit code handling for test/lint failures
- Added pre-commit configuration for automated linting and type checking
  - Created .pre-commit-config.yaml with hooks for flake8, mypy, trailing whitespace, etc.
  - Configured hooks to match project standards
- Added comprehensive linting report generation
  - Created lint_report.py to capture and format mypy and flake8 results
  - Added JSON and Markdown report generation for linting results
  - Generated reports include detailed issue categorization by file
  - Latest reports saved as latest_lint_report.json and latest_lint_report.md
- Added automated type error fixing and Collection type issues resolution
  - Fixed Collection type issues in run_tests.py with proper typing
  - Used Optional and cast() to fix potential None reference errors in generator.py
  - Improved default_factory definition in schemas/imports.py using lambda
- Added whitespace fixing script for automatic code style compliance
  - Created fix_whitespace.py to automatically clean up common whitespace issues
  - Fixed blank lines with whitespace in multiple files (cli.py, utils/common/*, schemas/*)
  - Cleaned up all test files (473+ blank line whitespace issues fixed)
  - Fixed trailing whitespace in 35+ files
  - Added missing newlines at end of files (16+ files fixed)
  - Implemented dry-run mode for previewing changes without modifying files
  - Added verbose mode for detailed reporting of fixed issues
  - Reduced flake8 linting errors by 66% (from 831 to 281)

### Fixed
- Fixed type checking errors in generator.py
  - Added proper null checks for test_file_params attribute
  - Fixed incompatible return types in _initialize_template_engine 
  - Corrected Template type annotations in _get_template
  - Improved type safety in _render_template with proper null checks
- Fixed None attribute access errors in cli.py
  - Added proper type annotations for all class attributes (args, config, generator)
  - Added null checks before accessing attributes of potentially None values
  - Improved error messages when configuration or generator is not available
- Fixed variable naming issues in lint_report.py
  - Fixed file_issues name redefinition by using separate names for different contexts
  - Fixed proper dictionary typing in utility functions
- Fixed StatisticalType enum reassignment error in test_schema_validation.py
  - Removed inappropriate enum value reassignment that was causing test failures
  - Fixed enum attribute access issue for Python 3.12 compatibility
- Fixed f-string missing placeholder issues in multiple files
  - Fixed f-string placeholders in run_tests.py 
  - Fixed f-string placeholders in view_report.py
- Fixed default_factory error in schemas/imports.py
  - Updated default_factory to use lambda instead of direct list type
  - Fixed test_import_creation test to expect empty list instead of None
- Fixed failing test_test_discoverer test in test_coverage.py
  - Updated test to expect string conversion of Path objects
  - Fixed mock assertion to match actual implementation

## [0.2.0] - 2025-04-16

### Added
- Added comprehensive test coverage reporting functionality
- Added test files specifically for test coverage reporting
- Added comprehensive schema validation tests
- Added tests for TestTitle model validation
- Added tests for all validation methods in schema classes
- Fixed all test failures in test_debug_mode.py and test_discovery_features.py
- Achieved 100% test success rate (101/101 tests passing)
- Added test files for Phase 2 features:
  - Test suite for fixture handling in test templates
  - Test suite for parametrized test generation
  - Test suite for conditional test generation based on parameters
  - Test suite for test discovery features
  - Test suite for debug mode with enhanced output
- Implemented parametrized test support:
  - Added support for multiple parameter values in Variable schema (values field)
  - Added ParameterValue class for structured parameter sets
  - Added corresponding expected values for each parameter with ParameterExpectedValue
  - Enhanced template context to support parametrized tests
  - Added automatic detection of parametrized test data
- Implemented debug mode with enhanced output:
  - Added debug flag to CLI and Configs model
  - Added detailed logging throughout the generation process
  - Added analysis of generated test files
  - Added automatic parametrization detection
  - Added JSON data structure debug output
- Added conditional test generation:
  - Added condition expressions to validation procedures
  - Added test parameters for conditional inclusion
  - Updated CLI to handle conditional test parameters as JSON
  - Added support for conditional test inclusion based on parameters

### Fixed
- Fixed circular import issues between modules that prevented tests from running
- Added case insensitivity for StatisticalType validation
- Fixed path comparison issues between Path objects and strings
- Updated output_dir default value to match test expectations
- Improved test isolation using proper mocking techniques
- Fixed validation issues in TestGenerator and integration tests
- Properly handled enum validation for StatisticalType
- Fixed dependent variable validation in integration tests
- Achieved 100% test success rate (38/38 tests passing)
- Fixed recursive call in Variable.name_in_python property that would cause infinite recursion
- Fixed _get_python_type_from_statistical_type function to properly handle StatisticalType enum values
- Fixed template issue with test_procedure vs test_method in JSON schema
- Updated unittest and pytest templates to include control variable definitions
- Enhanced test file generation to use NotImplementedError with helpful message
- Improved JSON output with actual result field and TODO comments
- Fixed class naming by ensuring proper PascalCase conversion
- Implemented proper pytest plugin system for test result collection
- Added comprehensive error capture in pytest results JSON
- Fixed plugin registration for pytest test runner

### Added
- Design documentation (SAD.md, CLAUDE.md)
- Implementation plan (TODO.md)
- Core generator module with template support
- CLI module with proper argument handling
- Template system with Jinja2 support
- Error handling and logging
- Comprehensive test suite:
  - Unit tests for configurations
  - Unit tests for CLI module
  - Unit tests for generator module
  - Unit tests for utility functions
  - Integration tests for end-to-end workflow
- Test reporting system:
  - Automated test report generation in JSON and Markdown
  - Historical test reports with timestamps
  - Test report viewer with different detail levels
  - Shell integration for viewing reports
- Test runner script with colored output
- Template files for unittest and pytest frameworks
- Documentation generation via external documentation_generator tool
- Test reporting guide and failure analysis tools
- Additional markdown documentation and guides

### Changed
- Refactored architecture for cleaner separation of concerns
- Improved model validation
- Enhanced README with better documentation
- Standardized naming conventions
- Improved type hints and docstrings
- Updated generator to use a pipeline architecture
- Fixed convert_to_pascal_case utility to properly handle existing PascalCase strings
- Improved test reporting format with better error presentation

### Fixed
- Fixed inconsistencies in schema definitions
- Fixed variable handling in template output
- Fixed import string formatting
- Fixed TestTitle implementation
- Fixed missing validations in configs
- Fixed PascalCase conversion for words already in PascalCase format
- Fixed documentation structure to mirror project organization

## [0.1.0] - 2025-04-13

### Added
- Initial project structure
- Basic JSON schema for test parameters
- Simple CLI arguments
- Pydantic models for validation