"""
Tests for Bitcoin integration with Zodiac system
"""

import pytest
from datetime import datetime
from typing import Dict, Any
from pydantic import ValidationError

from core.mystical_systems.zodiac_system.zodiac_system import ZodiacSystem
from core.mystical_systems.zodiac_system.schemas import (
    ZodiacElement,
    ZodiacModality,
    ZodiacProfile,
    ZodiacSystemConfig
)
from core.utils.mystical.schemas import SystemValidation

@pytest.fixture
def zodiac_config():
    """Create a test configuration"""
    return {
        "use_bitcoin_influence": True,
        "default_sign": "Aries",
        "influence_weights": {
            "traits": 0.4,
            "bitcoin": 0.3,
            "ordinal": 0.2,
            "inscription": 0.1
        }
    }

@pytest.fixture
def zodiac_system(zodiac_config):
    """Create a ZodiacSystem instance for testing"""
    return ZodiacSystem(config=zodiac_config)

@pytest.fixture
def mock_governor_data():
    """Create mock governor data with Bitcoin attributes"""
    return {
        "name": "TestGovernor",
        "traits": ["leadership", "creativity", "wisdom", "power"],
        "birthdate": "2000-01-01",
        "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "ordinal_id": "ord1234567890",
        "inscription_id": "ins1234567890"
    }

def test_zodiac_system_initialization(zodiac_system, zodiac_config):
    """Test ZodiacSystem initialization"""
    assert isinstance(zodiac_system, ZodiacSystem)
    assert zodiac_system.id == "zodiac"
    assert zodiac_system.config["use_bitcoin_influence"] == zodiac_config["use_bitcoin_influence"]
    assert zodiac_system.config["default_sign"] == zodiac_config["default_sign"]

def test_zodiac_system_initialization_invalid_config():
    """Test ZodiacSystem initialization with invalid config"""
    invalid_config = {
        "use_bitcoin_influence": "not_a_boolean",
        "default_sign": 123,  # Should be string
        "influence_weights": "not_a_dict"
    }
    with pytest.raises(ValidationError):
        ZodiacSystem(config=invalid_config)

def test_validate_input_with_bitcoin_data(zodiac_system, mock_governor_data):
    """Test input validation with Bitcoin data"""
    validation = zodiac_system.validate_input(mock_governor_data)
    assert isinstance(validation, SystemValidation)
    assert validation.is_valid
    assert not validation.errors

def test_validate_input_invalid_bitcoin_data(zodiac_system):
    """Test input validation with invalid Bitcoin data"""
    invalid_data = {
        "name": "TestGovernor",
        "traits": ["leadership"],
        "birthdate": "2000-01-01",
        "txid": 12345,  # Should be string
        "ordinal_id": ["invalid"],  # Should be string
        "inscription_id": 67890  # Should be string
    }
    validation = zodiac_system.validate_input(invalid_data)
    assert isinstance(validation, SystemValidation)
    assert not validation.is_valid
    assert len(validation.errors) > 0
    assert any("txid" in error.field for error in validation.errors)

def test_generate_profile_with_bitcoin_data(zodiac_system, mock_governor_data):
    """Test profile generation with Bitcoin data"""
    profile = zodiac_system.generate_profile(mock_governor_data)
    
    # Check profile is valid Pydantic model
    assert isinstance(profile, ZodiacProfile)
    
    # Check Bitcoin-specific attributes
    assert profile.bitcoin_resonance is not None
    assert profile.chain_harmony is not None
    assert profile.ordinal_attributes != {}
    assert profile.inscription_attributes != {}
    assert profile.zodiac_resonances != {}
    
    # Check zodiac assignments
    assert profile.sun_sign != ""
    assert profile.rising_sign is None  # Now optional
    assert profile.moon_sign is None    # Now optional
    
    # Check element and modality distributions
    assert all(0 <= score <= 1.0 for score in profile.elements.values())
    assert all(0 <= score <= 1.0 for score in profile.modalities.values())
    assert sum(profile.elements.values()) == pytest.approx(1.0)
    assert sum(profile.modalities.values()) == pytest.approx(1.0)
    
    # Check Bitcoin influence on zodiac resonances
    assert all(0 <= score <= 1.0 for score in profile.zodiac_resonances.values())
    
    # Check relationships
    assert "ordinal" in profile.relationships
    assert "inscription" in profile.relationships
    assert profile.relationships["ordinal"] == ["ord1234567890"]
    assert profile.relationships["inscription"] == ["ins1234567890"]
    
    # Check metadata
    assert profile.metadata["bitcoin_influenced"] is True
    assert profile.metadata["ordinal_bound"] is True
    assert profile.metadata["inscription_bound"] is True

def test_generate_profile_without_bitcoin_data(zodiac_system):
    """Test profile generation without Bitcoin data"""
    basic_data = {
        "name": "TestGovernor",
        "traits": ["leadership", "creativity"],
        "birthdate": "2000-01-01"
    }
    profile = zodiac_system.generate_profile(basic_data)
    
    # Check Bitcoin-specific attributes are None/empty
    assert profile.bitcoin_resonance is None
    assert profile.chain_harmony is None
    assert profile.ordinal_attributes == {}
    assert profile.inscription_attributes == {}
    
    # Check zodiac assignments still work
    assert profile.sun_sign != ""
    assert profile.rising_sign is None
    assert profile.zodiac_resonances != {}
    
    # Check element and modality distributions
    assert all(0 <= score <= 1.0 for score in profile.elements.values())
    assert all(0 <= score <= 1.0 for score in profile.modalities.values())
    assert sum(profile.elements.values()) == pytest.approx(1.0)
    assert sum(profile.modalities.values()) == pytest.approx(1.0)
    
    # Check relationships
    assert profile.relationships["ordinal"] == []
    assert profile.relationships["inscription"] == []
    
    # Check metadata
    assert profile.metadata["bitcoin_influenced"] is False
    assert profile.metadata["ordinal_bound"] is False
    assert profile.metadata["inscription_bound"] is False

def test_calculate_correspondences_with_bitcoin(zodiac_system, mock_governor_data):
    """Test correspondence calculation with Bitcoin data"""
    correspondences = zodiac_system.calculate_correspondences(mock_governor_data)
    
    # Check basic correspondences
    assert "sun_sign" in correspondences
    assert "element" in correspondences
    assert "modality" in correspondences
    assert "ruling_planet" in correspondences
    
    # Check Bitcoin-specific correspondences
    assert "bitcoin_resonance" in correspondences
    assert "chain_harmony" in correspondences
    assert "zodiac_resonances" in correspondences
    assert all(0 <= score <= 1.0 for score in correspondences["zodiac_resonances"].values())

def test_calculate_correspondences_without_bitcoin(zodiac_system):
    """Test correspondence calculation without Bitcoin data"""
    basic_data = {
        "name": "TestGovernor",
        "traits": ["leadership", "creativity"],
        "birthdate": "2000-01-01"
    }
    correspondences = zodiac_system.calculate_correspondences(basic_data)
    
    # Check basic correspondences exist
    assert "sun_sign" in correspondences
    assert "element" in correspondences
    assert "modality" in correspondences
    
    # Check Bitcoin-specific correspondences are absent
    assert "bitcoin_resonance" not in correspondences
    assert "chain_harmony" not in correspondences

def test_bitcoin_sign_affinity_calculation(zodiac_system, mock_governor_data):
    """Test Bitcoin-influenced zodiac sign affinity calculation"""
    # Calculate affinities with Bitcoin
    bitcoin_scores = zodiac_system._calculate_bitcoin_sign_affinities(
        mock_governor_data["traits"],
        mock_governor_data["txid"]
    )
    
    # Calculate regular affinities
    regular_scores = zodiac_system._calculate_sign_affinities(
        mock_governor_data["traits"]
    )
    
    # Check that Bitcoin influence modifies the scores
    assert bitcoin_scores != regular_scores
    assert all(0 <= score <= 1.0 for score in bitcoin_scores.values())
    assert len(bitcoin_scores) == len(regular_scores)
    
    # Check that the differences are within expected range (30% Bitcoin influence)
    for sign in bitcoin_scores:
        diff = abs(bitcoin_scores[sign] - regular_scores[sign])
        assert diff <= 0.3  # Maximum possible difference due to 70-30 split

def test_format_output_includes_bitcoin_data(zodiac_system, mock_governor_data):
    """Test output formatting includes Bitcoin data"""
    profile = zodiac_system.generate_profile(mock_governor_data)
    output = zodiac_system.format_output(profile)
    
    # Check Bitcoin-specific fields in output
    assert "bitcoin_resonance" in output
    assert "chain_harmony" in output
    assert "ordinal_attributes" in output
    assert "inscription_attributes" in output
    assert "zodiac_resonances" in output
    assert output["metadata"]["bitcoin_influenced"] is True
    assert output["metadata"]["ordinal_bound"] is True
    assert output["metadata"]["inscription_bound"] is True

def test_element_modality_bitcoin_influence(zodiac_system, mock_governor_data):
    """Test Bitcoin influence on element and modality distributions"""
    profile = zodiac_system.generate_profile(mock_governor_data)
    
    # Get base distributions without Bitcoin
    basic_data = mock_governor_data.copy()
    del basic_data["txid"]
    del basic_data["ordinal_id"]
    del basic_data["inscription_id"]
    base_profile = zodiac_system.generate_profile(basic_data)
    
    # Check that Bitcoin influence affects distributions
    assert profile.elements != base_profile.elements
    assert profile.modalities != base_profile.modalities
    
    # But distributions should still be valid
    assert sum(profile.elements.values()) == pytest.approx(1.0)
    assert sum(profile.modalities.values()) == pytest.approx(1.0)
    assert all(0 <= score <= 1.0 for score in profile.elements.values())
    assert all(0 <= score <= 1.0 for score in profile.modalities.values()) 