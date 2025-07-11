"""
Generator module for creating visual aspects based on governor traits
"""

import logging
from typing import Dict, List, Optional, Set
from pathlib import Path
from dataclasses import dataclass

from .schemas.visual_aspect_schema import (
    AspectScale,
    AspectDimension,
    AspectMotion,
    ColorDefinition,
    PatternDefinition,
    VisualAspect,
    VisualAspectValidator
)
from .catalogs.form_types import (
    BaseFormType,
    InteractionType,
    FormDefinition,
    FormTypeRegistry,
    FormCombinationRules
)

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class GovernorTraits:
    """Essential traits of a governor that influence visual aspects"""
    name: str
    aethyrs: List[str]
    elements: List[str]
    traditions: List[str]
    personality_traits: List[str]
    mystical_domains: List[str]

class VisualAspectGenerator:
    """Generator for creating visual aspects based on governor traits"""

    def __init__(self):
        self.form_registry = FormTypeRegistry()
        self.validator = VisualAspectValidator()
        self._load_color_mappings()
        self._load_pattern_mappings()

    def _load_color_mappings(self):
        """Load color associations for different traits"""
        self.color_mappings: Dict[str, List[ColorDefinition]] = {
            # Element colors
            "fire": [ColorDefinition(
                name="Sacred Flame",
                rgb=(255, 64, 0),
                alpha=0.9,
                tradition_meaning="Divine Fire",
                elemental_association="fire"
            )],
            "water": [ColorDefinition(
                name="Celestial Ocean",
                rgb=(0, 64, 255),
                alpha=0.8,
                tradition_meaning="Primordial Waters",
                elemental_association="water"
            )],
            "air": [ColorDefinition(
                name="Ethereal Wind",
                rgb=(200, 200, 255),
                alpha=0.6,
                tradition_meaning="Divine Breath",
                elemental_association="air"
            )],
            "earth": [ColorDefinition(
                name="Sacred Earth",
                rgb=(102, 51, 0),
                alpha=1.0,
                tradition_meaning="Foundation Stone",
                elemental_association="earth"
            )],
            "spirit": [ColorDefinition(
                name="Divine Light",
                rgb=(255, 255, 255),
                alpha=0.95,
                tradition_meaning="Pure Spirit",
                elemental_association="spirit"
            )]
        }

    def _load_pattern_mappings(self):
        """Load pattern associations for different traits"""
        self.pattern_mappings: Dict[str, List[PatternDefinition]] = {
            # Aethyr patterns
            "LIL": [PatternDefinition(
                name="Crown of LIL",
                base_geometry="Dodecahedron",
                repetition_type="Fractal",
                sacred_meaning="Supreme Unity",
                aethyr_influence=["LIL"]
            )],
            "ARN": [PatternDefinition(
                name="Gates of ARN",
                base_geometry="Cube",
                repetition_type="Mirrored",
                sacred_meaning="Divine Justice",
                aethyr_influence=["ARN"]
            )],
            "ZOM": [PatternDefinition(
                name="Waters of ZOM",
                base_geometry="Icosahedron",
                repetition_type="Flowing",
                sacred_meaning="Cosmic Waters",
                aethyr_influence=["ZOM"]
            )]
        }

    def _determine_scale(self, traits: GovernorTraits) -> AspectScale:
        """Determine the appropriate scale based on governor traits"""
        if "cosmic" in traits.mystical_domains or "universal" in traits.mystical_domains:
            return AspectScale.COSMIC
        if "quantum" in traits.mystical_domains or "atomic" in traits.mystical_domains:
            return AspectScale.MICRO
        if "transcendent" in traits.mystical_domains:
            return AspectScale.TRANSCENDENT
        return AspectScale.HUMAN

    def _determine_dimensions(self, traits: GovernorTraits) -> Set[AspectDimension]:
        """Determine dimensional properties based on governor traits"""
        dimensions = set()
        
        # Add dimensions based on mystical domains
        if "geometry" in traits.mystical_domains:
            dimensions.add(AspectDimension.VOLUME)
        if "light" in traits.mystical_domains:
            dimensions.add(AspectDimension.LINE)
        if "spirit" in traits.mystical_domains:
            dimensions.add(AspectDimension.HYPERCUBE)
        if "nature" in traits.mystical_domains:
            dimensions.add(AspectDimension.FRACTAL)
            
        # Ensure at least one dimension
        if not dimensions:
            dimensions.add(AspectDimension.VOLUME)
            
        return dimensions

    def _determine_motions(self, traits: GovernorTraits) -> Set[AspectMotion]:
        """Determine motion properties based on governor traits"""
        motions = set()
        
        # Add motions based on personality traits
        if "dynamic" in traits.personality_traits:
            motions.add(AspectMotion.CHAOTIC)
        if "harmonious" in traits.personality_traits:
            motions.add(AspectMotion.HARMONIC)
        if "cyclical" in traits.personality_traits:
            motions.add(AspectMotion.PERIODIC)
        if "transformative" in traits.personality_traits:
            motions.add(AspectMotion.SPIRAL)
            
        # Ensure at least one motion
        if not motions:
            motions.add(AspectMotion.STATIC)
            
        return motions

    def _select_colors(self, traits: GovernorTraits) -> List[ColorDefinition]:
        """Select appropriate colors based on governor traits"""
        colors = []
        
        # Add colors based on elements
        for element in traits.elements:
            if element in self.color_mappings:
                colors.extend(self.color_mappings[element])
                
        # Ensure at least one color
        if not colors:
            colors.append(self.color_mappings["spirit"][0])
            
        return colors

    def _select_patterns(self, traits: GovernorTraits) -> List[PatternDefinition]:
        """Select appropriate patterns based on governor traits"""
        patterns = []
        
        # Add patterns based on aethyrs
        for aethyr in traits.aethyrs:
            if aethyr in self.pattern_mappings:
                patterns.extend(self.pattern_mappings[aethyr])
                
        # Ensure at least one pattern
        if not patterns:
            patterns.append(self.pattern_mappings["LIL"][0])
            
        return patterns

    def _select_forms(self, traits: GovernorTraits) -> tuple[Optional[FormDefinition], Optional[FormDefinition]]:
        """Select appropriate primary and secondary forms"""
        primary = None
        secondary = None

        # Map elements to form types
        element_to_form = {
            "fire": ["RADIANT_SYMBOLIC", "PRISMATIC_ARCHETYPAL"],
            "water": ["FLUID_CRYSTALLINE", "ETHEREAL_METAMORPHIC"],
            "air": ["ETHEREAL_METAMORPHIC", "RADIANT_SYMBOLIC"],
            "earth": ["ORGANIC_SYMBOLIC", "FLUID_CRYSTALLINE"],
            "spirit": ["PRISMATIC_ARCHETYPAL", "RADIANT_SYMBOLIC"]
        }

        # Select primary form based on first element
        if traits.elements:
            primary_element = traits.elements[0]
            if primary_element in element_to_form:
                primary_form_name = element_to_form[primary_element][0]
                primary = self.form_registry.get_form(primary_form_name)

            # Select secondary form if there's a second element
            if len(traits.elements) > 1:
                secondary_element = traits.elements[1]
                if secondary_element in element_to_form:
                    secondary_form_name = element_to_form[secondary_element][0]
                    potential_secondary = self.form_registry.get_form(secondary_form_name)
                    
                    # Validate combination
                    if primary and potential_secondary and self.form_registry.validate_form_combination(
                        primary.name, potential_secondary.name
                    ):
                        secondary = potential_secondary

        return primary, secondary

    def generate_aspect(self, traits: GovernorTraits) -> VisualAspect:
        """Generate a complete visual aspect based on governor traits"""
        logger.info(f"Generating visual aspect for governor: {traits.name}")
        
        # Select forms
        primary_form, secondary_form = self._select_forms(traits)
        if not primary_form:
            logger.warning(f"Could not determine primary form for {traits.name}")
            primary_form = self.form_registry.get_form("ETHEREAL_FORM")  # Default form
            
        # Create aspect
        aspect = VisualAspect(
            governor_name=traits.name,
            primary_form=primary_form,
            secondary_form=secondary_form,
            scale=self._determine_scale(traits),
            dimensions=self._determine_dimensions(traits),
            motions=self._determine_motions(traits),
            colors=self._select_colors(traits),
            patterns=self._select_patterns(traits),
            aethyr_resonances=traits.aethyrs,
            elemental_influences=traits.elements,
            tradition_alignments=traits.traditions
        )
        
        # Validate aspect
        if not self.validator.validate_aspect(aspect):
            logger.error(f"Generated invalid aspect for {traits.name}")
            raise ValueError(f"Invalid visual aspect generated for {traits.name}")
            
        logger.info(f"Successfully generated visual aspect for {traits.name}")
        return aspect

    def generate_aspects_batch(self, traits_list: List[GovernorTraits]) -> Dict[str, VisualAspect]:
        """Generate visual aspects for multiple governors"""
        aspects = {}
        for traits in traits_list:
            try:
                aspects[traits.name] = self.generate_aspect(traits)
            except Exception as e:
                logger.error(f"Failed to generate aspect for {traits.name}: {str(e)}")
                continue
        return aspects 