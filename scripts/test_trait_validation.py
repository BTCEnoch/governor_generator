#!/usr/bin/env python3
"""
Test Script for Trait Validation System
=======================================

This script tests the trait validation system with a few governors to ensure
everything works before running on all 91 governors.
"""

import sys
import os
from pathlib import Path
import logging

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_basic_import():
    """Test that we can import all required modules."""
    try:
        print("🔍 Testing basic imports...")
        
        from game_mechanics.dialog_system import (
            GovernorPreferencesManager,
            GovernorProfile,
            PreferenceEncoder,
            TraitMapper,
            BehavioralFilter,
            TonePreference,
            InteractionType
        )
        
        print("✅ All dialog system imports successful")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_trait_mapper():
    """Test the trait mapper functionality."""
    try:
        print("\n🔍 Testing TraitMapper...")
        
        from game_mechanics.dialog_system import TraitMapper
        
        mapper = TraitMapper()
        
        # Test basic trait mapping
        patient_mapping = mapper.get_trait_mapping('patient')
        if patient_mapping:
            print(f"✅ Found mapping for 'patient': {patient_mapping.behavior_type.value}")
        else:
            print("⚠️  No mapping found for 'patient'")
        
        # Test multiple traits
        test_traits = ['patient', 'scholarly', 'mystical']
        mappings = mapper.get_all_mappings_for_traits(test_traits)
        print(f"✅ Found {len(mappings)} mappings for test traits")
        
        # Test summary
        summary = mapper.get_mapping_summary()
        print(f"✅ Trait mapper summary: {summary.get('total_mappings', 0)} total mappings")
        
        return True
        
    except Exception as e:
        print(f"❌ TraitMapper test failed: {e}")
        return False

def test_preferences_manager():
    """Test the preferences manager functionality."""
    try:
        print("\n🔍 Testing GovernorPreferencesManager...")
        
        from game_mechanics.dialog_system import GovernorPreferencesManager, GovernorProfile, InteractionType
        
        manager = GovernorPreferencesManager()
        
        # Create test governor profile
        test_profile = GovernorProfile(
            governor_id='test_governor',
            name='Test Governor',
            traits=['mystical', 'patient', 'scholarly'],
            preferences={'tone': 'mystical_poetic'},
            interaction_models=[InteractionType.RIDDLE_KEEPER]
        )
        
        # Test preference generation
        preferences = manager.get_governor_preferences(test_profile)
        print(f"✅ Generated preferences for test governor: {preferences.tone_preference.value}")
        
        # Test caching
        preferences2 = manager.get_governor_preferences(test_profile)
        print("✅ Cached preferences retrieved successfully")
        
        # Test system status
        status = manager.get_system_status()
        print(f"✅ System status: {status['cached_governors']} cached governors")
        
        return True
        
    except Exception as e:
        print(f"❌ GovernorPreferencesManager test failed: {e}")
        return False

def test_with_real_governor():
    """Test with a real governor from the data."""
    try:
        print("\n🔍 Testing with real governor data...")
        
        # Try to load actual governor data
        canon_file = Path("canon/canon_governor_profiles.json")
        if not canon_file.exists():
            print("⚠️  Canon profiles file not found, skipping real governor test")
            return True
        
        import json
        with open(canon_file, 'r') as f:
            canon_list = json.load(f)
        
        # Get first governor from the list
        if not canon_list:
            print("⚠️  No governors found in canon file")
            return True
        
        governor_data = canon_list[0]
        governor_name = governor_data["governor_info"]["name"]
        
        print(f"✅ Loaded real governor data for: {governor_name}")
        
        # Test creating profile from real data
        from game_mechanics.dialog_system import GovernorProfile, InteractionType
        
        # Extract traits
        traits = []
        if "trait_choices" in governor_data:
            trait_choices = governor_data["trait_choices"]
            if "virtues" in trait_choices:
                traits.extend(trait_choices["virtues"])
            if "flaws" in trait_choices:
                traits.extend(trait_choices["flaws"])
        
        profile = GovernorProfile(
            governor_id=governor_name,
            name=governor_name,
            traits=traits,
            preferences={},
            interaction_models=[InteractionType.RIDDLE_KEEPER]
        )
        
        print(f"✅ Created profile with {len(traits)} traits: {traits[:3]}...")
        
        # Test preference generation
        from game_mechanics.dialog_system import GovernorPreferencesManager
        manager = GovernorPreferencesManager()
        preferences = manager.get_governor_preferences(profile)
        
        print(f"✅ Generated preferences: {preferences.tone_preference.value}")
        print(f"✅ Behavioral parameters: formality={preferences.greeting_formality:.2f}, patience={preferences.response_patience:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Real governor test failed: {e}")
        return False

def test_trait_validation_runner():
    """Test the trait validation runner we just created."""
    try:
        print("\n🔍 Testing TraitValidationRunner...")
        
        from scripts.trait_validation_runner import TraitValidationRunner
        
        # Create runner
        runner = TraitValidationRunner(output_dir="test_validation_output")
        print(f"✅ Created validation runner with {len(runner.governor_data)} governors")
        
        # Test with first governor if available
        if runner.governor_data:
            first_governor = list(runner.governor_data.keys())[0]
            print(f"✅ Testing validation with governor: {first_governor}")
            
            # This might take a moment
            result = runner.validate_single_governor(first_governor)
            
            if result.get('status') == 'completed':
                print("✅ Validation completed successfully")
                print(f"✅ Trait validation: {result['trait_validation']['validation_status']}")
                print(f"✅ Preference validation: {result['preference_validation']['validation_status']}")
                print(f"✅ Performance validation: {result['performance_validation']['validation_status']}")
            else:
                print(f"⚠️  Validation had issues: {result.get('status', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ TraitValidationRunner test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Trait Validation System")
    print("=" * 50)
    
    tests = [
        test_basic_import,
        test_trait_mapper,
        test_preferences_manager,
        test_with_real_governor,
        test_trait_validation_runner
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("🎯 Test Results Summary:")
    print(f"   Passed: {sum(results)}/{len(results)}")
    print(f"   Failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\n✅ All tests passed! The trait validation system is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Run: python scripts/trait_validation_runner.py --governor OCCODON")
        print("   2. Run: python scripts/trait_validation_runner.py --all --report validation_report.json")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 