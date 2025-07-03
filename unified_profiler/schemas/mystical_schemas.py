from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

# Import existing tarot schemas
from mystical_systems.tarot_system.schemas.tarot_schemas import TarotCard, TarotSuit, CardPosition, TarotReading, GovernorTarotProfile

# =============================================================================
# KABBALAH & TREE OF LIFE SYSTEM
# =============================================================================

class SefirotPosition(Enum):
    KETER = "keter"           # Crown
    CHOKHMAH = "chokhmah"     # Wisdom  
    BINAH = "binah"           # Understanding
    CHESED = "chesed"         # Kindness/Mercy
    GEVURAH = "gevurah"       # Strength/Severity
    TIFERET = "tiferet"       # Beauty/Harmony
    NETZACH = "netzach"       # Victory/Eternity
    HOD = "hod"               # Glory/Splendor
    YESOD = "yesod"           # Foundation
    MALKHUT = "malkhut"       # Kingdom/Sovereignty

@dataclass
class Sefirah:
    # Required fields first
    position: SefirotPosition
    name: str
    hebrew_name: str
    number: int  # 1-10
    wikipedia_url: str
    divine_attribute: str
    human_attribute: str
    spiritual_meaning: str
    practical_meaning: str
    shadow_aspect: str
    # Optional fields with defaults
    element: Optional[str] = None
    planet: Optional[str] = None
    influence_categories: Optional[Dict[str, float]] = field(default_factory=dict)

# =============================================================================
# NUMEROLOGY SYSTEM
# =============================================================================

class NumerologySystem(Enum):
    PYTHAGOREAN = "pythagorean"
    CHALDEAN = "chaldean"

@dataclass
class NumerologyProfile:
    # Required fields first
    life_path_number: int  # 1-9, 11, 22, 33
    system: NumerologySystem
    wikipedia_url: str
    positive_traits: List[str]
    negative_traits: List[str]
    life_purpose: str
    spiritual_meaning: str
    compatible_numbers: List[int]
    challenging_numbers: List[int]
    # Optional fields with defaults
    influence_categories: Optional[Dict[str, float]] = field(default_factory=dict)

# =============================================================================
# WESTERN ZODIAC SYSTEM
# =============================================================================

class ZodiacElement(Enum):
    FIRE = "fire"
    EARTH = "earth"
    AIR = "air"
    WATER = "water"

class ZodiacModality(Enum):
    CARDINAL = "cardinal"
    FIXED = "fixed"
    MUTABLE = "mutable"

@dataclass
class ZodiacSign:
    # Required fields first
    name: str
    symbol: str
    dates: str  # e.g., "March 21 - April 19"
    element: ZodiacElement
    modality: ZodiacModality
    ruling_planet: str
    wikipedia_url: str
    positive_traits: List[str]
    negative_traits: List[str]
    keywords: List[str]
    # Optional fields with defaults
    tarot_correspondence: Optional[str] = None  # Major Arcana card
    body_parts: Optional[List[str]] = field(default_factory=list)
    colors: Optional[List[str]] = field(default_factory=list)
    stones: Optional[List[str]] = field(default_factory=list)
    influence_categories: Optional[Dict[str, float]] = field(default_factory=dict)

# =============================================================================
# UNIFIED MYSTICAL PROFILE
# =============================================================================

@dataclass
class CompleteMysticalProfile:
    # Required fields first
    governor_name: str
    tarot_profile: GovernorTarotProfile
    sefirot_influences: List[Sefirah]
    numerology_profile: NumerologyProfile
    zodiac_sign: ZodiacSign
    combined_personality_modifiers: Dict[str, float]
    unified_storyline_themes: List[str]
    mystical_synthesis: str
    elemental_balance: Dict[str, float]
    planetary_influences: List[str]
    archetypal_themes: List[str]

# =============================================================================
# ENHANCED READINGS SYSTEM
# =============================================================================

@dataclass
class MysticalReading:
    """Enhanced reading incorporating all mystical systems"""
    # Required fields first
    reading_type: str  # "complete_profile", "compatibility", "guidance"
    mystical_synthesis: str
    practical_guidance: str
    spiritual_insight: str
    timestamp: str
    systems_used: List[str]
    # Optional fields with defaults
    tarot_reading: Optional[TarotReading] = None
    sefirot_guidance: Optional[str] = None
    numerology_insight: Optional[str] = None
    zodiac_influence: Optional[str] = None 