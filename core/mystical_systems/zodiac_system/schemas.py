"""
Zodiac System Schemas
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from core.utils.mystical.schemas import MysticalSystemConfig
from core.utils.mystical.base import MysticalAttribute

class ZodiacElement(str, Enum):
    """Elements in Western astrology"""
    FIRE = "fire"
    EARTH = "earth"
    AIR = "air"
    WATER = "water"

class ZodiacModality(str, Enum):
    """Modalities (qualities) in Western astrology"""
    CARDINAL = "cardinal"
    FIXED = "fixed"
    MUTABLE = "mutable"

class ZodiacSign(BaseModel):
    """A single sign in the Western zodiac"""
    name: str = Field(..., description="Name of the zodiac sign")
    symbol: str = Field(..., description="Astrological symbol for the sign")
    dates: str = Field(..., description="Date range for the sign")
    element: ZodiacElement = Field(..., description="Element associated with the sign")
    modality: ZodiacModality = Field(..., description="Modality/quality of the sign")
    ruling_planet: str = Field(..., description="Planet that rules this sign")
    wikipedia_url: str = Field(..., description="Reference URL for the sign")
    positive_traits: List[str] = Field(default_factory=list, description="Positive characteristics")
    negative_traits: List[str] = Field(default_factory=list, description="Challenging characteristics")
    keywords: List[str] = Field(default_factory=list, description="Key themes and concepts")
    tarot_correspondence: str = Field(..., description="Associated tarot card")
    body_parts: List[str] = Field(default_factory=list, description="Associated body parts")
    colors: List[str] = Field(default_factory=list, description="Associated colors")
    stones: List[str] = Field(default_factory=list, description="Associated stones/crystals")
    influence_categories: Dict[str, float] = Field(
        default_factory=dict,
        description="Categories of influence with strength values"
    )

class ZodiacProfile(BaseModel):
    """Zodiac profile for a governor or entity"""
    # MysticalEntity base fields
    id: str = Field(..., description="Unique identifier for the profile")
    name: str = Field(..., description="Name of the profile")
    attributes: List[MysticalAttribute] = Field(default_factory=list, description="Mystical attributes")
    relationships: Dict[str, List[str]] = Field(default_factory=dict, description="Related entity IDs")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # Zodiac-specific fields
    sun_sign: str = Field(..., description="Primary zodiac sign")
    rising_sign: Optional[str] = Field(None, description="Ascendant sign if known")
    moon_sign: Optional[str] = Field(None, description="Lunar sign if known")
    elements: Dict[str, float] = Field(
        default_factory=dict,
        description="Distribution of elemental influences"
    )
    modalities: Dict[str, float] = Field(
        default_factory=dict,
        description="Distribution of modality influences"
    )
    ruling_planets: List[str] = Field(
        default_factory=list,
        description="Influential planets"
    )
    positive_traits: List[str] = Field(
        default_factory=list,
        description="Positive characteristics"
    )
    negative_traits: List[str] = Field(
        default_factory=list,
        description="Challenging characteristics"
    )
    keywords: List[str] = Field(
        default_factory=list,
        description="Key themes and concepts"
    )
    tarot_correspondences: List[str] = Field(
        default_factory=list,
        description="Associated tarot cards"
    )
    body_parts: List[str] = Field(
        default_factory=list,
        description="Associated body parts"
    )
    colors: List[str] = Field(
        default_factory=list,
        description="Associated colors"
    )
    stones: List[str] = Field(
        default_factory=list,
        description="Associated stones/crystals"
    )
    influence_categories: Dict[str, float] = Field(
        default_factory=dict,
        description="Categories of influence with strength values"
    )
    bitcoin_resonance: Optional[int] = Field(
        None,
        description="Bitcoin-derived resonance value"
    )
    chain_harmony: Optional[int] = Field(
        None,
        description="Blockchain harmony value"
    )
    ordinal_attributes: Dict[str, Any] = Field(
        default_factory=dict,
        description="Attributes derived from ordinals"
    )
    inscription_attributes: Dict[str, Any] = Field(
        default_factory=dict,
        description="Attributes derived from inscriptions"
    )
    zodiac_resonances: Dict[str, float] = Field(
        default_factory=dict,
        description="Resonance values with each zodiac sign"
    )

class ZodiacSystemConfig(BaseModel):
    """Configuration for the Zodiac system"""
    system_id: str = "zodiac"
    name: str = "Zodiac System"
    description: str = "Mystical system based on astrological zodiac"
    version: str = "1.0.0"
    use_bitcoin_influence: bool = True
    weights: Dict[str, float] = {
        "ordinal": 0.4,
        "txid": 0.5,
        "inscription": 0.1
    } 