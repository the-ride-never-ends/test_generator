#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the Generator module.
"""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock


# Adjust the import path to properly import the generator module
sys.path.insert(0, str(Path(__file__).parent.parent))



from configs import Configs
from generator import TestGenerator, TestFileParameters
from schemas.statistical_type import StatisticalType
from schemas.variable import Variable




class TestTestFileParameters(unittest.TestCase):
    """Test case for the TestFileParameters class."""

    @patch('generator.TestFileParameters._parse_variable')
    @patch('generator.TestFileParameters._parse_test_method')
    @patch('generator.TestFileParameters._parse_materials')
    @patch('generator.TestFileParameters._parse_imports')
    @patch('generator.TestFileParameters._parse_control_variables')
    def test_parse_test_title_string(self, mock_control_vars, mock_imports, mock_materials, mock_test_method, mock_parse_variable) -> None:
        """Test parsing test title from string."""
        # Mock the methods to avoid validation errors
        mock_parse_variable.return_value = None
        mock_test_method.return_value = None
        mock_materials.return_value = []
        mock_imports.return_value = []
        mock_control_vars.return_value = []

        json_data = {
            "test_file_parameters": {
                "test_title": "Test Title"
            }
        }

        params = TestFileParameters(json_data)
        self.assertEqual(params.test_title, "Test Title")

    @patch('generator.TestFileParameters._parse_variable')
    @patch('generator.TestFileParameters._parse_test_method')
    @patch('generator.TestFileParameters._parse_materials')
    @patch('generator.TestFileParameters._parse_imports')
    @patch('generator.TestFileParameters._parse_control_variables')
    def test_parse_test_title_dict(self, mock_control_vars, mock_imports, mock_materials, mock_test_method, mock_parse_variable) -> None:
        """Test parsing test title from dictionary."""
        # Mock the methods to avoid validation errors
        mock_parse_variable.return_value = None
        mock_test_method.return_value = None
        mock_materials.return_value = []
        mock_imports.return_value = []
        mock_control_vars.return_value = []

        json_data = {
            "test_file_parameters": {
                "test_title": {"test_title": "Test Title"}
            }
        }

        params = TestFileParameters(json_data)
        self.assertEqual(params.test_title, "TestTitle")

    @patch('generator.TestFileParameters._parse_variable')
    @patch('generator.TestFileParameters._parse_test_method')
    @patch('generator.TestFileParameters._parse_materials')
    @patch('generator.TestFileParameters._parse_imports')
    @patch('generator.TestFileParameters._parse_control_variables')
    def test_parse_background(self, mock_control_vars, mock_imports, mock_materials, mock_test_method, mock_parse_variable) -> None:
        """Test parsing background information."""
        # Mock the methods to avoid validation errors
        mock_parse_variable.return_value = None
        mock_test_method.return_value = None
        mock_materials.return_value = []
        mock_imports.return_value = []
        mock_control_vars.return_value = []

        json_data = {
            "test_file_parameters": {
                "background": {
                    "orientation": "Test orientation",
                    "purpose": "Test purpose",
                    "hypothesis": "Test hypothesis",
                    "citation_path": "path/to/citation",
                    "citation": "Test citation"
                }
            }
        }

        params = TestFileParameters(json_data)
        self.assertEqual(params.background["orientation"], "Test orientation")
        self.assertEqual(params.background["purpose"], "Test purpose")
        self.assertEqual(params.background["hypothesis"], "Test hypothesis")

    def test_parse_empty_json(self) -> None:
        """Test handling of empty JSON data."""
        json_data = {}

        with self.assertRaises(ValueError):
            TestFileParameters(json_data)


class TestTestGenerator(unittest.TestCase):
    """Test case for the TestGenerator class."""

    def setUp(self) -> None:
        """Set up test environment."""
        # Create a temporary JSON file
        self.temp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        sample_data = {
            "test_file_parameters": {
                "test_title": "Test Title",
                "background": {
                    "orientation": "Test orientation",
                    "purpose": "Test purpose",
                    "hypothesis": "Test hypothesis",
                    "citation_path": "path/to/citation",
                    "citation": "Test citation"
                },
                "independent_variable": {
                    "name": "Independent Var",
                    "description": "Test independent var",
                    "statistical_type": "DISCRETE",
                    "unit": "units",
                    "value": 10
                },
                "dependent_variable": {
                    "name": "Dependent Var",
                    "description": "Test dependent var",
                    "statistical_type": "CONTINUOUS",
                    "expected_value": {
                        "value": 100.0
                    }
                },
                "control_variables": [],
                "test_procedure": {
                    "steps": ["Step 1", "Step 2"],
                    "data_collection": "Test data collection",
                    "analysis_technique": "Test analysis"
                },
                "imports": [
                    {"name": "unittest"}
                ]
            }
        }
        self.temp_json.write(json.dumps(sample_data).encode('utf-8'))
        self.temp_json.close()

        # Create a temporary output directory
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create config
        self.config = Configs.model_validate({
            "name": "Test Name",
            "description": "Test Description",
            "json_file_path": self.temp_json.name,
            "output_dir": self.temp_dir.name,
            "harness": "unittest"
        })

        # Create generator
        self.generator = TestGenerator(self.config)

    def tearDown(self) -> None:
        """Clean up temporary files."""
        os.unlink(self.temp_json.name)
        self.temp_dir.cleanup()

    def test_load_json_file(self) -> None:
        """Test loading JSON file."""
        json_data = self.generator._load_json_file()
        self.assertIn("test_file_parameters", json_data)
        self.assertEqual(json_data["test_file_parameters"]["test_title"], "Test Title")

    @patch('generator.Variable')
    @patch('generator.TestFileParameters._parse_variable')
    def test_parse_test_parameters(self, mock_parse_variable, mock_variable):
        """Test parsing test parameters."""
        # Mock the Variable class and _parse_variable method to avoid validation errors
        mock_variable_obj = MagicMock()
        mock_variable_obj.name = "Dependent Var"
        mock_parse_variable.side_effect = lambda var_type: mock_variable_obj if var_type == "dependent_variable" else Variable(**{
            "name": "Independent Var",
            "description": "Test independent var",
            "statistical_type": StatisticalType.DISCRETE,
            "unit": "units",
            "value": 10
        })

        json_data = self.generator._load_json_file()
        params = self.generator._parse_test_parameters(json_data)

        self.assertEqual(params.test_title, "Test Title")
        self.assertEqual(params.background["orientation"], "Test orientation")
        self.assertEqual(params.dependent_variable.name, "Dependent Var")

    def test_get_template_unittest(self) -> None:
        """Test getting unittest template."""
        self.config.harness = "unittest"
        template = self.generator._get_template()
        self.assertIsNotNone(template)

        # If using inline template, should be a string
        if isinstance(template, str):
            self.assertIn("unittest", template)

    def test_get_template_pytest(self) -> None:
        """Test getting pytest template."""
        self.config.harness = "pytest"
        template = self.generator._get_template()
        self.assertIsNotNone(template)

        # If using inline template, should be a string
        if isinstance(template, str):
            self.assertIn("pytest", template)

    def test_get_template_invalid(self) -> None:
        """Test getting template for invalid harness."""
        self.config.harness = "invalid"
        with self.assertRaises(ValueError):
            self.generator._get_template()

    @patch('generator.TestGenerator._get_template')
    @patch('generator.TestFileParameters')
    def test_render_template(self, mock_test_file_params, mock_get_template) -> None:
        """Test rendering template."""
        # Mock template
        mock_template = MagicMock()
        mock_template.render.return_value = "Rendered template"
        mock_get_template.return_value = mock_template

        # Create mock test parameters with all the required attributes
        mock_params = MagicMock()
        mock_params.test_title = "Test Title"
        mock_params.background = {"orientation": "Test orientation"}
        mock_params.independent_variable = MagicMock()
        mock_params.dependent_variable = MagicMock()
        mock_params.control_variables = []
        mock_params.materials = []
        mock_params.test_method = MagicMock()
        mock_params.imports = []

        # Set the mock parameters
        self.generator.test_file_params = mock_params

        # Render template
        result = self.generator._render_template(mock_template)
        self.assertEqual(result, "Rendered template")
        mock_template.render.assert_called_once()

    @patch('generator.TestGenerator._load_json_file')
    @patch('generator.TestGenerator._parse_test_parameters')
    @patch('generator.TestGenerator._get_template')
    @patch('generator.TestGenerator._render_template')
    def test_generate_test_file(self, mock_render, mock_get_template, mock_parse, mock_load) -> None:
        """Test generating test file."""
        # Set up mocks
        mock_load.return_value = {"test_file_parameters": {}}
        mock_params = MagicMock()
        mock_parse.return_value = mock_params
        mock_template = MagicMock()
        mock_get_template.return_value = mock_template
        mock_render.return_value = "Generated test content"

        # Generate file
        result = self.generator.generate_test_file()

        # Should be the mocked rendered content
        self.assertEqual(result, "Generated test content")

        # Verify all methods were called
        mock_load.assert_called_once()
        mock_parse.assert_called_once()
        mock_get_template.assert_called_once()
        mock_render.assert_called_once_with(mock_template)

    def test_write_test_file(self) -> None:
        """Test writing test file to disk."""
        # Generate content
        content = "Test file content"

        # Write to file
        file_path = self.generator.write_test_file(content)

        # Should return a Path object
        self.assertIsInstance(file_path, Path)

        # File should exist
        self.assertTrue(file_path.exists())

        # File should contain the content
        with open(file_path, 'r') as f:
            read_content = f.read()
            self.assertEqual(read_content, content)


if __name__ == "__main__":
    unittest.main()
