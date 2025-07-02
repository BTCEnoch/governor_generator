#!/usr/bin/env python3
"""
Complete the remaining 2 traditions
"""

import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from archives.knowledge_extractor import KnowledgeExtractor

def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    extractor = KnowledgeExtractor(
        links_dir="../links",
        archive_dir="."
    )
    
    # Process the remaining traditions
    remaining_files = [
        "research_sufi_mysticism.json",
        "research_taoism.json"
    ]
    
    print("🏛️ Processing remaining traditions:")
    for filename in remaining_files:
        print(f"  📚 {filename}")
    
    try:
        archives = extractor.process_batch(remaining_files)
        print(f"\n✅ Successfully processed {len(archives)} traditions!")
        
        for archive in archives:
            print(f"  📚 {archive.display_name}: {len(archive.personality_traits)} traits")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 