from typing import Any, List, Optional, Type, Union


from pydantic import BaseModel, computed_field, Field


from .statistical_type import StatisticalType
from .expected_value import ExpectedValue
from utils.common import convert_to_snake_case


class ParameterValue(BaseModel):
    """
    Represents a single parameter value for parametrized tests.

    Attributes:
        value: The actual value of the parameter
        description: Optional description of what this parameter value represents
    """
    value: Any
    description: Optional[str] = None


def _get_python_type_from_statistical_type(statistical_type: StatisticalType) -> Type:
    """
    Returns the python type of the variable based on the statistical type.
    """
    if isinstance(statistical_type, StatisticalType):
        if statistical_type == StatisticalType.ORDINAL or statistical_type == StatisticalType.NOMINAL:
            return str
        elif statistical_type == StatisticalType.DISCRETE:
            return int
        elif statistical_type == StatisticalType.CONTINUOUS:
            return float
        else:
            raise ValueError(f"Unknown statistical type: {statistical_type}")
    else:
        raise ValueError(f"Unknown statistical type: {statistical_type}")


class Variable(BaseModel):
    """
    A variable is any characteristic, number, or quantity that can be measured or counted.
    Age, sex, business income and expenses, country of birth, capital expenditure, class grades, eye color
    and vehicle type are examples of variables. It is called a variable because the value may vary between data units in a population,
    and may change in value over time.

    For example, 'income' is a variable that can vary between data units in a population
    (i.e. the people or businesses being studied may not have the same incomes) and can also
    vary over time for each data unit (i.e. income can go up or down).

    Attributes:
        - name : The plain English label for the variable. Ex: "Number of CPU Cores"
        - description : A plain English description of what the variable is. Ex: "The quantity of physical CPU cores."
        - statistical_type : The categorization of a variable. See StatisticalType class
        - unit : A plain English description of the measurement unit. Ex: "Cores"
        - name_in_python : The name of the variable in python. Ex: num_cpu_cores.
        - type_in_python : The variable's python type. Can be extended by different packages like Pandas or Numpy. Ex: int
        - value : The value a variable is assigned. For control variables, it is pre-assigned and fixed.
            For independent variables, it is pre-assigned for each test but is not fixed overall.
            For dependent variables, it is not pre-assigned or fixed.
        - values : For parametrized tests, a list of values to use for the variable.
        - expected_value : The value a variable is expected to have pre-experiment.
            This is only used by dependent variables. This can be a pydantic validation type.
    """
    name: str
    description: str
    statistical_type: StatisticalType
    unit: str
    value: Optional[Any] = None
    values: Optional[List[Union[ParameterValue, Any]]] = Field(default=None, description="For parametrized tests, a list of values to use")
    expected_value: Optional[ExpectedValue] = None

    @computed_field # type: ignore[prop-decorator]
    @property
    def type_in_python(self) -> Type:
        """
        Returns the python type of the variable.
        This is used to determine how to handle the variable in code.
        """
        return _get_python_type_from_statistical_type(self.statistical_type)

    @computed_field # type: ignore[prop-decorator]
    @property
    def name_in_python(self) -> str:
        """
        Returns the name of the variable in python.
        This is used to determine how to handle the variable in code.
        """
        return convert_to_snake_case(self.name)

