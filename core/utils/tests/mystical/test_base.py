"""
Tests for mystical base utilities
"""

import pytest
from typing import Dict, Any
from core.utils.mystical.base import (
    MysticalSystem,
    MysticalEntity,
    MysticalAttribute,
    MysticalRelationship,
    MysticalSystemRegistry
)

@pytest.fixture
def sample_attribute():
    """Create a sample mystical attribute"""
    return MysticalAttribute(
        name="wisdom",
        value=42,
        description="Level of mystical wisdom",
        metadata={"source": "ancient texts"}
    )

@pytest.fixture
def sample_entity():
    """Create a sample mystical entity"""
    attributes = {
        "wisdom": MysticalAttribute(
            name="wisdom",
            value=42,
            description="Level of mystical wisdom"
        ),
        "power": MysticalAttribute(
            name="power",
            value=100,
            description="Mystical power level"
        )
    }
    return MysticalEntity(
        id="test_entity",
        name="Test Entity",
        system_id="test_system",
        attributes=attributes
    )

@pytest.fixture
def sample_system():
    """Create a sample mystical system"""
    return MysticalSystem(
        id="test_system",
        name="Test System",
        description="A test mystical system"
    )

def test_mystical_attribute():
    """Test mystical attribute functionality"""
    # Test basic attribute
    attr = MysticalAttribute(
        name="test",
        value="value",
        description="test description"
    )
    assert attr.name == "test"
    assert attr.value == "value"
    assert attr.description == "test description"
    assert attr.metadata == {}
    
    # Test with metadata
    attr = MysticalAttribute(
        name="test",
        value=42,
        description="test description",
        metadata={"source": "ancient texts"}
    )
    assert attr.metadata["source"] == "ancient texts"
    
    # Test value types
    numeric_attr = MysticalAttribute(name="numeric", value=42)
    assert isinstance(numeric_attr.value, int)
    
    string_attr = MysticalAttribute(name="string", value="test")
    assert isinstance(string_attr.value, str)
    
    dict_attr = MysticalAttribute(
        name="dict",
        value={"key": "value"},
        metadata={"type": "mapping"}
    )
    assert isinstance(dict_attr.value, dict)

def test_mystical_entity(sample_entity):
    """Test mystical entity functionality"""
    # Test basic properties
    assert sample_entity.id == "test_entity"
    assert sample_entity.name == "Test Entity"
    assert sample_entity.system_id == "test_system"
    
    # Test attributes
    assert len(sample_entity.attributes) == 2
    assert "wisdom" in sample_entity.attributes
    assert "power" in sample_entity.attributes
    
    # Test attribute access
    wisdom = sample_entity.get_attribute("wisdom")
    assert wisdom.value == 42
    
    # Test nonexistent attribute
    assert sample_entity.get_attribute("nonexistent") is None
    
    # Test attribute modification
    sample_entity.set_attribute(
        "wisdom",
        MysticalAttribute(name="wisdom", value=50)
    )
    assert sample_entity.get_attribute("wisdom").value == 50
    
    # Test new attribute addition
    new_attr = MysticalAttribute(
        name="intelligence",
        value=75,
        description="Mental acuity"
    )
    sample_entity.set_attribute("intelligence", new_attr)
    assert len(sample_entity.attributes) == 3
    assert sample_entity.get_attribute("intelligence").value == 75
    
    # Test relationships
    relationship = MysticalRelationship(
        entity_id="other_entity",
        relationship_type="teaches",
        strength=0.8
    )
    sample_entity.add_relationship(relationship)
    assert len(sample_entity.relationships) == 1
    assert sample_entity.relationships[0].entity_id == "other_entity"
    
    # Test multiple relationships
    another_rel = MysticalRelationship(
        entity_id="third_entity",
        relationship_type="learns_from",
        strength=0.6
    )
    sample_entity.add_relationship(another_rel)
    assert len(sample_entity.relationships) == 2
    assert sample_entity.relationships[1].entity_id == "third_entity"

def test_mystical_relationship():
    """Test mystical relationship functionality"""
    # Test basic relationship
    rel = MysticalRelationship(
        entity_id="test_entity",
        relationship_type="teaches",
        strength=0.8
    )
    assert rel.entity_id == "test_entity"
    assert rel.relationship_type == "teaches"
    assert rel.strength == 0.8
    assert rel.metadata == {}
    
    # Test with metadata
    rel = MysticalRelationship(
        entity_id="test_entity",
        relationship_type="teaches",
        strength=0.8,
        metadata={"source": "ancient records"}
    )
    assert rel.metadata["source"] == "ancient records"
    
    # Test strength validation
    with pytest.raises(ValueError):
        MysticalRelationship(
            entity_id="test",
            relationship_type="test",
            strength=1.5
        )
    
    with pytest.raises(ValueError):
        MysticalRelationship(
            entity_id="test",
            relationship_type="test",
            strength=-0.1
        )
    
    # Test boundary values
    rel = MysticalRelationship(
        entity_id="test",
        relationship_type="test",
        strength=0.0
    )
    assert rel.strength == 0.0
    
    rel = MysticalRelationship(
        entity_id="test",
        relationship_type="test",
        strength=1.0
    )
    assert rel.strength == 1.0

def test_mystical_system(sample_system):
    """Test mystical system functionality"""
    # Test basic properties
    assert sample_system.id == "test_system"
    assert sample_system.name == "Test System"
    assert sample_system.description == "A test mystical system"
    
    # Test entity management
    entity = MysticalEntity(
        id="test_entity",
        name="Test Entity",
        system_id=sample_system.id
    )
    sample_system.add_entity(entity)
    assert len(sample_system.entities) == 1
    assert "test_entity" in sample_system.entities
    
    # Test entity from different system
    other_entity = MysticalEntity(
        id="other_entity",
        name="Other Entity",
        system_id="other_system"
    )
    with pytest.raises(ValueError) as exc:
        sample_system.add_entity(other_entity)
    assert "belongs to system" in str(exc.value)
    
    # Test entity retrieval
    retrieved = sample_system.get_entity("test_entity")
    assert retrieved.id == "test_entity"
    assert retrieved.name == "Test Entity"
    
    # Test nonexistent entity retrieval
    assert sample_system.get_entity("nonexistent") is None
    
    # Test entity removal
    sample_system.remove_entity("test_entity")
    assert len(sample_system.entities) == 0
    
    # Test removing nonexistent entity (should not raise)
    sample_system.remove_entity("nonexistent")
    assert len(sample_system.entities) == 0

def test_mystical_system_registry():
    """Test mystical system registry functionality"""
    registry = MysticalSystemRegistry()
    
    # Test empty system ID validation
    with pytest.raises(ValueError) as exc:
        registry.register_system(MysticalSystem(id="", name="Invalid"))
    assert "System ID cannot be empty" in str(exc.value)
    
    # Test system registration
    system = MysticalSystem(
        id="test_system",
        name="Test System",
        description="A test mystical system"
    )
    registry.register_system(system)
    assert len(registry.systems) == 1
    assert "test_system" in registry.systems
    
    # Test duplicate registration
    with pytest.raises(ValueError) as exc:
        registry.register_system(system)
    assert "already registered" in str(exc.value)
    
    # Test system retrieval
    retrieved = registry.get_system("test_system")
    assert retrieved.id == "test_system"
    assert retrieved.name == "Test System"
    
    # Test empty ID retrieval
    with pytest.raises(ValueError) as exc:
        registry.get_system("")
    assert "System ID cannot be empty" in str(exc.value)
    
    # Test nonexistent system retrieval
    with pytest.raises(KeyError) as exc:
        registry.get_system("nonexistent")
    assert "not registered" in str(exc.value)
    
    # Test system deregistration
    registry.deregister_system("test_system")
    assert len(registry.systems) == 0
    
    # Test empty ID deregistration
    with pytest.raises(ValueError) as exc:
        registry.deregister_system("")
    assert "System ID cannot be empty" in str(exc.value)
    
    # Test nonexistent system deregistration
    with pytest.raises(KeyError) as exc:
        registry.deregister_system("nonexistent")
    assert "not registered" in str(exc.value) 