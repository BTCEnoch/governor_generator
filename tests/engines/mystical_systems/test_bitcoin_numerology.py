"""
Tests for Bitcoin integration with Numerology system
"""

import pytest
from typing import Dict, Any

from core.mystical_systems.numerology_system.numerology_system import NumerologySystem
from core.mystical_systems.numerology_system.schemas import NumerologyProfile

@pytest.fixture
def numerology_system():
    """Create a NumerologySystem instance for testing"""
    return NumerologySystem()

@pytest.fixture
def mock_governor_data():
    """Create mock governor data with Bitcoin attributes"""
    return {
        "name": "TestGovernor",
        "birthdate": "2000-01-01",
        "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "ordinal_id": "ord1234567890",
        "inscription_id": "ins1234567890"
    }

def test_numerology_system_initialization(numerology_system):
    """Test NumerologySystem initialization"""
    assert isinstance(numerology_system, NumerologySystem)
    system_info = numerology_system.get_system_info()
    assert system_info["system_id"] == "numerology_system_v1"

def test_validate_input_with_bitcoin_data(numerology_system, mock_governor_data):
    """Test input validation with Bitcoin data"""
    assert numerology_system.validate_input(mock_governor_data) is True

def test_validate_input_invalid_bitcoin_data(numerology_system):
    """Test input validation with invalid Bitcoin data"""
    invalid_data = {
        "name": "TestGovernor",
        "birthdate": "2000-01-01",
        "txid": 12345,  # Should be string
        "ordinal_id": ["invalid"],  # Should be string
        "inscription_id": 67890  # Should be string
    }
    assert numerology_system.validate_input(invalid_data) is False

def test_generate_profile_with_bitcoin_data(numerology_system, mock_governor_data):
    """Test profile generation with Bitcoin data"""
    profile = numerology_system.generate_profile(mock_governor_data)
    
    # Check Bitcoin-specific attributes
    assert isinstance(profile, NumerologyProfile)
    assert profile.bitcoin_number is not None
    assert 1 <= profile.bitcoin_number <= 9  # Life path numbers are 1-9
    assert profile.bitcoin_resonance is not None
    assert profile.chain_harmony is not None
    assert profile.ordinal_numbers != {}
    assert profile.inscription_numbers != {}
    assert profile.numerological_patterns != {}
    
    # Check system type updated to Bitcoin
    assert profile.system == NumerologySystem.BITCOIN
    
    # Check traditional numerology still works
    assert profile.life_path_number > 0
    assert profile.positive_traits
    assert profile.negative_traits
    assert profile.life_purpose
    assert profile.spiritual_meaning
    assert profile.compatible_numbers
    assert profile.challenging_numbers
    
    # Check numerological patterns
    patterns = profile.numerological_patterns
    assert "resonance_sequence" in patterns
    assert "harmony_sequence" in patterns
    assert "combined_roots" in patterns
    assert len(patterns["resonance_sequence"]) == 9  # Last 9 digits
    assert len(patterns["harmony_sequence"]) == 9
    assert all(1 <= n <= 9 for n in patterns["combined_roots"])  # Life path numbers
    
    # Check ordinal numbers
    assert "primary" in profile.ordinal_numbers
    assert "secondary" in profile.ordinal_numbers
    assert "tertiary" in profile.ordinal_numbers
    assert all(1 <= n <= 9 for n in profile.ordinal_numbers.values())
    
    # Check inscription numbers
    assert "primary" in profile.inscription_numbers
    assert "secondary" in profile.inscription_numbers
    assert "tertiary" in profile.inscription_numbers
    assert all(1 <= n <= 9 for n in profile.inscription_numbers.values())
    
    # Check relationships
    assert "ordinal" in profile.relationships
    assert "inscription" in profile.relationships
    assert profile.relationships["ordinal"] == ["ord1234567890"]
    assert profile.relationships["inscription"] == ["ins1234567890"]
    
    # Check metadata
    assert profile.metadata["calculation_method"] == "bitcoin_pythagorean"
    assert profile.metadata["bitcoin_derived"] is True
    assert profile.metadata["ordinal_bound"] is True
    assert profile.metadata["inscription_bound"] is True

def test_generate_profile_without_bitcoin_data(numerology_system):
    """Test profile generation without Bitcoin data"""
    basic_data = {
        "name": "TestGovernor",
        "birthdate": "2000-01-01"
    }
    profile = numerology_system.generate_profile(basic_data)
    
    # Check Bitcoin-specific attributes are None/empty
    assert profile.bitcoin_number is None
    assert profile.bitcoin_resonance is None
    assert profile.chain_harmony is None
    assert profile.ordinal_numbers == {}
    assert profile.inscription_numbers == {}
    assert profile.numerological_patterns == {}
    
    # Check system type remains Pythagorean
    assert profile.system == NumerologySystem.PYTHAGOREAN
    
    # Check traditional numerology works
    assert profile.life_path_number > 0
    assert profile.positive_traits
    assert profile.negative_traits
    assert profile.life_purpose
    assert profile.spiritual_meaning
    
    # Check relationships
    assert profile.relationships["ordinal"] == []
    assert profile.relationships["inscription"] == []
    
    # Check metadata
    assert profile.metadata["calculation_method"] == "pythagorean"
    assert profile.metadata["bitcoin_derived"] is False
    assert profile.metadata["ordinal_bound"] is False
    assert profile.metadata["inscription_bound"] is False

def test_calculate_correspondences_with_bitcoin(numerology_system, mock_governor_data):
    """Test correspondence calculation with Bitcoin data"""
    correspondences = numerology_system.calculate_correspondences(mock_governor_data)
    
    # Check traditional correspondences
    assert "life_path" in correspondences
    assert "traits" in correspondences
    assert "purpose" in correspondences
    assert "name_number" in correspondences
    assert "name_traits" in correspondences
    
    # Check Bitcoin-specific correspondences
    assert "bitcoin_number" in correspondences
    assert 1 <= correspondences["bitcoin_number"] <= 9
    assert "bitcoin_resonance" in correspondences
    assert "chain_harmony" in correspondences
    assert "numerological_patterns" in correspondences
    assert "bitcoin_compatibility" in correspondences
    assert 0 <= correspondences["bitcoin_compatibility"] <= 1.0
    
    # Check ordinal correspondences
    assert "ordinal_numbers" in correspondences
    assert "primary" in correspondences["ordinal_numbers"]
    assert "secondary" in correspondences["ordinal_numbers"]
    assert "tertiary" in correspondences["ordinal_numbers"]
    
    # Check inscription correspondences
    assert "inscription_numbers" in correspondences
    assert "primary" in correspondences["inscription_numbers"]
    assert "secondary" in correspondences["inscription_numbers"]
    assert "tertiary" in correspondences["inscription_numbers"]

def test_calculate_correspondences_without_bitcoin(numerology_system):
    """Test correspondence calculation without Bitcoin data"""
    basic_data = {
        "name": "TestGovernor",
        "birthdate": "2000-01-01"
    }
    correspondences = numerology_system.calculate_correspondences(basic_data)
    
    # Check traditional correspondences exist
    assert "life_path" in correspondences
    assert "traits" in correspondences
    assert "purpose" in correspondences
    assert "name_number" in correspondences
    assert "name_traits" in correspondences
    
    # Check Bitcoin-specific correspondences are absent
    assert "bitcoin_number" not in correspondences
    assert "bitcoin_resonance" not in correspondences
    assert "chain_harmony" not in correspondences
    assert "numerological_patterns" not in correspondences
    assert "bitcoin_compatibility" not in correspondences
    assert "ordinal_numbers" not in correspondences
    assert "inscription_numbers" not in correspondences

def test_extract_numerological_patterns(numerology_system):
    """Test numerological pattern extraction"""
    resonance = 123456789
    harmony = 987654321
    
    patterns = numerology_system._extract_numerological_patterns(resonance, harmony)
    
    # Check pattern structure
    assert "resonance_sequence" in patterns
    assert "harmony_sequence" in patterns
    assert "combined_roots" in patterns
    
    # Check sequence lengths
    assert len(patterns["resonance_sequence"]) == 9
    assert len(patterns["harmony_sequence"]) == 9
    assert len(patterns["combined_roots"]) == 9
    
    # Check sequence values
    assert patterns["resonance_sequence"] == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert patterns["harmony_sequence"] == [9, 8, 7, 6, 5, 4, 3, 2, 1]
    
    # Check combined roots are valid life path numbers
    assert all(1 <= n <= 9 for n in patterns["combined_roots"])

def test_calculate_number_compatibility(numerology_system):
    """Test numerological compatibility calculation"""
    # Test same numbers
    assert numerology_system._calculate_number_compatibility(1, 1) == 1.0
    assert numerology_system._calculate_number_compatibility(9, 9) == 1.0
    
    # Test adjacent numbers
    assert numerology_system._calculate_number_compatibility(1, 2) == 0.8
    assert numerology_system._calculate_number_compatibility(8, 9) == 0.8
    
    # Test complementary numbers (sum to 9)
    assert numerology_system._calculate_number_compatibility(1, 8) == 0.7
    assert numerology_system._calculate_number_compatibility(2, 7) == 0.7
    assert numerology_system._calculate_number_compatibility(3, 6) == 0.7
    assert numerology_system._calculate_number_compatibility(4, 5) == 0.7
    
    # Test other combinations
    assert numerology_system._calculate_number_compatibility(1, 5) == 0.5
    assert numerology_system._calculate_number_compatibility(2, 8) == 0.5
    assert numerology_system._calculate_number_compatibility(3, 7) == 0.5 