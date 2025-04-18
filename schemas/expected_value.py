

from typing import Any, List, Optional


from pydantic import BaseModel, Field


from .validation_procedure import ValidationProcedure


class ParameterExpectedValue(BaseModel):
    """
    Defines an expected value for a specific parameter input.

    Attributes:
        input: The input value this expected value corresponds to.
        expected: The expected result for this input.
        description: Optional description of the expected behavior.
    """
    input: Any = Field(..., description="The input value this expected output corresponds to.")
    expected: Any = Field(..., description="The expected output value.")
    description: Optional[str] = Field(None, description="Description of this expected behavior.")

class ExpectedValue(BaseModel):
    """
    Defines expected values for dependent variables with validation.

    Attributes:
        value: The expected value or range (used for non-parametrized tests)
        values: List of expected values for parametrized tests
        validation_procedures: Method or methods used to validate actual results
    """
    value: Optional[Any] = Field(None, description="The expected value for non-parametrized tests")
    values: Optional[List[ParameterExpectedValue]] = Field(None, description="Expected values for parametrized tests")
    validation_procedures: Optional[List[ValidationProcedure]] = Field(None, description="Methods to validate results")

