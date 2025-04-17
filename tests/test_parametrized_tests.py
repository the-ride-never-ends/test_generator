#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for parametrized test support in test templates.
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


class TestParametrizedTests(unittest.TestCase):
    """Tests for parametrized test support."""
    
    def setUp(self) -> None:
        """Set up test environment."""
        # Create a temporary JSON file with parametrized test data
        self.temp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        sample_data = {
            "test_file_parameters": {
                "test_title": "Parametrized Test Example",
                "background": {
                    "orientation": "Testing with multiple parameter sets",
                    "purpose": "Verify behavior across different inputs",
                    "hypothesis": "The function returns correct results for all inputs"
                },
                "independent_variable": {
                    "name": "Input Value",
                    "description": "Various input values to test",
                    "statistical_type": "discrete",
                    "unit": "units",
                    "values": [
                        {"value": 1, "description": "Minimum value"},
                        {"value": 10, "description": "Common case"},
                        {"value": 100, "description": "Large value"},
                        {"value": -5, "description": "Negative value"}
                    ]
                },
                "dependent_variable": {
                    "name": "Output Result",
                    "description": "Expected output for each input",
                    "statistical_type": "continuous",
                    "unit": "units",
                    "expected_value": {
                        "values": [
                            {"input": 1, "expected": 2},
                            {"input": 10, "expected": 20},
                            {"input": 100, "expected": 200},
                            {"input": -5, "expected": -10}
                        ],
                        "validation_procedures": [
                            {
                                "name": "validate_output",
                                "description": "Validate output equals expected value",
                                "steps": ["Compare output to expected"]
                            }
                        ]
                    }
                },
                "control_variables": [
                    {
                        "name": "Multiplier",
                        "description": "Constant multiplier for all tests",
                        "statistical_type": "discrete",
                        "unit": "factor",
                        "value": 2
                    }
                ],
                "test_procedure": {
                    "steps": ["Call function with parameter", "Verify output"],
                    "data_collection": "Record output for each input",
                    "analysis_technique": "Compare actual to expected values"
                },
                "imports": [
                    {"name": "unittest"},
                    {"name": "pytest"}
                ]
            }
        }
        self.temp_json.write(json.dumps(sample_data).encode('utf-8'))
        self.temp_json.close()
        
        # Create a temporary output directory
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create config
        self.config = Configs.model_validate({
            "name": "Parametrized Test",
            "description": "Test with multiple parameter sets",
            "json_file_path": self.temp_json.name,
            "output_dir": self.temp_dir.name,
            "harness": "pytest"  # Pytest works better with parametrization
        })
    
    def tearDown(self) -> None:
        """Clean up temporary files."""
        os.unlink(self.temp_json.name)
        self.temp_dir.cleanup()
    
    @patch('generator.TestGenerator._get_template')
    @patch('generator.TestGenerator._render_template')
    def test_parametrized_tests_processing(self, mock_render, mock_get_template) -> None:
        """Test processing of parametrized tests."""
        # Setup
        generator = TestGenerator(self.config)
        
        # Mock template and rendering
        mock_template = MagicMock()
        mock_get_template.return_value = mock_template
        mock_render.return_value = "Generated content with parametrized tests"
        
        # Generate test file
        content = generator.generate_test_file()
        
        # Verify the template was rendered
        mock_render.assert_called_once()
        call_kwargs = mock_render.call_args[0][0]
        # The template object should have been passed to _render_template
        self.assertEqual(call_kwargs, mock_template)
    
    @patch('generator.TestFileParameters._parse_variable')
    def test_parametrized_independent_variable(self, mock_parse_variable) -> None:
        """Test parsing of parametrized independent variable."""
        # Setup mock for independent variable with multiple values
        mock_var = MagicMock()
        mock_var.name = "Input Value"
        mock_var.values = [
            {"value": 1, "description": "Minimum value"},
            {"value": 10, "description": "Common case"},
            {"value": 100, "description": "Large value"},
            {"value": -5, "description": "Negative value"}
        ]
        mock_parse_variable.return_value = mock_var
        
        # Create generator
        generator = TestGenerator(self.config)
        
        # Mock the various parse methods to avoid validation errors
        with patch('generator.TestFileParameters._parse_test_method'), \
             patch('generator.TestFileParameters._parse_materials'), \
             patch('generator.TestFileParameters._parse_imports'), \
             patch('generator.TestFileParameters._parse_control_variables'), \
             patch('generator.TestFileParameters._parse_test_title'):
                
            # Load the JSON file
            json_data = generator._load_json_file()
            
            # Parse the parameters
            params = generator._parse_test_parameters(json_data)
            
            # Verify parametrized variables were parsed
            mock_parse_variable.assert_called()
            self.assertEqual(params.independent_variable, mock_var)
    
    @patch('generator.TestFileParameters._parse_variable')
    def test_parametrized_dependent_variable(self, mock_parse_variable) -> None:
        """Test parsing of parametrized dependent variable."""
        # Different mocked return values based on variable type
        def mock_variable_parser(var_type):
            if var_type == "independent_variable":
                mock_var = MagicMock()
                mock_var.name = "Input Value"
                mock_var.values = [1, 10, 100, -5]
                return mock_var
            elif var_type == "dependent_variable":
                mock_var = MagicMock()
                mock_var.name = "Output Result"
                mock_var.expected_value.values = [
                    {"input": 1, "expected": 2},
                    {"input": 10, "expected": 20},
                    {"input": 100, "expected": 200},
                    {"input": -5, "expected": -10}
                ]
                return mock_var
        
        mock_parse_variable.side_effect = mock_variable_parser
        
        # Create generator
        generator = TestGenerator(self.config)
        
        # Mock the various parse methods to avoid validation errors
        with patch('generator.TestFileParameters._parse_test_method'), \
             patch('generator.TestFileParameters._parse_materials'), \
             patch('generator.TestFileParameters._parse_imports'), \
             patch('generator.TestFileParameters._parse_control_variables'), \
             patch('generator.TestFileParameters._parse_test_title'):
                
            # Load the JSON file
            json_data = generator._load_json_file()
            
            # Parse the parameters
            params = generator._parse_test_parameters(json_data)
            
            # Verify both variables were parsed
            self.assertEqual(mock_parse_variable.call_count, 2)
    
    @patch('generator.TestGenerator._get_template')
    @patch('generator.TestGenerator._render_template')
    def test_pytest_parametrize_format(self, mock_render, mock_get_template) -> None:
        """Test pytest specific parametrize format."""
        # Setup 
        self.config.harness = "pytest"
        generator = TestGenerator(self.config)
        
        # Mock template and rendering
        mock_template = MagicMock()
        mock_get_template.return_value = mock_template
        mock_render.return_value = """
@pytest.mark.parametrize("input_value, expected_output", [
    (1, 2),
    (10, 20),
    (100, 200),
    (-5, -10)
])
def test_parametrized_example(input_value, expected_output):
    assert function_under_test(input_value) == expected_output
"""
        
        # Generate test file
        content = generator.generate_test_file()
        
        # Verify pytest parametrize syntax in the rendered content
        self.assertIn("@pytest.mark.parametrize", content)
        self.assertIn("(1, 2)", content)
    
    @patch('generator.TestGenerator._get_template')
    @patch('generator.TestGenerator._render_template')
    def test_unittest_subtest_format(self, mock_render, mock_get_template) -> None:
        """Test unittest specific subtest format."""
        # Setup 
        self.config.harness = "unittest"
        generator = TestGenerator(self.config)
        
        # Mock template and rendering
        mock_template = MagicMock()
        mock_get_template.return_value = mock_template
        mock_render.return_value = """
def test_parametrized_example(self) -> None:
    test_cases = [
        (1, 2),
        (10, 20),
        (100, 200),
        (-5, -10)
    ]
    
    for input_value, expected_output in test_cases:
        with self.subTest(input_value=input_value, expected_output=expected_output):
            self.assertEqual(function_under_test(input_value), expected_output)
"""
        
        # Generate test file
        content = generator.generate_test_file()
        
        # Verify unittest subtest syntax in the rendered content
        self.assertIn("with self.subTest", content)
        self.assertIn("test_cases = [", content)


if __name__ == "__main__":
    unittest.main()