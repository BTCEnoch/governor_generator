"""
Tests for mystical system utilities
"""

import pytest
from typing import Dict, Any
from core.utils.mystical.base import (
    MysticalAttribute,
    MysticalEntity,
    MysticalSystem,
    MysticalSystemRegistry
)
from core.utils.data.validation import ValidationResult

# Test data
@pytest.fixture
def sample_attribute():
    """Sample mystical attribute"""
    return MysticalAttribute(
        name="wisdom",
        value=42,
        description="Level of mystical wisdom",
        correspondences={"planet": "Jupiter", "element": "Air"},
        metadata={"source": "ancient texts"}
    )

@pytest.fixture
def sample_entity():
    """Sample mystical entity"""
    return MysticalEntity(
        id="test_entity_001",
        name="Test Entity",
        attributes=[
            MysticalAttribute(name="power", value=100),
            MysticalAttribute(name="wisdom", value=75)
        ],
        relationships={"allies": ["entity_002", "entity_003"]},
        metadata={"type": "test", "version": "1.0"}
    )

# Test implementation
class TestMysticalSystem(MysticalSystem):
    """Test mystical system implementation"""
    
    def validate_input(self, data: Any) -> ValidationResult:
        if not isinstance(data, dict):
            return ValidationResult(
                is_valid=False,
                errors=["Input must be a dictionary"]
            )
        return ValidationResult(is_valid=True, data=data)
        
    def format_output(self, result: Any) -> Any:
        if isinstance(result, dict):
            return {k.upper(): v for k, v in result.items()}
        return result
        
    def calculate_correspondences(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "element": "test_element",
            "planet": "test_planet",
            "number": 42
        }

# Mystical attribute tests
@pytest.mark.mystical
class TestMysticalAttribute:
    def test_attribute_creation(self, sample_attribute):
        """Test mystical attribute creation"""
        assert sample_attribute.name == "wisdom"
        assert sample_attribute.value == 42
        assert sample_attribute.description == "Level of mystical wisdom"
        assert sample_attribute.correspondences["planet"] == "Jupiter"
        assert sample_attribute.metadata["source"] == "ancient texts"
        
    def test_attribute_defaults(self):
        """Test mystical attribute defaults"""
        attr = MysticalAttribute(name="test", value=1)
        assert attr.description is None
        assert attr.correspondences == {}
        assert attr.metadata == {}

# Mystical entity tests
@pytest.mark.mystical
class TestMysticalEntity:
    def test_entity_creation(self, sample_entity):
        """Test mystical entity creation"""
        assert sample_entity.id == "test_entity_001"
        assert sample_entity.name == "Test Entity"
        assert len(sample_entity.attributes) == 2
        assert "allies" in sample_entity.relationships
        assert sample_entity.metadata["type"] == "test"
        
    def test_entity_defaults(self):
        """Test mystical entity defaults"""
        entity = MysticalEntity(id="test", name="Test")
        assert entity.attributes == []
        assert entity.relationships == {}
        assert entity.metadata == {}
        
    def test_entity_attributes(self, sample_entity):
        """Test entity attribute access"""
        power_attr = next(
            attr for attr in sample_entity.attributes 
            if attr.name == "power"
        )
        assert power_attr.value == 100

# Mystical system tests
@pytest.mark.mystical
class TestMysticalSystem:
    def test_system_creation(self):
        """Test mystical system creation"""
        system = TestMysticalSystem("test_system")
        assert system.name == "test_system"
        assert system.config == {}
        
    def test_system_validation(self):
        """Test input validation"""
        system = TestMysticalSystem("test_system")
        
        # Valid input
        result = system.validate_input({"test": "data"})
        assert result.is_valid
        assert result.data == {"test": "data"}
        
        # Invalid input
        result = system.validate_input("not a dict")
        assert not result.is_valid
        assert "Input must be a dictionary" in result.errors
        
    def test_system_output_formatting(self):
        """Test output formatting"""
        system = TestMysticalSystem("test_system")
        result = system.format_output({"test": "data"})
        assert result == {"TEST": "data"}
        
    def test_system_correspondences(self):
        """Test correspondence calculation"""
        system = TestMysticalSystem("test_system")
        result = system.calculate_correspondences({})
        assert result["element"] == "test_element"
        assert result["planet"] == "test_planet"
        assert result["number"] == 42

# Mystical system registry tests
@pytest.mark.mystical
class TestMysticalSystemRegistry:
    def test_registry_creation(self):
        """Test registry creation"""
        registry = MysticalSystemRegistry()
        assert registry.list_systems() == []
        
    def test_system_registration(self):
        """Test system registration"""
        registry = MysticalSystemRegistry()
        system = TestMysticalSystem("test_system")
        
        registry.register(system)
        assert "test_system" in registry.list_systems()
        
    def test_system_retrieval(self):
        """Test system retrieval"""
        registry = MysticalSystemRegistry()
        system = TestMysticalSystem("test_system")
        
        registry.register(system)
        retrieved = registry.get_system("test_system")
        assert retrieved == system
        assert retrieved.name == "test_system"
        
    def test_nonexistent_system(self):
        """Test retrieval of nonexistent system"""
        registry = MysticalSystemRegistry()
        assert registry.get_system("nonexistent") is None 