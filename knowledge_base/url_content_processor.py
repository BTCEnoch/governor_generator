#!/usr/bin/env python3
"""
URL Content Processor
Processes the existing 186 collected research URLs to extract actual content.
Works with lighthouse_research_results.json data.
"""

import json
import requests
from bs4 import BeautifulSoup, Tag
import time
from typing import Dict, List, Any, Optional
import logging
from urllib.parse import urlparse, parse_qs
import re

# LOGGING SETUP (VITAL for progress tracking)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("URLContentProcessor")

class URLContentProcessor:
    """
    Processes existing research URLs to extract actual content.
    Handles Wikipedia search URLs and converts them to actual articles.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Educational Research Bot'
        })
    
    def load_research_data(self) -> Dict[str, Any]:
        """Load existing lighthouse research results."""
        try:
            with open('lighthouse_research_results.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Error loading research data: {e}")
            return {}
    
    def convert_search_url_to_article(self, search_url: str) -> str:
        """
        Convert Wikipedia search URL to direct article URL.
        Example: wikipedia.org/search?q=Hermetic+Order -> en.wikipedia.org/wiki/Hermetic_Order_of_the_Golden_Dawn
        """
        try:
            # Extract search terms from URL
            if 'wikipedia.org/search' in search_url:
                parsed = urlparse(search_url)
                query_params = parse_qs(parsed.query)
                search_term = query_params.get('q', [''])[0]
                
                # Clean up search term
                search_term = search_term.replace('+', '_')
                search_term = search_term.replace(' wikipedia', '')
                search_term = search_term.replace('"', '')
                
                # Common Wikipedia article name mappings
                article_mappings = {
                    'Hermetic_Order_of_the_Golden_Dawn': 'Hermetic_Order_of_the_Golden_Dawn',
                    'Middle_Pillar_Technique': 'Middle_Pillar_(Kabbalah)',
                    'Thelema': 'Thelema',
                    'Aleister_Crowley': 'Aleister_Crowley',
                    'Ancient_Egyptian_Magic': 'Ancient_Egyptian_religion',
                    'Chaos_Magic': 'Chaos_magic',
                    'Norse_Germanic_Traditions': 'Norse_mythology',
                    'Sufi_Mysticism': 'Sufism',
                    'Celtic_Druidic_Traditions': 'Celtic_mythology',
                    'Sacred_Geometry': 'Sacred_geometry',
                    'Kabbalah': 'Kabbalah',
                    'Gnostic_Traditions': 'Gnosticism'
                }
                
                # Try to map to known article
                article_name = article_mappings.get(search_term, search_term)
                return f"https://en.wikipedia.org/wiki/{article_name}"
            
            return search_url  # Return as-is if not a search URL
            
        except Exception as e:
            logger.warning(f"⚠️ Error converting search URL {search_url}: {e}")
            return search_url
    
    def extract_wikipedia_content(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract content from a Wikipedia article."""
        try:
            logger.info(f"🌐 Extracting: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_elem = soup.find('h1', {'class': 'firstHeading'})
            title = title_elem.get_text() if title_elem else "Unknown Article"
            
            # Extract main content
            content_div = soup.find('div', {'class': 'mw-parser-output'})
            if not content_div or not isinstance(content_div, Tag):
                logger.warning(f"⚠️ No content found for {url}")
                return None
                
            # Get introduction paragraphs
            paragraphs = content_div.find_all('p')[:4]  # First 4 paragraphs
            intro_text = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            
            # Extract key sections
            sections = []
            headings = content_div.find_all(['h2', 'h3'], limit=6)
            for heading in headings:
                if isinstance(heading, Tag):
                    section_title = heading.get_text().replace('[edit]', '').strip()
                    if section_title and len(section_title) > 2:
                        sections.append(section_title)
            
            return {
                'title': title,
                'url': url,
                'introduction': intro_text[:800] + '...' if len(intro_text) > 800 else intro_text,
                'full_content': intro_text,
                'sections': sections,
                'word_count': len(intro_text.split()),
                'source_type': 'wikipedia',
                'extraction_success': True
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Network error for {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error extracting {url}: {e}")
            return None
    
    def process_tradition_sources(self, tradition_name: str, tradition_data: Dict) -> Dict[str, Any]:
        """Process all sources for a single tradition."""
        logger.info(f"📚 Processing tradition: {tradition_name}")
        
        all_sources = tradition_data.get('all_sources', [])
        extracted_content = []
        success_count = 0
        
        # Process up to 3 Wikipedia sources per tradition for manageable content
        wikipedia_sources = [s for s in all_sources if 'wikipedia.org' in str(s)][:3]
        
        for i, source_str in enumerate(wikipedia_sources):
            logger.info(f"📖 Processing {i+1}/{len(wikipedia_sources)}: {tradition_name}")
            
            # Extract URL from source string
            url_match = re.search(r"url='([^']+)'", str(source_str))
            if not url_match:
                continue
                
            search_url = url_match.group(1)
            article_url = self.convert_search_url_to_article(search_url)
            
            content = self.extract_wikipedia_content(article_url)
            if content:
                extracted_content.append(content)
                success_count += 1
            
            # Be respectful - small delay
            time.sleep(0.5)
        
        return {
            'tradition_name': tradition_name,
            'display_name': tradition_data.get('display_name', tradition_name.title()),
            'extracted_articles': extracted_content,
            'success_count': success_count,
            'total_attempted': len(wikipedia_sources),
            'success_rate': success_count / max(len(wikipedia_sources), 1)
        }
    
    def process_all_traditions(self) -> Dict[str, Any]:
        """Process all traditions from research data."""
        logger.info("🏛️ Starting URL content processing for all traditions")
        
        research_data = self.load_research_data()
        if not research_data:
            logger.error("❌ No research data found")
            return {}
        
        blocks = research_data.get('research_blocks', [])
        processed_traditions = {}
        total_articles = 0
        total_successes = 0
        
        for block in blocks:
            traditions = block.get('traditions_researched', {})
            
            for tradition_name, tradition_data in traditions.items():
                result = self.process_tradition_sources(tradition_name, tradition_data)
                
                if result['extracted_articles']:
                    processed_traditions[tradition_name] = result
                    total_articles += result['total_attempted']
                    total_successes += result['success_count']
        
        summary = {
            'processed_traditions': len(processed_traditions),
            'total_articles_attempted': total_articles,
            'total_successful_extractions': total_successes,
            'overall_success_rate': total_successes / max(total_articles, 1),
            'extraction_method': 'wikipedia_direct_conversion'
        }
        
        return {
            'summary': summary,
            'traditions': processed_traditions,
            'processing_timestamp': time.time()
        }
    
    def save_extracted_content(self, content_data: Dict[str, Any]) -> bool:
        """Save extracted content to file."""
        try:
            with open('extracted_knowledge_content.json', 'w', encoding='utf-8') as f:
                json.dump(content_data, f, indent=2, ensure_ascii=False)
            
            logger.info("💾 Extracted content saved to extracted_knowledge_content.json")
            
            # Print summary
            summary = content_data['summary']
            logger.info("📊 EXTRACTION SUMMARY:")
            logger.info(f"   Traditions processed: {summary['processed_traditions']}")
            logger.info(f"   Articles attempted: {summary['total_articles_attempted']}")
            logger.info(f"   Successful extractions: {summary['total_successful_extractions']}")
            logger.info(f"   Success rate: {summary['overall_success_rate']:.1%}")
            
            return True
        except Exception as e:
            logger.error(f"❌ Error saving content: {e}")
            return False

def main():
    """Main function to process all URL content."""
    logger.info("🚀 Starting URL Content Processing")
    logger.info("💰 Cost: $0.00 (Using existing research URLs)")
    
    processor = URLContentProcessor()
    content_data = processor.process_all_traditions()
    
    if content_data:
        success = processor.save_extracted_content(content_data)
        if success:
            logger.info("✅ URL CONTENT PROCESSING COMPLETE!")
        else:
            logger.error("❌ Failed to save extracted content")
    else:
        logger.error("❌ No content extracted")

if __name__ == "__main__":
    main() 