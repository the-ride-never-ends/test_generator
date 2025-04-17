import json
from pathlib import Path
from typing import Any, Dict, Union


def load_json_file(json_file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a JSON file and return its contents.
    
    Args:
        json_file_path: Path to the JSON file (string or Path object)
    Returns:
        Dict[str, Any]: Parsed JSON data
    """
    file_path = Path(json_file_path) if isinstance(json_file_path, str) else json_file_path
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Ensure we return a Dict[str, Any] as specified in the return type
    if not isinstance(data, dict):
        raise ValueError(f"JSON file {json_file_path} must contain a JSON object at the root level")
        
    return data