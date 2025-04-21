#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the test coverage reporting system.
"""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


from utils.for_tests.run_tests import TestResultCollector, TestDiscoverer


# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestCoverageReporting(unittest.TestCase):
    """Test case for the test coverage reporting system."""

    def setUp(self) -> None:
        """Set up the test environment."""
        # Create a temp dir for test reports
        self.test_reports_dir = Path("./test_reports_temp")
        self.test_reports_dir.mkdir(exist_ok=True)

        # Mock test start time
        self.start_time = 1600000000.0  # A fixed timestamp for testing

        # Create a collector with our fixed start time
        self.collector = TestResultCollector(self.start_time)

    def tearDown(self) -> None:
        """Clean up the test environment."""
        # Remove any test files created
        for file in self.test_reports_dir.glob("*"):
            file.unlink()

        # Remove the temp directory
        if self.test_reports_dir.exists():
            self.test_reports_dir.rmdir()

    def test_collector_initialization(self) -> None:
        """Test that the test result collector initializes correctly."""
        # Check that the results structure is created correctly
        self.assertEqual(self.collector.results["summary"]["tests"], 0)
        self.assertEqual(self.collector.results["summary"]["errors"], 0)
        self.assertEqual(self.collector.results["summary"]["failures"], 0)
        self.assertEqual(self.collector.results["summary"]["skipped"], 0)
        self.assertEqual(self.collector.results["summary"]["success_rate"], 0.0)
        self.assertEqual(len(self.collector.results["test_cases"]), 0)

    def test_collect_results(self) -> None:
        """Test collecting results from a TestResult object."""
        # Create a mock TestResult
        mock_result = MagicMock()
        mock_result.testsRun = 10
        mock_result.errors = [(self._create_mock_test("test_error"), "Error traceback")]
        mock_result.failures = [(self._create_mock_test("test_failure"), "Failure traceback")]
        mock_result.skipped = [(self._create_mock_test("test_skipped"), "Skipped reason")]
        mock_result.expectedFailures = [(self._create_mock_test("test_expected_failure"), "Expected failure")]
        mock_result.unexpectedSuccesses = [self._create_mock_test("test_unexpected_success")]

        # Collect results
        self.collector.collect_results(mock_result)

        # Check summary
        self.assertEqual(self.collector.results["summary"]["tests"], 10)
        self.assertEqual(self.collector.results["summary"]["errors"], 1)
        self.assertEqual(self.collector.results["summary"]["failures"], 1)
        self.assertEqual(self.collector.results["summary"]["skipped"], 1)
        self.assertEqual(self.collector.results["summary"]["expected_failures"], 1)
        self.assertEqual(self.collector.results["summary"]["unexpected_successes"], 1)

        # Success rate should be (10 - 1 - 1) / 10 = 0.8 = 80%
        self.assertEqual(self.collector.results["summary"]["success_rate"], 80.0)

        # Check that we captured the right number of test cases
        self.assertEqual(len(self.collector.results["test_cases"]), 5)

        # Check specific test cases
        statuses = [test["status"] for test in self.collector.results["test_cases"]]
        self.assertIn("ERROR", statuses)
        self.assertIn("FAIL", statuses)
        self.assertIn("SKIPPED", statuses)
        self.assertIn("EXPECTED_FAILURE", statuses)
        self.assertIn("UNEXPECTED_SUCCESS", statuses)

    def test_generate_json_report(self) -> None:
        """Test generating a JSON report of test results."""
        # Create a mock TestResult
        mock_result = MagicMock()
        mock_result.testsRun = 5
        mock_result.errors = []
        mock_result.failures = []
        mock_result.skipped = []
        mock_result.expectedFailures = []
        mock_result.unexpectedSuccesses = []

        # Collect results
        self.collector.collect_results(mock_result)

        # Generate report
        json_path = self.test_reports_dir / "test_report.json"
        self.collector.generate_json_report(json_path)

        # Check that the file was created
        self.assertTrue(json_path.exists())

        # Check the contents
        with open(json_path, 'r') as f:
            report = json.load(f)

        self.assertEqual(report["summary"]["tests"], 5)
        self.assertEqual(report["summary"]["errors"], 0)
        self.assertEqual(report["summary"]["success_rate"], 100.0)

    def test_generate_markdown_report(self) -> None:
        """Test generating a Markdown report of test results."""
        # Create a mock TestResult
        mock_result = MagicMock()
        mock_result.testsRun = 5
        mock_result.errors = []
        mock_result.failures = []
        mock_result.skipped = []
        mock_result.expectedFailures = []
        mock_result.unexpectedSuccesses = []

        # Collect results
        self.collector.collect_results(mock_result)

        # Generate report
        md_path = self.test_reports_dir / "test_report.md"
        self.collector.generate_markdown_report(md_path)

        # Check that the file was created
        self.assertTrue(md_path.exists())

        # Check the contents
        with open(md_path, 'r') as f:
            content = f.read()

        self.assertIn("# Test Generator - Test Report", content)
        self.assertIn("- **Tests Run**: 5", content)
        self.assertIn("- **Success Rate**: 100.00%", content)

    def test_markdown_report_with_failures(self) -> None:
        """Test generating a Markdown report with failures."""
        # Create a mock TestResult
        mock_result = MagicMock()
        mock_result.testsRun = 5
        mock_result.errors = [(self._create_mock_test("test_error"), "Error traceback")]
        mock_result.failures = [(self._create_mock_test("test_failure"), "Failure traceback\nAssertionError: 1 != 0")]
        mock_result.skipped = []
        mock_result.expectedFailures = []
        mock_result.unexpectedSuccesses = []

        # Collect results
        self.collector.collect_results(mock_result)

        # Generate report
        md_path = self.test_reports_dir / "test_report_with_failures.md"
        self.collector.generate_markdown_report(md_path)

        # Check the contents
        with open(md_path, 'r') as f:
            content = f.read()

        self.assertIn("## Failure and Error Details", content)
        self.assertIn("### ERROR:", content)
        self.assertIn("### FAIL:", content)
        self.assertIn("**Message**: AssertionError: 1 != 0", content)

    def test_test_discoverer(self) -> None:
        """Test the TestDiscoverer class."""
        # Mock unittest.defaultTestLoader
        with patch('unittest.defaultTestLoader') as mock_loader:
            # Mock the discover method
            mock_suite = MagicMock()
            mock_loader.discover.return_value = mock_suite

            # Mock unittest.TextTestRunner
            with patch('unittest.TextTestRunner') as mock_runner_class:
                # Mock the runner and result
                mock_runner = MagicMock()
                mock_runner_class.return_value = mock_runner

                # Create a result that has testsRun as an int, not a MagicMock
                mock_result = MagicMock()
                mock_result.testsRun = 10  # Set it to a concrete integer
                mock_result.errors = []
                mock_result.failures = []
                mock_result.skipped = []
                mock_result.expectedFailures = []
                mock_result.unexpectedSuccesses = []
                mock_result.wasSuccessful.return_value = True

                mock_runner.run.return_value = mock_result

                # Create a discoverer and run tests
                test_dir = Path("./tests")
                discoverer = TestDiscoverer(test_dir)

                # Mock the report generation methods to avoid writing files
                with patch.object(TestResultCollector, 'generate_json_report'), \
                    patch.object(TestResultCollector, 'generate_markdown_report'):
                    success, results = discoverer.run_tests()

                # Check that tests were discovered and run
                mock_loader.discover.assert_called_once_with(str(test_dir))
                mock_runner.run.assert_called_once_with(mock_suite)

                # Check the result
                self.assertTrue(success)

    def _create_mock_test(self, name):
        """Create a mock test case for testing."""
        mock_test = MagicMock()
        mock_test._testMethodName = name
        mock_test.__class__.__name__ = "MockTestCase"
        mock_test.__class__.__module__ = "tests.test_mock"
        mock_test.id.return_value = f"tests.test_mock.MockTestCase.{name}"
        return mock_test


if __name__ == "__main__":
    unittest.main()
