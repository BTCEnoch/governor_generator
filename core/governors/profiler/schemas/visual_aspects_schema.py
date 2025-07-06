"""
Schema definitions for Governor Visual Aspects.

This module defines the data structures and validation rules for Governor visual appearances
across different dimensions and manifestations.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum

class FormType(Enum):
    """Base form types a Governor can manifest as"""
    ETHEREAL = "ethereal"  # Pure energy/light forms
    GEOMETRIC = "geometric"  # Sacred geometry based
    ABSTRACT = "abstract"  # Non-euclidean/conceptual
    COMPOSITE = "composite"  # Multiple forms combined
    METAMORPHIC = "metamorphic"  # Shape-shifting/fluid
    SYMBOLIC = "symbolic"  # Manifests as pure symbols
    ELEMENTAL = "elemental"  # Pure elemental form
    OTHER = "other"  # Unique/special cases

class ColorScheme(Enum):
    """Primary color energies and auras"""
    GOLDEN = "golden"
    SILVER = "silver"
    PRISMATIC = "prismatic"
    OPALESCENT = "opalescent"
    CRYSTALLINE = "crystalline"
    VOID = "void"  # Absence of color/deep space
    PLASMA = "plasma"  # Living color/shifting
    CUSTOM = "custom"  # Unique color descriptions

class GeometryPattern(Enum):
    """Sacred geometry base patterns"""
    METATRON = "metatron"  # Metatron's Cube
    FLOWER_OF_LIFE = "flower_of_life"
    MERKABA = "merkaba"
    TORUS = "torus"
    FRACTAL = "fractal"
    SPIRAL = "spiral"
    CUSTOM = "custom"

@dataclass
class EnvironmentalEffect:
    """Changes to surroundings when Governor manifests"""
    primary_effect: str  # Main environmental change
    radius: str  # Affected area description
    duration: str  # How long effects persist
    intensity: str  # Strength of the effect
    secondary_effects: List[str]  # Additional changes

@dataclass
class TimeVariation:
    """How appearance changes with time/conditions"""
    astrological_influences: List[str]  # Affecting planets/signs
    cycle_description: str  # How/when changes occur
    peak_manifestation: str  # Strongest form
    dormant_manifestation: str  # Resting form

@dataclass
class EnergySignature:
    """Governor's unique energy pattern"""
    frequency: str  # Vibrational description
    polarity: str  # Energy direction/flow
    intensity: str  # Power level
    special_properties: List[str]  # Unique energy traits

@dataclass
class SymbolSet:
    """Governor's personal symbols and marks"""
    sigils: List[str]  # Personal sigils
    emblems: List[str]  # Identifying marks
    seals: List[str]  # Power seals
    scripts: List[str]  # Special writing

@dataclass
class LightShadowDynamics:
    """Interaction with light and shadow"""
    light_expression: str  # How light manifests
    shadow_interaction: str  # Shadow effects
    balance_point: str  # Light/shadow equilibrium
    special_effects: List[str]  # Unique phenomena

@dataclass
class DimensionalManifestation:
    """How Governor appears across dimensions"""
    base_form: FormType  # Primary manifestation type
    form_description: str  # Detailed appearance
    dimensional_variations: Dict[str, str]  # Different forms per dimension
    transition_effects: str  # Changes between dimensions
    constant_elements: List[str]  # Features that remain consistent

@dataclass
class VisualAspects:
    """Complete visual aspect profile for a Governor"""
    governor_id: str  # Unique identifier
    name: str  # Governor's name
    
    # Core visual aspects
    dimensional_manifestation: DimensionalManifestation
    color_scheme: ColorScheme
    geometry_patterns: List[GeometryPattern]
    environmental_effects: EnvironmentalEffect
    time_variations: TimeVariation
    energy_signature: EnergySignature
    symbol_set: SymbolSet
    light_shadow: LightShadowDynamics
    
    # Scale and proportion
    scale_description: str  # Size relative to human perception
    scale_variations: Dict[str, str]  # Different sizes in different contexts
    
    # Additional properties
    special_properties: List[str]  # Unique visual traits
    manifestation_triggers: List[str]  # What causes appearance changes
    observer_effects: str  # How perception affects appearance

    def validate(self) -> bool:
        """
        Validate the visual aspects profile for completeness and consistency.
        Returns True if valid, raises ValidationError if invalid.
        """
        # TODO: Implement validation logic
        return True

    def to_dict(self) -> dict:
        """Convert to dictionary format for storage/transmission"""
        # TODO: Implement conversion logic
        return {} 