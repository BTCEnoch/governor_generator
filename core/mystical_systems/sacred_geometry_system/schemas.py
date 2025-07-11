"""
Sacred Geometry System Schemas

This module defines the data models for the Sacred Geometry system.
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class GeometricForm(str, Enum):
    """Sacred geometric forms"""
    POINT = "point"  # 0D - Unity
    LINE = "line"  # 1D - Duality
    TRIANGLE = "triangle"  # 2D - Dynamic force
    SQUARE = "square"  # 2D - Material stability
    PENTAGON = "pentagon"  # 2D - Life force
    HEXAGON = "hexagon"  # 2D - Harmony
    CIRCLE = "circle"  # 2D - Wholeness
    VESICA_PISCIS = "vesica_piscis"  # 2D - Sacred intersection
    SEED_OF_LIFE = "seed_of_life"  # 2D - Genesis pattern
    FLOWER_OF_LIFE = "flower_of_life"  # 2D - Creation matrix
    METATRONS_CUBE = "metatrons_cube"  # 2D/3D - Archetypal forms
    TETRAHEDRON = "tetrahedron"  # 3D - Fire element
    CUBE = "cube"  # 3D - Earth element
    OCTAHEDRON = "octahedron"  # 3D - Air element
    DODECAHEDRON = "dodecahedron"  # 3D - Aether element
    ICOSAHEDRON = "icosahedron"  # 3D - Water element

class SacredProportion(str, Enum):
    """Sacred proportions and ratios"""
    PHI = "phi"  # Golden ratio (1.618...)
    PI = "pi"  # Circle ratio (3.14159...)
    SQRT2 = "sqrt2"  # Square root of 2 (1.414...)
    SQRT3 = "sqrt3"  # Square root of 3 (1.732...)
    SQRT5 = "sqrt5"  # Square root of 5 (2.236...)

class GeometryPattern(BaseModel):
    """A sacred geometry pattern with its properties"""
    form: GeometricForm
    proportions: List[SacredProportion]
    complexity: int = Field(..., ge=1, le=10, description="Pattern complexity (1-10)")
    dimensions: int = Field(..., ge=0, le=3, description="Pattern dimensions (0-3)")
    symmetry_order: int = Field(..., ge=1, description="Order of rotational symmetry")
    ritual_points: List[Dict[str, float]] = Field(
        ..., 
        description="Key points for ritual interaction"
    )
    power_level: int = Field(
        ..., 
        ge=1, 
        le=100, 
        description="Energy/power level (1-100)"
    )
    resonance: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="Bitcoin resonance (0.0-1.0)"
    )

class SacredGeometryProfile(BaseModel):
    """Complete sacred geometry reading/profile"""
    primary_form: GeometricForm
    secondary_forms: List[GeometricForm]
    patterns: List[GeometryPattern]
    dominant_proportion: SacredProportion
    power_centers: List[Dict[str, float]]
    resonance_score: float = Field(..., ge=0.0, le=1.0)
    ritual_complexity: int = Field(..., ge=1, le=10)
    governor_alignment: float = Field(..., ge=0.0, le=1.0)
    timestamp: str
    bitcoin_block_hash: str

class SacredGeometrySystemConfig(BaseModel):
    """Configuration for the Sacred Geometry system"""
    min_complexity: int = Field(1, ge=1, le=10)
    max_complexity: int = Field(10, ge=1, le=10)
    resonance_threshold: float = Field(0.7, ge=0.0, le=1.0)
    power_scale: int = Field(100, ge=1, le=1000)
    ritual_points_required: int = Field(3, ge=1, le=12)
    bitcoin_integration: Optional[Dict] = None 