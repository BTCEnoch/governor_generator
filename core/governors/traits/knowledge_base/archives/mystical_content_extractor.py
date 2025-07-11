#!/usr/bin/env python3
"""
Mystical Content Extractor
Specialized extractor for rich content from our mystical tradition research files
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class MysticalContentExtractor:
    """Extract rich content from mystical tradition research files"""
    
    def __init__(self):
        self.logger = logging.getLogger("MysticalContentExtractor")
    
    def extract_concepts_from_sources(self, tradition_data: Dict) -> List[Dict]:
        """Extract detailed concepts from categorized sources"""
        concepts = []
        
        categorized = tradition_data.get('categorized_sources', {})
        tradition_name = tradition_data.get('display_name', '')
        
        # Extract from all source categories
        all_sources = []
        for category, sources in categorized.items():
            all_sources.extend(sources)
        
        # Process each source to create concepts
        for i, source in enumerate(all_sources[:5]):  # Limit to 5 key concepts
            if isinstance(source, dict):
                concept = {
                    "name": source.get('title', f'Concept {i+1}').split(' - ')[0],
                    "core_principle": source.get('summary', ''),
                    "practical_wisdom": source.get('content', '')[:200] + '...',
                    "personality_influence": f"Influences {tradition_name} governors through {source.get('title', 'this concept').lower()}",
                    "decision_making_style": self.get_decision_style(tradition_name),
                    "communication_approach": self.get_communication_style(tradition_name),
                    "conflict_resolution": self.get_conflict_style(tradition_name),
                    "growth_potential": f"Through understanding {source.get('title', 'this principle').lower()}",
                    "interaction_triggers": source.get('key_concepts', ['spiritual guidance', 'wisdom seeking', 'personal growth']),
                    "wisdom_quotes": [
                        f"Through {source.get('title', 'wisdom')} we find deeper understanding.",
                        f"The path of {tradition_name} reveals truth through {source.get('title', 'knowledge').lower()}."
                    ],
                    "source_tradition": tradition_name
                }
                concepts.append(concept)
        
        return concepts
    
    def extract_wisdom_teachings(self, tradition_data: Dict) -> List[str]:
        """Extract wisdom teachings from tradition sources"""
        teachings = []
        tradition_name = tradition_data.get('display_name', '')
        
        # Base teachings for each tradition type
        if 'enochian' in tradition_name.lower():
            teachings = [
                "Governance requires clear communication with higher wisdom",
                "True authority comes from divine alignment and authentic purpose", 
                "Leadership involves bridging earthly concerns with spiritual insight",
                "Effective governors maintain connection to both human needs and divine will",
                "Wisdom flows through those who remain open to angelic guidance",
                "Sacred language and proper invocation create powerful change",
                "The 91 governors teach unique approaches to spiritual leadership",
                "Aethyric wisdom provides multi-dimensional perspective on challenges"
            ]
        elif 'hermetic' in tradition_name.lower():
            teachings = [
                "As above, so below - governance must align earthly and cosmic principles",
                "Mental mastery precedes effective external leadership",
                "All phenomena operate through universal laws that can be understood",
                "Polarity thinking resolves apparent contradictions in governance",
                "Rhythm and cycles guide optimal timing for decision-making",
                "Every action has consequences that ripple through multiple planes",
                "Balance of masculine and feminine principles creates wholeness"
            ]
        elif 'kabbalah' in tradition_name.lower():
            teachings = [
                "The Tree of Life provides a complete map for spiritual governance",
                "Each Sefirah offers unique wisdom for different aspects of leadership",
                "Divine emanation flows from crown to kingdom through balanced channels",
                "Wisdom (Chokhmah) and Understanding (Binah) must work in harmony",
                "The heart center (Tiferet) balances all opposing forces",
                "Practical manifestation requires grounding in Malkuth",
                "Gematria reveals hidden connections and deeper meanings",
                "Four Worlds teach progressive refinement of consciousness"
            ]
        else:
            # Generic mystical teachings
            teachings = [
                f"{tradition_name} teaches authentic self-expression in leadership",
                "Wisdom governance balances authority with compassion",
                "True power serves the highest good of all beings",
                "Sacred principles guide ethical decision-making",
                "Spiritual insight illuminates practical solutions"
            ]
        
        return teachings
    
    def get_decision_style(self, tradition: str) -> str:
        """Get decision-making style based on tradition"""
        styles = {
            'enochian': 'Divinely-guided with angelic consultation',
            'hermetic': 'Principled through universal laws',
            'kabbalah': 'Balanced through Sefirot wisdom',
            'golden_dawn': 'Ritually-informed with ceremonial preparation'
        }
        
        for key, style in styles.items():
            if key in tradition.lower():
                return style
        return 'Wisdom-informed with spiritual consideration'
    
    def get_communication_style(self, tradition: str) -> str:
        """Get communication style based on tradition"""
        styles = {
            'enochian': 'Sacred language with divine authority',
            'hermetic': 'Analogical and correspondence-based',
            'kabbalah': 'Symbolic and numerologically-aware',
            'golden_dawn': 'Ritualistic and formally structured'
        }
        
        for key, style in styles.items():
            if key in tradition.lower():
                return style
        return 'Authentic and wisdom-centered'
    
    def get_conflict_style(self, tradition: str) -> str:
        """Get conflict resolution style based on tradition"""
        styles = {
            'enochian': 'Invokes higher powers for divine resolution',
            'hermetic': 'Applies universal principles to find balance',
            'kabbalah': 'Seeks harmony through Tree of Life wisdom',
            'golden_dawn': 'Uses ceremonial methods for clarity'
        }
        
        for key, style in styles.items():
            if key in tradition.lower():
                return style
        return 'Seeks understanding through wisdom application'
    
    def create_enhanced_archive(self, tradition_data: Dict) -> Dict:
        """Create enhanced archive with rich content"""
        tradition_name = tradition_data.get('tradition_name', '')
        display_name = tradition_data.get('display_name', '')
        
        concepts = self.extract_concepts_from_sources(tradition_data)
        teachings = self.extract_wisdom_teachings(tradition_data)
        
        # Generate decision frameworks
        frameworks = [
            f"How does this align with {display_name} principles?",
            "What would the highest wisdom counsel in this situation?",
            "How can I serve the greatest good while maintaining integrity?",
            f"What approach honors the {display_name} tradition?",
            "How does this choice affect all levels of being?",
            "What would a wise {display_name} master recommend?"
        ]
        
        archive = {
            "tradition_name": tradition_name,
            "display_name": display_name,
            "overview": f"{display_name} provides comprehensive wisdom for governance through authentic spiritual principles and practical magical knowledge.",
            "governor_essence": f"A {display_name} Governor embodies the synthesis of spiritual wisdom and practical leadership, guided by {tradition_name.replace('_', ' ')} principles.",
            "key_concepts": concepts,
            "personality_traits": ["wise", "authentic", "spiritually-grounded", "balanced", "insightful"],
            "interaction_patterns": [
                f"Speaks from {display_name} wisdom",
                "Integrates spiritual and practical concerns",
                "Offers multi-dimensional perspective",
                "Maintains connection to higher principles"
            ],
            "decision_frameworks": frameworks,
            "wisdom_teachings": teachings,
            "conflict_styles": [self.get_conflict_style(display_name)],
            "growth_paths": [f"Through deepening {display_name} understanding", "Via practical application of spiritual principles"],
            "communication_styles": [self.get_communication_style(display_name)],
            "ethical_principles": [
                "Act in alignment with divine will",
                "Serve the highest good of all beings", 
                "Maintain authentic spiritual authority",
                f"Honor the wisdom of {display_name}"
            ],
            "power_dynamics": [f"Uses {display_name} principles for empowerment", "Balances authority with wisdom"],
            "relationship_approaches": [f"Connects through {display_name} understanding", "Builds trust through authentic wisdom"],
            "source_count": len(tradition_data.get('categorized_sources', {}).get('primary_sources', [])) + 
                           len(tradition_data.get('categorized_sources', {}).get('academic_sources', [])),
            "quality_rating": "ENHANCED",
            "extraction_timestamp": datetime.now().isoformat()
        }
        
        return archive
    
    def process_mystical_tradition(self, research_file: Path) -> bool:
        """Process a single mystical tradition research file"""
        try:
            with open(research_file, 'r', encoding='utf-8') as f:
                tradition_data = json.load(f)
            
            # Create enhanced archive
            archive = self.create_enhanced_archive(tradition_data)
            
            # Save only the complete archive (streamlined approach)
            tradition_name = archive['tradition_name']
            archive_dir = Path("governor_archives")
            archive_dir.mkdir(exist_ok=True)
            
            archive_file = archive_dir / f"{tradition_name}_governor_archive.json"
            with open(archive_file, 'w', encoding='utf-8') as f:
                json.dump(archive, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing {research_file}: {str(e)}")
            return False

def main():
    """Process all mystical tradition research files"""
    extractor = MysticalContentExtractor()
    
    research_files = [
        "../links/research_enochian_magic.json",
        "../links/research_hermetic_philosophy.json", 
        "../links/research_kabbalistic_mysticism.json"
    ]
    
    print("🔮 Mystical Content Enhanced Extraction")
    print("=" * 50)
    
    processed = 0
    for research_file in research_files:
        file_path = Path(research_file)
        if file_path.exists():
            tradition_name = file_path.stem.replace('research_', '').replace('_', ' ').title()
            print(f"🔄 Processing: {tradition_name}")
            
            success = extractor.process_mystical_tradition(file_path)
            if success:
                print(f"✅ Enhanced: {tradition_name}")
                processed += 1
            else:
                print(f"❌ Failed: {tradition_name}")
        else:
            print(f"❌ File not found: {research_file}")
    
    print()
    print(f"🎉 Successfully enhanced {processed}/{len(research_files)} mystical traditions!")
    print("📁 Rich content created in governor_archives/")

if __name__ == "__main__":
    main() 