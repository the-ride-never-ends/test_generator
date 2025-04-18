# Example Templates for Test Generator

This directory contains example JSON templates for generating different types of tests using the Test Generator tool. These templates demonstrate various testing scenarios and can be used as starting points for your own test definitions.

## Available Templates

### 1. Simple Parametrized Test Example (`simple_parametrized_test.json`)

A straightforward example of a parametrized test for string length calculation.
- Tests string length with various input types (basic string, empty string, whitespace, numeric)
- Shows the correct schema format for parametrized tests
- A good starting point for understanding parametrized tests

```bash
python -m test_generator_mk2 --name "String Length Test" --description "Tests for string length calculation" --test_parameter_json example_templates/simple_parametrized_test.json --parametrized
```

### 2. Advanced Parametrized Test Example (`parametrized_test.json`) (Schema Reference Only)

Demonstrates how to create tests with multiple input/output value pairs for a string capitalization function.
- Tests multiple input types (normal string, already capitalized, all caps, mixed case, etc.)
- Defines expected outputs for each input case
- Shows how to structure parametrized test data

```bash
# NOTE: This template is for reference only - use simple_parametrized_test.json for actual test generation
```

### 3. Fixture-Based Test Example (`fixture_test.json`) (Schema Reference Only)

Shows how to define tests that require test fixtures, such as a database connection.
- Demonstrates database interaction testing
- Includes setup and teardown steps
- Shows how to test record insertion and retrieval

```bash
# NOTE: This template is for reference only - actual implementation requires schema modifications
# python -m test_generator_mk2 --name "Database Record Test" --test_parameter_json example_templates/fixture_test.json --has-fixtures
```

### 4. Conditional Test Example (`conditional_test.json`) (Schema Reference Only)

Illustrates how to create tests with conditional validation procedures based on input parameters.
- Demonstrates testing with different response formats (JSON, XML, YAML)
- Shows how to conditionally execute different validation procedures
- Includes custom test parameters

```bash
# NOTE: This template is for reference only - actual implementation requires schema modifications
# python -m test_generator_mk2 --name "Response Format Test" --test_parameter_json example_templates/conditional_test.json --test-params '{"response_type": "json"}'
```

### 5. API Testing Example (`api_test.json`) (Schema Reference Only)

Provides a template for testing REST API endpoints with different request/response scenarios.
- Tests both successful and error response handling
- Includes multiple test cases for different validation errors
- Shows how to structure API test expectations

```bash
# NOTE: This template is for reference only - actual implementation requires schema modifications
# python -m test_generator_mk2 --name "User Registration API Test" --test_parameter_json example_templates/api_test.json --parametrized
```

### 6. Data Validation Example (`data_validation_test.json`) (Schema Reference Only)

Demonstrates testing data validation logic with various input scenarios.
- Tests both valid and invalid data cases
- Covers multiple validation rules (required fields, format validation, etc.)
- Shows how to structure validation test expectations

```bash
# NOTE: This template is for reference only - actual implementation requires schema modifications
# python -m test_generator_mk2 --name "User Profile Validation Test" --test_parameter_json example_templates/data_validation_test.json --parametrized
```

## Using the Templates

1. Choose a template that matches your testing needs
2. Copy and modify the template for your specific use case
3. Run the test generator with your modified template
4. The generated test file will be in your specified output directory

## Template Structure

Each template follows the standard test_file_parameters JSON structure:

- `background`: Context and purpose of the test
- `test_title`: The title of the test
- `independent_variable`: The input or action being tested
- `dependent_variable`: The expected output or result
- `control_variables`: Variables kept constant during testing
- `test_materials`: Libraries and dependencies needed
- `test_procedure`: The steps to execute the test
- `imports`: Required import statements

For parametrized tests, the `values` array within the independent and dependent variables allows defining multiple test cases.

For conditional tests, add a `condition` field to validation procedures to specify when they should be executed.

## Custom Test Parameters

For conditional tests, you can pass custom parameters using the `--test-params` option:

```bash
python -m test_generator_mk2 --name "API Test" --test_parameter_json example_templates/conditional_test.json --test-params '{"response_type": "xml", "auth_enabled": true}'
```

These parameters can be referenced in the validation procedures' `condition` field to control which validation procedures are included in the generated test.