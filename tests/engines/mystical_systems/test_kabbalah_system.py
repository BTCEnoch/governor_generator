"""
Tests for the Kabbalah System
"""

import pytest
from typing import Dict, Any

from core.mystical_systems.kabbalah_system.kabbalah_system import KabbalahSystem
from core.mystical_systems.kabbalah_system.schemas import (
    SefirotPosition,
    KabbalahProfile,
    KabbalahSystemConfig
)

@pytest.fixture
def kabbalah_system():
    """Create a Kabbalah system instance for testing"""
    config = KabbalahSystemConfig(
        use_bitcoin_influence=True,
        default_sefirah="tiferet",
        influence_weights={
            "traits": 0.4,
            "bitcoin": 0.3,
            "ordinal": 0.2,
            "inscription": 0.1
        }
    )
    return KabbalahSystem(config.dict())

@pytest.fixture
def sample_input_data():
    """Sample input data for testing"""
    return {
        "name": "Test Entity",
        "traits": [
            "wisdom",
            "insight",
            "creativity",
            "divine inspiration",
            "enlightenment"
        ],
        "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "ordinal_id": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef_0",
        "inscription_id": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef_i0"
    }

def test_kabbalah_system_initialization(kabbalah_system):
    """Test Kabbalah system initialization"""
    assert kabbalah_system is not None
    assert kabbalah_system.system_name == "kabbalah"
    assert isinstance(kabbalah_system.config, dict)
    assert kabbalah_system.config["use_bitcoin_influence"] is True
    assert kabbalah_system.config["default_sefirah"] == "tiferet"

def test_validate_input_valid_data(kabbalah_system, sample_input_data):
    """Test input validation with valid data"""
    validation = kabbalah_system.validate_input(sample_input_data)
    assert validation.is_valid is True
    assert len(validation.errors) == 0

def test_validate_input_invalid_data(kabbalah_system):
    """Test input validation with invalid data"""
    invalid_data = {
        "name": "Test Entity",
        "traits": "not a list",  # Should be a list
        "txid": 12345  # Should be a string
    }
    validation = kabbalah_system.validate_input(invalid_data)
    assert validation.is_valid is False
    assert len(validation.errors) > 0

def test_calculate_sefirot_affinities(kabbalah_system):
    """Test calculation of Sefirot affinities"""
    traits = ["wisdom", "insight", "creativity"]
    scores = kabbalah_system._calculate_sefirot_affinities(traits)
    
    assert isinstance(scores, dict)
    assert len(scores) > 0
    assert all(isinstance(v, float) for v in scores.values())
    assert all(0 <= v <= 1 for v in scores.values())
    
    # Test that wisdom-related Sefirot have higher scores
    assert scores["chokhmah"] > 0.5  # Chokhmah = Wisdom

def test_calculate_bitcoin_sefirot_affinities(kabbalah_system, sample_input_data):
    """Test calculation of Bitcoin-influenced Sefirot affinities"""
    traits = sample_input_data["traits"]
    txid = sample_input_data["txid"]
    
    scores = kabbalah_system._calculate_bitcoin_sefirot_affinities(traits, txid)
    
    assert isinstance(scores, dict)
    assert len(scores) > 0
    assert all(isinstance(v, float) for v in scores.values())
    assert all(0 <= v <= 1 for v in scores.values())

def test_generate_profile_without_bitcoin(kabbalah_system):
    """Test profile generation without Bitcoin data"""
    input_data = {
        "name": "Test Entity",
        "traits": ["wisdom", "insight", "creativity"]
    }
    
    profile = kabbalah_system.generate_profile(input_data)
    
    assert isinstance(profile, KabbalahProfile)
    assert profile.name == "Kabbalah Profile for Test Entity"
    assert profile.primary_sefirah in [pos.value for pos in SefirotPosition]
    assert len(profile.secondary_sefirot) == 2
    assert profile.bitcoin_resonance is None
    assert profile.chain_harmony is None
    assert not profile.ordinal_attributes
    assert not profile.inscription_attributes

def test_generate_profile_with_bitcoin(kabbalah_system, sample_input_data):
    """Test profile generation with Bitcoin data"""
    profile = kabbalah_system.generate_profile(sample_input_data)
    
    assert isinstance(profile, KabbalahProfile)
    assert profile.name == "Kabbalah Profile for Test Entity"
    assert profile.primary_sefirah in [pos.value for pos in SefirotPosition]
    assert len(profile.secondary_sefirot) == 2
    assert profile.bitcoin_resonance is not None
    assert profile.chain_harmony is not None
    assert profile.ordinal_attributes
    assert profile.inscription_attributes

def test_calculate_correspondences(kabbalah_system, sample_input_data):
    """Test correspondence calculation"""
    correspondences = kabbalah_system.calculate_correspondences(sample_input_data)
    
    assert isinstance(correspondences, dict)
    assert "primary_sefirah" in correspondences
    assert "secondary_sefirot" in correspondences
    assert "divine_attribute" in correspondences
    assert "human_attribute" in correspondences
    assert "element" in correspondences
    assert "planet" in correspondences
    assert "sefirot_resonances" in correspondences
    
    if sample_input_data.get("txid"):
        assert "bitcoin_resonance" in correspondences
        assert "chain_harmony" in correspondences

def test_format_output(kabbalah_system, sample_input_data):
    """Test output formatting"""
    profile = kabbalah_system.generate_profile(sample_input_data)
    output = kabbalah_system.format_output(profile)
    
    assert isinstance(output, dict)
    assert "id" in output
    assert "name" in output
    assert "primary_sefirah" in output
    assert "secondary_sefirot" in output
    assert "divine_attributes" in output
    assert "human_attributes" in output
    assert "elements" in output
    assert "planets" in output
    assert "bitcoin_resonance" in output
    assert "chain_harmony" in output
    assert "ordinal_attributes" in output
    assert "inscription_attributes" in output
    assert "sefirot_resonances" in output

def test_error_handling(kabbalah_system):
    """Test error handling for invalid inputs"""
    with pytest.raises(ValueError):
        kabbalah_system.generate_profile({"invalid": "data"})
        
    with pytest.raises(ValueError):
        kabbalah_system.generate_profile({
            "name": "Test",
            "traits": ["wisdom"],
            "txid": "invalid_txid"
        }) 