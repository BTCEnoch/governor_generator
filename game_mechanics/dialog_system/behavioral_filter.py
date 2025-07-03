"""
Behavioral Filter for Governor Dialog System
==========================================

This module implements behavioral filtering for the Context-Aware Dialog System.
It applies governor-specific constraints, content filtering, and behavioral 
modifications based on personality traits and interaction preferences.

Key Components:
- BehavioralFilter: Main filtering engine for governor-specific constraints
- ContentFilter: Filters inappropriate content based on preferences
- InteractionConstraint: Applies behavioral constraints to interactions
"""

from typing import Dict, List, Any, Optional, Tuple, Set
import logging
from dataclasses import dataclass, field

from .preference_structures import GovernorPreferences, TonePreference
from .core_structures import PlayerState, IntentCategory, ResponseType

logger = logging.getLogger(__name__)


@dataclass
class FilterResult:
    """Result of applying behavioral filters to content or interactions."""
    passed: bool
    filtered_content: Optional[str] = None
    reasons: List[str] = field(default_factory=list)
    modifications_applied: List[str] = field(default_factory=list)
    constraint_violations: List[str] = field(default_factory=list)


class BehavioralFilter:
    """
    Main filtering engine that applies governor-specific constraints and 
    behavioral modifications to dialog content and interactions.
    
    This class ensures that all content and interactions align with each
    governor's personality traits and behavioral preferences.
    """
    
    def __init__(self):
        """Initialize the behavioral filter with constraint rules."""
        self.interaction_constraints = self._initialize_interaction_constraints()
        self.content_filters = self._initialize_content_filters()
        self.reputation_modifiers = self._initialize_reputation_modifiers()
        logger.info("BehavioralFilter initialized with constraint and filtering rules")
    
    def apply_behavioral_constraints(self, interaction_data: Dict[str, Any], 
                                   preferences: GovernorPreferences,
                                   player_state: PlayerState) -> FilterResult:
        """
        Apply behavioral constraints to an interaction attempt.
        
        Args:
            interaction_data: Data about the attempted interaction
            preferences: Governor's behavioral preferences
            player_state: Current player state
            
        Returns:
            FilterResult indicating if interaction is allowed and any modifications
        """
        logger.debug(f"Applying behavioral constraints for governor {preferences.governor_id}")
        
        result = FilterResult(passed=True)
        
        try:
            # Check formality requirements
            formality_result = self._check_formality_constraints(interaction_data, preferences)
            if not formality_result.passed:
                result.passed = False
                result.constraint_violations.extend(formality_result.constraint_violations)
                result.reasons.extend(formality_result.reasons)
            
            # Check reputation requirements
            reputation_result = self._check_reputation_constraints(interaction_data, preferences, player_state)
            if not reputation_result.passed:
                result.passed = False
                result.constraint_violations.extend(reputation_result.constraint_violations)
                result.reasons.extend(reputation_result.reasons)
            
            # Check patience constraints
            patience_result = self._check_patience_constraints(interaction_data, preferences)
            if not patience_result.passed:
                result.passed = False
                result.constraint_violations.extend(patience_result.constraint_violations)
                result.reasons.extend(patience_result.reasons)
            
            # Apply behavioral modifications if constraints passed
            if result.passed:
                modification_result = self._apply_behavioral_modifications(interaction_data, preferences)
                result.filtered_content = modification_result.filtered_content
                result.modifications_applied = modification_result.modifications_applied
            
            logger.debug(f"Behavioral constraints check: {'PASSED' if result.passed else 'FAILED'}")
            return result
            
        except Exception as e:
            logger.error(f"Error applying behavioral constraints: {e}")
            result.passed = False
            result.reasons.append(f"Internal error: {str(e)}")
            return result
    
    def filter_content_by_preferences(self, content: str, preferences: GovernorPreferences) -> FilterResult:
        """
        Filter content based on governor preferences.
        
        Args:
            content: Content to filter
            preferences: Governor's behavioral preferences
            
        Returns:
            FilterResult with filtered content and modification details
        """
        logger.debug(f"Filtering content for governor {preferences.governor_id}")
        
        result = FilterResult(passed=True, filtered_content=content)
        
        try:
            # Check for forbidden words
            forbidden_result = self._filter_forbidden_content(content, preferences)
            if not forbidden_result.passed:
                result.passed = False
                result.reasons.extend(forbidden_result.reasons)
                return result
            
            # Apply tone-based content modifications
            tone_result = self._apply_tone_content_filter(content, preferences.tone_preference)
            result.filtered_content = tone_result.filtered_content
            result.modifications_applied.extend(tone_result.modifications_applied)
            
            # Apply metaphor tolerance filtering
            content_for_metaphor = result.filtered_content or content
            metaphor_result = self._apply_metaphor_filter(content_for_metaphor, preferences)
            result.filtered_content = metaphor_result.filtered_content
            result.modifications_applied.extend(metaphor_result.modifications_applied)
            
            logger.debug(f"Content filtering completed with {len(result.modifications_applied)} modifications")
            return result
            
        except Exception as e:
            logger.error(f"Error filtering content: {e}")
            result.passed = False
            result.reasons.append(f"Content filtering error: {str(e)}")
            return result
    
    def validate_interaction_appropriateness(self, intent: IntentCategory, 
                                           preferences: GovernorPreferences,
                                           context: Dict[str, Any]) -> FilterResult:
        """
        Validate if an interaction intent is appropriate for the governor.
        
        Args:
            intent: The player's interaction intent
            preferences: Governor's behavioral preferences
            context: Current interaction context
            
        Returns:
            FilterResult indicating if the interaction is appropriate
        """
        logger.debug(f"Validating interaction intent {intent.value} for governor {preferences.governor_id}")
        
        result = FilterResult(passed=True)
        
        # Check if intent matches governor's interaction style
        if not self._is_intent_compatible(intent, preferences):
            result.passed = False
            result.reasons.append(f"Intent {intent.value} incompatible with governor's {preferences.interaction_style} style")
            return result
        
        # Check context-specific constraints
        context_result = self._validate_context_constraints(intent, preferences, context)
        if not context_result.passed:
            result.passed = False
            result.reasons.extend(context_result.reasons)
            result.constraint_violations.extend(context_result.constraint_violations)
        
        logger.debug(f"Interaction validation: {'APPROPRIATE' if result.passed else 'INAPPROPRIATE'}")
        return result
    
    def calculate_reputation_impact(self, interaction_result: Dict[str, Any], 
                                  preferences: GovernorPreferences) -> int:
        """
        Calculate reputation impact based on governor preferences and interaction outcome.
        
        Args:
            interaction_result: Result data from the interaction
            preferences: Governor's behavioral preferences
            
        Returns:
            Reputation change amount (positive or negative)
        """
        base_reputation = interaction_result.get('base_reputation', 0)
        
        # Apply reputation sensitivity modifier
        sensitivity_modifier = preferences.reputation_sensitivity
        modified_reputation = int(base_reputation * sensitivity_modifier)
        
        # Apply additional modifiers based on behavioral parameters
        if 'success' in interaction_result and interaction_result['success']:
            success_bonus = preferences.get_behavioral_modifier('success_bonus', 1.0)
            modified_reputation = int(modified_reputation * success_bonus)
        
        if 'failure_penalty' in preferences.behavioral_modifiers:
            failure_modifier = preferences.behavioral_modifiers['failure_penalty']
            if 'failure' in interaction_result and interaction_result['failure']:
                modified_reputation = int(modified_reputation * (1.0 + failure_modifier))
        
        logger.debug(f"Reputation calculation: {base_reputation} -> {modified_reputation} (sensitivity: {sensitivity_modifier:.2f})")
        return modified_reputation
    
    def _initialize_interaction_constraints(self) -> Dict[str, Any]:
        """Initialize interaction constraint rules."""
        return {
            'formality_thresholds': {
                'strict': 0.8,
                'moderate': 0.5,
                'relaxed': 0.2
            },
            'reputation_requirements': {
                'basic': 0,
                'intermediate': 5,
                'advanced': 10,
                'master': 15
            },
            'patience_limits': {
                'impatient': 0.3,
                'normal': 0.6,
                'patient': 0.9
            }
        }
    
    def _initialize_content_filters(self) -> Dict[str, List[str]]:
        """Initialize content filtering rules."""
        return {
            'profanity': ['damn', 'hell', 'crap'],
            'modern_references': ['internet', 'computer', 'phone', 'email'],
            'casual_speech': ['yeah', 'ok', 'cool', 'awesome'],
            'disrespectful': ['stupid', 'dumb', 'idiot', 'moron']
        }
    
    def _initialize_reputation_modifiers(self) -> Dict[str, float]:
        """Initialize reputation impact modifiers."""
        return {
            'success_multiplier': 1.2,
            'failure_penalty': 0.8,
            'respect_bonus': 1.1,
            'disrespect_penalty': 0.5
        }
    
    def _check_formality_constraints(self, interaction_data: Dict[str, Any], 
                                   preferences: GovernorPreferences) -> FilterResult:
        """Check if interaction meets formality requirements."""
        result = FilterResult(passed=True)
        
        player_input = interaction_data.get('player_input', '')
        required_formality = preferences.greeting_formality
        
        # Simple formality check based on keywords
        formal_indicators = ['please', 'respectfully', 'kindly', 'may i', 'would you']
        casual_indicators = ['hey', 'yo', 'sup', 'whatever']
        
        input_lower = player_input.lower()
        formal_count = sum(1 for word in formal_indicators if word in input_lower)
        casual_count = sum(1 for word in casual_indicators if word in input_lower)
        
        if required_formality > 0.7 and casual_count > 0:
            result.passed = False
            result.reasons.append("Governor requires formal address")
            result.constraint_violations.append("excessive_casualness")
        
        if required_formality > 0.8 and formal_count == 0:
            result.passed = False
            result.reasons.append("Governor requires explicit formal courtesy")
            result.constraint_violations.append("insufficient_formality")
        
        return result
    
    def _check_reputation_constraints(self, interaction_data: Dict[str, Any], 
                                    preferences: GovernorPreferences,
                                    player_state: PlayerState) -> FilterResult:
        """Check if player meets reputation requirements."""
        result = FilterResult(passed=True)
        
        current_reputation = player_state.get_reputation(preferences.governor_id)
        required_reputation = interaction_data.get('required_reputation', 0)
        
        if current_reputation < required_reputation:
            result.passed = False
            result.reasons.append(f"Insufficient reputation: {current_reputation} < {required_reputation}")
            result.constraint_violations.append("insufficient_reputation")
        
        return result
    
    def _check_patience_constraints(self, interaction_data: Dict[str, Any], 
                                  preferences: GovernorPreferences) -> FilterResult:
        """Check patience-related constraints."""
        result = FilterResult(passed=True)
        
        # Check if player is being too hasty or impatient
        player_input = interaction_data.get('player_input', '')
        haste_indicators = ['hurry', 'quick', 'fast', 'now', 'immediately']
        
        if preferences.response_patience > 0.7:  # Patient governor
            input_lower = player_input.lower()
            if any(indicator in input_lower for indicator in haste_indicators):
                result.passed = False
                result.reasons.append("Governor values patience and deliberation")
                result.constraint_violations.append("excessive_haste")
        
        return result
    
    def _apply_behavioral_modifications(self, interaction_data: Dict[str, Any], 
                                      preferences: GovernorPreferences) -> FilterResult:
        """Apply behavioral modifications to interaction."""
        result = FilterResult(passed=True)
        
        # Apply tone-based modifications
        if 'response_template' in interaction_data:
            modified_template = interaction_data['response_template']
            
            # Add formality modifications
            if preferences.greeting_formality > 0.8:
                modified_template = f"*speaks with formal dignity* {modified_template}"
                result.modifications_applied.append("formal_dignity_prefix")
            
            # Add patience modifications
            if preferences.response_patience > 0.8:
                modified_template = modified_template.replace(".", "... ")
                result.modifications_applied.append("patience_pacing")
            
            result.filtered_content = modified_template
        
        return result
    
    def _filter_forbidden_content(self, content: str, preferences: GovernorPreferences) -> FilterResult:
        """Filter out forbidden content based on preferences."""
        result = FilterResult(passed=True)
        
        # Check against forbidden words
        if preferences.has_forbidden_word(content):
            result.passed = False
            result.reasons.append("Content contains forbidden words")
        
        # Check against content filters
        content_lower = content.lower()
        for category, words in self.content_filters.items():
            if any(word in content_lower for word in words):
                if category == 'profanity':
                    result.passed = False
                    result.reasons.append("Content contains inappropriate language")
                    break
        
        return result
    
    def _apply_tone_content_filter(self, content: str, tone_preference: TonePreference) -> FilterResult:
        """Apply tone-based content filtering."""
        result = FilterResult(passed=True, filtered_content=content)
        
        # Apply tone-specific modifications
        if tone_preference == TonePreference.MYSTICAL_POETIC:
            if 'truth' in content.lower():
                result.filtered_content = content.replace('truth', 'sacred truth')
                result.modifications_applied.append("mystical_language_enhancement")
        
        elif tone_preference == TonePreference.SCHOLARLY_PATIENT:
            if 'wrong' in content.lower():
                result.filtered_content = content.replace('wrong', 'not quite accurate')
                result.modifications_applied.append("scholarly_softening")
        
        return result
    
    def _apply_metaphor_filter(self, content: str, preferences: GovernorPreferences) -> FilterResult:
        """Apply metaphor tolerance filtering."""
        result = FilterResult(passed=True, filtered_content=content)
        
        if preferences.metaphor_tolerance < 0.3:  # Low metaphor tolerance
            # Convert metaphors to more literal language
            metaphor_replacements = {
                'shadow of doubt': 'uncertainty',
                'light of understanding': 'clarity',
                'path of wisdom': 'learning process'
            }
            
            modified_content = content
            for metaphor, literal in metaphor_replacements.items():
                if metaphor in modified_content.lower():
                    modified_content = modified_content.replace(metaphor, literal)
                    result.modifications_applied.append(f"literalized_{metaphor.replace(' ', '_')}")
            
            result.filtered_content = modified_content
        
        return result
    
    def _is_intent_compatible(self, intent: IntentCategory, preferences: GovernorPreferences) -> bool:
        """Check if intent is compatible with governor's interaction style."""
        compatibility_map = {
            'riddle_keeper': [IntentCategory.RIDDLE_ANSWER, IntentCategory.QUESTION],
            'ceremonial_governor': [IntentCategory.FORMAL_GREETING, IntentCategory.RITUAL_PHRASE],
            'secret_keeper': [IntentCategory.SECRET_KNOWLEDGE, IntentCategory.FORMAL_GREETING],
            'tribute_taker': [IntentCategory.OFFERING, IntentCategory.FORMAL_GREETING]
        }
        
        compatible_intents = compatibility_map.get(preferences.interaction_style, [])
        return intent in compatible_intents or intent == IntentCategory.FORMAL_GREETING  # Always allow formal greetings
    
    def _validate_context_constraints(self, intent: IntentCategory, preferences: GovernorPreferences, 
                                    context: Dict[str, Any]) -> FilterResult:
        """Validate context-specific constraints."""
        result = FilterResult(passed=True)
        
        # Check time-based constraints
        if 'interaction_count' in context:
            daily_limit = preferences.get_behavioral_modifier('daily_interaction_limit', 10)
            if context['interaction_count'] >= daily_limit:
                result.passed = False
                result.reasons.append("Daily interaction limit reached")
                result.constraint_violations.append("daily_limit_exceeded")
        
        # Check sequential interaction constraints
        if intent == IntentCategory.RIDDLE_ANSWER and 'last_interaction' in context:
            if context['last_interaction'] != 'riddle_posed':
                result.passed = False
                result.reasons.append("Cannot answer riddle without one being posed")
                result.constraint_violations.append("invalid_sequence")
        
        return result 