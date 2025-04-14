#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Command-line interface for the Test Generator Mk2.
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from pydantic import ValidationError

from __version__ import __version__
from configs import Configs
from generator import TestGenerator

sys.path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("test_generator")


class CLI:
    """
    Command-line interface for the Test Generator Mk2.
    
    Handles command-line arguments, configuration loading, and pipeline orchestration.
    """
    
    def __init__(self):
        """Initialize the CLI with an argument parser."""
        self.parser = self._create_parser()
        self.args = None
        self.config = None
        self.generator = None
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create the argument parser for the CLI.
        
        Returns:
            argparse.ArgumentParser: Configured argument parser
        """
        parser = argparse.ArgumentParser(description="Generate test files based on JSON input.")
        parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
        parser.add_argument("--name", type=str, required=True, help="Test name")
        parser.add_argument("--description", type=str, help="A short description of the test")
        parser.add_argument(
            "--test_parameter_json", type=str, required=True, 
            help="The file path to the test parameters JSON file"
        )
        
        parser.add_argument(
            "--output_dir", type=str, default="./tests", 
            help="Path to output directory for tests (default: ./tests)"
        )
        parser.add_argument(
            "--verbose", action="store_true", default=True, 
            help="Enable verbose output (default: true)"
        )
        parser.add_argument(
            "--harness", type=str, default="unittest", choices=["unittest", "pytest"],
            help="Which python testing harness to use (default: unittest)"
        )
        parser.add_argument(
            "--has-fixtures", action="store_true", default=False, 
            help="Whether a test needs fixtures in order to run (default: false)"
        )
        parser.add_argument(
            "--docstring-style", type=str, default="google", 
            help="Docstring style to parse (default: google)"
        )
        
        return parser
    
    def parse_args(self, args: Optional[list[str]] = None) -> Dict[str, Any]:
        """
        Parse command-line arguments.
        
        Args:
            args: Command-line arguments (uses sys.argv if None)
            
        Returns:
            Dict[str, Any]: Dictionary of parsed arguments
        """
        self.args = self.parser.parse_args(args)
        
        # Convert Namespace to dict for Pydantic
        return vars(self.args)
    
    def validate_config(self, args_dict: Dict[str, Any]) -> bool:
        """
        Validate configuration using Pydantic models.
        
        Args:
            args_dict: Dictionary of arguments to validate
            
        Returns:
            bool: True if validation passed, False otherwise
        """
        try:
            # Rename test_parameter_json to json_file_path for backward compatibility
            if "test_parameter_json" in args_dict and "json_file_path" not in args_dict:
                args_dict["json_file_path"] = args_dict.pop("test_parameter_json")
            
            # If output_dir is provided, ensure it exists before validation
            if 'output_dir' in args_dict and args_dict['output_dir']:
                output_dir = Path(args_dict['output_dir'])
                if not output_dir.exists():
                    logger.info(f"Creating output directory: {output_dir}")
                    output_dir.mkdir(parents=True, exist_ok=True)
                
            self.config = Configs.model_validate(args_dict)
            return True
        except ValidationError as e:
            logger.error(f"Configuration validation error: {e}")
            return False
    
    def run(self) -> int:
        """
        Run the test generator pipeline.
        
        Returns:
            int: Exit code (0 for success, non-zero for errors)
        """
        try:
            # Set up logging level
            if self.config and self.config.verbose:
                logger.setLevel(logging.DEBUG)
            
            # Initialize generator
            self.generator = TestGenerator(self.config)
            
            # Generate and save test file
            test_file = self.generator.generate_test_file()
            output_path = self.generator.write_test_file(test_file)
            
            logger.info(f"Test file generated successfully at {output_path}")
            return 0
            
        except Exception as e:
            logger.error(f"Error generating test file: {e}")
            if self.config and self.config.verbose:
                import traceback
                traceback.print_exc()
            return 1


def main() -> int:
    """
    Main entry point for the CLI.
    
    Returns:
        int: Exit code
    """
    cli = CLI()
    args_dict = cli.parse_args()
    
    if not cli.validate_config(args_dict):
        return 1
    
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())