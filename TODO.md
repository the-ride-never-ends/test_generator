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
- [ ] Fix mypy type checking errors:
  - [x] Fix None checks in generator.py (14 errors)
  - [x] Fix Collection type issues in run_tests.py (16+ errors)
  - [x] Fix incompatible return types in generator.py (4 errors)
  - [x] Fix argument type errors in schemas/imports.py (1 error)
  - [x] Fix name redefinition in generator.py (1 error)
- [ ] Fix flake8 linting errors:
  - [ ] Fix blank line whitespace issues (50+ errors)
  - [ ] Fix f-string missing placeholders (2 errors)
  - [ ] Fix line length issues (1+ errors)
  - [ ] Fix trailing whitespace (4+ errors)
  - [ ] Add missing newlines at end of files (2 errors)
- [x] Implement pre-commit hooks
  - [x] Create .pre-commit-config.yaml with hooks for flake8, mypy, etc.
  - [ ] Test and refine pre-commit hooks
- [x] Implement lint reporting
  - [x] Create system for generating JSON and Markdown reports for linting results
  - [x] Store historical and latest lint reports
  - [x] Display lint reports in run_tests.sh
- [ ] Code review and refinement

### 2. Release Preparation
- [ ] Version bumping mechanism
- [x] Update CHANGELOG
- [ ] Package for distribution
- [ ] Create example templates

## Next Tasks

1. Fix remaining type checking errors in test files:
   - Fix StatisticalType attribute access issues in test_variable.py and test_schema_validation.py
   - Fix ExpectedValue missing parameter errors in tests
   - Fix remaining no-untyped-def errors in tests
2. Fix flake8 linting errors:
   - Fix blank line whitespace issues (696 errors)
   - Fix f-string missing placeholders in lint_report.py and view_report.py
   - Fix line length issues (58 errors)
   - Fix trailing whitespace (46 errors)
   - Add missing newlines at end of files
3. Fix type issues in lint_report.py (name redefinition error)
4. Test and refine pre-commit hooks
5. Add support for async functions