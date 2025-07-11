"""
Base trait definitions for the Governor system.
Provides standardized data structures for all governor traits.
"""

import logging
from dataclasses import dataclass
from typing import List, Dict, Optional, Set
from enum import Enum, auto

from .mystical import MysticalTraits, MysticalAlignment, ElementalEssence
from .personality import PersonalityTraits, PersonalityCore, TeachingStyle
from ..visual_aspects.schemas.visual_aspect_schema import VisualAspect, VisualAspectValidator

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class CanonicalTraits:
    """Core canonical traits that define a governor's essence"""
    name: str
    aethyr: str
    aethyr_number: int
    region: str
    correspondence: str
    personality: List[str]
    domain: str
    visual_motif: str
    letter_influence: List[str]

@dataclass
class EnhancedTraits:
    """Enhanced trait definitions with expanded context"""
    name: str
    definition: str
    category: str
    usage_context: str
    ai_personality_impact: str
    related_traits: List[str]
    mystical_correspondences: Optional[str]

@dataclass
class GovernorTraits:
    """Complete unified trait definition for a governor"""
    # Identity
    governor_id: str
    governor_number: int
    
    # Core traits
    canonical: CanonicalTraits
    personality: PersonalityTraits
    mystical: MysticalTraits
    visual: VisualAspect
    enhanced: Dict[str, EnhancedTraits]  # Map of trait name to enhanced definition
    
    # Metadata
    version: str = "1.0.0"
    last_updated: Optional[str] = None  # ISO format timestamp
    
    def validate(self) -> bool:
        """Validate all trait components are consistent"""
        try:
            # Validate canonical traits match governor ID
            if self.canonical.name != self.governor_id:
                return False
                
            # Validate personality traits
            if not isinstance(self.personality, PersonalityTraits):
                return False
                
            # Validate mystical traits
            if not isinstance(self.mystical, MysticalTraits):
                return False
                
            # Validate visual aspects
            validator = VisualAspectValidator()
            if not validator.validate_aspect(self.visual):
                return False
                
            # Validate enhanced traits reference valid canonical traits
            for trait_name in self.enhanced:
                if trait_name not in self.canonical.personality:
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Trait validation error: {e}")
            return False 