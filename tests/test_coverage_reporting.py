#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for running test coverage reports.
"""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

# Add the parent directory to sys.path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestCoverageReporting(unittest.TestCase):
    """Test coverage reporting using the coverage tool."""
    
    def setUp(self) -> None:
        """Set up test environment."""
        self.test_dir = Path("tests")
        self.project_root = Path(__file__).parent.parent
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".coverage")
        self.temp_file.close()
        self.coverage_file = Path(self.temp_file.name)
    
    def tearDown(self) -> None:
        """Clean up test environment."""
        try:
            if Path(self.coverage_file.name).exists():
                os.unlink(self.coverage_file.name)
        except (FileNotFoundError, OSError):
            # The file might have been deleted already or never created
            pass
    
    def test_coverage_run(self) -> None:
        """Test running coverage on the project."""
        # Skip if coverage is not installed
        try:
            import coverage
        except ImportError:
            self.skipTest("coverage package not installed")
        
        # Run coverage on a single test file to verify it works
        cmd = [
            sys.executable, "-m", "coverage", "run", 
            "--data-file", str(self.coverage_file),
            "-m", "unittest", "tests.test_cli"
        ]
        
        result = subprocess.run(
            cmd, 
            cwd=self.project_root,
            capture_output=True,
            text=True
        )
        
        # Check that the command succeeded
        self.assertEqual(result.returncode, 0, f"Coverage run failed with output: {result.stderr}")
        
        # Check that the coverage file was created
        self.assertTrue(self.coverage_file.exists(), "Coverage file was not created")
    
    def test_coverage_report(self) -> None:
        """Test generating a coverage report."""
        # Skip if coverage is not installed
        try:
            import coverage
        except ImportError:
            self.skipTest("coverage package not installed")
        
        # First, run coverage to generate data
        run_cmd = [
            sys.executable, "-m", "coverage", "run", 
            "--data-file", str(self.coverage_file),
            "-m", "unittest", "tests.test_cli"
        ]
        
        run_result = subprocess.run(
            run_cmd, 
            cwd=self.project_root,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(run_result.returncode, 0, "Coverage run failed")
        
        # Now, generate a report
        report_cmd = [
            sys.executable, "-m", "coverage", "report",
            "--data-file", str(self.coverage_file),
        ]
        
        report_result = subprocess.run(
            report_cmd, 
            cwd=self.project_root,
            capture_output=True,
            text=True
        )
        
        # Check that the report generation succeeded
        self.assertEqual(report_result.returncode, 0, "Coverage report failed")
        
        # Check that the report contains expected content
        self.assertIn("Name", report_result.stdout)
        self.assertIn("Stmts", report_result.stdout)
        self.assertIn("Miss", report_result.stdout)
        self.assertIn("Cover", report_result.stdout)
        self.assertIn("cli.py", report_result.stdout)
    
    def test_coverage_html_report(self) -> None:
        """Test generating an HTML coverage report."""
        # Skip if coverage is not installed
        try:
            import coverage
        except ImportError:
            self.skipTest("coverage package not installed")
        
        # First, run coverage to generate data
        run_cmd = [
            sys.executable, "-m", "coverage", "run", 
            "--data-file", str(self.coverage_file),
            "-m", "unittest", "tests.test_cli"
        ]
        
        run_result = subprocess.run(
            run_cmd, 
            cwd=self.project_root,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(run_result.returncode, 0, "Coverage run failed")
        
        # Create a temporary directory for the HTML report
        with tempfile.TemporaryDirectory() as temp_dir:
            html_dir = Path(temp_dir)
            
            # Generate an HTML report
            html_cmd = [
                sys.executable, "-m", "coverage", "html",
                "--data-file", str(self.coverage_file),
                "-d", str(html_dir)
            ]
            
            html_result = subprocess.run(
                html_cmd, 
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            # Check that the HTML report generation succeeded
            self.assertEqual(html_result.returncode, 0, "HTML coverage report failed")
            
            # Check that the HTML report files were created
            self.assertTrue((html_dir / "index.html").exists(), "HTML index file was not created")
            self.assertTrue((html_dir / "status.json").exists(), "Status JSON file was not created")


if __name__ == "__main__":
    unittest.main()