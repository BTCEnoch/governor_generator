"""
Schema definitions for validating visual aspects of Enochian Governors
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Set
from enum import Enum, auto
from ..catalogs.form_types import BaseFormType, InteractionType, FormDefinition, FormCombinationRules

class AspectScale(Enum):
    """Standardized scales for measuring visual aspect properties"""
    MICRO = auto()      # Smallest scale, atomic/quantum level
    HUMAN = auto()      # Human-perceivable scale
    COSMIC = auto()     # Universal/cosmic scale
    TRANSCENDENT = auto()# Beyond physical scale

class AspectDimension(Enum):
    """Dimensional properties of visual aspects"""
    POINT = auto()      # Zero-dimensional
    LINE = auto()       # One-dimensional
    PLANE = auto()      # Two-dimensional
    VOLUME = auto()     # Three-dimensional
    HYPERCUBE = auto()  # Four-dimensional+
    FRACTAL = auto()    # Self-similar across dimensions

class AspectMotion(Enum):
    """Types of motion exhibited by visual aspects"""
    STATIC = auto()     # No movement
    PERIODIC = auto()   # Regular, repeating motion
    CHAOTIC = auto()    # Unpredictable motion
    HARMONIC = auto()   # Musical/wave-like motion
    SPIRAL = auto()     # Spiral/vortex motion
    QUANTUM = auto()    # Probability-based motion

@dataclass
class ColorDefinition:
    """Definition of a color in the visual aspect"""
    name: str
    rgb: tuple[int, int, int]
    alpha: float
    tradition_meaning: str
    elemental_association: str

@dataclass
class PatternDefinition:
    """Definition of a pattern in the visual aspect"""
    name: str
    base_geometry: str
    repetition_type: str
    sacred_meaning: str
    aethyr_influence: List[str]

@dataclass
class VisualAspect:
    """Complete definition of a governor's visual aspect"""
    governor_name: str
    primary_form: Optional[FormDefinition]
    secondary_form: Optional[FormDefinition]
    scale: AspectScale
    dimensions: Set[AspectDimension]
    motions: Set[AspectMotion]
    colors: List[ColorDefinition]
    patterns: List[PatternDefinition]
    aethyr_resonances: List[str]
    elemental_influences: List[str]
    tradition_alignments: List[str]

class VisualAspectValidator:
    """Validator for visual aspect definitions"""
    
    @staticmethod
    def validate_color(color: ColorDefinition) -> bool:
        """Validate a color definition"""
        if not all(0 <= x <= 255 for x in color.rgb):
            return False
        if not 0 <= color.alpha <= 1:
            return False
        return True

    @staticmethod
    def validate_pattern(pattern: PatternDefinition) -> bool:
        """Validate a pattern definition"""
        if not pattern.name or not pattern.base_geometry:
            return False
        if not pattern.aethyr_influence:
            return False
        return True

    @staticmethod
    def validate_aspect(aspect: VisualAspect) -> bool:
        """Validate a complete visual aspect"""
        # Validate forms
        if not aspect.primary_form:
            return False
        if aspect.secondary_form and not FormCombinationRules.can_combine(
            aspect.primary_form.base_type,
            aspect.secondary_form.base_type
        ):
            return False

        # Validate colors
        if not all(VisualAspectValidator.validate_color(c) for c in aspect.colors):
            return False

        # Validate patterns
        if not all(VisualAspectValidator.validate_pattern(p) for p in aspect.patterns):
            return False

        # Validate resonances and influences
        if not aspect.aethyr_resonances or not aspect.elemental_influences:
            return False

        return True

    @staticmethod
    def validate_aspect_combination(aspect1: VisualAspect, aspect2: VisualAspect) -> bool:
        """Validate if two aspects can be combined"""
        # Check form compatibility
        if aspect1.secondary_form or aspect2.secondary_form:
            return False  # Can't combine aspects that already have secondary forms

        # Check scale compatibility
        if aspect1.scale == aspect2.scale:
            return False  # Aspects must be of different scales

        # Check dimensional compatibility
        if not aspect1.dimensions.isdisjoint(aspect2.dimensions):
            return False  # Dimensions must not overlap

        # Check motion compatibility
        if not aspect1.motions.isdisjoint(aspect2.motions):
            return False  # Motions must not overlap

        return True 