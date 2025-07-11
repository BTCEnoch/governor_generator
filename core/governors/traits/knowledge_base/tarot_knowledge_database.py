#!/usr/bin/env python3
"""
Tarot Tradition Knowledge Database
Loads and processes Tarot tradition data from consolidated JSON format
"""

from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from core.lighthouse.schemas.knowledge_schemas import (
    KnowledgeEntry, 
    ProcessedTradition,
    KnowledgeType,
    ContentQuality
)

from core.utils.common.file_ops import safe_json_read
from core.utils.custom_logging import custom_logger

logger = custom_logger.setup_logger(__name__)

TAROT_JSON_PATH = Path("data/knowledge/archives/governor_archives/tarot_tradition.json")

def load_tarot_data() -> Optional[Dict]:
    """Load the consolidated Tarot tradition data"""
    try:
        data = safe_json_read(TAROT_JSON_PATH)
        logger.info(f"✅ Loaded Tarot tradition data from {TAROT_JSON_PATH}")
        return data
    except Exception as e:
        logger.error(f"❌ Failed to load Tarot tradition data: {e}")
        return None

def get_major_arcana_cards() -> List[Dict]:
    """Get all Major Arcana card data"""
    data = load_tarot_data()
    if data:
        for system in data["core_systems"]:
            if system["id"] == "tarot_major_arcana":
                return system["cards"]
    return []

def get_minor_arcana_cards(suit: Optional[str] = None) -> List[Dict]:
    """Get Minor Arcana cards, optionally filtered by suit"""
    data = load_tarot_data()
    if data:
        for system in data["core_systems"]:
            if system["id"] == "tarot_minor_arcana":
                if suit:
                    for suit_data in system["suits"]:
                        if suit_data["name"].lower() == suit.lower():
                            return suit_data["cards"]
                else:
                    all_cards = []
                    for suit_data in system["suits"]:
                        all_cards.extend(suit_data["cards"])
                    return all_cards
    return []

def get_court_cards(rank: Optional[str] = None) -> List[Dict]:
    """Get Court cards, optionally filtered by rank (Page, Knight, Queen, King)"""
    data = load_tarot_data()
    if data:
        for system in data["core_systems"]:
            if system["id"] == "tarot_court_cards":
                if rank:
                    for rank_data in system["courts"]:
                        if rank_data["rank"].lower() == rank.lower():
                            return rank_data["cards"]
                else:
                    all_cards = []
                    for rank_data in system["courts"]:
                        all_cards.extend(rank_data["cards"])
                    return all_cards
    return []

def get_card_by_id(card_id: str) -> Optional[Dict]:
    """Get a specific card by its ID"""
    # Check Major Arcana
    major_cards = get_major_arcana_cards()
    for card in major_cards:
        if card["id"] == card_id:
            return card
            
    # Check Minor Arcana
    minor_cards = get_minor_arcana_cards()
    for card in minor_cards:
        if card["id"] == card_id:
            return card
            
    # Check Court Cards
    court_cards = get_court_cards()
    for card in court_cards:
        if card["id"] == card_id:
            return card
            
    return None

def get_cards_by_element(element: str) -> List[Dict]:
    """Get all cards associated with a specific element"""
    cards = []
    
    # Check Major Arcana
    for card in get_major_arcana_cards():
        if card.get("element", "").lower() == element.lower():
            cards.append(card)
            
    # Check Minor Arcana suits
    data = load_tarot_data()
    if data:
        for system in data["core_systems"]:
            if system["id"] == "tarot_minor_arcana":
                for suit in system["suits"]:
                    if suit["element"].lower() == element.lower():
                        cards.extend(suit["cards"])
    
    return cards

def get_cards_by_governor(governor_name: str) -> List[Dict]:
    """Get all cards associated with a specific Governor"""
    cards = []
    
    # Check Major Arcana
    for card in get_major_arcana_cards():
        if governor_name in [gov.split(" - ")[0] for gov in card.get("governor_associations", [])]:
            cards.append(card)
            
    # Check Minor Arcana
    for card in get_minor_arcana_cards():
        if governor_name in [gov.split(" - ")[0] for gov in card.get("governor_associations", [])]:
            cards.append(card)
            
    # Check Court Cards
    for card in get_court_cards():
        if governor_name in [gov.split(" - ")[0] for gov in card.get("governor_associations", [])]:
            cards.append(card)
            
    return cards

def get_tarot_spreads() -> List[Dict]:
    """Get all available Tarot spreads"""
    data = load_tarot_data()
    if data:
        for system in data["core_systems"]:
            if system["id"] == "tarot_spreads":
                return system["spreads"]
    return []

def get_correspondences() -> Dict:
    """Get Tarot correspondences with other systems"""
    data = load_tarot_data()
    if data:
        for system in data["core_systems"]:
            if system["id"] == "tarot_correspondences":
                return {
                    "tags": system["tags"],
                    "related_concepts": system["related_concepts"],
                    "cross_references": system["cross_references"]
                }
    return {}

def create_tarot_tradition() -> ProcessedTradition:
    """Create a complete ProcessedTradition object for Tarot"""
    data = load_tarot_data()
    if not data:
        raise ValueError("Failed to load Tarot tradition data")
    
    entries = []
    
    # Process Major Arcana
    major_arcana = get_major_arcana_cards()
    for card in major_arcana:
        entry = KnowledgeEntry(
            id=card["id"],
            tradition="tarot",
            title=card["name"],
            summary=f"Major Arcana {card['number']}: {card['name']}",
            full_content=card["description"],
            knowledge_type=KnowledgeType.SYSTEM,
            tags=card["keywords"],
            related_concepts=[card["hebrew_letter"], card["astrological"], card["path"]],
            source_url="",
            confidence_score=0.95,
            quality=ContentQuality.HIGH,
            created_date=datetime.now().isoformat()
        )
        entries.append(entry)
    
    # Process Minor Arcana
    minor_arcana = get_minor_arcana_cards()
    for card in minor_arcana:
        entry = KnowledgeEntry(
            id=card["id"],
            tradition="tarot",
            title=card["name"],
            summary=card["name"],
            full_content=card["description"],
            knowledge_type=KnowledgeType.SYSTEM,
            tags=card["keywords"],
            related_concepts=[],
            source_url="",
            confidence_score=0.95,
            quality=ContentQuality.HIGH,
            created_date=datetime.now().isoformat()
        )
        entries.append(entry)
    
    tradition = ProcessedTradition(
        name=data["display_name"],
        description=data["description"],
        total_entries=len(entries),
        systems=entries,
        cross_references=data["cross_references"]
    )
    
    return tradition 