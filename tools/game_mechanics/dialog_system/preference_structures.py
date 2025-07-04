"""
Governor Preference Data Structures
==================================

This module defines the data structures used for encoding and managing governor
preferences in the Context-Aware Dialog System. These structures convert governor
traits into actionable behavioral parameters for personalized interactions.

Key Components:
- GovernorPreferences: Complete preference profile for a governor
- PreferenceEncoding: Encoded behavioral parameters and weights
- TraitBehaviorMapping: Maps traits to specific behavioral effects
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class TonePreference(Enum):
    """Tone preferences that govern response style."""
    SOLEMN_CRYPTIC = "solemn_cryptic"
    PLAYFUL_RIDDLES = "playful_riddles"
    STERN_FORMAL = "stern_formal"
    MYSTICAL_POETIC = "mystical_poetic"
    SCHOLARLY_PATIENT = "scholarly_patient"
    ENIGMATIC_BRIEF = "enigmatic_brief"
    WARM_ENCOURAGING = "warm_encouraging"
    COLD_DISTANT = "cold_distant"

class PuzzleDifficulty(Enum):
    """Puzzle difficulty levels for governors."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    MASTERFUL = "masterful"

class BehaviorType(Enum):
    """Types of behavioral modifications."""
    RESPONSE_STYLE = "response_style"
    INTERACTION_FILTER = "interaction_filter"
    CONTENT_MODIFIER = "content_modifier"
    REPUTATION_EFFECT = "reputation_effect"
    PATIENCE_MODIFIER = "patience_modifier"

@dataclass
class GovernorPreferences:
    """
    Complete preference profile for a governor, encoding personality traits
    into actionable behavioral parameters for dialog interactions.
    
    This structure transforms abstract governor traits into concrete parameters
    that guide response selection, interaction filtering, and behavioral adaptation.
    """
    governor_id: str
    tone_preference: TonePreference
    interaction_style: str  # Primary interaction model preference
    greeting_formality: float  # 0.0-1.0 (casual to formal)
    puzzle_difficulty: PuzzleDifficulty
    response_patience: float  # 0.0-1.0 (impatient to very patient)
    metaphor_tolerance: float  # 0.0-1.0 (literal to highly metaphorical)
    reputation_sensitivity: float  # 0.0-1.0 (reputation impact on behavior)
    trigger_words: List[str] = field(default_factory=list)  # Words that provoke specific responses
    forbidden_words: List[str] = field(default_factory=list)  # Words that cause negative reactions
    preferred_topics: List[str] = field(default_factory=list)  # Topics that increase engagement
    behavioral_modifiers: Dict[str, float] = field(default_factory=dict)  # Custom behavior weightings
    
    def __post_init__(self):
        """Validate preference values after initialization."""
        if not self.governor_id:
            raise ValueError("GovernorPreferences must have a non-empty governor_id")
        
        # Validate float ranges
        float_fields = {
            'greeting_formality': self.greeting_formality,
            'response_patience': self.response_patience,
            'metaphor_tolerance': self.metaphor_tolerance,
            'reputation_sensitivity': self.reputation_sensitivity
        }
        
        for field_name, value in float_fields.items():
            if not (0.0 <= value <= 1.0):
                raise ValueError(f"{field_name} must be between 0.0 and 1.0, got {value}")
        
        logger.debug(f"Initialized preferences for governor {self.governor_id}")
    
    def get_behavioral_modifier(self, modifier_key: str, default: float = 1.0) -> float:
        """Get a behavioral modifier value with optional default."""
        return self.behavioral_modifiers.get(modifier_key, default)
    
    def has_trigger_word(self, text: str) -> bool:
        """Check if text contains any trigger words."""
        text_lower = text.lower()
        return any(trigger.lower() in text_lower for trigger in self.trigger_words)
    
    def has_forbidden_word(self, text: str) -> bool:
        """Check if text contains any forbidden words."""
        text_lower = text.lower()
        return any(forbidden.lower() in text_lower for forbidden in self.forbidden_words)
    
    def is_preferred_topic(self, topic: str) -> bool:
        """Check if topic is in preferred topics list."""
        topic_lower = topic.lower()
        return any(preferred.lower() == topic_lower for preferred in self.preferred_topics)

@dataclass
class PreferenceEncoding:
    """
    Encoded behavioral parameters and trait weights for a governor.
    
    This structure contains the computed weights and thresholds derived from
    governor traits, providing runtime parameters for behavioral decisions.
    """
    encoding_id: str
    governor_id: str
    trait_weights: Dict[str, float] = field(default_factory=dict)  # trait_name -> weight (0.0-1.0)
    interaction_probabilities: Dict[str, float] = field(default_factory=dict)  # interaction_type -> probability
    response_filters: Dict[str, Any] = field(default_factory=dict)  # content filtering rules
    behavioral_thresholds: Dict[str, float] = field(default_factory=dict)  # decision thresholds
    encoded_timestamp: int = 0
    version: str = "1.0"
    
    def __post_init__(self):
        """Validate encoding structure after initialization."""
        if not self.encoding_id:
            raise ValueError("PreferenceEncoding must have a non-empty encoding_id")
        if not self.governor_id:
            raise ValueError("PreferenceEncoding must have a non-empty governor_id")
        
        logger.debug(f"Initialized preference encoding {self.encoding_id} for governor {self.governor_id}")
    
    def get_trait_weight(self, trait: str, default: float = 0.0) -> float:
        """Get the weight for a specific trait."""
        return self.trait_weights.get(trait.lower(), default)
    
    def get_interaction_probability(self, interaction_type: str, default: float = 0.5) -> float:
        """Get the probability for a specific interaction type."""
        return self.interaction_probabilities.get(interaction_type, default)
    
    def get_behavioral_threshold(self, threshold_key: str, default: float = 0.5) -> float:
        """Get a behavioral decision threshold."""
        return self.behavioral_thresholds.get(threshold_key, default)

@dataclass
class TraitBehaviorMapping:
    """
    Maps a single trait to specific behavioral effects and modifications.
    
    This structure defines how individual personality traits translate into
    concrete behavioral parameters and interaction modifications.
    """
    trait_name: str
    behavior_type: BehaviorType
    effect_strength: float  # 0.0-1.0 - how strongly this trait affects behavior
    conditional_triggers: List[str] = field(default_factory=list)  # When this mapping applies
    parameter_modifications: Dict[str, float] = field(default_factory=dict)  # How this trait modifies behavior
    description: str = ""  # Human-readable description of the mapping
    
    def __post_init__(self):
        """Validate mapping structure after initialization."""
        if not self.trait_name:
            raise ValueError("TraitBehaviorMapping must have a non-empty trait_name")
        
        if not (0.0 <= self.effect_strength <= 1.0):
            raise ValueError(f"effect_strength must be between 0.0 and 1.0, got {self.effect_strength}")
        
        logger.debug(f"Initialized trait mapping for {self.trait_name} -> {self.behavior_type.value}")
    
    def applies_to_context(self, context: Dict[str, Any]) -> bool:
        """Check if this mapping applies in the given context."""
        if not self.conditional_triggers:
            return True  # No conditions means always applies
        
        # Check if any trigger conditions are met
        for trigger in self.conditional_triggers:
            if trigger in context and context[trigger]:
                return True
        
        return False
    
    def get_parameter_modification(self, parameter: str, default: float = 0.0) -> float:
        """Get the modification value for a specific parameter."""
        return self.parameter_modifications.get(parameter, default) 