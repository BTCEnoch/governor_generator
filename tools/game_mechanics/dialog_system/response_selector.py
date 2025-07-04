"""
Response Selector for Governor Dialog System
==========================================

This module implements preference-based response selection for the Context-Aware
Dialog System. It analyzes governor preferences to choose appropriate response
variants and applies tone modifications to match governor personalities.

Key Components:
- ResponseSelector: Main response selection engine
- ToneModifier: Applies tone-based modifications to responses
- ContextAnalyzer: Analyzes interaction context for better selection
"""

from typing import Dict, List, Any, Optional, Tuple
import logging
import hashlib
import re

from .preference_structures import GovernorPreferences, TonePreference
from .core_structures import PlayerState

logger = logging.getLogger(__name__)

class ResponseSelector:
    """
    Main response selection engine that chooses appropriate dialog variants
    based on governor preferences and interaction context.
    
    This class implements the core logic for matching responses to governor
    personalities and filtering inappropriate content based on preferences.
    """
    
    def __init__(self):
        """Initialize the response selector with tone modification rules."""
        self.tone_modifiers = self._initialize_tone_modifiers()
        self.forbidden_patterns = self._initialize_forbidden_patterns()
        self.preference_weights = self._initialize_preference_weights()
        logger.info("ResponseSelector initialized with tone modification and filtering rules")
    
    def select_response_variant(self, variants: List[str], preferences: GovernorPreferences, 
                               context: Dict[str, Any]) -> str:
        """
        Select the most appropriate response variant based on preferences and context.
        
        Args:
            variants: List of available response variants
            preferences: Governor's behavioral preferences
            context: Current interaction context
            
        Returns:
            Selected and potentially modified response text
        """
        if not variants:
            logger.warning("No response variants provided for selection")
            return "I must contemplate your words further, seeker."
        
        logger.debug(f"Selecting from {len(variants)} variants for governor {preferences.governor_id}")
        
        try:
            # Step 1: Filter inappropriate responses
            filtered_variants = self.filter_inappropriate_responses(variants, preferences)
            
            if not filtered_variants:
                logger.warning("All responses filtered out, using fallback")
                filtered_variants = [variants[0]]  # Fallback to first variant
            
            # Step 2: Score variants by preference alignment
            scored_variants = self._score_variants_by_preferences(filtered_variants, preferences, context)
            
            # Step 3: Select highest scoring variant (with deterministic tie-breaking)
            selected_variant = self._select_best_variant(scored_variants, context)
            
            # Step 4: Apply tone modifications
            modified_response = self.apply_tone_modifications(selected_variant, preferences.tone_preference)
            
            logger.debug(f"Selected variant with score {scored_variants[selected_variant]:.3f}")
            return modified_response
            
        except Exception as e:
            logger.error(f"Error in response selection: {e}")
            return self.apply_tone_modifications(variants[0], preferences.tone_preference)
    
    def filter_inappropriate_responses(self, responses: List[str], 
                                     preferences: GovernorPreferences) -> List[str]:
        """
        Filter out responses that don't match governor preferences.
        
        Args:
            responses: List of response candidates
            preferences: Governor's behavioral preferences
            
        Returns:
            Filtered list of appropriate responses
        """
        filtered_responses = []
        
        for response in responses:
            response_lower = response.lower()
            
            # Check for forbidden words
            if preferences.has_forbidden_word(response):
                logger.debug(f"Filtered response containing forbidden words: {response[:50]}...")
                continue
            
            # Check formality level
            if not self._matches_formality_preference(response, preferences):
                logger.debug(f"Filtered response due to formality mismatch: {response[:50]}...")
                continue
            
            # Check metaphor tolerance
            if not self._matches_metaphor_preference(response, preferences):
                logger.debug(f"Filtered response due to metaphor mismatch: {response[:50]}...")
                continue
            
            filtered_responses.append(response)
        
        logger.debug(f"Filtered {len(responses)} responses down to {len(filtered_responses)}")
        return filtered_responses
    
    def apply_tone_modifications(self, response: str, tone_preference: TonePreference) -> str:
        """
        Apply tone-based modifications to a response.
        
        Args:
            response: Original response text
            tone_preference: Desired tone for the response
            
        Returns:
            Modified response with appropriate tone
        """
        if tone_preference not in self.tone_modifiers:
            logger.debug(f"No tone modifier found for {tone_preference}, returning original")
            return response
        
        modifiers = self.tone_modifiers[tone_preference]
        modified_response = response
        
        # Apply prefix modification
        if 'prefix' in modifiers and modifiers['prefix']:
            modified_response = f"{modifiers['prefix']} {modified_response}"
        
        # Apply suffix modification
        if 'suffix' in modifiers and modifiers['suffix']:
            modified_response = f"{modified_response} {modifiers['suffix']}"
        
        # Apply word replacements
        if 'replacements' in modifiers:
            for original, replacement in modifiers['replacements'].items():
                pattern = r'\b' + re.escape(original) + r'\b'
                modified_response = re.sub(pattern, replacement, modified_response, flags=re.IGNORECASE)
        
        # Apply punctuation modifications
        if 'punctuation' in modifiers:
            punct_rules = modifiers['punctuation']
            if 'ellipsis' in punct_rules and punct_rules['ellipsis']:
                modified_response = modified_response.replace('.', '...')
            if 'formal_ending' in punct_rules and punct_rules['formal_ending']:
                if not modified_response.endswith(('.', '!', '?')):
                    modified_response += '.'
        
        logger.debug(f"Applied {tone_preference} tone modification")
        return modified_response
    
    def _initialize_tone_modifiers(self) -> Dict[TonePreference, Dict[str, Any]]:
        """Initialize tone modification rules for each tone preference."""
        return {
            TonePreference.SOLEMN_CRYPTIC: {
                'prefix': '',
                'suffix': '',
                'replacements': {
                    'yes': 'indeed',
                    'no': 'nay',
                    'understand': 'perceive',
                    'think': 'contemplate'
                },
                'punctuation': {'ellipsis': True, 'formal_ending': True}
            },
            
            TonePreference.MYSTICAL_POETIC: {
                'prefix': '',
                'suffix': ', blessed seeker',
                'replacements': {
                    'know': 'divine',
                    'see': 'witness',
                    'truth': 'sacred truth',
                    'wisdom': 'ancient wisdom'
                },
                'punctuation': {'ellipsis': False, 'formal_ending': True}
            },
            
            TonePreference.SCHOLARLY_PATIENT: {
                'prefix': '',
                'suffix': '',
                'replacements': {
                    'wrong': 'not quite accurate',
                    'stupid': 'unwise',
                    'failure': 'learning opportunity'
                },
                'punctuation': {'ellipsis': False, 'formal_ending': True}
            },
            
            TonePreference.STERN_FORMAL: {
                'prefix': '',
                'suffix': '',
                'replacements': {
                    'please': 'you must',
                    'maybe': 'perhaps',
                    'ok': 'very well'
                },
                'punctuation': {'ellipsis': False, 'formal_ending': True}
            },
            
            TonePreference.ENIGMATIC_BRIEF: {
                'prefix': '',
                'suffix': '',
                'replacements': {},
                'punctuation': {'ellipsis': True, 'formal_ending': False}
            },
            
            TonePreference.PLAYFUL_RIDDLES: {
                'prefix': '',
                'suffix': ', clever one',
                'replacements': {
                    'difficult': 'challenging',
                    'problem': 'puzzle',
                    'answer': 'solution'
                },
                'punctuation': {'ellipsis': False, 'formal_ending': False}
            },
            
            TonePreference.COLD_DISTANT: {
                'prefix': '',
                'suffix': '',
                'replacements': {
                    'friend': 'seeker',
                    'please': 'you will',
                    'thank you': 'acknowledged'
                },
                'punctuation': {'ellipsis': False, 'formal_ending': True}
            },
            
            TonePreference.WARM_ENCOURAGING: {
                'prefix': '',
                'suffix': ', dear seeker',
                'replacements': {
                    'wrong': 'not quite there yet',
                    'failure': 'attempt',
                    'difficult': 'challenging but achievable'
                },
                'punctuation': {'ellipsis': False, 'formal_ending': False}
            }
        }
    
    def _initialize_forbidden_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns that should be filtered based on tone preferences."""
        return {
            'overly_casual': ['dude', 'hey', 'sup', 'lol', 'whatever'],
            'disrespectful': ['stupid', 'dumb', 'ridiculous', 'nonsense'],
            'modern_slang': ['cool', 'awesome', 'sick', 'lit', 'fire']
        }
    
    def _initialize_preference_weights(self) -> Dict[str, float]:
        """Initialize weights for different preference factors in scoring."""
        return {
            'formality_match': 0.3,
            'metaphor_alignment': 0.2,
            'trigger_word_bonus': 0.2,
            'topic_relevance': 0.2,
            'tone_consistency': 0.1
        }
    
    def _score_variants_by_preferences(self, variants: List[str], preferences: GovernorPreferences, 
                                     context: Dict[str, Any]) -> Dict[str, float]:
        """Score response variants based on preference alignment."""
        scores = {}
        
        for variant in variants:
            score = 0.0
            
            # Formality scoring
            formality_score = self._calculate_formality_score(variant, preferences.greeting_formality)
            score += formality_score * self.preference_weights['formality_match']
            
            # Metaphor scoring
            metaphor_score = self._calculate_metaphor_score(variant, preferences.metaphor_tolerance)
            score += metaphor_score * self.preference_weights['metaphor_alignment']
            
            # Trigger word bonus
            if preferences.has_trigger_word(variant):
                score += self.preference_weights['trigger_word_bonus']
            
            # Topic relevance (if context provides topic info)
            topic_score = self._calculate_topic_relevance(variant, preferences, context)
            score += topic_score * self.preference_weights['topic_relevance']
            
            scores[variant] = score
        
        return scores
    
    def _select_best_variant(self, scored_variants: Dict[str, float], context: Dict[str, Any]) -> str:
        """Select the highest scoring variant with deterministic tie-breaking."""
        if not scored_variants:
            return "I ponder your words in silence."
        
        max_score = max(scored_variants.values())
        best_variants = [variant for variant, score in scored_variants.items() if score == max_score]
        
        if len(best_variants) == 1:
            return best_variants[0]
        
        # Deterministic tie-breaking using context hash
        context_str = str(sorted(context.items())) if context else "default"
        hash_value = int(hashlib.sha256(context_str.encode()).hexdigest(), 16)
        selected_index = hash_value % len(best_variants)
        
        return best_variants[selected_index]
    
    def _matches_formality_preference(self, response: str, preferences: GovernorPreferences) -> bool:
        """Check if response matches governor's formality preference."""
        response_formality = self._calculate_formality_score(response, 0.5)  # Neutral baseline
        formality_diff = abs(response_formality - preferences.greeting_formality)
        
        # Allow responses within 0.3 range of preferred formality
        return formality_diff <= 0.3
    
    def _matches_metaphor_preference(self, response: str, preferences: GovernorPreferences) -> bool:
        """Check if response matches governor's metaphor tolerance."""
        response_metaphor = self._calculate_metaphor_score(response, 0.5)  # Neutral baseline
        metaphor_diff = abs(response_metaphor - preferences.metaphor_tolerance)
        
        # Allow responses within 0.4 range of preferred metaphor level
        return metaphor_diff <= 0.4
    
    def _calculate_formality_score(self, text: str, baseline: float) -> float:
        """Calculate formality score of text (0.0 = casual, 1.0 = formal)."""
        formal_indicators = ['please', 'kindly', 'respectfully', 'indeed', 'shall', 'might', 'would']
        casual_indicators = ['hey', 'yeah', 'ok', 'gonna', 'wanna', 'cool']
        
        formal_count = sum(1 for word in formal_indicators if word in text.lower())
        casual_count = sum(1 for word in casual_indicators if word in text.lower())
        
        # Adjust baseline based on indicators
        if formal_count > casual_count:
            return min(1.0, baseline + 0.1 * (formal_count - casual_count))
        elif casual_count > formal_count:
            return max(0.0, baseline - 0.1 * (casual_count - formal_count))
        
        return baseline
    
    def _calculate_metaphor_score(self, text: str, baseline: float) -> float:
        """Calculate metaphor usage score (0.0 = literal, 1.0 = highly metaphorical)."""
        metaphor_indicators = ['like', 'as', 'shadow', 'light', 'path', 'journey', 'veil', 'mirror']
        literal_indicators = ['exactly', 'precisely', 'specifically', 'clearly', 'directly']
        
        metaphor_count = sum(1 for word in metaphor_indicators if word in text.lower())
        literal_count = sum(1 for word in literal_indicators if word in text.lower())
        
        if metaphor_count > literal_count:
            return min(1.0, baseline + 0.1 * (metaphor_count - literal_count))
        elif literal_count > metaphor_count:
            return max(0.0, baseline - 0.1 * (literal_count - metaphor_count))
        
        return baseline
    
    def _calculate_topic_relevance(self, text: str, preferences: GovernorPreferences, 
                                 context: Dict[str, Any]) -> float:
        """Calculate how well text aligns with preferred topics."""
        if not preferences.preferred_topics:
            return 0.5  # Neutral score if no preferences
        
        text_lower = text.lower()
        relevance_score = 0.0
        
        for topic in preferences.preferred_topics:
            topic_words = topic.lower().replace('_', ' ').split()
            topic_matches = sum(1 for word in topic_words if word in text_lower)
            if topic_matches > 0:
                relevance_score += topic_matches / len(topic_words)
        
        return min(1.0, relevance_score / len(preferences.preferred_topics)) 