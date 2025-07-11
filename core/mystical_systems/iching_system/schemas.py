"""
I Ching System Schemas
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class LineChange(str, Enum):
    """Type of line change in a hexagram"""
    STABLE_YIN = "stable_yin"    # Line value 8
    STABLE_YANG = "stable_yang"  # Line value 7
    YIN_TO_YANG = "yin_to_yang"  # Line value 6
    YANG_TO_YIN = "yang_to_yin"  # Line value 9

class HexagramLine(BaseModel):
    """Single line in a hexagram"""
    position: int = Field(..., ge=1, le=6)
    value: int = Field(..., ge=6, le=9)
    is_changing: bool
    change_type: LineChange
    meaning: Optional[str] = None

class IChingHexagram(BaseModel):
    """Complete hexagram representation"""
    number: int = Field(..., ge=1, le=64)
    binary: str = Field(..., min_length=6, max_length=6)
    unicode_char: str
    name: str
    description: str
    judgment: str
    image: str
    lines: List[HexagramLine]
    changing_lines: List[int]
    relationships: Dict[str, List[str]] = Field(default_factory=dict)

class IChingProfile(BaseModel):
    """Complete I Ching reading profile"""
    id: str
    name: str
    initial_hexagram: IChingHexagram
    transformed_hexagram: Optional[IChingHexagram] = None
    changing_line_meanings: List[str] = Field(default_factory=list)
    bitcoin_resonance: Optional[float] = None
    chain_harmony: Optional[float] = None
    governor_resonances: Dict[str, float] = Field(default_factory=dict)
    attributes: List[Dict[str, str]] = Field(default_factory=list)
    metadata: Dict[str, str] = Field(default_factory=dict)

class IChingSystemConfig(BaseModel):
    """Configuration for the I Ching system"""
    use_bitcoin_influence: bool = True
    use_yarrow_method: bool = False  # If False, use three-coin method
    default_coin_method: str = "three_coin"
    wikipedia_cache_ttl: int = 3600  # Cache Wikipedia data for 1 hour
    generate_art: bool = False 