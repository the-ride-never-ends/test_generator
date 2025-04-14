import json
from typing import Any, Dict


def load_json_file(json_file_path: str) -> Dict[str, Any]:
    """
    Load a JSON file and return its contents.
    
    Args:
        json_file_path: Path to the JSON file
    Returns:
        Dict[str, Any]: Parsed JSON data
    """
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data