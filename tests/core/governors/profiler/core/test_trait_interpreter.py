"""Tests for the trait interpreter system."""

import pytest
from unittest.mock import Mock, MagicMock
from core.governors.profiler.core.trait_interpreter import TraitInterpreter, TraitUnderstanding

@pytest.fixture
def trait_index_manager():
    """Create a mock trait index manager"""
    manager = Mock()
    
    # Set up test trait data
    test_traits = {
        "Form_1": {
            "name": "Geometric Form",
            "definition": "Manifests as perfect geometric shapes",
            "category": "form",
            "usage_context": "When geometric forms appear, they represent mathematical perfection",
            "ai_personality_impact": "Influences AI to express precise, structured patterns",
            "related_traits": ["Color_1", "Geometry_1"],
            "mystical_correspondences": {"element": "Earth"}
        },
        "Color_1": {
            "name": "Golden Light",
            "definition": "Radiates with divine golden luminescence",
            "category": "color",
            "usage_context": "When golden light manifests, it signifies divine wisdom",
            "ai_personality_impact": "Influences AI to express enlightened understanding",
            "related_traits": ["Form_1"],
            "mystical_correspondences": {"element": "Fire"}
        }
    }
    
    manager.get_trait_data = lambda name: test_traits.get(name)
    return manager

@pytest.fixture
def interpreter(trait_index_manager):
    """Create a trait interpreter instance"""
    return TraitInterpreter(trait_index_manager)

def test_decode_binary_traits(interpreter):
    """Test binary trait decoding"""
    # Create test binary data
    binary_data = bytearray(b'VIS1' + bytes([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    
    # Decode traits
    traits = interpreter._decode_binary_traits(binary_data)
    
    # Verify results
    assert "Form_1" in traits
    assert "Color_1" in traits
    assert len(traits) == 2

def test_get_trait_understanding(interpreter):
    """Test retrieving trait understanding"""
    # Get understanding for known trait
    understanding = interpreter._get_trait_understanding("Form_1")
    
    # Verify understanding
    assert understanding is not None
    assert understanding.name == "Geometric Form"
    assert understanding.category == "form"
    assert "geometric" in understanding.definition.lower()
    
    # Test caching
    cached = interpreter._get_trait_understanding("Form_1")
    assert cached is understanding  # Should return cached instance

def test_interpret_binary_traits(interpreter):
    """Test full binary trait interpretation"""
    # Create test binary data
    binary_data = bytearray(b'VIS1' + bytes([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    
    # Interpret traits
    understandings = interpreter.interpret_binary_traits(binary_data)
    
    # Verify results
    assert len(understandings) == 2
    assert any(u.name == "Geometric Form" for u in understandings)
    assert any(u.name == "Golden Light" for u in understandings)

def test_get_trait_relationships(interpreter):
    """Test retrieving trait relationships"""
    # Get relationships for Form_1
    relationships = interpreter.get_trait_relationships("Form_1")
    
    # Verify relationships
    assert "Color_1" in relationships.get("enhances", [])

def test_explain_trait_combination(interpreter):
    """Test generating trait combination explanations"""
    # Get explanation for Form_1 and Color_1
    explanation = interpreter.explain_trait_combination(["Form_1", "Color_1"])
    
    # Verify explanation content
    assert "Geometric Form" in explanation
    assert "Golden Light" in explanation
    assert "form" in explanation.lower()
    assert "color" in explanation.lower()
    assert "Context" in explanation

def test_invalid_trait_handling(interpreter):
    """Test handling of invalid traits"""
    # Try to get understanding for unknown trait
    understanding = interpreter._get_trait_understanding("NonexistentTrait")
    assert understanding is None
    
    # Try to get relationships for unknown trait
    relationships = interpreter.get_trait_relationships("NonexistentTrait")
    assert relationships == {} 