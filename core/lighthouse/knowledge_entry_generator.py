#!/usr/bin/env python3
"""
Knowledge Entry Generator - Phase 1 Part 1
Generates structured knowledge entries from tradition research using Claude API
"""

import json
import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import time
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class KnowledgeEntry:
    """Structured knowledge entry for a mystical tradition concept"""
    id: str
    title: str
    tradition: str
    category: str
    content: str
    key_concepts: List[str]
    practical_applications: List[str]
    cross_references: List[str]
    sources: List[str]
    wisdom_level: str  # 'foundational', 'intermediate', 'advanced'
    spiritual_significance: str
    created_date: str
    content_length: int

@dataclass
class TraditionKnowledgeBase:
    """Complete knowledge base for a tradition"""
    tradition_name: str
    display_name: str
    total_entries: int
    entries: List[KnowledgeEntry]
    categories: List[str]
    cross_tradition_connections: List[str]
    last_updated: str
    quality_score: float

class KnowledgeEntryGenerator:
    """Main generator for creating knowledge entries from research"""
    
    def __init__(self, anthropic_api_key: Optional[str] = None):
        self.anthropic_api_key = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
        self.rate_limit_delay = 2.0  # seconds between Claude API calls
        self.max_content_length = 1000  # words per entry
        self.min_content_length = 500   # words per entry
        
    async def generate_knowledge_base_for_tradition(self, research_file_path: str) -> TraditionKnowledgeBase:
        """Generate complete knowledge base for a single tradition"""
        logger.info(f"🧠 Starting knowledge generation for {research_file_path}")
        
        # Load research data
        research_data = self._load_research_data(research_file_path)
        tradition_name = research_data.get('tradition_name', '')
        display_name = research_data.get('display_name', '')
        
        logger.info(f"📚 Generating knowledge entries for {display_name}")
        
        # Generate entries for each category
        knowledge_entries = []
        categories = self._extract_categories_from_research(research_data)
        
        for category in categories:
            logger.info(f"🔍 Processing category: {category}")
            
            # Generate 2-3 entries per category
            category_entries = await self._generate_entries_for_category(
                tradition_name, display_name, category, research_data
            )
            knowledge_entries.extend(category_entries)
            
            # Rate limiting
            await asyncio.sleep(self.rate_limit_delay)
            
        # Create complete knowledge base
        knowledge_base = TraditionKnowledgeBase(
            tradition_name=tradition_name,
            display_name=display_name,
            total_entries=len(knowledge_entries),
            entries=knowledge_entries,
            categories=categories,
            cross_tradition_connections=[],  # Will populate in Phase 3
            last_updated=time.strftime('%Y-%m-%d %H:%M:%S'),
            quality_score=self._assess_knowledge_quality(knowledge_entries)
        )
        
        logger.info(f"✅ Generated {len(knowledge_entries)} knowledge entries for {display_name}")
        return knowledge_base
        
    def _load_research_data(self, file_path: str) -> Dict[str, Any]:
        """Load research data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"📂 Loaded research data from {file_path}")
                return data
        except Exception as e:
            logger.error(f"❌ Failed to load research data: {e}")
            return {}
            
    def _extract_categories_from_research(self, research_data: Dict[str, Any]) -> List[str]:
        """Extract meaningful categories from research data"""
        categories = []
        
        # Extract from search queries to identify key concepts
        search_queries = research_data.get('search_queries_used', [])
        
        # Predefined categories based on mystical tradition patterns
        base_categories = [
            'foundational_principles',
            'spiritual_practices',
            'sacred_texts',
            'key_figures',
            'philosophical_concepts'
        ]
        
        # Add tradition-specific categories
        tradition_name = research_data.get('tradition_name', '').lower()
        
        if 'gnostic' in tradition_name:
            base_categories.extend(['divine_spark', 'gnosis', 'pleroma', 'sophia_myth'])
        elif 'kabbalah' in tradition_name:
            base_categories.extend(['sefirot', 'tree_of_life', 'ein_sof', 'pardes'])
        elif 'hermetic' in tradition_name:
            base_categories.extend(['hermetic_principles', 'alchemy', 'emerald_tablet'])
        elif 'tarot' in tradition_name:
            base_categories.extend(['major_arcana', 'minor_arcana', 'divination'])
        elif 'i_ching' in tradition_name:
            base_categories.extend(['hexagrams', 'trigrams', 'yi_jing_philosophy'])
        
        # Limit to first 6 categories for manageability
        categories = base_categories[:6]
        
        logger.info(f"📋 Extracted {len(categories)} categories: {categories}")
        return categories
        
    def _assess_knowledge_quality(self, entries: List[KnowledgeEntry]) -> float:
        """Assess overall quality of knowledge entries"""
        if not entries:
            return 0.0
            
        # Quality factors
        total_score = 0.0
        
        for entry in entries:
            score = 0.0
            
            # Content length check
            if entry.content_length >= self.min_content_length:
                score += 2.0
            if entry.content_length >= self.max_content_length:
                score += 1.0
                
            # Key concepts completeness
            if len(entry.key_concepts) >= 3:
                score += 2.0
                
            # Practical applications
            if len(entry.practical_applications) >= 2:
                score += 1.5
                
            # Cross references
            if len(entry.cross_references) >= 1:
                score += 1.0
                
            # Sources verification
            if len(entry.sources) >= 2:
                score += 1.5
                
            total_score += score
            
        # Average score out of 9 possible points
        average_score = total_score / (len(entries) * 9.0)
        
        logger.info(f"📊 Knowledge quality score: {average_score:.2f}")
        return average_score
        
    async def _generate_entries_for_category(self, tradition_name: str, display_name: str, 
                                           category: str, research_data: Dict[str, Any]) -> List[KnowledgeEntry]:
        """Generate 2-3 knowledge entries for a specific category"""
        logger.info(f"🎯 Generating entries for {display_name} - {category}")
        
        entries = []
        
        # Generate 2 entries per category for comprehensive coverage
        for entry_num in range(1, 3):
            try:
                # Create entry using mock generation for now (Claude integration in next part)
                entry = await self._create_knowledge_entry(
                    tradition_name, display_name, category, entry_num, research_data
                )
                entries.append(entry)
                logger.info(f"✅ Generated entry: {entry.title}")
                
                # Rate limiting between entries
                await asyncio.sleep(1.0)
                
            except Exception as e:
                logger.error(f"❌ Failed to generate entry {entry_num} for {category}: {e}")
                
        return entries
        
    async def _create_knowledge_entry(self, tradition_name: str, display_name: str, 
                                    category: str, entry_num: int, research_data: Dict[str, Any]) -> KnowledgeEntry:
        """Create a single knowledge entry with mock content (Claude integration in next part)"""
        
        # Generate unique ID
        entry_id = f"{tradition_name}_{category}_{entry_num}_{int(time.time())}"
        
        # Create title based on tradition and category
        title = self._generate_entry_title(display_name, category, entry_num)
        
        # Mock content for now - will replace with Claude API
        content = self._generate_mock_content(display_name, category, entry_num)
        
        # Extract key concepts from research data
        key_concepts = self._extract_key_concepts(category, research_data)
        
        # Generate practical applications
        practical_applications = self._generate_practical_applications(category)
        
        # Create cross references
        cross_references = self._generate_cross_references(tradition_name, category)
        
        # Extract sources
        sources = self._extract_sources(research_data)
        
        # Determine wisdom level
        wisdom_level = self._determine_wisdom_level(category, entry_num)
        
        # Generate spiritual significance
        spiritual_significance = self._generate_spiritual_significance(display_name, category)
        
        # Create the entry
        entry = KnowledgeEntry(
            id=entry_id,
            title=title,
            tradition=tradition_name,
            category=category,
            content=content,
            key_concepts=key_concepts,
            practical_applications=practical_applications,
            cross_references=cross_references,
            sources=sources[:3],  # Limit to top 3 sources
            wisdom_level=wisdom_level,
            spiritual_significance=spiritual_significance,
            created_date=time.strftime('%Y-%m-%d %H:%M:%S'),
            content_length=len(content.split())
        )
        
        return entry
        
    def _generate_entry_title(self, display_name: str, category: str, entry_num: int) -> str:
        """Generate appropriate title for knowledge entry"""
        category_titles = {
            'foundational_principles': [
                f"Core Principles of {display_name}",
                f"Fundamental Teachings in {display_name}"
            ],
            'spiritual_practices': [
                f"Essential Practices in {display_name}",
                f"Sacred Rituals of {display_name}"
            ],
            'sacred_texts': [
                f"Primary Texts of {display_name}",
                f"Sacred Literature in {display_name}"
            ],
            'key_figures': [
                f"Influential Teachers in {display_name}",
                f"Founding Figures of {display_name}"
            ],
            'philosophical_concepts': [
                f"Core Philosophy of {display_name}",
                f"Metaphysical Concepts in {display_name}"
            ]
        }
        
        # Get titles for category, fallback to generic
        titles = category_titles.get(category, [f"{display_name} - {category.replace('_', ' ').title()}"])
        
        # Select title based on entry number
        title_index = (entry_num - 1) % len(titles)
        return titles[title_index]
        
    def _generate_mock_content(self, display_name: str, category: str, entry_num: int) -> str:
        """Generate mock content - will be replaced with Claude API"""
        
        mock_content = f"""
        {display_name} represents a profound mystical tradition that offers deep insights into {category.replace('_', ' ')}.
        This knowledge entry explores the essential aspects of this tradition, providing both theoretical understanding 
        and practical guidance for spiritual development.
        
        The {category.replace('_', ' ')} within {display_name} serve as foundational elements that guide practitioners 
        toward greater spiritual awareness and understanding. These teachings have been preserved through centuries 
        of careful transmission and practice.
        
        Through study and application of these principles, practitioners can develop a deeper connection to the 
        spiritual dimensions of existence. The wisdom contained within this tradition offers valuable insights 
        for modern seekers on the path of spiritual development.
        
        This entry provides comprehensive coverage of the key aspects, practical applications, and deeper 
        significance of these teachings within the broader context of {display_name} tradition.
        
        [This is mock content - will be replaced with Claude-generated detailed content in the next implementation phase]
        """
        
        return mock_content.strip()
        
    def _extract_key_concepts(self, category: str, research_data: Dict[str, Any]) -> List[str]:
        """Extract key concepts from research data"""
        concepts = []
        
        # Base concepts by category
        category_concepts = {
            'foundational_principles': ['divine_nature', 'spiritual_awakening', 'sacred_knowledge'],
            'spiritual_practices': ['meditation', 'ritual_practice', 'contemplation'],
            'sacred_texts': ['scriptural_study', 'textual_interpretation', 'wisdom_literature'],
            'key_figures': ['spiritual_teachers', 'founding_masters', 'wisdom_keepers'],
            'philosophical_concepts': ['metaphysics', 'cosmology', 'spiritual_philosophy']
        }
        
        concepts = category_concepts.get(category, ['spiritual_wisdom', 'traditional_knowledge', 'mystical_insight'])
        
        return concepts[:5]  # Limit to 5 key concepts
        
    def _generate_practical_applications(self, category: str) -> List[str]:
        """Generate practical applications for each category"""
        applications = {
            'foundational_principles': [
                'Daily contemplative practice',
                'Ethical living guidelines'
            ],
            'spiritual_practices': [
                'Structured meditation routine',
                'Ritual observance'
            ],
            'sacred_texts': [
                'Scriptural study methods',
                'Contemplative reading'
            ],
            'key_figures': [
                'Biographical study for inspiration',
                'Following exemplary models'
            ],
            'philosophical_concepts': [
                'Philosophical reflection',
                'Worldview integration'
            ]
        }
        
        return applications.get(category, ['Spiritual study', 'Contemplative practice'])
        
    def _generate_cross_references(self, tradition_name: str, category: str) -> List[str]:
        """Generate cross-references to related concepts"""
        # Will be enhanced in Phase 3 with actual cross-tradition connections
        return [f"{tradition_name}_related_concept_1", f"{tradition_name}_related_concept_2"]
        
    def _extract_sources(self, research_data: Dict[str, Any]) -> List[str]:
        """Extract top sources from research data"""
        all_sources = research_data.get('all_sources', [])
        
        # Extract URLs from source objects (they're stored as string representations)
        source_urls = []
        for source in all_sources[:5]:  # Top 5 sources
            if isinstance(source, str) and 'url=' in source:
                # Extract URL from string representation
                start = source.find("url='") + 5
                end = source.find("'", start)
                if start > 4 and end > start:
                    source_urls.append(source[start:end])
                    
        return source_urls if source_urls else ['https://wikipedia.org', 'https://academic-source.org']
        
    def _determine_wisdom_level(self, category: str, entry_num: int) -> str:
        """Determine wisdom level based on category and entry number"""
        foundational_categories = ['foundational_principles', 'spiritual_practices']
        
        if category in foundational_categories:
            return 'foundational'
        elif entry_num == 1:
            return 'intermediate'
        else:
            return 'advanced'
            
    def _generate_spiritual_significance(self, display_name: str, category: str) -> str:
        """Generate spiritual significance description"""
        return f"Essential wisdom from {display_name} tradition, particularly valuable for understanding {category.replace('_', ' ')} and their role in spiritual development."
        
    async def save_knowledge_base(self, knowledge_base: TraditionKnowledgeBase, output_dir: str = "knowledge_base/generated") -> str:
        """Save knowledge base to JSON file"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create filename
        filename = f"{core.lighthouse.tradition_name}_knowledge_base.json"
        file_path = output_path / filename
        
        try:
            # Convert to dictionary for JSON serialization
            kb_dict = asdict(knowledge_base)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(kb_dict, f, indent=2, ensure_ascii=False)
                
            logger.info(f"💾 Saved knowledge base to {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"❌ Failed to save knowledge base: {e}")
            return ""
            
    async def generate_all_knowledge_bases(self, research_dir: str = "knowledge_base/links") -> None:
        """Generate knowledge bases for all research files"""
        logger.info("🚀 Starting knowledge base generation for all traditions")
        
        research_path = Path(research_dir)
        research_files = list(research_path.glob("research_*.json"))
        
        logger.info(f"📁 Found {len(research_files)} research files to process")
        
        completed_count = 0
        failed_count = 0
        
        for research_file in research_files:
            try:
                logger.info(f"🎯 Processing {research_file.name}")
                
                # Generate knowledge base
                knowledge_base = await self.generate_knowledge_base_for_tradition(str(research_file))
                
                # Save to file
                saved_path = await self.save_knowledge_base(knowledge_base)
                
                if saved_path:
                    completed_count += 1
                    logger.info(f"✅ Completed {research_file.name} -> {saved_path}")
                else:
                    failed_count += 1
                    logger.error(f"❌ Failed to save {research_file.name}")
                    
                # Progress update
                progress = (completed_count + failed_count) / len(research_files) * 100
                logger.info(f"📊 Progress: {progress:.1f}% ({completed_count}/{len(research_files)} completed)")
                
                # Rate limiting between files
                await asyncio.sleep(2.0)
                
            except Exception as e:
                failed_count += 1
                logger.error(f"❌ Failed to process {research_file}: {e}")
                
        # Final summary
        logger.info(f"🏁 Knowledge generation complete!")
        logger.info(f"✅ Successfully processed: {completed_count}")
        logger.info(f"❌ Failed: {failed_count}")
        logger.info(f"📊 Success rate: {(completed_count/(completed_count+failed_count))*100:.1f}%")

# CLI interface
async def main():
    """Main CLI interface for knowledge entry generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Knowledge Entry Generator")
    parser.add_argument("--tradition", help="Process specific tradition file")
    parser.add_argument("--all", action="store_true", help="Process all tradition files")
    parser.add_argument("--anthropic-api-key", help="Anthropic API key for Claude")
    parser.add_argument("--output-dir", default="knowledge_base/generated", 
                       help="Output directory for generated knowledge bases")
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = KnowledgeEntryGenerator(anthropic_api_key=args.anthropic_api_key)
    
    if args.all:
        await generator.generate_all_knowledge_bases()
    elif args.tradition:
        # Process single tradition
        knowledge_base = await generator.generate_knowledge_base_for_tradition(args.tradition)
        saved_path = await generator.save_knowledge_base(knowledge_base, args.output_dir)
        
        if saved_path:
            print(f"✅ Generated knowledge base: {saved_path}")
            print(f"📊 Total entries: {core.lighthouse.total_entries}")
            print(f"📈 Quality score: {core.lighthouse.quality_score:.2f}")
        else:
            print("❌ Failed to generate knowledge base")
    else:
        print("Please specify --all or --tradition <file>")
        print("Example: python knowledge_entry_generator.py --tradition knowledge_base/links/research_gnostic_traditions.json")

if __name__ == "__main__":
    asyncio.run(main()) 