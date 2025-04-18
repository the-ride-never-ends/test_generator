

from typing import List
from pydantic import BaseModel


class Method(BaseModel):
    """
    Describes the method used for testing.

    Attributes:
        steps: Ordered list of test procedure steps
        data_collection: How data is collected and recorded
        analysis_technique: Statistical methods applied to the data
    """
    steps: List[str]
    data_collection: str
    analysis_technique: str

    @property
    def comments(self) -> str:
        """
        Generate comments for the test method.

        Returns:
            str: Formatted test method comments with each step on its own line
        """
        return '\n\n'.join([f"# {step}" for step in self.steps])
