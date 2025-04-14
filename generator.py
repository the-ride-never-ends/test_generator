#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Core test generation logic for Test Generator Mk2.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import ValidationError

from configs import Configs
from schemas.method import Method
from schemas.material import Material
from schemas.imports import Imports
from schemas.test_title import TestTitle
from schemas.variable import Variable
from utils.common.convert_to_snake_case import convert_to_snake_case
from utils.common.convert_to_pascal_case import convert_to_pascal_case
from utils.common.load_json_file import load_json_file
from utils.common.sanitize_variable_name import sanitize_variable_name


# Set up logger
logger = logging.getLogger("test_generator.generator")


class TestFileParameters:
    """
    Container for all test file parameters.
    
    This class handles loading, validating, and transforming the test parameters
    from JSON into usable Python objects.
    """
    
    def __init__(self, json_data: Dict[str, Any]):
        """
        Initialize test file parameters from JSON data.
        
        Args:
            json_data: Dictionary of test file parameters
        """
        self.raw_data = json_data.get("test_file_parameters", {})
        if not self.raw_data:
            raise ValueError("No test file parameters found in JSON data")
        
        # Parse and validate components
        self.test_title = self._parse_test_title()
        self.background = self._parse_background()
        self.independent_variable = self._parse_variable("independent_variable")
        self.dependent_variable = self._parse_variable("dependent_variable")
        self.control_variables = self._parse_control_variables()
        self.materials = self._parse_materials()
        self.test_method = self._parse_test_method()
        self.imports = self._parse_imports()
    
    def _parse_test_title(self) -> str:
        """Parse and validate the test title."""
        title_data = self.raw_data.get("test_title", "")
        if isinstance(title_data, str):
            # Simple string title
            return title_data
        elif isinstance(title_data, dict):
            # TestTitle object
            try:
                title_obj = TestTitle(**title_data)
                return title_obj.test_title
            except ValidationError as e:
                logger.warning(f"Error parsing test title: {e}")
                return "DefaultTestTitle"
        else:
            logger.warning(f"Unknown test title format: {title_data}")
            return "DefaultTestTitle"
    
    def _parse_background(self) -> Dict[str, Any]:
        """Parse and validate the background information."""
        bg_data = self.raw_data.get("background", {})
        return {
            "orientation": bg_data.get("orientation", ""),
            "purpose": bg_data.get("purpose", ""),
            "hypothesis": bg_data.get("hypothesis", ""),
            "citation_path": bg_data.get("citation_path", ""),
            "citation": bg_data.get("citation", "")
        }
    
    def _parse_variable(self, var_type: str) -> Variable:
        """
        Parse and validate a variable (independent or dependent).
        
        Args:
            var_type: Type of variable (independent_variable or dependent_variable)
            
        Returns:
            Variable: Validated variable object
        """
        var_data = self.raw_data.get(var_type, {})
        try:
            # Handle case insensitivity for statistical_type
            if "statistical_type" in var_data and isinstance(var_data["statistical_type"], str):
                var_data["statistical_type"] = var_data["statistical_type"].lower()
            return Variable(**var_data)
        except ValidationError as e:
            logger.error(f"Error parsing {var_type}: {e}")
            raise ValueError(f"Invalid {var_type} data") from e
    
    def _parse_control_variables(self) -> list[Variable]:
        """Parse and validate control variables."""
        control_vars_data = self.raw_data.get("control_variables", [])
        control_vars = []
        
        for var_data in control_vars_data:
            try:
                # Handle case insensitivity for statistical_type
                if "statistical_type" in var_data and isinstance(var_data["statistical_type"], str):
                    var_data["statistical_type"] = var_data["statistical_type"].lower()
                control_vars.append(Variable(**var_data))
            except ValidationError as e:
                logger.warning(f"Skipping invalid control variable: {e}")
        
        return control_vars
    
    def _parse_materials(self) -> list[Material]:
        """Parse and validate test materials."""
        # Handle both "material" and "test_materials" keys for compatibility
        materials_data = self.raw_data.get("test_materials", [])
        if not materials_data:
            materials_data = self.raw_data.get("material", [])
            if isinstance(materials_data, dict):
                # Handle single material as dict
                materials_data = [materials_data]
        
        materials = []
        for mat_data in materials_data:
            try:
                materials.append(Material(**mat_data))
            except ValidationError as e:
                logger.warning(f"Skipping invalid material: {e}")
        
        return materials
    
    def _parse_test_method(self) -> Method:
        """Parse and validate the test method."""
        method_data = self.raw_data.get("test_method", {})
        try:
            return Method(**method_data)
        except ValidationError as e:
            logger.error(f"Error parsing test method: {e}")
            raise ValueError("Invalid test method data") from e
    
    def _parse_imports(self) -> list[Imports]:
        """Parse and validate imports."""
        imports_data = self.raw_data.get("imports", [])
        imports = []
        
        for imp_data in imports_data:
            try:
                imports.append(Imports(**imp_data))
            except ValidationError as e:
                logger.warning(f"Skipping invalid import: {e}")
        
        return imports


class TestGenerator:
    """
    Core test generation logic.
    
    This class handles loading test specifications, applying templates,
    and managing the generation process.
    """
    
    def __init__(self, config: Configs):
        """
        Initialize the test generator.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.template_engine = self._initialize_template_engine()
        self.test_file_params = None
    
    def _initialize_template_engine(self) -> Environment:
        """
        Initialize the Jinja2 template engine.
        
        Returns:
            Environment: Configured Jinja2 environment
        """
        # First try package templates, then fall back to inline templates
        template_paths = [
            Path(__file__).parent / "templates",
            Path(__file__).parent / "test_templates"
        ]
        
        # Create a list of paths that exist
        existing_paths = [p for p in template_paths if p.exists()]
        
        if not existing_paths:
            logger.warning("No template directories found, using inline templates")
            # We'll use string templates later
            return None
        
        return Environment(
            loader=FileSystemLoader(existing_paths),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def _load_json_file(self) -> Dict[str, Any]:
        """
        Load and parse the JSON file with test parameters.
        
        Returns:
            Dict[str, Any]: Parsed JSON data
        """
        logger.info(f"Loading test parameters from {self.config.json_file_path}")
        return load_json_file(self.config.json_file_path)
    
    def _parse_test_parameters(self, json_data: Dict[str, Any]) -> TestFileParameters:
        """
        Parse and validate test parameters from JSON data.
        
        Args:
            json_data: Dictionary with JSON data
            
        Returns:
            TestFileParameters: Validated parameters
        """
        logger.info("Parsing test parameters")
        return TestFileParameters(json_data)
    
    def _get_template(self) -> Union[str, None]:
        """
        Get the appropriate template for the test framework.
        
        Returns:
            Union[str, None]: Template string or None if template engine is not available
        """
        harness = self.config.harness.lower()
        
        if self.template_engine:
            try:
                return self.template_engine.get_template(f"{harness}_test.py.j2")
            except Exception as e:
                logger.warning(f"Error loading template for {harness}: {e}")
        
        # Fall back to inline templates
        if harness == "unittest":
            return UNITTEST_TEMPLATE
        elif harness == "pytest":
            return PYTEST_TEMPLATE
        else:
            logger.error(f"Unsupported test harness: {harness}")
            raise ValueError(f"Unsupported test harness: {harness}")
    
    def _render_template(self, template: str) -> str:
        """
        Render the template with test parameters.
        
        Args:
            template: Template string or Jinja2 template
            
        Returns:
            str: Rendered test file
        """
        logger.info("Rendering test file template")
        
        # Check if the expected value is an exception class
        is_exception_test = False
        expected_value = None
        if hasattr(self.test_file_params.dependent_variable, 'expected_value'):
            ev = self.test_file_params.dependent_variable.expected_value
            expected_value = ev.value if ev else None
            if isinstance(expected_value, str) and "Error" in expected_value:
                is_exception_test = True
        
        # Sanitize variable names for Python
        independent_var_name = sanitize_variable_name(
            self.test_file_params.independent_variable.name)
            
        # Generate timestamp for the template
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create a rendered timestamp to replace the placeholder in the template
        rendered_content = None
        
        # Prepare context for template rendering
        context = {
            "config": self.config,
            "test_title": self.test_file_params.test_title,
            "test_class_name": convert_to_pascal_case(self.config.name),
            "test_func_name": convert_to_snake_case(self.config.name),
            "background": self.test_file_params.background,
            "independent_variable": self.test_file_params.independent_variable,
            "dependent_variable": self.test_file_params.dependent_variable,
            "control_variables": self.test_file_params.control_variables,
            "materials": self.test_file_params.materials,
            "test_method": self.test_file_params.test_method,
            "imports": self.test_file_params.imports,
            "independent_var_name": independent_var_name,
            "is_exception_test": is_exception_test,
            "expected_value": expected_value,
            "timestamp": timestamp
        }
        
        # Render template
        if hasattr(template, "render"):
            # Jinja2 template
            rendered_content = template.render(**context)
        else:
            # String template (basic formatting)
            rendered_content = template.format(**context)
            
        # Replace the timestamp placeholder with the actual timestamp
        rendered_content = rendered_content.replace("{{timestamp}}", timestamp)
        
        return rendered_content
    
    def generate_test_file(self) -> str:
        """
        Generate a test file based on JSON input.
        
        Returns:
            str: Generated test file content
        """
        # Load JSON data
        json_data = self._load_json_file()
        
        # Parse test parameters
        self.test_file_params = self._parse_test_parameters(json_data)
        
        # Get template
        template = self._get_template()
        
        # Render template
        return self._render_template(template)
    
    def write_test_file(self, content: str) -> Path:
        """
        Write the generated test file to disk.
        
        Args:
            content: Test file content
            
        Returns:
            Path: Path to the output file
        """
        # Create output directory if it doesn't exist
        output_dir = self.config.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create file path
        test_name = convert_to_snake_case(self.config.name)
        file_path = output_dir / f"test_{test_name}.py"
        
        # Write file
        file_path.write_text(content)
        logger.info(f"Test file written to {file_path}")
        
        return file_path


# Inline templates (used as fallback if template files are not available)
UNITTEST_TEMPLATE = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
{config.description}
"""
import unittest
import json
{% for imp in imports %}
{{ imp.import_string }}
{% endfor %}

class Test{test_class_name}(unittest.TestCase):
    """Test case for {test_title}."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def tearDown(self):
        """Tear down test fixtures."""
        pass
    
    def test_{test_func_name}(self):
        """
        Background: {background.orientation}
        Test Purpose: {background.purpose}
        Hypothesis: {background.hypothesis}
        
        Args:
            Independent Variable: 
                {independent_variable.name}: {independent_variable.description}
            Dependent Variable:
                {dependent_variable.name}: {dependent_variable.description}
            Control Variables:
            {% for var in control_variables %}
                {var.name}: {var.description}
            {% endfor %}
        """
        # Set up independent variable
        {{ independent_var_name }} = {{ independent_variable.value }}
        
        {% if is_exception_test %}
        # This is an exception test that expects {{ expected_value }}
        with self.assertRaises({{ expected_value }}):
            {% for step in test_method.steps %}
            # {{ step }}
            {% endfor %}
            # Add implementation to trigger the expected exception
            pass
        {% else %}
        # Expected result
        expected_value = {{ dependent_variable.expected_value.value }}
        
        # Test steps
        {% for step in test_method.steps %}
        # {{ step }}
        {% endfor %}
        
        # Validate results
        actual_value = None  # Replace with actual test result
        self.assertEqual(actual_value, expected_value)
        {% endif %}


if __name__ == "__main__":
    unittest.main()
'''

PYTEST_TEMPLATE = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
{config.description}
"""
import pytest
import json
{% for imp in imports %}
{{ imp.import_string }}
{% endfor %}

# Test fixtures
@pytest.fixture
def setup_test():
    """Set up test fixtures."""
    # Setup code here
    yield
    # Teardown code here


def test_{test_func_name}(setup_test):
    """
    Background: {background.orientation}
    Test Purpose: {background.purpose}
    Hypothesis: {background.hypothesis}
    
    Args:
        Independent Variable: 
            {independent_variable.name}: {independent_variable.description}
        Dependent Variable:
            {dependent_variable.name}: {dependent_variable.description}
        Control Variables:
        {% for var in control_variables %}
            {var.name}: {var.description}
        {% endfor %}
    """
    # Set up independent variable
    {{ independent_var_name }} = {{ independent_variable.value }}
    
    {% if is_exception_test %}
    # This is an exception test that expects {{ expected_value }}
    with pytest.raises({{ expected_value }}):
        {% for step in test_method.steps %}
        # {{ step }}
        {% endfor %}
        # Add implementation to trigger the expected exception
        pass
    {% else %}
    # Expected result
    expected_value = {{ dependent_variable.expected_value.value }}
    
    # Test steps
    {% for step in test_method.steps %}
    # {{ step }}
    {% endfor %}
    
    # Validate results
    actual_value = None  # Replace with actual test result
    assert actual_value == expected_value
    {% endif %}
'''