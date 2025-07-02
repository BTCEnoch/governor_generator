#!/usr/bin/env python3
"""
Create Unified Knowledge Index
"""

import json
from pathlib import Path
from datetime import datetime

def create_unified_index():
    """Create a unified index of all extracted knowledge"""
    print("📇 Creating unified knowledge index...")
    
    archives_dir = Path("governor_archives")
    index_data = {
        "extraction_summary": {
            "total_traditions": 0,
            "total_concepts": 0,
            "extraction_timestamp": datetime.now().isoformat()
        },
        "traditions": {},
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
            
            print(f"  📚 Indexing: {display_name}")
            
            # Add to traditions index
            index_data['traditions'][tradition_name] = {
                'display_name': display_name,
                'overview': archive_data['overview'][:200] + "..." if len(archive_data['overview']) > 200 else archive_data['overview'],
                'concept_count': len(archive_data['core_concepts']),
                'quality_rating': archive_data['quality_rating'],
                'source_count': archive_data['source_count'],
                'personality_traits': archive_data['personality_traits'],
                'interaction_patterns': archive_data['interaction_patterns']
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
            print(f"⚠️ Failed to index {archive_file}: {e}")
    
    # Save unified index
    index_file = Path("unified_knowledge_index.json")
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Unified index created with {index_data['extraction_summary']['total_traditions']} traditions")
    print(f"📊 Total unique personality traits: {len(index_data['personality_traits_index'])}")
    print(f"💬 Total interaction patterns: {len(index_data['interaction_patterns_index'])}")
    
    return index_data

if __name__ == "__main__":
    create_unified_index() 