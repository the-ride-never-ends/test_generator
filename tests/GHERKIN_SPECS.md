# Gherkin Specifications for Test Generator

This directory contains Gherkin feature files that describe the externally confirmable behavior of the Test Generator's public API.

## Overview

The Gherkin specifications focus on **externally confirmable behavior** - the observable interactions and outcomes that users can verify when using the Test Generator. These specifications describe what the system does from an external perspective, not internal implementation details.

## Feature Files

### 1. cli.feature (13 scenarios)
**Focus**: Command-Line Interface public methods and behavior

Covers the public callables in the CLI module:
- `CLI.parse_args()` - Parsing command-line arguments
- `CLI.validate_config()` - Configuration validation
- `CLI.run()` - Test generation execution
- `cli.main()` - Main entry point

**Key Behaviors**:
- Argument parsing with required and optional parameters
- Configuration validation with valid and invalid inputs
- Debug mode activation and logging
- Test file generation workflow
- Error handling and exit codes
- Parametrized and fixture-based test generation

### 2. test_generator.feature (22 scenarios)
**Focus**: TestGenerator class public methods

Covers the public callables in the TestGenerator class:
- `TestGenerator.__init__()` - Generator initialization
- `TestGenerator.generate_test_file()` - Test file content generation
- `TestGenerator.write_test_file()` - Writing test files to disk

**Key Behaviors**:
- Template engine initialization
- JSON file loading and parsing
- Template selection for different frameworks (unittest, pytest)
- Template rendering with test parameters
- Exception test generation
- Parametrized test generation (auto-detection and explicit)
- Debug output and logging
- File system operations

### 3. test_file_parameters.feature (24 scenarios)
**Focus**: TestFileParameters class parsing and validation

Covers the public callable TestFileParameters constructor:
- `TestFileParameters.__init__()` - JSON parameter parsing

**Key Behaviors**:
- Parsing test specifications from JSON
- Validating required fields
- Handling different data formats (strings, objects, arrays)
- Default value handling
- Error handling for invalid data
- Component parsing (variables, materials, imports, procedures)
- Parametrized test data structures

### 4. test_generation_workflow.feature (20 scenarios)
**Focus**: End-to-end test generation workflows

Covers the complete system behavior from user perspective:
- Full workflow from specification to generated test file
- Framework-specific generation (unittest and pytest)
- Special test types (exception, parametrized, fixtures)
- File system interactions
- Result generation
- Error scenarios

**Key Behaviors**:
- Complete test file generation for both frameworks
- Exception handling test generation
- Parametrized test generation with multiple parameter sets
- Fixture support
- Custom output directories
- Debug mode operation
- Auto-detection of parametrized tests
- Variable name sanitization
- JSON result file generation
- Error handling for missing or invalid inputs

## Scenario Statistics

- **Total Feature Files**: 4
- **Total Scenarios**: 79
- **Total Lines**: 645
- **Total Given Steps**: 83
- **Total When Steps**: 79
- **Total Then Steps**: 79

## Design Principles

The Gherkin specifications follow these principles:

1. **External Perspective**: Focus on what users can observe and verify, not internal implementation
2. **Behavior-Driven**: Describe behaviors and outcomes, not code structure
3. **Testable**: Each scenario describes a specific, verifiable behavior
4. **Complete Coverage**: Cover all public callables and their edge cases
5. **User-Centric**: Written from the perspective of developers using the tool

## Usage

These Gherkin specifications serve multiple purposes:

1. **Documentation**: Human-readable description of system behavior
2. **Specification**: Define expected behavior for implementation
3. **Test Planning**: Guide for creating automated tests
4. **Communication**: Share understanding between developers, testers, and stakeholders
5. **Validation**: Verify that the system meets requirements

## Relationship to Existing Tests

The repository already contains comprehensive Python unit tests in files like:
- `test_cli.py`
- `test_generator.py`
- `test_integration.py`
- `test_parametrized_tests.py`
- etc.

These Gherkin specifications complement the existing tests by:
- Providing a high-level, framework-agnostic description of behavior
- Focusing on external, observable outcomes
- Serving as living documentation
- Making requirements explicit and understandable to non-programmers

## Reading the Specifications

Each feature file follows the Gherkin format:

```gherkin
Feature: High-level capability
  As a [role]
  I want to [action]
  So that [benefit]

  Background:
    Given [common preconditions]

  Scenario: Specific behavior
    Given [preconditions]
    When [action]
    Then [expected outcome]
    And [additional outcomes]
```

- **Feature**: Describes a high-level capability
- **Background**: Common setup for all scenarios
- **Scenario**: Specific behavior with Given-When-Then structure
- **Given**: Preconditions and context
- **When**: Action taken
- **Then**: Expected observable outcome
- **And**: Additional conditions or outcomes

## Future Enhancements

These specifications could be used to:
- Generate automated tests using BDD frameworks (behave, pytest-bdd)
- Create executable specifications
- Generate additional documentation
- Validate system behavior against requirements
- Guide regression testing
