from __future__ import annotations


from pathlib import Path
from typing import Dict, Any, Optional


from pydantic import BaseModel, DirectoryPath, Field, FilePath, field_validator


from __version__ import __version__


ROOT_DIR = Path(__file__).parent


class Configs(BaseModel):
    """
    Configuration settings for test generator.

    Validates and stores command-line arguments and settings.
    """
    version: str = Field(default=__version__, description="Version of the test generator")
    name: str = Field(..., description="Name of the test")
    description: str = Field(..., description="A short description of the test")
    json_file_path: FilePath = Field(..., description="The file path to the test parameters JSON file")
    output_dir: DirectoryPath = Field(default=Path("tests"), description="Path to output directory for tests")
    verbose: bool = Field(default=True, description="Enable verbose output")
    harness: str = Field(default="unittest", description="Which python testing harness to use")
    has_fixtures: bool = Field(default=False, description="Whether a test needs fixtures in order to run")
    parametrized: bool = Field(default=False, description="Whether to generate parametrized tests")
    debug: bool = Field(default=False, description="Enable debug mode with enhanced output")
    docstring_style: str = Field(default="google", description="Docstring style to parse")
    test_params: Optional[Dict[str, Any]] = Field(default=None, description="Parameters for conditional test generation")

    @field_validator("harness")
    def validate_harness(cls, v: str) -> str:
        """Validate test harness name."""
        valid_harnesses = ["unittest", "pytest"]
        if v.lower() not in valid_harnesses:
            raise ValueError(f"Harness must be one of: {', '.join(valid_harnesses)}")
        return v.lower()
