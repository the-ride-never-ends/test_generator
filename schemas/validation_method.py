import asyncio
from datetime import datetime
import inspect
import importlib
from pathlib import Path
from typing import Annotated as Annot, Any, Callable, Optional
from jinja2 import Environment, FileSystemLoader, Template


from pydantic import AfterValidator as AV, BaseModel, computed_field, Field, PrivateAttr, ValidationError


from configs import ROOT_DIR


def _validate_validator_func(validator_func: Callable) -> Callable:


    # Check if validator_func is callable
    if not isinstance(validator_func, Callable):
        raise ValueError("validator_func must be a callable.")

    # Check if validator_func is a coroutine function
    if asyncio.iscoroutinefunction(validator_func):
        raise ValueError("validator_func must not be a coroutine function.")

    # Check if the function is implemented
    source = inspect.getsource(validator_func)
    if "NotImplementedError" in source:
        raise NotImplementedError("Validator function is not implemented. Please implement it before proceeding.")

    # Check if validator_func has the correct signature
    # 1. It must have no non-keyword arguments.
    params = inspect.signature(validator_func).parameters
    if "value" not in params or "expected_value" not in params:
        raise ValueError("validator_func must have 'value' and 'expected_value' as arguments.")

    # 2. It must not have any non-keyword arguments.
    if any(param.kind not in (inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.VAR_KEYWORD) for param in params.values()):
        raise ValueError("validator_func must not have any non-keyword arguments.")

    # 3. It must contain exceptions.
    if not any(isinstance(param.annotation, Exception) for param in params.values()):
        raise ValueError("validator_func must contain exceptions.")
    return validator_func


def _validate_validator_func_kwargs(validator_func: Callable, kwargs: Optional[dict[str, Any]] = None) -> None:
    params = inspect.signature(validator_func).parameters
    if kwargs:
        for key, value in kwargs.items():
            if key not in params.keys():
                raise ValueError(f"validator_func does not accept the keyword argument '{key}'.")
            if not isinstance(value, params[key].annotation):
                raise ValueError(f"Keyword argument '{key}' must be of type '{params[key].annotation}', not '{type(value)}'.")


def make_validator_fun_from_jinja2_template(name: str, description: str, steps: list[str], kwargs: Optional[dict[str, Any]]=None) -> Path:
    """
    Generates a validator function from a Jinja2 template.
    
    Args:
        name: Name of the validator function.
        description: Description of the validator function.
        kwargs: Optional dictionary of keyword arguments used to define the inputs to the template.

    Returns:
        Path to the generated validator function.

    """
    msg = f"Validator function file for '{name}' exists but is not implemented. Please implement it before proceeding."

    # Check if the function file already exists
    output_file_path = ROOT_DIR / 'utils' / 'schemas' / 'validator_functions' / f"validator_{name}.py"
    if output_file_path.exists():
        with open(output_file_path, "r") as f:
            function_file_str = f.read()
            # Check if the file contains a NotImplementedError


    # Load the template file
    template_path = Path(__file__).parent / "templates" / "validator_func_template.py"
    validator_template = Environment(loader=FileSystemLoader(template_path.parent)).get_template(template_path.name)

    # Render the template with the provided kwargs
    kwargs = kwargs or {}
    kwargs.update({
        'name': name,
        'description': description,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    rendered_content = validator_template.render(**kwargs)

    # Save the rendered content to a new Python file
    output_dir = Path(__file__).parent / "generated"
    output_dir.mkdir(exist_ok=True)

    with open(output_file_path, "w") as f:
        f.write(rendered_content)

    # Stop the program to force the user/llm to implement the function
    if "NotImplementedError" in function_file_str:
        # If the file exists but is not implemented, raise a NotImplementedError
        raise NotImplementedError(msg)
    else:
        # If the file exists and is implemented, return the existing file
        return output_file_path


class ValidationMethod(BaseModel):
    """
    Annot[Optional[Callable], AV(_validate_validator_func)]
    Defines a method for validating expected values against actual values.
    
    Attributes:
        name: Name of the validation method
        description: Description of what the validation does
        kwargs: Additional keyword arguments required by the validation method
    """
    name:           str            = Field(description="Name of the validation method")
    description:    str            = Field(description="Description of what the method does")
    steps:          list[str]      = Field(default=[], description="List of steps to be build the method")
    kwargs:         Optional[dict[str, Any]] = Field(default=None, description="Additional key-word arguments for the method")

    _validator_func: Callable = PrivateAttr(default=None)

    @computed_field # type: ignore[prop-decorator]
    @property
    def validator_func(self) -> Callable:
        """
        Callable function for validation. 
        This function must accept the expected value, actual value, and any kwargs as arguments.
        It must have no non-keyword arguments and must contain exceptions.
        """
        if not self.validator_func:
            # If no validator function is provided, make one from a jinja2 template
            make_validator_fun_from_jinja2_template(self.name, self.description, self.kwargs)

        validator_func_module = importlib.import_module(f"utils.schemas.validator_functions.validator_{self.name}")
        validator_func = getattr(validator_func_module, f"validate_{self.name}", None)
        if not validator_func:
            raise ImportError(f"Validator function 'validate_{self.name}' not found in module '{validator_func_module.__name__}'.")

        # Validate the validator function
        _validate_validator_func(self.validator_func)

        if self.kwargs:
            _validate_validator_func_kwargs(self.validator_func, self.kwargs)

        self._validator_func = validator_func

        return self._validator_func


    def validate_test_output_value(self, value, expected_value): # NOTE this overrides pydantic's old validation method.
        """
        Validates the expected value against the actual value using the specified validation method.
        
        Args:
            expected_value: The expected value
            actual_value: The actual value
            kwargs: Additional keyword arguments for the validation method
        """
        try:
            if self.kwargs:
                self.validator_func(value=value, expected_value=expected_value, **self.kwargs)
            self.validator_func(value=value, expected_value=value)
        except Exception as e:
            raise ValidationError(f"Validation failed for {self.name}: {e}")
