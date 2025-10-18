Feature: Test File Generation
  As a developer
  I want to generate test files from JSON specifications
  So that I can create standardized test boilerplate code

  Background:
    Given the TestGenerator class is available
    And a valid Configs object exists

  Scenario: Initialize TestGenerator with configuration
    Given I have a valid Configs object
    When I create a TestGenerator instance
    Then the generator should be initialized with the configuration
    And the template engine should be set up
    And the test file parameters should be None initially

  Scenario: Initialize TestGenerator with debug mode
    Given I have a Configs object with debug enabled
    When I create a TestGenerator instance
    Then the generator should enable debug logging
    And debug messages should be logged during initialization

  Scenario: Load JSON file successfully
    Given I have a valid test parameter JSON file
    And the TestGenerator is initialized
    When the generator loads the JSON file
    Then the JSON data should be parsed correctly
    And the test file parameters structure should be present

  Scenario: Load JSON file with parametrized test data
    Given I have a test parameter JSON with parameter values
    And debug mode is enabled
    When the generator loads the JSON file
    Then the parameter count should be logged
    And the expected values count should be logged

  Scenario: Parse test parameters successfully
    Given I have valid JSON test data
    When the generator parses the test parameters
    Then a TestFileParameters object should be created
    And the test title should be extracted
    And the independent variable should be validated
    And the dependent variable should be validated
    And control variables should be parsed
    And materials should be parsed
    And imports should be parsed

  Scenario: Parse test parameters with invalid data
    Given I have JSON test data with missing required fields
    When the generator attempts to parse the test parameters
    Then a validation error should be raised
    And an error message should indicate the missing fields

  Scenario: Get template for unittest framework
    Given the configuration specifies unittest as the harness
    When the generator gets the template
    Then the unittest template should be returned
    And the template should contain TestCase class structure

  Scenario: Get template for pytest framework
    Given the configuration specifies pytest as the harness
    When the generator gets the template
    Then the pytest template should be returned
    And the template should contain pytest fixtures

  Scenario: Get template with invalid harness
    Given the configuration specifies an unsupported harness
    When the generator attempts to get the template
    Then a ValueError should be raised
    And an error message should indicate the unsupported harness

  Scenario: Render template with basic test data
    Given I have a template and test parameters
    When the generator renders the template
    Then the test content should be generated
    And the content should include the test title
    And the content should include variable definitions
    And the content should include the test procedure steps
    And the content should include import statements

  Scenario: Render template for exception test
    Given I have test parameters with exception expected value
    When the generator renders the template
    Then the test content should include exception handling
    And the test should verify the exception type
    And the test should capture the exception message

  Scenario: Render template with parametrized flag
    Given I have test parameters with multiple parameter values
    And the configuration has parametrized enabled
    When the generator renders the template
    Then the test content should include parametrization markers
    And each parameter set should be included

  Scenario: Auto-enable parametrization from data structure
    Given I have test parameters with values array
    And the configuration does not have parametrized enabled
    And debug mode is enabled
    When the generator renders the template
    Then parametrization should be auto-enabled
    And a debug message should indicate auto-enabling

  Scenario: Generate test file for unittest
    Given I have a valid configuration for unittest
    And valid test parameters exist in JSON file
    When I call generate_test_file
    Then a complete test file string should be returned
    And the content should be valid Python code
    And the content should include unittest.TestCase class
    And the content should include setUp and tearDown methods
    And the content should include test methods
    And the content should include JSON result logging

  Scenario: Generate test file for pytest
    Given I have a valid configuration for pytest
    And valid test parameters exist in JSON file
    When I call generate_test_file
    Then a complete test file string should be returned
    And the content should be valid Python code
    And the content should include pytest fixtures
    And the content should include test functions
    And the content should include result logger fixture

  Scenario: Generate test file with debug output
    Given I have a configuration with debug enabled
    When I call generate_test_file
    Then debug messages should show configuration settings
    And debug messages should show the harness type
    And debug messages should show parametrization status
    And debug messages should show generated content statistics

  Scenario: Write test file to disk
    Given I have generated test content
    And a valid output directory path
    When I call write_test_file with the content
    Then the output directory should be created if missing
    And a file should be created with test_ prefix
    And the file should have .py extension
    And the file should contain the generated content
    And the file path should be returned
    And a success message should be logged

  Scenario: Write test file with custom output directory
    Given I have generated test content
    And a custom output directory is configured
    When I call write_test_file with the content
    Then the file should be created in the custom directory
    And parent directories should be created if needed

  Scenario: Generate parametrized unittest test
    Given I have a configuration for unittest with parametrized enabled
    And test parameters contain multiple parameter values
    When I call generate_test_file
    Then the test should use subTest for parametrization
    And each parameter set should be tested in a subTest block

  Scenario: Generate parametrized pytest test
    Given I have a configuration for pytest with parametrized enabled
    And test parameters contain multiple parameter values
    When I call generate_test_file
    Then the test should use pytest.mark.parametrize decorator
    And parameter names and values should be specified

  Scenario: Generate test with fixtures
    Given I have a configuration with has_fixtures enabled
    When I call generate_test_file
    Then the test should include fixture setup code
    And the test should include fixture teardown code
    And fixtures should be properly used in test methods

  Scenario: Generate test with conditional validation
    Given I have test parameters with condition expressions
    And test_params are provided in configuration
    When I call generate_test_file
    Then conditional test logic should be included
    And conditions should be evaluated based on test_params
