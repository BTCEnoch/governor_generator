"""
Trait index mapping all defined governor traits from dossiers.
This serves as the single source of truth for all trait definitions.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

# PERSONA TRAITS
class Element(Enum):
    AIR = "Air"
    FIRE = "Fire"
    WATER = "Water" 
    EARTH = "Earth"
    SPIRIT = "Spirit"

@dataclass
class PersonaTraits:
    """Core identity traits that define who the governor is"""
    name: str
    title: str
    element: Element
    aethyr: str
    essence: str
    angelic_role: str

# KNOWLEDGE BASE
@dataclass 
class KnowledgeBase:
    """The governor's mystical knowledge and traditions"""
    traditions: List[str]  # e.g. hermetic_qabalah, enochian_magic, etc.

# ARCHETYPAL CORRESPONDENCES
@dataclass
class ArchetypalCorrespondences:
    """Sacred alignments and correspondences"""
    tarot: str
    sephirot: str
    zodiac_sign: str
    zodiac_angel: str
    numerology: int

# POLAR TRAITS
@dataclass
class PolarTraits:
    """Personality aspects and behaviors"""
    baseline_approach: str
    baseline_tone: str
    motive_alignment: str
    role_archetype: str
    orientation: str
    polarity: str
    self_regard: str
    virtues: List[str]
    flaws: List[str]

@dataclass
class Approaches:
    """Teaching and interaction approaches"""
    bad: str
    average: str
    good: str

@dataclass
class Tones:
    """Communication and presence tones"""
    bad: str
    average: str
    good: str

# VISUAL ASPECTS
@dataclass
class VisualForm:
    """Physical manifestation form"""
    name: str
    description: str

@dataclass
class VisualGeometry:
    """Sacred geometric patterns"""
    patterns: List[str]
    complexity: Optional[int]

@dataclass
class VisualEnvironment:
    """Environmental effects and influence"""
    effect_type: Optional[str]
    radius: Optional[str]
    intensity: Optional[str]

@dataclass
class VisualAspects:
    """Complete visual manifestation"""
    form: VisualForm
    color: str
    geometry: VisualGeometry
    environment: VisualEnvironment
    time_variations: Optional[str]
    energy_signature: Optional[str]
    symbol_set: Optional[str]
    light_shadow: Optional[str]
    special_properties: List[str]

@dataclass
class GovernorTraits:
    """Complete unified trait definition for a governor"""
    governor_name: str
    governor_id: str
    persona: PersonaTraits
    knowledge_base: KnowledgeBase
    archetypal_correspondences: ArchetypalCorrespondences
    polar_traits: PolarTraits
    approaches: Approaches
    tones: Tones
    visual_aspects: VisualAspects 