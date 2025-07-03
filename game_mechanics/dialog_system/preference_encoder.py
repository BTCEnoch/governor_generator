"""
Preference Encoder for Governor Dialog System
===========================================

This module implements the PreferenceEncoder class that converts governor traits
into actionable behavioral preferences. It analyzes personality traits and mystical
specializations to generate concrete parameters for dialog interactions.

Key Components:
- PreferenceEncoder: Main encoding engine for trait-to-preference conversion
- TraitAnalyzer: Analyzes and weights governor traits
- ParameterGenerator: Generates behavioral parameters from trait analysis
"""

from typing import Dict, List, Any, Optional
import logging
import hashlib
from dataclasses import asdict

from .core_structures import GovernorProfile, InteractionType
from .preference_structures import (
    GovernorPreferences, PreferenceEncoding, TraitBehaviorMapping,
    TonePreference, PuzzleDifficulty, BehaviorType
)

logger = logging.getLogger(__name__)


class PreferenceEncoder:
    """
    Main encoding engine that converts governor traits into behavioral preferences.
    
    This class analyzes personality traits, mystical specializations, and existing
    preferences to generate comprehensive behavioral parameters for each governor.
    """
    
    def __init__(self):
        """Initialize the preference encoder with default trait mappings."""
        self.trait_mappings = self._initialize_trait_mappings()
        self.tone_trait_mappings = self._initialize_tone_mappings()
        self.difficulty_trait_mappings = self._initialize_difficulty_mappings()
        logger.info("PreferenceEncoder initialized with trait mapping database")
    
    def encode_governor_preferences(self, governor_profile: GovernorProfile) -> GovernorPreferences:
        """
        Convert governor traits into behavioral preferences.
        
        Args:
            governor_profile: The governor profile to analyze
            
        Returns:
            GovernorPreferences: Complete preference profile
        """
        logger.info(f"Encoding preferences for governor {governor_profile.governor_id}")
        
        try:
            # Step 1: Extract and analyze traits
            traits = governor_profile.traits
            trait_weights = self.calculate_trait_weights(traits)
            logger.debug(f"Calculated trait weights: {trait_weights}")
            
            # Step 2: Determine tone preference from traits
            tone_preference = self._determine_tone_preference(traits, trait_weights)
            logger.debug(f"Determined tone preference: {tone_preference}")
            
            # Step 3: Determine interaction style
            interaction_style = self._determine_interaction_style(governor_profile.interaction_models)
            
            # Step 4: Calculate behavioral parameters
            behavioral_params = self._generate_behavioral_parameters(traits, trait_weights)
            
            # Step 5: Generate trigger and forbidden words
            trigger_words = self._generate_trigger_words(traits, governor_profile)
            forbidden_words = self._generate_forbidden_words(traits)
            preferred_topics = self._generate_preferred_topics(governor_profile)
            
            # Step 6: Create preferences object
            preferences = GovernorPreferences(
                governor_id=governor_profile.governor_id,
                tone_preference=tone_preference,
                interaction_style=interaction_style,
                greeting_formality=behavioral_params.get('greeting_formality', 0.5),
                puzzle_difficulty=self._determine_puzzle_difficulty(traits, trait_weights),
                response_patience=behavioral_params.get('response_patience', 0.5),
                metaphor_tolerance=behavioral_params.get('metaphor_tolerance', 0.5),
                reputation_sensitivity=behavioral_params.get('reputation_sensitivity', 0.5),
                trigger_words=trigger_words,
                forbidden_words=forbidden_words,
                preferred_topics=preferred_topics,
                behavioral_modifiers=behavioral_params.get('modifiers', {})
            )
            
            logger.info(f"Successfully encoded preferences for governor {governor_profile.governor_id}")
            return preferences
            
        except Exception as e:
            logger.error(f"Failed to encode preferences for governor {governor_profile.governor_id}: {e}")
            # Return default preferences on error
            return self._create_default_preferences(governor_profile.governor_id)
    
    def calculate_trait_weights(self, traits: List[str]) -> Dict[str, float]:
        """
        Calculate relative importance weights for each trait.
        
        Args:
            traits: List of personality traits
            
        Returns:
            Dictionary mapping trait names to importance weights (0.0-1.0)
        """
        if not traits:
            return {}
        
        # Normalize trait names
        normalized_traits = [trait.lower().strip() for trait in traits]
        
        # Calculate base weights (equal distribution)
        base_weight = 1.0 / len(normalized_traits)
        trait_weights = {trait: base_weight for trait in normalized_traits}
        
        # Apply modifiers based on trait importance
        trait_importance_modifiers = {
            'patient': 1.2,      # High importance for dialog flow
            'cryptic': 1.3,      # High importance for response style
            'scholarly': 1.1,    # Moderate importance
            'mystical': 1.4,     # Very high importance for tone
            'formal': 1.2,       # High importance for interaction style
            'stern': 1.1,        # Moderate importance
            'playful': 1.0,      # Normal importance
            'wise': 1.2,         # High importance
            'methodical': 1.1    # Moderate importance
        }
        
        # Apply importance modifiers
        for trait, weight in trait_weights.items():
            modifier = trait_importance_modifiers.get(trait, 1.0)
            trait_weights[trait] = weight * modifier
        
        # Renormalize to ensure sum is 1.0
        total_weight = sum(trait_weights.values())
        if total_weight > 0:
            trait_weights = {trait: weight / total_weight for trait, weight in trait_weights.items()}
        
        logger.debug(f"Calculated trait weights: {trait_weights}")
        return trait_weights
    
    def generate_behavioral_parameters(self, preferences: GovernorPreferences) -> Dict[str, Any]:
        """
        Generate runtime behavioral parameters from preferences.
        
        Args:
            preferences: Governor preferences to parameterize
            
        Returns:
            Dictionary of behavioral parameters for runtime use
        """
        parameters = {
            'tone_modifier': preferences.tone_preference.value,
            'formality_threshold': preferences.greeting_formality,
            'patience_multiplier': preferences.response_patience,
            'metaphor_weight': preferences.metaphor_tolerance,
            'reputation_factor': preferences.reputation_sensitivity,
            'difficulty_level': preferences.puzzle_difficulty.value
        }
        
        # Add custom behavioral modifiers
        parameters.update(preferences.behavioral_modifiers)
        
        logger.debug(f"Generated behavioral parameters for {preferences.governor_id}: {parameters}")
        return parameters
    
    def _initialize_trait_mappings(self) -> Dict[str, TraitBehaviorMapping]:
        """Initialize the trait-to-behavior mapping database."""
        mappings = {}
        
        # Patient trait mapping
        mappings['patient'] = TraitBehaviorMapping(
            trait_name='patient',
            behavior_type=BehaviorType.PATIENCE_MODIFIER,
            effect_strength=0.8,
            parameter_modifications={'response_patience': 0.3, 'greeting_formality': 0.1},
            description="Increases patience and slight formality boost"
        )
        
        # Cryptic trait mapping
        mappings['cryptic'] = TraitBehaviorMapping(
            trait_name='cryptic',
            behavior_type=BehaviorType.RESPONSE_STYLE,
            effect_strength=0.9,
            parameter_modifications={'metaphor_tolerance': 0.4, 'puzzle_difficulty_boost': 0.2},
            description="Increases metaphor usage and puzzle complexity"
        )
        
        # Scholarly trait mapping
        mappings['scholarly'] = TraitBehaviorMapping(
            trait_name='scholarly',
            behavior_type=BehaviorType.CONTENT_MODIFIER,
            effect_strength=0.7,
            parameter_modifications={'greeting_formality': 0.2, 'response_patience': 0.2},
            description="Increases formality and patience in explanations"
        )
        
        # Mystical trait mapping
        mappings['mystical'] = TraitBehaviorMapping(
            trait_name='mystical',
            behavior_type=BehaviorType.RESPONSE_STYLE,
            effect_strength=0.9,
            parameter_modifications={'metaphor_tolerance': 0.5, 'mystical_language': 0.4},
            description="Heavy use of mystical language and metaphors"
        )
        
        # Formal trait mapping
        mappings['formal'] = TraitBehaviorMapping(
            trait_name='formal',
            behavior_type=BehaviorType.INTERACTION_FILTER,
            effect_strength=0.8,
            parameter_modifications={'greeting_formality': 0.4, 'casual_penalty': 0.3},
            description="Requires formal interaction and penalizes casual approaches"
        )
        
        # Stern trait mapping
        mappings['stern'] = TraitBehaviorMapping(
            trait_name='stern',
            behavior_type=BehaviorType.REPUTATION_EFFECT,
            effect_strength=0.6,
            parameter_modifications={'reputation_sensitivity': -0.1, 'failure_penalty': 0.2},
            description="Less reputation sensitive but harsher failure penalties"
        )
        
        return mappings
    
    def _initialize_tone_mappings(self) -> Dict[str, TonePreference]:
        """Initialize trait combinations to tone preference mappings."""
        return {
            'mystical_cryptic': TonePreference.SOLEMN_CRYPTIC,
            'mystical_scholarly': TonePreference.MYSTICAL_POETIC,
            'patient_scholarly': TonePreference.SCHOLARLY_PATIENT,
            'stern_formal': TonePreference.STERN_FORMAL,
            'cryptic_wise': TonePreference.ENIGMATIC_BRIEF,
            'playful_wise': TonePreference.PLAYFUL_RIDDLES,
            'cold_stern': TonePreference.COLD_DISTANT,
            'warm_patient': TonePreference.WARM_ENCOURAGING
        }
    
    def _initialize_difficulty_mappings(self) -> Dict[str, PuzzleDifficulty]:
        """Initialize trait combinations to puzzle difficulty mappings."""
        return {
            'scholarly_methodical': PuzzleDifficulty.COMPLEX,
            'wise_cryptic': PuzzleDifficulty.MASTERFUL,
            'mystical_ancient': PuzzleDifficulty.COMPLEX,
            'patient_teaching': PuzzleDifficulty.MODERATE,
            'playful_simple': PuzzleDifficulty.SIMPLE,
            'stern_challenging': PuzzleDifficulty.COMPLEX
        }
    
    def _determine_tone_preference(self, traits: List[str], trait_weights: Dict[str, float]) -> TonePreference:
        """Determine tone preference from traits and weights."""
        normalized_traits = [trait.lower().strip() for trait in traits]
        
        # Check for specific trait combinations first
        for combo, tone in self.tone_trait_mappings.items():
            combo_traits = combo.split('_')
            if all(trait in normalized_traits for trait in combo_traits):
                logger.debug(f"Found tone combo match: {combo} -> {tone}")
                return tone
        
        # Fall back to individual trait analysis
        trait_tone_scores = {
            TonePreference.SOLEMN_CRYPTIC: 0.0,
            TonePreference.MYSTICAL_POETIC: 0.0,
            TonePreference.SCHOLARLY_PATIENT: 0.0,
            TonePreference.STERN_FORMAL: 0.0,
            TonePreference.ENIGMATIC_BRIEF: 0.0,
            TonePreference.PLAYFUL_RIDDLES: 0.0,
            TonePreference.COLD_DISTANT: 0.0,
            TonePreference.WARM_ENCOURAGING: 0.0
        }
        
        # Score each tone based on trait weights
        for trait, weight in trait_weights.items():
            if trait == 'mystical':
                trait_tone_scores[TonePreference.MYSTICAL_POETIC] += weight * 0.8
                trait_tone_scores[TonePreference.SOLEMN_CRYPTIC] += weight * 0.6
            elif trait == 'scholarly':
                trait_tone_scores[TonePreference.SCHOLARLY_PATIENT] += weight * 0.9
            elif trait == 'cryptic':
                trait_tone_scores[TonePreference.SOLEMN_CRYPTIC] += weight * 0.9
                trait_tone_scores[TonePreference.ENIGMATIC_BRIEF] += weight * 0.7
            elif trait == 'stern':
                trait_tone_scores[TonePreference.STERN_FORMAL] += weight * 0.8
                trait_tone_scores[TonePreference.COLD_DISTANT] += weight * 0.6
            elif trait == 'patient':
                trait_tone_scores[TonePreference.SCHOLARLY_PATIENT] += weight * 0.7
                trait_tone_scores[TonePreference.WARM_ENCOURAGING] += weight * 0.5
            elif trait == 'playful':
                trait_tone_scores[TonePreference.PLAYFUL_RIDDLES] += weight * 0.9
        
        # Return the highest scoring tone
        best_tone = max(trait_tone_scores.items(), key=lambda x: x[1])
        return best_tone[0] if best_tone[1] > 0 else TonePreference.SCHOLARLY_PATIENT  # Default
    
    def _determine_interaction_style(self, interaction_models: List[InteractionType]) -> str:
        """Determine primary interaction style from available models."""
        if not interaction_models:
            return "riddle_keeper"  # Default style
        
        # Prefer more complex interaction types
        preference_order = [
            InteractionType.SECRET_KEEPER,
            InteractionType.RITUAL_GUIDE,
            InteractionType.ARCHETYPAL_MIRROR,
            InteractionType.TRIBUTE_TAKER,
            InteractionType.RIDDLE_KEEPER,
            InteractionType.CEREMONIAL_GOVERNOR,
            InteractionType.KNOWLEDGE_SEEKER
        ]
        
        for preferred_type in preference_order:
            if preferred_type in interaction_models:
                return preferred_type.value
        
        return interaction_models[0].value  # Fallback to first available
    
    def _determine_puzzle_difficulty(self, traits: List[str], trait_weights: Dict[str, float]) -> PuzzleDifficulty:
        """Determine puzzle difficulty based on traits."""
        normalized_traits = [trait.lower().strip() for trait in traits]
        
        # Check for specific combinations first
        for combo, difficulty in self.difficulty_trait_mappings.items():
            combo_traits = combo.split('_')
            if all(trait in normalized_traits for trait in combo_traits):
                return difficulty
        
        # Calculate difficulty score from individual traits
        difficulty_score = 0.0
        
        trait_difficulty_contributions = {
            'wise': 0.3,
            'scholarly': 0.2,
            'cryptic': 0.3,
            'mystical': 0.2,
            'methodical': 0.2,
            'patient': -0.1,  # Patient governors might use easier puzzles
            'playful': -0.2   # Playful governors prefer simpler challenges
        }
        
        for trait, weight in trait_weights.items():
            contribution = trait_difficulty_contributions.get(trait, 0.0)
            difficulty_score += weight * contribution
        
        # Map score to difficulty level  
        if difficulty_score >= 0.3:
            return PuzzleDifficulty.MASTERFUL
        elif difficulty_score >= 0.15:
            return PuzzleDifficulty.COMPLEX
        elif difficulty_score >= 0.0:
            return PuzzleDifficulty.MODERATE
        else:
            return PuzzleDifficulty.SIMPLE
    
    def _generate_behavioral_parameters(self, traits: List[str], trait_weights: Dict[str, float]) -> Dict[str, Any]:
        """Generate behavioral parameters from traits and weights."""
        params = {
            'greeting_formality': 0.5,
            'response_patience': 0.5,
            'metaphor_tolerance': 0.5,
            'reputation_sensitivity': 0.5,
            'modifiers': {}
        }
        
        # Apply trait-based modifications
        for trait, weight in trait_weights.items():
            if trait in self.trait_mappings:
                mapping = self.trait_mappings[trait]
                for param, modification in mapping.parameter_modifications.items():
                    if param in params:
                        params[param] = min(1.0, max(0.0, params[param] + (weight * modification)))
                    else:
                        params['modifiers'][param] = weight * modification
        
        return params
    
    def _generate_trigger_words(self, traits: List[str], governor_profile: GovernorProfile) -> List[str]:
        """Generate trigger words based on traits and profile."""
        trigger_words = []
        
        # Base trigger words from traits
        trait_triggers = {
            'mystical': ['sacred', 'divine', 'mystery', 'hidden', 'secret'],
            'scholarly': ['knowledge', 'wisdom', 'learn', 'study', 'ancient'],
            'cryptic': ['riddle', 'puzzle', 'enigma', 'cipher', 'code'],
            'patient': ['time', 'patience', 'understanding', 'careful'],
            'stern': ['discipline', 'order', 'respect', 'honor'],
            'formal': ['ceremony', 'ritual', 'tradition', 'proper']
        }
        
        normalized_traits = [trait.lower().strip() for trait in traits]
        for trait in normalized_traits:
            if trait in trait_triggers:
                trigger_words.extend(trait_triggers[trait])
        
        # Add words from governor name (mystical context)
        governor_name = governor_profile.name.lower()
        if len(governor_name) > 3:
            trigger_words.append(governor_name)
        
        return list(set(trigger_words))  # Remove duplicates
    
    def _generate_forbidden_words(self, traits: List[str]) -> List[str]:
        """Generate forbidden words that cause negative reactions."""
        forbidden_words = []
        
        trait_forbidden = {
            'formal': ['dude', 'whatever', 'casual', 'hey', 'sup'],
            'stern': ['joke', 'silly', 'funny', 'lol', 'haha'],
            'mystical': ['fake', 'nonsense', 'ridiculous', 'stupid'],
            'scholarly': ['boring', 'dull', 'waste', 'pointless'],
            'patient': ['hurry', 'fast', 'quick', 'rush']
        }
        
        normalized_traits = [trait.lower().strip() for trait in traits]
        for trait in normalized_traits:
            if trait in trait_forbidden:
                forbidden_words.extend(trait_forbidden[trait])
        
        return list(set(forbidden_words))  # Remove duplicates
    
    def _generate_preferred_topics(self, governor_profile: GovernorProfile) -> List[str]:
        """Generate preferred topics from profile data."""
        topics = []
        
        # Extract from existing preferences
        if 'puzzle_style' in governor_profile.preferences:
            style = governor_profile.preferences['puzzle_style']
            if style == 'metaphor':
                topics.extend(['symbolism', 'mysticism', 'hidden_meanings'])
            elif style == 'direct':
                topics.extend(['facts', 'logic', 'reasoning'])
        
        # Add topics based on traits
        trait_topics = {
            'mystical': ['occultism', 'spirituality', 'divine_mysteries'],
            'scholarly': ['academia', 'research', 'ancient_texts'],
            'cryptic': ['puzzles', 'riddles', 'hidden_knowledge'],
            'wise': ['philosophy', 'wisdom_traditions', 'life_lessons']
        }
        
        for trait in governor_profile.traits:
            trait_lower = trait.lower().strip()
            if trait_lower in trait_topics:
                topics.extend(trait_topics[trait_lower])
        
        return list(set(topics))  # Remove duplicates
    
    def _create_default_preferences(self, governor_id: str) -> GovernorPreferences:
        """Create default preferences for error cases."""
        logger.warning(f"Creating default preferences for governor {governor_id}")
        
        return GovernorPreferences(
            governor_id=governor_id,
            tone_preference=TonePreference.SCHOLARLY_PATIENT,
            interaction_style="riddle_keeper",
            greeting_formality=0.5,
            puzzle_difficulty=PuzzleDifficulty.MODERATE,
            response_patience=0.7,
            metaphor_tolerance=0.5,
            reputation_sensitivity=0.5,
            trigger_words=['knowledge', 'wisdom'],
            forbidden_words=['casual', 'whatever'],
            preferred_topics=['general_mysticism'],
            behavioral_modifiers={}
        ) 