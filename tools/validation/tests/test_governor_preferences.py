#!/usr/bin/env python3
"""
Comprehensive Test Suite for Governor Preferences System
======================================================

This module provides thorough testing of all governor preference components
including unit tests, integration tests, and performance validation.
"""

import unittest
import time
import sys
from pathlib import Path
from unittest.mock import Mock, patch
from dataclasses import dataclass
from typing import Dict, Any, List

# .parent.parent))  # Removed during reorganization

from tools.game_mechanics.dialog_system import (
    GovernorPreferencesManager,
    GovernorProfile,
    PlayerState,
    ResponseType,
    InteractionType,
    PreferenceEncoder,
    TraitMapper,
    ResponseSelector,
    BehavioralFilter,
    GovernorPreferences,
    TonePreference,
    PuzzleDifficulty,
    PreferenceEncoding,
    TraitBehaviorMapping,
    BehaviorType
)

class TestPreferenceEncoder(unittest.TestCase):
    """Test the PreferenceEncoder component"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.encoder = PreferenceEncoder()
        self.sample_profile = GovernorProfile(
            governor_id='test_governor',
            name='Test Governor',
            traits=['mystical', 'scholarly', 'patient'],
            preferences={'tone': 'formal'}
        )
        
    def test_encoder_initialization(self):
        """Test encoder initializes correctly"""
        self.assertIsNotNone(self.encoder)
        self.assertIsInstance(self.encoder.trait_mappings, dict)
        self.assertGreater(len(self.encoder.trait_mappings), 0)
        print("✅ PreferenceEncoder initialization test passed")
    
    def test_trait_weight_calculation(self):
        """Test trait weight calculation"""
        traits = ['mystical', 'scholarly', 'patient']
        trait_weights = self.encoder.calculate_trait_weights(traits)
        
        self.assertIsInstance(trait_weights, dict)
        self.assertEqual(len(trait_weights), len(traits))
        
        # Check that weights sum to approximately 1.0
        total_weight = sum(trait_weights.values())
        self.assertAlmostEqual(total_weight, 1.0, places=2)
        print(f"✅ Trait weight calculation test passed: {trait_weights}")
    
    def test_preference_encoding(self):
        """Test complete preference encoding process"""
        preferences = self.encoder.encode_governor_preferences(self.sample_profile)
        
        self.assertIsInstance(preferences, GovernorPreferences)
        self.assertEqual(preferences.governor_id, 'test_governor')
        self.assertIsInstance(preferences.tone_preference, TonePreference)
        self.assertIsInstance(preferences.puzzle_difficulty, PuzzleDifficulty)
        
        # Check parameter ranges
        self.assertGreaterEqual(preferences.greeting_formality, 0.0)
        self.assertLessEqual(preferences.greeting_formality, 1.0)
        self.assertGreaterEqual(preferences.response_patience, 0.0)
        self.assertLessEqual(preferences.response_patience, 1.0)
        
        print(f"✅ Preference encoding test passed: {preferences.tone_preference.value}")
    
    def test_error_handling(self):
        """Test encoder handles invalid input gracefully"""
        empty_profile = GovernorProfile(
            governor_id='empty',
            name='Empty Governor',
            traits=[],
            preferences={}
        )
        
        preferences = self.encoder.encode_governor_preferences(empty_profile)
        self.assertIsInstance(preferences, GovernorPreferences)
        self.assertEqual(preferences.governor_id, 'empty')
        print("✅ Error handling test passed: graceful degradation with empty traits")

class TestTraitMapper(unittest.TestCase):
    """Test the TraitMapper component"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mapper = TraitMapper()
        
    def test_mapper_initialization(self):
        """Test mapper initializes with correct mappings"""
        self.assertIsNotNone(self.mapper)
        self.assertGreater(len(self.mapper.mappings_registry), 0)
        
        # Check for core trait mappings
        core_traits = ['patient', 'cryptic', 'scholarly', 'mystical', 'formal']
        for trait in core_traits:
            self.assertIn(trait, self.mapper.mappings_registry)
        print(f"✅ TraitMapper initialization test passed: {len(self.mapper.mappings_registry)} mappings")
    
    def test_trait_mapping_retrieval(self):
        """Test individual trait mapping retrieval"""
        patient_mapping = self.mapper.get_trait_mapping('patient')
        self.assertIsNotNone(patient_mapping)
        if patient_mapping:
            self.assertIsInstance(patient_mapping, TraitBehaviorMapping)
            self.assertEqual(patient_mapping.trait_name, 'patient')
            print(f"✅ Trait mapping retrieval test passed: {patient_mapping.trait_name}")
        else:
            print("✅ Trait mapping retrieval test passed: mapping not found (acceptable)")
    
    def test_multiple_trait_mappings(self):
        """Test retrieving mappings for multiple traits"""
        traits = ['patient', 'scholarly', 'mystical']
        mappings = self.mapper.get_all_mappings_for_traits(traits)
        
        self.assertIsInstance(mappings, dict)
        self.assertGreaterEqual(len(mappings), 0)
        
        # Check that we got mappings for the traits that exist
        for trait in traits:
            if trait in self.mapper.mappings_registry:
                self.assertIn(trait, mappings)
        
        print(f"✅ Multiple trait mappings test passed: {len(mappings)} mappings retrieved")
    
    def test_mapping_summary(self):
        """Test mapping summary generation"""
        summary = self.mapper.get_mapping_summary()
        
        self.assertIsInstance(summary, dict)
        self.assertIn('total_mappings', summary)
        self.assertIn('behavior_types', summary)
        self.assertIn('parameter_coverage', summary)
        
        self.assertGreater(summary['total_mappings'], 0)
        print(f"✅ Mapping summary test passed: {summary['total_mappings']} total mappings")

class TestResponseSelector(unittest.TestCase):
    """Test the ResponseSelector component"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.selector = ResponseSelector()
        self.sample_preferences = GovernorPreferences(
            governor_id='test_selector',
            tone_preference=TonePreference.SCHOLARLY_PATIENT,
            interaction_style='riddle_keeper',
            greeting_formality=0.8,
            puzzle_difficulty=PuzzleDifficulty.MODERATE,
            response_patience=0.7,
            metaphor_tolerance=0.6,
            reputation_sensitivity=0.5,
            trigger_words=['wisdom', 'knowledge', 'learning'],
            forbidden_words=['whatever', 'dude', 'chill']
        )
        
    def test_selector_initialization(self):
        """Test selector initializes correctly"""
        self.assertIsNotNone(self.selector)
        self.assertIsInstance(self.selector.tone_modifiers, dict)
        self.assertGreater(len(self.selector.tone_modifiers), 0)
        print("✅ ResponseSelector initialization test passed")
    
    def test_response_filtering(self):
        """Test response filtering based on preferences"""
        response_variants = [
            'Indeed, seeker, your wisdom grows through patient study.',
            'Yeah, whatever, here\'s your answer dude.',
            'The ancient knowledge reveals itself to those who seek.'
        ]
        
        filtered_responses = self.selector.filter_inappropriate_responses(
            response_variants, 
            self.sample_preferences
        )
        
        self.assertIsInstance(filtered_responses, list)
        self.assertGreater(len(filtered_responses), 0)
        
        # Check that casual response with forbidden words is filtered out
        casual_response = 'Yeah, whatever, here\'s your answer dude.'
        self.assertNotIn(casual_response, filtered_responses)
        
        print(f"✅ Response filtering test passed: {len(filtered_responses)} responses remain")
    
    def test_response_selection(self):
        """Test complete response selection process"""
        response_variants = [
            'Indeed, seeker, your wisdom grows through patient study.',
            'Yeah, whatever, here\'s your answer dude.',
            'The ancient knowledge reveals itself to those who seek.'
        ]
        
        context = {'base_reputation': 1, 'player_input': 'I seek wisdom about the sacred mysteries.'}
        
        selected_response = self.selector.select_response_variant(
            response_variants, 
            self.sample_preferences, 
            context
        )
        
        self.assertIsInstance(selected_response, str)
        self.assertGreater(len(selected_response), 0)
        
        # Should not select the casual response
        self.assertNotIn('whatever', selected_response)
        self.assertNotIn('dude', selected_response)
        
        print(f"✅ Response selection test passed: '{selected_response[:50]}...'")
    
    def test_tone_modifications(self):
        """Test tone-based response modification"""
        base_response = "The answer is revealed."
        modified_response = self.selector.apply_tone_modifications(
            base_response, 
            TonePreference.MYSTICAL_POETIC
        )
        
        self.assertIsInstance(modified_response, str)
        self.assertGreater(len(modified_response), 0)
        print(f"✅ Tone modification test passed: '{base_response}' → '{modified_response}'")

if __name__ == '__main__':
    print("🚀 Governor Preferences System - Comprehensive Test Suite")
    print("=" * 60)
    
    # Run tests with detailed output
    unittest.main(verbosity=2) 
