#!/usr/bin/env python3
"""
Test Knowledge Extractor
Quick test to verify the system works before processing all batches
"""

import logging
import sys
from pathlib import Path
import json

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from archives.knowledge_extractor import KnowledgeExtractor

def test_single_tradition():
    """Test extraction with a single tradition"""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Initialize extractor with correct paths for running from archives directory
    extractor = KnowledgeExtractor(
        links_dir="../links",  # Go up to knowledge_base, then to links
        archive_dir="."        # Current directory (archives)
    )
    
    # Test with Thelema (it has good data structure)
    test_file = "research_thelema.json"
    print(f"🧪 Testing knowledge extraction with {test_file}")
    
    try:
        # Process single tradition
        archives = extractor.process_batch([test_file])
        
        if archives:
            archive = archives[0]
            print(f"\n✅ Successfully extracted knowledge for: {archive.display_name}")
            print(f"📊 Overview length: {len(archive.overview)} characters")
            print(f"🧠 Core concepts: {len(archive.core_concepts)}")
            print(f"🎭 Personality traits: {len(archive.personality_traits)}")
            print(f"💬 Interaction patterns: {len(archive.interaction_patterns)}")
            
            print(f"\n📝 Sample Overview:")
            print(f"   {archive.overview[:200]}...")
            
            print(f"\n🧠 Core Concepts:")
            for i, concept in enumerate(archive.core_concepts, 1):
                print(f"   {i}. {concept.name}")
                if concept.wiki_extract:
                    print(f"      📖 Wikipedia: ✅ (Found)")
                    print(f"      🔗 URL: {concept.wiki_url}")
                else:
                    print(f"      📖 Wikipedia: ❌ (Pattern-based)")
                print(f"      📋 Description: {concept.description[:100]}...")
                print()
            
            print(f"🎭 Personality Traits: {', '.join(archive.personality_traits)}")
            print(f"💬 Interaction Patterns:")
            for pattern in archive.interaction_patterns:
                print(f"   - {pattern}")
            
            return True
        else:
            print("❌ No archives were created")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def preview_batch_structure():
    """Preview what a full batch would look like"""
    print(f"\n{'='*50}")
    print("📋 BATCH PROCESSING PREVIEW")
    print(f"{'='*50}")
    
    batches = {
        "batch_1": ["research_celtic_druidic.json", "research_classical_philosophy.json", 
                   "research_egyptian_magic.json", "research_gnostic_traditions.json", 
                   "research_norse_traditions.json"],
        "batch_2": ["research_golden_dawn.json", "research_i_ching.json", 
                   "research_kuji_kiri.json", "research_sacred_geometry.json", 
                   "research_tarot_knowledge.json"],
        "batch_3": ["research_chaos_magic.json", "research_sufi_mysticism.json", 
                   "research_taoism.json", "research_thelema.json"]
    }
    
    total_files = 0
    for batch_name, files in batches.items():
        print(f"\n{batch_name.upper()}:")
        for file in files:
            tradition_name = file.replace('research_', '').replace('.json', '').replace('_', ' ').title()
            print(f"  📚 {tradition_name}")
        print(f"  📊 Total: {len(files)} traditions")
        total_files += len(files)
    
    print(f"\n🏛️ GRAND TOTAL: {total_files} mystical traditions")
    print(f"📈 Expected output:")
    print(f"   - {total_files} tradition archives")
    print(f"   - ~{total_files * 5} core concepts (5 per tradition)")
    print(f"   - {total_files} personality seed files")
    print(f"   - 1 unified knowledge index")

def check_requirements():
    """Check if required modules are available"""
    print("🔧 Checking requirements...")
    
    try:
        import requests
        print("✅ requests module available")
    except ImportError:
        print("❌ requests module required for Wikipedia API")
        return False
    
    # Check file structure - adjust path for running from archives directory
    links_dir = Path("../links")  # Go up one level to knowledge_base, then to links
    if not links_dir.exists():
        print(f"❌ Links directory not found: {links_dir}")
        return False
    
    json_files = list(links_dir.glob("research_*.json"))
    print(f"✅ Found {len(json_files)} research JSON files")
    
    return True

if __name__ == "__main__":
    print("🏛️ KNOWLEDGE EXTRACTOR TEST SUITE")
    print("="*50)
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed")
        sys.exit(1)
    
    # Preview batch structure
    preview_batch_structure()
    
    # Test single extraction
    print(f"\n{'='*50}")
    success = test_single_tradition()
    
    if success:
        print(f"\n🎉 Test completed successfully!")
        print(f"📁 Check knowledge_base/archives/ for extracted files")
        print(f"🚀 Ready to run full batch processing")
    else:
        print(f"\n❌ Test failed - check logs for details")
        sys.exit(1) 