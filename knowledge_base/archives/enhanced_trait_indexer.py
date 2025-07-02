#!/usr/bin/env python3
"""
Enhanced Trait Indexer for Governor Personality Refinement System
================================================================

This script consolidates all governor_indexes files into comprehensive enhanced indexes
that provide rich definitions and context for governor personality traits.

Part 1: Core indexer structure and JSON file loading
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Configure logging with UTF-8 encoding for Windows compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_trait_indexer.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TraitDefinition:
    """Enhanced trait definition with expanded context"""
    name: str
    definition: str
    category: str
    usage_context: str
    ai_personality_impact: str
    related_traits: List[str]
    mystical_correspondences: Optional[str] = None

@dataclass
class EnhancedTraitIndex:
    """Comprehensive trait index for governor personality refinement"""
    version: str
    creation_timestamp: str
    total_traits: int
    categories: Dict[str, int]
    trait_definitions: Dict[str, TraitDefinition]
    cross_references: Dict[str, List[str]]

class EnhancedTraitIndexer:
    """Builds comprehensive enhanced trait indexes from governor_indexes"""
    
    def __init__(self, indexes_dir: str = "../../governor_indexes"):
        self.indexes_dir = Path(indexes_dir)
        self.logger = logging.getLogger("EnhancedTraitIndexer")
        self.enhanced_index = None
        
        # Ensure indexes directory exists
        if not self.indexes_dir.exists():
            raise FileNotFoundError(f"Governor indexes directory not found: {self.indexes_dir}")
        
        self.logger.info("🏛️ Enhanced Trait Indexer initialized")
        self.logger.info(f"📁 Reading from: {self.indexes_dir.absolute()}")

    def load_json_file(self, filename: str) -> Optional[Any]:
        """Load and parse a JSON file from the indexes directory"""
        file_path = self.indexes_dir / filename
        
        if not file_path.exists():
            self.logger.warning(f"⚠️ File not found: {filename}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"✅ Loaded {filename} ({len(data) if isinstance(data, list) else 'dict'} items)")
            return data
        except Exception as e:
            self.logger.error(f"❌ Error loading {filename}: {e}")
            return None

    def get_available_index_files(self) -> List[str]:
        """Get list of available JSON index files"""
        json_files = list(self.indexes_dir.glob("*.json"))
        filenames = [f.name for f in json_files]
        
        self.logger.info(f"Found {len(filenames)} index files:")
        for filename in sorted(filenames):
            self.logger.info(f"   • {filename}")
        
        return sorted(filenames)

    def enhance_trait_definition(self, name: str, definition: str, category: str) -> TraitDefinition:
        """Create enhanced trait definition with AI personality context"""
        
        # Generate usage context based on category
        usage_contexts = {
            "virtues": f"When {name.lower()} is activated in governor personality, it drives positive leadership behaviors",
            "flaws": f"When {name.lower()} manifests in governor personality, it creates character depth and growth opportunities", 
            "approaches": f"When using {name.lower()} approach, governor communication style adapts to this method",
            "tones": f"When speaking in {name.lower()} tone, governor voice and manner reflect this emotional quality",
            "alignments": f"When aligned to {name.lower()}, governor moral compass and decision-making follows this philosophy",
            "roles": f"When embodying {name.lower()} archetype, governor behavior patterns match this leadership style",
            "orientations": f"When focused {name.lower()}, governor energy and attention flow in this direction",
            "polarities": f"When expressing {name.lower()} polarity, governor power manifests through this creative force"
        }
        
        usage_context = usage_contexts.get(category, f"When expressing {name.lower()}, governor personality is influenced by this trait")
        
        # Generate AI personality impact description
        personality_impacts = {
            "virtues": f"Enhances governor's noble qualities, creating inspiring and trustworthy AI responses that embody {definition.lower()}",
            "flaws": f"Adds realistic character complexity, making AI responses more nuanced with the challenge of {definition.lower()}",
            "approaches": f"Shapes governor's interaction methodology, making AI responses follow {definition.lower()} patterns",
            "tones": f"Influences governor's communication style, making AI voice {definition.lower()}",
            "alignments": f"Guides governor's ethical framework, making AI decisions reflect {definition.lower()} philosophy",
            "roles": f"Defines governor's leadership archetype, making AI behavior match {definition.lower()} patterns",
            "orientations": f"Directs governor's focus and energy, making AI attention flow toward {definition.lower()} concerns",
            "polarities": f"Channels governor's creative force, making AI power expression {definition.lower()}"
        }
        
        ai_impact = personality_impacts.get(category, f"Influences AI personality to express {definition.lower()}")
        
        return TraitDefinition(
            name=name,
            definition=definition,
            category=category,
            usage_context=usage_context,
            ai_personality_impact=ai_impact,
            related_traits=[],  # Will be populated during cross-reference phase
            mystical_correspondences=None  # Will be added based on tradition analysis
        )

    def process_trait_category(self, filename: str, category_name: str) -> Dict[str, TraitDefinition]:
        """Process a single trait category file into enhanced definitions"""
        data = self.load_json_file(filename)
        if not data:
            return {}
        
        enhanced_traits = {}
        
        # Handle different data structures
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and 'name' in item and 'definition' in item:
                    name = item['name']
                    definition = item['definition']
                    enhanced_trait = self.enhance_trait_definition(name, definition, category_name)
                    enhanced_traits[name] = enhanced_trait
        
        self.logger.info(f"Enhanced {len(enhanced_traits)} {category_name} traits from {filename}")
        return enhanced_traits

    def build_enhanced_index(self) -> EnhancedTraitIndex:
        """Build comprehensive enhanced trait index from all governor_indexes files"""
        self.logger.info("Building comprehensive enhanced trait index...")
        
        all_traits = {}
        categories = {}
        
        # Define category mappings
        category_mappings = {
            "virtues_pool.json": "virtues",
            "flaws_pool.json": "flaws", 
            "approaches.json": "approaches",
            "tones.json": "tones",
            "motive_alignment.json": "alignments",
            "role_archtypes.json": "roles",
            "orientation_io.json": "orientations",
            "polarity_cd.json": "polarities",
            "self_regard_options.json": "self_regard"
        }
        
        # Process each category
        for filename, category in category_mappings.items():
            enhanced_traits = self.process_trait_category(filename, category)
            all_traits.update(enhanced_traits)
            categories[category] = len(enhanced_traits)
            
        self.logger.info(f"Total enhanced traits created: {len(all_traits)}")
        
        # Build cross-references (simplified for now)
        cross_references = {}
        
        # Create the enhanced index
        enhanced_index = EnhancedTraitIndex(
            version="1.0.0",
            creation_timestamp=datetime.now().isoformat(),
            total_traits=len(all_traits),
            categories=categories,
            trait_definitions=all_traits,
            cross_references=cross_references
        )
        
        self.enhanced_index = enhanced_index
        return enhanced_index

    def save_enhanced_index(self, output_file: str = "enhanced_trait_index.json") -> bool:
        """Save the enhanced trait index to JSON file"""
        if not self.enhanced_index:
            self.logger.error("No enhanced index to save. Build index first.")
            return False
        
        try:
            # Convert dataclass to dict for JSON serialization
            index_dict = asdict(self.enhanced_index)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(index_dict, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Enhanced trait index saved to {output_file}")
            self.logger.info(f"Total traits: {self.enhanced_index.total_traits}")
            self.logger.info(f"Categories: {list(self.enhanced_index.categories.keys())}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving enhanced index: {e}")
            return False

    def get_traits_by_category(self, category: str) -> Dict[str, TraitDefinition]:
        """Get all traits for a specific category"""
        if not self.enhanced_index:
            return {}
        
        category_traits = {
            name: trait for name, trait in self.enhanced_index.trait_definitions.items()
            if trait.category == category
        }
        
        return category_traits

    def search_traits(self, search_term: str) -> List[TraitDefinition]:
        """Search traits by name or definition content"""
        if not self.enhanced_index:
            return []
        
        results = []
        search_lower = search_term.lower()
        
        for trait in self.enhanced_index.trait_definitions.values():
            if (search_lower in trait.name.lower() or 
                search_lower in trait.definition.lower() or
                search_lower in trait.usage_context.lower()):
                results.append(trait)
        
        return results

def main():
    """Test the complete enhanced trait indexer system"""
    print("Testing Enhanced Trait Indexer System...")
    
    try:
        # Initialize indexer
        indexer = EnhancedTraitIndexer()
        
        # List available files
        files = indexer.get_available_index_files()
        print(f"\nAvailable index files: {len(files)}")
        
        # Build enhanced index
        print("\nBuilding enhanced trait index...")
        enhanced_index = indexer.build_enhanced_index()
        
        # Display summary
        print(f"\nEnhanced Index Summary:")
        print(f"  Version: {enhanced_index.version}")
        print(f"  Total traits: {enhanced_index.total_traits}")
        print(f"  Categories: {len(enhanced_index.categories)}")
        
        for category, count in enhanced_index.categories.items():
            print(f"    • {category}: {count} traits")
        
        # Test category access
        print(f"\nTesting category access...")
        virtues = indexer.get_traits_by_category("virtues")
        print(f"  Virtues found: {len(virtues)}")
        
        if virtues:
            # Show sample virtue
            sample_virtue = next(iter(virtues.values()))
            print(f"\n  Sample virtue: {sample_virtue.name}")
            print(f"    Definition: {sample_virtue.definition}")
            print(f"    AI Impact: {sample_virtue.ai_personality_impact[:100]}...")
        
        # Test search
        print(f"\nTesting search functionality...")
        courage_results = indexer.search_traits("courage")
        print(f"  'Courage' search results: {len(courage_results)}")
        
        # Save index
        print(f"\nSaving enhanced index...")
        success = indexer.save_enhanced_index()
        if success:
            print("Enhanced trait index saved successfully!")
        
        print(f"\nEnhanced Trait Indexer system test completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 