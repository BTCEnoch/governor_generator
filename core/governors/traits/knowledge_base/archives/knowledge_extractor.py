#!/usr/bin/env python3
"""
Knowledge Archive Extractor
Processes research JSON files to extract summaries, key concepts, and personality-relevant data
Uses Wikipedia API for authentic content retrieval
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
class ConceptSummary:
    """Core concept extracted from a mystical tradition"""
    name: str
    description: str
    practical_application: str
    personality_relevance: str
    source_quality: str
    tradition: str
    wiki_extract: Optional[str] = None
    wiki_url: Optional[str] = None

@dataclass
class TraditionArchive:
    """Complete archive for a mystical tradition"""
    tradition_name: str
    display_name: str
    overview: str
    wiki_summary: Optional[str]
    core_concepts: List[ConceptSummary]
    practical_applications: List[str]
    personality_traits: List[str]
    interaction_patterns: List[str]
    key_terminology: Dict[str, str]
    source_count: int
    quality_rating: str
    extraction_timestamp: str

class WikipediaAPI:
    """Helper class for Wikipedia API interactions"""
    
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/api/rest_v1"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Governor-Generator-Knowledge-Extractor/1.0 (Educational/Research)'
        })
        self.rate_limit_delay = 1  # 1 second between requests
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Ensure we don't exceed rate limits"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()
    
    def search_articles(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for Wikipedia articles"""
        self._rate_limit()
        
        search_url = f"{self.base_url}/page/search/{quote(query)}"
        params = {'limit': limit}
        
        try:
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get('pages', [])
        except Exception as e:
            logging.warning(f"Wikipedia search failed for '{query}': {e}")
            return []
    
    def get_page_summary(self, title: str) -> Optional[Dict]:
        """Get page summary from Wikipedia"""
        self._rate_limit()
        
        summary_url = f"{self.base_url}/page/summary/{quote(title)}"
        
        try:
            response = self.session.get(summary_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.warning(f"Failed to get summary for '{title}': {e}")
            return None
    
    def get_best_match(self, concept: str, tradition_context: str = "") -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Get the best Wikipedia match for a concept"""
        # Try different search variations
        search_terms = [
            f"{concept} {tradition_context}".strip(),
            concept,
            f"{concept} mysticism",
            f"{concept} spirituality"
        ]
        
        for search_term in search_terms:
            articles = self.search_articles(search_term, limit=3)
            if articles:
                # Get summary of the first/best match
                best_article = articles[0]
                summary = self.get_page_summary(best_article['title'])
                if summary:
                    return (
                        summary.get('extract', ''),
                        summary.get('content_urls', {}).get('desktop', {}).get('page', ''),
                        best_article['title']
                    )
        
        return None, None, None

class KnowledgeExtractor:
    """Extracts and archives knowledge from research JSON files"""
    
    def __init__(self, links_dir: str = "knowledge_base/links", 
                 archive_dir: str = "knowledge_base/archives"):
        self.links_dir = Path(links_dir)
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Create only essential directories for streamlined approach
        (self.archive_dir / "governor_archives").mkdir(exist_ok=True)
        (self.archive_dir / "personality_seeds").mkdir(exist_ok=True)
        
        self.wiki_api = WikipediaAPI()
        self.logger = logging.getLogger("KnowledgeExtractor")
        self.logger.info("🏛️ Knowledge Archive Extractor initialized with Wikipedia API")
    
    def extract_tradition_overview(self, tradition_data: Dict) -> Tuple[str, Optional[str]]:
        """Extract high-level overview of the tradition using Wikipedia"""
        display_name = tradition_data.get('display_name', '')
        tradition_name = tradition_data.get('tradition_name', '')
        
        self.logger.info(f"🔍 Extracting overview for {display_name}")
        
        # Get Wikipedia summary for the tradition
        wiki_extract, wiki_url, wiki_title = self.wiki_api.get_best_match(
            display_name, "mysticism spirituality"
        )
        
        if wiki_extract:
            # Use Wikipedia content as primary overview
            overview = wiki_extract[:500] + "..." if len(wiki_extract) > 500 else wiki_extract
        else:
            # Fallback to pattern-based overview
            overview = f"{display_name} is a mystical tradition that encompasses "
            search_queries = tradition_data.get('search_queries_used', [])
            key_themes = self._extract_themes_from_queries(search_queries)
            
            if key_themes:
                overview += f"concepts such as {', '.join(key_themes[:3])}. "
            
            overview += f"This tradition offers practical wisdom for personal development and spiritual growth."
        
        return overview, wiki_extract
    
    def _extract_themes_from_queries(self, queries: List[str]) -> List[str]:
        """Extract key themes from search queries"""
        themes = []
        for query in queries:
            # Extract quoted concepts
            quoted_matches = re.findall(r'"([^"]+)"', query)
            for match in quoted_matches:
                # Clean up the theme
                theme = match.replace('+', ' ').replace('_', ' ').title()
                if theme not in themes and len(theme) < 50:
                    themes.append(theme)
        return themes[:10]  # Limit to top 10 themes
    
    def extract_core_concepts(self, tradition_data: Dict) -> List[ConceptSummary]:
        """Extract core concepts from tradition data using Wikipedia"""
        concepts = []
        themes = self._extract_themes_from_queries(tradition_data.get('search_queries_used', []))
        tradition_name = tradition_data.get('tradition_name', '')
        display_name = tradition_data.get('display_name', '')
        
        self.logger.info(f"🧠 Extracting {len(themes[:5])} core concepts for {display_name}")
        
        # Create concept summaries from themes using Wikipedia
        for i, theme in enumerate(themes[:5]):  # Limit to top 5 concepts
            self.logger.info(f"  📖 Processing concept {i+1}/5: {theme}")
            
            # Get Wikipedia information for this concept
            wiki_extract, wiki_url, wiki_title = self.wiki_api.get_best_match(
                theme, display_name
            )
            
            concept = ConceptSummary(
                name=theme,
                description=self._create_concept_description(theme, wiki_extract, tradition_name),
                practical_application=self._generate_practical_application(theme, wiki_extract),
                personality_relevance=self._generate_personality_relevance(theme, tradition_name),
                source_quality=tradition_data.get('research_quality', 'GOOD'),
                tradition=tradition_name,
                wiki_extract=wiki_extract,
                wiki_url=wiki_url
            )
            concepts.append(concept)
        
        return concepts
    
    def _create_concept_description(self, concept: str, wiki_extract: Optional[str], tradition: str) -> str:
        """Create description using Wikipedia content when available"""
        if wiki_extract and len(wiki_extract) > 50:
            # Use first 2-3 sentences from Wikipedia
            sentences = wiki_extract.split('. ')
            if len(sentences) >= 2:
                return '. '.join(sentences[:2]) + '.'
            else:
                return sentences[0] if sentences else wiki_extract[:200]
        else:
            # Fallback to pattern-based description
            return self._generate_concept_description(concept, tradition)
    
    def _generate_concept_description(self, concept: str, tradition: str) -> str:
        """Generate description for a concept based on tradition context"""
        concept_lower = concept.lower()
        
        # Pattern-based descriptions for common mystical concepts
        if 'divine' in concept_lower or 'sacred' in concept_lower:
            return f"A sacred principle in {tradition} representing connection to higher consciousness and spiritual truth."
        elif 'energy' in concept_lower or 'power' in concept_lower or 'force' in concept_lower:
            return f"A fundamental energy concept in {tradition} used for spiritual transformation and practical manifestation."
        elif 'wisdom' in concept_lower or 'knowledge' in concept_lower:
            return f"Core wisdom teaching in {tradition} that provides practical guidance for spiritual development."
        elif 'ritual' in concept_lower or 'practice' in concept_lower:
            return f"A practical method in {tradition} for applying spiritual principles in daily life."
        elif 'balance' in concept_lower or 'harmony' in concept_lower:
            return f"A principle of equilibrium in {tradition} that guides ethical behavior and spiritual growth."
        else:
            return f"A key concept in {tradition} that shapes understanding of spiritual reality and practical application."
    
    def _generate_practical_application(self, concept: str, wiki_extract: Optional[str] = None) -> str:
        """Generate practical application, enhanced by Wikipedia context"""
        concept_lower = concept.lower()
        
        # If we have Wikipedia content, try to extract practical elements
        if wiki_extract:
            wiki_lower = wiki_extract.lower()
            if any(word in wiki_lower for word in ['practice', 'used', 'applied', 'method', 'technique']):
                # Try to extract practical sentences
                sentences = wiki_extract.split('. ')
                for sentence in sentences:
                    if any(word in sentence.lower() for word in ['practice', 'used', 'applied', 'method']):
                        return sentence.strip() + '.'
        
        # Fallback to pattern-based applications
        if 'meditation' in concept_lower or 'contemplation' in concept_lower:
            return "Used for daily spiritual practice, stress reduction, and inner development."
        elif 'divination' in concept_lower or 'oracle' in concept_lower:
            return "Applied for decision-making, gaining insight into situations, and understanding patterns."
        elif 'ritual' in concept_lower or 'ceremony' in concept_lower:
            return "Practiced for marking important transitions, creating sacred space, and focusing intention."
        elif 'healing' in concept_lower or 'therapy' in concept_lower:
            return "Utilized for physical, emotional, and spiritual wellness and transformation."
        elif 'protection' in concept_lower or 'defense' in concept_lower:
            return "Employed for creating boundaries, maintaining energetic integrity, and ensuring safety."
        else:
            return "Integrated into daily spiritual practice for personal growth and practical wisdom."
    
    def _generate_personality_relevance(self, concept: str, tradition: str) -> str:
        """Generate personality relevance for AI interaction"""
        concept_lower = concept.lower()
        
        if 'wisdom' in concept_lower or 'knowledge' in concept_lower:
            return "Provides depth and insight in conversations, offering thoughtful perspectives on complex topics."
        elif 'compassion' in concept_lower or 'love' in concept_lower:
            return "Enhances empathetic responses and creates supportive, understanding interactions."
        elif 'balance' in concept_lower or 'harmony' in concept_lower:
            return "Promotes balanced viewpoints and helps navigate conflicting perspectives diplomatically."
        elif 'mystery' in concept_lower or 'secret' in concept_lower:
            return "Adds intrigue and depth to interactions, encouraging curiosity and deeper exploration."
        elif 'power' in concept_lower or 'strength' in concept_lower:
            return "Contributes confidence and authority in guidance while maintaining humility."
        else:
            return "Enriches personality with authentic spiritual wisdom and practical life guidance."
    
    def extract_personality_traits(self, tradition_data: Dict, concepts: List[ConceptSummary]) -> List[str]:
        """Extract personality traits that could be used for AI character development"""
        traits = []
        display_name = tradition_data.get('display_name', '')
        
        # Map traditions to personality characteristics
        tradition_traits = {
            'celtic_druidic': ['nature-connected', 'intuitive', 'cyclical-thinking', 'earth-grounded'],
            'chaos_magic': ['adaptable', 'results-oriented', 'paradigm-flexible', 'experimental'],
            'classical_philosophy': ['logical', 'ethical', 'contemplative', 'systematic'],
            'egyptian_magic': ['structured', 'ceremonial', 'cosmic-aware', 'transformative'],
            'gnostic_traditions': ['seeking', 'transcendent', 'mystical', 'knowledge-focused'],
            'golden_dawn': ['scholarly', 'ceremonial', 'hierarchical', 'synthesizing'],
            'i_ching': ['pattern-aware', 'cyclical', 'balanced', 'oracular'],
            'kuji_kiri': ['disciplined', 'protective', 'energy-focused', 'practical'],
            'norse_traditions': ['honorable', 'fate-aware', 'ancestral', 'courage-focused'],
            'sacred_geometry': ['pattern-conscious', 'mathematical', 'harmonic', 'universal'],
            'sufi_mysticism': ['devotional', 'heart-centered', 'ecstatic', 'unity-seeking'],
            'taoism': ['flowing', 'natural', 'effortless', 'balanced'],
            'tarot_knowledge': ['symbolic', 'intuitive', 'archetypal', 'guidance-oriented'],
            'thelema': ['will-focused', 'individualistic', 'magical', 'self-discovering']
        }
        
        tradition_name = tradition_data.get('tradition_name', '')
        if tradition_name in tradition_traits:
            traits.extend(tradition_traits[tradition_name])
        
        # Add traits based on concepts
        for concept in concepts:
            if 'wisdom' in concept.name.lower():
                traits.append('wise')
            elif 'power' in concept.name.lower():
                traits.append('empowered')
            elif 'love' in concept.name.lower():
                traits.append('compassionate')
        
        return list(set(traits))  # Remove duplicates
    
    def extract_interaction_patterns(self, tradition_data: Dict) -> List[str]:
        """Extract interaction patterns for AI personality"""
        patterns = []
        tradition_name = tradition_data.get('tradition_name', '')
        
        # Map traditions to interaction styles
        interaction_styles = {
            'sufi_mysticism': ['speaks from the heart', 'uses poetic language', 'emphasizes love and unity'],
            'taoism': ['speaks simply and naturally', 'avoids forcing answers', 'suggests rather than commands'],
            'classical_philosophy': ['asks probing questions', 'uses logical reasoning', 'provides structured responses'],
            'chaos_magic': ['adapts communication style', 'focuses on practical results', 'challenges assumptions'],
            'golden_dawn': ['provides detailed explanations', 'uses formal language', 'references multiple sources'],
            'norse_traditions': ['speaks directly and honestly', 'emphasizes honor and integrity', 'values courage'],
            'tarot_knowledge': ['speaks in symbols and metaphors', 'asks reflective questions', 'guides self-discovery']
        }
        
        if tradition_name in interaction_styles:
            patterns.extend(interaction_styles[tradition_name])
        
        return patterns
    
    def process_tradition(self, json_file: Path) -> TraditionArchive:
        """Process a single tradition JSON file into an archive"""
        self.logger.info(f"🏛️ Processing tradition file: {json_file.name}")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            tradition_data = json.load(f)
        
        # Extract overview with Wikipedia content
        overview, wiki_summary = self.extract_tradition_overview(tradition_data)
        
        # Extract core concepts using Wikipedia
        core_concepts = self.extract_core_concepts(tradition_data)
        
        # Extract personality-relevant information
        personality_traits = self.extract_personality_traits(tradition_data, core_concepts)
        interaction_patterns = self.extract_interaction_patterns(tradition_data)
        
        # Generate practical applications list
        practical_applications = [concept.practical_application for concept in core_concepts]
        
        # Generate key terminology from concepts
        key_terminology = {concept.name: concept.description[:100] + "..." 
                          for concept in core_concepts}
        
        # Create archive
        archive = TraditionArchive(
            tradition_name=tradition_data.get('tradition_name', ''),
            display_name=tradition_data.get('display_name', ''),
            overview=overview,
            wiki_summary=wiki_summary,
            core_concepts=core_concepts,
            practical_applications=practical_applications,
            personality_traits=personality_traits,
            interaction_patterns=interaction_patterns,
            key_terminology=key_terminology,
            source_count=tradition_data.get('source_count', 0),
            quality_rating=tradition_data.get('research_quality', 'UNKNOWN'),
            extraction_timestamp=datetime.now().isoformat()
        )
        
        return archive
    
    def save_archive(self, archive: TraditionArchive) -> None:
        """Save tradition archive to streamlined locations"""
        tradition_name = archive.tradition_name
        
        # Save complete archive to governor_archives
        archive_file = self.archive_dir / "governor_archives" / f"{tradition_name}_governor_archive.json"
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(archive), f, indent=2, ensure_ascii=False)
        
        # Save personality seed (essential for Governor development)
        personality_seed = {
            'tradition': archive.display_name,
            'overview': archive.overview[:300] + "..." if len(archive.overview) > 300 else archive.overview,
            'traits': archive.personality_traits,
            'interaction_patterns': archive.interaction_patterns,
            'key_concepts': [concept.name for concept in archive.core_concepts],
            'wisdom_elements': [concept.personality_relevance for concept in archive.core_concepts]
        }
        
        personality_file = self.archive_dir / "personality_seeds" / f"{tradition_name}_seed.json"
        with open(personality_file, 'w', encoding='utf-8') as f:
            json.dump(personality_seed, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"✅ Saved archive for {archive.display_name}")
    
    def process_batch(self, tradition_files: List[str]) -> List[TraditionArchive]:
        """Process a batch of tradition files"""
        archives = []
        
        for filename in tradition_files:
            file_path = self.links_dir / filename
            if file_path.exists():
                try:
                    archive = self.process_tradition(file_path)
                    self.save_archive(archive)
                    archives.append(archive)
                except Exception as e:
                    self.logger.error(f"❌ Failed to process {filename}: {e}")
            else:
                self.logger.warning(f"⚠️ File not found: {filename}")
        
        return archives 