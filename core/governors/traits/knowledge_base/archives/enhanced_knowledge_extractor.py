#!/usr/bin/env python3
"""
Enhanced Knowledge Archive Extractor
Extracts detailed concepts and wisdom elements specifically for Governor Angel personality development
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import re
import requests
import time
from urllib.parse import quote

@dataclass
class GovernorConcept:
    """Enhanced concept specifically for Governor Angel development"""
    name: str
    core_principle: str
    practical_wisdom: str
    personality_influence: str
    decision_making_style: str
    communication_approach: str
    conflict_resolution: str
    growth_potential: str
    interaction_triggers: List[str]
    wisdom_quotes: List[str]
    source_tradition: str

@dataclass
class GovernorArchive:
    """Complete archive for Governor Angel personality development"""
    tradition_name: str
    display_name: str
    overview: str
    governor_essence: str  # Core personality essence for governors
    key_concepts: List[GovernorConcept]
    personality_traits: List[str]
    interaction_patterns: List[str]
    decision_frameworks: List[str]
    wisdom_teachings: List[str]
    conflict_styles: List[str]
    growth_paths: List[str]
    communication_styles: List[str]
    ethical_principles: List[str]
    power_dynamics: List[str]
    relationship_approaches: List[str]
    source_count: int
    quality_rating: str
    extraction_timestamp: str

class EnhancedKnowledgeExtractor:
    """Enhanced extractor for Governor Angel personality development"""
    
    def __init__(self, links_dir: str = "../links", archive_dir: str = "."):
        self.links_dir = Path(links_dir)
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Create only the essential directories
        (self.archive_dir / "governor_archives").mkdir(exist_ok=True)
        
        self.logger = logging.getLogger("EnhancedKnowledgeExtractor")
        self.logger.info("🏛️ Enhanced Governor Knowledge Extractor initialized")
    
    def extract_core_concepts_from_research(self, tradition_data: Dict) -> List[str]:
        """Extract core concepts from research queries and sources"""
        concepts = []
        
        # Extract from search queries (remove wikipedia/academic/etc suffixes)
        search_queries = tradition_data.get('search_queries_used', [])
        for query in search_queries:
            # Remove common suffixes
            clean_query = query.replace(' wikipedia', '').replace(' academic research', '')
            clean_query = clean_query.replace(' scholarly articles', '').replace(' encyclopedia britannica', '')
            clean_query = clean_query.replace(' academic wiki', '').replace(' scholarly source', '')
            
            # Skip general tradition queries
            if clean_query.lower() != tradition_data.get('tradition_name', '').lower():
                if clean_query not in concepts and len(clean_query) > 3:
                    concepts.append(clean_query)
        
        # Extract from categorized sources with subcategories
        categorized = tradition_data.get('categorized_sources', {})
        for category, sources in categorized.items():
            for source_str in sources:
                # Extract titles and descriptions for additional concepts
                if 'title=' in source_str:
                    title_match = re.search(r"title='([^']+)'", source_str)
                    if title_match:
                        title = title_match.group(1)
                        # Clean up the title
                        clean_title = title.split(' - ')[0]  # Remove source suffix
                        if clean_title not in concepts and len(clean_title) > 3:
                            concepts.append(clean_title)
        
        return concepts[:10]  # Limit to top 10 concepts
    
    def create_governor_concept(self, concept_name: str, tradition: str, tradition_data: Dict) -> GovernorConcept:
        """Create detailed Governor concept with personality development focus"""
        
        # Core wisdom mappings for different mystical traditions
        wisdom_mappings = {
            'thelema': {
                'core_principles': 'Individual will and divine purpose alignment',
                'decision_style': 'Will-driven with ethical consideration',
                'communication': 'Direct, purposeful, and transformative',
                'conflict': 'Confronts obstacles to true will expression',
                'growth': 'Through discovering and manifesting authentic self'
            },
            'chaos_magic': {
                'core_principles': 'Pragmatic results through belief manipulation',
                'decision_style': 'Adaptable and results-focused',
                'communication': 'Flexible, paradigm-shifting',
                'conflict': 'Uses creative and unconventional solutions',
                'growth': 'Through experimentation and paradigm flexibility'
            },
            'taoism': {
                'core_principles': 'Natural flow and effortless action',
                'decision_style': 'Intuitive, harmonious, minimalistic',
                'communication': 'Gentle, metaphorical, patient',
                'conflict': 'Seeks balance and natural resolution',
                'growth': 'Through understanding natural patterns'
            },
            'norse_traditions': {
                'core_principles': 'Honor, courage, and ancestral wisdom',
                'decision_style': 'Bold, honorable, community-focused',
                'communication': 'Direct, honest, story-driven',
                'conflict': 'Faces challenges with courage and integrity',
                'growth': 'Through trials and maintaining honor'
            },
            'sufi_mysticism': {
                'core_principles': 'Love, surrender, and divine union',
                'decision_style': 'Heart-centered and surrender-based',
                'communication': 'Poetic, loving, transcendent',
                'conflict': 'Dissolves through love and understanding',
                'growth': 'Through purification and divine love'
            }
        }
        
        tradition_key = tradition.lower().replace(' ', '_').replace('(', '').replace(')', '')
        for key in wisdom_mappings.keys():
            if key in tradition_key:
                tradition_key = key
                break
        
        mapping = wisdom_mappings.get(tradition_key, {
            'core_principles': 'Universal wisdom and spiritual insight',
            'decision_style': 'Balanced and wisdom-informed',
            'communication': 'Thoughtful and authentic',
            'conflict': 'Seeks understanding and growth',
            'growth': 'Through integration of spiritual principles'
        })
        
        # Generate concept-specific details
        concept_lower = concept_name.lower()
        
        # Determine core principle based on concept
        if 'will' in concept_lower or 'power' in concept_lower:
            core_principle = f"The principle of directed intention and {mapping['core_principles']}"
        elif 'love' in concept_lower or 'heart' in concept_lower:
            core_principle = f"The principle of compassionate wisdom and {mapping['core_principles']}"
        elif 'knowledge' in concept_lower or 'wisdom' in concept_lower:
            core_principle = f"The principle of illuminated understanding and {mapping['core_principles']}"
        elif 'balance' in concept_lower or 'harmony' in concept_lower:
            core_principle = f"The principle of dynamic equilibrium and {mapping['core_principles']}"
        else:
            core_principle = f"The principle of {concept_name.lower()} within {mapping['core_principles']}"
        
        # Generate practical wisdom
        practical_wisdom = f"In governance, {concept_name} teaches that true leadership comes from understanding {core_principle.lower()}. This manifests as the ability to guide others while maintaining authentic connection to deeper wisdom."
        
        # Generate personality influence
        personality_influence = f"Governors influenced by {concept_name} tend to be {mapping['decision_style'].split(',')[0]}, integrating {tradition} wisdom into their core identity and expressing it through their unique leadership approach."
        
        return GovernorConcept(
            name=concept_name,
            core_principle=core_principle,
            practical_wisdom=practical_wisdom,
            personality_influence=personality_influence,
            decision_making_style=mapping['decision_style'],
            communication_approach=mapping['communication'],
            conflict_resolution=mapping['conflict'],
            growth_potential=mapping['growth'],
            interaction_triggers=[
                f"Questions about {concept_name.lower()}",
                f"Discussions of {tradition.lower()} principles",
                "Moments requiring wisdom guidance",
                "Ethical decision points",
                "Personal growth conversations"
            ],
            wisdom_quotes=[
                f"Through {concept_name}, we discover the deeper currents of existence.",
                f"The wisdom of {tradition} flows through understanding {concept_name.lower()}.",
                f"In {concept_name.lower()}, we find both mystery and practical guidance."
            ],
            source_tradition=tradition
        )
    
    def generate_governor_essence(self, tradition_data: Dict, concepts: List[GovernorConcept]) -> str:
        """Generate core governor essence for personality development"""
        tradition_name = tradition_data.get('display_name', '')
        
        essence_templates = {
            'thelema': f"A {tradition_name} Governor embodies the principle of True Will - the authentic expression of one's deepest purpose. They lead through discovering and manifesting their unique divine nature while helping others find their own path.",
            
            'chaos_magic': f"A {tradition_name} Governor adapts their approach based on what achieves results. They are paradigm-flexible leaders who can shift beliefs and methods to accomplish their goals while maintaining ethical boundaries.",
            
            'taoism': f"A {tradition_name} Governor leads through wu wei - effortless action that flows with natural patterns. They guide with minimal interference, allowing situations to evolve naturally while providing gentle wisdom.",
            
            'norse_traditions': f"A {tradition_name} Governor upholds honor, courage, and ancestral wisdom. They face challenges directly, maintain integrity under pressure, and draw strength from connection to lineage and community.",
            
            'sufi_mysticism': f"A {tradition_name} Governor leads from the heart, seeing divine presence in all interactions. Their governance is an act of devotion, dissolving separation through love and compassionate understanding.",
            
            'celtic_druidic': f"A {tradition_name} Governor connects deeply with natural cycles and earth wisdom. They lead with intuitive understanding of balance, honoring both seen and unseen forces in decision-making.",
            
            'golden_dawn': f"A {tradition_name} Governor integrates multiple wisdom traditions systematically. They approach leadership through structured knowledge, ceremonial awareness, and hierarchical understanding of spiritual principles.",
            
            'classical_philosophy': f"A {tradition_name} Governor applies reason, ethics, and systematic thinking to governance. They seek truth through logical inquiry while maintaining virtue in all decisions.",
            
            'egyptian_magic': f"A {tradition_name} Governor works with cosmic principles and transformative energies. They understand the deeper structures of reality and guide others through periods of profound change.",
            
            'gnostic_traditions': f"A {tradition_name} Governor seeks hidden knowledge and transcendent understanding. They guide others toward liberation from limiting beliefs and connection to divine wisdom.",
            
            'i_ching': f"A {tradition_name} Governor reads the patterns of change and timing. They understand when to act and when to wait, guiding others through natural cycles of transformation.",
            
            'kuji_kiri': f"A {tradition_name} Governor maintains disciplined focus and protective awareness. They lead through mastery of inner energies and practical application of spiritual techniques.",
            
            'sacred_geometry': f"A {tradition_name} Governor perceives universal patterns and harmonic principles. They create order through understanding of mathematical relationships that underlie reality.",
            
            'tarot_knowledge': f"A {tradition_name} Governor reads symbolic patterns and archetypal energies. They guide others through understanding of life's deeper meanings and spiritual development phases."
        }
        
        # Find matching essence
        tradition_key = tradition_data.get('tradition_name', '').lower()
        for key, essence in essence_templates.items():
            if key in tradition_key:
                return essence
        
        # Default essence
        return f"A {tradition_name} Governor integrates wisdom from {tradition_name} to guide others with authentic spiritual insight and practical wisdom."
    
    def generate_decision_frameworks(self, tradition: str, concepts: List[GovernorConcept]) -> List[str]:
        """Generate decision-making frameworks for governors"""
        frameworks = []
        
        # Base frameworks from tradition
        tradition_frameworks = {
            'thelema': [
                "Does this action align with my True Will?",
                "Will this serve the highest good while respecting individual freedom?",
                "How does this manifest love under will?"
            ],
            'chaos_magic': [
                "What belief system will produce the best results here?",
                "Can I adapt my approach for greater effectiveness?",
                "What paradigm shift might reveal new solutions?"
            ],
            'taoism': [
                "What is the natural flow of this situation?",
                "How can I act with minimal interference?",
                "Where is the balance point that serves all?"
            ],
            'norse_traditions': [
                "What choice would bring honor to my lineage?",
                "How can I face this challenge with courage?",
                "What serves the community's highest good?"
            ],
            'sufi_mysticism': [
                "How can love guide this decision?",
                "What choice serves divine presence?",
                "How do I surrender while taking right action?"
            ]
        }
        
        # Find matching frameworks
        tradition_key = tradition.lower().replace(' ', '_').replace('(', '').replace(')', '')
        for key, frame_list in tradition_frameworks.items():
            if key in tradition_key:
                frameworks.extend(frame_list)
                break
        
        # Add universal frameworks if none found
        if not frameworks:
            frameworks = [
                "What choice serves the highest wisdom?",
                "How does this align with spiritual principles?",
                "What action creates the most beneficial outcome?"
            ]
        
        # Add concept-specific frameworks
        for concept in concepts[:3]:  # Top 3 concepts
            frameworks.append(f"How does this relate to {concept.name.lower()}?")
        
        return frameworks
    
    def generate_wisdom_teachings(self, tradition: str, concepts: List[GovernorConcept]) -> List[str]:
        """Generate wisdom teachings for governor development"""
        teachings = []
        
        # Extract wisdom from concepts
        for concept in concepts:
            teachings.append(concept.practical_wisdom)
        
        # Add tradition-specific teachings
        tradition_teachings = {
            'thelema': [
                "Every person has a unique divine purpose that seeks expression",
                "True leadership comes from authenticity rather than conformity",
                "Love guided by wisdom creates transformation"
            ],
            'chaos_magic': [
                "Belief is a tool - use what works and discard what doesn't",
                "Flexibility in approach leads to effective results",
                "Question assumptions to discover new possibilities"
            ],
            'taoism': [
                "The softest things overcome the hardest",
                "Lead by example rather than force",
                "Understanding natural timing prevents unnecessary struggle"
            ],
            'norse_traditions': [
                "Honor is more valuable than life itself",
                "Courage grows through facing rather than avoiding challenges",
                "Wisdom comes from ancestors and personal experience"
            ],
            'sufi_mysticism': [
                "The heart knows what the mind cannot understand",
                "Divine love dissolves all barriers",
                "Surrender paradoxically leads to true power"
            ]
        }
        
        tradition_key = tradition.lower().replace(' ', '_').replace('(', '').replace(')', '')
        for key, teaching_list in tradition_teachings.items():
            if key in tradition_key:
                teachings.extend(teaching_list)
                break
        
        return teachings[:8]  # Limit to 8 teachings
    
    def generate_communication_styles(self, tradition: str, concepts: List[GovernorConcept]) -> List[str]:
        """Generate communication styles for governors"""
        styles = []
        
        # Extract from concepts
        for concept in concepts:
            styles.append(concept.communication_approach)
        
        # Add tradition-specific styles
        tradition_styles = {
            'thelema': ["Direct and purposeful", "Transformative dialogue", "Authenticity-focused"],
            'chaos_magic': ["Paradigm-shifting", "Adaptable messaging", "Results-oriented communication"],
            'taoism': ["Gentle and metaphorical", "Patient listening", "Minimal but impactful words"],
            'norse_traditions': ["Direct and honest", "Story-driven", "Honor-based dialogue"],
            'sufi_mysticism': ["Poetic and heart-centered", "Love-infused speech", "Transcendent expression"],
            'celtic_druidic': ["Intuitive and nature-connected", "Cyclical storytelling", "Earth wisdom"],
            'golden_dawn': ["Formal and structured", "Multi-traditional references", "Ceremonial language"],
            'classical_philosophy': ["Logical and reasoned", "Ethical questioning", "Systematic discourse"],
            'egyptian_magic': ["Symbolic and powerful", "Transformative language", "Cosmic perspective"],
            'gnostic_traditions': ["Mystical and seeking", "Hidden knowledge sharing", "Liberation-focused"],
            'i_ching': ["Pattern-aware", "Timing-sensitive", "Change-oriented dialogue"],
            'kuji_kiri': ["Disciplined and focused", "Energy-aware", "Practical technique sharing"],
            'sacred_geometry': ["Mathematical and harmonic", "Pattern-based", "Universal principles"],
            'tarot_knowledge': ["Symbolic and archetypal", "Guidance-oriented", "Intuitive messaging"]
        }
        
        tradition_key = tradition.lower().replace(' ', '_').replace('(', '').replace(')', '')
        for key, style_list in tradition_styles.items():
            if key in tradition_key:
                styles.extend(style_list)
                break
        
        return list(set(styles))  # Remove duplicates
    
    def generate_ethical_principles(self, tradition: str, concepts: List[GovernorConcept]) -> List[str]:
        """Generate ethical principles for governors"""
        principles = []
        
        tradition_ethics = {
            'thelema': ["Respect individual will and freedom", "Love guided by wisdom", "Authentic self-expression"],
            'chaos_magic': ["Results must not harm others", "Flexibility within ethical bounds", "Question dogma, maintain compassion"],
            'taoism': ["Follow the natural way", "Maintain balance and harmony", "Act with minimal interference"],
            'norse_traditions': ["Honor above all", "Courage in facing truth", "Loyalty to community"],
            'sufi_mysticism': ["Love as highest principle", "Surrender to divine will", "Compassion for all beings"],
            'celtic_druidic': ["Respect for all life", "Honor natural cycles", "Balance between worlds"],
            'golden_dawn': ["Knowledge brings responsibility", "Hierarchy serves growth", "Integration of wisdom traditions"],
            'classical_philosophy': ["Virtue as highest good", "Reason guides action", "Justice for all"],
            'egyptian_magic': ["Ma'at - truth and order", "Transformation serves evolution", "Cosmic responsibility"],
            'gnostic_traditions': ["Seek truth beyond illusion", "Liberation for all", "Knowledge serves awakening"],
            'i_ching': ["Harmony with change", "Right timing", "Balance of opposing forces"],
            'kuji_kiri': ["Disciplined practice", "Protection of the innocent", "Mastery serves others"],
            'sacred_geometry': ["Universal harmony", "Mathematical truth", "Pattern integrity"],
            'tarot_knowledge': ["Guidance without manipulation", "Archetypal wisdom", "Personal growth focus"]
        }
        
        tradition_key = tradition.lower().replace(' ', '_').replace('(', '').replace(')', '')
        for key, principle_list in tradition_ethics.items():
            if key in tradition_key:
                principles.extend(principle_list)
                break
        
        if not principles:
            principles = ["Act with wisdom and compassion", "Serve the highest good", "Respect individual sovereignty"]
        
        return principles
    
    def process_tradition_enhanced(self, json_file: Path) -> GovernorArchive:
        """Process a tradition file for enhanced governor development"""
        self.logger.info(f"🏛️ Enhanced processing: {json_file.name}")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            tradition_data = json.load(f)
        
        tradition_name = tradition_data.get('tradition_name', '')
        display_name = tradition_data.get('display_name', '')
        
        # Extract concepts from research data
        concept_names = self.extract_core_concepts_from_research(tradition_data)
        self.logger.info(f"🧠 Found {len(concept_names)} concepts: {concept_names[:3]}...")
        
        # Create detailed governor concepts
        governor_concepts = []
        for concept_name in concept_names[:5]:  # Top 5 concepts
            concept = self.create_governor_concept(concept_name, display_name, tradition_data)
            governor_concepts.append(concept)
        
        # Generate governor essence
        governor_essence = self.generate_governor_essence(tradition_data, governor_concepts)
        
        # Generate enhanced personality elements
        decision_frameworks = self.generate_decision_frameworks(display_name, governor_concepts)
        wisdom_teachings = self.generate_wisdom_teachings(display_name, governor_concepts)
        communication_styles = self.generate_communication_styles(display_name, governor_concepts)
        ethical_principles = self.generate_ethical_principles(display_name, governor_concepts)
        
        # Extract personality traits (existing method from base class)
        tradition_traits = {
            'thelema': ['will-focused', 'individualistic', 'magical', 'self-discovering'],
            'chaos_magic': ['adaptable', 'results-oriented', 'paradigm-flexible', 'experimental'],
            'taoism': ['flowing', 'natural', 'effortless', 'balanced'],
            'norse_traditions': ['honorable', 'fate-aware', 'ancestral', 'courage-focused'],
            'sufi_mysticism': ['devotional', 'heart-centered', 'ecstatic', 'unity-seeking'],
            'celtic_druidic': ['nature-connected', 'intuitive', 'cyclical-thinking', 'earth-grounded'],
            'golden_dawn': ['scholarly', 'ceremonial', 'hierarchical', 'synthesizing'],
            'classical_philosophy': ['logical', 'ethical', 'contemplative', 'systematic'],
            'egyptian_magic': ['structured', 'ceremonial', 'cosmic-aware', 'transformative'],
            'gnostic_traditions': ['seeking', 'transcendent', 'mystical', 'knowledge-focused'],
            'i_ching': ['pattern-aware', 'cyclical', 'balanced', 'oracular'],
            'kuji_kiri': ['disciplined', 'protective', 'energy-focused', 'practical'],
            'sacred_geometry': ['pattern-conscious', 'mathematical', 'harmonic', 'universal'],
            'tarot_knowledge': ['symbolic', 'intuitive', 'archetypal', 'guidance-oriented']
        }
        
        personality_traits = tradition_traits.get(tradition_name, ['wise', 'balanced', 'authentic'])
        
        # Create enhanced archive
        archive = GovernorArchive(
            tradition_name=tradition_name,
            display_name=display_name,
            overview=f"{display_name} represents a mystical tradition that offers profound wisdom for governance and personal development.",
            governor_essence=governor_essence,
            key_concepts=governor_concepts,
            personality_traits=personality_traits,
            interaction_patterns=communication_styles[:3],  # Top 3
            decision_frameworks=decision_frameworks,
            wisdom_teachings=wisdom_teachings,
            conflict_styles=[concept.conflict_resolution for concept in governor_concepts],
            growth_paths=[concept.growth_potential for concept in governor_concepts],
            communication_styles=communication_styles,
            ethical_principles=ethical_principles,
            power_dynamics=[f"Uses {tradition_name.lower()} principles for empowerment", "Balances authority with wisdom"],
            relationship_approaches=[f"Connects through {tradition_name.lower()} understanding", "Builds trust through authenticity"],
            source_count=tradition_data.get('source_count', 0),
            quality_rating=tradition_data.get('research_quality', 'GOOD'),
            extraction_timestamp=datetime.now().isoformat()
        )
        
        return archive 

    def save_governor_archive(self, archive: GovernorArchive) -> None:
        """Save enhanced governor archive to streamlined location"""
        tradition_name = archive.tradition_name
        
        # Save only the complete governor archive (all data in one place)
        archive_file = self.archive_dir / "governor_archives" / f"{tradition_name}_governor_archive.json"
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(archive), f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"✅ Saved enhanced governor archive for {archive.display_name}")
        self.logger.info(f"📊 Key concepts: {len(archive.key_concepts)}, Wisdom teachings: {len(archive.wisdom_teachings)}")
    
    def process_enhanced_batch(self, tradition_files: List[str]) -> List[GovernorArchive]:
        """Process a batch of traditions for enhanced governor development"""
        archives = []
        
        for filename in tradition_files:
            file_path = self.links_dir / filename
            if file_path.exists():
                try:
                    archive = self.process_tradition_enhanced(file_path)
                    self.save_governor_archive(archive)
                    archives.append(archive)
                    print(f"✅ Enhanced: {archive.display_name} - {len(archive.key_concepts)} concepts")
                except Exception as e:
                    self.logger.error(f"❌ Failed to process {filename}: {e}")
            else:
                self.logger.warning(f"⚠️ File not found: {filename}")
        
        return archives

def main():
    """Test the enhanced extractor"""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    extractor = EnhancedKnowledgeExtractor()
    
    # Test with a single tradition
    test_files = ["research_thelema.json"]
    
    print("🏛️ Testing Enhanced Governor Knowledge Extraction")
    print("=" * 50)
    
    archives = extractor.process_enhanced_batch(test_files)
    
    if archives:
        archive = archives[0]
        print(f"\n🎉 Enhanced extraction completed for: {archive.display_name}")
        print(f"📊 Governor Essence: {archive.governor_essence[:100]}...")
        print(f"🧠 Key Concepts: {len(archive.key_concepts)}")
        print(f"📋 Decision Frameworks: {len(archive.decision_frameworks)}")
        print(f"💬 Communication Styles: {len(archive.communication_styles)}")
        print(f"⚖️ Ethical Principles: {len(archive.ethical_principles)}")
        print(f"🌟 Wisdom Teachings: {len(archive.wisdom_teachings)}")
        
        print(f"\n📝 Sample Key Concept:")
        if archive.key_concepts:
            concept = archive.key_concepts[0]
            print(f"   Name: {concept.name}")
            print(f"   Principle: {concept.core_principle[:100]}...")
            print(f"   Wisdom: {concept.practical_wisdom[:100]}...")
            print(f"   Triggers: {concept.interaction_triggers[:2]}")
        
        print(f"\n💡 Sample Decision Framework:")
        print(f"   {archive.decision_frameworks[0] if archive.decision_frameworks else 'None'}")
        
        print(f"\n🎭 Personality Traits: {', '.join(archive.personality_traits)}")
    
    print(f"\n📁 Enhanced files saved to:")
    print(f"   - governor_archives/ (complete archive data)")

if __name__ == "__main__":
    main() 