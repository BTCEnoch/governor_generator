"""
Tests for the knowledge mapper.
"""

import json
import time
import pytest
from pathlib import Path
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import MagicMock

from core.governors.traits.knowledge_mapper import KnowledgeMapper, TraditionKnowledge, GovernorKnowledge
from core.governors.traits.schemas.trait_schemas import ElementType, GovernorTraits

@pytest.fixture
def test_data_dir(tmp_path):
    """Create test data directory structure"""
    data_dir = tmp_path
    
    # Create knowledge directories
    knowledge_dir = data_dir / "knowledge"
    archives_dir = knowledge_dir / "archives" / "governor_archives"
    archives_dir.mkdir(parents=True)
    
    # Create governors directories
    governors_dir = data_dir / "governors"
    traits_dir = governors_dir / "traits"
    for subdir in ["canonical", "enhanced", "mystical", "personality", "visual"]:
        (traits_dir / subdir).mkdir(parents=True)
    
    # Create test tradition archive
    tradition_data = {
        "core_concepts": ["Wisdom", "Balance", "Transformation"],
        "practices": ["Meditation", "Ritual", "Study"],
        "correspondences": {
            "elements": ["fire", "air"],
            "planets": ["Sun", "Mercury"]
        },
        "historical_context": "Ancient mystical tradition",
        "modern_applications": ["Self-development", "Spiritual growth"]
    }
    
    with open(archives_dir / "spiritual_ascension_governor_archive.json", "w") as f:
        json.dump(tradition_data, f)
    
    # Create test governor traits
    canonical_data = {
        "name": "OCCODON",
        "aethyr": "LIL",
        "aethyr_number": 1,
        "region": "Egypt",
        "correspondence": "The Universe",
        "personality": ["wise", "authoritative"],
        "domain": "Spiritual Ascension",
        "visual_motif": "Golden sage",
        "letter_influence": ["A", "B"],
        "version": "1.0.0"
    }
    
    enhanced_data = {
        "wise": {
            "trait_name": "wise",
            "definition": "Deep understanding",
            "source": "OCCODON",
            "correspondences": {
                "domain": ["Wisdom Teaching"],
                "elements": ["air"]
            },
            "practical_application": "Teaching through wisdom",
            "version": "1.0.0"
        }
    }
    
    mystical_data = {
        "element": "fire",
        "alignment": "lawful_good",
        "zodiac": "Leo",
        "tarot": "The Sun",
        "sephirot": "Tiphareth",
        "angel": "Michael",
        "number": 6,
        "version": "1.0.0"
    }
    
    personality_data = {
        "archetype": "Sage",
        "primary_traits": ["Wisdom", "Authority"],
        "secondary_traits": ["Patience", "Insight"],
        "teaching_style": "Direct Instruction",
        "approach": "Guiding",
        "tone": "Formal",
        "version": "1.0.0"
    }
    
    visual_data = {
        "form_type": "ETHEREAL",
        "color_scheme": "PRISMATIC",
        "sacred_geometry": ["MERKABA"],
        "manifestation": "Pure light",
        "effects": ["Phase shifting"],
        "version": "1.0.0"
    }
    
    # Write trait files
    with open(traits_dir / "canonical" / "occodon_canonical.json", "w") as f:
        json.dump(canonical_data, f)
    
    with open(traits_dir / "enhanced" / "occodon_enhanced.json", "w") as f:
        json.dump(enhanced_data, f)
    
    with open(traits_dir / "mystical" / "occodon_mystical.json", "w") as f:
        json.dump(mystical_data, f)
    
    with open(traits_dir / "personality" / "occodon_personality.json", "w") as f:
        json.dump(personality_data, f)
    
    with open(traits_dir / "visual" / "occodon_visual.json", "w") as f:
        json.dump(visual_data, f)
    
    return data_dir

@pytest.fixture
def invalid_tradition_data(test_data_dir):
    """Create invalid tradition data for testing"""
    archives_dir = test_data_dir / "knowledge" / "archives" / "governor_archives"
    
    # Invalid core concepts (not a list)
    invalid_data = {
        "core_concepts": "Not a list",
        "practices": ["Meditation"],
        "correspondences": {"elements": ["fire"]},
        "historical_context": "Test",
        "modern_applications": ["Test"]
    }
    
    with open(archives_dir / "invalid_tradition_governor_archive.json", "w") as f:
        json.dump(invalid_data, f)

def test_knowledge_mapper_initialization(test_data_dir):
    """Test knowledge mapper initialization"""
    mapper = KnowledgeMapper(test_data_dir)
    assert mapper.data_root == test_data_dir
    assert mapper.knowledge_root == test_data_dir / "knowledge"
    assert mapper.governors_root == test_data_dir / "governors"
    assert isinstance(mapper._executor, ThreadPoolExecutor)

def test_load_tradition_knowledge(test_data_dir):
    """Test loading tradition knowledge"""
    mapper = KnowledgeMapper(test_data_dir)
    knowledge = mapper._load_tradition_knowledge("Spiritual Ascension")
    
    assert isinstance(knowledge, TraditionKnowledge)
    assert knowledge.tradition_name == "Spiritual Ascension"
    assert "Wisdom" in knowledge.core_concepts
    assert "Meditation" in knowledge.practices
    assert knowledge.correspondences["elements"] == ["fire", "air"]
    assert knowledge.validate()

def test_get_mystical_traditions(test_data_dir):
    """Test extracting mystical traditions"""
    mapper = KnowledgeMapper(test_data_dir)
    traits = mapper.trait_loader.load_all_traits("OCCODON", 1)
    assert traits is not None
    
    traditions = mapper._get_mystical_traditions(traits)
    assert "Astrology" in traditions  # From zodiac
    assert "Tarot" in traditions  # From tarot
    assert "Kabbalah" in traditions  # From sephirot
    assert "Angelology" in traditions  # From angel
    assert "Elemental_Magic" in traditions  # From element

def test_extract_specialized_domains(test_data_dir):
    """Test extracting specialized domains"""
    mapper = KnowledgeMapper(test_data_dir)
    traits = mapper.trait_loader.load_all_traits("OCCODON", 1)
    assert traits is not None
    
    domains = mapper._extract_specialized_domains(traits)
    assert "Spiritual Ascension" in domains
    assert "Wisdom Teaching" in domains
    assert "Sephirot: Tiphareth" in domains

def test_extract_teaching_methods(test_data_dir):
    """Test extracting teaching methods"""
    mapper = KnowledgeMapper(test_data_dir)
    traits = mapper.trait_loader.load_all_traits("OCCODON", 1)
    assert traits is not None
    
    methods = mapper._extract_teaching_methods(traits)
    assert "Direct Instruction" in methods
    assert "Guiding" in methods
    assert "Teaching through wisdom" in methods

def test_extract_ritual_practices(test_data_dir):
    """Test extracting ritual practices"""
    mapper = KnowledgeMapper(test_data_dir)
    traits = mapper.trait_loader.load_all_traits("OCCODON", 1)
    assert traits is not None
    
    practices = mapper._extract_ritual_practices(traits)
    assert "fire rituals" in practices
    assert "Leo workings" in practices
    assert "The Sun meditations" in practices
    assert "Tiphareth invocations" in practices
    assert "Michael rituals" in practices

def test_extract_correspondences(test_data_dir):
    """Test extracting correspondences"""
    mapper = KnowledgeMapper(test_data_dir)
    traits = mapper.trait_loader.load_all_traits("OCCODON", 1)
    assert traits is not None
    
    correspondences = mapper._extract_correspondences(traits)
    assert "fire" in correspondences["elements"]
    assert "air" in correspondences["elements"]
    assert "Leo" in correspondences["zodiac"]
    assert "The Sun" in correspondences["tarot"]
    assert "Tiphareth" in correspondences["sephirot"]
    assert "Michael" in correspondences["angels"]
    assert "6" in correspondences["numbers"]

def test_map_governor_knowledge(test_data_dir):
    """Test mapping complete governor knowledge"""
    mapper = KnowledgeMapper(test_data_dir)
    knowledge = mapper.map_governor_knowledge("OCCODON", 1)
    
    assert isinstance(knowledge, GovernorKnowledge)
    assert knowledge.governor_id == "OCCODON"
    assert knowledge.primary_tradition.tradition_name == "Spiritual Ascension"
    assert len(knowledge.secondary_traditions) > 0
    assert "Spiritual Ascension" in knowledge.specialized_domains
    assert "Direct Instruction" in knowledge.teaching_methods
    assert "fire rituals" in knowledge.ritual_practices
    assert "fire" in knowledge.mystical_correspondences["elements"]
    assert knowledge.validate()

def test_map_nonexistent_governor(test_data_dir):
    """Test mapping knowledge for nonexistent governor"""
    mapper = KnowledgeMapper(test_data_dir)
    knowledge = mapper.map_governor_knowledge("NONEXISTENT", 999)
    assert knowledge is None

def test_knowledge_caching(test_data_dir):
    """Test knowledge caching"""
    mapper = KnowledgeMapper(test_data_dir)
    
    # First load should cache
    knowledge1 = mapper.map_governor_knowledge("OCCODON", 1)
    assert knowledge1 is not None
    
    # Second load should use cache
    knowledge2 = mapper.map_governor_knowledge("OCCODON", 1)
    assert knowledge2 is not None
    assert knowledge1 is knowledge2  # Same object from cache

def test_cache_invalidation(test_data_dir):
    """Test cache invalidation"""
    mapper = KnowledgeMapper(test_data_dir)
    
    # Load and cache knowledge
    knowledge1 = mapper.map_governor_knowledge("OCCODON", 1)
    assert knowledge1 is not None
    
    # Modify last_updated to force cache invalidation
    knowledge1.last_updated = time.time() - (mapper.CACHE_TTL + 1)
    
    # Next load should create new object
    knowledge2 = mapper.map_governor_knowledge("OCCODON", 1)
    assert knowledge2 is not None
    assert knowledge1 is not knowledge2  # Different object after cache invalidation

def test_invalid_tradition_validation(test_data_dir, invalid_tradition_data):
    """Test validation of invalid tradition data"""
    mapper = KnowledgeMapper(test_data_dir)
    knowledge = mapper._load_tradition_knowledge("invalid_tradition")
    assert knowledge is None

def test_concurrent_tradition_loading(test_data_dir):
    """Test concurrent loading of traditions"""
    mapper = KnowledgeMapper(test_data_dir)
    traits = mapper.trait_loader.load_all_traits("OCCODON", 1)
    assert traits is not None
    
    # Get traditions and load concurrently
    traditions = mapper._get_mystical_traditions(traits)
    assert len(traditions) > 0
    
    # Create futures for concurrent loading
    futures = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        for tradition in traditions:
            future = executor.submit(mapper._load_tradition_knowledge, tradition)
            futures.append(future)
    
    # Check results
    results = [future.result() for future in futures]
    assert any(isinstance(result, TraditionKnowledge) for result in results)

def test_error_handling(test_data_dir):
    """Test error handling in various methods"""
    mapper = KnowledgeMapper(test_data_dir)
    
    # Create mock traits that will raise exceptions
    mock_traits = MagicMock(spec=GovernorTraits)
    mock_traits.mystical = MagicMock(side_effect=Exception("Mystical error"))
    mock_traits.canonical = MagicMock(side_effect=Exception("Canonical error"))
    mock_traits.personality = MagicMock(side_effect=Exception("Personality error"))
    mock_traits.enhanced = MagicMock(side_effect=Exception("Enhanced error"))
    
    # Test error handling in each method
    assert mapper._get_mystical_traditions(mock_traits) == set()
    assert mapper._extract_specialized_domains(mock_traits) == []
    assert mapper._extract_teaching_methods(mock_traits) == []
    assert mapper._extract_ritual_practices(mock_traits) == []
    assert mapper._extract_correspondences(mock_traits) == {} 