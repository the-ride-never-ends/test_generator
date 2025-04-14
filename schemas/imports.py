

from pydantic import BaseModel


class Imports(BaseModel):
    """
    Imports used in the test method.
    
    Attributes:
        name: Name of the library
        import_funcs: Functions to import from the library
    Propterties:
        import_string: Formatted import statement
    """
    name: str
    import_funcs: list[str] = None

    @property
    def import_string(self):
        """
        Format the import statement for the template.
        
        Returns:
            str: Properly formatted import statement
        """
        if self.import_funcs:
            return f"from {self.name} import {', '.join(self.import_funcs)}"
        return f"import {self.name}"
