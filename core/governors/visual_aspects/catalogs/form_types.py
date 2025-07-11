"""
Form Types Catalog for Enochian Governor Visual Aspects

This module defines the standardized form categories and their valid combinations
for Enochian Governor visual manifestations.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Dict, Set, Optional
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class BaseFormType(Enum):
    """Base form categories that define primary manifestation types"""
    FLUID = auto()      # Water-like, flowing forms
    CRYSTALLINE = auto() # Structured, geometric forms
    RADIANT = auto()    # Light-based, luminous forms
    ETHEREAL = auto()   # Mist-like, translucent forms
    COMPOSITE = auto()  # Combined material forms
    PRISMATIC = auto()  # Multi-faceted, refractive forms
    ORGANIC = auto()    # Nature-based, growing forms
    SYMBOLIC = auto()   # Glyph-like, sigil forms
    METAMORPHIC = auto()# Transforming, shifting forms
    ARCHETYPAL = auto() # Pure concept forms

class InteractionType(Enum):
    """Defines how the form interacts with its environment and observers"""
    EMANATING = auto()  # Radiates energy/influence outward
    ABSORBING = auto()  # Takes in energy/information
    REFLECTING = auto() # Mirrors/returns energy
    TRANSMUTING = auto()# Changes energy forms
    RESONATING = auto() # Creates harmonic patterns
    PULSING = auto()   # Rhythmic energy patterns
    FLOWING = auto()    # Continuous movement patterns
    CYCLING = auto()    # Repeating transformation patterns
    CATALYZING = auto()# Triggers changes in others
    HARMONIZING = auto()# Balances surrounding energies

@dataclass
class FormDefinition:
    """Detailed definition of a form type"""
    name: str
    base_type: BaseFormType
    description: str
    valid_interactions: Set[InteractionType]
    tradition_origins: List[str]
    elemental_affinities: List[str]
    aethyr_resonance: List[str]

class FormCombinationRules:
    """Rules for valid form combinations"""
    
    # Mapping of which base forms can be combined
    VALID_COMBINATIONS: Dict[BaseFormType, Set[BaseFormType]] = {
        BaseFormType.FLUID: {
            BaseFormType.ETHEREAL,
            BaseFormType.METAMORPHIC,
            BaseFormType.ORGANIC
        },
        BaseFormType.CRYSTALLINE: {
            BaseFormType.PRISMATIC,
            BaseFormType.SYMBOLIC,
            BaseFormType.ARCHETYPAL
        },
        BaseFormType.RADIANT: {
            BaseFormType.ETHEREAL,
            BaseFormType.PRISMATIC,
            BaseFormType.SYMBOLIC
        },
        BaseFormType.ETHEREAL: {
            BaseFormType.FLUID,
            BaseFormType.RADIANT,
            BaseFormType.METAMORPHIC
        },
        BaseFormType.COMPOSITE: {
            BaseFormType.CRYSTALLINE,
            BaseFormType.ORGANIC,
            BaseFormType.SYMBOLIC
        },
        BaseFormType.PRISMATIC: {
            BaseFormType.CRYSTALLINE,
            BaseFormType.RADIANT,
            BaseFormType.ARCHETYPAL
        },
        BaseFormType.ORGANIC: {
            BaseFormType.FLUID,
            BaseFormType.COMPOSITE,
            BaseFormType.METAMORPHIC
        },
        BaseFormType.SYMBOLIC: {
            BaseFormType.CRYSTALLINE,
            BaseFormType.RADIANT,
            BaseFormType.ARCHETYPAL
        },
        BaseFormType.METAMORPHIC: {
            BaseFormType.FLUID,
            BaseFormType.ETHEREAL,
            BaseFormType.ORGANIC
        },
        BaseFormType.ARCHETYPAL: {
            BaseFormType.CRYSTALLINE,
            BaseFormType.PRISMATIC,
            BaseFormType.SYMBOLIC
        }
    }

    @classmethod
    def can_combine(cls, form1: BaseFormType, form2: BaseFormType) -> bool:
        """Check if two base forms can be combined"""
        return form2 in cls.VALID_COMBINATIONS[form1]

    @classmethod
    def get_valid_combinations(cls, form: BaseFormType) -> Set[BaseFormType]:
        """Get all valid combinations for a base form"""
        return cls.VALID_COMBINATIONS[form]

class FormTypeRegistry:
    """Registry of all defined form types and their definitions"""
    
    def __init__(self):
        self.forms: Dict[str, FormDefinition] = {}
        self._load_definitions()

    def _load_definitions(self):
        """Load form definitions from JSON data"""
        definitions_file = Path(__file__).parent / "data" / "form_definitions.json"
        if definitions_file.exists():
            with open(definitions_file) as f:
                data = json.load(f)
                if "forms" in data:  # Handle the correct JSON structure
                    for form_data in data["forms"]:
                        try:
                            self.forms[form_data["name"]] = FormDefinition(
                                name=form_data["name"],
                                base_type=BaseFormType[form_data["base_type"]],
                                description=form_data["description"],
                                valid_interactions={InteractionType[i] for i in form_data["valid_interactions"]},
                                tradition_origins=form_data["tradition_origins"],
                                elemental_affinities=form_data["elemental_affinities"],
                                aethyr_resonance=form_data["aethyr_resonance"]
                            )
                        except (KeyError, ValueError) as e:
                            logger.error(f"Error loading form definition for {form_data.get('name', 'unknown')}: {str(e)}")
                            continue

    def get_form(self, name: str) -> Optional[FormDefinition]:
        """Get a form definition by name"""
        return self.forms.get(name)

    def validate_form_combination(self, form1_name: str, form2_name: str) -> bool:
        """Validate if two forms can be combined"""
        form1 = self.get_form(form1_name)
        form2 = self.get_form(form2_name)
        if not form1 or not form2:
            return False
        return FormCombinationRules.can_combine(form1.base_type, form2.base_type)

# Initialize the global registry
form_registry = FormTypeRegistry() 