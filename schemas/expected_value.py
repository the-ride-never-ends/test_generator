

from typing import Any, Optional


from pydantic import BaseModel


from .validation_method import ValidationMethod


class ExpectedValue(BaseModel):
    """
    Defines expected values for dependent variables with validation.
    
    Attributes:
        value: The expected value or range
        validation_method: Method or methods used to validate actual results
    """
    value: Any
    validation_methods: Optional[list[ValidationMethod]] = None

