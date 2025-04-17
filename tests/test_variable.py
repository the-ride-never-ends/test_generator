import unittest
from pydantic import ValidationError

from schemas.variable import Variable, _get_python_type_from_statistical_type
from schemas.statistical_type import StatisticalType
from schemas.expected_value import ExpectedValue


class TestGetPythonType(unittest.TestCase):
    """Test the _get_python_type_from_statistical_type function."""

    def test_ordinal_type(self) -> None:
        """Test that ORDINAL returns str type."""
        self.assertEqual(_get_python_type_from_statistical_type(StatisticalType.ORDINAL), str)

    def test_nominal_type(self) -> None:
        """Test that NOMINAL returns str type."""
        self.assertEqual(_get_python_type_from_statistical_type(StatisticalType.NOMINAL), str)

    def test_discrete_type(self) -> None:
        """Test that DISCRETE returns int type."""
        self.assertEqual(_get_python_type_from_statistical_type(StatisticalType.DISCRETE), int)

    def test_continuous_type(self) -> None:
        """Test that CONTINUOUS returns float type."""
        self.assertEqual(_get_python_type_from_statistical_type(StatisticalType.CONTINOUS), float)

    def test_invalid_type(self) -> None:
        """Test that a non-StatisticalType value raises ValueError."""
        with self.assertRaises(ValueError):
            _get_python_type_from_statistical_type("INVALID")


class TestVariableProperties(unittest.TestCase):
    """Test the properties of the Variable class."""

    def setUp(self) -> None:
        """Set up test variables."""
        self.variable_ordinal = Variable(
            name="Test Status",
            description="The status of the test",
            statistical_type=StatisticalType.ORDINAL,
            unit="status"
        )
        
        self.variable_discrete = Variable(
            name="Number of Errors",
            description="Count of errors in the test",
            statistical_type=StatisticalType.DISCRETE,
            unit="errors",
            value=5
        )
        
        self.variable_with_expected = Variable(
            name="Response Time",
            description="Time taken to respond",
            statistical_type=StatisticalType.CONTINOUS,
            unit="ms",
            value=100.5,
            expected_value=ExpectedValue(
                value=100.0,
                validation_procedures=[
                    {
                        "name": "range",
                        "description": "Check if within range",
                        "kwargs": {"min": 50.0, "max": 150.0}
                    }
                ]
            )
        )

    def test_name_in_python(self) -> None:
        """Test the name_in_python property."""
        self.assertEqual(self.variable_ordinal.name_in_python, "test_status")
        self.assertEqual(self.variable_discrete.name_in_python, "number_of_errors")
        
        # Test with multi-word name
        variable = Variable(
            name="Multi Word Variable Name",
            description="Test",
            statistical_type=StatisticalType.NOMINAL,
            unit="test"
        )
        self.assertEqual(variable.name_in_python, "multi_word_variable_name")

    def test_type_in_python(self) -> None:
        """Test the type_in_python property."""
        self.assertEqual(self.variable_ordinal.type_in_python, str)
        self.assertEqual(self.variable_discrete.type_in_python, int)
        self.assertEqual(self.variable_with_expected.type_in_python, float)


if __name__ == "__main__":
    unittest.main()