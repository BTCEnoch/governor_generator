from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum

class TarotSuit(Enum):
    MAJOR_ARCANA = "major_arcana"
    WANDS = "wands"
    CUPS = "cups" 
    SWORDS = "swords"
    PENTACLES = "pentacles"

class CardPosition(Enum):
    UPRIGHT = "upright"
    REVERSED = "reversed"

@dataclass
class TarotCard:
    id: str  # e.g., "fool", "ace_of_wands"
    name: str  # e.g., "The Fool", "Ace of Wands"
    suit: TarotSuit
    number: Optional[int]  # None for Major Arcana, 1-14 for Minor
    wikipedia_url: str
    
    # Core meanings
    upright_keywords: List[str]
    reversed_keywords: List[str]
    upright_meaning: str
    reversed_meaning: str
    
    # Symbolic associations
    element: Optional[str] = None  # Fire, Water, Air, Earth
    planet: Optional[str] = None
    zodiac: Optional[str] = None
    hebrew_letter: Optional[str] = None
    tree_of_life_path: Optional[int] = None
    
    # Governor influence weights
    influence_categories: Optional[Dict[str, float]] = None

@dataclass 
class GovernorTarotProfile:
    governor_name: str
    primary_card: TarotCard  # Main influence
    secondary_cards: List[TarotCard]  # 2-3 supporting influences
    shadow_card: TarotCard  # Hidden/challenging aspect
    
    # Calculated influences
    personality_modifiers: Dict[str, float]
    storyline_themes: List[str]
    magical_affinities: List[str]
    
@dataclass
class TarotReading:
    spread_type: str  # "three_card", "celtic_cross"
    cards_drawn: List[Tuple[TarotCard, CardPosition]]
    interpretation: str
    themes: List[str]
    advice: str
    timestamp: str 