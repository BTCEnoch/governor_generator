"""Schemas for visual aspects data validation."""

from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field

class Point3D(BaseModel):
    """3D point schema"""
    x: float = Field(..., description="X coordinate")
    y: float = Field(..., description="Y coordinate")
    z: float = Field(..., description="Z coordinate")

class EffectSchema(BaseModel):
    """Game effect schema"""
    type: str = Field(..., description="Effect type")
    intensity: float = Field(..., ge=0, le=1, description="Effect intensity (0-1)")
    duration: float = Field(..., ge=0, description="Effect duration in seconds")
    radius: float = Field(..., ge=0, description="Effect radius in meters")

class DimensionalManifestationSchema(BaseModel):
    """Schema for dimensional manifestation data"""
    base_form: str = Field(..., description="Base form type")
    form_description: str = Field(..., description="Detailed form description")
    dimensional_variations: Dict[str, str] = Field(
        ...,
        description="Variations for different planes"
    )
    transition_effects: List[str] = Field(
        default_factory=list,
        description="Effects during form transitions"
    )
    constant_elements: List[str] = Field(
        default_factory=list,
        description="Elements present in all forms"
    )

class ColorSchemeSchema(BaseModel):
    """Schema for color scheme data"""
    primary_colors: List[str] = Field(..., description="Primary color list")
    elemental_association: str = Field(..., description="Associated element")
    intensity_levels: Dict[str, int] = Field(
        ...,
        description="Color intensity levels"
    )
    transition_effects: List[str] = Field(
        default_factory=list,
        description="Color transition effects"
    )

class GeometrySystemSchema(BaseModel):
    """Schema for geometry system data"""
    pattern_type: List[str] = Field(..., description="Sacred geometry patterns")
    complexity_level: int = Field(
        ...,
        ge=1,
        le=10,
        description="Pattern complexity (1-10)"
    )
    interaction_points: List[Point3D] = Field(
        ...,
        description="Points for ritual interaction"
    )
    power_requirements: Dict[str, int] = Field(
        ...,
        description="Power requirements per interaction"
    )

class EnvironmentalEffectSchema(BaseModel):
    """Schema for environmental effect data"""
    primary_effect: str = Field(..., description="Main environmental effect")
    radius: float = Field(..., ge=0, description="Effect radius in meters")
    duration: str = Field(..., description="Effect duration")
    intensity: str = Field(..., description="Effect intensity")
    secondary_effects: List[str] = Field(
        default_factory=list,
        description="Additional effects"
    )

class TimeVariationSchema(BaseModel):
    """Schema for time variation data"""
    astrological_influences: List[str] = Field(
        ...,
        description="Astrological conditions"
    )
    cycle_description: str = Field(..., description="Time cycle details")
    peak_manifestation: str = Field(..., description="Peak state description")
    dormant_manifestation: str = Field(..., description="Dormant state description")

class EnergySignatureSchema(BaseModel):
    """Schema for energy signature data"""
    frequency: str = Field(..., description="Energy frequency")
    polarity: str = Field(..., description="Energy polarity")
    intensity: str = Field(..., description="Energy intensity")
    special_properties: List[str] = Field(
        default_factory=list,
        description="Special energy properties"
    )

class SymbolSetSchema(BaseModel):
    """Schema for symbol set data"""
    sigils: List[str] = Field(..., description="Magical sigils")
    emblems: List[str] = Field(..., description="Power emblems")
    seals: List[str] = Field(..., description="Mystical seals")
    scripts: List[str] = Field(..., description="Sacred scripts")

class LightShadowSchema(BaseModel):
    """Schema for light/shadow dynamics data"""
    light_expression: str = Field(..., description="Light manifestation")
    shadow_interaction: str = Field(..., description="Shadow interaction")
    balance_point: str = Field(..., description="Light/shadow balance")
    special_effects: List[str] = Field(
        default_factory=list,
        description="Special lighting effects"
    )

class ScaleSystemSchema(BaseModel):
    """Schema for scale system data"""
    base_scale: str = Field(..., description="Base manifestation scale")
    plane_variations: Dict[str, str] = Field(
        ...,
        description="Scale variations per plane"
    )
    interaction_ranges: Dict[str, float] = Field(
        ...,
        description="Interaction distances"
    )
    ritual_requirements: Dict[str, str] = Field(
        ...,
        description="Scale requirements for rituals"
    )

class VisualAspectSchema(BaseModel):
    """Complete schema for visual aspects"""
    governor_id: str = Field(..., description="Unique governor identifier")
    dimensional: DimensionalManifestationSchema = Field(
        ...,
        description="Dimensional manifestation data"
    )
    color_scheme: ColorSchemeSchema = Field(
        ...,
        description="Color scheme data"
    )
    geometry: GeometrySystemSchema = Field(
        ...,
        description="Sacred geometry data"
    )
    environment: EnvironmentalEffectSchema = Field(
        ...,
        description="Environmental effects data"
    )
    time_variation: TimeVariationSchema = Field(
        ...,
        description="Time-based variation data"
    )
    energy: EnergySignatureSchema = Field(
        ...,
        description="Energy signature data"
    )
    symbols: SymbolSetSchema = Field(
        ...,
        description="Symbol set data"
    )
    light_shadow: LightShadowSchema = Field(
        ...,
        description="Light/shadow dynamics data"
    )
    scale: ScaleSystemSchema = Field(
        ...,
        description="Scale system data"
    )

    class Config:
        """Pydantic config"""
        schema_extra = {
            "example": {
                "governor_id": "VOANAMB",
                "dimensional": {
                    "base_form": "ETHEREAL",
                    "form_description": "Shifting prismatic mist",
                    "dimensional_variations": {
                        "etheric": "Luminous vapor",
                        "astral": "Crystalline cloud",
                        "mental": "Geometric pattern",
                        "causal": "Pure light"
                    },
                    "transition_effects": ["fade", "shimmer"],
                    "constant_elements": ["core glow"]
                },
                "color_scheme": {
                    "primary_colors": ["azure", "gold"],
                    "elemental_association": "air",
                    "intensity_levels": {
                        "low": 1,
                        "medium": 2,
                        "high": 3
                    },
                    "transition_effects": ["pulse"]
                },
                "geometry": {
                    "pattern_type": ["MERKABA"],
                    "complexity_level": 7,
                    "interaction_points": [
                        {"x": 0, "y": 0, "z": 0}
                    ],
                    "power_requirements": {
                        "activation": 100
                    }
                },
                "environment": {
                    "primary_effect": "sanctify",
                    "radius": 24.0,
                    "duration": "constant",
                    "intensity": "variable",
                    "secondary_effects": ["purify"]
                },
                "time_variation": {
                    "astrological_influences": ["venus"],
                    "cycle_description": "Dawn to dusk",
                    "peak_manifestation": "Noon",
                    "dormant_manifestation": "Midnight"
                },
                "energy": {
                    "frequency": "high",
                    "polarity": "positive",
                    "intensity": "strong",
                    "special_properties": ["healing"]
                },
                "symbols": {
                    "sigils": ["protection"],
                    "emblems": ["wisdom"],
                    "seals": ["binding"],
                    "scripts": ["celestial"]
                },
                "light_shadow": {
                    "light_expression": "radiant",
                    "shadow_interaction": "illuminating",
                    "balance_point": "twilight",
                    "special_effects": ["glow"]
                },
                "scale": {
                    "base_scale": "human",
                    "plane_variations": {
                        "physical": "normal",
                        "etheric": "large"
                    },
                    "interaction_ranges": {
                        "close": 1.0,
                        "far": 10.0
                    },
                    "ritual_requirements": {
                        "summoning": "large"
                    }
                }
            }
        } 