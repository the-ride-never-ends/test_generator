from typing import Any, Optional


from pydantic import BaseModel, Field


class ValidationMethod(BaseModel):
    """
    Defines a method for validating expected values against actual values.
    
    Attributes:
        name: Name of the validation method
        description: Description of what the validation does
        kwargs: Additional keyword arguments required by the validation method
    """
    name:        str            = Field(description="Name of the validation method")
    description: str            = Field(description="Description of what the validation does")
    kwargs:      dict[str, Any] = Field(default_factory=dict, description="Additional arguments for the validation method")


class ExpectedValue(BaseModel):
    """
    Defines expected values for dependent variables with validation.
    
    Attributes:
        value: The expected value or range
        validation_method: Method or methods used to validate actual results
    """
    value: Any
    validation_methods: Optional[list[ValidationMethod]]

