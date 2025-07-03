#!/usr/bin/env python3
"""
Component Validation Test Suite
Tests each storyline engine component individually
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

def test_core_loader():
    """Test core data loader component"""
    print("🧪 Testing Core Data Loader...")
    
    try:
        from core_loader import CoreDataLoader
        
        loader = CoreDataLoader()
        governors = loader.list_available_governors()
        
        if not governors:
            print("❌ No governors found")
            return False
        
        print(f"✅ Found {len(governors)} governors")
        
        # Test loading first governor
        test_gov = governors[0]
        profile = loader.load_enhanced_governor(test_gov)
        
        if not profile:
            print(f"❌ Failed to load {test_gov}")
            return False
        
        print(f"✅ Loaded {profile.governor_name}")
        print(f"   Traditions: {len(profile.knowledge_base_selections.chosen_traditions)}")
        print(f"   Voidmaker blocks: {len(profile.voidmaker_expansion)}")
        
        # Test validation
        validation = loader.validate_governor_completeness(test_gov)
        if not validation.get("is_complete", False):
            print(f"❌ Governor validation failed: {validation}")
            return False
        
        print("✅ Core loader validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Core loader test failed: {e}")
        return False

def test_canonical_loader():
    """Test canonical elements loader"""
    print("\n🧪 Testing Canonical Loader...")
    
    try:
        from canonical_loader import CanonicalLoader
        
        loader = CanonicalLoader()
        
        # Test each canonical file
        watchtowers = loader.load_watchtowers()
        aethyrs = loader.load_aethyrs()
        alphabet = loader.load_enochian_alphabet()
        
        print(f"✅ Loaded canonical elements:")
        print(f"   Watchtowers: {len(watchtowers)} entries")
        print(f"   Aethyrs: {len(aethyrs)} entries")
        print(f"   Alphabet: {len(alphabet)} entries")
        
        return True
        
    except Exception as e:
        print(f"❌ Canonical loader test failed: {e}")
        return False

def test_element_detector():
    """Test enhanced element detector"""
    print("\n🧪 Testing Element Detector...")
    
    try:
        from enhanced_element_detector import EnhancedElementDetector
        
        detector = EnhancedElementDetector()
        
        # Test with sample fire-themed data
        test_data = {
            "blocks": {
                "B_elemental_essence": {
                    "6": "Flames of passion burn within my solar essence, igniting courage and determination"
                },
                "C_personality": {
                    "11": "Fierce will, blazing courage, fiery determination"
                }
            }
        }
        
        element, confidence = detector.detect_element(test_data)
        description = detector.get_element_description(element)
        
        print(f"✅ Element detection working:")
        print(f"   Element: {element} (confidence: {confidence:.2f})")
        print(f"   Description: {description}")
        
        # Should detect fire with high confidence
        if element == "fire" and confidence > 0.5:
            print("✅ Fire detection validated")
            return True
        else:
            print(f"❌ Expected fire element with high confidence, got {element} ({confidence})")
            return False
        
    except Exception as e:
        print(f"❌ Element detector test failed: {e}")
        return False

def test_story_builder():
    """Test enhanced story builder"""
    print("\n🧪 Testing Story Builder...")
    
    try:
        from enhanced_story_builder import EnhancedStoryBuilder
        
        builder = EnhancedStoryBuilder()
        
        # Test story tree creation
        test_info = {
            "name": "TEST_GOVERNOR",
            "element": "fire",
            "traditions": ["Hermetic Tradition", "Kabbalah", "Sacred Geometry"]
        }
        
        story_tree = builder.build_enhanced_story_tree(test_info)
        
        nodes = story_tree.get("nodes", {})
        start_node = story_tree.get("start_node", "")
        
        print(f"✅ Story tree created:")
        print(f"   Nodes: {len(nodes)}")
        print(f"   Start node: {start_node}")
        
        # Validate minimum node count and structure
        if len(nodes) >= 8 and start_node == "introduction":
            print("✅ Story structure validated")
            
            # Check if introduction node exists and has choices
            intro_node = nodes.get("introduction", {})
            if intro_node.get("choices") and len(intro_node["choices"]) >= 2:
                print("✅ Introduction node validated")
                return True
            else:
                print("❌ Introduction node missing or invalid")
                return False
        else:
            print(f"❌ Expected >=8 nodes with 'introduction' start, got {len(nodes)} nodes, start: {start_node}")
            return False
        
    except Exception as e:
        print(f"❌ Story builder test failed: {e}")
        return False

def run_component_tests():
    """Run all component tests"""
    print("🚀 Starting Component Validation Tests...\n")
    
    tests = [
        ("Core Loader", test_core_loader),
        ("Canonical Loader", test_canonical_loader),
        ("Element Detector", test_element_detector),
        ("Story Builder", test_story_builder)
    ]
    
    results = {"passed": 0, "failed": 0}
    
    for test_name, test_func in tests:
        try:
            if test_func():
                results["passed"] += 1
                print(f"✅ {test_name} PASSED")
            else:
                results["failed"] += 1
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            results["failed"] += 1
            print(f"❌ {test_name} ERROR: {e}")
        
        print("-" * 50)
    
    print(f"\n📊 Component Test Results:")
    print(f"   Passed: {results['passed']}")
    print(f"   Failed: {results['failed']}")
    print(f"   Total: {results['passed'] + results['failed']}")
    
    if results["failed"] == 0:
        print("🎉 All component tests PASSED!")
        return True
    else:
        print("❌ Some component tests FAILED!")
        return False

if __name__ == "__main__":
    success = run_component_tests()
    sys.exit(0 if success else 1) 