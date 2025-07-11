"""
Schemas for ritual mechanics
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from enum import Enum

class Direction(str, Enum):
    """Cardinal and ordinal directions"""
    NORTH = "north"
    NORTHEAST = "northeast"
    EAST = "east"
    SOUTHEAST = "southeast"
    SOUTH = "south"
    SOUTHWEST = "southwest"
    WEST = "west"
    NORTHWEST = "northwest"

class RitualPoint(BaseModel):
    """A point in ritual space"""
    x: float = Field(ge=0.0, le=1.0, description="X coordinate (0-1)")
    y: float = Field(ge=0.0, le=1.0, description="Y coordinate (0-1)")
    energy_level: float = Field(ge=0.0, le=1.0, description="Energy level (0-1)")
    element: str = Field(description="Associated element")
    governor_influence: Optional[str] = Field(default=None, description="Influencing Governor")
    aethyr_resonance: str = Field(description="Resonating Aethyr")

class RitualPattern(BaseModel):
    """A pattern formed by ritual points"""
    points: List[RitualPoint] = Field(description="Points forming the pattern")
    pattern_type: str = Field(description="Type of pattern")
    total_energy: float = Field(ge=0.0, description="Total energy of the pattern")
    elements: List[str] = Field(description="Elements involved")
    governors: List[str] = Field(description="Governors involved")
    aethyrs: List[str] = Field(description="Aethyrs involved")
    bitcoin_entropy: str = Field(description="Bitcoin entropy used for validation")

class ValidationResult(BaseModel):
    """Result of ritual validation"""
    is_valid: bool = Field(description="Whether the ritual is valid")
    data: Dict = Field(description="Validation data")
    errors: List[str] = Field(description="Validation errors") 