#!/usr/bin/env python3
"""
Organized Tradition Mapper
Creates comprehensive organized mappings for all 14 wisdom traditions.
Processes research data and creates structured content mappings without Claude API.
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime
import logging

# Import our free scraper
from free_web_scraper import WikipediaContentExtractor

# LOGGING SETUP (VITAL for progress tracking)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("OrganizedMapper")

class TraditionMapper:
    """
    Creates organized mappings for all wisdom traditions.
    Maps research sources to structured content without API costs.
    """
    
    def __init__(self):
        self.extractor = WikipediaContentExtractor()
        self.tradition_files = [
            "research_golden_dawn.json",
            "research_hermetic_tradition.json", 
            "research_thelema.json",
            "research_egyptian_magic.json",
            "research_gnostic_tradition.json",
            "research_tarot_tradition.json",
            "research_sacred_geometry.json",
            "research_alchemy_tradition.json",
            "research_astrology_tradition.json",
            "research_kabbalah_tradition.json",
            "research_ritual_magic.json",
            "research_chaos_magic.json",
            "research_norse_traditions.json",
            "research_sufi_mysticism.json",
            "research_celtic_druidic.json"
        ]
        
        # Organized mapping structure
        self.master_mapping = {
            "mapping_metadata": {
                "created_at": datetime.now().isoformat(),
                "total_traditions": 0,
                "processing_method": "free_web_scraping",
                "api_cost": "$0.00",
                "content_sources": "wikipedia_direct_scraping"
            },
            "tradition_categories": {
                "foundational_systems": [],      # Golden Dawn, Hermetic, Kabbalah
                "historical_traditions": [],     # Egyptian, Gnostic, Norse, Celtic  
                "practical_arts": [],           # Tarot, Alchemy, Astrology, Ritual
                "modern_experimental": [],       # Chaos Magic, Thelema
                "mystical_traditions": []       # Sufi, advanced practices
            },
            "traditions": {},
            "cross_references": {},
            "content_summary": {
                "total_articles_scraped": 0,
                "total_word_count": 0,
                "average_words_per_tradition": 0,
                "scraping_success_rate": 0.0
            }
        }
    
    def categorize_tradition(self, tradition_name: str) -> str:
        """Categorize tradition into appropriate system type."""
        categories = {
            "foundational_systems": ["golden_dawn", "hermetic_tradition", "kabbalah_tradition"],
            "historical_traditions": ["egyptian_magic", "gnostic_tradition", "norse_traditions", "celtic_druidic"],
            "practical_arts": ["tarot_tradition", "alchemy_tradition", "astrology_tradition", "ritual_magic", "sacred_geometry"],
            "modern_experimental": ["chaos_magic", "thelema"],
            "mystical_traditions": ["sufi_mysticism"]
        }
        
        for category, traditions in categories.items():
            if tradition_name in traditions:
                return category
        return "foundational_systems"  # Default category
    
    def process_tradition_file(self, filename: str) -> Dict[str, Any]:
        """
        Process a single tradition research file into organized mapping.
        """
        if not os.path.exists(filename):
            logger.warning(f"⚠️ File not found: {filename}")
            return {}
            
        logger.info(f"📚 Processing tradition file: {filename}")
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                research_data = json.load(f)
        except Exception as e:
            logger.error(f"❌ Error loading {filename}: {e}")
            return {}
        
        tradition_name = research_data.get('tradition_name', 'unknown')
        display_name = research_data.get('display_name', tradition_name.replace('_', ' ').title())
        all_sources = research_data.get('all_sources', [])
        
        # Extract Wikipedia URLs for scraping
        wikipedia_urls = []
        for source_str in all_sources:
            if isinstance(source_str, str) and 'wikipedia.org' in source_str:
                if "url='" in source_str:
                    url = source_str.split("url='")[1].split("'")[0]
                    wikipedia_urls.append(url)
        
        # Scrape content from Wikipedia URLs
        scraped_articles = []
        total_words = 0
        successful_scrapes = 0
        
        logger.info(f"🕸️ Scraping {len(wikipedia_urls)} Wikipedia sources for {tradition_name}")
        
        for i, url in enumerate(wikipedia_urls[:3]):  # Limit to 3 per tradition for organized approach
            logger.info(f"📖 Scraping {i+1}/3: {url}")
            
            content = self.extractor.extract_wikipedia_content(url)
            if content:
                scraped_articles.append(content)
                total_words += content.get('word_count', 0)
                successful_scrapes += 1
            
            # Small delay to be respectful
            import time
            time.sleep(0.5)
        
        # Create organized tradition mapping
        tradition_mapping = {
            "tradition_info": {
                "name": tradition_name,
                "display_name": display_name,
                "category": self.categorize_tradition(tradition_name),
                "source_count": len(all_sources),
                "wikipedia_sources": len(wikipedia_urls)
            },
            "content_summary": {
                "articles_scraped": len(scraped_articles),
                "successful_scrapes": successful_scrapes,
                "total_words": total_words,
                "scraping_success_rate": successful_scrapes / max(len(wikipedia_urls[:3]), 1)
            },
            "scraped_content": scraped_articles,
            "source_urls": wikipedia_urls,
            "knowledge_areas": self.extract_knowledge_areas(scraped_articles),
            "key_concepts": self.extract_key_concepts(scraped_articles)
        }
        
        logger.info(f"✅ {tradition_name} processed: {successful_scrapes} articles, {total_words} words")
        return tradition_mapping
    
    def extract_knowledge_areas(self, articles: List[Dict]) -> List[str]:
        """Extract main knowledge areas from scraped articles."""
        areas = set()
        for article in articles:
            sections = article.get('sections', [])
            for section in sections:
                if len(section) > 3 and section not in ['References', 'External links', 'See also']:
                    areas.add(section)
        return sorted(list(areas))[:10]  # Top 10 areas
    
    def extract_key_concepts(self, articles: List[Dict]) -> List[str]:
        """Extract key concepts from article titles and content."""
        concepts = set()
        for article in articles:
            title = article.get('title', '')
            if title and len(title) > 3:
                concepts.add(title)
            
            # Extract concepts from summary
            summary = article.get('summary', '')
            # Simple concept extraction - words that appear multiple times
            words = summary.lower().split()
            for word in words:
                if len(word) > 6 and word.isalpha():
                    concepts.add(word.title())
        
        return sorted(list(concepts))[:15]  # Top 15 concepts
    
    def create_master_mapping(self) -> Dict[str, Any]:
        """
        Create comprehensive organized mapping for all traditions.
        """
        logger.info("🏛️ Creating MASTER ORGANIZED MAPPING for all traditions")
        
        processed_count = 0
        total_articles = 0
        total_words = 0
        
        for filename in self.tradition_files:
            tradition_mapping = self.process_tradition_file(filename)
            
            if tradition_mapping:
                tradition_name = tradition_mapping['tradition_info']['name']
                category = tradition_mapping['tradition_info']['category']
                
                # Add to master mapping
                self.master_mapping['traditions'][tradition_name] = tradition_mapping
                
                # Add to appropriate category
                self.master_mapping['tradition_categories'][category].append(tradition_name)
                
                # Update totals
                processed_count += 1
                total_articles += tradition_mapping['content_summary']['articles_scraped']
                total_words += tradition_mapping['content_summary']['total_words']
        
        # Update metadata
        self.master_mapping['mapping_metadata']['total_traditions'] = processed_count
        self.master_mapping['content_summary'] = {
            "total_articles_scraped": total_articles,
            "total_word_count": total_words,
            "average_words_per_tradition": total_words // max(processed_count, 1),
            "scraping_success_rate": self.calculate_overall_success_rate()
        }
        
        # Create cross-references
        self.create_cross_references()
        
        logger.info(f"✅ MASTER MAPPING COMPLETE: {processed_count} traditions, {total_articles} articles, {total_words} words")
        return self.master_mapping
    
    def calculate_overall_success_rate(self) -> float:
        """Calculate overall scraping success rate."""
        total_attempts = 0
        total_successes = 0
        
        for tradition_data in self.master_mapping['traditions'].values():
            summary = tradition_data['content_summary']
            total_attempts += 3  # We attempt 3 scrapes per tradition
            total_successes += summary['successful_scrapes']
        
        return total_successes / max(total_attempts, 1)
    
    def create_cross_references(self):
        """Create cross-references between related traditions."""
        # Simple cross-referencing based on shared concepts
        for tradition_name, tradition_data in self.master_mapping['traditions'].items():
            related_traditions = []
            current_concepts = set(tradition_data.get('key_concepts', []))
            
            for other_name, other_data in self.master_mapping['traditions'].items():
                if other_name != tradition_name:
                    other_concepts = set(other_data.get('key_concepts', []))
                    shared_concepts = current_concepts.intersection(other_concepts)
                    if len(shared_concepts) >= 2:  # At least 2 shared concepts
                        related_traditions.append({
                            'tradition': other_name,
                            'shared_concepts': list(shared_concepts)
                        })
            
            self.master_mapping['cross_references'][tradition_name] = related_traditions[:5]  # Top 5 related
    
    def save_organized_mapping(self, filename: str = "organized_tradition_mapping.json"):
        """Save the complete organized mapping to file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.master_mapping, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Organized mapping saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"❌ Error saving mapping: {e}")
            return False

def create_complete_organized_mapping():
    """Main function to create organized mapping for all traditions."""
    logger.info("🚀 STARTING COMPLETE ORGANIZED TRADITION MAPPING")
    logger.info("💰 Cost: $0.00 (No API usage - Pure web scraping)")
    
    mapper = TraditionMapper()
    master_mapping = mapper.create_master_mapping()
    
    # Save the organized mapping
    success = mapper.save_organized_mapping()
    
    if success:
        # Print summary
        summary = master_mapping['content_summary']
        logger.info("📊 ORGANIZED MAPPING SUMMARY:")
        logger.info(f"   Traditions processed: {master_mapping['mapping_metadata']['total_traditions']}")
        logger.info(f"   Total articles scraped: {summary['total_articles_scraped']}")  
        logger.info(f"   Total word count: {summary['total_word_count']:,}")
        logger.info(f"   Average words/tradition: {summary['average_words_per_tradition']}")
        logger.info(f"   Scraping success rate: {summary['scraping_success_rate']:.1%}")
        logger.info("✅ ORGANIZED MAPPING COMPLETE - Ready for governor storylines!")
    
    return master_mapping

if __name__ == "__main__":
    create_complete_organized_mapping() 