#!/usr/bin/env python3
"""
Full Pipeline Test Suite
Tests complete end-to-end storyline generation workflow
"""

import sys
import json
import time
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

def test_batch_generation_pipeline():
    """Test batch generation pipeline"""
    print("🧪 Testing Batch Generation Pipeline...")
    
    try:
        from enhanced_generator_v2 import EnhancedGeneratorV2
        
        generator = EnhancedGeneratorV2()
        
        # Test batch generation with small sample
        governor_files = list(generator.governor_path.glob("*.json"))
        test_batch = [f.stem for f in governor_files[:5]]  # Test 5 governors
        
        print(f"   Testing batch of {len(test_batch)} governors...")
        
        start_time = time.time()
        successful_generations = 0
        
        for i, gov_name in enumerate(test_batch):
            print(f"   [{i+1}/{len(test_batch)}] Generating {gov_name}...")
            
            success = generator.generate_enhanced_single(gov_name)
            if success:
                successful_generations += 1
            else:
                print(f"   ❌ Failed: {gov_name}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Validate results
        success_rate = successful_generations / len(test_batch)
        avg_time_per_governor = duration / len(test_batch)
        
        print(f"✅ Batch generation completed:")
        print(f"   Total: {len(test_batch)} governors")
        print(f"   Successful: {successful_generations}")
        print(f"   Success rate: {success_rate:.2%}")
        print(f"   Total time: {duration:.2f}s")
        print(f"   Avg time per governor: {avg_time_per_governor:.2f}s")
        
        # Pipeline should have high success rate and reasonable performance
        if success_rate >= 0.8 and avg_time_per_governor < 5.0:
            print("✅ Batch pipeline performance validated")
            return True
        else:
            print(f"❌ Pipeline performance issues: {success_rate:.2%} success, {avg_time_per_governor:.2f}s avg")
            return False
        
    except Exception as e:
        print(f"❌ Batch generation pipeline test failed: {e}")
        return False

def test_output_quality_pipeline():
    """Test output quality across pipeline"""
    print("\n🧪 Testing Output Quality Pipeline...")
    
    try:
        from enhanced_generator_v2 import EnhancedGeneratorV2
        
        generator = EnhancedGeneratorV2()
        
        # Load existing outputs for quality analysis
        output_files = list(generator.output_path.glob("*_enhanced_v2.json"))
        
        if len(output_files) < 3:
            print("❌ Insufficient output files for quality test")
            return False
        
        print(f"   Analyzing {len(output_files)} generated storylines...")
        
        quality_metrics = {
            "total_files": len(output_files),
            "valid_json": 0,
            "complete_structure": 0,
            "rich_content": 0,
            "element_detected": 0,
            "tradition_integration": 0
        }
        
        detailed_results = []
        
        for output_file in output_files[:10]:  # Analyze first 10
            gov_name = output_file.stem.replace("_enhanced_v2", "")
            
            try:
                # Load and validate JSON
                with open(output_file, 'r', encoding='utf-8') as f:
                    storyline = json.load(f)
                
                quality_metrics["valid_json"] += 1
                
                # Check structure completeness
                required_sections = ["metadata", "persona", "story_tree", "voidmaker_integration"]
                if all(section in storyline for section in required_sections):
                    quality_metrics["complete_structure"] += 1
                
                # Check content richness
                nodes = len(storyline.get("story_tree", {}).get("nodes", {}))
                traits = len(storyline.get("persona", {}).get("traits", []))
                
                if nodes >= 8 and traits >= 2:
                    quality_metrics["rich_content"] += 1
                
                # Check element detection
                element = storyline.get("metadata", {}).get("primary_element", "unknown")
                if element != "unknown":
                    quality_metrics["element_detected"] += 1
                
                # Check tradition integration
                traditions = storyline.get("metadata", {}).get("tradition_count", 0)
                if traditions >= 2:
                    quality_metrics["tradition_integration"] += 1
                
                detailed_results.append({
                    "governor": gov_name,
                    "nodes": nodes,
                    "traits": traits,
                    "element": element,
                    "traditions": traditions,
                    "quality": "high" if nodes >= 8 and traits >= 2 and traditions >= 2 else "medium"
                })
                
            except Exception as e:
                print(f"   ⚠️ Error analyzing {gov_name}: {e}")
                continue
        
        # Calculate quality percentages
        analyzed_count = quality_metrics["valid_json"]
        if analyzed_count == 0:
            print("❌ No valid files to analyze")
            return False
        
        structure_rate = quality_metrics["complete_structure"] / analyzed_count
        content_rate = quality_metrics["rich_content"] / analyzed_count
        element_rate = quality_metrics["element_detected"] / analyzed_count
        tradition_rate = quality_metrics["tradition_integration"] / analyzed_count
        
        print(f"✅ Quality analysis completed:")
        print(f"   Valid JSON: {quality_metrics['valid_json']}/{analyzed_count} (100%)")
        print(f"   Complete structure: {structure_rate:.2%}")
        print(f"   Rich content: {content_rate:.2%}")
        print(f"   Element detected: {element_rate:.2%}")
        print(f"   Tradition integration: {tradition_rate:.2%}")
        
        # Show sample results
        print(f"\n   Sample results:")
        for result in detailed_results[:3]:
            print(f"   {result['governor']}: {result['nodes']} nodes, {result['traits']} traits, "
                  f"{result['element']} element, {result['traditions']} traditions ({result['quality']})")
        
        # Quality thresholds
        high_quality_threshold = 0.8
        if (structure_rate >= high_quality_threshold and 
            content_rate >= high_quality_threshold and
            tradition_rate >= high_quality_threshold):
            print("✅ Output quality pipeline validated")
            return True
        else:
            print("❌ Output quality below thresholds")
            return False
        
    except Exception as e:
        print(f"❌ Output quality pipeline test failed: {e}")
        return False

def test_data_integrity_pipeline():
    """Test data integrity throughout pipeline"""
    print("\n🧪 Testing Data Integrity Pipeline...")
    
    try:
        from core_loader import CoreDataLoader
        from enhanced_generator_v2 import EnhancedGeneratorV2
        
        # Load original governor data
        loader = CoreDataLoader()
        generator = EnhancedGeneratorV2()
        
        governors = loader.list_available_governors()
        test_gov = governors[0]
        
        print(f"   Testing data integrity for {test_gov}...")
        
        # Load original profile
        original_profile = loader.load_enhanced_governor(test_gov)
        
        # Generate storyline
        storyline = generator.create_enhanced_storyline(test_gov)
        
        if not storyline:
            print(f"❌ Failed to generate storyline for integrity test")
            return False
        
        # Verify data integrity
        metadata = storyline["metadata"]
        
        # Check governor name preservation
        if metadata["governor_name"] != original_profile.governor_name:
            print(f"❌ Governor name mismatch: {metadata['governor_name']} vs {original_profile.governor_name}")
            return False
        
        # Check governor number preservation
        if metadata["governor_number"] != original_profile.governor_number:
            print(f"❌ Governor number mismatch: {metadata['governor_number']} vs {original_profile.governor_number}")
            return False
        
        # Check traditions preservation
        original_traditions = set(original_profile.knowledge_base_selections.chosen_traditions)
        storyline_traditions = set(metadata["selected_traditions"])
        
        if original_traditions != storyline_traditions:
            print(f"❌ Traditions mismatch:")
            print(f"   Original: {original_traditions}")
            print(f"   Storyline: {storyline_traditions}")
            return False
        
        # Check tradition count consistency
        if metadata["tradition_count"] != len(original_traditions):
            print(f"❌ Tradition count mismatch: {metadata['tradition_count']} vs {len(original_traditions)}")
            return False
        
        print(f"✅ Data integrity validated:")
        print(f"   Governor: {metadata['governor_name']} (#{metadata['governor_number']})")
        print(f"   Traditions: {metadata['tradition_count']} preserved")
        print(f"   Element: {metadata['primary_element']} (confidence: {metadata['element_confidence']:.2f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Data integrity pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scalability_pipeline():
    """Test pipeline scalability"""
    print("\n🧪 Testing Scalability Pipeline...")
    
    try:
        from enhanced_generator_v2 import EnhancedGeneratorV2
        
        generator = EnhancedGeneratorV2()
        
        # Test memory usage and performance with larger batch
        governor_files = list(generator.governor_path.glob("*.json"))
        total_governors = len(governor_files)
        
        print(f"   Total governors available: {total_governors}")
        
        # Estimate full generation time based on sample
        sample_size = min(3, total_governors)
        sample_governors = [f.stem for f in governor_files[:sample_size]]
        
        print(f"   Testing scalability with {sample_size} governor sample...")
        
        start_time = time.time()
        
        for gov_name in sample_governors:
            storyline = generator.create_enhanced_storyline(gov_name)
            if not storyline:
                print(f"   ❌ Failed to generate {gov_name}")
                return False
        
        sample_time = time.time() - start_time
        avg_time_per_governor = sample_time / sample_size
        
        # Estimate full batch time
        estimated_full_time = avg_time_per_governor * total_governors
        estimated_minutes = estimated_full_time / 60
        
        print(f"✅ Scalability analysis:")
        print(f"   Sample time: {sample_time:.2f}s for {sample_size} governors")
        print(f"   Avg per governor: {avg_time_per_governor:.2f}s")
        print(f"   Estimated full batch: {estimated_minutes:.1f} minutes for {total_governors} governors")
        
        # Scalability thresholds
        if avg_time_per_governor < 3.0 and estimated_minutes < 30:
            print("✅ Scalability pipeline validated")
            return True
        else:
            print(f"❌ Scalability concerns: {avg_time_per_governor:.2f}s per governor, {estimated_minutes:.1f}min total")
            return False
        
    except Exception as e:
        print(f"❌ Scalability pipeline test failed: {e}")
        return False

def run_pipeline_tests():
    """Run all pipeline tests"""
    print("🚀 Starting Full Pipeline Tests...\n")
    
    tests = [
        ("Batch Generation Pipeline", test_batch_generation_pipeline),
        ("Output Quality Pipeline", test_output_quality_pipeline),
        ("Data Integrity Pipeline", test_data_integrity_pipeline),
        ("Scalability Pipeline", test_scalability_pipeline)
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
    
    print(f"\n📊 Pipeline Test Results:")
    print(f"   Passed: {results['passed']}")
    print(f"   Failed: {results['failed']}")
    print(f"   Total: {results['passed'] + results['failed']}")
    
    if results["failed"] == 0:
        print("🎉 All pipeline tests PASSED!")
        print("\n🏆 SYSTEM READY FOR PRODUCTION!")
        return True
    else:
        print("❌ Some pipeline tests FAILED!")
        return False

if __name__ == "__main__":
    success = run_pipeline_tests()
    sys.exit(0 if success else 1) 