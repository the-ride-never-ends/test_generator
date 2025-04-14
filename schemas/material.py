from typing import Any, Dict, Optional


from pydantic import BaseModel


class Material(BaseModel):
    """
    Defines materials used in testing.
    This represents a catch-all for the various methods, fixtures, libraries, and other errata that go into test creation.
    
    Attributes:
        name: Name of the material
        description: Description of the material
        type: Type of material (fixture, library, file, directory, etc.)
        version: Version or model
        configuration: Configuration details
        source: Where the material was obtained
    """
    name: str
    description: str
    type: str  # software, hardware, library, etc.
    version: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    source: Optional[str] = None