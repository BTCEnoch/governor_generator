#!/usr/bin/env python3
"""
Enhanced Personality Seeds Generator
===================================

This script regenerates personality seeds with rich interaction patterns using:
1. Wikipedia API for authentic interaction styles
2. Governor archives data for wisdom teachings and communication styles
3. Enhanced pattern extraction for comprehensive personality development

Features:
- Wiki API integration for authentic tradition information
- Governor archives data integration
- Rich interaction pattern extraction
- Comprehensive personality trait enhancement
- Small manageable chunks processing
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import requests
from datetime import datetime

@dataclass
class EnhancedPersonalitySeed:
    """Enhanced personality seed with rich interaction patterns"""
    tradition_name: str
    display_name: str
    overview: str
    personality_traits: List[str]
    interaction_patterns: List[str]
    communication_styles: List[str]
    wisdom_approaches: List[str]
    decision_patterns: List[str]
    key_concepts: List[str]
    wisdom_elements: List[str]
    wiki_insights: List[str]
    archive_source: str
    quality_rating: str

class WikipediaEnhancedAPI:
    """Enhanced Wikipedia API with better interaction pattern extraction"""
    
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/api/rest_v1"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'GovernorPersonalityExtractor/1.0 (Educational Research)'
        })
        self.last_request_time = 0
        self.rate_limit_delay = 1.0  # 1 second between requests
        
    def _rate_limit(self):
        """Ensure rate limiting between API calls"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()
    
    def search_tradition(self, tradition_name: str, context: str = "") -> Optional[Dict]:
        """Search for tradition information with context"""
        self._rate_limit()
        
        # Create search query
        search_terms = [tradition_name]
        if context:
            search_terms.append(context)
        
        query = " ".join(search_terms)
        
        try:
            # Use Wikipedia search API
            search_url = f"https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': query,
                'srlimit': 3
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            search_data = response.json()
            
            if 'query' in search_data and 'search' in search_data['query']:
                results = search_data['query']['search']
                if results:
                    # Get the first result
                    best_match = results[0]
                    return self.get_page_content(best_match['title'])
            
            return None
            
        except Exception as e:
            logging.warning(f"Wikipedia search failed for {tradition_name}: {e}")
            return None
    
    def get_page_content(self, title: str) -> Optional[Dict]:
        """Get page content with interaction-relevant information"""
        self._rate_limit()
        
        try:
            # Get page summary
            summary_url = f"https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'prop': 'extracts|info',
                'exintro': True,
                'explaintext': True,
                'exsectionformat': 'plain',
                'titles': title,
                'inprop': 'url'
            }
            
            response = self.session.get(summary_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'query' in data and 'pages' in data['query']:
                pages = data['query']['pages']
                page_id = list(pages.keys())[0]
                
                if page_id != '-1':  # Page exists
                    page = pages[page_id]
                    return {
                        'title': page.get('title', ''),
                        'extract': page.get('extract', ''),
                        'url': page.get('fullurl', '')
                    }
            
            return None
            
        except Exception as e:
            logging.warning(f"Failed to get page content for {title}: {e}")
            return None
    
    def extract_interaction_patterns(self, content: str, tradition_name: str) -> List[str]:
        """Extract interaction patterns from Wikipedia content"""
        if not content:
            return []
        
        patterns = []
        content_lower = content.lower()
        
        # Look for communication and interaction keywords
        interaction_keywords = {
            'teaching': 'teaches through guidance and instruction',
            'meditation': 'encourages contemplative and mindful approaches',
            'ritual': 'emphasizes ceremonial and structured practices',
            'community': 'values collective wisdom and shared experience',
            'individual': 'focuses on personal development and self-discovery',
            'oral tradition': 'shares wisdom through storytelling and spoken teaching',
            'written': 'communicates through texts and documented knowledge',
            'mystical': 'speaks from transcendent and spiritual perspectives',
            'practical': 'emphasizes applicable and concrete guidance',
            'philosophical': 'engages in deep reasoning and logical discourse',
            'intuitive': 'trusts inner knowing and felt sense',
            'scholarly': 'draws from extensive study and research',
            'experiential': 'learns through direct practice and experience'
        }
        
        # Extract patterns based on content
        for keyword, pattern in interaction_keywords.items():
            if keyword in content_lower:
                patterns.append(pattern)
        
        # Add tradition-specific patterns
        tradition_patterns = self._get_tradition_specific_patterns(tradition_name, content_lower)
        patterns.extend(tradition_patterns)
        
        return patterns[:8]  # Limit to 8 most relevant patterns
    
    def _get_tradition_specific_patterns(self, tradition_name: str, content: str) -> List[str]:
        """Get tradition-specific interaction patterns"""
        patterns = []
        
        tradition_specific = {
            'celtic_druidic': [
                'speaks with seasonal wisdom and natural metaphors',
                'bridges seen and unseen realms in communication',
                'honors the sacred in everyday interactions'
            ],
            'chaos_magic': [
                'adapts communication style to achieve desired outcomes',
                'challenges conventional thinking patterns',
                'focuses on practical effectiveness over tradition'
            ],
            'sufi_mysticism': [
                'speaks from the heart with poetic expression',
                'emphasizes love and unity in all interactions',
                'uses music and movement to convey wisdom'
            ],
            'taoism': [
                'speaks simply and naturally without forcing',
                'suggests rather than commands or insists',
                'embodies wu wei in communication style'
            ]
        }
        
        if tradition_name in tradition_specific:
            patterns.extend(tradition_specific[tradition_name])
        
        return patterns

class EnhancedPersonalitySeedsGenerator:
    """Main generator class for enhanced personality seeds"""
    
    def __init__(self, archives_dir: str = "knowledge_base/archives/governor_archives", seeds_dir: str = "personality_seeds"):
        self.archives_dir = Path(archives_dir)
        self.seeds_dir = Path(seeds_dir)
        self.wiki_api = WikipediaEnhancedAPI()
        self.logger = logging.getLogger("EnhancedSeedsGenerator")
        
        # Ensure directories exist
        self.seeds_dir.mkdir(exist_ok=True)
        
        # Progress tracking
        self.processed_count = 0
        self.total_count = 0
        self.enhanced_seeds = []
    
    def load_governor_archive(self, archive_file: Path) -> Optional[Dict[str, Any]]:
        """Load a governor archive file"""
        try:
            with open(archive_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load archive {archive_file}: {e}")
            return None
    
    def extract_wisdom_approaches(self, archive_data: Dict[str, Any]) -> List[str]:
        """Extract wisdom approaches from archive data"""
        approaches = []
        
        # Extract from wisdom teachings
        wisdom_teachings = archive_data.get('wisdom_teachings', [])
        for teaching in wisdom_teachings[:5]:  # Limit to 5
            if isinstance(teaching, str) and len(teaching) > 10:
                # Extract the core approach from the teaching
                if 'through' in teaching.lower():
                    approach = teaching.lower().split('through')[1].strip()
                    if len(approach) < 50:  # Keep it concise
                        approaches.append(f"teaches through {approach}")
                elif 'by' in teaching.lower():
                    approach = teaching.lower().split('by')[1].strip()
                    if len(approach) < 50:
                        approaches.append(f"guides by {approach}")
        
        # Extract from decision frameworks
        frameworks = archive_data.get('decision_frameworks', [])
        for framework in frameworks[:3]:  # Limit to 3
            if isinstance(framework, str) and '?' in framework:
                # Convert question to approach
                approach = framework.replace('?', '').lower().strip()
                if 'how' in approach:
                    approaches.append(f"considers {approach.replace('how', 'ways that')}")
                elif 'what' in approach:
                    approaches.append(f"examines {approach.replace('what', 'the nature of')}")
        
        return approaches[:6]  # Limit to 6 approaches
    
    def extract_decision_patterns(self, archive_data: Dict[str, Any]) -> List[str]:
        """Extract decision-making patterns from archive data"""
        patterns = []
        
        # Extract from ethical principles
        ethical_principles = archive_data.get('ethical_principles', [])
        for principle in ethical_principles[:4]:  # Limit to 4
            if isinstance(principle, str):
                # Convert principle to decision pattern
                if 'must' in principle.lower():
                    pattern = principle.lower().replace('must', 'ensures decisions').strip()
                    patterns.append(pattern)
                elif 'should' in principle.lower():
                    pattern = principle.lower().replace('should', 'seeks to').strip()
                    patterns.append(pattern)
                else:
                    patterns.append(f"considers {principle.lower()}")
        
        # Extract from key concepts
        key_concepts = archive_data.get('key_concepts', [])
        for concept in key_concepts[:3]:  # Limit to 3
            if isinstance(concept, dict) and 'core_principle' in concept:
                principle = concept['core_principle']
                patterns.append(f"applies {principle.lower()} in decision-making")
        
        return patterns[:5]  # Limit to 5 patterns
    
    def generate_enhanced_seed(self, archive_file: Path) -> Optional[EnhancedPersonalitySeed]:
        """Generate an enhanced personality seed from archive data and Wikipedia"""
        self.logger.info(f"🔄 Processing: {archive_file.name}")
        
        # Load archive data
        archive_data = self.load_governor_archive(archive_file)
        if not archive_data:
            return None
        
        tradition_name = archive_data.get('tradition_name', '')
        display_name = archive_data.get('display_name', '')
        
        print(f"   📚 Tradition: {display_name}")
        
        # Get Wikipedia content for enhanced interaction patterns
        wiki_data = None
        wiki_insights = []
        
        # Try different search terms for better Wikipedia matches
        search_terms = [
            display_name,
            tradition_name.replace('_', ' '),
            f"{display_name} tradition",
            f"{display_name} mysticism"
        ]
        
        for search_term in search_terms:
            wiki_data = self.wiki_api.search_tradition(search_term, "mysticism tradition")
            if wiki_data and wiki_data.get('extract'):
                print(f"   🌐 Found Wikipedia content for: {search_term}")
                break
            time.sleep(0.5)  # Small delay between searches
        
        # Extract Wikipedia insights
        if wiki_data and wiki_data.get('extract'):
            extract = wiki_data['extract']
            wiki_insights = self.wiki_api.extract_interaction_patterns(extract, tradition_name)
            print(f"   💡 Extracted {len(wiki_insights)} Wikipedia insights")
        else:
            print(f"   ⚠️  No Wikipedia content found")
        
        # Extract data from archive
        personality_traits = archive_data.get('personality_traits', [])
        
        # Get existing interaction patterns and enhance them
        existing_patterns = archive_data.get('interaction_patterns', [])
        communication_styles = archive_data.get('communication_styles', [])
        
        # Combine existing patterns with Wikipedia insights
        enhanced_interaction_patterns = []
        enhanced_interaction_patterns.extend(existing_patterns)
        enhanced_interaction_patterns.extend(wiki_insights)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_patterns = []
        for pattern in enhanced_interaction_patterns:
            if pattern.lower() not in seen:
                seen.add(pattern.lower())
                unique_patterns.append(pattern)
        
        # Extract wisdom approaches and decision patterns
        wisdom_approaches = self.extract_wisdom_approaches(archive_data)
        decision_patterns = self.extract_decision_patterns(archive_data)
        
        # Get key concepts and wisdom elements
        key_concepts = []
        wisdom_elements = []
        
        concepts = archive_data.get('key_concepts', [])
        for concept in concepts:
            if isinstance(concept, dict):
                key_concepts.append(concept.get('name', ''))
                wisdom_elements.append(concept.get('practical_wisdom', ''))
            elif isinstance(concept, str):
                key_concepts.append(concept)
        
        # Create enhanced seed
        enhanced_seed = EnhancedPersonalitySeed(
            tradition_name=tradition_name,
            display_name=display_name,
            overview=archive_data.get('overview', '')[:400] + "..." if len(archive_data.get('overview', '')) > 400 else archive_data.get('overview', ''),
            personality_traits=personality_traits[:6],  # Limit to 6
            interaction_patterns=unique_patterns[:8],  # Limit to 8
            communication_styles=communication_styles[:5],  # Limit to 5
            wisdom_approaches=wisdom_approaches,
            decision_patterns=decision_patterns,
            key_concepts=key_concepts[:8],  # Limit to 8
            wisdom_elements=wisdom_elements[:6],  # Limit to 6
            wiki_insights=wiki_insights,
            archive_source=archive_file.name,
            quality_rating=archive_data.get('quality_rating', 'ENHANCED')
        )
        
        print(f"   ✅ Enhanced seed created with {len(unique_patterns)} interaction patterns")
        return enhanced_seed
    
    def save_enhanced_seed(self, seed: EnhancedPersonalitySeed) -> bool:
        """Save enhanced seed to JSON file"""
        try:
            # Convert to dictionary for JSON serialization
            seed_dict = {
                'tradition_name': seed.tradition_name,
                'display_name': seed.display_name,
                'overview': seed.overview,
                'personality_traits': seed.personality_traits,
                'interaction_patterns': seed.interaction_patterns,
                'communication_styles': seed.communication_styles,
                'wisdom_approaches': seed.wisdom_approaches,
                'decision_patterns': seed.decision_patterns,
                'key_concepts': seed.key_concepts,
                'wisdom_elements': seed.wisdom_elements,
                'wiki_insights': seed.wiki_insights,
                'archive_source': seed.archive_source,
                'quality_rating': seed.quality_rating,
                'generated_at': datetime.now().isoformat(),
                'enhancement_version': '2.0'
            }
            
            # Save to file
            output_file = self.seeds_dir / f"{seed.tradition_name}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(seed_dict, f, indent=2, ensure_ascii=False)
            
            print(f"   💾 Saved: {output_file.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save seed for {seed.tradition_name}: {e}")
            return False
    
    def process_all_archives(self) -> Dict[str, Any]:
        """Process all governor archives to generate enhanced personality seeds"""
        print("🚀 Enhanced Personality Seeds Generator Starting...")
        print("=" * 60)
        
        # Find all archive files
        archive_files = list(self.archives_dir.glob("*.json"))
        self.total_count = len(archive_files)
        
        if not archive_files:
            print("❌ No archive files found in governor_archives directory")
            return {'success': False, 'message': 'No archive files found'}
        
        print(f"📁 Found {self.total_count} archive files to process")
        print()
        
        # Process each archive
        successful_count = 0
        failed_count = 0
        
        for archive_file in archive_files:
            try:
                # Generate enhanced seed
                enhanced_seed = self.generate_enhanced_seed(archive_file)
                
                if enhanced_seed:
                    # Save the enhanced seed
                    if self.save_enhanced_seed(enhanced_seed):
                        successful_count += 1
                        self.enhanced_seeds.append(enhanced_seed)
                    else:
                        failed_count += 1
                else:
                    failed_count += 1
                    print(f"   ❌ Failed to generate seed for {archive_file.name}")
                
                self.processed_count += 1
                
                # Progress update
                progress = (self.processed_count / self.total_count) * 100
                print(f"   📊 Progress: {progress:.1f}% ({self.processed_count}/{self.total_count})")
                print()
                
                # Small delay to avoid overwhelming APIs
                time.sleep(1)
                
            except Exception as e:
                failed_count += 1
                self.logger.error(f"Error processing {archive_file.name}: {e}")
                print(f"   ❌ Error: {e}")
                print()
        
        # Generate summary
        summary = {
            'success': True,
            'total_processed': self.processed_count,
            'successful': successful_count,
            'failed': failed_count,
            'enhancement_rate': (successful_count / self.total_count) * 100 if self.total_count > 0 else 0,
            'generated_at': datetime.now().isoformat()
        }
        
        print("=" * 60)
        print("📈 Enhancement Summary:")
        print(f"   ✅ Successfully enhanced: {successful_count}")
        print(f"   ❌ Failed: {failed_count}")
        print(f"   📊 Success rate: {summary['enhancement_rate']:.1f}%")
        print()
        
        return summary

def main():
    """Main execution function"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create generator
    generator = EnhancedPersonalitySeedsGenerator()
    
    # Process all archives
    summary = generator.process_all_archives()
    
    # Save summary report
    summary_file = Path("enhanced_seeds_generation_report.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Summary report saved to: {summary_file}")
    print("🎉 Enhanced personality seeds generation complete!")

if __name__ == "__main__":
    main() 