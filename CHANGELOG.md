# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added comprehensive test coverage reporting functionality
- Added test files specifically for test coverage reporting
- Added comprehensive schema validation tests
- Added tests for TestTitle model validation
- Added tests for all validation methods in schema classes

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