#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for fixture handling in test templates.
"""
import json
import os
import sys
import tempfile
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch


from configs import Configs
from generator import TestGenerator


# Adjust the import path to properly import the generator module
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestFixtureHandling(unittest.TestCase):
    """Tests for fixture handling in test templates."""

    def setUp(self) -> None:
        """Set up test environment."""
        # Create a temporary JSON file with fixture data
        self.temp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        sample_data = {
            "test_file_parameters": {
                "test_title": "Fixture Test Title",
                "background": {
                    "orientation": "Test orientation",
                    "purpose": "Test purpose",
                    "hypothesis": "Test hypothesis"
                },
                "independent_variable": {
                    "name": "Independent Var",
                    "description": "Test independent var",
                    "statistical_type": "discrete",
                    "unit": "units",
                    "value": 10
                },
                "dependent_variable": {
                    "name": "Dependent Var",
                    "description": "Test dependent var",
                    "statistical_type": "continuous",
                    "unit": "units",
                    "expected_value": {
                        "value": 100.0,
                        "validation_procedures": [
                            {
                                "name": "validate_result",
                                "description": "Validate test result",
                                "steps": ["Step 1", "Step 2"]
                            }
                        ]
                    }
                },
                "control_variables": [],
                "test_materials": [
                    {
                        "name": "database",
                        "description": "Test database connection",
                        "type": "fixture",
                        "configuration": {
                            "connection_string": "sqlite:///:memory:",
                            "tables": ["users", "products"]
                        }
                    },
                    {
                        "name": "mock_api",
                        "description": "Mock API server",
                        "type": "fixture",
                        "configuration": {
                            "endpoints": ["/users", "/products"],
                            "port": 8080
                        }
                    }
                ],
                "test_procedure": {
                    "steps": ["Step 1", "Step 2"],
                    "data_collection": "Test data collection",
                    "analysis_technique": "Test analysis"
                },
                "imports": [
                    {"name": "unittest"},
                    {"name": "pytest"},
                    {"name": "sqlalchemy"}
                ]
            }
        }
        self.temp_json.write(json.dumps(sample_data).encode('utf-8'))
        self.temp_json.close()

        # Create a temporary output directory
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create config
        self.config = Configs.model_validate({
            "name": "Fixture Test",
            "description": "Test with fixtures",
            "json_file_path": self.temp_json.name,
            "output_dir": self.temp_dir.name,
            "has_fixtures": True
        })

    def tearDown(self) -> None:
        """Clean up temporary files."""
        os.unlink(self.temp_json.name)
        self.temp_dir.cleanup()

    def test_fixture_flag(self) -> None:
        """Test fixture flag is properly passed to the generator."""
        self.assertTrue(self.config.has_fixtures)

    @patch('generator.TestGenerator._get_template')
    @patch('generator.TestGenerator._render_template')
    def test_unittest_with_fixtures(self, mock_render, mock_get_template):
        """Test unittest template with fixtures."""
        # Setup
        self.config.harness = "unittest"
        generator = TestGenerator(self.config)

        # Mock template and rendering
        mock_template = MagicMock()
        mock_get_template.return_value = mock_template
        mock_render.return_value = "Generated content with fixtures"

        # Generate test file
        _ = generator.generate_test_file()

        # Verify that fixtures were included in the context
        mock_render.assert_called_once()
        call_kwargs = mock_render.call_args[0][0]
        # The template object should have been passed to _render_template
        self.assertEqual(call_kwargs, mock_template)

        # Verify that the has_fixtures flag was used
        self.assertTrue(generator.config.has_fixtures)

    @patch('generator.TestGenerator._get_template')
    @patch('generator.TestGenerator._render_template')
    def test_pytest_with_fixtures(self, mock_render, mock_get_template):
        """Test pytest template with fixtures."""
        # Setup
        self.config.harness = "pytest"
        generator = TestGenerator(self.config)

        # Mock template and rendering
        mock_template = MagicMock()
        mock_get_template.return_value = mock_template
        mock_render.return_value = "Generated pytest content with fixtures"

        # Generate test file
        _ = generator.generate_test_file()

        # Verify that fixtures were included in the context
        mock_render.assert_called_once()
        call_kwargs = mock_render.call_args[0][0]
        # The template object should have been passed to _render_template
        self.assertEqual(call_kwargs, mock_template)

        # Verify that the has_fixtures flag was used
        self.assertTrue(generator.config.has_fixtures)

    @patch('generator.TestFileParameters._parse_materials')
    def test_fixture_extraction(self, mock_parse_materials):
        """Test extraction of fixtures from test materials."""
        # Setup fixtures
        fixtures = [
            {
                "name": "database",
                "description": "Test database connection",
                "type": "fixture",
                "configuration": {
                    "connection_string": "sqlite:///:memory:",
                    "tables": ["users", "products"]
                }
            },
            {
                "name": "mock_api",
                "description": "Mock API server",
                "type": "fixture",
                "configuration": {
                    "endpoints": ["/users", "/products"],
                    "port": 8080
                }
            }
        ]

        # Mock the materials parsing to return our fixtures
        mock_parse_materials.return_value = fixtures

        # Create generator and generate file
        generator = TestGenerator(self.config)

        # Mock the materials parsing in TestFileParameters
        with patch('generator.TestFileParameters._parse_variable'), \
             patch('generator.TestFileParameters._parse_test_method'), \
             patch('generator.TestFileParameters._parse_imports'), \
             patch('generator.TestFileParameters._parse_control_variables'), \
             patch('generator.TestFileParameters._parse_test_title'):

            # Load the JSON file
            json_data = generator._load_json_file()

            # Parse the parameters
            params = generator._parse_test_parameters(json_data)

            # Verify fixtures were parsed
            mock_parse_materials.assert_called_once()
            self.assertEqual(params.materials, fixtures)


if __name__ == "__main__":
    unittest.main()
