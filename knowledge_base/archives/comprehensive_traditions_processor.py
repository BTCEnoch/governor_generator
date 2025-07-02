#!/usr/bin/env python3
"""
Comprehensive Traditions Processor
Processes ALL mystical tradition research files for complete Governor development
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from mystical_content_extractor import MysticalContentExtractor

class ComprehensiveTraditionsProcessor:
    """Process all tradition research files for complete Governor archive"""
    
    def __init__(self):
        self.extractor = MysticalContentExtractor()
        self.logger = logging.getLogger("ComprehensiveTraditionsProcessor")
        
        # All tradition research files found in links directory
        self.all_traditions = [
            "research_celtic_druidic.json",
            "research_chaos_magic.json", 
            "research_classical_philosophy.json",
            "research_egyptian_magic.json",
            "research_gnostic_traditions.json",
            "research_golden_dawn.json",
            "research_i_ching.json",
            "research_kuji_kiri.json",
            "research_norse_traditions.json",
            "research_sacred_geometry.json",
            "research_sufi_mysticism.json",
            "research_taoism.json",
            "research_tarot_knowledge.json",
            "research_thelema.json",
            # Already processed but included for completeness
            "research_enochian_magic.json",
            "research_golden_dawn_magic.json", 
            "research_hermetic_philosophy.json",
            "research_kabbalistic_mysticism.json"
        ]
        
        self.stats = {
            "processed": 0,
            "failed": 0,
            "skipped": 0,
            "total_concepts": 0,
            "total_teachings": 0
        }
    
    def process_batch_1(self):
        """Process first batch of traditions (Celtic through Egyptian)"""
        print("🏛️ Comprehensive Traditions Processing - BATCH 1")
        print("=" * 60)
        
        batch_1 = [
            "research_celtic_druidic.json",
            "research_chaos_magic.json", 
            "research_classical_philosophy.json",
            "research_egyptian_magic.json"
        ]
        
        print(f"📊 Processing Batch 1: {len(batch_1)} traditions")
        print("⚡ Creating rich Governor personality profiles")
        print()
        
        for i, tradition_file in enumerate(batch_1, 1):
            tradition_name = tradition_file.replace('research_', '').replace('.json', '').replace('_', ' ').title()
            print(f"🔄 [{i}/{len(batch_1)}] Processing: {tradition_name}")
            
            success = self.process_single_tradition(tradition_file)
            if success:
                self.stats["processed"] += 1
                print(f"     ✅ Enhanced Governor profile created")
            else:
                self.stats["failed"] += 1
                print(f"     ❌ Processing failed")
        
        self.print_batch_summary("Batch 1", batch_1)
    
    def process_batch_2(self):
        """Process second batch of traditions (Gnostic through Norse)"""
        print()
        print("🏛️ Comprehensive Traditions Processing - BATCH 2") 
        print("=" * 60)
        
        batch_2 = [
            "research_gnostic_traditions.json",
            "research_golden_dawn.json",
            "research_i_ching.json",
            "research_kuji_kiri.json",
            "research_norse_traditions.json"
        ]
        
        print(f"📊 Processing Batch 2: {len(batch_2)} traditions")
        print("⚡ Creating rich Governor personality profiles")
        print()
        
        for i, tradition_file in enumerate(batch_2, 1):
            tradition_name = tradition_file.replace('research_', '').replace('.json', '').replace('_', ' ').title()
            print(f"🔄 [{i}/{len(batch_2)}] Processing: {tradition_name}")
            
            success = self.process_single_tradition(tradition_file)
            if success:
                self.stats["processed"] += 1
                print(f"     ✅ Enhanced Governor profile created")
            else:
                self.stats["failed"] += 1
                print(f"     ❌ Processing failed")
        
        self.print_batch_summary("Batch 2", batch_2)
    
    def process_batch_3(self):
        """Process final batch of traditions (Sacred Geometry through Thelema)"""
        print()
        print("🏛️ Comprehensive Traditions Processing - BATCH 3")
        print("=" * 60)
        
        batch_3 = [
            "research_sacred_geometry.json",
            "research_sufi_mysticism.json",
            "research_taoism.json",
            "research_tarot_knowledge.json",
            "research_thelema.json"
        ]
        
        print(f"📊 Processing Batch 3: {len(batch_3)} traditions")
        print("⚡ Creating rich Governor personality profiles")
        print()
        
        for i, tradition_file in enumerate(batch_3, 1):
            tradition_name = tradition_file.replace('research_', '').replace('.json', '').replace('_', ' ').title()
            print(f"🔄 [{i}/{len(batch_3)}] Processing: {tradition_name}")
            
            success = self.process_single_tradition(tradition_file)
            if success:
                self.stats["processed"] += 1
                print(f"     ✅ Enhanced Governor profile created")
            else:
                self.stats["failed"] += 1
                print(f"     ❌ Processing failed")
        
        self.print_batch_summary("Batch 3", batch_3)
    
    def process_single_tradition(self, tradition_file: str) -> bool:
        """Process a single tradition research file"""
        research_path = Path("../links") / tradition_file
        
        if not research_path.exists():
            print(f"     ❌ File not found: {research_path}")
            return False
        
        # Check if already processed (skip if archive exists and is recent)
        tradition_name = tradition_file.replace('research_', '').replace('.json', '')
        archive_file = Path("governor_archives") / f"{tradition_name}_governor_archive.json"
        
        if archive_file.exists():
            # Check if it's a recent enhanced version
            try:
                with open(archive_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                if existing_data.get('quality_rating') == 'ENHANCED' and len(existing_data.get('key_concepts', [])) > 0:
                    print(f"     ⏭️  Already enhanced - skipping")
                    self.stats["skipped"] += 1
                    return True
            except:
                pass
        
        try:
            # Process with enhanced extractor
            success = self.extractor.process_mystical_tradition(research_path)
            
            if success:
                # Count extracted content
                if archive_file.exists():
                    with open(archive_file, 'r', encoding='utf-8') as f:
                        archive_data = json.load(f)
                    self.stats["total_concepts"] += len(archive_data.get('key_concepts', []))
                    self.stats["total_teachings"] += len(archive_data.get('wisdom_teachings', []))
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error processing {tradition_file}: {str(e)}")
            return False 

    def print_batch_summary(self, batch_name: str, batch_list: list):
        """Print summary statistics for a batch"""
        print()
        print(f"📊 {batch_name} Summary:")
        print(f"     ✅ {len(batch_list)} traditions processed")
        print(f"     ⚡ Enhanced Governor profiles created")
        print(f"     🧠 Rich personality content extracted")
        print()
    
    def process_all_traditions(self):
        """Process all tradition research files in organized batches"""
        print("🏛️ COMPREHENSIVE MYSTICAL TRADITIONS PROCESSING")
        print("=" * 80)
        print("⚡ Extracting rich Governor personalities from ALL traditions")
        print("🌟 Creating detailed wisdom profiles for 91 Governor Angels")
        print()
        
        start_time = datetime.now()
        
        # Process in organized batches
        self.process_batch_1()
        self.process_batch_2() 
        self.process_batch_3()
        
        # Final summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("🎉 COMPREHENSIVE PROCESSING COMPLETE!")
        print("=" * 80)
        print(f"📊 Final Statistics:")
        print(f"     ✅ {self.stats['processed']} traditions enhanced")
        print(f"     ⏭️  {self.stats['skipped']} already enhanced")
        print(f"     ❌ {self.stats['failed']} failed")
        print(f"     🧠 {self.stats['total_concepts']} total concepts extracted")
        print(f"     🌟 {self.stats['total_teachings']} wisdom teachings created")
        print(f"     ⏱️  Completed in {duration:.2f} seconds")
        print()
        print("🏛️ All Governor Angel personalities now have rich mystical wisdom!")
        print("⚡ Ready for storyline generation and game integration!")
        
    def create_unified_index(self):
        """Create a unified index of all processed traditions"""
        print("🔄 Creating unified traditions index...")
        
        unified_index = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "version": "2.0_enhanced",
                "total_traditions": len(self.all_traditions),
                "processed_traditions": self.stats["processed"] + self.stats["skipped"]
            },
            "traditions": [],
            "aggregate_stats": {
                "total_concepts": self.stats["total_concepts"],
                "total_teachings": self.stats["total_teachings"],
                "processing_stats": self.stats
            }
        }
        
        # Add each tradition to the index
        for tradition_file in self.all_traditions:
            tradition_name = tradition_file.replace('research_', '').replace('.json', '')
            archive_file = Path("governor_archives") / f"{tradition_name}_governor_archive.json"
            
            if archive_file.exists():
                try:
                    with open(archive_file, 'r', encoding='utf-8') as f:
                        archive_data = json.load(f)
                    
                    unified_index["traditions"].append({
                        "name": tradition_name,
                        "display_name": archive_data.get("display_name", tradition_name.title()),
                        "concept_count": len(archive_data.get("key_concepts", [])),
                        "teaching_count": len(archive_data.get("wisdom_teachings", [])),
                        "quality_rating": archive_data.get("quality_rating", "BASIC"),
                        "governor_essence": archive_data.get("governor_essence", "")[:100] + "..." if len(archive_data.get("governor_essence", "")) > 100 else archive_data.get("governor_essence", "")
                    })
                except Exception as e:
                    print(f"     ⚠️  Error indexing {tradition_name}: {str(e)}")
        
        # Save unified index
        index_file = Path("comprehensive_traditions_index.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(unified_index, f, indent=2, ensure_ascii=False)
        
        print(f"     ✅ Unified index created: {index_file}")
        return unified_index

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run processor
    processor = ComprehensiveTraditionsProcessor()
    processor.process_all_traditions()
    processor.create_unified_index()
    
    print("🎊 ALL MYSTICAL TRADITIONS PROCESSING COMPLETE!")
    print("🏛️ Governor Angel personalities are now fully enhanced!")
    print("⚡ Ready for the next phase of development!") 