def convert_to_pascal_case(string: str) -> str:
    """
    Convert a string to PascalCase.
    
    Args:
        string: The input string to convert
        
    Returns:
        str: The converted string in PascalCase
    """
    # If the string is already in PascalCase format with multiple words (e.g., HelloWorld)
    if (all(not c.isspace() and c not in "_-" for c in string) and 
            any(c.isupper() for c in string[1:]) and
            string[0].isupper()):
        return string
        
    # Handle snake_case, kebab-case, and space-separated words
    words = string.replace("_", " ").replace("-", " ").split()
    return ''.join(word.capitalize() for word in words)