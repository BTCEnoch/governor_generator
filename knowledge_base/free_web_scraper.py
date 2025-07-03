#!/usr/bin/env python3
"""
Free Web Scraper for Lighthouse Content
Extracts Wikipedia articles without using Claude API - saves $4.83 in tokens!
Uses requests + BeautifulSoup for direct content extraction.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from typing import Dict, List, Optional
from urllib.parse import urlparse, unquote
import logging

# LOGGING SETUP (VITAL for debugging) 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("FreeWebScraper")

class WikipediaContentExtractor:
    """
    Extracts content directly from Wikipedia articles.
    NO API TOKENS REQUIRED - Pure web scraping approach.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def search_to_direct_url(self, search_url: str) -> Optional[str]:
        """
        Convert Wikipedia search URL to direct article URL.
        Input: 'https://wikipedia.org/search?q=Hermetic+Order+of+the+Golden+Dawn'
        Output: 'https://en.wikipedia.org/wiki/Hermetic_Order_of_the_Golden_Dawn'
        """
        try:
            if 'search?q=' in search_url:
                # Extract search term from URL
                query = search_url.split('search?q=')[1]
                # Remove '+' and decode URL
                topic = unquote(query.replace('+', '_'))
                # Convert to direct Wikipedia URL
                direct_url = f"https://en.wikipedia.org/wiki/{topic}"
                logger.info(f"🔗 Converted search URL to direct: {direct_url}")
                return direct_url
            return search_url
        except Exception as e:
            logger.error(f"❌ Error converting URL: {e}")
            return None
    
    def extract_wikipedia_content(self, url: str) -> Optional[Dict]:
        """
        Extract main content from Wikipedia article.
        Returns structured content ready for knowledge entries.
        """
        try:
            logger.info(f"🌐 Scraping Wikipedia: {url}")
            
            # Convert search URL to direct article URL if needed
            direct_url = self.search_to_direct_url(url)
            if not direct_url:
                return None
                
            response = self.session.get(direct_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_elem = soup.find('h1', {'class': 'firstHeading'})
            title = title_elem.get_text() if title_elem else "Unknown Article"
            
            # Extract main content paragraphs
            content_div = soup.find('div', {'class': 'mw-parser-output'})
            if not content_div:
                logger.warning(f"⚠️ No content found for {url}")
                return None
                
            # Get first few paragraphs (summary)
            if content_div and hasattr(content_div, 'find_all'):
                paragraphs = content_div.find_all('p')[:5]  # First 5 paragraphs
                content_text = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                
                # Extract key sections
                sections = []
                headings = content_div.find_all(['h2', 'h3'], limit=10)
            else:
                content_text = ""
                sections = []
                headings = []
            for heading in headings:
                section_title = heading.get_text().replace('[edit]', '').strip()
                if section_title and len(section_title) > 2:
                    sections.append(section_title)
            
            result = {
                'title': title,
                'url': direct_url,
                'summary': content_text[:500] + '...' if len(content_text) > 500 else content_text,
                'full_content': content_text,
                'sections': sections[:5],  # Top 5 sections
                'word_count': len(content_text.split()),
                'scraped_successfully': True
            }
            
            logger.info(f"✅ Scraped {title}: {result['word_count']} words")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Network error scraping {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error scraping {url}: {e}")
            return None
    
    def scrape_tradition_sources(self, tradition_file: str) -> Dict:
        """
        Scrape all Wikipedia sources for a specific tradition.
        Input: 'research_golden_dawn.json'
        Output: Structured content ready for knowledge base
        """
        logger.info(f"📚 Starting tradition scraping: {tradition_file}")
        
        try:
            with open(tradition_file, 'r') as f:
                tradition_data = json.load(f)
        except Exception as e:
            logger.error(f"❌ Error loading {tradition_file}: {e}")
            return {}
        
        tradition_name = tradition_data.get('tradition_name', 'unknown')
        all_sources = tradition_data.get('all_sources', [])
        
        scraped_content = {
            'tradition_name': tradition_name,
            'articles': [],
            'scraping_summary': {
                'total_sources': len(all_sources),
                'scraped_successfully': 0,
                'failed_scrapes': 0,
                'total_words': 0
            }
        }
        
        # Extract Wikipedia URLs only (skip API URLs for now)
        wikipedia_urls = []
        for source in all_sources:
            if isinstance(source, str) and 'wikipedia.org' in source:
                # Parse the source string to get URL
                if "url='" in source:
                    url = source.split("url='")[1].split("'")[0]
                    wikipedia_urls.append(url)
        
        logger.info(f"🎯 Found {len(wikipedia_urls)} Wikipedia URLs to scrape")
        
        # Scrape each Wikipedia URL
        for i, url in enumerate(wikipedia_urls[:5]):  # Limit to first 5 for testing
            logger.info(f"📖 Scraping {i+1}/{min(5, len(wikipedia_urls))}: {url}")
            
            content = self.extract_wikipedia_content(url)
            if content:
                scraped_content['articles'].append(content)
                scraped_content['scraping_summary']['scraped_successfully'] += 1
                scraped_content['scraping_summary']['total_words'] += content['word_count']
            else:
                scraped_content['scraping_summary']['failed_scrapes'] += 1
            
            # Be polite to Wikipedia - small delay
            time.sleep(1)
        
        logger.info(f"✅ Tradition scraping complete: {scraped_content['scraping_summary']}")
        return scraped_content

def scrape_tradition_content(tradition_name: str) -> bool:
    """
    Scrape content for a specific tradition and save results.
    """
    logger.info(f"🚀 Starting FREE content extraction for {tradition_name}")
    
    input_file = f"research_{tradition_name}.json"
    output_file = f"scraped_{tradition_name}.json"
    
    extractor = WikipediaContentExtractor()
    scraped_data = extractor.scrape_tradition_sources(input_file)
    
    if scraped_data:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(scraped_data, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Saved scraped content to {output_file}")
            return True
        except Exception as e:
            logger.error(f"❌ Error saving {output_file}: {e}")
            return False
    else:
        logger.error(f"❌ No content scraped for {tradition_name}")
        return False

if __name__ == "__main__":
    # Test with Golden Dawn tradition first
    logger.info("🕸️ STARTING FREE WEB SCRAPING - NO API COSTS!")
    
    success = scrape_tradition_content("golden_dawn")
    if success:
        logger.info("✅ Golden Dawn scraping successful - ready to expand to other traditions!")
    else:
        logger.info("❌ Golden Dawn scraping failed - check URLs and connection") 