#!/usr/bin/env python3
"""
Enhanced Batch Processor for Governor Angel Development
Processes all traditions with rich content extraction for Governor personalities
"""

import logging
import json
from pathlib import Path
from datetime import datetime
from enhanced_knowledge_extractor import EnhancedKnowledgeExtractor

class EnhancedBatchProcessor:
    """Processes all traditions for enhanced Governor development"""
    
    def __init__(self):
        self.extractor = EnhancedKnowledgeExtractor()
        self.logger = logging.getLogger("EnhancedBatchProcessor")
        
        # All 14 tradition files
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
            "research_thelema.json"
        ]
    
    def process_all_traditions(self) -> bool:
        """Process all 14 traditions with enhanced extraction"""
        print("🏛️ Enhanced Governor Knowledge Extraction")
        print("="*60)
        print(f"📊 Processing {len(self.all_traditions)} mystical traditions")
        print("⚡ Extracting detailed concepts and wisdom elements")
        print()
        
        start_time = datetime.now()
        archives = []
        failed = []
        
        for i, filename in enumerate(self.all_traditions, 1):
            print(f"🔄 [{i:2d}/14] Processing: {filename.replace('research_', '').replace('.json', '').replace('_', ' ').title()}")
            
            try:
                file_archives = self.extractor.process_enhanced_batch([filename])
                if file_archives:
                    archives.extend(file_archives)
                    archive = file_archives[0]
                    print(f"     ✅ {len(archive.key_concepts)} concepts, {len(archive.wisdom_teachings)} teachings")
                else:
                    failed.append(filename)
                    print(f"     ❌ No archive created")
                
            except Exception as e:
                failed.append(filename)
                print(f"     ❌ Error: {str(e)[:50]}...")
        
        # Results summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print()
        print("="*60)
        print("📋 ENHANCED EXTRACTION RESULTS")
        print("="*60)
        print(f"✅ Successfully processed: {len(archives)}/14 traditions")
        print(f"❌ Failed: {len(failed)} traditions")
        print(f"⏱️  Total time: {duration:.1f} seconds")
        
        if archives:
            total_concepts = sum(len(a.key_concepts) for a in archives)
            total_teachings = sum(len(a.wisdom_teachings) for a in archives)
            total_frameworks = sum(len(a.decision_frameworks) for a in archives)
            
            print(f"🧠 Total concepts extracted: {total_concepts}")
            print(f"🌟 Total wisdom teachings: {total_teachings}")
            print(f"📋 Total decision frameworks: {total_frameworks}")
        
        if failed:
            print(f"\n⚠️  Failed files: {', '.join(failed)}")
        
        return len(failed) == 0
    
    def create_enhanced_index(self) -> None:
        """Create enhanced index optimized for Governor development"""
        print("\n📇 Creating Enhanced Governor Index...")
        
        governor_archives_dir = Path("governor_archives")
        
        enhanced_index = {
            "extraction_summary": {
                "total_traditions": 0,
                "total_concepts": 0,
                "total_wisdom_teachings": 0,
                "total_decision_frameworks": 0,
                "extraction_timestamp": datetime.now().isoformat()
            },
            "governor_essences": {},
            "concept_library": {},
            "wisdom_teachings_library": {},
            "decision_frameworks_library": {},
            "personality_trait_combinations": {},
            "communication_style_matrix": {},
            "ethical_principle_index": {},
            "governor_applications": {
                "decision_making": {},
                "conflict_resolution": {},
                "growth_guidance": {},
                "relationship_building": {},
                "power_management": {}
            }
        }
        
        # Process all governor archives
        for archive_file in governor_archives_dir.glob("*_governor_archive.json"):
            try:
                with open(archive_file, 'r', encoding='utf-8') as f:
                    archive_data = json.load(f)
                
                tradition_name = archive_data['tradition_name']
                display_name = archive_data['display_name']
                
                print(f"  📚 Indexing: {display_name}")
                
                # Governor essences
                enhanced_index['governor_essences'][tradition_name] = {
                    'display_name': display_name,
                    'essence': archive_data['governor_essence'],
                    'personality_traits': archive_data['personality_traits']
                }
                
                # Concepts
                for concept in archive_data['key_concepts']:
                    concept_key = f"{tradition_name}:{concept['name']}"
                    enhanced_index['concept_library'][concept_key] = {
                        'name': concept['name'],
                        'tradition': tradition_name,
                        'principle': concept['core_principle'],
                        'wisdom': concept['practical_wisdom'],
                        'triggers': concept['interaction_triggers'],
                        'quotes': concept['wisdom_quotes']
                    }
                
                # Wisdom teachings
                enhanced_index['wisdom_teachings_library'][tradition_name] = archive_data['wisdom_teachings']
                
                # Decision frameworks  
                enhanced_index['decision_frameworks_library'][tradition_name] = archive_data['decision_frameworks']
                
                # Communication styles
                enhanced_index['communication_style_matrix'][tradition_name] = archive_data['communication_styles']
                
                # Ethical principles
                enhanced_index['ethical_principle_index'][tradition_name] = archive_data['ethical_principles']
                
                # Update counters
                enhanced_index['extraction_summary']['total_traditions'] += 1
                enhanced_index['extraction_summary']['total_concepts'] += len(archive_data['key_concepts'])
                enhanced_index['extraction_summary']['total_wisdom_teachings'] += len(archive_data['wisdom_teachings'])
                enhanced_index['extraction_summary']['total_decision_frameworks'] += len(archive_data['decision_frameworks'])
                
            except Exception as e:
                print(f"  ⚠️ Failed to index {archive_file}: {e}")
        
        # Save enhanced index
        index_file = Path("enhanced_governor_index.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_index, f, indent=2, ensure_ascii=False)
        
        summary = enhanced_index['extraction_summary']
        print(f"✅ Enhanced index created:")
        print(f"   📊 {summary['total_traditions']} traditions")
        print(f"   🧠 {summary['total_concepts']} concepts")
        print(f"   🌟 {summary['total_wisdom_teachings']} wisdom teachings")
        print(f"   📋 {summary['total_decision_frameworks']} decision frameworks")

def main():
    """Run enhanced batch processing"""
    logging.basicConfig(level=logging.WARNING)  # Reduce log noise
    
    processor = EnhancedBatchProcessor()
    
    # Process all traditions
    success = processor.process_all_traditions()
    
    # Create enhanced index
    processor.create_enhanced_index()
    
    print()
    print("🎉 Enhanced Governor Knowledge Extraction Complete!")
    print("📁 Check these directories:")
    print("   - governor_archives/ (complete archives)")
    print("   - enhanced_governor_index.json (unified index)")

if __name__ == "__main__":
    main() 