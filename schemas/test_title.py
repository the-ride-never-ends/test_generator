from typing import Self


from pydantic import BaseModel, Field, model_validator


class TestTitle(BaseModel):
    test_title: str= Field(default="This is a generic title", description="Title of the test")

    @model_validator(mode='after')
    def convert_to_pascal_case(self) -> Self:
        """
        Convert the test title to PascalCase.
        """
        words = self.test_title.split()
        self.test_title = ''.join(word.capitalize() for word in words)
        return self