#!/usr/bin/env python3
"""
Mystical Traditions Processor
Specialized processor for the core mystical traditions with extensive knowledge bases
"""

import logging
import json
from pathlib import Path
from datetime import datetime
from enhanced_knowledge_extractor import EnhancedKnowledgeExtractor

class MysticalTraditionsProcessor:
    """Processes the core mystical traditions for Governor development"""
    
    def __init__(self):
        self.extractor = EnhancedKnowledgeExtractor()
        self.logger = logging.getLogger("MysticalTraditionsProcessor")
        
        # The new mystical traditions to process
        self.mystical_traditions = [
            "research_enochian_magic.json",
            "research_hermetic_philosophy.json", 
            "research_kabbalistic_mysticism.json"
        ]
        
        self.stats = {
            "processed": 0,
            "failed": 0,
            "total_concepts": 0,
            "total_teachings": 0,
            "total_frameworks": 0
        }
    
    def process_all_traditions(self):
        """Process all mystical traditions"""
        print("🏛️ Mystical Traditions Enhanced Extraction")
        print("=" * 60)
        print(f"📊 Processing {len(self.mystical_traditions)} mystical traditions")
        print("⚡ Extracting detailed Governor personality profiles")
        print()
        
        start_time = datetime.now()
        
        for i, tradition_file in enumerate(self.mystical_traditions, 1):
            print(f"🔄 [{i:2}/{len(self.mystical_traditions)}] Processing: {tradition_file.replace('research_', '').replace('.json', '').replace('_', ' ').title()}")
            
            try:
                success = self.process_tradition(tradition_file)
                if success:
                    self.stats["processed"] += 1
                    print(f"     ✅ Enhanced extraction completed")
                else:
                    self.stats["failed"] += 1
                    print(f"     ❌ Processing failed")
            except Exception as e:
                self.stats["failed"] += 1
                print(f"     ❌ Error: {str(e)}")
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        self.create_mystical_index()
        self.print_results(processing_time)
    
    def process_tradition(self, tradition_file: str) -> bool:
        """Process a single tradition file"""
        links_dir = Path("../links")
        tradition_path = links_dir / tradition_file
        
        if not tradition_path.exists():
            print(f"     ❌ File not found: {tradition_path}")
            return False
        
        try:
            # Load and process the tradition
            with open(tradition_path, 'r', encoding='utf-8') as f:
                tradition_data = json.load(f)
            
            # Extract enhanced knowledge  
            archive = self.extractor.process_tradition_enhanced(tradition_path)
            
            # Save the results
            self.extractor.save_governor_archive(archive)
            
            # Update stats
            self.stats["total_concepts"] += len(archive.key_concepts)
            self.stats["total_teachings"] += len(archive.wisdom_teachings)
            self.stats["total_frameworks"] += len(archive.decision_frameworks)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing {tradition_file}: {str(e)}")
            return False
    
    def create_mystical_index(self):
        """Create unified index for mystical traditions"""
        print()
        print("📇 Creating Mystical Traditions Index...")
        
        all_archives = []
        all_concepts = []
        all_teachings = []
        all_frameworks = []
        
        # Load all processed archives
        archive_dir = Path("governor_archives")
        if archive_dir.exists():
            for archive_file in archive_dir.glob("*_governor_archive.json"):
                try:
                    with open(archive_file, 'r', encoding='utf-8') as f:
                        archive_data = json.load(f)
                        all_archives.append(archive_data)
                        all_concepts.extend(archive_data.get('key_concepts', []))
                        all_teachings.extend(archive_data.get('wisdom_teachings', []))
                        all_frameworks.extend(archive_data.get('decision_frameworks', []))
                        print(f"  📚 Indexed: {archive_data.get('tradition_name', 'Unknown')}")
                except Exception as e:
                    print(f"  ❌ Error indexing {archive_file}: {str(e)}")
        
        # Create unified index
        mystical_index = {
            "mystical_traditions_index": {
                "creation_date": datetime.now().isoformat(),
                "total_traditions": len(all_archives),
                "total_concepts": len(all_concepts),
                "total_teachings": len(all_teachings), 
                "total_frameworks": len(all_frameworks),
                "traditions": all_archives
            }
        }
        
        # Save index
        index_path = Path("mystical_traditions_index.json")
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(mystical_index, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Mystical index created:")
        print(f"   📊 {len(all_archives)} traditions")
        print(f"   🧠 {len(all_concepts)} concepts")
        print(f"   🌟 {len(all_teachings)} wisdom teachings")  
        print(f"   📋 {len(all_frameworks)} decision frameworks")
    
    def print_results(self, processing_time: float):
        """Print final processing results"""
        print()
        print("=" * 60)
        print("📋 MYSTICAL TRADITIONS EXTRACTION RESULTS")
        print("=" * 60)
        print(f"✅ Successfully processed: {self.stats['processed']}/{len(self.mystical_traditions)} traditions")
        print(f"❌ Failed: {self.stats['failed']} traditions")
        print(f"⏱️  Total time: {processing_time:.1f} seconds")
        print(f"🧠 Total concepts extracted: {self.stats['total_concepts']}")
        print(f"🌟 Total wisdom teachings: {self.stats['total_teachings']}")
        print(f"📋 Total decision frameworks: {self.stats['total_frameworks']}")
        print()
        print(f"🎉 Mystical Traditions Enhanced Extraction Complete!")
        print(f"📁 Check these directories:")
        print(f"   - governor_archives/ (complete archives)")
        print(f"   - mystical_traditions_index.json (unified index)")

if __name__ == "__main__":
    processor = MysticalTraditionsProcessor()
    processor.process_all_traditions() 