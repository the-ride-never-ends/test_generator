#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for utility functions.
"""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest


from utils.common.convert_to_snake_case import convert_to_snake_case
from utils.common.convert_to_pascal_case import convert_to_pascal_case
from utils.common.load_json_file import load_json_file


# Adjust the import path to properly import util modules
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestConvertToSnakeCase(unittest.TestCase):
    """Test case for convert_to_snake_case function."""

    def test_convert_space_separated(self) -> None:
        """Test converting space-separated words."""
        result = convert_to_snake_case("Hello World")
        self.assertEqual(result, "hello_world")

    def test_convert_already_snake_case(self) -> None:
        """Test converting already snake_case string."""
        result = convert_to_snake_case("hello_world")
        self.assertEqual(result, "hello_world")

    def test_convert_multiple_spaces(self) -> None:
        """Test converting string with multiple spaces."""
        result = convert_to_snake_case("Hello  World  Test")
        self.assertEqual(result, "hello__world__test")

    def test_convert_single_word(self) -> None:
        """Test converting single word."""
        result = convert_to_snake_case("Hello")
        self.assertEqual(result, "hello")


class TestConvertToPascalCase(unittest.TestCase):
    """Test case for convert_to_pascal_case function."""

    def test_convert_space_separated(self) -> None:
        """Test converting space-separated words."""
        result = convert_to_pascal_case("hello world")
        self.assertEqual(result, "HelloWorld")

    def test_convert_snake_case(self) -> None:
        """Test converting snake_case string."""
        result = convert_to_pascal_case("hello_world")
        self.assertEqual(result, "HelloWorld")

    def test_convert_kebab_case(self) -> None:
        """Test converting kebab-case string."""
        result = convert_to_pascal_case("hello-world")
        self.assertEqual(result, "HelloWorld")

    def test_convert_mixed_case(self) -> None:
        """Test converting mixed case string."""
        result = convert_to_pascal_case("hello_World-test")
        self.assertEqual(result, "HelloWorldTest")

    def test_convert_already_pascal_case(self) -> None:
        """Test converting already PascalCase string."""
        result = convert_to_pascal_case("HelloWorld")
        self.assertEqual(result, "HelloWorld")

    def test_convert_single_word(self) -> None:
        """Test converting single word."""
        result = convert_to_pascal_case("hello")
        self.assertEqual(result, "Hello")


class TestLoadJsonFile(unittest.TestCase):
    """Test case for load_json_file function."""

    def setUp(self) -> None:
        """Set up test environment."""
        # Create a temporary JSON file
        self.temp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        sample_data = {"test": "data", "number": 42, "list": [1, 2, 3]}
        self.temp_json.write(json.dumps(sample_data).encode('utf-8'))
        self.temp_json.close()

    def tearDown(self) -> None:
        """Clean up temporary files."""
        os.unlink(self.temp_json.name)

    def test_load_valid_json(self) -> None:
        """Test loading valid JSON file."""
        result = load_json_file(self.temp_json.name)
        self.assertEqual(result["test"], "data")
        self.assertEqual(result["number"], 42)
        self.assertEqual(result["list"], [1, 2, 3])

    def test_load_nonexistent_file(self) -> None:
        """Test loading non-existent file."""
        with self.assertRaises(FileNotFoundError):
            load_json_file("/path/to/nonexistent/file.json")

    def test_load_invalid_json(self) -> None:
        """Test loading invalid JSON file."""
        # Create temporary file with invalid JSON
        temp_invalid = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        temp_invalid.write(b'{"test": "data", invalid json}')
        temp_invalid.close()

        try:
            with self.assertRaises(json.JSONDecodeError):
                load_json_file(temp_invalid.name)
        finally:
            os.unlink(temp_invalid.name)


if __name__ == "__main__":
    unittest.main()
