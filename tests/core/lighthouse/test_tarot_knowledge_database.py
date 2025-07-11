#!/usr/bin/env python3
"""
Tests for the Tarot Tradition Knowledge Database
"""

import pytest
from pathlib import Path

from core.lighthouse.schemas.knowledge_schemas import (
    KnowledgeEntry,
    ProcessedTradition,
    KnowledgeType,
    ContentQuality
)

from core.governors.traits.knowledge_base.tarot_knowledge_database import (
    load_tarot_data,
    get_major_arcana_cards,
    get_minor_arcana_cards,
    get_court_cards,
    get_card_by_id,
    get_cards_by_element,
    get_cards_by_governor,
    get_tarot_spreads,
    get_correspondences,
    create_tarot_tradition
)

def test_load_tarot_data():
    """Test loading Tarot tradition data"""
    data = load_tarot_data()
    assert data is not None
    assert isinstance(data, dict)
    assert "core_systems" in data
    assert "cross_references" in data
    assert len(data["core_systems"]) > 0

def test_get_major_arcana_cards():
    """Test retrieving Major Arcana cards"""
    cards = get_major_arcana_cards()
    assert isinstance(cards, list)
    assert len(cards) > 0
    for card in cards:
        assert "id" in card
        assert "name" in card
        assert "number" in card
        assert "hebrew_letter" in card
        assert "astrological" in card
        assert "element" in card
        assert "path" in card
        assert "keywords" in card
        assert "description" in card
        assert "reversed_meaning" in card
        assert "governor_associations" in card

def test_get_minor_arcana_cards():
    """Test retrieving Minor Arcana cards"""
    # Test all cards
    all_cards = get_minor_arcana_cards()
    assert isinstance(all_cards, list)
    assert len(all_cards) > 0
    
    # Test specific suit
    wands = get_minor_arcana_cards("Wands")
    assert isinstance(wands, list)
    assert len(wands) > 0
    for card in wands:
        assert "wands" in card["id"].lower()
        assert "keywords" in card
        assert "description" in card

def test_get_court_cards():
    """Test retrieving Court cards"""
    # Test all court cards
    all_courts = get_court_cards()
    assert isinstance(all_courts, list)
    assert len(all_courts) > 0
    
    # Test specific rank
    pages = get_court_cards("Page")
    assert isinstance(pages, list)
    assert len(pages) > 0
    for card in pages:
        assert "page" in card["id"].lower()
        assert "keywords" in card
        assert "description" in card

def test_get_card_by_id():
    """Test retrieving a specific card by ID"""
    # Test Major Arcana card
    fool = get_card_by_id("major_00")
    assert fool is not None
    assert fool["name"] == "The Fool"
    assert fool["number"] == 0
    
    # Test Minor Arcana card
    ace_wands = get_card_by_id("wands_ace")
    assert ace_wands is not None
    assert ace_wands["name"] == "Ace of Wands"
    
    # Test nonexistent card
    assert get_card_by_id("nonexistent") is None

def test_get_cards_by_element():
    """Test retrieving cards by element"""
    fire_cards = get_cards_by_element("Fire")
    assert isinstance(fire_cards, list)
    assert len(fire_cards) > 0
    for card in fire_cards:
        if "element" in card:
            assert card["element"].lower() == "fire"

def test_get_cards_by_governor():
    """Test retrieving cards associated with a Governor"""
    cards = get_cards_by_governor("ARFAOLG")
    assert isinstance(cards, list)
    assert len(cards) > 0
    for card in cards:
        assert any("ARFAOLG" in gov for gov in card["governor_associations"])

def test_get_tarot_spreads():
    """Test retrieving Tarot spreads"""
    spreads = get_tarot_spreads()
    assert isinstance(spreads, list)
    assert len(spreads) > 0
    celtic_cross = next(s for s in spreads if s["name"] == "Celtic Cross")
    assert celtic_cross["positions"] == 10
    assert "LAIDROM" in celtic_cross["governor_associations"]

def test_get_correspondences():
    """Test retrieving Tarot correspondences"""
    correspondences = get_correspondences()
    assert isinstance(correspondences, dict)
    assert "tags" in correspondences
    assert "related_concepts" in correspondences
    assert "cross_references" in correspondences
    assert "kabbalah" in correspondences["cross_references"]
    assert "astrology" in correspondences["cross_references"]
    assert "enochian" in correspondences["cross_references"]

def test_create_tarot_tradition():
    """Test creating a complete ProcessedTradition object"""
    tradition = create_tarot_tradition()
    assert isinstance(tradition, ProcessedTradition)
    assert tradition.name == "Tarot Divination System"
    assert len(tradition.systems) > 0
    assert tradition.total_entries == len(tradition.systems)
    assert "kabbalah" in tradition.cross_references
    
    # Test a Major Arcana entry
    fool = next(
        entry for entry in tradition.systems 
        if entry.id == "major_00"
    )
    assert fool.title == "The Fool"
    assert fool.knowledge_type == KnowledgeType.SYSTEM
    assert fool.quality == ContentQuality.HIGH
    assert len(fool.tags) > 0
    assert len(fool.related_concepts) > 0
    
    # Test a Minor Arcana entry
    ace_wands = next(
        entry for entry in tradition.systems 
        if entry.id == "wands_ace"
    )
    assert ace_wands.title == "Ace of Wands"
    assert ace_wands.knowledge_type == KnowledgeType.SYSTEM
    assert ace_wands.quality == ContentQuality.HIGH
    assert len(ace_wands.tags) > 0 