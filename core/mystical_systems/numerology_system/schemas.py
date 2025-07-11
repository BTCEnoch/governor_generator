"""
Numerology System Schemas
"""

from typing import Dict, List, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field

from core.utils.mystical.base import MysticalAttribute

class NumerologySystem(str, Enum):
    """Numerology system types"""
    PYTHAGOREAN = "pythagorean"
    CHALDEAN = "chaldean"
    KABBALAH = "kabbalah"

class NumerologyProfile(BaseModel):
    """Numerology profile with Bitcoin integration"""
    name: str = Field(..., description="Name being analyzed")
    birthdate: str = Field(..., description="Birth date in YYYY-MM-DD format")
    life_path_number: int = Field(..., description="Life path number")
    destiny_number: int = Field(..., description="Destiny/expression number")
    soul_urge_number: int = Field(..., description="Soul urge/heart's desire number")
    personality_number: int = Field(..., description="Personality number")
    birth_day_number: int = Field(..., description="Birth day number")
    current_year_number: int = Field(..., description="Current year personal number")
    attributes: List[MysticalAttribute] = Field(default_factory=list, description="Mystical attributes")
    bitcoin_resonance: Optional[float] = Field(None, description="Bitcoin resonance score")
    chain_harmony: Optional[float] = Field(None, description="Blockchain harmony score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class NumerologySystemConfig(BaseModel):
    """Configuration for numerology system"""
    system_type: NumerologySystem = Field(
        default=NumerologySystem.PYTHAGOREAN,
        description="Type of numerology system to use"
    )
    use_bitcoin_influence: bool = Field(
        default=True,
        description="Whether to use Bitcoin for additional insights"
    )
    bitcoin_integration: Dict[str, Any] = Field(
        default_factory=dict,
        description="Bitcoin integration configuration"
    )
    art_generation: Dict[str, Any] = Field(
        default_factory=dict,
        description="Art generation configuration"
    ) 