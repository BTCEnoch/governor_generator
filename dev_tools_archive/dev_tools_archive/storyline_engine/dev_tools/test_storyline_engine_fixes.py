#!/usr/bin/env python3
"""
Test Storyline Engine Fixes
Comprehensive testing of the parsing issue fixes and enhanced functionality
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path for imports
current_file_dir = Path(__file__).parent
sys.path.append(str(current_file_dir))

try:
    from core_loader import CoreDataLoader, EnhancedGovernorProfile
    from enhanced_generator_v2 import EnhancedGeneratorV2
    from enhanced_element_detector import EnhancedElementDetector
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_core_loader_fixes():
    """Test the core loader data structure fixes"""
    print("🧪 TESTING CORE LOADER FIXES")
    print("=" * 40)
    
    try:
        # Determine correct base path - if running from storyline_engine, go up one level
        current_dir = Path.cwd()
        if current_dir.name == "storyline_engine":
            base_path = current_dir.parent
        else:
            base_path = current_dir
        
        loader = CoreDataLoader(base_path=base_path)
        available_governors = loader.list_available_governors()
        
        if not available_governors:
            print("❌ No governors found for testing")
            return False
        
        # Test with an enhanced governor (preferably ZAXANIN if available)
        test_governor = "ZAXANIN" if "ZAXANIN" in available_governors else available_governors[0]
        print(f"📋 Testing with: {test_governor}")
        
        # Load governor
        profile = loader.load_enhanced_governor(test_governor)
        print(f"✅ Loaded governor profile successfully")
        
        # Validate structure
        assert isinstance(profile, EnhancedGovernorProfile)
        print(f"✅ Profile structure validation passed")
        
        # Test voidmaker expansion parsing
        if profile.voidmaker_expansion:
            print(f"📊 Voidmaker blocks: {len(profile.voidmaker_expansion)}")
            
            for block_name, block in profile.voidmaker_expansion.items():
                print(f"   {block_name}: {len(block.questions)} questions, {len(block.themes)} themes")
                
                # Verify question structure
                if block.questions:
                    sample_q = next(iter(block.questions.values()))
                    if isinstance(sample_q, dict):
                        assert "question" in sample_q and "answer" in sample_q
                        print(f"✅ Question structure validation passed for {block_name}")
                    else:
                        print(f"⚠️  Old format detected in {block_name}")
        
        # Test derived attributes
        print(f"🔍 Derived attributes:")
        print(f"   Element: {profile.elemental_nature}")
        print(f"   Aethyr: {profile.home_aethyr}")
        print(f"   Traditions: {profile.tradition_depth}")
        
        # Validate completeness
        validation = loader.validate_governor_completeness(test_governor)
        print(f"📋 Completeness validation: {validation}")
        
        print(f"✅ Core loader tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Core loader test failed: {e}")
        return False

def test_enhanced_generator_fixes():
    """Test the enhanced generator voidmaker integration"""
    print(f"\n🧪 TESTING ENHANCED GENERATOR FIXES")
    print("=" * 40)
    
    try:
        # Determine correct base path - if running from storyline_engine, go up one level
        current_dir = Path.cwd()
        if current_dir.name == "storyline_engine":
            base_path = current_dir.parent
        else:
            base_path = current_dir
        
        generator = EnhancedGeneratorV2(base_path=base_path)
        
        # Find an enhanced governor
        available_files = list(generator.governor_path.glob("*.json"))
        if not available_files:
            print("❌ No governor files found")
            return False
        
        test_file = available_files[0]
        test_governor = test_file.stem
        print(f"📋 Testing with: {test_governor}")
        
        # Load governor data
        gov_data = generator.load_governor_data(test_governor)
        if not gov_data:
            print(f"❌ Failed to load {test_governor}")
            return False
        
        print(f"✅ Loaded governor data")
        
        # Test enhanced info extraction
        info = generator.extract_enhanced_info(gov_data)
        print(f"📊 Enhanced info extracted:")
        print(f"   Name: {info['name']}")
        print(f"   Element: {info['element']} (confidence: {info['element_confidence']:.2f})")
        print(f"   Profile element: {info.get('profile_element', 'None')}")
        print(f"   Traditions: {len(info['traditions'])}")
        print(f"   Voidmaker questions: {info['voidmaker_question_count']}")
        print(f"   Voidmaker themes: {info['voidmaker_themes']}")
        
        # Test storyline creation
        storyline = generator.create_enhanced_storyline(test_governor)
        if not storyline:
            print(f"❌ Failed to create storyline")
            return False
        
        print(f"✅ Created enhanced storyline")
        
        # Validate voidmaker integration
        vm_integration = storyline.get("voidmaker_integration", {})
        if "statistics" in vm_integration:
            stats = vm_integration["statistics"]
            print(f"📊 Voidmaker integration stats:")
            print(f"   Total questions: {stats.get('total_questions', 0)}")
            print(f"   Enabled tiers: {stats.get('enabled_tiers', 0)}")
            print(f"   Primary themes: {stats.get('primary_themes', [])}")
        
        # Check for actual content
        for tier_name in ["cosmic_awareness", "reality_influence", "integration_unity"]:
            if tier_name in vm_integration:
                tier = vm_integration[tier_name]
                if tier.get("enabled"):
                    print(f"✅ {tier_name}: {len(tier.get('questions', []))} questions")
        
        print(f"✅ Enhanced generator tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced generator test failed: {e}")
        return False

def test_element_detector():
    """Test element detector functionality"""
    print(f"\n🧪 TESTING ELEMENT DETECTOR")
    print("=" * 40)
    
    try:
        detector = EnhancedElementDetector()
        
        # Test with sample data
        test_data = {
            "profile": {
                "element": "Earth"
            },
            "blocks": {
                "B_elemental_essence": {
                    "6": "The earth beneath my feet provides stability and grounding energy"
                }
            }
        }
        
        element, confidence = detector.detect_element(test_data)
        description = detector.get_element_description(element)
        
        print(f"✅ Element detection working")
        print(f"   Detected: {element} (confidence: {confidence:.2f})")
        print(f"   Description: {description}")
        
        return True
        
    except Exception as e:
        print(f"❌ Element detector test failed: {e}")
        return False

def test_end_to_end_processing():
    """Test complete end-to-end storyline generation"""
    print(f"\n🧪 TESTING END-TO-END PROCESSING")
    print("=" * 40)
    
    try:
        # Determine correct base path - if running from storyline_engine, go up one level
        current_dir = Path.cwd()
        if current_dir.name == "storyline_engine":
            base_path = current_dir.parent
        else:
            base_path = current_dir
        
        generator = EnhancedGeneratorV2(base_path=base_path)
        
        # Find an enhanced governor for testing
        enhanced_governors = []
        for json_file in generator.governor_path.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if "voidmaker_expansion" in data and "knowledge_base_selections" in data:
                    enhanced_governors.append(json_file.stem)
            except:
                continue
        
        if not enhanced_governors:
            print("❌ No enhanced governors found for end-to-end test")
            return False
        
        test_governor = enhanced_governors[0]
        print(f"📋 Testing complete pipeline with: {test_governor}")
        
        # Generate storyline
        success = generator.generate_enhanced_single(test_governor)
        
        if success:
            # Verify output file exists
            output_file = generator.output_path / f"{test_governor}_enhanced_v2.json"
            if output_file.exists():
                with open(output_file, 'r', encoding='utf-8') as f:
                    storyline = json.load(f)
                    
                print(f"✅ End-to-end processing successful")
                print(f"📄 Output file: {output_file}")
                print(f"📊 Storyline metadata:")
                print(f"   Version: {storyline.get('version', 'unknown')}")
                print(f"   Generator: {storyline.get('generator', 'unknown')}")
                
                metadata = storyline.get("metadata", {})
                print(f"   Element: {metadata.get('primary_element', 'unknown')}")
                print(f"   Traditions: {metadata.get('tradition_count', 0)}")
                
                return True
            else:
                print(f"❌ Output file not created")
                return False
        else:
            print(f"❌ Generation failed")
            return False
        
    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 STORYLINE ENGINE FIX VALIDATION")
    print("=" * 50)
    
    tests = [
        ("Core Loader Fixes", test_core_loader_fixes),
        ("Enhanced Generator Fixes", test_enhanced_generator_fixes),
        ("Element Detector", test_element_detector),
        ("End-to-End Processing", test_end_to_end_processing)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print(f"🎯 TEST RESULTS SUMMARY")
    print(f"{'='*50}")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print(f"🎉 ALL TESTS PASSED - Storyline engine ready!")
        return True
    else:
        print(f"⚠️  Some tests failed - review issues above")
        return False

if __name__ == "__main__":
    main() 