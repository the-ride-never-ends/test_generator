
from typing import Any, Optional, List

from pydantic import BaseModel

from .validation_procedure import ValidationProcedure

class ExpectedValue(BaseModel):
    """
    Defines expected values for dependent variables with validation.
    
    Attributes:
        value: The expected value or range
        validation_procedures: Method or methods used to validate actual results
    """
    value: Any
    validation_procedures: Optional[List[ValidationProcedure]] = None

