#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to automatically fix common whitespace issues in Python files.
"""
import argparse
import glob
import os
from typing import List, Tuple, Optional


def clean_whitespace_in_blank_lines(file_path: str) -> int:
    """
    Clean whitespace in blank lines in a file.

    Args:
        file_path: Path to the file to clean

    Returns:
        Number of lines fixed
    """
    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Clean blank lines
    cleaned_lines = []
    fixed_count = 0

    for line in lines:
        # If line contains only whitespace, replace with an empty line
        if line.strip() == '':
            if line != '\n':  # Only count lines that actually had whitespace
                fixed_count += 1
            cleaned_lines.append('\n')
        else:
            cleaned_lines.append(line)

    # Only write if changes were made
    if fixed_count > 0:
        # Write the cleaned content back to the file
        with open(file_path, 'w') as f:
            f.writelines(cleaned_lines)

    return fixed_count


def fix_trailing_whitespace(file_path: str) -> int:
    """
    Fix trailing whitespace in a file.

    Args:
        file_path: Path to the file to fix

    Returns:
        Number of lines fixed
    """
    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Clean trailing whitespace
    cleaned_lines = []
    fixed_count = 0

    for line in lines:
        # Check if there's trailing whitespace (not counting blank lines)
        stripped = line.rstrip()
        # Only count lines that have content AND trailing whitespace
        if stripped and line != stripped + ('\n' if line.endswith('\n') else ''):
            fixed_count += 1

        # Remove trailing whitespace and preserve newline for all lines
        cleaned_lines.append(stripped + ('\n' if line.endswith('\n') else ''))

    # Only write if changes were made
    if fixed_count > 0 or any(line != cleaned_line for line, cleaned_line in zip(lines, cleaned_lines)):
        # Write the cleaned content back to the file
        with open(file_path, 'w') as f:
            f.writelines(cleaned_lines)

    return fixed_count


def ensure_newline_at_end_of_file(file_path: str) -> int:
    """
    Ensure file ends with a newline.

    Args:
        file_path: Path to the file to fix

    Returns:
        1 if fixed, 0 if already correct
    """
    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()

    # Add newline if missing
    if content and not content.endswith('\n'):
        with open(file_path, 'a') as f:
            f.write('\n')
        return 1

    return 0


def find_files(patterns: List[str], exclude_dirs: Optional[List[str]] = None) -> List[str]:
    """
    Find files matching the given patterns.

    Args:
        patterns: List of file patterns (e.g. ["*.py"])
        exclude_dirs: List of directory patterns to exclude

    Returns:
        List of file paths
    """
    if exclude_dirs is None:
        exclude_dirs = []

    # Convert exclude directories to absolute paths
    exclude_abs = [os.path.abspath(d) for d in exclude_dirs]

    # Find all files matching the patterns
    all_files = set()
    for pattern in patterns:
        for file_path in glob.glob(pattern, recursive=True):
            # Check if file is in an excluded directory
            file_abs = os.path.abspath(file_path)
            if not any(file_abs.startswith(excl) for excl in exclude_abs):
                all_files.add(file_path)

    return sorted(list(all_files))


def fix_files(file_paths: List[str], fix_blank: bool = True, fix_trailing: bool = True,
              fix_newlines: bool = True, verbose: bool = False) -> Tuple[int, int, int, int]:
    """
    Fix issues in the given files.

    Args:
        file_paths: List of file paths to fix
        fix_blank: Whether to fix blank lines with whitespace
        fix_trailing: Whether to fix trailing whitespace
        fix_newlines: Whether to ensure files end with a newline
        verbose: Whether to print details about each file

    Returns:
        Tuple of (number of files fixed, blank line fixes, trailing whitespace fixes, newline fixes)
    """
    files_fixed = 0
    blank_fixes = 0
    trailing_fixes = 0
    newline_fixes = 0

    for i, file_path in enumerate(file_paths):
        if verbose:
            print(f"Processing file {i + 1}/{len(file_paths)}: {file_path}")

        file_modified = False

        # Fix blank lines
        if fix_blank:
            blank_count = clean_whitespace_in_blank_lines(file_path)
            blank_fixes += blank_count
            if blank_count > 0:
                file_modified = True
                if verbose:
                    print(f"  Fixed {blank_count} blank lines with whitespace")

        # Fix trailing whitespace
        if fix_trailing:
            trailing_count = fix_trailing_whitespace(file_path)
            trailing_fixes += trailing_count
            if trailing_count > 0:
                file_modified = True
                if verbose:
                    print(f"  Fixed {trailing_count} lines with trailing whitespace")

        # Ensure newline at end of file
        if fix_newlines:
            newline_fixed = ensure_newline_at_end_of_file(file_path)
            newline_fixes += newline_fixed
            if newline_fixed > 0:
                file_modified = True
                if verbose:
                    print("  Added missing newline at end of file")

        if file_modified:
            files_fixed += 1

    return files_fixed, blank_fixes, trailing_fixes, newline_fixes


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Fix common whitespace issues in Python files")
    parser.add_argument("--patterns", nargs="+", default=["**/*.py"],
                        help="File patterns to match (default: '**/*.py')")
    parser.add_argument("--exclude", nargs="+", default=[".venv", ".git", "__pycache__"],
                        help="Directories to exclude (default: .venv, .git, __pycache__)")
    parser.add_argument("--no-blank", action="store_true",
                        help="Don't fix blank lines with whitespace")
    parser.add_argument("--no-trailing", action="store_true",
                        help="Don't fix trailing whitespace")
    parser.add_argument("--no-newlines", action="store_true",
                        help="Don't ensure files end with a newline")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print detailed information for each file")
    parser.add_argument("--dry-run", action="store_true",
                        help="Don't make any changes, just show what would be done")

    args = parser.parse_args()

    # Find files
    file_paths = find_files(args.patterns, args.exclude)
    print(f"Found {len(file_paths)} files to process")

    if args.dry_run:
        print("Dry run mode - no changes will be made")
        for file_path in file_paths:
            print(f"Would process: {file_path}")
        return

    # Fix files
    files_fixed, blank_fixes, trailing_fixes, newline_fixes = fix_files(
        file_paths,
        fix_blank=not args.no_blank,
        fix_trailing=not args.no_trailing,
        fix_newlines=not args.no_newlines,
        verbose=args.verbose
    )

    # Print summary
    print(f"\nFixed {files_fixed} out of {len(file_paths)} files:")
    if not args.no_blank:
        print(f"- {blank_fixes} blank lines with whitespace")
    if not args.no_trailing:
        print(f"- {trailing_fixes} lines with trailing whitespace")
    if not args.no_newlines:
        print(f"- {newline_fixes} files missing final newline")


if __name__ == "__main__":
    main()
