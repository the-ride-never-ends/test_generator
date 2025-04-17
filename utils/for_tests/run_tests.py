#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to run all tests for Test Generator and generate reports.
"""
import datetime
import json
from pathlib import Path
import sys
import time
from typing import Dict, Tuple, Any
import unittest


class TestResultCollector:
    """Collects and formats test results for reporting."""

    def __init__(self, start_time: float):
        """Initialize the collector with a start time."""
        self.start_time = start_time
        self.results = {
            "summary": {
                "tests": 0,
                "errors": 0,
                "failures": 0,
                "skipped": 0,
                "expected_failures": 0,
                "unexpected_successes": 0,
                "success_rate": 0.0,
                "duration": 0.0,
                "timestamp": datetime.datetime.now().isoformat(),
            },
            "test_cases": []
        }

    def collect_results(self, result: unittest.TestResult) -> None:
        """
        Collect results from a TestResult object.
        
        Args:
            result: TestResult object from the test run
        """
        # Calculate duration
        duration = time.time() - self.start_time

        # Update summary
        self.results["summary"]["tests"] = result.testsRun
        self.results["summary"]["errors"] = len(result.errors)
        self.results["summary"]["failures"] = len(result.failures)
        self.results["summary"]["skipped"] = len(result.skipped)
        self.results["summary"]["expected_failures"] = len(result.expectedFailures)
        self.results["summary"]["unexpected_successes"] = len(result.unexpectedSuccesses)

        # Calculate success rate
        success_count = result.testsRun - len(result.errors) - len(result.failures)
        self.results["summary"]["success_rate"] = (success_count / result.testsRun) * 100 if result.testsRun > 0 else 0
        self.results["summary"]["duration"] = round(duration, 2)

        # Process failures
        for test, traceback in result.failures:
            self.results["test_cases"].append({
                "id": str(test.id()),
                "name": test._testMethodName,
                "module": test.__class__.__module__,
                "class": test.__class__.__name__,
                "status": "FAIL",
                "message": self._extract_message(traceback),
                "traceback": traceback
            })

        # Process errors
        for test, traceback in result.errors:
            self.results["test_cases"].append({
                "id": str(test.id()),
                "name": test._testMethodName,
                "module": test.__class__.__module__,
                "class": test.__class__.__name__,
                "status": "ERROR",
                "message": self._extract_message(traceback),
                "traceback": traceback
            })

        # Process skipped tests
        for test, reason in result.skipped:
            self.results["test_cases"].append({
                "id": str(test.id()),
                "name": test._testMethodName,
                "module": test.__class__.__module__,
                "class": test.__class__.__name__,
                "status": "SKIPPED",
                "message": reason,
                "traceback": ""
            })

        # Process expected failures
        for test, traceback in getattr(result, 'expectedFailures', []):
            self.results["test_cases"].append({
                "id": str(test.id()),
                "name": test._testMethodName,
                "module": test.__class__.__module__,
                "class": test.__class__.__name__,
                "status": "EXPECTED_FAILURE",
                "message": self._extract_message(traceback),
                "traceback": traceback
            })

        # Process unexpected successes
        for test in getattr(result, 'unexpectedSuccesses', []):
            self.results["test_cases"].append({
                "id": str(test.id()),
                "name": test._testMethodName,
                "module": test.__class__.__module__,
                "class": test.__class__.__name__,
                "status": "UNEXPECTED_SUCCESS",
                "message": "Test unexpectedly passed",
                "traceback": ""
            })

    def _extract_message(self, traceback: str) -> str:
        """Extract the error message from a traceback."""
        lines = traceback.strip().split('\n')
        return lines[-1] if lines else "No message"

    def generate_json_report(self, output_path: Path) -> None:
        """
        Generate a JSON report of the test results.
        
        Args:
            output_path: Path to write the report to
        """
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)

    def generate_markdown_report(self, output_path: Path) -> None:
        """
        Generate a Markdown report of the test results.

        Args:
            output_path: Path to write the report to
        """
        summary = self.results["summary"]
        test_cases = self.results["test_cases"]

        # Format timestamp
        timestamp = datetime.datetime.fromisoformat(summary["timestamp"])
        formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # Build markdown content
        content = [
            "# Test Generator Mk2 - Test Report",
            f"Generated on: {formatted_time}",
            "",
            "## Summary",
            "",
            f"- **Tests Run**: {summary['tests']}",
            f"- **Passed**: {summary['tests'] - summary['failures'] - summary['errors']}",
            f"- **Failures**: {summary['failures']}",
            f"- **Errors**: {summary['errors']}",
            f"- **Skipped**: {summary['skipped']}",
            f"- **Expected Failures**: {summary['expected_failures']}",
            f"- **Unexpected Successes**: {summary['unexpected_successes']}",
            f"- **Success Rate**: {summary['success_rate']:.2f}%",
            f"- **Duration**: {summary['duration']} seconds",
            "",
        ]

        # Add test details if there are any issues
        if test_cases:
            content.extend([
                "## Test Details",
                "",
                "| Status | Module | Class | Test |",
                "|--------|--------|-------|------|",
            ])

            for test_case in test_cases:
                status = test_case["status"]
                module = test_case["module"]
                cls = test_case["class"]
                name = test_case["name"]
                
                content.append(f"| {status} | {module} | {cls} | {name} |")

            # Add failure/error details
            failures_or_errors = [tc for tc in test_cases if tc["status"] in ("FAIL", "ERROR")]
            if failures_or_errors:
                content.extend([
                    "",
                    "## Failure and Error Details",
                    ""
                ])

                for tc in failures_or_errors:
                    content.extend([
                        f"### {tc['status']}: {tc['module']}.{tc['class']}.{tc['name']}",
                        "",
                        f"**Message**: {tc['message']}",
                        "",
                        "```",
                        tc["traceback"],
                        "```",
                        ""
                    ])

        # Write the markdown file
        with open(output_path, 'w') as f:
            f.write('\n'.join(content))


class TestDiscoverer:
    """Discovers and runs tests, then generates reports."""

    def __init__(self, test_dir: Path, verbosity: int = 2):
        """
        Initialize the test discoverer.

        Args:
            test_dir: Directory to look for tests in
            verbosity: Verbosity level for test output
        """
        self.test_dir = test_dir
        self.verbosity = verbosity

    def run_tests(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Discover and run tests, then return the results.

        Returns:
            Tuple containing success status and test results
        """
        # Discover tests
        test_suite = unittest.defaultTestLoader.discover(self.test_dir)

        # Create result collector
        start_time = time.time()
        collector = TestResultCollector(start_time)

        # Run tests
        test_runner = unittest.TextTestRunner(verbosity=self.verbosity)
        result = test_runner.run(test_suite)

        # Collect results
        collector.collect_results(result)

        # Generate reports
        reports_dir = Path("test_reports")
        reports_dir.mkdir(exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        json_path = reports_dir / f"test_report_{timestamp}.json"
        markdown_path = reports_dir / f"test_report_{timestamp}.md"

        collector.generate_json_report(json_path)
        collector.generate_markdown_report(markdown_path)

        print(f"\nTest reports generated:")
        print(f"  - JSON: {json_path}")
        print(f"  - Markdown: {markdown_path}")

        # Also generate latest report links
        latest_json = reports_dir / "latest_report.json"
        latest_md = reports_dir / "latest_report.md"

        collector.generate_json_report(latest_json)
        collector.generate_markdown_report(latest_md)

        return result.wasSuccessful(), collector.results


if __name__ == "__main__":
    # Set verbosity from command line arguments
    verbosity = 2
    if len(sys.argv) > 1 and sys.argv[1] == "-q":
        verbosity = 1

    # Discover and run tests
    # Use the current working directory (which should be the project root due to cd in run_tests.sh)
    test_dir = Path.cwd() / "tests"
    print(f"Looking for tests in: {test_dir}")
    discoverer = TestDiscoverer(test_dir, verbosity)

    success, _ = discoverer.run_tests()

    # Exit with non-zero code if tests failed
    sys.exit(0 if success else 1)