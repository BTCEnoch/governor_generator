"""
Kabbalah System Schemas
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from core.utils.mystical.schemas import MysticalSystemConfig
from core.utils.mystical.base import MysticalAttribute

class SefirotPosition(str, Enum):
    """Positions on the Tree of Life"""
    KETER = "keter"
    CHOKHMAH = "chokhmah"
    BINAH = "binah"
    CHESED = "chesed"
    GEVURAH = "gevurah"
    TIFERET = "tiferet"
    NETZACH = "netzach"
    HOD = "hod"
    YESOD = "yesod"
    MALKUTH = "malkuth"

class Sefirah(BaseModel):
    """A single Sefirah on the Tree of Life"""
    position: SefirotPosition = Field(..., description="Position on the Tree of Life")
    name: str = Field(..., description="English name")
    hebrew_name: str = Field(..., description="Hebrew name")
    number: int = Field(..., description="Numerical value")
    wikipedia_url: str = Field(..., description="Reference URL")
    divine_attribute: str = Field(..., description="Divine attribute or quality")
    human_attribute: str = Field(..., description="Human manifestation")
    spiritual_meaning: str = Field(..., description="Spiritual significance")
    practical_meaning: str = Field(..., description="Practical application")
    shadow_aspect: str = Field(..., description="Shadow or challenging aspect")
    element: str = Field(..., description="Associated element")
    planet: str = Field(..., description="Associated planet")
    influence_categories: Dict[str, float] = Field(
        default_factory=dict,
        description="Categories of influence with strength values"
    )
    keywords: List[str] = Field(
        default_factory=list,
        description="Key concepts and themes"
    )
    correspondences: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Additional mystical correspondences"
    )

class KabbalahProfile(BaseModel):
    """Kabbalah profile for a governor or entity"""
    # MysticalEntity base fields
    id: str = Field(..., description="Unique identifier for the profile")
    name: str = Field(..., description="Name of the profile")
    attributes: List[MysticalAttribute] = Field(default_factory=list, description="Mystical attributes")
    relationships: Dict[str, List[str]] = Field(default_factory=dict, description="Related entity IDs")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # Kabbalah-specific fields
    primary_sefirah: str = Field(..., description="Primary Sefirah position")
    secondary_sefirot: List[str] = Field(default_factory=list, description="Secondary Sefirah positions")
    divine_attributes: List[str] = Field(default_factory=list, description="Divine attributes")
    human_attributes: List[str] = Field(default_factory=list, description="Human attributes")
    spiritual_meanings: List[str] = Field(default_factory=list, description="Spiritual meanings")
    practical_meanings: List[str] = Field(default_factory=list, description="Practical applications")
    shadow_aspects: List[str] = Field(default_factory=list, description="Shadow aspects")
    elements: List[str] = Field(default_factory=list, description="Associated elements")
    planets: List[str] = Field(default_factory=list, description="Associated planets")
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
    sefirot_resonances: Dict[str, float] = Field(
        default_factory=dict,
        description="Resonance values with each Sefirah"
    )

class KabbalahSystemConfig(MysticalSystemConfig):
    """Configuration for the Kabbalah system"""
    # Base fields from MysticalSystemConfig
    system_id: str = Field(
        default="kabbalah_system_v1",
        description="Unique identifier for the mystical system"
    )
    name: str = Field(
        default="Kabbalah System",
        description="Human-readable name of the system"
    )
    description: str = Field(
        default="A Bitcoin-integrated Kabbalah system for mystical analysis and divination",
        description="Description of the system's purpose and capabilities"
    )
    version: str = Field(
        default="1.0.0",
        description="System version number"
    )
    capabilities: List[str] = Field(
        default=[
            "sefirot_analysis",
            "bitcoin_integration",
            "trait_analysis",
            "mystical_correspondences"
        ],
        description="List of system capabilities"
    )
    
    # Kabbalah-specific fields
    use_bitcoin_influence: bool = Field(
        default=True,
        description="Whether to use Bitcoin-derived values for calculations"
    )
    default_sefirah: str = Field(
        default="tiferet",
        description="Default Sefirah to use when no other data is available"
    )
    influence_weights: Dict[str, float] = Field(
        default_factory=lambda: {
            "traits": 0.4,
            "bitcoin": 0.3,
            "ordinal": 0.2,
            "inscription": 0.1
        },
        description="Weights for different influence sources"
    ) 