from typing import Any, Optional


from pydantic import  BaseModel, Field


class ValidationProcedure(BaseModel):
    """
    Defines a procedure for validating expected values against actual values.
    NOTE: The purpose of this class is to provide a structure for validation procedures, not an implementation.
    
    Attributes:
        name: Name of the validation procedure
        description: Description of what the procedure does
        kwargs: Additional key-word arguments for the procedure
        steps: List of steps to needed to make the procedure.
        condition: Optional condition expression for when this validation procedure should be applied
        
    Example condition expressions:
        - "input_type == 'string'"
        - "value > 10"
        - "is_numeric == True"
    """
    name:           str            = Field(description="Name of the validation procedure")
    description:    str            = Field(description="Description of what the procedure does")
    steps:          list[str]      = Field(default=[], description="List of steps to needed to make the procedure.")
    kwargs:         Optional[dict[str, Any]] = Field(default=None, description="Additional key-word arguments for the procedure")
    condition:      Optional[str]  = Field(default=None, description="Condition expression for when this procedure should be applied")
