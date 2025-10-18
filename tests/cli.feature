Feature: Command-Line Interface
  As a developer
  I want to use the CLI to generate test files
  So that I can automate test creation from JSON specifications

  Background:
    Given the test generator CLI is available
    And a valid test parameter JSON file exists

  Scenario: Parse command-line arguments successfully
    Given I have command-line arguments with required parameters
    When I parse the arguments
    Then the arguments should be returned as a dictionary
    And all required fields should be present

  Scenario: Parse arguments with optional parameters
    Given I have command-line arguments with optional parameters
    When I parse the arguments
    Then the optional parameters should have their default values
    And the test-params should be properly parsed from JSON string

  Scenario: Validate configuration with valid inputs
    Given I have a valid configuration dictionary
    When I validate the configuration
    Then the validation should succeed
    And a Configs object should be created
    And the output directory should be created if it doesn't exist

  Scenario: Validate configuration with invalid JSON file path
    Given I have a configuration with an invalid JSON file path
    When I validate the configuration
    Then the validation should fail
    And an error message should be logged

  Scenario: Validate configuration with invalid test-params JSON
    Given I have a configuration with malformed test-params JSON
    When I validate the configuration
    Then the validation should fail
    And a JSON decode error should be logged

  Scenario: Enable debug mode via configuration
    Given I have a configuration with debug flag enabled
    When I validate the configuration
    Then the logging level should be set to DEBUG
    And debug messages should be logged

  Scenario: Run test generation successfully
    Given I have a valid CLI configuration
    And the test parameter JSON contains valid test data
    When I run the CLI
    Then the test file should be generated
    And the test file should be written to the output directory
    And the exit code should be 0
    And a success message should be logged

  Scenario: Run test generation with missing configuration
    Given the CLI configuration is not set
    When I run the CLI
    Then the run should fail
    And the exit code should be 1
    And an error message should indicate missing configuration

  Scenario: Run test generation with invalid test parameters
    Given I have a valid CLI configuration
    But the test parameter JSON is invalid
    When I run the CLI
    Then the run should fail
    And the exit code should be 1
    And an error message should be logged with traceback in verbose mode

  Scenario: Generate parametrized test via CLI
    Given I have command-line arguments with parametrized flag
    And the test parameter JSON contains parameter values
    When I run the CLI
    Then a parametrized test file should be generated
    And the test file should include parametrization markers

  Scenario: Generate test with fixtures via CLI
    Given I have command-line arguments with has-fixtures flag
    When I run the CLI
    Then the test file should include fixture setup code
    And the test file should include fixture teardown code

  Scenario: Main entry point executes successfully
    Given I have valid command-line arguments as a list
    When I call the main function with those arguments
    Then the CLI should be initialized
    And the arguments should be parsed
    And the configuration should be validated
    And the generator should run
    And the exit code should be 0

  Scenario: Main entry point handles validation errors
    Given I have invalid command-line arguments
    When I call the main function with those arguments
    Then the validation should fail
    And the exit code should be 1
    And no test file should be generated
