#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Integration tests for the Test Generator.
"""
import json
import os
import tempfile
import unittest
from pathlib import Path

# Adjust the import path to properly import modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from cli import CLI


class TestIntegration(unittest.TestCase):
    """Integration tests for Test Generator."""

    def setUp(self) -> None:
        """Set up test environment."""
        # Create a temporary JSON file with test parameters
        self.temp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        sample_data = {
            "test_file_parameters": {
                "test_title": "Integration Test",
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
                    "unit": "milliseconds",
                    "expected_value": {
                        "value": 100.0,
                        "validation_procedures": [
                            {
                                "name": "equals",
                                "description": "Check if the value equals expected",
                                "kwargs": {}
                            }
                        ]
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

    def tearDown(self) -> None:
        """Clean up temporary files."""
        os.unlink(self.temp_json.name)
        self.temp_dir.cleanup()

    def test_end_to_end_unittest(self) -> None:
        """Test end-to-end process with unittest framework."""
        # Create command-line arguments
        args = [
            "--name", "IntegrationTest",
            "--description", "Integration test for Test Generator",
            "--test_parameter_json", self.temp_json.name,
            "--output_dir", self.temp_dir.name,
            "--harness", "unittest"
        ]

        # Run CLI
        cli = CLI()
        args_dict = cli.parse_args(args)
        self.assertTrue(cli.validate_config(args_dict))
        exit_code = cli.run()

        # Should exit with success
        self.assertEqual(exit_code, 0)

        # Output file should exist
        output_file = Path(self.temp_dir.name) / "test_integrationtest.py"
        self.assertTrue(output_file.exists())

        # Check file contents
        with open(output_file, 'r') as f:
            content = f.read()

            # Should contain key elements
            self.assertIn("class TestIntegrationTest(unittest.TestCase):", content)
            self.assertIn("def test_integrationtest", content)
            self.assertIn("Test orientation", content)
            self.assertIn("Test hypothesis", content)
            self.assertIn("Independent Var", content)
            self.assertIn("Dependent Var", content)
            self.assertIn("Step 1", content)
            self.assertIn("Step 2", content)

    def test_end_to_end_pytest(self) -> None:
        """Test end-to-end process with pytest framework."""
        # Create command-line arguments
        args = [
            "--name", "IntegrationTest",
            "--description", "Integration test for Test Generator",
            "--test_parameter_json", self.temp_json.name,
            "--output_dir", self.temp_dir.name,
            "--harness", "pytest"
        ]

        # Run CLI
        cli = CLI()
        args_dict = cli.parse_args(args)
        self.assertTrue(cli.validate_config(args_dict))
        exit_code = cli.run()

        # Should exit with success
        self.assertEqual(exit_code, 0)

        # Output file should exist
        output_file = Path(self.temp_dir.name) / "test_integrationtest.py"
        self.assertTrue(output_file.exists())

        # Check file contents
        with open(output_file, 'r') as f:
            content = f.read()

            # Should contain key elements for pytest
            self.assertIn("import pytest", content)
            self.assertIn("def test_integrationtest", content)
            self.assertIn("Test orientation", content)
            self.assertIn("Test hypothesis", content)
            self.assertIn("Independent Var", content)
            self.assertIn("Dependent Var", content)
            self.assertIn("Step 1", content)
            self.assertIn("Step 2", content)


if __name__ == "__main__":
    unittest.main()
