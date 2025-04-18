#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the fix_whitespace script.
"""
import os
import tempfile
import unittest
from pathlib import Path

# Add the parent directory to sys.path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.for_tests.fix_whitespace import (
    clean_whitespace_in_blank_lines,
    fix_trailing_whitespace,
    ensure_newline_at_end_of_file,
    find_files,
    fix_files
)


class TestFixWhitespace(unittest.TestCase):
    """Test case for the fix_whitespace script."""

    def setUp(self) -> None:
        """Set up the test environment."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        """Clean up the test environment."""
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def test_clean_whitespace_in_blank_lines(self) -> None:
        """Test cleaning whitespace in blank lines."""
        # Create a test file with blank lines containing whitespace
        test_file = self.test_dir / "blank_lines.txt"
        with open(test_file, 'w') as f:
            f.write("Line 1\n")
            f.write("    \n")  # Blank line with whitespace
            f.write("Line 3\n")
            f.write("  \t  \n")  # Blank line with mixed whitespace
            f.write("Line 5\n")

        # Fix blank lines
        fixed_count = clean_whitespace_in_blank_lines(str(test_file))

        # Check results
        self.assertEqual(fixed_count, 2, "Should have fixed 2 blank lines")

        # Verify file contents
        with open(test_file, 'r') as f:
            lines = f.readlines()

        self.assertEqual(lines, ["Line 1\n", "\n", "Line 3\n", "\n", "Line 5\n"])

    def test_fix_trailing_whitespace(self) -> None:
        """Test fixing trailing whitespace."""
        # Create a test file with trailing whitespace
        test_file = self.test_dir / "trailing.txt"
        with open(test_file, 'w') as f:
            f.write("Line 1\n")
            f.write("Line 2  \n")  # Trailing whitespace
            f.write("Line 3\t\n")  # Trailing tab
            f.write("Line 4  \t  \n")  # Mixed trailing whitespace
            f.write("Line 5")  # No newline

        # Fix trailing whitespace
        fixed_count = fix_trailing_whitespace(str(test_file))

        # Check results
        self.assertEqual(fixed_count, 3, "Should have fixed 3 lines with trailing whitespace")

        # Verify file contents
        with open(test_file, 'r') as f:
            lines = f.readlines()

        self.assertEqual(lines, ["Line 1\n", "Line 2\n", "Line 3\n", "Line 4\n", "Line 5"])

    def test_ensure_newline_at_end_of_file(self) -> None:
        """Test ensuring file ends with a newline."""
        # Create a test file without a final newline
        test_file = self.test_dir / "no_newline.txt"
        with open(test_file, 'w') as f:
            f.write("Line 1\n")
            f.write("Line 2")  # No final newline

        # Fix final newline
        fixed = ensure_newline_at_end_of_file(str(test_file))

        # Check results
        self.assertEqual(fixed, 1, "Should have fixed the missing newline")

        # Verify file contents
        with open(test_file, 'r') as f:
            content = f.read()

        self.assertTrue(content.endswith("\n"), "File should end with a newline")
        self.assertEqual(content, "Line 1\nLine 2\n")

        # Check that running again doesn't change anything
        fixed = ensure_newline_at_end_of_file(str(test_file))
        self.assertEqual(fixed, 0, "Should not fix anything if newline already exists")

    def test_find_files(self) -> None:
        """Test finding files matching patterns."""
        # Create various test files
        (self.test_dir / "file1.py").touch()
        (self.test_dir / "file2.py").touch()
        (self.test_dir / "file.txt").touch()

        # Create a subdirectory
        subdir = self.test_dir / "subdir"
        subdir.mkdir()
        (subdir / "subfile.py").touch()

        # Create an excluded directory
        exclude_dir = self.test_dir / "exclude"
        exclude_dir.mkdir()
        (exclude_dir / "excluded.py").touch()

        # Find all Python files
        files = find_files([str(self.test_dir / "**/*.py")], [str(exclude_dir)])

        # Normalize paths for comparison
        normalized_files = [os.path.normpath(f) for f in files]

        # Expected files (using normalized paths)
        expected = [
            os.path.normpath(str(self.test_dir / "file1.py")),
            os.path.normpath(str(self.test_dir / "file2.py")),
            os.path.normpath(str(subdir / "subfile.py"))
        ]

        # Check results
        self.assertEqual(sorted(normalized_files), sorted(expected),
                         "Should find all Python files except in excluded directories")

    def test_fix_files(self) -> None:
        """Test fixing multiple files at once."""
        # Create test files with various issues
        file1 = self.test_dir / "file1.py"
        with open(file1, 'w') as f:
            f.write("Line 1\n")
            f.write("    \n")  # Blank line with whitespace
            f.write("Line 3  \n")  # Trailing whitespace

        file2 = self.test_dir / "file2.py"
        with open(file2, 'w') as f:
            f.write("Line 1\n")
            f.write("Line 2")  # No final newline

        file3 = self.test_dir / "file3.py"
        with open(file3, 'w') as f:
            f.write("This file is fine\n")

        # Fix all files
        files_fixed, blank_fixes, trailing_fixes, newline_fixes = fix_files(
            [str(file1), str(file2), str(file3)],
            fix_blank=True,
            fix_trailing=True,
            fix_newlines=True,
            verbose=False
        )

        # Check results
        self.assertEqual(files_fixed, 2, "Should have fixed 2 files")
        self.assertEqual(blank_fixes, 1, "Should have fixed 1 blank line")
        self.assertEqual(trailing_fixes, 1, "Should have fixed 1 trailing whitespace")
        self.assertEqual(newline_fixes, 1, "Should have fixed 1 missing newline")

        # Verify file contents
        with open(file1, 'r') as f:
            content1 = f.read()
        self.assertEqual(content1, "Line 1\n\nLine 3\n", "File 1 should be fixed correctly")

        with open(file2, 'r') as f:
            content2 = f.read()
        self.assertEqual(content2, "Line 1\nLine 2\n", "File 2 should be fixed correctly")

        with open(file3, 'r') as f:
            content3 = f.read()
        self.assertEqual(content3, "This file is fine\n", "File 3 should remain unchanged")


if __name__ == "__main__":
    unittest.main()
