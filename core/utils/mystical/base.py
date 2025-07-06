"""
Base Mystical System Utilities
Common functionality for all mystical systems
"""

import logging
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path
from ..data.validation import ValidationResult, validate_required_fields
from ..custom_logging import get_mystical_logger

@dataclass
class MysticalSystemConfig:
    """Configuration for a mystical system"""
    name: str
    data_path: Path
    cache_enabled: bool = True
    validation_enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CorrespondenceMap:
    """Mapping of correspondences between mystical systems"""
    source_system: str
    target_system: str
    mappings: Dict[str, Any]
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)

class MysticalSystemBase:
    """Base class for all mystical systems"""
    
    def __init__(self, config: MysticalSystemConfig):
        """Initialize the mystical system"""
        self.config = config
        self.logger = get_mystical_logger(config.name)
        
        # Validate configuration
        if config.validation_enabled:
            self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate system configuration"""
        result = validate_required_fields(
            data=self.config.__dict__,
            required_fields=['name', 'data_path']
        )
        
        if not result.is_valid:
            raise ValueError(f"Invalid configuration: {', '.join(result.errors)}")
    
    def calculate_correspondences(self, target_system: str,
                               source_data: Any) -> CorrespondenceMap:
        """Calculate correspondences with another mystical system"""
        self.logger.info(f"Calculating correspondences with {target_system}")
        
        try:
            # Implement in derived classes
            raise NotImplementedError("Must be implemented by derived class")
            
        except Exception as e:
            self.logger.error(f"Failed to calculate correspondences: {str(e)}")
            raise
    
    def validate_input(self, data: Any) -> ValidationResult:
        """Validate input data for the mystical system"""
        self.logger.info("Validating input data")
        
        try:
            # Implement in derived classes
            raise NotImplementedError("Must be implemented by derived class")
            
        except Exception as e:
            self.logger.error(f"Input validation failed: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=[str(e)]
            )
    
    def format_output(self, data: Any) -> Any:
        """Format output data from the mystical system"""
        self.logger.info("Formatting output data")
        
        try:
            # Implement in derived classes
            raise NotImplementedError("Must be implemented by derived class")
            
        except Exception as e:
            self.logger.error(f"Output formatting failed: {str(e)}")
            raise
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get system metadata"""
        return {
            "name": self.config.name,
            "data_path": str(self.config.data_path),
            "cache_enabled": self.config.cache_enabled,
            "validation_enabled": self.config.validation_enabled,
            **self.config.metadata
        }
    
    def clear_cache(self) -> None:
        """Clear system cache"""
        if self.config.cache_enabled:
            self.logger.info("Clearing system cache")
            # Implement cache clearing in derived classes
            pass 

@dataclass
class MysticalAttribute:
    """A mystical attribute with a name, value, and optional metadata"""
    name: str
    value: Any
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MysticalRelationship:
    """A relationship between mystical entities"""
    entity_id: str
    relationship_type: str
    strength: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate relationship strength"""
        if not 0 <= self.strength <= 1:
            raise ValueError("Relationship strength must be between 0 and 1")

@dataclass
class MysticalEntity:
    """A mystical entity with attributes and relationships"""
    id: str
    name: str
    system_id: str
    attributes: Dict[str, MysticalAttribute] = field(default_factory=dict)
    relationships: List[MysticalRelationship] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_attribute(self, name: str) -> Optional[MysticalAttribute]:
        """Get an attribute by name"""
        return self.attributes.get(name)
    
    def set_attribute(self, name: str, attribute: MysticalAttribute):
        """Set an attribute"""
        self.attributes[name] = attribute
    
    def add_relationship(self, relationship: MysticalRelationship):
        """Add a relationship to another entity"""
        self.relationships.append(relationship)

@dataclass
class MysticalSystem:
    """A mystical system containing entities and their relationships"""
    id: str
    name: str
    description: str = ""
    entities: Dict[str, MysticalEntity] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_entity(self, entity: MysticalEntity):
        """Add an entity to the system"""
        if entity.system_id != self.id:
            raise ValueError(f"Entity {entity.id} belongs to system {entity.system_id}, not {self.id}")
        self.entities[entity.id] = entity
    
    def get_entity(self, entity_id: str) -> Optional[MysticalEntity]:
        """Get an entity by ID"""
        return self.entities.get(entity_id)
    
    def remove_entity(self, entity_id: str):
        """Remove an entity from the system"""
        if entity_id in self.entities:
            del self.entities[entity_id]

class MysticalSystemRegistry:
    """Registry for mystical systems"""
    def __init__(self):
        self.systems: Dict[str, MysticalSystem] = {}
        self.logger = get_mystical_logger("system_registry")
    
    def register_system(self, system: MysticalSystem):
        """Register a mystical system"""
        if not system.id:
            raise ValueError("System ID cannot be empty")
        if system.id in self.systems:
            raise ValueError(f"System {system.id} is already registered")
        self.systems[system.id] = system
        self.logger.info(f"Registered system {system.id}")
    
    def get_system(self, system_id: str) -> MysticalSystem:
        """Get a system by ID"""
        if not system_id:
            raise ValueError("System ID cannot be empty")
        if system_id not in self.systems:
            raise KeyError(f"System {system_id} is not registered")
        return self.systems[system_id]
    
    def deregister_system(self, system_id: str):
        """Remove a system from the registry"""
        if not system_id:
            raise ValueError("System ID cannot be empty")
        if system_id not in self.systems:
            raise KeyError(f"System {system_id} is not registered")
        del self.systems[system_id]
        self.logger.info(f"Deregistered system {system_id}")

# Export all classes
__all__ = [
    'MysticalAttribute',
    'MysticalRelationship',
    'MysticalEntity',
    'MysticalSystem',
    'MysticalSystemRegistry'
] 