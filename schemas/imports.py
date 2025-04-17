
from typing import Callable, List, Optional
from pydantic import BaseModel, Field


class Imports(BaseModel):
    """
    Imports used in the test method.
    
    Attributes:
        name: Name of the library
        import_funcs: Functions to import from the library
    Properties:
        import_string: Formatted import statement
    """
    name: str
    import_funcs: Optional[List[str]] = Field(default_factory=lambda: [])

    @property
    def import_string(self) -> str:
        """
        Format the import statement for the template.
        
        Returns:
            str: Properly formatted import statement
        """
        if self.import_funcs and len(self.import_funcs) > 0:
            return f"from {self.name} import {', '.join(self.import_funcs)}"
        return f"import {self.name}"
