"""
Tests for Bitcoin integration across mystical systems
"""

import pytest
from typing import Dict, Any

from core.mystical_systems.tarot_system.tarot_system import TarotSystem
from core.mystical_systems.kabbalah_system.kabbalah_system import KabbalahSystem
from core.mystical_systems.zodiac_system.zodiac_system import ZodiacSystem
from core.mystical_systems.numerology_system.numerology_system import NumerologySystem

@pytest.fixture
def mystical_systems() -> Dict[str, Any]:
    """Create instances of all mystical systems"""
    config = {
        "use_bitcoin_influence": True,
        "bitcoin_integration": {
            "network": "mainnet",
            "mode": "online"
        }
    }
    return {
        "tarot": TarotSystem(config),
        "kabbalah": KabbalahSystem(config),
        "zodiac": ZodiacSystem(config),
        "numerology": NumerologySystem(config)
    }

@pytest.fixture
def mock_governor_data():
    """Create mock governor data with Bitcoin attributes"""
    return {
        "name": "TestGovernor",
        "birthdate": "2000-01-01",
        "traits": ["wisdom", "power", "creativity"],
        "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "ordinal_id": "ord1234567890",
        "inscription_id": "ins1234567890"
    }

def test_all_systems_initialization(mystical_systems):
    """Test initialization of all mystical systems"""
    for name, system in mystical_systems.items():
        assert system.name == name
        assert hasattr(system, "generate_deterministic_seed")
        assert hasattr(system, "derive_mystical_attributes")
        assert hasattr(system, "bind_to_ordinal")
        assert hasattr(system, "bind_to_inscription")

def test_consistent_bitcoin_derivation(mystical_systems, mock_governor_data):
    """Test that Bitcoin-derived attributes are consistent across systems"""
    txid = mock_governor_data["txid"]
    
    # Get Bitcoin attributes from each system
    bitcoin_attrs = {
        name: system.derive_mystical_attributes(txid)
        for name, system in mystical_systems.items()
    }
    
    # Check resonance consistency
    resonance_values = {
        name: next(a for a in attrs if a.name == "bitcoin_resonance").value
        for name, attrs in bitcoin_attrs.items()
    }
    assert len(set(resonance_values.values())) == 1  # All systems should have same resonance
    
    # Check harmony consistency
    harmony_values = {
        name: next(a for a in attrs if a.name == "chain_harmony").value
        for name, attrs in bitcoin_attrs.items()
    }
    assert len(set(harmony_values.values())) == 1  # All systems should have same harmony

def test_ordinal_binding_consistency(mystical_systems, mock_governor_data):
    """Test that ordinal binding produces consistent results across systems"""
    ordinal_id = mock_governor_data["ordinal_id"]
    
    # Bind each system to the ordinal
    for system in mystical_systems.values():
        system.bind_to_ordinal(ordinal_id)
    
    # Check ordinal data consistency
    ordinal_data = {
        name: system.ordinal_data
        for name, system in mystical_systems.items()
    }
    
    # All systems should have same sat number
    sat_numbers = {
        name: data.get("sat", 0)
        for name, data in ordinal_data.items()
    }
    assert len(set(sat_numbers.values())) == 1
    
    # All systems should have mystical properties
    for data in ordinal_data.values():
        assert "mystical_properties" in data
        props = data["mystical_properties"]
        assert "sat_degree" in props
        assert "sat_element" in props
        assert "sat_quality" in props

def test_inscription_binding_consistency(mystical_systems, mock_governor_data):
    """Test that inscription binding produces consistent results across systems"""
    inscription_id = mock_governor_data["inscription_id"]
    
    # Bind each system to the inscription
    for system in mystical_systems.values():
        system.bind_to_inscription(inscription_id)
    
    # Check inscription data consistency
    inscription_data = {
        name: system.inscription_data
        for name, system in mystical_systems.items()
    }
    
    # All systems should have same inscription number
    insc_numbers = {
        name: data.get("number", 0)
        for name, data in inscription_data.items()
    }
    assert len(set(insc_numbers.values())) == 1
    
    # All systems should have mystical properties
    for data in inscription_data.values():
        assert "mystical_properties" in data
        props = data["mystical_properties"]
        assert "inscription_phase" in props
        assert "inscription_element" in props
        assert "inscription_pattern" in props

def test_cross_system_influence(mystical_systems, mock_governor_data):
    """Test that systems can influence each other through Bitcoin data"""
    # Generate profiles from each system
    profiles = {
        name: system.generate_profile(mock_governor_data)
        for name, system in mystical_systems.items()
    }
    
    # Check Tarot-Kabbalah connections
    tarot_profile = profiles["tarot"]
    kabbalah_profile = profiles["kabbalah"]
    
    # Tarot cards should align with Sephirot positions
    assert any(
        card in kabbalah_profile.divine_attributes
        for card in tarot_profile.primary_influences
    )
    
    # Check Zodiac-Numerology connections
    zodiac_profile = profiles["zodiac"]
    numerology_profile = profiles["numerology"]
    
    # Life path number should influence zodiac elements
    life_path = numerology_profile.life_path_number
    element_strength = zodiac_profile.elements.get(
        ["fire", "earth", "air", "water"][life_path % 4],
        0.0
    )
    assert element_strength > 0.0
    
    # Check Bitcoin number consistency
    bitcoin_numbers = {
        name: getattr(profile, "bitcoin_number", None)
        for name, profile in profiles.items()
        if hasattr(profile, "bitcoin_number")
    }
    assert len(set(bitcoin_numbers.values())) == 1  # All systems should derive same Bitcoin number

def test_profile_generation_consistency(mystical_systems, mock_governor_data):
    """Test that profile generation is consistent across systems"""
    # Generate profiles multiple times
    profiles1 = {
        name: system.generate_profile(mock_governor_data)
        for name, system in mystical_systems.items()
    }
    
    profiles2 = {
        name: system.generate_profile(mock_governor_data)
        for name, system in mystical_systems.items()
    }
    
    # Check that each system produces consistent results
    for name in mystical_systems:
        profile1 = profiles1[name]
        profile2 = profiles2[name]
        
        # Check Bitcoin-derived attributes
        if hasattr(profile1, "bitcoin_number"):
            assert profile1.bitcoin_number == profile2.bitcoin_number
        if hasattr(profile1, "bitcoin_resonance"):
            assert profile1.bitcoin_resonance == profile2.bitcoin_resonance
        if hasattr(profile1, "chain_harmony"):
            assert profile1.chain_harmony == profile2.chain_harmony
            
        # Check ordinal numbers
        if hasattr(profile1, "ordinal_numbers"):
            assert profile1.ordinal_numbers == profile2.ordinal_numbers
            
        # Check inscription numbers
        if hasattr(profile1, "inscription_numbers"):
            assert profile1.inscription_numbers == profile2.inscription_numbers

def test_correspondence_calculation_consistency(mystical_systems, mock_governor_data):
    """Test that correspondence calculations are consistent across systems"""
    # Calculate correspondences for each system
    correspondences = {
        name: system.calculate_correspondences(mock_governor_data)
        for name, system in mystical_systems.items()
    }
    
    # Check Bitcoin-specific correspondences
    for name, corr in correspondences.items():
        # Each system should have Bitcoin data
        if "bitcoin_number" in corr:
            assert 1 <= corr["bitcoin_number"] <= 9
        if "bitcoin_resonance" in corr:
            assert isinstance(corr["bitcoin_resonance"], int)
        if "chain_harmony" in corr:
            assert isinstance(corr["chain_harmony"], int)
            
        # Check ordinal data
        if "ordinal_numbers" in corr:
            assert all(1 <= n <= 9 for n in corr["ordinal_numbers"].values())
            
        # Check inscription data
        if "inscription_numbers" in corr:
            assert all(1 <= n <= 9 for n in corr["inscription_numbers"].values())
            
    # Check cross-system consistency
    bitcoin_numbers = {
        name: corr.get("bitcoin_number")
        for name, corr in correspondences.items()
        if "bitcoin_number" in corr
    }
    assert len(set(bitcoin_numbers.values())) == 1  # All systems should derive same Bitcoin number

def test_error_handling_consistency(mystical_systems):
    """Test that all systems handle errors consistently"""
    invalid_data = {
        "name": "TestGovernor",
        "txid": 12345,  # Invalid: should be string
        "ordinal_id": ["invalid"],  # Invalid: should be string
        "inscription_id": 67890  # Invalid: should be string
    }
    
    # All systems should reject invalid data
    for system in mystical_systems.values():
        assert system.validate_input(invalid_data) is False
        
    # All systems should handle missing Bitcoin data gracefully
    minimal_data = {"name": "TestGovernor", "birthdate": "2000-01-01"}
    for system in mystical_systems.values():
        try:
            profile = system.generate_profile(minimal_data)
            assert profile is not None
        except Exception as e:
            pytest.fail(f"System {system.name} failed to handle missing Bitcoin data: {e}")

def test_bitcoin_influence_calculation_consistency(mystical_systems, mock_governor_data):
    """Test that Bitcoin influence calculations are consistent"""
    txid = mock_governor_data["txid"]
    test_scores = [0.0, 0.3, 0.5, 0.7, 1.0]
    
    for base_score in test_scores:
        # Calculate influence across all systems
        influences = {
            name: system.calculate_bitcoin_influence(txid, base_score)
            for name, system in mystical_systems.items()
        }
        
        # All systems should produce same influence for same input
        assert len(set(influences.values())) == 1
        
        # Influence should be in valid range
        influence = next(iter(influences.values()))
        assert 0 <= influence <= 1.0
        
        # Influence should differ from base score
        assert influence != base_score 