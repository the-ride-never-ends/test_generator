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
- [ ] Add support for fixture handling

### 2. Enhanced Features
- [ ] Add support for parametrized tests
- [ ] Implement conditional test generation
- [ ] Add test discovery features
- [x] Support generating both test file and JSON output
- [x] Automatic test result collection and reporting

### 3. Error Handling
- [x] Create custom exception hierarchy
- [x] Add detailed error messages
- [x] Implement input validation with useful feedback
- [ ] Add debug mode with enhanced output

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
- [ ] Add test coverage reporting

## Phase 4: Polish and Release

### 1. Quality Improvements
- [ ] Add mypy type checking
- [ ] Run flake8 linting
- [ ] Implement pre-commit hooks
- [ ] Code review and refinement

### 2. Release Preparation
- [ ] Version bumping mechanism
- [x] Update CHANGELOG
- [ ] Package for distribution
- [ ] Create example templates

## Next Tasks

1. Fix remaining test issues with `Variable.reject_null` functionality  
2. Improve test coverage for schema validation methods  
3. Add test coverage reporting to measure code quality  
4. Add support for parameterized tests  
5. Implement debug mode with enhanced logging  
6. Add `mypy` type checking and `flake8` linting  
7. Package for distribution with proper versioning  
8. ✅ Enhance test templates with more robust implementations (completed for unittest and pytest)
9. ✅ Add validation for template generation success (implemented with test reporting)
10. ✅ Implement automatic test data collection and result statistics (added with JSON result output)
11. Create visual reports of test results and coverage  
12. Add support for async functions
