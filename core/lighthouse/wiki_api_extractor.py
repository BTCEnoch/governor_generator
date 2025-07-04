#!/usr/bin/env python3
"""
Wikipedia API Knowledge Extractor
Uses Wikipedia-API for reliable content extraction from our 186 research sources.
Much more reliable than URL scraping approach.
"""

import json
import wikipediaapi
import time
from typing import Dict, List, Any, Optional
import logging
import re

# LOGGING SETUP (VITAL for progress tracking)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WikiAPIExtractor")

class WikiAPIKnowledgeExtractor:
    """
    Enhanced knowledge extractor using Wikipedia API.
    Handles article disambiguation, redirects, and provides clean content.
    """
    
    def __init__(self):
        # Initialize Wikipedia API
        self.wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='EnochianGovernorGenerator/1.0 (Educational Research)'
        )
        
        # Article name mappings for our mystical traditions
        self.tradition_article_mappings = {
            'golden_dawn': [
                'Hermetic Order of the Golden Dawn',
                'Golden Dawn (organization)',
                'Israel Regardie'
            ],
            'thelema': [
                'Thelema',
                'Aleister Crowley',
                'The Book of the Law'
            ],
            'egyptian_magic': [
                'Ancient Egyptian religion',
                'Egyptian mythology',
                'Magic in ancient Egypt'
            ],
            'taoism': [
                'Taoism',
                'Dao',
                'Wu wei'
            ],
            'i_ching': [
                'I Ching',
                'Hexagram (I Ching)',
                'Yin and yang'
            ],
            'kuji_kiri': [
                'Kuji-kiri',
                'Mudra',
                'Ninjutsu'
            ],
            'classical_philosophy': [
                'Ancient Greek philosophy',
                'Neoplatonism',
                'Hermeticism'
            ],
            'gnostic_traditions': [
                'Gnosticism',
                'Gnostic Gospels',
                'Sophia (Gnosticism)'
            ],
            'tarot_knowledge': [
                'Tarot',
                'Major Arcana',
                'Rider-Waite tarot deck'
            ],
            'sacred_geometry': [
                'Sacred geometry',
                'Golden ratio',
                'Platonic solid'
            ],
            'chaos_magic': [
                'Chaos magic',
                'Paradigm shift',
                'Austin Osman Spare'
            ],
            'norse_traditions': [
                'Norse mythology',
                'Runes',
                'Odin'
            ],
            'sufi_mysticism': [
                'Sufism',
                'Whirling dervishes',
                'Rumi'
            ],
            'celtic_druidic': [
                'Celtic mythology',
                'Druid',
                'Celtic polytheism'
            ]
        }
    
    def extract_article_content(self, article_title: str) -> Optional[Dict[str, Any]]:
        """Extract clean content from a Wikipedia article using the API."""
        try:
            logger.info(f"📖 Extracting: {article_title}")
            
            # Get the page
            page = self.wiki_wiki.page(article_title)
            
            if not page.exists():
                logger.warning(f"⚠️ Article not found: {article_title}")
                return None
            
            if page.summary == "":
                logger.warning(f"⚠️ Empty content for: {article_title}")
                return None
            
            # Extract sections (first 6 main sections)
            sections = []
            if hasattr(page, 'sections'):
                for section in list(page.sections)[:6]:
                    if section.title and len(section.title) > 2:
                        sections.append({
                            'title': section.title,
                            'content': section.text[:200] + '...' if len(section.text) > 200 else section.text
                        })
            
            # Get categories for context
            categories = []
            if hasattr(page, 'categories'):
                categories = [cat for cat in list(page.categories.keys())[:5] if 'Category:' in cat]
            
            return {
                'title': page.title,
                'url': page.fullurl,
                'summary': page.summary[:500] + '...' if len(page.summary) > 500 else page.summary,
                'full_content': page.text[:1500] + '...' if len(page.text) > 1500 else page.text,
                'sections': sections,
                'categories': categories,
                'word_count': len(page.text.split()),
                'summary_word_count': len(page.summary.split()),
                'source_type': 'wikipedia_api',
                'extraction_success': True
            }
            
        except Exception as e:
            logger.error(f"❌ Error extracting {article_title}: {e}")
            return None
    
    def process_tradition(self, tradition_name: str) -> Dict[str, Any]:
        """Process all articles for a single tradition using mapped article names."""
        logger.info(f"🏛️ Processing tradition: {tradition_name}")
        
        if tradition_name not in self.tradition_article_mappings:
            logger.warning(f"⚠️ No article mapping for tradition: {tradition_name}")
            return {'tradition_name': tradition_name, 'extracted_articles': [], 'success_count': 0}
        
        article_titles = self.tradition_article_mappings[tradition_name]
        extracted_content = []
        success_count = 0
        
        for i, article_title in enumerate(article_titles):
            logger.info(f"📚 Processing {i+1}/{len(article_titles)}: {article_title}")
            
            content = self.extract_article_content(article_title)
            if content:
                extracted_content.append(content)
                success_count += 1
            
            # Be respectful - small delay
            time.sleep(0.3)
        
        return {
            'tradition_name': tradition_name,
            'display_name': tradition_name.replace('_', ' ').title(),
            'extracted_articles': extracted_content,
            'success_count': success_count,
            'total_attempted': len(article_titles),
            'success_rate': success_count / len(article_titles) if article_titles else 0
        }
    
    def extract_all_traditions(self) -> Dict[str, Any]:
        """Extract content for all mystical traditions."""
        logger.info("🌟 Starting Wikipedia API knowledge extraction")
        logger.info("💰 Cost: $0.00 (Free Wikipedia API)")
        
        all_traditions = {}
        total_articles = 0
        total_successes = 0
        total_words = 0
        
        for tradition_name in self.tradition_article_mappings.keys():
            result = self.process_tradition(tradition_name)
            
            if result['extracted_articles']:
                all_traditions[tradition_name] = result
                total_articles += result['total_attempted']
                total_successes += result['success_count']
                
                # Count total words extracted
                for article in result['extracted_articles']:
                    total_words += article['word_count']
        
        summary = {
            'extraction_method': 'wikipedia_api',
            'processed_traditions': len(all_traditions),
            'total_articles_attempted': total_articles,
            'total_successful_extractions': total_successes,
            'overall_success_rate': total_successes / max(total_articles, 1),
            'total_words_extracted': total_words,
            'average_words_per_article': total_words / max(total_successes, 1)
        }
        
        return {
            'summary': summary,
            'traditions': all_traditions,
            'extraction_timestamp': time.time()
        }
    
    def save_knowledge_content(self, content_data: Dict[str, Any]) -> bool:
        """Save extracted knowledge to file."""
        try:
            with open('wiki_api_knowledge_content.json', 'w', encoding='utf-8') as f:
                json.dump(content_data, f, indent=2, ensure_ascii=False)
            
            logger.info("💾 Wiki API knowledge saved to wiki_api_knowledge_content.json")
            
            # Print comprehensive summary
            summary = content_data['summary']
            logger.info("📊 WIKIPEDIA API EXTRACTION SUMMARY:")
            logger.info(f"   Extraction method: {summary['extraction_method']}")
            logger.info(f"   Traditions processed: {summary['processed_traditions']}")
            logger.info(f"   Articles attempted: {summary['total_articles_attempted']}")
            logger.info(f"   Successful extractions: {summary['total_successful_extractions']}")
            logger.info(f"   Success rate: {summary['overall_success_rate']:.1%}")
            logger.info(f"   Total words extracted: {summary['total_words_extracted']:,}")
            logger.info(f"   Average words per article: {summary['average_words_per_article']:.0f}")
            
            return True
        except Exception as e:
            logger.error(f"❌ Error saving content: {e}")
            return False

def main():
    """Main function to extract all mystical tradition knowledge."""
    logger.info("🚀 Starting Wikipedia API Knowledge Extraction")
    
    extractor = WikiAPIKnowledgeExtractor()
    content_data = extractor.extract_all_traditions()
    
    if content_data and content_data['traditions']:
        success = extractor.save_knowledge_content(content_data)
        if success:
            logger.info("✅ WIKIPEDIA API EXTRACTION COMPLETE!")
            logger.info("🎯 Ready to build retriever system for governor integration")
        else:
            logger.error("❌ Failed to save extracted content")
    else:
        logger.error("❌ No content extracted")

if __name__ == "__main__":
    main() 