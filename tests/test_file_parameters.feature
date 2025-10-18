Feature: Test File Parameters Parsing
  As a test generator
  I want to parse JSON test parameters into validated objects
  So that I can ensure test specifications are properly structured

  Background:
    Given the TestFileParameters class is available
    And JSON test data is available

  Scenario: Parse test file parameters successfully
    Given I have valid JSON data with test_file_parameters key
    When I create a TestFileParameters instance
    Then all parameters should be parsed correctly
    And the test title should be extracted
    And the background information should be parsed
    And the independent variable should be validated
    And the dependent variable should be validated
    And control variables should be parsed as a list
    And materials should be parsed as a list
    And the test method should be validated
    And imports should be parsed as a list

  Scenario: Parse test file parameters without test_file_parameters key
    Given I have JSON data without test_file_parameters key
    When I attempt to create a TestFileParameters instance
    Then a ValueError should be raised
    And the error message should indicate missing test file parameters

  Scenario: Parse string test title
    Given I have JSON data with a string test title
    When I create a TestFileParameters instance
    Then the test title should be stored as a string
    And the test title should match the input value

  Scenario: Parse TestTitle object
    Given I have JSON data with a TestTitle object
    When I create a TestFileParameters instance
    Then the TestTitle object should be validated
    And the test_title field should be extracted
    And the title should be stored as a string

  Scenario: Parse invalid TestTitle object
    Given I have JSON data with an invalid TestTitle object
    When I create a TestFileParameters instance
    Then a warning should be logged
    And a default test title should be used

  Scenario: Parse unknown test title format
    Given I have JSON data with a non-string, non-dict test title
    When I create a TestFileParameters instance
    Then a warning should be logged
    And a default test title should be used

  Scenario: Parse background information
    Given I have JSON data with complete background information
    When I create a TestFileParameters instance
    Then the orientation field should be extracted
    And the purpose field should be extracted
    And the hypothesis field should be extracted
    And the citation_path field should be extracted
    And the citation field should be extracted

  Scenario: Parse background with missing fields
    Given I have JSON data with partial background information
    When I create a TestFileParameters instance
    Then missing fields should have empty string defaults
    And present fields should have their specified values

  Scenario: Parse independent variable
    Given I have JSON data with a valid independent variable
    When I create a TestFileParameters instance
    Then the independent variable should be validated as a Variable object
    And the variable should have a name
    And the variable should have a description
    And the variable should have a statistical_type
    And the variable should have a unit
    And the variable should have a value

  Scenario: Parse independent variable with parameter values
    Given I have JSON data with an independent variable containing values array
    When I create a TestFileParameters instance
    Then the variable should be parsed with multiple parameter values
    And each parameter value should be accessible

  Scenario: Parse dependent variable
    Given I have JSON data with a valid dependent variable
    When I create a TestFileParameters instance
    Then the dependent variable should be validated as a Variable object
    And the variable should have an expected_value
    And the expected_value should have validation_procedures

  Scenario: Parse dependent variable with exception expected value
    Given I have JSON data with a dependent variable expecting an exception
    When I create a TestFileParameters instance
    Then the expected_value should specify the exception type
    And the validation_procedures should describe exception checking

  Scenario: Parse dependent variable with multiple expected values
    Given I have JSON data with a dependent variable containing values array
    When I create a TestFileParameters instance
    Then multiple expected values should be parsed
    And each expected value should have validation procedures

  Scenario: Parse control variables list
    Given I have JSON data with multiple control variables
    When I create a TestFileParameters instance
    Then each control variable should be validated
    And control variables should be stored as a list
    And each variable should have required fields

  Scenario: Parse control variables with invalid entry
    Given I have JSON data with an invalid control variable
    When I create a TestFileParameters instance
    Then the invalid variable should be skipped with a warning
    And valid control variables should still be parsed

  Scenario: Parse empty control variables list
    Given I have JSON data with an empty control variables array
    When I create a TestFileParameters instance
    Then the control variables list should be empty
    And no errors should be raised

  Scenario: Parse materials list
    Given I have JSON data with test materials
    When I create a TestFileParameters instance
    Then each material should be validated as a Material object
    And materials should include name, type, and version
    And materials may include configuration details

  Scenario: Parse materials with invalid entry
    Given I have JSON data with an invalid material
    When I create a TestFileParameters instance
    Then the invalid material should be skipped with a warning
    And valid materials should still be parsed

  Scenario: Parse test procedure
    Given I have JSON data with a test procedure
    When I create a TestFileParameters instance
    Then the test procedure should be validated as a Method object
    And the procedure should include steps
    And the procedure should include data_collection method
    And the procedure should include analysis_technique

  Scenario: Parse test procedure with invalid data
    Given I have JSON data with an invalid test procedure
    When I attempt to create a TestFileParameters instance
    Then a ValueError should be raised
    And the error message should indicate invalid test procedure data

  Scenario: Parse imports list
    Given I have JSON data with import statements
    When I create a TestFileParameters instance
    Then each import should be validated as an Imports object
    And imports should have a name field
    And imports may have alias or from_module fields

  Scenario: Parse imports with invalid entry
    Given I have JSON data with an invalid import
    When I create a TestFileParameters instance
    Then the invalid import should be skipped with a warning
    And valid imports should still be parsed

  Scenario: Parse empty imports list
    Given I have JSON data with an empty imports array
    When I create a TestFileParameters instance
    Then the imports list should be empty
    And no errors should be raised

  Scenario: Parse complete test specification
    Given I have JSON data with all fields properly specified
    When I create a TestFileParameters instance
    Then all components should be parsed without errors
    And the instance should contain complete test specification
    And the specification should be ready for template rendering
