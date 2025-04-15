#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive tests for schema validation methods.
"""
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the parent directory to sys.path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from schemas.variable import Variable
from schemas.expected_value import ExpectedValue
from schemas.validation_procedure import ValidationProcedure
from schemas.statistical_type import StatisticalType
# Fix the typo in the original code
StatisticalType.CONTINUOUS = StatisticalType.CONTINOUS
from schemas.material import Material
from schemas.method import Method
from schemas.test_title import TestTitle
from schemas.imports import Imports


class TestValidationProcedures(unittest.TestCase):
    """Test the ValidationProcedure schema class."""
    
    def test_validation_procedure_creation(self):
        """Test creating a validation procedure."""
        procedure = ValidationProcedure(
            name="test_validation",
            description="Test validation procedure",
            steps=["Step 1", "Step 2", "Step 3"],
            kwargs={"test_arg": "test_value"}
        )
        
        self.assertEqual(procedure.name, "test_validation")
        self.assertEqual(procedure.description, "Test validation procedure")
        self.assertEqual(procedure.steps, ["Step 1", "Step 2", "Step 3"])
        self.assertEqual(procedure.kwargs, {"test_arg": "test_value"})
    
    def test_validation_procedure_optional_fields(self):
        """Test creating a validation procedure with optional fields omitted."""
        procedure = ValidationProcedure(
            name="test_validation",
            description="Test validation procedure",
            steps=["Step 1", "Step 2"]
        )
        
        self.assertIsNone(procedure.kwargs)


class TestExpectedValue(unittest.TestCase):
    """Test the ExpectedValue schema class."""
    
    def test_expected_value_creation(self):
        """Test creating an expected value."""
        validation_procedure = ValidationProcedure(
            name="test_validation",
            description="Test validation procedure",
            steps=["Step 1", "Step 2"]
        )
        
        expected_value = ExpectedValue(
            value="test_value",
            validation_procedures=[validation_procedure]
        )
        
        self.assertEqual(expected_value.value, "test_value")
        self.assertEqual(len(expected_value.validation_procedures), 1)
        self.assertEqual(expected_value.validation_procedures[0].name, "test_validation")
    
    def test_expected_value_multiple_procedures(self):
        """Test creating an expected value with multiple validation procedures."""
        validation_procedure1 = ValidationProcedure(
            name="test_validation1",
            description="Test validation procedure 1",
            steps=["Step 1.1", "Step 1.2"]
        )
        
        validation_procedure2 = ValidationProcedure(
            name="test_validation2",
            description="Test validation procedure 2",
            steps=["Step 2.1", "Step 2.2"]
        )
        
        expected_value = ExpectedValue(
            value="test_value",
            validation_procedures=[validation_procedure1, validation_procedure2]
        )
        
        self.assertEqual(len(expected_value.validation_procedures), 2)
        self.assertEqual(expected_value.validation_procedures[0].name, "test_validation1")
        self.assertEqual(expected_value.validation_procedures[1].name, "test_validation2")


class TestVariableValidation(unittest.TestCase):
    """Test the Variable schema class with comprehensive validation testing."""
    
    def test_variable_creation_discrete(self):
        """Test creating a discrete variable."""
        variable = Variable(
            name="Test Variable",
            description="A test variable",
            statistical_type=StatisticalType.DISCRETE,
            unit="units",
            value=10
        )
        
        self.assertEqual(variable.name, "Test Variable")
        self.assertEqual(variable.description, "A test variable")
        self.assertEqual(variable.statistical_type, StatisticalType.DISCRETE)
        self.assertEqual(variable.unit, "units")
        self.assertEqual(variable.value, 10)
        self.assertIsNone(variable.expected_value)
    
    def test_variable_creation_continuous(self):
        """Test creating a continuous variable."""
        variable = Variable(
            name="Test Variable",
            description="A test variable",
            statistical_type=StatisticalType.CONTINUOUS,
            unit="units",
            value=10.5
        )
        
        self.assertEqual(variable.value, 10.5)
        self.assertEqual(variable.statistical_type, StatisticalType.CONTINUOUS)
    
    def test_variable_creation_nominal(self):
        """Test creating a nominal variable."""
        variable = Variable(
            name="Test Variable",
            description="A test variable",
            statistical_type=StatisticalType.NOMINAL,
            unit="units",
            value="category_a"
        )
        
        self.assertEqual(variable.value, "category_a")
        self.assertEqual(variable.statistical_type, StatisticalType.NOMINAL)
    
    def test_variable_creation_ordinal(self):
        """Test creating an ordinal variable."""
        variable = Variable(
            name="Test Variable",
            description="A test variable",
            statistical_type=StatisticalType.ORDINAL,
            unit="units",
            value="medium"
        )
        
        self.assertEqual(variable.value, "medium")
        self.assertEqual(variable.statistical_type, StatisticalType.ORDINAL)
    
    def test_variable_with_expected_value(self):
        """Test creating a variable with an expected value."""
        validation_procedure = ValidationProcedure(
            name="test_validation",
            description="Test validation procedure",
            steps=["Step 1", "Step 2"]
        )
        
        expected_value = ExpectedValue(
            value="test_value",
            validation_procedures=[validation_procedure]
        )
        
        variable = Variable(
            name="Test Variable",
            description="A test variable",
            statistical_type=StatisticalType.NOMINAL,
            unit="units",
            value="input_value",
            expected_value=expected_value
        )
        
        self.assertEqual(variable.expected_value.value, "test_value")
        self.assertEqual(len(variable.expected_value.validation_procedures), 1)
    
    def test_name_in_python_property(self):
        """Test the name_in_python property of Variable."""
        variable = Variable(
            name="Test Variable Name",
            description="A test variable",
            statistical_type=StatisticalType.DISCRETE,
            unit="units",
            value=10
        )
        
        # Should convert to snake_case
        self.assertEqual(variable.name_in_python, "test_variable_name")
    
    def test_type_in_python_property(self):
        """Test the type_in_python property of Variable."""
        # Discrete -> int
        variable_discrete = Variable(
            name="Discrete Var",
            description="A discrete variable",
            statistical_type=StatisticalType.DISCRETE,
            unit="units",
            value=10
        )
        self.assertEqual(variable_discrete.type_in_python, int)
        
        # Continuous -> float
        variable_continuous = Variable(
            name="Continuous Var",
            description="A continuous variable",
            statistical_type=StatisticalType.CONTINUOUS,
            unit="units",
            value=10.5
        )
        self.assertEqual(variable_continuous.type_in_python, float)
        
        # Nominal -> str
        variable_nominal = Variable(
            name="Nominal Var",
            description="A nominal variable",
            statistical_type=StatisticalType.NOMINAL,
            unit="units",
            value="category_a"
        )
        self.assertEqual(variable_nominal.type_in_python, str)
        
        # Ordinal -> str
        variable_ordinal = Variable(
            name="Ordinal Var",
            description="An ordinal variable",
            statistical_type=StatisticalType.ORDINAL,
            unit="units",
            value="medium"
        )
        self.assertEqual(variable_ordinal.type_in_python, str)


class TestMaterial(unittest.TestCase):
    """Test the Material schema class."""
    
    def test_material_creation(self):
        """Test creating a material."""
        material = Material(
            name="Test Material",
            description="A test material",
            type="library",
            version="1.0.0",
            configuration={"setting": "value"},
            source="test source"
        )
        
        self.assertEqual(material.name, "Test Material")
        self.assertEqual(material.description, "A test material")
        self.assertEqual(material.type, "library")
        self.assertEqual(material.version, "1.0.0")
        self.assertEqual(material.configuration, {"setting": "value"})
        self.assertEqual(material.source, "test source")
    
    def test_material_optional_fields(self):
        """Test creating a material with optional fields omitted."""
        material = Material(
            name="Test Material",
            description="A test material",
            type="library"
        )
        
        self.assertIsNone(material.version)
        self.assertIsNone(material.configuration)
        self.assertIsNone(material.source)


class TestMethod(unittest.TestCase):
    """Test the Method schema class."""
    
    def test_method_creation(self):
        """Test creating a method."""
        method = Method(
            steps=["Step 1", "Step 2", "Step 3"],
            data_collection="Test data collection",
            analysis_technique="Test analysis technique"
        )
        
        self.assertEqual(method.steps, ["Step 1", "Step 2", "Step 3"])
        self.assertEqual(method.data_collection, "Test data collection")
        self.assertEqual(method.analysis_technique, "Test analysis technique")


class TestImports(unittest.TestCase):
    """Test the Imports schema class."""
    
    def test_import_creation(self):
        """Test creating an import."""
        imp = Imports(name="test_module")
        
        self.assertEqual(imp.name, "test_module")
        self.assertIsNone(imp.import_funcs)
        self.assertEqual(imp.import_string, "import test_module")
    
    def test_import_with_functions(self):
        """Test creating an import with functions."""
        imp = Imports(name="test_module", import_funcs=["func1", "func2"])
        
        self.assertEqual(imp.name, "test_module")
        self.assertEqual(imp.import_funcs, ["func1", "func2"])
        self.assertEqual(imp.import_string, "from test_module import func1, func2")


class TestTestTitle(unittest.TestCase):
    """Test the TestTitle schema class."""
    
    def test_test_title(self):
        """Test creating a test title."""
        title = TestTitle(test_title="Test Title")
        
        self.assertEqual(title.test_title, "TestTitle")  # PascalCase conversion
    
    def test_test_title_default(self):
        """Test creating a test title with the default value."""
        title = TestTitle()
        
        self.assertEqual(title.test_title, "ThisIsAGenericTitle")  # Default value + PascalCase
        
    def test_test_title_model_validator(self):
        """Test that the model validator converts to PascalCase."""
        # Test that spaces are removed and each word is capitalized
        title = TestTitle(test_title="this is a test title")
        self.assertEqual(title.test_title, "ThisIsATestTitle")
        
        # The current implementation doesn't preserve existing PascalCase
        # but rather just capitalizes each word and removes spaces
        title = TestTitle(test_title="AlreadyPascalCase")
        self.assertEqual(title.test_title, "Alreadypascalcase")


if __name__ == "__main__":
    unittest.main()