"""
Tests for the Governor Trait Generation System
"""

import pytest
from pathlib import Path
import json
from datetime import datetime

from core.governors.traits.generator import TraitGenerator
from core.governors.traits.schemas.core_schemas import (
    TraitIndex,
    TraitEntry,
    TraitMetadata
)
from core.governors.traits.schemas.trait_schemas import (
    ElementType,
    AlignmentType,
    CanonicalTraits,
    GovernorTraits
)

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory for test data"""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return data_dir

@pytest.fixture
def trait_index(test_data_dir):
    """Create a sample trait index"""
    traits = [
        TraitEntry(
            id="TRAIT001",
            name="Wisdom",
            definition="Deep understanding and insight",
            category="Mental",
            metadata=TraitMetadata(source="Test"),
            subcategory="Knowledge",
            correspondences=["Mercury", "Air"]
        ),
        TraitEntry(
            id="TRAIT002",
            name="Strength",
            definition="Inner and outer power",
            category="Physical",
            metadata=TraitMetadata(source="Test"),
            subcategory="Power",
            correspondences=["Mars", "Fire"]
        )
    ]
    
    index = TraitIndex(
        schema_version="1.0.0",
        last_updated=datetime.now(),
        entries=traits
    )
    
    # Save to file
    index_file = test_data_dir / "trait_index.json"
    with open(index_file, 'w') as f:
        json.dump({
            "schema_version": index.schema_version,
            "last_updated": index.last_updated.isoformat(),
            "entries": [
                {
                    "id": t.id,
                    "name": t.name,
                    "definition": t.definition,
                    "category": t.category,
                    "metadata": {"source": t.metadata.source},
                    "subcategory": t.subcategory,
                    "correspondences": t.correspondences
                }
                for t in traits
            ]
        }, f)
    
    return index

@pytest.fixture
def correspondences(test_data_dir):
    """Create sample correspondence data"""
    data = {
        "regions": ["Celestial", "Terrestrial", "Infernal"],
        "correspondences": ["Light", "Shadow", "Balance"],
        "elements": ["Fire", "Water", "Air", "Earth", "Spirit"]
    }
    
    # Save to file
    corresp_file = test_data_dir / "correspondences.json"
    with open(corresp_file, 'w') as f:
        json.dump(data, f)
    
    return data

@pytest.fixture
def trait_generator(test_data_dir, trait_index, correspondences):
    """Create a TraitGenerator instance"""
    return TraitGenerator(test_data_dir)

def test_generate_governor_traits(trait_generator):
    """Test generating a complete set of governor traits"""
    traits = trait_generator.generate_governor_traits(
        governor_id="TEST001",
        governor_number=1
    )
    
    assert isinstance(traits, GovernorTraits)
    assert traits.governor_id == "TEST001"
    assert traits.governor_number == 1
    assert traits.canonical.aethyr_number == 1
    assert traits.canonical.personality
    assert traits.enhanced
    assert traits.mystical.element in ElementType
    assert traits.mystical.alignment in AlignmentType

def test_generate_with_seed_data(trait_generator):
    """Test generating traits with seed data"""
    seed_data = {
        'canonical': {
            'name': "Test Governor",
            'aethyr': "LIL01",
            'aethyr_number': 1,
            'region': "Celestial",
            'correspondence': "Light",
            'personality': ["Wisdom"],
            'domain': "Knowledge",
            'visual_motif': "Scrolls",
            'letter_influence': ["A"]
        }
    }
    
    traits = trait_generator.generate_governor_traits(
        governor_id="TEST002",
        governor_number=2,
        seed_data=seed_data
    )
    
    assert traits.canonical.name == "Test Governor"
    assert traits.canonical.personality == ["Wisdom"]

def test_trait_consistency(trait_generator):
    """Test that traits are consistent for the same governor"""
    traits1 = trait_generator.generate_governor_traits(
        governor_id="TEST003",
        governor_number=3
    )
    
    traits2 = trait_generator.generate_governor_traits(
        governor_id="TEST003",
        governor_number=3
    )
    
    # Core traits should be consistent
    assert traits1.canonical.aethyr == traits2.canonical.aethyr
    assert traits1.mystical.zodiac == traits2.mystical.zodiac
    assert traits1.mystical.sephirot == traits2.mystical.sephirot

def test_unique_traits(trait_generator):
    """Test that different governors get different traits"""
    traits1 = trait_generator.generate_governor_traits(
        governor_id="TEST004",
        governor_number=4
    )
    
    traits2 = trait_generator.generate_governor_traits(
        governor_id="TEST005",
        governor_number=5
    )
    
    # Should have different values
    assert traits1.canonical.aethyr != traits2.canonical.aethyr
    assert traits1.mystical.zodiac != traits2.mystical.zodiac
    assert traits1.personality.archetype != traits2.personality.archetype

def test_bitcoin_entropy_influence(trait_generator):
    """Test that Bitcoin entropy influences trait generation"""
    # Generate traits with different entropy
    traits1 = trait_generator.generate_governor_traits(
        governor_id="TEST006",
        governor_number=6
    )
    
    # Mock different entropy by using a different ID
    traits2 = trait_generator.generate_governor_traits(
        governor_id="TEST007",
        governor_number=6  # Same number, different ID
    )
    
    # Core numerical traits should be same (based on number)
    assert traits1.canonical.aethyr_number == traits2.canonical.aethyr_number
    
    # But entropy-influenced traits should differ
    assert traits1.mystical.element != traits2.mystical.element or \
           traits1.mystical.alignment != traits2.mystical.alignment 