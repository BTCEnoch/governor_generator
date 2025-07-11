#!/usr/bin/env python3
"""
Wiki Tarot Extractor - Specialized Wikipedia API extractor for tarot cards
Extracts missing major and minor arcana cards from Wikipedia
"""

import json
import wikipediaapi
import time
from typing import Dict, List, Any, Optional, Tuple
import logging
from pathlib import Path

# Import our tarot schemas
from core.mystical_systems.tarot_system.schemas.tarot_schemas import TarotCard, TarotSuit

# LOGGING SETUP
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WikiTarotExtractor")

class WikiTarotExtractor:
    """
    Specialized Wikipedia API extractor for tarot cards.
    Extracts missing major arcana and minor arcana cards from Wikipedia.
    """
    
    def __init__(self):
        # Initialize Wikipedia API
        self.wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='EnochianGovernorGenerator/1.0 (Educational Research)'
        )
        
        # Track what we've extracted
        self.extracted_cards = []
        self.extraction_stats = {
            'total_attempted': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'errors': []
        }
        
        # Missing Major Arcana cards (17 cards missing from current database)
        self.missing_major_arcana = [
            ("The Hierophant", 5, "Taurus"),
            ("The Lovers", 6, "Gemini"),
            ("The Chariot", 7, "Cancer"),
            ("Strength", 8, "Leo"),
            ("The Hermit", 9, "Virgo"),
            ("Wheel of Fortune", 10, "Jupiter"),
            ("Justice", 11, "Libra"),
            ("The Hanged Man", 12, "Neptune"),
            ("Death", 13, "Scorpio"),
            ("Temperance", 14, "Sagittarius"),
            ("The Devil", 15, "Capricorn"),
            ("The Tower", 16, "Mars"),
            ("The Star", 17, "Aquarius"),
            ("The Moon", 18, "Pisces"),
            ("The Sun", 19, "Sun"),
            ("Judgement", 20, "Pluto"),
            ("The World", 21, "Saturn")
        ]
        
        logger.info("WikiTarotExtractor initialized")
        logger.info(f"Missing major arcana cards to extract: {len(self.missing_major_arcana)}")
    
    def extract_article_content(self, article_title: str) -> Optional[Dict[str, Any]]:
        """Extract clean content from a Wikipedia article using the API."""
        try:
            logger.info(f"🃏 Extracting tarot article: {article_title}")
            
            # Get the page
            page = self.wiki_wiki.page(article_title)
            
            if not page.exists():
                logger.warning(f"⚠️ Article not found: {article_title}")
                return None
            
            if page.summary == "":
                logger.warning(f"⚠️ Empty content for: {article_title}")
                return None
            
            return {
                'title': page.title,
                'url': page.fullurl,
                'summary': page.summary[:300] + '...' if len(page.summary) > 300 else page.summary,
                'full_content': page.text[:800] + '...' if len(page.text) > 800 else page.text,
                'word_count': len(page.text.split()),
                'source_type': 'wikipedia_api',
                'extraction_success': True
            }
            
        except Exception as e:
            logger.error(f"❌ Error extracting {article_title}: {e}")
            self.extraction_stats['errors'].append(f"Error extracting {article_title}: {e}")
            return None
    
    def extract_major_arcana_cards(self) -> List[Dict[str, Any]]:
        """Extract all missing major arcana cards from Wikipedia."""
        logger.info("🏛️ Starting major arcana extraction...")
        
        extracted_cards = []
        
        for card_name, card_number, astrological_correspondence in self.missing_major_arcana:
            try:
                self.extraction_stats['total_attempted'] += 1
                
                # Extract Wikipedia content
                wikipedia_title = f"{card_name} (Tarot card)"
                content = self.extract_article_content(wikipedia_title)
                
                if content:
                    # Create structured card data
                    card_data = {
                        'id': card_name.lower().replace(' ', '_').replace('the_', ''),
                        'name': card_name,
                        'number': card_number,
                        'suit': 'MAJOR_ARCANA',
                        'wikipedia_url': content['url'],
                        'summary': content['summary'],
                        'full_content': content['full_content'],
                        'astrological_correspondence': astrological_correspondence,
                        'extraction_source': 'wikipedia_api'
                    }
                    
                    extracted_cards.append(card_data)
                    self.extraction_stats['successful_extractions'] += 1
                    logger.info(f"✅ Successfully extracted: {card_name}")
                    
                else:
                    self.extraction_stats['failed_extractions'] += 1
                    logger.warning(f"❌ Failed to extract: {card_name}")
                
                # Be respectful - small delay between requests
                time.sleep(0.5)
                
            except Exception as e:
                self.extraction_stats['failed_extractions'] += 1
                error_msg = f"Error extracting {card_name}: {e}"
                self.extraction_stats['errors'].append(error_msg)
                logger.error(f"❌ {error_msg}")
        
        logger.info(f"🏛️ Major arcana extraction complete: {len(extracted_cards)}/{len(self.missing_major_arcana)} cards extracted")
        return extracted_cards
    
    def extract_minor_arcana_suit(self, suit_name: str, element: str) -> List[Dict[str, Any]]:
        """Extract a complete minor arcana suit from Wikipedia."""
        logger.info(f"♠️ Extracting {suit_name} suit...")
        
        extracted_cards = []
        
        # Number cards (3-10 for each suit, since we have Ace and Two already)
        for number in range(3, 11):
            try:
                self.extraction_stats['total_attempted'] += 1
                
                # Extract Wikipedia content
                wikipedia_title = f"{number} of {suit_name}"
                content = self.extract_article_content(wikipedia_title)
                
                if content:
                    card_data = {
                        'id': f"{str(number).lower()}_of_{suit_name.lower()}",
                        'name': f"{number} of {suit_name}",
                        'number': number,
                        'suit': suit_name.upper(),
                        'element': element,
                        'wikipedia_url': content['url'],
                        'summary': content['summary'],
                        'full_content': content['full_content'],
                        'extraction_source': 'wikipedia_api'
                    }
                    
                    extracted_cards.append(card_data)
                    self.extraction_stats['successful_extractions'] += 1
                    logger.info(f"✅ Successfully extracted: {number} of {suit_name}")
                    
                else:
                    self.extraction_stats['failed_extractions'] += 1
                    logger.warning(f"❌ Failed to extract: {number} of {suit_name}")
                
                time.sleep(0.3)  # Shorter delay for minor arcana
                
            except Exception as e:
                self.extraction_stats['failed_extractions'] += 1
                error_msg = f"Error extracting {number} of {suit_name}: {e}"
                self.extraction_stats['errors'].append(error_msg)
                logger.error(f"❌ {error_msg}")
        
        # Court cards (Page, Knight, Queen, King)
        court_cards = ["Page", "Knight", "Queen", "King"]
        for court_card in court_cards:
            try:
                self.extraction_stats['total_attempted'] += 1
                
                # Extract Wikipedia content
                wikipedia_title = f"{court_card} of {suit_name}"
                content = self.extract_article_content(wikipedia_title)
                
                if content:
                    card_data = {
                        'id': f"{court_card.lower()}_of_{suit_name.lower()}",
                        'name': f"{court_card} of {suit_name}",
                        'number': 0,  # Court cards don't have numbers
                        'suit': suit_name.upper(),
                        'element': element,
                        'wikipedia_url': content['url'],
                        'summary': content['summary'],
                        'full_content': content['full_content'],
                        'court_card': True,
                        'extraction_source': 'wikipedia_api'
                    }
                    
                    extracted_cards.append(card_data)
                    self.extraction_stats['successful_extractions'] += 1
                    logger.info(f"✅ Successfully extracted: {court_card} of {suit_name}")
                    
                else:
                    self.extraction_stats['failed_extractions'] += 1
                    logger.warning(f"❌ Failed to extract: {court_card} of {suit_name}")
                
                time.sleep(0.3)
                
            except Exception as e:
                self.extraction_stats['failed_extractions'] += 1
                error_msg = f"Error extracting {court_card} of {suit_name}: {e}"
                self.extraction_stats['errors'].append(error_msg)
                logger.error(f"❌ {error_msg}")
        
        logger.info(f"♠️ {suit_name} suit extraction complete: {len(extracted_cards)} cards extracted")
        return extracted_cards
    
    def extract_all_minor_arcana(self) -> List[Dict[str, Any]]:
        """Extract all missing minor arcana cards from Wikipedia."""
        logger.info("🃏 Starting minor arcana extraction...")
        
        all_cards = []
        
        # Define the four suits with their elements
        suits = [
            ("Wands", "Fire"),
            ("Cups", "Water"),
            ("Swords", "Air"),
            ("Pentacles", "Earth")
        ]
        
        for suit_name, element in suits:
            try:
                suit_cards = self.extract_minor_arcana_suit(suit_name, element)
                all_cards.extend(suit_cards)
                logger.info(f"✅ Completed {suit_name} suit: {len(suit_cards)} cards")
                
                # Longer delay between suits to be respectful
                time.sleep(1.0)
                
            except Exception as e:
                error_msg = f"Error extracting {suit_name} suit: {e}"
                self.extraction_stats['errors'].append(error_msg)
                logger.error(f"❌ {error_msg}")
        
        logger.info(f"🃏 Minor arcana extraction complete: {len(all_cards)} cards extracted")
        return all_cards
    
    def extract_all_cards(self) -> Dict[str, Any]:
        """Extract all missing tarot cards (major and minor arcana)."""
        logger.info("🔮 Starting complete tarot card extraction...")
        
        all_extracted_cards = {
            'major_arcana': [],
            'minor_arcana': [],
            'extraction_stats': {},
            'total_cards_extracted': 0
        }
        
        # Extract major arcana
        try:
            major_arcana_cards = self.extract_major_arcana_cards()
            all_extracted_cards['major_arcana'] = major_arcana_cards
            logger.info(f"✅ Major arcana: {len(major_arcana_cards)} cards extracted")
        except Exception as e:
            error_msg = f"Error extracting major arcana: {e}"
            self.extraction_stats['errors'].append(error_msg)
            logger.error(f"❌ {error_msg}")
        
        # Extract minor arcana
        try:
            minor_arcana_cards = self.extract_all_minor_arcana()
            all_extracted_cards['minor_arcana'] = minor_arcana_cards
            logger.info(f"✅ Minor arcana: {len(minor_arcana_cards)} cards extracted")
        except Exception as e:
            error_msg = f"Error extracting minor arcana: {e}"
            self.extraction_stats['errors'].append(error_msg)
            logger.error(f"❌ {error_msg}")
        
        # Calculate totals
        total_cards = len(all_extracted_cards['major_arcana']) + len(all_extracted_cards['minor_arcana'])
        all_extracted_cards['total_cards_extracted'] = total_cards
        all_extracted_cards['extraction_stats'] = self.extraction_stats
        
        logger.info(f"🔮 Complete tarot extraction finished: {total_cards} total cards extracted")
        return all_extracted_cards
    
    def save_extracted_cards(self, extracted_data: Dict[str, Any], output_file: str = "extracted_tarot_cards.json") -> bool:
        """Save extracted tarot cards to a JSON file."""
        try:
            output_path = Path(__file__).parent / output_file
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(extracted_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Extracted tarot cards saved to: {output_path}")
            return True
            
        except Exception as e:
            error_msg = f"Error saving extracted cards: {e}"
            self.extraction_stats['errors'].append(error_msg)
            logger.error(f"❌ {error_msg}")
            return False

def main():
    """Main function to run the tarot card extraction."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract missing tarot cards from Wikipedia')
    parser.add_argument('--major-only', action='store_true', 
                       help='Extract only major arcana cards')
    parser.add_argument('--minor-only', action='store_true',
                       help='Extract only minor arcana cards')
    parser.add_argument('--output', type=str, default='extracted_tarot_cards.json',
                       help='Output file name (default: extracted_tarot_cards.json)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be extracted without actually doing it')
    
    args = parser.parse_args()
    
    # Initialize extractor
    extractor = WikiTarotExtractor()
    
    if args.dry_run:
        logger.info("🔍 DRY RUN - Showing what would be extracted:")
        logger.info(f"Major arcana cards to extract: {len(extractor.missing_major_arcana)}")
        logger.info("Major arcana cards:")
        for card_name, card_number, correspondence in extractor.missing_major_arcana:
            logger.info(f"  • {card_number}. {card_name} ({correspondence})")
        
        logger.info("\nMinor arcana cards to extract:")
        suits = [("Wands", "Fire"), ("Cups", "Water"), ("Swords", "Air"), ("Pentacles", "Earth")]
        for suit_name, element in suits:
            logger.info(f"  • {suit_name} ({element}): Numbers 3-10 + Court cards (12 cards)")
        
        total_minor = len(suits) * 12  # 4 suits * 12 cards per suit
        total_cards = len(extractor.missing_major_arcana) + total_minor
        logger.info(f"\nTotal cards to extract: {total_cards}")
        return
    
    # Extract cards based on arguments
    if args.major_only:
        logger.info("🏛️ Extracting only major arcana cards...")
        major_cards = extractor.extract_major_arcana_cards()
        extracted_data = {
            'major_arcana': major_cards,
            'minor_arcana': [],
            'extraction_stats': extractor.extraction_stats,
            'total_cards_extracted': len(major_cards)
        }
        
    elif args.minor_only:
        logger.info("🃏 Extracting only minor arcana cards...")
        minor_cards = extractor.extract_all_minor_arcana()
        extracted_data = {
            'major_arcana': [],
            'minor_arcana': minor_cards,
            'extraction_stats': extractor.extraction_stats,
            'total_cards_extracted': len(minor_cards)
        }
        
    else:
        logger.info("🔮 Extracting all tarot cards...")
        extracted_data = extractor.extract_all_cards()
    
    # Save extracted cards
    if extractor.save_extracted_cards(extracted_data, args.output):
        logger.info("✅ Extraction process completed successfully!")
        
        # Print final statistics
        stats = extracted_data['extraction_stats']
        logger.info(f"""
📊 FINAL EXTRACTION STATISTICS:
   • Total attempted: {stats['total_attempted']}
   • Successful extractions: {stats['successful_extractions']}
   • Failed extractions: {stats['failed_extractions']}
   • Success rate: {(stats['successful_extractions']/stats['total_attempted']*100):.1f}%
   • Total cards extracted: {extracted_data['total_cards_extracted']}
   • Major arcana: {len(extracted_data['major_arcana'])}
   • Minor arcana: {len(extracted_data['minor_arcana'])}
   • Errors: {len(stats['errors'])}
        """)
        
        if stats['errors']:
            logger.warning("❌ Errors encountered:")
            for error in stats['errors']:
                logger.warning(f"   • {error}")
                
    else:
        logger.error("❌ Extraction process failed!")
        exit(1)

if __name__ == "__main__":
    main() 