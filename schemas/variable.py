from typing import Any, Optional, Type


from pydantic import BaseModel, computed_field, ValidationError


from .statistical_type import StatisticalType
from .expected_value import ExpectedValue, ValidationMethod
from utils.common.convert_to_snake_case import convert_to_snake_case


def _get_python_type_from_statistical_type(statistical_type: StatisticalType) -> Type:
    """
    Returns the python type of the variable based on the statistical type.
    """
    if isinstance(statistical_type, StatisticalType):
        if statistical_type == StatisticalType.ORDINAL or statistical_type == StatisticalType.NOMINAL:
            return str
        elif statistical_type == StatisticalType.DISCRETE:
            return int
        elif statistical_type == StatisticalType.CONTINOUS:
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
        - expected_value : The value a variable is expected to have pre-experiment. 
            This is only used by dependent variables. This can be a pydantic validation type.
    """
    name:             str
    description:      str
    statistical_type: StatisticalType
    unit:             str
    value:            Optional[Any] = None
    expected_value:   Optional[ExpectedValue] = None

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

    @computed_field # type: ignore[prop-decorator]
    @property
    def reject_null(self) -> bool:
        if self.value and self.expected_value:
            # Verify if the value rejects the null hypothesis
            try:
                if self.expected_value.validation_methods:
                    for method in self.expected_value.validation_methods:
                        method: ValidationMethod
                        


                        # Assuming each validation method has a validate method
                        if not method.validate_the_value(self.value):
                            raise ValidationError(f"Validation failed for {self.name}")
                else:
                    # If no validation methods are provided, use the default validation
                    if self.value != self.expected_value.value:
                        raise ValidationError(f"Value '{self.value}' does not match expected value '{self.expected_value.value}' for {self.name_in_python}")


                ExpectedValue(value=self.value, expected_value=self.expected_value)
                return True
            except ValidationError as e:
                print(f"Cannot reject null hypothesis for {self.name}: {e}")
                return False
        return False

