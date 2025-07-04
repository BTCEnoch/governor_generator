from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class MysticalProfile:
    """Standard format all mystical systems must produce"""
    system_name: str                    # "tarot", "numerology", etc.
    governor_name: str                  # Governor being profiled  
    primary_influences: List[str]       # Main influences from this system
    secondary_influences: List[str]     # Supporting influences
    personality_modifiers: Dict[str, float]  # Trait modifications
    storyline_themes: List[str]         # Themes for story enhancement
    symbolic_elements: List[str]        # Symbols, archetypes, etc.
    conflict_sources: List[str]         # Sources of conflict
    growth_paths: List[str]             # Character development directions
    metadata: Dict[str, Any]            # System-specific extra data

class BaseMysticalSystem(ABC):
    """Base class that all mystical systems must implement"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.database = self._load_database()
    
    @abstractmethod
    def generate_profile(self, governor_data: Dict) -> MysticalProfile:
        """Generate mystical profile for a governor"""
        pass
    
    @abstractmethod  
    def get_system_info(self) -> Dict[str, Any]:
        """Return system metadata and capabilities"""
        pass
    
    @abstractmethod
    def validate_profile(self, profile: MysticalProfile) -> bool:
        """Validate generated profile meets system standards"""
        pass
    
    def _load_database(self):
        """Load system-specific database - override in subclasses"""
        return None
