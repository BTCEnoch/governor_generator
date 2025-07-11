"""
Tests for Bitcoin integration with Tarot system
"""

import pytest
from typing import Dict, Any

from core.mystical_systems.tarot_system.tarot_system import TarotSystem, TarotProfile

@pytest.fixture
def tarot_system():
    """Create a TarotSystem instance for testing"""
    return TarotSystem()

@pytest.fixture
def mock_governor_data():
    """Create mock governor data with Bitcoin attributes"""
    return {
        "name": "TestGovernor",
        "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "ordinal_id": "ord1234567890",
        "inscription_id": "ins1234567890"
    }

def test_tarot_system_initialization(tarot_system):
    """Test TarotSystem initialization"""
    assert isinstance(tarot_system, TarotSystem)
    assert tarot_system.name == "tarot"

def test_validate_input_with_bitcoin_data(tarot_system, mock_governor_data):
    """Test input validation with Bitcoin data"""
    assert tarot_system.validate_input(mock_governor_data) is True

def test_validate_input_invalid_bitcoin_data(tarot_system):
    """Test input validation with invalid Bitcoin data"""
    invalid_data = {
        "name": "TestGovernor",
        "txid": 12345,  # Should be string
        "ordinal_id": ["invalid"],  # Should be string
        "inscription_id": 67890  # Should be string
    }
    assert tarot_system.validate_input(invalid_data) is False

def test_generate_profile_with_bitcoin_data(tarot_system, mock_governor_data):
    """Test profile generation with Bitcoin data"""
    profile = tarot_system.generate_profile(mock_governor_data)
    
    # Check Bitcoin-specific attributes
    assert isinstance(profile, TarotProfile)
    assert profile.bitcoin_resonance is not None
    assert profile.chain_harmony is not None
    assert profile.ordinal_attributes != {}
    assert profile.inscription_attributes != {}
    
    # Check Bitcoin-influenced elements
    assert any("Bitcoin resonance level" in elem for elem in profile.symbolic_elements)
    assert any("Chain harmony disruption" in source for source in profile.conflict_sources)
    assert any("ordinal essence integration" in path for path in profile.growth_paths)
    
    # Check relationships
    assert "ordinal" in profile.relationships
    assert "inscription" in profile.relationships
    assert profile.relationships["ordinal"] == ["ord1234567890"]
    assert profile.relationships["inscription"] == ["ins1234567890"]
    
    # Check metadata
    assert profile.metadata["bitcoin_derived"] is True
    assert profile.metadata["ordinal_bound"] is True
    assert profile.metadata["inscription_bound"] is True

def test_generate_profile_without_bitcoin_data(tarot_system):
    """Test profile generation without Bitcoin data"""
    basic_data = {"name": "TestGovernor"}
    profile = tarot_system.generate_profile(basic_data)
    
    # Check Bitcoin-specific attributes are None/empty
    assert profile.bitcoin_resonance is None
    assert profile.chain_harmony is None
    assert profile.ordinal_attributes == {}
    assert profile.inscription_attributes == {}
    
    # Check no Bitcoin-influenced elements
    assert not any("Bitcoin resonance level" in elem for elem in profile.symbolic_elements)
    assert not any("Chain harmony disruption" in source for source in profile.conflict_sources)
    assert not any("ordinal essence integration" in path for path in profile.growth_paths)
    
    # Check relationships
    assert profile.relationships["ordinal"] == []
    assert profile.relationships["inscription"] == []
    
    # Check metadata
    assert profile.metadata["bitcoin_derived"] is False
    assert profile.metadata["ordinal_bound"] is False
    assert profile.metadata["inscription_bound"] is False

def test_system_info_includes_bitcoin_capabilities(tarot_system):
    """Test system info includes Bitcoin capabilities"""
    info = tarot_system.get_system_info()
    assert "bitcoin_resonance" in info["capabilities"]
    assert "ordinal_binding" in info["capabilities"]
    assert "inscription_integration" in info["capabilities"]

def test_format_output_includes_bitcoin_data(tarot_system, mock_governor_data):
    """Test output formatting includes Bitcoin data"""
    profile = tarot_system.generate_profile(mock_governor_data)
    output = tarot_system.format_output(profile)
    
    # Check Bitcoin-specific fields in output
    assert "bitcoin_resonance" in output
    assert "chain_harmony" in output
    assert "ordinal_attributes" in output
    assert "inscription_attributes" in output
    assert output["metadata"]["bitcoin_derived"] is True
    assert output["metadata"]["ordinal_bound"] is True
    assert output["metadata"]["inscription_bound"] is True 