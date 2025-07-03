#!/usr/bin/env python3
"""
Integration Test Suite
Tests how storyline engine components work together
"""

import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

def test_simple_generator_integration():
    """Test simple generator integration"""
    print("🧪 Testing Simple Generator Integration...")
    
    try:
        from simple_generator import SimpleStorylineGenerator
        
        generator = SimpleStorylineGenerator()
        governors = generator.list_governors()
        
        if not governors:
            print("❌ No governors found")
            return False
        
        # Test single generation
        test_gov = governors[0]
        success = generator.generate_single(test_gov)
        
        if not success:
            print(f"❌ Failed to generate storyline for {test_gov}")
            return False
        
        # Verify output file exists and is valid
        output_file = generator.output_path / f"{test_gov}_storyline.json"
        if not output_file.exists():
            print(f"❌ Output file not created: {output_file}")
            return False
        
        # Load and validate JSON structure
        with open(output_file, 'r') as f:
            storyline = json.load(f)
        
        required_keys = ["governor_id", "version", "persona", "story_tree", "voidmaker_integration"]
        for key in required_keys:
            if key not in storyline:
                print(f"❌ Missing required key: {key}")
                return False
        
        nodes = storyline["story_tree"]["nodes"]
        print(f"✅ Simple generator integration validated:")
        print(f"   Generated: {storyline['generator']}")
        print(f"   Nodes: {len(nodes)}")
        print(f"   Governor: {storyline['governor_id']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple generator integration test failed: {e}")
        return False

def test_enhanced_generator_integration():
    """Test enhanced generator V2 integration"""
    print("\n🧪 Testing Enhanced Generator V2 Integration...")
    
    try:
        from enhanced_generator_v2 import EnhancedGeneratorV2
        
        generator = EnhancedGeneratorV2()
        
        # Find a test governor
        governor_files = list(generator.governor_path.glob("*.json"))
        if not governor_files:
            print("❌ No governor files found")
            return False
        
        test_gov = governor_files[0].stem
        success = generator.generate_enhanced_single(test_gov)
        
        if not success:
            print(f"❌ Failed to generate enhanced storyline for {test_gov}")
            return False
        
        # Verify enhanced output
        output_file = generator.output_path / f"{test_gov}_enhanced_v2.json"
        if not output_file.exists():
            print(f"❌ Enhanced output file not created: {output_file}")
            return False
        
        # Load and validate enhanced structure
        with open(output_file, 'r') as f:
            storyline = json.load(f)
        
        # Check enhanced features
        enhanced_keys = ["metadata", "persona", "story_tree", "voidmaker_integration", "utilities"]
        for key in enhanced_keys:
            if key not in storyline:
                print(f"❌ Missing enhanced key: {key}")
                return False
        
        # Validate enhanced metadata
        metadata = storyline["metadata"]
        if "element_confidence" not in metadata:
            print("❌ Missing element_confidence in metadata")
            return False
        
        # Validate enhanced persona
        persona = storyline["persona"]
        if not isinstance(persona["traits"], list) or len(persona["traits"]) == 0:
            print("❌ Invalid or empty traits in persona")
            return False
        
        # Validate story tree complexity
        nodes = storyline["story_tree"]["nodes"]
        if len(nodes) < 8:
            print(f"❌ Expected >=8 nodes, got {len(nodes)}")
            return False
        
        print(f"✅ Enhanced generator integration validated:")
        print(f"   Generator: {storyline['generator']}")
        print(f"   Version: {storyline['version']}")
        print(f"   Nodes: {len(nodes)}")
        print(f"   Element: {metadata['primary_element']} ({metadata['element_confidence']:.2f})")
        print(f"   Traits: {len(persona['traits'])}")
        print(f"   Traditions: {metadata['tradition_count']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced generator integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_flow_integration():
    """Test data flow between components"""
    print("\n🧪 Testing Data Flow Integration...")
    
    try:
        from core_loader import CoreDataLoader
        from enhanced_element_detector import EnhancedElementDetector
        from enhanced_story_builder import EnhancedStoryBuilder
        
        # Load governor data
        loader = CoreDataLoader()
        governors = loader.list_available_governors()
        
        if not governors:
            print("❌ No governors for data flow test")
            return False
        
        test_gov = governors[0]
        profile = loader.load_enhanced_governor(test_gov)
        
        if not profile:
            print(f"❌ Failed to load governor: {test_gov}")
            return False
        
        # Convert to raw data for element detector
        gov_data = {
            "governor_name": profile.governor_name,
            "blocks": profile.blocks,
            "knowledge_base_selections": {
                "chosen_traditions": profile.knowledge_base_selections.chosen_traditions
            }
        }
        
        # Test element detection
        detector = EnhancedElementDetector()
        element, confidence = detector.detect_element(gov_data)
        
        # Create info structure for story builder
        info = {
            "name": profile.governor_name,
            "element": element,
            "traditions": profile.knowledge_base_selections.chosen_traditions
        }
        
        # Test story building
        builder = EnhancedStoryBuilder()
        story_tree = builder.build_enhanced_story_tree(info)
        
        # Validate data flow
        if not story_tree or "nodes" not in story_tree:
            print("❌ Story tree generation failed")
            return False
        
        nodes = story_tree["nodes"]
        if len(nodes) < 8:
            print(f"❌ Insufficient nodes generated: {len(nodes)}")
            return False
        
        print(f"✅ Data flow integration validated:")
        print(f"   Governor: {profile.governor_name}")
        print(f"   Element: {element} (confidence: {confidence:.2f})")
        print(f"   Traditions: {len(info['traditions'])}")
        print(f"   Story nodes: {len(nodes)}")
        print(f"   Start node: {story_tree['start_node']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data flow integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_quality_consistency():
    """Test quality consistency across multiple governors"""
    print("\n🧪 Testing Quality Consistency...")
    
    try:
        from enhanced_generator_v2 import EnhancedGeneratorV2
        
        generator = EnhancedGeneratorV2()
        
        # Test with multiple governors
        governor_files = list(generator.governor_path.glob("*.json"))
        test_governors = [f.stem for f in governor_files[:3]]  # Test first 3
        
        results = []
        
        for gov_name in test_governors:
            print(f"   Testing {gov_name}...")
            
            storyline = generator.create_enhanced_storyline(gov_name)
            if not storyline:
                print(f"   ❌ Failed to create storyline for {gov_name}")
                continue
            
            # Analyze quality metrics
            nodes = len(storyline["story_tree"]["nodes"])
            traits = len(storyline["persona"]["traits"])
            traditions = storyline["metadata"]["tradition_count"]
            element = storyline["metadata"]["primary_element"]
            confidence = storyline["metadata"]["element_confidence"]
            
            quality_score = 0
            if nodes >= 8: quality_score += 25
            if traits >= 2: quality_score += 25
            if traditions >= 2: quality_score += 25
            if element != "unknown": quality_score += 25
            
            result = {
                "governor": gov_name,
                "nodes": nodes,
                "traits": traits,
                "traditions": traditions,
                "element": element,
                "confidence": confidence,
                "quality_score": quality_score
            }
            
            results.append(result)
            print(f"   ✅ {gov_name}: Quality {quality_score}/100")
        
        if not results:
            print("❌ No successful generations for quality test")
            return False
        
        # Analyze consistency
        avg_nodes = sum(r["nodes"] for r in results) / len(results)
        avg_traits = sum(r["traits"] for r in results) / len(results)
        avg_quality = sum(r["quality_score"] for r in results) / len(results)
        
        print(f"✅ Quality consistency validated:")
        print(f"   Tested: {len(results)} governors")
        print(f"   Avg nodes: {avg_nodes:.1f}")
        print(f"   Avg traits: {avg_traits:.1f}")
        print(f"   Avg quality: {avg_quality:.1f}/100")
        
        # Consistency check: all should have >= 8 nodes and >= 75% quality
        consistent_quality = all(r["quality_score"] >= 75 for r in results)
        consistent_nodes = all(r["nodes"] >= 8 for r in results)
        
        if consistent_quality and consistent_nodes:
            print("✅ Quality consistency PASSED")
            return True
        else:
            print("❌ Quality consistency issues detected")
            for r in results:
                if r["quality_score"] < 75 or r["nodes"] < 8:
                    print(f"   ⚠️ {r['governor']}: {r['quality_score']}/100, {r['nodes']} nodes")
            return False
        
    except Exception as e:
        print(f"❌ Quality consistency test failed: {e}")
        return False

def run_integration_tests():
    """Run all integration tests"""
    print("🚀 Starting Integration Tests...\n")
    
    tests = [
        ("Simple Generator Integration", test_simple_generator_integration),
        ("Enhanced Generator Integration", test_enhanced_generator_integration),
        ("Data Flow Integration", test_data_flow_integration),
        ("Quality Consistency", test_quality_consistency)
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
    
    print(f"\n📊 Integration Test Results:")
    print(f"   Passed: {results['passed']}")
    print(f"   Failed: {results['failed']}")
    print(f"   Total: {results['passed'] + results['failed']}")
    
    if results["failed"] == 0:
        print("🎉 All integration tests PASSED!")
        return True
    else:
        print("❌ Some integration tests FAILED!")
        return False

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1) 