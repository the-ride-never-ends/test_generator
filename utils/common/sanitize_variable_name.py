def sanitize_variable_name(name: str) -> str:
    """
    Sanitizes a variable name to be a valid Python identifier.
    
    Args:
        name: The variable name to sanitize
        
    Returns:
        str: A valid Python identifier in snake_case
    """
    # Remove special characters and replace spaces with underscores
    sanitized = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
    sanitized = sanitized.replace(" ", "_").lower()
    
    # Ensure the name doesn't start with a digit
    if sanitized and sanitized[0].isdigit():
        sanitized = "var_" + sanitized
        
    # Ensure the name isn't empty
    if not sanitized:
        return "variable"
        
    return sanitized