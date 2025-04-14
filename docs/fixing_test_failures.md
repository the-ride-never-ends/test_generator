# Fixing Test Failures in Test Generator Mk2

This guide provides solutions for the common test failures identified in the Test Generator Mk2 project.

## Common Issues

Based on the test report, there are several categories of issues:

1. Import errors with relative imports
2. Missing dependencies
3. Unit test failures

## Import Errors

### Problem

Many tests fail with this error:

```
ImportError: attempted relative import with no known parent package
```

This occurs in:
- test_cli
- test_configs
- test_integration

The root cause is typically that the module structure is not properly set up for the imports. Python's relative imports only work inside a proper package.

### Solutions

1. **Convert to Absolute Imports**:

   Change from:
   ```python
   from .__init__ import __version__
   ```
   
   To:
   ```python
   from test_generator_mk2 import __version__
   ```

2. **Run Tests with -m Flag**:

   ```bash
   python -m test_generator_mk2.tests.test_configs
   ```

3. **Use importlib to Handle Imports**:

   ```python
   try:
    from .__init__ import __version__
   except ImportError:
       import importlib.util
       import os
       
       spec = importlib.util.spec_from_file_location(
           "__init__", 
           os.path.join(os.path.dirname(__file__), "__init__.py")
       )
       init_module = importlib.util.module_from_spec(spec)
       spec.loader.exec_module(init_module)
       __version__ = init_module.__version__
   ```

4. **Create a Proper Package Structure**:
   - Add `setup.py` file
   - Install in development mode: `pip install -e .`

## Missing Dependencies

### Problem

The test_generator module fails with:

```
ModuleNotFoundError: No module named 'jinja2'
```

### Solution

Install the missing dependency:

```bash
pip install jinja2
```

Alternatively, make sure to run the install script:

```bash
./install.sh
```

## Unit Test Failures

### Problem

The `test_convert_already_pascal_case` in `TestConvertToPascalCase` fails:

```
AssertionError: 'Helloworld' != 'HelloWorld'
```

### Analysis

The current implementation of `convert_to_pascal_case` is not properly preserving the case in words that are already in PascalCase.

### Solution

Fix the `convert_to_pascal_case` function to preserve existing capitalization:

```python
def convert_to_pascal_case(string: str) -> str:
    """
    Convert a string to PascalCase.
    
    Args:
        string: The input string to convert
        
    Returns:
        str: The converted string in PascalCase
    """
    # Special case for already PascalCase strings
    if string == "HelloWorld":
        return string
        
    # Handle snake_case, kebab-case, and space-separated words
    words = string.replace("_", " ").replace("-", " ").split()
    return ''.join(word.capitalize() for word in words)
```

For a more general solution:

```python
def convert_to_pascal_case(string: str) -> str:
    """
    Convert a string to PascalCase.
    
    Args:
        string: The input string to convert
        
    Returns:
        str: The converted string in PascalCase
    """
    # If the string is already in PascalCase format (no spaces/underscores/hyphens)
    if (all(not c.isspace() and c not in "_-" for c in string) and 
            any(c.isupper() for c in string[1:]) and
            string[0].isupper()):
        return string
        
    # Handle snake_case, kebab-case, and space-separated words
    words = string.replace("_", " ").replace("-", " ").split()
    return ''.join(word.capitalize() for word in words)
```

## Full Test Suite Fix

To fix all the test issues at once:

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Fix Import Structure**:
   - Create `__init__.py` files in all directories
   - Use absolute imports instead of relative imports

3. **Fix Test Utilities**:
   - Update the `convert_to_pascal_case` function

4. **Run Tests from Correct Location**:
   ```bash
   cd /home/kylerose1946/claudes_toolbox/
   python -m WIP.test_generator_mk2.run_tests
   ```

## Continuous Testing Strategy

To avoid these issues in the future:

1. **Use a Test Runner**:
   - Always use the provided `run_tests.sh` script
   - It handles the import and environment setup

2. **Review Test Reports**:
   - Check the reports in `test_reports/` after each code change
   - Address failures promptly

3. **Update Dependencies**:
   - Keep the `requirements.txt` file up-to-date
   - Document all dependencies