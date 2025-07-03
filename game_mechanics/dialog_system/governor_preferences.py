"""
Governor Preferences Integration Interface
========================================

This module provides the main interface for the Governor Preferences System,
integrating all components (PreferenceEncoder, TraitMapper, ResponseSelector, 
BehavioralFilter) into a unified API for dialog system use.

Key Components:
- GovernorPreferencesManager: Main interface for preference management
- PreferenceCache: Performance optimization through caching
- IntegratedDialogProcessor: Complete dialog processing pipeline
"""

from typing import Dict, List, Any, Optional, Tuple
import logging
from dataclasses import asdict
import hashlib
import time

from .core_structures import GovernorProfile, PlayerState, DialogResponse, ResponseType
from .preference_structures import GovernorPreferences, PreferenceEncoding
from .preference_encoder import PreferenceEncoder
from .trait_mapper import TraitMapper
from .response_selector import ResponseSelector
from .behavioral_filter import BehavioralFilter, FilterResult

logger = logging.getLogger(__name__)


class GovernorPreferencesManager:
    """
    Main interface for the Governor Preferences System.
    
    This class orchestrates all preference-related components and provides
    a unified API for encoding preferences, selecting responses, and applying
    behavioral filters throughout the dialog system.
    """
    
    def __init__(self, enable_caching: bool = True):
        """
        Initialize the preferences manager with all component systems.
        
        Args:
            enable_caching: Whether to enable preference caching for performance
        """
        self.preference_encoder = PreferenceEncoder()
        self.trait_mapper = TraitMapper()
        self.response_selector = ResponseSelector()
        self.behavioral_filter = BehavioralFilter()
        
        # Performance optimization
        self.enable_caching = enable_caching
        self.preference_cache: Dict[str, GovernorPreferences] = {}
        self.cache_timestamps: Dict[str, float] = {}
        self.cache_ttl = 3600  # 1 hour cache TTL
        
        logger.info("GovernorPreferencesManager initialized with all systems")
    
    def get_governor_preferences(self, governor_profile: GovernorProfile, 
                               force_refresh: bool = False) -> GovernorPreferences:
        """
        Get or generate preferences for a governor.
        
        Args:
            governor_profile: The governor profile to analyze
            force_refresh: Force regeneration even if cached
            
        Returns:
            Complete preferences for the governor
        """
        cache_key = governor_profile.governor_id
        
        # Check cache first
        if self.enable_caching and not force_refresh and self._is_cache_valid(cache_key):
            logger.debug(f"Returning cached preferences for {cache_key}")
            return self.preference_cache[cache_key]
        
        logger.info(f"Generating preferences for governor {governor_profile.governor_id}")
        
        try:
            # Step 1: Encode base preferences from profile
            base_preferences = self.preference_encoder.encode_governor_preferences(governor_profile)
            
            # Step 2: Apply trait mappings for refinement
            refined_preferences = self.trait_mapper.apply_trait_mappings_to_preferences(
                governor_profile, base_preferences
            )
            
            # Cache the result
            if self.enable_caching:
                self.preference_cache[cache_key] = refined_preferences
                self.cache_timestamps[cache_key] = time.time()
            
            logger.info(f"Successfully generated preferences for {governor_profile.governor_id}")
            return refined_preferences
            
        except Exception as e:
            logger.error(f"Failed to generate preferences for {governor_profile.governor_id}: {e}")
            # Return basic fallback preferences
            return self._create_fallback_preferences(governor_profile.governor_id)
    
    def process_dialog_interaction(self, player_input: str, 
                                 response_variants: List[str],
                                 governor_profile: GovernorProfile,
                                 player_state: PlayerState,
                                 context: Dict[str, Any]) -> DialogResponse:
        """
        Process a complete dialog interaction using preferences.
        
        Args:
            player_input: Player's input text
            response_variants: Available response variants
            governor_profile: Governor profile
            player_state: Current player state
            context: Interaction context
            
        Returns:
            Complete dialog response with all preference modifications applied
        """
        logger.info(f"Processing dialog interaction for governor {governor_profile.governor_id}")
        
        try:
            # Step 1: Get governor preferences
            preferences = self.get_governor_preferences(governor_profile)
            
            # Step 2: Apply behavioral constraints to the interaction
            interaction_data = {
                'player_input': player_input,
                'context': context,
                'required_reputation': context.get('required_reputation', 0)
            }
            
            constraint_result = self.behavioral_filter.apply_behavioral_constraints(
                interaction_data, preferences, player_state
            )
            
            if not constraint_result.passed:
                logger.warning(f"Interaction failed behavioral constraints: {constraint_result.reasons}")
                return self._create_constraint_violation_response(constraint_result)
            
            # Step 3: Select appropriate response variant
            enhanced_context = {**context, 'constraint_result': constraint_result}
            selected_response = self.response_selector.select_response_variant(
                response_variants, preferences, enhanced_context
            )
            
            # Step 4: Apply content filtering
            content_filter_result = self.behavioral_filter.filter_content_by_preferences(
                selected_response, preferences
            )
            
            if not content_filter_result.passed:
                logger.warning(f"Response failed content filtering: {content_filter_result.reasons}")
                selected_response = "I must consider my words more carefully..."
            else:
                selected_response = content_filter_result.filtered_content or selected_response
            
            # Step 5: Calculate reputation impact
            interaction_result = {
                'base_reputation': context.get('base_reputation', 1),
                'success': constraint_result.passed and content_filter_result.passed,
                'failure': not (constraint_result.passed and content_filter_result.passed)
            }
            
            reputation_change = self.behavioral_filter.calculate_reputation_impact(
                interaction_result, preferences
            )
            
            # Step 6: Create final response
            response = DialogResponse(
                response_text=selected_response,
                response_type=ResponseType.SUCCESS if constraint_result.passed else ResponseType.FAILURE,
                reputation_change=reputation_change,
                metadata={
                    'preference_applied': True,
                    'constraint_violations': constraint_result.constraint_violations,
                    'content_modifications': content_filter_result.modifications_applied,
                    'tone_preference': preferences.tone_preference.value,
                    'interaction_style': preferences.interaction_style
                }
            )
            
            logger.info(f"Dialog interaction processed successfully with {reputation_change} reputation change")
            return response
            
        except Exception as e:
            logger.error(f"Error processing dialog interaction: {e}")
            return self._create_error_response(str(e))
    
    def get_preference_summary(self, governor_id: str) -> Dict[str, Any]:
        """
        Get a summary of preferences for a governor.
        
        Args:
            governor_id: The governor to summarize
            
        Returns:
            Dictionary containing preference summary
        """
        if governor_id in self.preference_cache:
            preferences = self.preference_cache[governor_id]
            return {
                'governor_id': preferences.governor_id,
                'tone_preference': preferences.tone_preference.value,
                'interaction_style': preferences.interaction_style,
                'greeting_formality': preferences.greeting_formality,
                'puzzle_difficulty': preferences.puzzle_difficulty.value,
                'response_patience': preferences.response_patience,
                'metaphor_tolerance': preferences.metaphor_tolerance,
                'trigger_words_count': len(preferences.trigger_words),
                'forbidden_words_count': len(preferences.forbidden_words),
                'preferred_topics_count': len(preferences.preferred_topics),
                'behavioral_modifiers_count': len(preferences.behavioral_modifiers)
            }
        else:
            return {'error': f'No preferences found for governor {governor_id}'}
    
    def clear_cache(self, governor_id: Optional[str] = None) -> None:
        """
        Clear preference cache for specific governor or all governors.
        
        Args:
            governor_id: Specific governor to clear, or None for all
        """
        if governor_id:
            self.preference_cache.pop(governor_id, None)
            self.cache_timestamps.pop(governor_id, None)
            logger.info(f"Cleared cache for governor {governor_id}")
        else:
            self.preference_cache.clear()
            self.cache_timestamps.clear()
            logger.info("Cleared all preference cache")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status information about the preferences system."""
        return {
            'cache_enabled': self.enable_caching,
            'cached_governors': len(self.preference_cache),
            'cache_ttl_seconds': self.cache_ttl,
            'trait_mappings_count': len(self.trait_mapper.mappings_registry),
            'conflicts_recorded': len(self.trait_mapper.parameter_conflicts),
            'system_components': {
                'preference_encoder': 'active',
                'trait_mapper': 'active', 
                'response_selector': 'active',
                'behavioral_filter': 'active'
            }
        }
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached preferences are still valid."""
        if cache_key not in self.preference_cache:
            return False
        
        if cache_key not in self.cache_timestamps:
            return False
        
        cache_age = time.time() - self.cache_timestamps[cache_key]
        return cache_age < self.cache_ttl
    
    def _create_fallback_preferences(self, governor_id: str) -> GovernorPreferences:
        """Create fallback preferences when encoding fails."""
        from .preference_structures import TonePreference, PuzzleDifficulty
        
        logger.warning(f"Creating fallback preferences for {governor_id}")
        
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
    
    def _create_constraint_violation_response(self, constraint_result: FilterResult) -> DialogResponse:
        """Create response for when behavioral constraints are violated."""
        violation_messages = {
            'excessive_casualness': "Your casual manner is unbecoming in my presence.",
            'insufficient_formality': "Proper respect is required when addressing me.",
            'insufficient_reputation': "You have not yet earned the right to make such requests.",
            'excessive_haste': "Patience, seeker. Wisdom cannot be rushed.",
            'daily_limit_exceeded': "I have spoken enough for one day. Return tomorrow."
        }
        
        # Select appropriate message based on violations
        response_text = "Your approach does not meet my expectations."
        if constraint_result.constraint_violations:
            primary_violation = constraint_result.constraint_violations[0]
            response_text = violation_messages.get(primary_violation, response_text)
        
        return DialogResponse(
            response_text=response_text,
            response_type=ResponseType.REBUKE,
            reputation_change=-1,
            metadata={
                'constraint_violations': constraint_result.constraint_violations,
                'violation_reasons': constraint_result.reasons
            }
        )
    
    def _create_error_response(self, error_message: str) -> DialogResponse:
        """Create response for system errors."""
        logger.error(f"Creating error response: {error_message}")
        
        return DialogResponse(
            response_text="The mystical energies are disturbed. Please try again.",
            response_type=ResponseType.FAILURE,
            reputation_change=0,
            metadata={
                'system_error': True,
                'error_message': error_message
            }
        ) 