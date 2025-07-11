"""
Tests for the Tarot Reading Engine
"""

import pytest
from datetime import datetime
from pathlib import Path

from core.mystical_systems.tarot_system.engines.reading_engine import ReadingEngine
from core.mystical_systems.tarot_system.spreads.spread_definitions import SpreadType
from core.mystical_systems.tarot_system.tarot_system import TarotSystem

def test_reading_engine_initialization():
    """Test reading engine initialization"""
    tarot_system = TarotSystem()
    engine = ReadingEngine(tarot_system)
    assert engine.tarot_system is not None
    assert engine.card_data is not None
    assert len(engine.card_data) > 0  # Should have loaded cards

def test_card_data_loading():
    """Test card data is loaded correctly"""
    tarot_system = TarotSystem()
    engine = ReadingEngine(tarot_system)
    
    # Check major arcana
    assert "the_fool" in engine.card_data
    assert "the_magician" in engine.card_data
    
    # Check suits
    assert "ace_of_wands" in engine.card_data
    assert "ace_of_cups" in engine.card_data
    assert "ace_of_swords" in engine.card_data
    assert "ace_of_pentacles" in engine.card_data

@pytest.mark.parametrize("spread_type", [
    SpreadType.THREE_CARD,
    SpreadType.CELTIC_CROSS,
    SpreadType.GOVERNORS_GUIDANCE
])
def test_generate_reading(spread_type):
    """Test reading generation for different spreads"""
    tarot_system = TarotSystem()
    engine = ReadingEngine(tarot_system)
    
    # Generate reading
    reading = engine.generate_reading(
        spread_type=spread_type,
        question="What guidance do I need right now?",
        seed="test_seed_123"  # Use fixed seed for reproducibility
    )
    
    # Check reading structure
    assert reading.id.startswith("reading_")
    assert isinstance(reading.timestamp, datetime)
    assert reading.spread_type == spread_type
    assert reading.question == "What guidance do I need right now?"
    
    # Check cards
    assert len(reading.cards) > 0
    for card in reading.cards:
        assert card.card_id in engine.card_data
        assert card.position_name
        assert card.position_meaning
        assert card.element in ["Fire", "Water", "Air", "Earth", "Spirit"]
        assert isinstance(card.upright, bool)
        assert card.interpretation
        assert isinstance(card.elemental_resonance, float)
        assert isinstance(card.governor_resonance, float)
    
    # Check narrative
    assert reading.narrative_summary
    assert reading.overall_theme
    assert len(reading.guidance_points) > 0
    
    # Check elemental balance
    assert all(0 <= v <= 1 for v in reading.elemental_balance.values())
    assert abs(sum(reading.elemental_balance.values()) - 1.0) < 0.0001

def test_governor_influenced_reading():
    """Test reading with governor influence"""
    tarot_system = TarotSystem()
    engine = ReadingEngine(tarot_system)
    
    governor_data = {
        "name": "ADVORPT",
        "element": "Fire",
        "domain": "Wisdom"
    }
    
    reading = engine.generate_reading(
        spread_type=SpreadType.GOVERNORS_GUIDANCE,
        question="What is my spiritual path?",
        governor_data=governor_data,
        seed="test_seed_456"
    )
    
    # Check governor influences
    assert reading.metadata["governor_influenced"] is True
    assert any("ADVORPT" in influence for influence in reading.governor_influences.keys())
    
    # Check narrative includes governor
    assert "ADVORPT" in reading.narrative_summary
    assert any("ADVORPT" in point for point in reading.guidance_points)

def test_reading_reproducibility():
    """Test that readings are reproducible with same seed"""
    tarot_system = TarotSystem()
    engine = ReadingEngine(tarot_system)
    seed = "test_seed_789"
    
    # Generate two readings with same seed
    reading1 = engine.generate_reading(
        spread_type=SpreadType.THREE_CARD,
        seed=seed
    )
    
    reading2 = engine.generate_reading(
        spread_type=SpreadType.THREE_CARD,
        seed=seed
    )
    
    # Check cards are same
    for card1, card2 in zip(reading1.cards, reading2.cards):
        assert card1.card_id == card2.card_id
        assert card1.upright == card2.upright
        assert card1.interpretation == card2.interpretation

def test_elemental_resonance():
    """Test elemental resonance calculations"""
    tarot_system = TarotSystem()
    engine = ReadingEngine(tarot_system)
    
    # Generate reading with fixed seed
    reading = engine.generate_reading(
        spread_type=SpreadType.THREE_CARD,
        seed="test_seed_resonance"
    )
    
    # Check resonances
    for card in reading.cards:
        assert 0 <= card.elemental_resonance <= 1
        if card.element == card.position_name:
            assert card.elemental_resonance > 0.5  # Higher resonance for matching elements

def test_error_handling():
    """Test error handling in reading generation"""
    tarot_system = TarotSystem()
    engine = ReadingEngine(tarot_system)
    
    # Test invalid spread type
    with pytest.raises(KeyError):
        # Using an invalid enum value to test error handling
        invalid_type = SpreadType("invalid_spread")  # This will raise ValueError
        engine.generate_reading(spread_type=invalid_type)
    
    # Test missing card data
    engine.card_data = {}  # Clear card data
    with pytest.raises(ValueError):
        engine.generate_reading(spread_type=SpreadType.THREE_CARD) 