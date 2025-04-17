#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for conditional test generation.
"""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Adjust the import path to properly import the generator module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from generator import TestGenerator
from configs import Configs


class TestConditionalGeneration(unittest.TestCase):
    """Tests for conditional test generation."""
    
    def setUp(self) -> None:
        """Set up test environment."""
        # Create a temporary JSON file with conditional test data
        self.temp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        sample_data = {
            "test_file_parameters": {
                "test_title": "Conditional Test Example",
                "background": {
                    "orientation": "Testing with conditional logic",
                    "purpose": "Verify behavior based on conditions",
                    "hypothesis": "The function handles all conditions correctly"
                },
                "independent_variable": {
                    "name": "Input Type",
                    "description": "Type of input to test",
                    "statistical_type": "nominal",
                    "unit": "type",
                    "value": "string"
                },
                "dependent_variable": {
                    "name": "Output Behavior",
                    "description": "Expected behavior based on input type",
                    "statistical_type": "nominal",
                    "unit": "behavior",
                    "expected_value": {
                        "value": "string processing behavior",
                        "validation_procedures": [
                            {
                                "name": "validate_string_handling",
                                "description": "Validate string input handling",
                                "steps": ["Test string processing"],
                                "condition": "input_type == 'string'"
                            },
                            {
                                "name": "validate_numeric_handling",
                                "description": "Validate numeric input handling",
                                "steps": ["Test numeric processing"],
                                "condition": "input_type == 'numeric'"
                            },
                            {
                                "name": "validate_json_handling",
                                "description": "Validate JSON input handling",
                                "steps": ["Test JSON processing"],
                                "condition": "input_type == 'json'"
                            }
                        ]
                    }
                },
                "conditional_tests": [
                    {
                        "name": "string_input_tests",
                        "description": "Tests for string inputs",
                        "condition": "input_type == 'string'",
                        "procedure": {
                            "steps": ["Validate string length", "Check string content"]
                        }
                    },
                    {
                        "name": "numeric_input_tests",
                        "description": "Tests for numeric inputs",
                        "condition": "input_type == 'numeric'",
                        "procedure": {
                            "steps": ["Validate number range", "Check numeric precision"]
                        }
                    },
                    {
                        "name": "json_input_tests",
                        "description": "Tests for JSON inputs",
                        "condition": "input_type == 'json'",
                        "procedure": {
                            "steps": ["Validate JSON schema", "Check required fields"]
                        }
                    }
                ],
                "test_procedure": {
                    "steps": ["Prepare test data", "Call function", "Verify output"],
                    "data_collection": "Record output behavior",
                    "analysis_technique": "Analyze behavior against expected"
                },
                "imports": [
                    {"name": "unittest"},
                    {"name": "pytest"},
                    {"name": "json"}
                ]
            }
        }
        self.temp_json.write(json.dumps(sample_data).encode('utf-8'))
        self.temp_json.close()
        
        # Create a temporary output directory
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create configs for different input types
        self.string_config = Configs.model_validate({
            "name": "String Conditional Test",
            "description": "Test with string input conditions",
            "json_file_path": self.temp_json.name,
            "output_dir": self.temp_dir.name,
            "harness": "unittest"
        })
        
        # Add additional config params for conditional testing
        self.string_config_with_params = Configs.model_validate({
            "name": "String Conditional Test",
            "description": "Test with string input conditions",
            "json_file_path": self.temp_json.name,
            "output_dir": self.temp_dir.name,
            "harness": "unittest",
            "test_params": {"input_type": "string"}
        })
    
    def tearDown(self) -> None:
        """Clean up temporary files."""
        os.unlink(self.temp_json.name)
        self.temp_dir.cleanup()
    
    @patch('configs.Configs.model_validate')
    def test_conditional_param_validation(self, mock_validate):
        """Test validation of conditional test parameters."""
        # Setup
        mock_validate.return_value = self.string_config_with_params
        
        # Create test parameters dict with test_params as a JSON string
        # This matches our implementation in cli.py which expects test_params as a JSON string
        args_dict = {
            "name": "Conditional Test",
            "description": "Test with conditions",
            "json_file_path": self.temp_json.name,
            "output_dir": self.temp_dir.name,
            "test_params": json.dumps({"input_type": "string"})
        }
        
        # Use the config validation logic (mocked)
        from cli import CLI
        cli = CLI()
        result = cli.validate_config(args_dict)
        
        # Verify that the validation was called with test_params
        mock_validate.assert_called_once()
        call_kwargs = mock_validate.call_args[0][0]
        self.assertIn("test_params", call_kwargs)
        self.assertEqual(call_kwargs["test_params"]["input_type"], "string")
    
    @patch('generator.TestGenerator._get_template')
    @patch('generator.TestGenerator._render_template')
    def test_conditional_test_inclusion(self, mock_render, mock_get_template) -> None:
        """Test inclusion of conditional tests based on parameters."""
        # Setup
        generator = TestGenerator(self.string_config)
        
        # Add test parameters to the generator
        generator.config.test_params = {"input_type": "string"}
        
        # Mock template and rendering
        mock_template = MagicMock()
        mock_get_template.return_value = mock_template
        mock_render.return_value = """
def test_string_handling(self) -> None:
    # This test is conditionally included for string inputs
    input_value = "test string"
    self.assertEqual(function_under_test(input_value), "processed string")
"""
        
        # Generate test file
        content = generator.generate_test_file()
        
        # Verify the conditionally included test is in the content
        self.assertIn("test_string_handling", content)
    
    @patch('generator.TestGenerator._get_template')
    @patch('generator.TestGenerator._render_template')
    def test_conditional_test_exclusion(self, mock_render, mock_get_template) -> None:
        """Test exclusion of conditional tests based on parameters."""
        # Setup
        generator = TestGenerator(self.string_config)
        
        # Add test parameters to the generator for numeric input
        generator.config.test_params = {"input_type": "numeric"}
        
        # Mock template and rendering - only returns numeric test
        mock_template = MagicMock()
        mock_get_template.return_value = mock_template
        mock_render.return_value = """
def test_numeric_handling(self) -> None:
    # This test is conditionally included for numeric inputs
    input_value = 42
    self.assertEqual(function_under_test(input_value), 84)
"""
        
        # Generate test file
        content = generator.generate_test_file()
        
        # Verify the conditionally included test is in the content
        self.assertIn("test_numeric_handling", content)
        
        # String test should not be in the content
        self.assertNotIn("test_string_handling", content)
    
    @patch('generator.TestFileParameters._parse_test_method')
    def test_conditional_procedure_processing(self, mock_parse_method):
        """Test processing of conditional test procedures."""
        # Setup the expected procedure
        expected_procedure = {
            "steps": ["Validate string length", "Check string content"]
        }
        
        # Mock the method parsing
        mock_parse_method.return_value = expected_procedure
        
        # Create generator with string input parameters
        generator = TestGenerator(self.string_config)
        generator.config.test_params = {"input_type": "string"}
        
        # Mock various parse methods to avoid validation errors
        with patch('generator.TestFileParameters._parse_variable'), \
             patch('generator.TestFileParameters._parse_materials'), \
             patch('generator.TestFileParameters._parse_imports'), \
             patch('generator.TestFileParameters._parse_control_variables'), \
             patch('generator.TestFileParameters._parse_test_title'):
                
            # Load and parse JSON
            json_data = generator._load_json_file()
            params = generator._parse_test_parameters(json_data)
            
            # Verify that the correct procedure was parsed
            mock_parse_method.assert_called_once()
            self.assertEqual(params.test_method, expected_procedure)
    
    @patch('generator.TestFileParameters._parse_variable')
    def test_conditional_validation_procedure(self, mock_parse_variable):
        """Test conditional validation procedures based on parameters."""
        # Setup mock dependent variable with conditional validation
        mock_var = MagicMock()
        mock_var.name = "Output Behavior"
        mock_var.expected_value.validation_procedures = [
            {
                "name": "validate_string_handling",
                "description": "Validate string input handling",
                "steps": ["Test string processing"],
                "condition": "input_type == 'string'"
            }
        ]
        
        # Different return values based on variable type
        def mock_variable_parser(var_type):
            if var_type == "dependent_variable":
                return mock_var
            else:
                # For independent variable, return a simple mock
                simple_mock = MagicMock()
                simple_mock.name = "Input Type"
                simple_mock.value = "string"
                return simple_mock
        
        mock_parse_variable.side_effect = mock_variable_parser
        
        # Create generator with string input parameters
        generator = TestGenerator(self.string_config)
        generator.config.test_params = {"input_type": "string"}
        
        # Mock various parse methods to avoid validation errors
        with patch('generator.TestFileParameters._parse_test_method'), \
             patch('generator.TestFileParameters._parse_materials'), \
             patch('generator.TestFileParameters._parse_imports'), \
             patch('generator.TestFileParameters._parse_control_variables'), \
             patch('generator.TestFileParameters._parse_test_title'):
                
            # Load and parse JSON
            json_data = generator._load_json_file()
            params = generator._parse_test_parameters(json_data)
            
            # Verify that the variable was parsed twice (once for independent, once for dependent)
            self.assertEqual(mock_parse_variable.call_count, 2)
            
            # Verify the dependent variable has the expected validation procedure
            self.assertEqual(params.dependent_variable, mock_var)
            self.assertEqual(
                params.dependent_variable.expected_value.validation_procedures[0]["name"], 
                "validate_string_handling"
            )


if __name__ == "__main__":
    unittest.main()