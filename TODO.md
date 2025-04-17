# Implementation Plan for Test Generator Mk2

## Phase 1: Core Refactoring

### 1. Project Structure Refactoring
- [x] Reorganize directory structure according to SAD
- [x] Create separate CLI module (cli.py)
- [x] Create core generator module (generator.py)
- [x] Set up template directory

### 2. Schema Refinements
- [x] Fix TestTitle implementation to be more intuitive
- [x] Standardize naming between JSON and models
- [x] Add proper validation for all fields
- [x] Fix circular imports in Variable class
- [x] Improve validation methods for expected values
- [x] Add case-insensitive handling for StatisticalType enum
- [x] Implement strict validation for dependent_variable

### 3. Core Logic Improvements
- [x] Implement proper logging instead of print statements
- [x] Create template engine integration (Jinja2)
- [x] Separate test generation from CLI concerns
- [x] Implement clean processing pipeline

## Phase 2: Templates and Features

### 1. Template System
- [x] Create base template
- [x] Implement unittest template
- [x] Implement pytest template with proper plugin support
- [x] Add support for fixture handling

### 2. Enhanced Features
- [x] Add support for parametrized tests
- [x] Implement conditional test generation
- [x] Add test discovery features
- [x] Support generating both test file and JSON output
- [x] Automatic test result collection and reporting

### 3. Error Handling
- [x] Create custom exception hierarchy
- [x] Add detailed error messages
- [x] Implement input validation with useful feedback
- [x] Add debug mode with enhanced output

## Phase 3: Documentation and Testing

### 1. Documentation
- [x] Update README with usage examples
- [x] Create schema documentation
- [x] Add inline code comments
- [x] Create example JSON templates

### 2. Testing
- [x] Create unit tests for core components
- [x] Add integration tests for pipeline
- [x] Implement test fixtures
- [x] Add test reporting in JSON and Markdown
- [x] Implement proper mocking for test isolation
- [x] Fix path comparison in tests
- [x] Achieve 100% test success rate
- [x] Add test coverage reporting

## Phase 4: Polish and Release

### 1. Quality Improvements
- [x] Fix all test failures
- [ ] Add mypy type checking (configuration added but many type errors remain)
- [ ] Run flake8 linting (configuration added but linting errors remain)
- [ ] Fix all mypy type checking errors
- [ ] Fix all flake8 linting errors
- [ ] Implement pre-commit hooks
- [ ] Code review and refinement

### 2. Release Preparation
- [ ] Version bumping mechanism
- [x] Update CHANGELOG
- [ ] Package for distribution
- [ ] Create example templates

## Next Tasks

2. ✅ Improve test coverage for schema validation methods (completed with comprehensive schema validation tests)
3. ✅ Add test coverage reporting to measure code quality (achieved 95% code coverage with test_coverage.py and test_coverage_reporting.py)
4. ✅ Add support for parameterized tests (implemented with Variable.values and ExpectedValue.values)
5. ✅ Implement debug mode with enhanced logging (added with verbose debug output and CLI parameter)
6. Add `mypy` type checking and `flake8` linting  
7. Package for distribution with proper versioning  
8. ✅ Enhance test templates with more robust implementations (completed for unittest and pytest)
9. ✅ Add validation for template generation success (implemented with test reporting)
10. ✅ Implement automatic test data collection and result statistics (added with JSON result output)
11. Create visual reports of test results and coverage  
12. Add support for async functions
