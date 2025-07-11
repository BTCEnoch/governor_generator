"""
Tests for the governor profile generation system
"""

import pytest
from datetime import datetime

from core.governors import (
    GovernorProfileGenerator,
    ProfileAnalyzer,
    OrdinalHandler
)
from core.governors.bitcoin import (
    BitcoinBlock,
    Inscription,
    StateProof
)
from core.governors.profiles.analyzer import (
    EnhancedProfile,
    ElementalEssence,
    VoidmakerAwareness,
    WisdomFoundation,
    TeachingDoctrine
)

@pytest.fixture
def generator():
    """Create profile generator instance"""
    return GovernorProfileGenerator()

@pytest.fixture
def analyzer():
    """Create profile analyzer instance"""
    return ProfileAnalyzer()

@pytest.fixture
def mock_block():
    """Create mock Bitcoin block data"""
    return BitcoinBlock(
        height=100000,
        hash="mock_hash_123",
        previous_hash="mock_prev_hash",
        timestamp=int(datetime.now().timestamp()),
        merkle_root="mock_merkle_root",
        difficulty=1
    )

async def test_profile_generation(generator, mock_block):
    """Test basic profile generation"""
    profile = await generator.generate_profile(1, mock_block.height)
    
    assert profile["governor_id"] == "GOV_001"
    assert "generation_context" in profile
    assert "mystical_profile" in profile
    assert "personality_profile" in profile

async def test_profile_inscription(generator, mock_block):
    """Test profile inscription"""
    profile = await generator.generate_and_inscribe_profile(
        1,
        mock_block.height
    )
    
    assert "inscription" in profile
    assert profile["inscription"]["id"].startswith("ord_")
    assert profile["inscription"]["block_height"] == mock_block.height

async def test_profile_analysis(generator, analyzer, mock_block):
    """Test profile analysis"""
    profile = await generator.generate_profile(1, mock_block.height)
    enhanced = await analyzer.analyze_profile(profile, mock_block.height)
    
    assert enhanced.governor_id == profile["governor_id"]
    assert 1 <= enhanced.difficulty_scale <= 10
    assert enhanced.narrative_tone
    assert enhanced.preferred_mechanics
    
    # Test elemental essence
    assert enhanced.elemental_essence.ruling_element in ["fire", "water", "air", "earth", "spirit"]
    assert len(enhanced.elemental_essence.secondary_elements) > 0
    assert 0 <= enhanced.elemental_essence.elemental_balance <= 1
    assert 1 <= enhanced.elemental_essence.manifestation_strength <= 10
    
    # Test void awareness
    assert 0 <= enhanced.void_awareness.resonance <= 1
    assert enhanced.void_awareness.manifestation
    assert len(enhanced.void_awareness.void_affinity) > 0
    assert len(enhanced.void_awareness.cosmic_patterns) > 0
    assert len(enhanced.void_awareness.reality_influence) > 0
    assert len(enhanced.void_awareness.integration_unity) > 0
    
    # Test wisdom foundation
    assert enhanced.wisdom_foundation.primary_domain
    assert len(enhanced.wisdom_foundation.teaching_methods) > 0
    assert len(enhanced.wisdom_foundation.difficulty_curve) > 0
    
    # Test teaching doctrine
    assert len(enhanced.teaching_doctrine.preferred_methods) > 0
    assert 0 <= enhanced.teaching_doctrine.adaptability <= 1
    assert len(enhanced.teaching_doctrine.progression_curve) > 0

async def test_elemental_essence_generation(generator, analyzer, mock_block):
    """Test elemental essence generation"""
    profile = await generator.generate_profile(1, mock_block.height)
    enhanced = await analyzer.analyze_profile(profile, mock_block.height)
    
    # Test elemental essence structure
    essence = enhanced.elemental_essence
    assert essence.ruling_element in ["fire", "water", "air", "earth", "spirit"]
    assert all(e in ["fire", "water", "air", "earth", "spirit"] for e in essence.secondary_elements)
    assert 0 <= essence.elemental_balance <= 1
    assert 1 <= essence.manifestation_strength <= 10
    
    # Test elemental relationships
    assert essence.ruling_element not in essence.secondary_elements
    assert len(set(essence.secondary_elements)) == len(essence.secondary_elements)

async def test_void_awareness_generation(generator, analyzer, mock_block):
    """Test void awareness generation"""
    profile = await generator.generate_profile(1, mock_block.height)
    enhanced = await analyzer.analyze_profile(profile, mock_block.height)
    
    # Test void awareness structure
    void = enhanced.void_awareness
    assert 0 <= void.resonance <= 1
    assert void.manifestation in ["Ethereal", "Material", "Balanced"]
    assert len(void.void_affinity) > 0
    
    # Test cosmic awareness
    assert len(void.cosmic_patterns) >= 2
    assert len(void.reality_influence) >= 2
    assert len(void.integration_unity) >= 2
    
    # Test pattern relationships
    assert len(set(void.cosmic_patterns)) == len(void.cosmic_patterns)
    assert len(set(void.reality_influence)) == len(void.reality_influence)
    assert len(set(void.integration_unity)) == len(void.integration_unity)

async def test_invalid_governor_number(generator):
    """Test handling of invalid governor numbers"""
    with pytest.raises(ValueError):
        await generator.generate_profile(92, 100000)  # Only 91 governors

async def test_profile_validation(generator, mock_block):
    """Test profile validation"""
    profile = await generator.generate_profile(1, mock_block.height)
    
    # Test required sections
    for section in ["mystical_profile", "personality_profile"]:
        assert section in profile
        
    # Test mystical profile structure
    mystical = profile["mystical_profile"]
    assert "alignment" in mystical
    assert "essence" in mystical
    
    # Test personality profile structure
    personality = profile["personality_profile"]
    assert "core" in personality
    assert "teaching" in personality 