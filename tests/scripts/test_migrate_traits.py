"""
Tests for the trait migration script.
"""

import json
import pytest
from pathlib import Path
from scripts.migrate_traits import TraitMigrator

@pytest.fixture
def test_data_dir(tmp_path):
    """Create test data directory structure"""
    data_dir = tmp_path / "data" / "governors"
    indexes_dir = data_dir / "indexes"
    traits_dir = data_dir / "traits"
    
    # Create directories
    indexes_dir.mkdir(parents=True)
    for subdir in ["canonical", "enhanced", "mystical", "personality", "visual"]:
        (traits_dir / subdir).mkdir(parents=True)
    
    # Create test data files
    canonical_data = [{
        "aethyr_name": "LIL",
        "aethyr_number": 1,
        "correspondence": "The Universe (Saturn)",
        "governors": [{
            "name": "OCCODON",
            "region": "Egypt",
            "canonical_traits": {
                "personality": ["wise", "authoritative", "spiritual"],
                "domain": "Spiritual Ascension",
                "visual_motif": "Golden sage with radiant sigil",
                "letter_influence": ["Transformation", "Intuition", "Love"]
            }
        }]
    }]
    
    enhanced_data = {
        "wise": {
            "trait_name": "wise",
            "definition": "Deep understanding and insight",
            "source": "OCCODON",
            "correspondences": ["The Universe", "Saturn", "Egypt"],
            "practical_application": "Manifests through Golden sage with radiant sigil"
        }
    }
    
    mystical_data = {
        "OCCODON": {
            "element": "fire",
            "alignment": "lawful_good",
            "zodiac": "Leo",
            "tarot": "The Sun",
            "sephirot": "Tiphareth",
            "angel": "Michael",
            "number": 6
        }
    }
    
    personality_data = {
        "OCCODON": {
            "archetype": "Sage",
            "primary_traits": ["Wisdom", "Authority"],
            "secondary_traits": ["Patience", "Insight"],
            "teaching_style": "Direct Instruction",
            "approach": "Guiding",
            "tone": "Formal"
        }
    }
    
    # Write test data files
    with open(indexes_dir / "canonical_traits.json", "w") as f:
        json.dump(canonical_data, f)
    
    with open(indexes_dir / "trait_definitions.json", "w") as f:
        json.dump(enhanced_data, f)
    
    with open(indexes_dir / "mystical_traits.json", "w") as f:
        json.dump(mystical_data, f)
    
    with open(indexes_dir / "personality_traits.json", "w") as f:
        json.dump(personality_data, f)
    
    with open(indexes_dir / "VISUAL_TRAIT_INDEX.md", "w") as f:
        f.write("# Visual Trait Index\n\n## Form Types\n- ETHEREAL: Pure light and energy form")
    
    return data_dir

def test_migrate_governor(test_data_dir):
    """Test migration of a single governor's traits"""
    migrator = TraitMigrator()
    migrator.root_dir = test_data_dir
    migrator.indexes_dir = test_data_dir / "indexes"
    migrator.traits_dir = test_data_dir / "traits"
    
    # Run migration
    migrator.migrate_all_governors()
    
    # Check canonical traits
    with open(migrator.traits_dir / "canonical" / "occodon_canonical.json") as f:
        canonical = json.load(f)
        assert canonical["name"] == "OCCODON"
        assert canonical["aethyr"] == "LIL"
        assert canonical["domain"] == "Spiritual Ascension"
    
    # Check enhanced traits
    with open(migrator.traits_dir / "enhanced" / "occodon_enhanced.json") as f:
        enhanced = json.load(f)
        assert "wise" in enhanced
        assert enhanced["wise"]["definition"] == "Deep understanding and insight"
    
    # Check mystical traits
    with open(migrator.traits_dir / "mystical" / "occodon_mystical.json") as f:
        mystical = json.load(f)
        assert mystical["element"] == "fire"
        assert mystical["zodiac"] == "Leo"
    
    # Check personality traits
    with open(migrator.traits_dir / "personality" / "occodon_personality.json") as f:
        personality = json.load(f)
        assert personality["archetype"] == "Sage"
        assert "Wisdom" in personality["primary_traits"]
    
    # Check visual traits
    with open(migrator.traits_dir / "visual" / "occodon_visual.json") as f:
        visual = json.load(f)
        assert visual["form_type"] == "ETHEREAL"
        assert visual["color_scheme"] == "PRISMATIC"

def test_migrate_missing_governor(test_data_dir):
    """Test migration with missing governor data"""
    migrator = TraitMigrator()
    migrator.root_dir = test_data_dir
    migrator.indexes_dir = test_data_dir / "indexes"
    migrator.traits_dir = test_data_dir / "traits"
    
    # Create empty data files
    for file_name in ["canonical_traits.json", "trait_definitions.json",
                     "mystical_traits.json", "personality_traits.json"]:
        with open(migrator.indexes_dir / file_name, "w") as f:
            json.dump({}, f)
    
    # Run migration
    migrator.migrate_all_governors()
    
    # Check no files were created
    assert not list(Path(migrator.traits_dir / "canonical").glob("*.json"))
    assert not list(Path(migrator.traits_dir / "enhanced").glob("*.json"))
    assert not list(Path(migrator.traits_dir / "mystical").glob("*.json"))
    assert not list(Path(migrator.traits_dir / "personality").glob("*.json"))
    assert not list(Path(migrator.traits_dir / "visual").glob("*.json")) 