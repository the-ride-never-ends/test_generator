#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the CLI module.
"""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Adjust the import path to properly import the cli module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from cli import CLI


class TestCLI(unittest.TestCase):
    """Test case for the CLI module."""
    
    def setUp(self):
        """Set up temporary files for testing."""
        # Create a temporary file to use as a valid file path
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b'{"test": "data"}')
        self.temp_file.close()
        
        # Create a temporary directory to use as a valid directory path
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Initialize CLI
        self.cli = CLI()
    
    def tearDown(self):
        """Clean up temporary files."""
        # Remove temporary file and directory
        os.unlink(self.temp_file.name)
        self.temp_dir.cleanup()
    
    def test_parser_creation(self):
        """Test that the argument parser is created correctly."""
        parser = self.cli._create_parser()
        
        # Check that parser has expected arguments
        args = parser.parse_args([
            "--name", "Test Name",
            "--description", "Test Description",
            "--test_parameter_json", self.temp_file.name
        ])
        
        self.assertEqual(args.name, "Test Name")
        self.assertEqual(args.description, "Test Description")
        self.assertEqual(args.test_parameter_json, self.temp_file.name)
    
    def test_parse_args(self):
        """Test parsing of command-line arguments."""
        args = [
            "--name", "Test Name",
            "--description", "Test Description",
            "--test_parameter_json", self.temp_file.name,
            "--output_dir", self.temp_dir.name,
            "--verbose"
        ]
        
        args_dict = self.cli.parse_args(args)
        
        # Check that args are parsed correctly
        self.assertEqual(args_dict["name"], "Test Name")
        self.assertEqual(args_dict["description"], "Test Description")
        self.assertEqual(args_dict["test_parameter_json"], self.temp_file.name)
        self.assertEqual(args_dict["output_dir"], self.temp_dir.name)
        self.assertTrue(args_dict["verbose"])
    
    def test_validate_config_valid(self):
        """Test validation of valid configuration."""
        args_dict = {
            "name": "Test Name",
            "description": "Test Description",
            "test_parameter_json": self.temp_file.name,
            "output_dir": self.temp_dir.name,
            "verbose": True,
            "harness": "unittest"
        }
        
        # Should return True for valid config
        self.assertTrue(self.cli.validate_config(args_dict))
        
        # Config should be stored in the CLI instance
        self.assertIsNotNone(self.cli.config)
        self.assertEqual(self.cli.config.name, "Test Name")
        self.assertEqual(str(self.cli.config.json_file_path), self.temp_file.name)
    
    def test_validate_config_invalid(self):
        """Test validation of invalid configuration."""
        # Missing required fields
        args_dict = {
            "output_dir": self.temp_dir.name,
            "verbose": True
        }
        
        # Should return False for invalid config
        self.assertFalse(self.cli.validate_config(args_dict))
        
        # Config should not be stored
        self.assertIsNone(self.cli.config)
    
    @patch('cli.TestGenerator')
    def test_run_success(self, mock_generator):
        """Test successful run of the CLI."""
        # Mock generator instance
        mock_generator_instance = MagicMock()
        mock_generator_instance.generate_test_file.return_value = "test file content"
        mock_generator_instance.write_test_file.return_value = Path("/path/to/output.py")
        
        # Mock generator class to return the mocked instance
        mock_generator.return_value = mock_generator_instance
        
        # Set up CLI with config
        self.cli.config = MagicMock()
        self.cli.config.verbose = True
        
        # Should return 0 for success
        self.assertEqual(self.cli.run(), 0)
        
        # Check that generator was called with config
        mock_generator.assert_called_once_with(self.cli.config)
        mock_generator_instance.generate_test_file.assert_called_once()
        mock_generator_instance.write_test_file.assert_called_once_with("test file content")
    
    @patch('cli.TestGenerator')
    def test_run_failure(self, mock_generator):
        """Test handling of failures during run."""
        # Mock generator to raise an exception
        mock_generator_instance = MagicMock()
        mock_generator_instance.generate_test_file.side_effect = ValueError("Test error")
        mock_generator.return_value = mock_generator_instance
        
        # Set up CLI with config
        self.cli.config = MagicMock()
        self.cli.config.verbose = True
        
        # Should return 1 for failure
        self.assertEqual(self.cli.run(), 1)


if __name__ == "__main__":
    unittest.main()