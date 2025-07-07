"""
Base Mystical System Utilities
Common functionality for all mystical systems
"""

import logging
from typing import Any, Dict, List, Optional, TypeVar, Generic
from dataclasses import dataclass, field
from pathlib import Path
from ..data.validation import ValidationResult

logger = logging.getLogger(__name__)

T = TypeVar('T')

@dataclass
class MysticalAttribute:
    """Base class for mystical attributes"""
    name: str
    value: Any
    description: Optional[str] = None
    correspondences: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MysticalEntity:
    """Base class for mystical entities"""
    id: str
    name: str
    attributes: List[MysticalAttribute] = field(default_factory=list)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

class MysticalSystem:
    """Base class for mystical systems"""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"mystical.{name}")
        
    def validate_input(self, data: Any) -> ValidationResult:
        """
        Validate input data for the mystical system
        
        Args:
            data: Input data to validate
            
        Returns:
            ValidationResult with validation status and errors
        """
        raise NotImplementedError("Subclasses must implement validate_input")
        
    def format_output(self, result: Any) -> Any:
        """
        Format output data from the mystical system
        
        Args:
            result: Raw output data
            
        Returns:
            Formatted output data
        """
        raise NotImplementedError("Subclasses must implement format_output")
        
    def calculate_correspondences(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate mystical correspondences
        
        Args:
            data: Input data
            
        Returns:
            Dictionary of calculated correspondences
        """
        raise NotImplementedError("Subclasses must implement calculate_correspondences")

class MysticalSystemRegistry:
    """Registry for mystical systems"""
    
    def __init__(self):
        self._systems: Dict[str, MysticalSystem] = {}
        self.logger = logging.getLogger(f"{__name__}.registry")
        
    def register(self, system: MysticalSystem) -> None:
        """Register a mystical system"""
        self.logger.info(f"Registering mystical system: {system.name}")
        self._systems[system.name] = system
        
    def get_system(self, name: str) -> Optional[MysticalSystem]:
        """Get a registered mystical system by name"""
        return self._systems.get(name)
        
    def list_systems(self) -> List[str]:
        """List all registered mystical systems"""
        return list(self._systems.keys()) 