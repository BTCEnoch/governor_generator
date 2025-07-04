"""
Context-Aware Dialog System for Enochian Governor Generation
===========================================================

This module implements a sophisticated dialog engine designed for on-chain story games
with 91 Enochian Governors. The system combines structured state machines with lightweight
language processing to achieve context-awareness and high variability under strict 
on-chain constraints.

Key Components:
- DialogNode: Core dialog state representation
- GovernorProfile: Governor-specific preferences and behaviors  
- PlayerState: Player progression and context tracking
- DialogEngine: Main processing pipeline for interactions
- NLU Components: Natural language understanding for player input
- Fallback Systems: Robust error handling and recovery

Governor Preferences System:
- GovernorPreferencesManager: Main interface for preference management
- PreferenceEncoder: Converts traits to behavioral preferences
- ResponseSelector: Preference-based response selection
- BehavioralFilter: Governor-specific content filtering
- TraitMapper: Trait-to-behavior mapping system

Usage:
    from tools.game_mechanics.dialog_system import DialogEngine, DialogNode
    from tools.game_mechanics.dialog_system import GovernorPreferencesManager
    
    # Basic dialog processing
    engine = DialogEngine()
    response = engine.process_interaction(player_input, governor_id, player_state)
    
    # Advanced preference-based processing
    preferences_manager = GovernorPreferencesManager()
    response = preferences_manager.process_dialog_interaction(
        player_input, response_variants, governor_profile, player_state, context
    )
"""

# Core dialog system components
from .core_structures import (
    DialogNode, GovernorProfile, PlayerState, DialogResponse,
    InteractionType, IntentCategory, ResponseType
)

# Storage and state management
from .storage_schemas import InscriptionReference, DialogLibrarySchema, StorageManager
from .state_machine import StateMachine, TransitionValidator, StateManager

# NLU and language processing
from .nlu_engine import TokenMatcher, EntityRecognizer, IntentPattern
from .similarity_engine import SimpleEmbedding, SimilarityMatcher
from .intent_classifier import IntentClassifier, ClassificationResult

# Governor Preferences System
from .preference_structures import (
    GovernorPreferences, PreferenceEncoding, TraitBehaviorMapping,
    TonePreference, PuzzleDifficulty, BehaviorType
)
from .preference_encoder import PreferenceEncoder
from .trait_mapper import TraitMapper, MappingConflict
from .response_selector import ResponseSelector
from .behavioral_filter import BehavioralFilter, FilterResult
from .governor_preferences import GovernorPreferencesManager

__version__ = "1.0.0"
__author__ = "Enochian Governor Generation Team"

# Core exports (backward compatibility)
__all__ = [
    # Core structures
    "DialogNode",
    "GovernorProfile", 
    "PlayerState",
    "DialogResponse",
    "InteractionType",
    "IntentCategory", 
    "ResponseType",
    
    # Storage and state
    "InscriptionReference",
    "DialogLibrarySchema",
    "StorageManager",
    "StateMachine",
    "TransitionValidator",
    "StateManager",
    
    # NLU components
    "TokenMatcher",
    "EntityRecognizer", 
    "IntentPattern",
    "SimpleEmbedding",
    "SimilarityMatcher",
    "IntentClassifier",
    "ClassificationResult",
    
    # Governor Preferences System
    "GovernorPreferences",
    "PreferenceEncoding",
    "TraitBehaviorMapping",
    "TonePreference",
    "PuzzleDifficulty",
    "BehaviorType",
    "PreferenceEncoder",
    "TraitMapper",
    "MappingConflict",
    "ResponseSelector",
    "BehavioralFilter",
    "FilterResult",
    "GovernorPreferencesManager",
]

# Convenience groupings for easier imports
PREFERENCE_COMPONENTS = [
    "GovernorPreferences",
    "PreferenceEncoder", 
    "TraitMapper",
    "ResponseSelector",
    "BehavioralFilter",
    "GovernorPreferencesManager"
]

NLU_COMPONENTS = [
    "TokenMatcher",
    "EntityRecognizer",
    "IntentClassifier",
    "SimilarityMatcher"
]

CORE_COMPONENTS = [
    "DialogNode",
    "GovernorProfile",
    "PlayerState", 
    "DialogResponse"
] 
