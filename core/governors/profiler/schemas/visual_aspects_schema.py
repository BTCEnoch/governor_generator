"""
Schema definitions for Governor Visual Aspects.

This module defines the data structures and validation rules for Governor visual appearances
across different dimensions and manifestations.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum
from core.utils.common.errors import ValidationError

class FormType(str, Enum):
    """Base form types for governor manifestations."""
    ETHEREAL = 'ethereal'  # Pure energy/light forms
    GEOMETRIC = 'geometric'  # Sacred geometry based
    CELESTIAL = 'celestial'  # Star/planet like
    HUMANOID = 'humanoid'  # Human-like forms
    FLAME = 'flame'  # Fire-based forms
    FLUID = 'fluid'  # Water/liquid based
    CRYSTALLINE = 'crystalline'  # Crystal/mineral based
    COMPOSITE = 'composite'  # Multiple form types
    ABSTRACT = "abstract"  # Non-euclidean/conceptual
    METAMORPHIC = "metamorphic"  # Shape-shifting/fluid
    SYMBOLIC = "symbolic"  # Manifests as pure symbols
    ELEMENTAL = "elemental"  # Pure elemental form
    OTHER = "other"  # Unique/special cases

class ColorScheme(str, Enum):
    """Color schemes for governor manifestations."""
    GOLDEN = 'golden'
    SILVER = 'silver'
    PRISMATIC = 'prismatic'
    PLASMA = 'plasma'
    AZURE = 'azure'
    EMERALD = 'emerald'
    OPALESCENT = 'opalescent'
    CRYSTALLINE = 'crystalline'
    VOID = "void"  # Absence of color/deep space
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
        Raises ValidationError if invalid with detailed reason.
        """
        try:
            # 1. Basic field validation
            self._validate_required_fields()
            
            # 2. Form type consistency
            self._validate_form_consistency()
            
            # 3. Color scheme validation
            self._validate_color_scheme()
            
            # 4. Geometry pattern validation
            self._validate_geometry_patterns()
            
            # 5. Environmental effects validation
            self._validate_environmental_effects()
            
            # 6. Dimensional consistency
            self._validate_dimensional_consistency()
            
            return True
            
        except ValidationError as e:
            raise ValidationError(f"Visual aspects validation failed: {str(e)}")

    def _validate_required_fields(self):
        """Validate all required fields are present and non-empty"""
        required_fields = [
            'governor_id', 'name', 'dimensional_manifestation',
            'color_scheme', 'geometry_patterns', 'environmental_effects',
            'time_variations', 'energy_signature', 'symbol_set',
            'light_shadow', 'scale_description'
        ]
        
        for field in required_fields:
            if not getattr(self, field):
                raise ValidationError(f"Missing required field: {field}")

    def _validate_form_consistency(self):
        """Validate form type matches governor's elemental affinity"""
        base_form = self.dimensional_manifestation.base_form
        
        # Check form transitions are valid
        if base_form == FormType.METAMORPHIC:
            if not self.dimensional_manifestation.transition_effects:
                raise ValidationError("Metamorphic form requires transition effects")
        
        # Verify constant elements exist for all form types
        if not self.dimensional_manifestation.constant_elements:
            raise ValidationError("Must have at least one constant element across manifestations")
        
        # Validate dimensional variations
        if not self.dimensional_manifestation.dimensional_variations:
            raise ValidationError("Must specify at least one dimensional variation")

    def _validate_color_scheme(self):
        """Validate color scheme aligns with governor's aethyr and nature"""
        # Verify color scheme matches base form
        if self.dimensional_manifestation.base_form == FormType.ETHEREAL:
            if self.color_scheme not in [ColorScheme.PRISMATIC, ColorScheme.PLASMA]:
                raise ValidationError("Ethereal forms must have prismatic or plasma color schemes")
        
        # Check light/shadow dynamics match color scheme
        if self.color_scheme == ColorScheme.VOID:
            if not self.light_shadow.shadow_interaction:
                raise ValidationError("Void color scheme requires shadow interaction details")

    def _validate_geometry_patterns(self):
        """Validate sacred geometry patterns match numerical correspondences"""
        if not self.geometry_patterns:
            raise ValidationError("Must have at least one geometry pattern")
        
        # Check for valid pattern combinations
        if GeometryPattern.MERKABA in self.geometry_patterns:
            if GeometryPattern.TORUS not in self.geometry_patterns:
                raise ValidationError("Merkaba pattern requires Torus pattern for stability")

    def _validate_environmental_effects(self):
        """Validate environmental effects are consistent with governor's powers"""
        if not self.environmental_effects.primary_effect:
            raise ValidationError("Must specify primary environmental effect")
        
        if not self.environmental_effects.radius:
            raise ValidationError("Must specify effect radius")
        
        # Verify secondary effects don't contradict primary
        if self.environmental_effects.secondary_effects:
            if len(self.environmental_effects.secondary_effects) > 3:
                raise ValidationError("Maximum of 3 secondary environmental effects allowed")

    def _validate_dimensional_consistency(self):
        """Validate consistency across dimensional manifestations"""
        variations = self.dimensional_manifestation.dimensional_variations
        
        # Must have at least etheric and astral manifestations
        required_dimensions = ['etheric', 'astral']
        for dim in required_dimensions:
            if dim not in variations:
                raise ValidationError(f"Missing required dimensional variation: {dim}")
        
        # Verify transitions between dimensions are defined
        if not self.dimensional_manifestation.transition_effects:
            raise ValidationError("Must define transition effects between dimensions")

    def to_dict(self) -> dict:
        """Convert to dictionary format for storage/transmission"""
        return {
            'governor_id': self.governor_id,
            'name': self.name,
            'dimensional_manifestation': {
                'base_form': self.dimensional_manifestation.base_form.value,
                'form_description': self.dimensional_manifestation.form_description,
                'dimensional_variations': self.dimensional_manifestation.dimensional_variations,
                'transition_effects': self.dimensional_manifestation.transition_effects,
                'constant_elements': self.dimensional_manifestation.constant_elements
            },
            'color_scheme': self.color_scheme.value,
            'geometry_patterns': [pattern.value for pattern in self.geometry_patterns],
            'environmental_effects': {
                'primary_effect': self.environmental_effects.primary_effect,
                'radius': self.environmental_effects.radius,
                'duration': self.environmental_effects.duration,
                'intensity': self.environmental_effects.intensity,
                'secondary_effects': self.environmental_effects.secondary_effects
            },
            'time_variations': {
                'astrological_influences': self.time_variations.astrological_influences,
                'cycle_description': self.time_variations.cycle_description,
                'peak_manifestation': self.time_variations.peak_manifestation,
                'dormant_manifestation': self.time_variations.dormant_manifestation
            },
            'energy_signature': {
                'frequency': self.energy_signature.frequency,
                'polarity': self.energy_signature.polarity,
                'intensity': self.energy_signature.intensity,
                'special_properties': self.energy_signature.special_properties
            },
            'symbol_set': {
                'sigils': self.symbol_set.sigils,
                'emblems': self.symbol_set.emblems,
                'seals': self.symbol_set.seals,
                'scripts': self.symbol_set.scripts
            },
            'light_shadow': {
                'light_expression': self.light_shadow.light_expression,
                'shadow_interaction': self.light_shadow.shadow_interaction,
                'balance_point': self.light_shadow.balance_point,
                'special_effects': self.light_shadow.special_effects
            },
            'scale_description': self.scale_description,
            'scale_variations': self.scale_variations,
            'special_properties': self.special_properties,
            'manifestation_triggers': self.manifestation_triggers,
            'observer_effects': self.observer_effects
        } 