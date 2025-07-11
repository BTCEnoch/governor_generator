"""
Tests for Bitcoin integration with Kabbalah system
"""

import pytest
from typing import Dict, Any

from core.mystical_systems.kabbalah_system.kabbalah_system import KabbalahSystem
from core.mystical_systems.kabbalah_system.schemas import SefirotPosition, KabbalahProfile

@pytest.fixture
def kabbalah_system():
    """Create a KabbalahSystem instance for testing"""
    return KabbalahSystem()

@pytest.fixture
def mock_governor_data():
    """Create mock governor data with Bitcoin attributes"""
    return {
        "name": "TestGovernor",
        "traits": ["wisdom", "understanding", "mercy", "power"],
        "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "ordinal_id": "ord1234567890",
        "inscription_id": "ins1234567890"
    }

def test_kabbalah_system_initialization(kabbalah_system):
    """Test KabbalahSystem initialization"""
    assert isinstance(kabbalah_system, KabbalahSystem)
    system_info = kabbalah_system.get_system_info()
    assert system_info["system_id"] == "kabbalah_system_v1"

def test_validate_input_with_bitcoin_data(kabbalah_system, mock_governor_data):
    """Test input validation with Bitcoin data"""
    assert kabbalah_system.validate_input(mock_governor_data) is True

def test_validate_input_invalid_bitcoin_data(kabbalah_system):
    """Test input validation with invalid Bitcoin data"""
    invalid_data = {
        "name": "TestGovernor",
        "traits": ["wisdom"],
        "txid": 12345,  # Should be string
        "ordinal_id": ["invalid"],  # Should be string
        "inscription_id": 67890  # Should be string
    }
    assert kabbalah_system.validate_input(invalid_data) is False

def test_generate_profile_with_bitcoin_data(kabbalah_system, mock_governor_data):
    """Test profile generation with Bitcoin data"""
    profile = kabbalah_system.generate_profile(mock_governor_data)
    
    # Check Bitcoin-specific attributes
    assert isinstance(profile, KabbalahProfile)
    assert profile.bitcoin_resonance is not None
    assert profile.chain_harmony is not None
    assert profile.ordinal_attributes != {}
    assert profile.inscription_attributes != {}
    assert profile.sefirot_resonances != {}
    
    # Check sefirot assignments
    assert profile.primary_sefirah != ""
    assert len(profile.secondary_sefirot) == 2
    assert all(isinstance(x, str) for x in profile.secondary_sefirot)
    
    # Check Bitcoin influence on sefirot resonances
    assert all(0 <= score <= 1.0 for score in profile.sefirot_resonances.values())
    assert len(profile.sefirot_resonances) == len(SefirotPosition)
    
    # Check relationships
    assert "ordinal" in profile.relationships
    assert "inscription" in profile.relationships
    assert profile.relationships["ordinal"] == ["ord1234567890"]
    assert profile.relationships["inscription"] == ["ins1234567890"]
    
    # Check metadata
    assert profile.metadata["bitcoin_derived"] is True
    assert profile.metadata["ordinal_bound"] is True
    assert profile.metadata["inscription_bound"] is True

def test_generate_profile_without_bitcoin_data(kabbalah_system):
    """Test profile generation without Bitcoin data"""
    basic_data = {
        "name": "TestGovernor",
        "traits": ["wisdom", "understanding"]
    }
    profile = kabbalah_system.generate_profile(basic_data)
    
    # Check Bitcoin-specific attributes are None/empty
    assert profile.bitcoin_resonance is None
    assert profile.chain_harmony is None
    assert profile.ordinal_attributes == {}
    assert profile.inscription_attributes == {}
    
    # Check sefirot assignments still work
    assert profile.primary_sefirah != ""
    assert len(profile.secondary_sefirot) == 2
    assert profile.sefirot_resonances != {}
    
    # Check relationships
    assert profile.relationships["ordinal"] == []
    assert profile.relationships["inscription"] == []
    
    # Check metadata
    assert profile.metadata["bitcoin_derived"] is False
    assert profile.metadata["ordinal_bound"] is False
    assert profile.metadata["inscription_bound"] is False

def test_calculate_correspondences_with_bitcoin(kabbalah_system, mock_governor_data):
    """Test correspondence calculation with Bitcoin data"""
    correspondences = kabbalah_system.calculate_correspondences(mock_governor_data)
    
    # Check basic correspondences
    assert "primary_sefirah" in correspondences
    assert "secondary_sefirot" in correspondences
    assert "divine_attribute" in correspondences
    assert "human_attribute" in correspondences
    assert "element" in correspondences
    assert "planet" in correspondences
    
    # Check Bitcoin-specific correspondences
    assert "bitcoin_resonance" in correspondences
    assert "chain_harmony" in correspondences
    assert "sefirot_resonances" in correspondences
    assert len(correspondences["sefirot_resonances"]) == len(SefirotPosition)

def test_calculate_correspondences_without_bitcoin(kabbalah_system):
    """Test correspondence calculation without Bitcoin data"""
    basic_data = {
        "name": "TestGovernor",
        "traits": ["wisdom", "understanding"]
    }
    correspondences = kabbalah_system.calculate_correspondences(basic_data)
    
    # Check basic correspondences exist
    assert "primary_sefirah" in correspondences
    assert "secondary_sefirot" in correspondences
    assert "sefirot_resonances" in correspondences
    
    # Check Bitcoin-specific correspondences are absent
    assert "bitcoin_resonance" not in correspondences
    assert "chain_harmony" not in correspondences

def test_bitcoin_sefirot_affinity_calculation(kabbalah_system, mock_governor_data):
    """Test Bitcoin-influenced sefirot affinity calculation"""
    # Calculate affinities with Bitcoin
    bitcoin_scores = kabbalah_system._calculate_bitcoin_sefirot_affinities(
        mock_governor_data["traits"],
        mock_governor_data["txid"]
    )
    
    # Calculate regular affinities
    regular_scores = kabbalah_system._calculate_sefirot_affinities(
        mock_governor_data["traits"]
    )
    
    # Check that Bitcoin influence modifies the scores
    assert bitcoin_scores != regular_scores
    assert all(0 <= score <= 1.0 for score in bitcoin_scores.values())
    assert len(bitcoin_scores) == len(regular_scores)
    
    # Check that the differences are within expected range (30% Bitcoin influence)
    for sefirah in bitcoin_scores:
        diff = abs(bitcoin_scores[sefirah] - regular_scores[sefirah])
        assert diff <= 0.3  # Maximum possible difference due to 70-30 split

def test_format_output_includes_bitcoin_data(kabbalah_system, mock_governor_data):
    """Test output formatting includes Bitcoin data"""
    profile = kabbalah_system.generate_profile(mock_governor_data)
    output = kabbalah_system.format_output(profile)
    
    # Check Bitcoin-specific fields in output
    assert "bitcoin_resonance" in output
    assert "chain_harmony" in output
    assert "ordinal_attributes" in output
    assert "inscription_attributes" in output
    assert "sefirot_resonances" in output
    assert output["metadata"]["bitcoin_derived"] is True
    assert output["metadata"]["ordinal_bound"] is True
    assert output["metadata"]["inscription_bound"] is True 