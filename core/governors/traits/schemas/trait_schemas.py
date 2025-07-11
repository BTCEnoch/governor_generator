"""
Unified schemas for all governor traits.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class ElementType(Enum):
    """Elemental associations"""
    FIRE = "fire"
    WATER = "water" 
    AIR = "air"
    EARTH = "earth"
    SPIRIT = "spirit"

class AlignmentType(Enum):
    """Moral/ethical alignments"""
    LAWFUL_GOOD = "lawful_good"
    NEUTRAL_GOOD = "neutral_good"
    CHAOTIC_GOOD = "chaotic_good"
    LAWFUL_NEUTRAL = "lawful_neutral"
    TRUE_NEUTRAL = "true_neutral"
    CHAOTIC_NEUTRAL = "chaotic_neutral"
    LAWFUL_EVIL = "lawful_evil"
    NEUTRAL_EVIL = "neutral_evil"
    CHAOTIC_EVIL = "chaotic_evil"

@dataclass
class CanonicalTraits:
    """Core canonical traits that define a governor's essence"""
    name: str
    aethyr: str
    aethyr_number: int
    region: str
    correspondence: str
    personality: List[str]
    domain: str
    visual_motif: str
    letter_influence: List[str]
    version: str = "1.0.0"

@dataclass 
class EnhancedTraits:
    """Expanded definitions and context for canonical traits"""
    trait_name: str
    definition: str
    source: str
    correspondences: List[str]
    practical_application: str
    version: str = "1.0.0"

@dataclass
class MysticalTraits:
    """Mystical alignments and correspondences"""
    element: ElementType
    alignment: AlignmentType
    zodiac: str
    tarot: str
    sephirot: str
    angel: str
    number: int
    version: str = "1.0.0"

@dataclass
class PersonalityTraits:
    """Generated personality characteristics"""
    archetype: str
    primary_traits: List[str]
    secondary_traits: List[str]
    teaching_style: str
    approach: str
    tone: str
    version: str = "1.0.0"

@dataclass
class VisualTraits:
    """Visual manifestation aspects"""
    form_type: str
    color_scheme: str
    sacred_geometry: List[str]
    manifestation: str
    effects: List[str]
    version: str = "1.0.0"

@dataclass
class GovernorTraits:
    """Complete unified trait definition for a governor"""
    governor_id: str
    governor_number: int
    canonical: CanonicalTraits
    enhanced: Dict[str, EnhancedTraits]
    mystical: MysticalTraits
    personality: PersonalityTraits
    visual: VisualTraits
    version: str = "1.0.0"
    last_updated: Optional[str] = None  # ISO format timestamp 