#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to generate reports for mypy and flake8 linting.
"""
import datetime
import json
import subprocess
from pathlib import Path
import sys
from typing import Dict, Any, List, Tuple


class LintResultCollector:
    """Collects and formats linting results for reporting."""

    def __init__(self) -> None:
        """Initialize the collector."""
        self.results: Dict[str, Any] = {
            "summary": {
                "mypy_errors": 0,
                "flake8_errors": 0,
                "total_errors": 0,
                "mypy_status": "not_run",
                "flake8_status": "not_run",
                "overall_status": "not_run",
                "timestamp": datetime.datetime.now().isoformat(),
            },
            "mypy_issues": [],
            "flake8_issues": []
        }

    def collect_mypy_results(self, output: str) -> Tuple[bool, int]:
        """
        Collect results from mypy output.

        Args:
            output: Output from mypy command

        Returns:
            Tuple of success status and error count
        """
        # Parse mypy output
        lines = output.strip().split('\n')
        error_count = 0

        for line in lines:
            if not line or "Success: no issues found" in line:
                continue

            error_count += 1

            # Try to parse the error line
            try:
                # Format is typically: file:line: error: message  [error-code]
                parts = line.split(':', 3)

                if len(parts) >= 3:
                    file_path = parts[0]
                    line_num = parts[1]
                    message = parts[2:]

                    # Join the remaining parts as the message
                    message_text = ':'.join(message).strip()

                    # Extract error code if present
                    error_code = ""
                    if "[" in message_text and "]" in message_text:
                        error_code = message_text.split('[')[-1].split(']')[0]

                    self.results["mypy_issues"].append({
                        "file": file_path,
                        "line": line_num,
                        "message": message_text,
                        "error_code": error_code
                    })
                else:
                    # If we can't parse it, just add the whole line
                    self.results["mypy_issues"].append({
                        "message": line
                    })
            except Exception:
                # If any parsing error, just add the whole line
                self.results["mypy_issues"].append({
                    "message": line
                })

        # Update summary
        self.results["summary"]["mypy_errors"] = error_count
        self.results["summary"]["total_errors"] += error_count
        self.results["summary"]["mypy_status"] = "pass" if error_count == 0 else "fail"

        # Return success status and error count
        return error_count == 0, error_count

    def collect_flake8_results(self, output: str) -> Tuple[bool, int]:
        """
        Collect results from flake8 output.

        Args:
            output: Output from flake8 command

        Returns:
            Tuple of success status and error count
        """
        # Parse flake8 output
        lines = output.strip().split('\n')
        error_count = 0

        for line in lines:
            if not line:
                continue

            error_count += 1

            # Try to parse the error line
            try:
                # Format is typically: ./file.py:line:col: code message
                parts = line.split(':', 3)

                if len(parts) >= 4:
                    file_path = parts[0]
                    line_num = parts[1]
                    col_num = parts[2]
                    code_message = parts[3].strip().split(' ', 1)

                    error_code = code_message[0] if len(code_message) > 0 else ""
                    message = code_message[1] if len(code_message) > 1 else ""

                    self.results["flake8_issues"].append({
                        "file": file_path,
                        "line": line_num,
                        "column": col_num,
                        "error_code": error_code,
                        "message": message
                    })
                else:
                    # If we can't parse it, just add the whole line
                    self.results["flake8_issues"].append({
                        "message": line
                    })
            except Exception:
                # If any parsing error, just add the whole line
                self.results["flake8_issues"].append({
                    "message": line
                })

        # Update summary
        self.results["summary"]["flake8_errors"] = error_count
        self.results["summary"]["total_errors"] += error_count
        self.results["summary"]["flake8_status"] = "pass" if error_count == 0 else "fail"

        # Return success status and error count
        return error_count == 0, error_count

    def update_overall_status(self) -> None:
        """Update the overall status based on mypy and flake8 statuses."""
        mypy_status = self.results["summary"]["mypy_status"]
        flake8_status = self.results["summary"]["flake8_status"]

        if mypy_status == "not_run" and flake8_status == "not_run":
            self.results["summary"]["overall_status"] = "not_run"
        elif mypy_status == "pass" and flake8_status == "pass":
            self.results["summary"]["overall_status"] = "pass"
        else:
            self.results["summary"]["overall_status"] = "fail"

    def generate_json_report(self, output_path: Path) -> None:
        """
        Generate a JSON report of the linting results.
        
        Args:
            output_path: Path to write the report to
        """
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)

    def generate_markdown_report(self, output_path: Path) -> None:
        """
        Generate a Markdown report of the linting results.

        Args:
            output_path: Path to write the report to
        """
        summary = self.results["summary"]
        mypy_issues = self.results["mypy_issues"]
        flake8_issues = self.results["flake8_issues"]

        # Format timestamp
        timestamp = datetime.datetime.fromisoformat(str(summary["timestamp"]))
        formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # Build markdown content
        content: List[str] = [
            "# Test Generator Mk2 - Linting Report",
            f"Generated on: {formatted_time}",
            "",
            "## Summary",
            "",
            f"- **Overall Status**: {summary['overall_status'].upper()}",
            f"- **Total Issues**: {summary['total_errors']}",
            f"- **Type Checking (mypy)**: {summary['mypy_status'].upper()} ({summary['mypy_errors']} issues)",
            f"- **Code Style (flake8)**: {summary['flake8_status'].upper()} ({summary['flake8_errors']} issues)",
            "",
        ]

        # Add mypy issues
        if mypy_issues:
            content.extend([
                "## Type Checking Issues (mypy)",
                "",
            ])

            # Group issues by file
            file_issues: Dict[str, List[Dict[str, Any]]] = {}
            for issue in mypy_issues:
                file_path = issue.get("file", "Unknown file")
                if file_path not in file_issues:
                    file_issues[file_path] = []
                file_issues[file_path].append(issue)

            # Add issues by file
            for file_path, issues in file_issues.items():
                content.append(f"### {file_path}")
                content.append("")

                for issue in issues:
                    line = issue.get("line", "")
                    message = issue.get("message", "")
                    error_code = issue.get("error_code", "")

                    error_info = f"Line {line}: {message}"
                    if error_code:
                        error_info += f" [{error_code}]"

                    content.append(f"- {error_info}")

                content.append("")

        # Add flake8 issues
        if flake8_issues:
            content.extend([
                "## Code Style Issues (flake8)",
                "",
            ])

            # Group issues by file
            file_issues: Dict[str, List[Dict[str, Any]]] = {}
            for issue in flake8_issues:
                file_path = issue.get("file", "Unknown file")
                if file_path not in file_issues:
                    file_issues[file_path] = []
                file_issues[file_path].append(issue)

            # Add issues by file
            for file_path, issues in file_issues.items():
                content.append(f"### {file_path}")
                content.append("")

                for issue in issues:
                    line = issue.get("line", "")
                    column = issue.get("column", "")
                    message = issue.get("message", "")
                    error_code = issue.get("error_code", "")

                    location = f"Line {line}"
                    if column:
                        location += f", Col {column}"

                    error_info = f"{location}: {error_code} {message}"

                    content.append(f"- {error_info}")

                content.append("")

        # Write the markdown file
        with open(output_path, 'w') as f:
            f.write('\n'.join(content))


def run_linting() -> Tuple[bool, Dict[str, Any]]:
    """
    Run linting and generate reports.
    
    Returns:
        Tuple of success status and lint results dictionary
    """
    # Set up collector
    collector = LintResultCollector()

    # Run mypy
    print("Running mypy type checking...")
    mypy_cmd = ["mypy", "--config-file", "mypy.ini", "."]
    try:
        mypy_result = subprocess.run(mypy_cmd, capture_output=True, text=True)
        mypy_success, mypy_errors = collector.collect_mypy_results(mypy_result.stdout + mypy_result.stderr)

        if mypy_success:
            print("✅ Type checking passed!")
        else:
            print(f"❌ Type checking failed with {mypy_errors} errors")
    except Exception as e:
        print(f"Error running mypy: {e}")
        mypy_success = False

    # Run flake8
    print("\nRunning flake8 linting...")
    flake8_cmd = ["flake8"]
    try:
        flake8_result = subprocess.run(flake8_cmd, capture_output=True, text=True)
        flake8_success, flake8_errors = collector.collect_flake8_results(flake8_result.stdout + flake8_result.stderr)

        if flake8_success:
            print("✅ Linting passed!")
        else:
            print(f"❌ Linting failed with {flake8_errors} errors")
    except Exception as e:
        print(f"Error running flake8: {e}")
        flake8_success = False

    # Update overall status
    collector.update_overall_status()

    # Generate reports
    reports_dir = Path("test_reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = reports_dir / f"lint_report_{timestamp}.json"
    markdown_path = reports_dir / f"lint_report_{timestamp}.md"

    collector.generate_json_report(json_path)
    collector.generate_markdown_report(markdown_path)

    print(f"\nLint reports generated:")
    print(f"  - JSON: {json_path}")
    print(f"  - Markdown: {markdown_path}")

    # Also generate latest report links
    latest_json = reports_dir / "latest_lint_report.json"
    latest_md = reports_dir / "latest_lint_report.md"

    collector.generate_json_report(latest_json)
    collector.generate_markdown_report(latest_md)

    # Overall success is mypy_success AND flake8_success
    overall_success = mypy_success and flake8_success

    return overall_success, collector.results


if __name__ == "__main__":
    success, _ = run_linting()
    # Exit with non-zero code if linting failed
    sys.exit(0 if success else 1)