def convert_to_snake_case(name: str) -> str:
    """
    Converts a given name to snake_case.

    Args:
        name: The name to convert.

    Returns:
        str: The converted name in snake_case.
    """
    return name.replace(" ", "_").lower()
