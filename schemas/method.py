

from pydantic import BaseModel


class Method(BaseModel):
    """
    Describes the method used for testing.
    
    Attributes:
        steps: Ordered list of test procedure steps
        data_collection: How data is collected and recorded
        analysis_technique: Statistical methods applied to the data
    """
    steps: list[str]
    data_collection: str
    analysis_technique: str

    @property
    def comments(self):
        """
        Generate comments for the test method.
        """
        return '\n\n'.join([f"# {step}" for step in self.steps])

