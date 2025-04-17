#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the Configs model.
"""
import os
import tempfile
import unittest
from pathlib import Path

from pydantic import ValidationError

# Adjust the import path to properly import the configs module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from configs import Configs


class TestConfigs(unittest.TestCase):
    """Test case for the Configs model."""
    
    def setUp(self) -> None:
        """Set up temporary files for testing."""
        # Create a temporary file to use as a valid file path
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b'{"test": "data"}')
        self.temp_file.close()
        
        # Create a temporary directory to use as a valid directory path
        self.temp_dir = tempfile.TemporaryDirectory()
        
    def tearDown(self) -> None:
        """Clean up temporary files."""
        # Remove temporary file and directory
        os.unlink(self.temp_file.name)
        self.temp_dir.cleanup()
    
    def test_valid_config(self) -> None:
        """Test that valid configuration passes validation."""
        config_data = {
            "name": "Test Name",
            "description": "Test Description",
            "json_file_path": self.temp_file.name,
            "output_dir": self.temp_dir.name,
            "verbose": True,
            "harness": "unittest",
            "has_fixtures": False,
            "docstring_style": "google"
        }
        
        # This should not raise an exception
        config = Configs.model_validate(config_data)
        
        # Check values
        self.assertEqual(config.name, "Test Name")
        self.assertEqual(config.description, "Test Description")
        self.assertEqual(config.harness, "unittest")
        self.assertEqual(config.verbose, True)
        self.assertEqual(config.has_fixtures, False)
        self.assertEqual(config.docstring_style, "google")
    
    def test_invalid_harness(self) -> None:
        """Test that invalid harness raises ValidationError."""
        config_data = {
            "name": "Test Name",
            "description": "Test Description",
            "json_file_path": self.temp_file.name,
            "output_dir": self.temp_dir.name,
            "harness": "invalid-harness"  # Invalid harness
        }
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError):
            Configs.model_validate(config_data)
    
    def test_missing_required_fields(self) -> None:
        """Test that missing required fields raise ValidationError."""
        config_data = {
            # Missing name and description
            "json_file_path": self.temp_file.name,
            "output_dir": self.temp_dir.name
        }
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError):
            Configs.model_validate(config_data)
    
    def test_invalid_file_path(self) -> None:
        """Test that non-existent file path raises ValidationError."""
        config_data = {
            "name": "Test Name",
            "description": "Test Description",
            "json_file_path": "/path/to/nonexistent/file.json",
            "output_dir": self.temp_dir.name
        }
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError):
            Configs.model_validate(config_data)
    
    def test_default_values(self) -> None:
        """Test that default values are set correctly."""
        config_data = {
            "name": "Test Name",
            "description": "Test Description",
            "json_file_path": self.temp_file.name,
            # output_dir not provided, should use default
            # verbose not provided, should use default
            # harness not provided, should use default
        }
        
        config = Configs.model_validate(config_data)
        
        # Check default values
        self.assertEqual(str(config.output_dir), str(Path("tests")))
        self.assertEqual(config.verbose, True)
        self.assertEqual(config.harness, "unittest")
        self.assertEqual(config.has_fixtures, False)
        self.assertEqual(config.docstring_style, "google")


if __name__ == "__main__":
    unittest.main()