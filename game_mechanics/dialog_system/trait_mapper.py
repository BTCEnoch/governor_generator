"""
Trait Mapper for Governor Dialog System
=====================================

This module manages the mappings between governor personality traits and specific
behavioral effects. It provides a centralized system for defining how traits
translate into dialog behaviors and interaction modifications.

Key Components:
- TraitMapper: Central registry for trait-behavior mappings
- MappingRegistry: Storage and retrieval of trait mappings
- ConflictResolver: Handles conflicts between multiple trait effects
"""

from typing import Dict, List, Any, Optional, Set, Tuple
import logging
from dataclasses import dataclass, field

from .preference_structures import TraitBehaviorMapping, BehaviorType, GovernorPreferences
from .core_structures import GovernorProfile

logger = logging.getLogger(__name__)


@dataclass
class MappingConflict:
    """Represents a conflict between multiple trait mappings."""
    parameter: str
    conflicting_traits: List[str]
    conflicting_values: List[float]
    resolution_strategy: str
    resolved_value: float


class TraitMapper:
    """
    Central registry for trait-behavior mappings.
    
    This class manages the database of how personality traits translate into
    specific behavioral parameters and provides conflict resolution when
    multiple traits affect the same parameter.
    """
    
    def __init__(self):
        """Initialize the trait mapper with comprehensive mappings."""
        self.mappings_registry: Dict[str, TraitBehaviorMapping] = {}
        self.parameter_conflicts: List[MappingConflict] = []
        self._initialize_comprehensive_mappings()
        logger.info("TraitMapper initialized with comprehensive trait mapping database")
    
    def get_trait_mapping(self, trait: str) -> Optional[TraitBehaviorMapping]:
        """
        Get the behavioral mapping for a specific trait.
        
        Args:
            trait: The trait name to look up
            
        Returns:
            TraitBehaviorMapping if found, None otherwise
        """
        normalized_trait = trait.lower().strip()
        return self.mappings_registry.get(normalized_trait)
    
    def get_all_mappings_for_traits(self, traits: List[str]) -> Dict[str, TraitBehaviorMapping]:
        """
        Get all behavioral mappings for a list of traits.
        
        Args:
            traits: List of trait names
            
        Returns:
            Dictionary mapping trait names to their behavioral mappings
        """
        mappings = {}
        for trait in traits:
            mapping = self.get_trait_mapping(trait)
            if mapping:
                mappings[trait.lower().strip()] = mapping
        
        logger.debug(f"Retrieved mappings for {len(mappings)} traits out of {len(traits)} requested")
        return mappings
    
    def resolve_parameter_conflicts(self, trait_mappings: Dict[str, TraitBehaviorMapping], 
                                  trait_weights: Dict[str, float]) -> Dict[str, float]:
        """
        Resolve conflicts when multiple traits affect the same parameter.
        
        Args:
            trait_mappings: Mappings for all active traits
            trait_weights: Relative weights for each trait
            
        Returns:
            Dictionary of resolved parameter values
        """
        parameter_effects: Dict[str, List[Tuple[str, float, float]]] = {}  # param -> [(trait, effect, weight)]
        
        # Collect all parameter effects from traits
        for trait, mapping in trait_mappings.items():
            trait_weight = trait_weights.get(trait, 0.0)
            for param, effect_value in mapping.parameter_modifications.items():
                if param not in parameter_effects:
                    parameter_effects[param] = []
                
                # Scale effect by trait weight and mapping strength
                scaled_effect = effect_value * trait_weight * mapping.effect_strength
                parameter_effects[param].append((trait, scaled_effect, trait_weight))
        
        # Resolve conflicts for each parameter
        resolved_parameters = {}
        for param, effects in parameter_effects.items():
            if len(effects) == 1:
                # No conflict - single effect
                resolved_parameters[param] = effects[0][1]
            else:
                # Multiple effects - resolve conflict
                resolved_value = self._resolve_conflict(param, effects)
                resolved_parameters[param] = resolved_value
                
                # Record the conflict for debugging
                conflict = MappingConflict(
                    parameter=param,
                    conflicting_traits=[effect[0] for effect in effects],
                    conflicting_values=[effect[1] for effect in effects],
                    resolution_strategy="weighted_average",
                    resolved_value=resolved_value
                )
                self.parameter_conflicts.append(conflict)
                logger.debug(f"Resolved conflict for parameter {param}: {[f'{t}:{v:.3f}' for t,v,w in effects]} -> {resolved_value:.3f}")
        
        return resolved_parameters
    
    def apply_trait_mappings_to_preferences(self, governor_profile: GovernorProfile, 
                                         base_preferences: GovernorPreferences) -> GovernorPreferences:
        """
        Apply trait mappings to modify base preferences.
        
        Args:
            governor_profile: The governor profile containing traits
            base_preferences: Base preferences to modify
            
        Returns:
            Modified preferences with trait effects applied
        """
        logger.info(f"Applying trait mappings to preferences for governor {governor_profile.governor_id}")
        
        # Get mappings for all traits
        trait_mappings = self.get_all_mappings_for_traits(governor_profile.traits)
        if not trait_mappings:
            logger.warning(f"No trait mappings found for governor {governor_profile.governor_id}")
            return base_preferences
        
        # Calculate trait weights (equal weighting for simplicity)
        trait_weights = {trait.lower().strip(): 1.0 / len(governor_profile.traits) 
                        for trait in governor_profile.traits}
        
        # Resolve parameter conflicts
        resolved_parameters = self.resolve_parameter_conflicts(trait_mappings, trait_weights)
        
        # Apply resolved parameters to preferences
        modified_preferences = self._apply_parameter_modifications(base_preferences, resolved_parameters)
        
        logger.info(f"Applied {len(resolved_parameters)} parameter modifications from {len(trait_mappings)} traits")
        return modified_preferences
    
    def add_custom_mapping(self, mapping: TraitBehaviorMapping) -> None:
        """
        Add a custom trait mapping to the registry.
        
        Args:
            mapping: The trait behavior mapping to add
        """
        trait_key = mapping.trait_name.lower().strip()
        self.mappings_registry[trait_key] = mapping
        logger.info(f"Added custom mapping for trait '{trait_key}'")
    
    def get_mapping_summary(self) -> Dict[str, Any]:
        """Get a summary of all registered mappings."""
        summary = {
            'total_mappings': len(self.mappings_registry),
            'behavior_types': {},
            'parameter_coverage': set(),
            'conflicts_recorded': len(self.parameter_conflicts)
        }
        
        for mapping in self.mappings_registry.values():
            behavior_type = mapping.behavior_type.value
            if behavior_type not in summary['behavior_types']:
                summary['behavior_types'][behavior_type] = 0
            summary['behavior_types'][behavior_type] += 1
            
            summary['parameter_coverage'].update(mapping.parameter_modifications.keys())
        
        summary['parameter_coverage'] = list(summary['parameter_coverage'])
        return summary
    
    def _initialize_comprehensive_mappings(self) -> None:
        """Initialize the comprehensive trait mapping database."""
        logger.debug("Initializing comprehensive trait mappings")
        
        # Core personality traits
        self.mappings_registry.update({
            'patient': TraitBehaviorMapping(
                trait_name='patient',
                behavior_type=BehaviorType.PATIENCE_MODIFIER,
                effect_strength=0.8,
                parameter_modifications={
                    'response_patience': 0.3,
                    'greeting_formality': 0.1,
                    'reputation_sensitivity': 0.1
                },
                description="Patient governors are more tolerant and slightly more formal"
            ),
            
            'cryptic': TraitBehaviorMapping(
                trait_name='cryptic',
                behavior_type=BehaviorType.RESPONSE_STYLE,
                effect_strength=0.9,
                parameter_modifications={
                    'metaphor_tolerance': 0.4,
                    'puzzle_difficulty_boost': 0.2,
                    'greeting_formality': 0.2
                },
                description="Cryptic governors use metaphors and complex puzzles"
            ),
            
            'scholarly': TraitBehaviorMapping(
                trait_name='scholarly',
                behavior_type=BehaviorType.CONTENT_MODIFIER,
                effect_strength=0.7,
                parameter_modifications={
                    'greeting_formality': 0.3,
                    'response_patience': 0.2,
                    'reputation_sensitivity': 0.1
                },
                description="Scholarly governors are formal and educational"
            ),
            
            'mystical': TraitBehaviorMapping(
                trait_name='mystical',
                behavior_type=BehaviorType.RESPONSE_STYLE,
                effect_strength=0.9,
                parameter_modifications={
                    'metaphor_tolerance': 0.5,
                    'mystical_language': 0.4,
                    'greeting_formality': 0.2
                },
                description="Mystical governors heavily use mystical language and metaphors"
            ),
            
            'formal': TraitBehaviorMapping(
                trait_name='formal',
                behavior_type=BehaviorType.INTERACTION_FILTER,
                effect_strength=0.8,
                parameter_modifications={
                    'greeting_formality': 0.4,
                    'casual_penalty': 0.3,
                    'reputation_sensitivity': 0.2
                },
                description="Formal governors require proper etiquette and formality"
            ),
            
            'stern': TraitBehaviorMapping(
                trait_name='stern',
                behavior_type=BehaviorType.REPUTATION_EFFECT,
                effect_strength=0.6,
                parameter_modifications={
                    'reputation_sensitivity': -0.1,
                    'failure_penalty': 0.2,
                    'greeting_formality': 0.1
                },
                description="Stern governors are harsh with failures but less reputation-sensitive"
            ),
            
            'wise': TraitBehaviorMapping(
                trait_name='wise',
                behavior_type=BehaviorType.CONTENT_MODIFIER,
                effect_strength=0.8,
                parameter_modifications={
                    'response_patience': 0.3,
                    'metaphor_tolerance': 0.2,
                    'teaching_bonus': 0.3
                },
                description="Wise governors are patient teachers with deep knowledge"
            ),
            
            'playful': TraitBehaviorMapping(
                trait_name='playful',
                behavior_type=BehaviorType.RESPONSE_STYLE,
                effect_strength=0.6,
                parameter_modifications={
                    'greeting_formality': -0.2,
                    'puzzle_difficulty_boost': -0.1,
                    'casual_acceptance': 0.3
                },
                description="Playful governors are less formal and more accepting of casual interaction"
            ),
            
            'methodical': TraitBehaviorMapping(
                trait_name='methodical',
                behavior_type=BehaviorType.CONTENT_MODIFIER,
                effect_strength=0.7,
                parameter_modifications={
                    'response_patience': 0.2,
                    'step_by_step_bonus': 0.3,
                    'precision_requirement': 0.2
                },
                description="Methodical governors prefer step-by-step approaches and precision"
            )
        })
        
        logger.info(f"Initialized {len(self.mappings_registry)} trait mappings")
    
    def _resolve_conflict(self, parameter: str, effects: List[Tuple[str, float, float]]) -> float:
        """
        Resolve conflicts between multiple trait effects on the same parameter.
        
        Args:
            parameter: The parameter name being modified
            effects: List of (trait_name, scaled_effect, trait_weight) tuples
            
        Returns:
            Resolved parameter value
        """
        if not effects:
            return 0.0
        
        if len(effects) == 1:
            return effects[0][1]  # Single effect, no conflict
        
        # Use weighted average as default resolution strategy
        total_weight = sum(effect[2] for effect in effects)
        if total_weight == 0:
            return 0.0
        
        weighted_sum = sum(effect[1] * effect[2] for effect in effects)
        resolved_value = weighted_sum / total_weight
        
        # Apply bounds checking for common parameters
        if parameter in ['greeting_formality', 'response_patience', 'metaphor_tolerance', 'reputation_sensitivity']:
            resolved_value = max(0.0, min(1.0, resolved_value))
        
        logger.debug(f"Resolved conflict for {parameter}: {len(effects)} effects -> {resolved_value:.3f}")
        return resolved_value
    
    def _apply_parameter_modifications(self, base_preferences: GovernorPreferences, 
                                     modifications: Dict[str, float]) -> GovernorPreferences:
        """
        Apply parameter modifications to base preferences.
        
        Args:
            base_preferences: Original preferences to modify
            modifications: Dictionary of parameter modifications
            
        Returns:  
            New preferences object with modifications applied
        """
        # Create a copy of the base preferences
        modified_preferences = GovernorPreferences(
            governor_id=base_preferences.governor_id,
            tone_preference=base_preferences.tone_preference,
            interaction_style=base_preferences.interaction_style,
            greeting_formality=base_preferences.greeting_formality,
            puzzle_difficulty=base_preferences.puzzle_difficulty,
            response_patience=base_preferences.response_patience,
            metaphor_tolerance=base_preferences.metaphor_tolerance,
            reputation_sensitivity=base_preferences.reputation_sensitivity,
            trigger_words=base_preferences.trigger_words.copy(),
            forbidden_words=base_preferences.forbidden_words.copy(),
            preferred_topics=base_preferences.preferred_topics.copy(),
            behavioral_modifiers=base_preferences.behavioral_modifiers.copy()
        )
        
        # Apply modifications to core parameters
        for param, modification in modifications.items():
            current_value = getattr(modified_preferences, param, None)
            if current_value is not None and isinstance(current_value, (int, float)):
                # Apply modification with bounds checking
                new_value = current_value + modification
                new_value = max(0.0, min(1.0, new_value))  # Clamp to [0,1] range
                setattr(modified_preferences, param, new_value)
                logger.debug(f"Modified {param}: {current_value:.3f} + {modification:.3f} = {new_value:.3f}")
            else:
                # Add to behavioral modifiers if not a direct attribute
                modified_preferences.behavioral_modifiers[param] = modification
                logger.debug(f"Added behavioral modifier {param}: {modification:.3f}")
        
        return modified_preferences 