"""
Tests for Bitcoin-integrated Mystical System Base Class
"""

import pytest
from typing import Dict, Any
from core.utils.mystical_systems.base import BitcoinMysticalSystem, MysticalAttribute

class TestBitcoinSystem(BitcoinMysticalSystem):
    """Test implementation of BitcoinMysticalSystem"""
    
    def __init__(self, config: Dict[str, Any] = {}):
        super().__init__("test_system", config)
        
    def validate_input(self, data: Any) -> bool:
        return True
        
    def format_output(self, result: Any) -> Any:
        return result
        
    def calculate_correspondences(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return data

@pytest.fixture
def bitcoin_system():
    """Create a test BitcoinMysticalSystem instance"""
    return TestBitcoinSystem()

@pytest.fixture
def mock_txid():
    """Create a mock Bitcoin transaction ID"""
    return "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

def test_generate_deterministic_seed(bitcoin_system, mock_txid):
    """Test deterministic seed generation"""
    seed1 = bitcoin_system.generate_deterministic_seed(mock_txid)
    seed2 = bitcoin_system.generate_deterministic_seed(mock_txid)
    
    # Same input should produce same seed
    assert seed1 == seed2
    assert len(seed1) == 32  # SHA-256 produces 32 bytes
    
    # Different input should produce different seed
    different_seed = bitcoin_system.generate_deterministic_seed(mock_txid + "1")
    assert seed1 != different_seed

def test_derive_mystical_attributes(bitcoin_system, mock_txid):
    """Test mystical attribute derivation from Bitcoin data"""
    attributes = bitcoin_system.derive_mystical_attributes(mock_txid)
    
    # Check we have all expected attributes
    assert len(attributes) == 5
    attribute_names = {attr.name for attr in attributes}
    expected_names = {
        "bitcoin_resonance",
        "chain_harmony",
        "elemental_affinity",
        "celestial_influence",
        "temporal_cycle"
    }
    assert attribute_names == expected_names
    
    # Check bitcoin_resonance attribute
    resonance = next(a for a in attributes if a.name == "bitcoin_resonance")
    assert isinstance(resonance.value, int)
    assert "vibrational_frequency" in resonance.correspondences
    assert "harmonic_pattern" in resonance.correspondences
    assert "numerological_sum" in resonance.correspondences
    assert 0 <= resonance.correspondences["vibrational_frequency"] < 144
    assert len(resonance.correspondences["harmonic_pattern"]) == 8
    assert 0 <= resonance.correspondences["numerological_sum"] <= 36  # Max sum of 4 digits
    
    # Check chain_harmony attribute
    harmony = next(a for a in attributes if a.name == "chain_harmony")
    assert isinstance(harmony.value, int)
    assert 0 <= harmony.correspondences["harmonic_ratio"] <= 1.0
    assert len(harmony.correspondences["resonance_pattern"]) == 7
    assert 0 <= harmony.correspondences["cyclic_position"] < 28
    
    # Check elemental_affinity attribute
    elemental = next(a for a in attributes if a.name == "elemental_affinity")
    assert elemental.value in ["fire", "water", "air", "earth"]
    assert 0 <= elemental.correspondences["strength"] <= 1.0
    assert elemental.correspondences["polarity"] in ["active", "passive"]
    assert elemental.correspondences["quality"] in ["hot", "cold"]
    
    # Check celestial_influence attribute
    celestial = next(a for a in attributes if a.name == "celestial_influence")
    assert celestial.value in ["solar", "lunar", "stellar"]
    assert 0 <= celestial.correspondences["strength"] <= 1.0
    assert 0 <= celestial.correspondences["phase"] < 8
    assert 0 <= celestial.correspondences["aspect"] < 12
    
    # Check temporal_cycle attribute
    temporal = next(a for a in attributes if a.name == "temporal_cycle")
    assert temporal.value in ["dawn", "noon", "dusk", "night"]
    assert 0 <= temporal.correspondences["strength"] <= 1.0
    assert 0 <= temporal.correspondences["hour"] < 24
    assert 0 <= temporal.correspondences["day"] < 7

def test_bind_to_ordinal(bitcoin_system):
    """Test binding to Bitcoin ordinal"""
    ordinal_id = "ord1234567890"
    bitcoin_system.bind_to_ordinal(ordinal_id)
    
    assert "mystical_properties" in bitcoin_system.ordinal_data
    props = bitcoin_system.ordinal_data["mystical_properties"]
    
    # Check all expected properties are present
    assert 0 <= props["sat_degree"] < 360
    assert 0 <= props["sat_cycle"] < 28
    assert props["sat_element"] in ["fire", "earth", "air", "water"]
    assert props["sat_quality"] in ["cardinal", "fixed", "mutable"]
    assert len(props["sat_resonance"]) == 12
    assert 0 <= props["sat_harmonic"] < 22

def test_bind_to_inscription(bitcoin_system):
    """Test binding to Bitcoin inscription"""
    inscription_id = "ins1234567890"
    bitcoin_system.bind_to_inscription(inscription_id)
    
    assert "mystical_properties" in bitcoin_system.inscription_data
    props = bitcoin_system.inscription_data["mystical_properties"]
    
    # Check all expected properties are present
    assert 0 <= props["inscription_phase"] < 8
    assert props["inscription_element"] in ["fire", "earth", "air", "water"]
    assert props["inscription_planet"] in ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"]
    assert 0 <= props["inscription_path"] < 22
    assert len(props["inscription_pattern"]) == 7
    assert 0 <= props["inscription_seal"] < 49

def test_calculate_bitcoin_influence(bitcoin_system, mock_txid):
    """Test Bitcoin influence calculation"""
    test_scores = [0.0, 0.3, 0.5, 0.7, 1.0]
    
    for base_score in test_scores:
        modified_score = bitcoin_system.calculate_bitcoin_influence(mock_txid, base_score)
        
        # Check score remains in valid range
        assert 0 <= modified_score <= 1.0
        
        # Check influence is applied (score should change)
        assert modified_score != base_score
        
        # Check golden ratio weighting
        # Modified score should be closer to original than to Bitcoin influence
        bitcoin_score = int.from_bytes(bitcoin_system.generate_deterministic_seed(mock_txid)[:4], 'big') / (2**32)
        assert abs(modified_score - base_score) < abs(modified_score - bitcoin_score)

def test_get_bitcoin_correspondences(bitcoin_system, mock_txid):
    """Test comprehensive Bitcoin correspondence generation"""
    correspondences = bitcoin_system.get_bitcoin_correspondences(mock_txid)
    
    # Check all major sections are present
    assert "resonance" in correspondences
    assert "elements" in correspondences
    assert "celestial" in correspondences
    assert "temporal" in correspondences
    
    # Check resonance section
    assert isinstance(correspondences["resonance"]["primary"], int)
    assert isinstance(correspondences["resonance"]["secondary"], int)
    assert "patterns" in correspondences["resonance"]
    assert "vibrational" in correspondences["resonance"]["patterns"]
    assert "harmonic" in correspondences["resonance"]["patterns"]
    assert "numerological" in correspondences["resonance"]["patterns"]
    
    # Check elements section
    assert correspondences["elements"]["primary"] in ["fire", "water", "air", "earth"]
    assert 0 <= correspondences["elements"]["strength"] <= 1.0
    assert correspondences["elements"]["polarity"] in ["active", "passive"]
    assert correspondences["elements"]["quality"] in ["hot", "cold"]
    
    # Check celestial section
    assert correspondences["celestial"]["body"] in ["solar", "lunar", "stellar"]
    assert 0 <= correspondences["celestial"]["strength"] <= 1.0
    assert 0 <= correspondences["celestial"]["phase"] < 8
    assert 0 <= correspondences["celestial"]["aspect"] < 12
    
    # Check temporal section
    assert correspondences["celestial"]["body"] in ["solar", "lunar", "stellar"]
    assert 0 <= correspondences["temporal"]["strength"] <= 1.0
    assert 0 <= correspondences["temporal"]["hour"] < 24
    assert 0 <= correspondences["temporal"]["day"] < 7
    
    # Bind to ordinal and check ordinal correspondences
    bitcoin_system.bind_to_ordinal("ord1234567890")
    correspondences = bitcoin_system.get_bitcoin_correspondences(mock_txid)
    assert "ordinal" in correspondences
    assert "sat_degree" in correspondences["ordinal"]
    assert "sat_element" in correspondences["ordinal"]
    
    # Bind to inscription and check inscription correspondences
    bitcoin_system.bind_to_inscription("ins1234567890")
    correspondences = bitcoin_system.get_bitcoin_correspondences(mock_txid)
    assert "inscription" in correspondences
    assert "inscription_phase" in correspondences["inscription"]
    assert "inscription_element" in correspondences["inscription"] 