#!/usr/bin/env python3
"""
Batch Knowledge Archive Processor
Processes research JSON files in manageable batches to extract summaries and concepts
"""

import logging

from pathlib import Path
from typing import List, Dict
import json

.parent.parent))

from archives.knowledge_extractor import KnowledgeExtractor

class BatchProcessor:
    """Processes tradition research files in organized batches"""
    
    def __init__(self):
        # Initialize extractor with correct paths for running from archives directory
        self.extractor = KnowledgeExtractor(
            links_dir="../links",  # Go up to knowledge_base, then to links
            archive_dir="."        # Current directory (archives)
        self.logger = logging.getLogger("BatchProcessor")
        
        # Define processing batches for manageable chunks
        self.batches = {
            "batch_1": {
                "name": "Ancient & Classical Traditions",
                "files": [
                    "research_celtic_druidic.json",
                    "research_classical_philosophy.json", 
                    "research_egyptian_magic.json",
                    "research_gnostic_traditions.json",
                    "research_norse_traditions.json"
                ]
            },
            "batch_2": {
                "name": "Organized Mystical Systems",
                "files": [
                    "research_golden_dawn.json",
                    "research_i_ching.json", 
                    "research_kuji_kiri.json",
                    "research_sacred_geometry.json",
                    "research_tarot_knowledge.json"
                ]
            },
            "batch_3": {
                "name": "Philosophical & Modern Traditions", 
                "files": [
                    "research_chaos_magic.json",
                    "research_sufi_mysticism.json",
                    "research_taoism.json",
                    "research_thelema.json"
                ]
            }
        }
    
    def process_single_batch(self, batch_name: str) -> bool:
        """Process a single batch of tradition files"""
        if batch_name not in self.batches:
            self.logger.error(f"❌ Unknown batch: {batch_name}")
            return False
        
        batch_info = self.batches[batch_name]
        self.logger.info(f"🚀 Starting {batch_name}: {batch_info['name']}")
        self.logger.info(f"📋 Processing {len(batch_info['files'])} files")
        
        try:
            archives = self.extractor.process_batch(batch_info['files'])
            
            self.logger.info(f"✅ Completed {batch_name}")
            self.logger.info(f"📊 Successfully processed {len(archives)} traditions")
            
            # Log summary
            for archive in archives:
                self.logger.info(f"  📚 {archive.display_name}: {len(archive.core_concepts)} concepts extracted")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Batch {batch_name} failed: {e}")
            return False
    
    def process_all_batches(self) -> Dict[str, bool]:
        """Process all batches in sequence"""
        results = {}
        
        self.logger.info("🏛️ Starting full knowledge extraction process")
        self.logger.info(f"📊 Total batches: {len(self.batches)}")
        
        for batch_name in self.batches.keys():
            self.logger.info(f"\n{'='*50}")
            success = self.process_single_batch(batch_name)
            results[batch_name] = success
            
            if not success:
                self.logger.warning(f"⚠️ Batch {batch_name} failed, continuing with next batch")
        
        # Summary report
        self.logger.info(f"\n{'='*50}")
        self.logger.info("📋 FINAL PROCESSING REPORT")
        self.logger.info(f"{'='*50}")
        
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        for batch_name, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            self.logger.info(f"  {batch_name}: {status}")
        
        self.logger.info(f"\n📊 Overall Results: {successful}/{total} batches successful")
        
        if successful == total:
            self.logger.info("🎉 All batches completed successfully!")
        else:
            self.logger.warning(f"⚠️ {total - successful} batches had issues")
        
        return results
    
    def create_unified_index(self) -> None:
        """Create a unified index of all extracted knowledge"""
        self.logger.info("📇 Creating unified knowledge index")
        
        archives_dir = Path("governor_archives")
        index_data = {
            "extraction_summary": {
                "total_traditions": 0,
                "total_concepts": 0,
                "extraction_timestamp": None
            },
            "traditions": {},
            "concept_index": {},
            "personality_traits_index": {},
            "interaction_patterns_index": {}
        }
        
        # Process all archive files
        for archive_file in archives_dir.glob("*_archive.json"):
            try:
                with open(archive_file, 'r', encoding='utf-8') as f:
                    archive_data = json.load(f)
                
                tradition_name = archive_data['tradition_name']
                display_name = archive_data['display_name']
                
                # Add to traditions index
                index_data['traditions'][tradition_name] = {
                    'display_name': display_name,
                    'overview': archive_data['overview'][:200] + "..." if len(archive_data['overview']) > 200 else archive_data['overview'],
                    'concept_count': len(archive_data['core_concepts']),
                    'quality_rating': archive_data['quality_rating'],
                    'source_count': archive_data['source_count']
                }
                
                # Add concepts to concept index
                for concept in archive_data['core_concepts']:
                    concept_key = f"{tradition_name}:{concept['name']}"
                    index_data['concept_index'][concept_key] = {
                        'name': concept['name'],
                        'tradition': tradition_name,
                        'description': concept['description'][:150] + "..." if len(concept['description']) > 150 else concept['description'],
                        'practical_application': concept['practical_application']
                    }
                
                # Add personality traits
                for trait in archive_data['personality_traits']:
                    if trait not in index_data['personality_traits_index']:
                        index_data['personality_traits_index'][trait] = []
                    index_data['personality_traits_index'][trait].append(tradition_name)
                
                # Add interaction patterns  
                for pattern in archive_data['interaction_patterns']:
                    if pattern not in index_data['interaction_patterns_index']:
                        index_data['interaction_patterns_index'][pattern] = []
                    index_data['interaction_patterns_index'][pattern].append(tradition_name)
                
                index_data['extraction_summary']['total_traditions'] += 1
                index_data['extraction_summary']['total_concepts'] += len(archive_data['core_concepts'])
                
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to index {archive_file}: {e}")
        
        # Save unified index
        index_file = Path("knowledge_base/archives/unified_knowledge_index.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"✅ Unified index created with {index_data['extraction_summary']['total_traditions']} traditions")
        self.logger.info(f"📊 Total concepts indexed: {index_data['extraction_summary']['total_concepts']}")

def main():
    """Main execution function"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('knowledge_extraction.log'),
            logging.StreamHandler()
        ]
    
    processor = BatchProcessor()
    
    # Process all batches
    results = processor.process_all_batches()
    
    # Create unified index if any batches succeeded
    if any(results.values()):
        processor.create_unified_index()
    
    print(f"\n🏛️ Knowledge extraction completed!")
    print(f"📋 Check 'knowledge_extraction.log' for detailed results")
    print(f"📁 Archives saved to: knowledge_base/archives/")

if __name__ == "__main__":
    main() 