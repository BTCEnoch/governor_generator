"""
Tests for the unified trait loading system
"""

import json
import pytest
from pathlib import Path
from datetime import datetime

from core.governors.traits import (
    TraitLoader,
    GovernorTraits,
    CanonicalTraits,
    EnhancedTraits
)

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary test data directory"""
    data_dir = tmp_path / "test_governors" / "traits"
    canonical_dir = data_dir / "canonical"
    enhanced_dir = data_dir / "enhanced"
    
    # Create directories
    canonical_dir.mkdir(parents=True)
    enhanced_dir.mkdir(parents=True)
    
    # Create test canonical traits
    canonical_traits = {
        "name": "OCCODON",
        "aethyr": "LIL",
        "aethyr_number": 1,
        "region": "Egypt",
        "correspondence": "The Universe (Saturn)",
        "personality": ["wise", "authoritative", "spiritual"],
        "domain": "Spiritual Ascension",
        "visual_motif": "Golden sage with radiant sigil",
        "letter_influence": ["A", "B", "C"]
    }
    
    with open(canonical_dir / "occodon_canonical.json", "w") as f:
        json.dump(canonical_traits, f)
    
    # Create test enhanced traits
    enhanced_traits = {
        "wise": {
            "name": "wise",
            "definition": "Deep understanding of spiritual truths",
            "category": "virtues",
            "usage_context": "Teaching and guidance",
            "ai_personality_impact": "Provides thoughtful, considered responses",
            "related_traits": ["spiritual", "authoritative"],
            "mystical_correspondences": "Saturn, LIL Aethyr"
        }
    }
    
    with open(enhanced_dir / "occodon_enhanced.json", "w") as f:
        json.dump(enhanced_traits, f)
    
    return data_dir

def test_trait_loader_initialization(test_data_dir):
    """Test trait loader initialization"""
    loader = TraitLoader(test_data_dir)
    assert loader.data_root == test_data_dir
    assert loader.canonical_path.exists()
    assert loader.enhanced_path.exists()

def test_load_canonical_traits(test_data_dir):
    """Test loading canonical traits"""
    loader = TraitLoader(test_data_dir)
    traits = loader._load_canonical_traits("OCCODON")
    
    assert traits is not None
    assert traits.name == "OCCODON"
    assert traits.aethyr == "LIL"
    assert traits.domain == "Spiritual Ascension"
    assert "wise" in traits.personality

def test_load_enhanced_traits(test_data_dir):
    """Test loading enhanced traits"""
    loader = TraitLoader(test_data_dir)
    traits = loader._load_enhanced_traits("OCCODON")
    
    assert traits is not None
    assert "wise" in traits
    assert traits["wise"].category == "virtues"
    assert traits["wise"].mystical_correspondences is not None
    assert "Saturn" in traits["wise"].mystical_correspondences

def test_load_all_traits(test_data_dir):
    """Test loading all traits for a governor"""
    loader = TraitLoader(test_data_dir)
    traits = loader.load_all_traits("OCCODON", 1)
    
    assert traits is not None
    assert traits.governor_id == "OCCODON"
    assert traits.governor_number == 1
    assert traits.canonical.name == "OCCODON"
    assert traits.canonical.aethyr == "LIL"
    assert traits.enhanced["wise"].category == "virtues"
    assert traits.last_updated is not None

def test_missing_canonical_traits(test_data_dir):
    """Test handling missing canonical traits"""
    loader = TraitLoader(test_data_dir)
    traits = loader.load_all_traits("NONEXISTENT", 99)
    assert traits is None

def test_invalid_canonical_traits(test_data_dir):
    """Test handling invalid canonical traits"""
    # Create invalid canonical traits
    invalid_traits = {
        "name": "INVALID",
        # Missing required fields
    }
    
    with open(test_data_dir / "canonical" / "invalid_canonical.json", "w") as f:
        json.dump(invalid_traits, f)
    
    loader = TraitLoader(test_data_dir)
    traits = loader.load_all_traits("INVALID", 99)
    assert traits is None

def test_trait_validation(test_data_dir):
    """Test trait validation"""
    loader = TraitLoader(test_data_dir)
    traits = loader.load_all_traits("OCCODON", 1)
    
    assert traits is not None
    assert traits.validate()
    
    # Test validation with mismatched governor ID
    traits.governor_id = "WRONG"
    assert not traits.validate() 