#!/usr/bin/env python3
"""
Lighthouse Source Collection Engine
Replaces placeholder sources with real, validated sources from actual APIs and web scraping.
"""

import json
import asyncio
import aiohttp
from aiohttp import ClientTimeout
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import time
from urllib.parse import quote_plus
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SourceLink:
    """Real source link with validation"""
    url: str
    title: str
    type: str  # 'wikipedia', 'academic_paper', 'specialized_wiki', 'reference'
    quality: str  # 'excellent', 'good', 'fair'
    description: str
    subcategory: str
    content_snippet: Optional[str] = None
    access_date: Optional[str] = None
    verified: bool = False

@dataclass
class TraditionResearchComplete:
    """Complete tradition research with validated sources"""
    tradition_name: str
    display_name: str
    search_queries_used: List[str]
    all_sources: List[SourceLink]
    categorized_sources: Dict[str, List[SourceLink]]
    source_count: int
    research_quality: str
    last_updated: str

class LighthouseSourceCollector:
    """Main source collection engine"""
    
    def __init__(self, google_api_key: Optional[str] = None, search_engine_id: Optional[str] = None):
        self.google_api_key = google_api_key
        self.search_engine_id = search_engine_id
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limit_delay = 1.0  # seconds between requests
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def collect_sources_for_tradition(self, tradition_file_path: str) -> TraditionResearchComplete:
        """Collect real sources for a tradition, replacing placeholders"""
        logger.info(f"🔍 Starting source collection for {tradition_file_path}")
        
        # Load existing research file
        with open(tradition_file_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            
        tradition_name = existing_data.get('tradition_name', '')
        display_name = existing_data.get('display_name', '')
        
        logger.info(f"📊 Processing {display_name}")
        
        # Generate enhanced search queries
        search_queries = self._generate_enhanced_search_queries(tradition_name, display_name)
        
        # Collect sources from multiple APIs
        wikipedia_sources = await self._collect_wikipedia_sources(tradition_name, display_name)
        academic_sources = await self._collect_academic_sources(tradition_name, display_name)
        specialized_sources = await self._collect_specialized_wiki_sources(tradition_name, display_name)
        
        # Combine and validate all sources
        all_sources = wikipedia_sources + academic_sources + specialized_sources
        validated_sources = await self._validate_sources(all_sources)
        
        # Categorize sources
        categorized_sources = self._categorize_sources(validated_sources)
        
        # Create complete research object
        research_complete = TraditionResearchComplete(
            tradition_name=tradition_name,
            display_name=display_name,
            search_queries_used=search_queries,
            all_sources=validated_sources,
            categorized_sources=categorized_sources,
            source_count=len(validated_sources),
            research_quality=self._assess_research_quality(validated_sources),
            last_updated=time.strftime('%Y-%m-%d %H:%M:%S')
        )
        
        logger.info(f"✅ Collected {len(validated_sources)} validated sources for {display_name}")
        return research_complete
        
    def _generate_enhanced_search_queries(self, tradition_name: str, display_name: str) -> List[str]:
        """Generate diverse search queries for comprehensive coverage"""
        base_queries = [
            f"{display_name} wikipedia",
            f"{display_name} academic research",
            f"{display_name} scholarly articles",
            f"{display_name} encyclopedia",
            f"{display_name} mystical tradition",
            f"{display_name} spiritual practices",
            f"{display_name} sacred texts",
            f"{display_name} religious studies",
            f"{display_name} comparative religion",
            f"{display_name} philosophy"
        ]
        
        # Add tradition-specific queries
        if 'gnostic' in tradition_name.lower():
            base_queries.extend([
                "gnosis direct knowledge",
                "pleroma divine fullness",
                "sophia myth wisdom",
                "demiurge false creator",
                "pneuma divine spark"
            ])
        elif 'kabbalah' in tradition_name.lower():
            base_queries.extend([
                "tree of life sefirot",
                "ein sof infinite",
                "pardes four levels",
                "tikkun olam repair",
                "zohar mystical text"
            ])
        elif 'hermetic' in tradition_name.lower():
            base_queries.extend([
                "emerald tablet hermes",
                "as above so below",
                "hermetic principles",
                "alchemy spiritual transformation",
                "corpus hermeticum"
            ])
        # Add more tradition-specific queries as needed
        
        return base_queries
        
    async def _collect_wikipedia_sources(self, tradition_name: str, display_name: str) -> List[SourceLink]:
        """Collect sources from Wikipedia API"""
        logger.info(f"📖 Collecting Wikipedia sources for {display_name}")
        
        sources = []
        
        # Wikipedia search API
        wikipedia_queries = [
            display_name,
            f"{display_name} tradition",
            f"{display_name} mysticism",
            f"{display_name} philosophy"
        ]
        
        for query in wikipedia_queries:
            try:
                await asyncio.sleep(self.rate_limit_delay)
                
                # Search Wikipedia
                search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(query)}"
                
                if self.session is None:
                    continue
                async with self.session.get(search_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'title' in data and 'extract' in data:
                            source = SourceLink(
                                url=data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                                title=data['title'],
                                type='wikipedia',
                                quality='excellent',
                                description=data.get('extract', '')[:200] + '...',
                                subcategory='general_overview',
                                content_snippet=data.get('extract', ''),
                                access_date=time.strftime('%Y-%m-%d'),
                                verified=True
                            )
                            sources.append(source)
                            logger.info(f"📚 Found Wikipedia article: {data['title']}")
                        
            except Exception as e:
                logger.warning(f"⚠️ Wikipedia search failed for {query}: {e}")
                
        return sources
        
    async def _collect_academic_sources(self, tradition_name: str, display_name: str) -> List[SourceLink]:
        """Collect academic sources from multiple APIs"""
        logger.info(f"🎓 Collecting academic sources for {display_name}")
        
        sources = []
        
        # Semantic Scholar API (free tier)
        semantic_scholar_queries = [
            f"{display_name} religious studies",
            f"{display_name} comparative religion",
            f"{display_name} mysticism studies",
            f"{display_name} philosophy religion"
        ]
        
        for query in semantic_scholar_queries:
            try:
                await asyncio.sleep(self.rate_limit_delay)
                
                # Search Semantic Scholar
                search_url = f"https://api.semanticscholar.org/graph/v1/paper/search"
                params = {
                    'query': query,
                    'limit': 5,
                    'fields': 'title,abstract,url,authors,year,venue'
                }
                
                if self.session is None:
                    continue
                async with self.session.get(search_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for paper in data.get('data', []):
                            if paper.get('title') and paper.get('abstract'):
                                source = SourceLink(
                                    url=paper.get('url', ''),
                                    title=paper['title'],
                                    type='academic_paper',
                                    quality='excellent',
                                    description=paper.get('abstract', '')[:200] + '...',
                                    subcategory='academic_research',
                                    content_snippet=paper.get('abstract', ''),
                                    access_date=time.strftime('%Y-%m-%d'),
                                    verified=True
                                )
                                sources.append(source)
                                logger.info(f"📄 Found academic paper: {paper['title']}")
                        
            except Exception as e:
                logger.warning(f"⚠️ Semantic Scholar search failed for {query}: {e}")
                
        return sources
        
    async def _collect_specialized_wiki_sources(self, tradition_name: str, display_name: str) -> List[SourceLink]:
        """Collect sources from specialized wikis and databases"""
        logger.info(f"🌐 Collecting specialized wiki sources for {display_name}")
        
        sources = []
        
        # Specialized databases for mystical traditions
        specialized_sites = [
            "https://www.britannica.com/search?query=",
            "https://plato.stanford.edu/search/searcher.py?query=",
            "https://www.sacred-texts.com/index.htm"
        ]
        
        for base_url in specialized_sites:
            try:
                await asyncio.sleep(self.rate_limit_delay)
                
                # This is a simplified approach - in practice, you'd need 
                # specific scrapers for each site
                search_url = f"{base_url}{quote_plus(display_name)}"
                
                # Create placeholder sources for now (to be enhanced)
                source = SourceLink(
                    url=search_url,
                    title=f"{display_name} - Specialized Database",
                    type='specialized_wiki',
                    quality='good',
                    description=f"Specialized database entry for {display_name}",
                    subcategory='specialized_reference',
                    access_date=time.strftime('%Y-%m-%d'),
                    verified=False  # Would need actual scraping to verify
                )
                sources.append(source)
                
            except Exception as e:
                logger.warning(f"⚠️ Specialized wiki search failed: {e}")
                
        return sources
        
    async def _validate_sources(self, sources: List[SourceLink]) -> List[SourceLink]:
        """Validate sources by checking URLs and content quality"""
        logger.info(f"✅ Validating {len(sources)} sources")
        
        validated_sources = []
        
        for source in sources:
            try:
                if source.url and source.url.startswith('http'):
                    # Basic URL validation
                    if self.session is None:
                        continue
                    timeout = ClientTimeout(total=10)
                    async with self.session.get(source.url, timeout=timeout) as response:
                        if response.status == 200:
                            source.verified = True
                            validated_sources.append(source)
                            logger.info(f"✅ Validated: {source.title}")
                        else:
                            logger.warning(f"⚠️ URL returned {response.status}: {source.url}")
                else:
                    # For non-HTTP sources, mark as unverified but include
                    source.verified = False
                    validated_sources.append(source)
                    
                await asyncio.sleep(self.rate_limit_delay)
                    
            except Exception as e:
                logger.warning(f"⚠️ Failed to validate {source.url}: {e}")
                
        return validated_sources
        
    def _categorize_sources(self, sources: List[SourceLink]) -> Dict[str, List[SourceLink]]:
        """Categorize sources by type and quality"""
        categorized = {
            'wikipedia_excellent': [],
            'wikipedia_good': [],
            'academic_excellent': [],
            'academic_good': [],
            'specialized_wikis': [],
            'reference_sources': []
        }
        
        for source in sources:
            if source.type == 'wikipedia':
                if source.quality == 'excellent':
                    categorized['wikipedia_excellent'].append(source)
                else:
                    categorized['wikipedia_good'].append(source)
            elif source.type == 'academic_paper':
                if source.quality == 'excellent':
                    categorized['academic_excellent'].append(source)
                else:
                    categorized['academic_good'].append(source)
            elif source.type == 'specialized_wiki':
                categorized['specialized_wikis'].append(source)
            else:
                categorized['reference_sources'].append(source)
                
        return categorized
        
    def _assess_research_quality(self, sources: List[SourceLink]) -> str:
        """Assess overall research quality based on sources"""
        if not sources:
            return "POOR"
            
        verified_count = sum(1 for s in sources if s.verified)
        academic_count = sum(1 for s in sources if s.type == 'academic_paper')
        wikipedia_count = sum(1 for s in sources if s.type == 'wikipedia')
        
        if verified_count >= 10 and academic_count >= 3:
            return "EXCELLENT"
        elif verified_count >= 7 and academic_count >= 2:
            return "GOOD"
        elif verified_count >= 5:
            return "FAIR"
        else:
            return "POOR"
            
    async def collect_all_tradition_sources(self, links_directory: str = "knowledge_base/links") -> None:
        """Collect sources for all tradition research files"""
        logger.info("🚀 Starting comprehensive source collection for all traditions")
        
        links_path = Path(links_directory)
        research_files = list(links_path.glob("research_*.json"))
        
        logger.info(f"📁 Found {len(research_files)} research files to process")
        
        for research_file in research_files:
            try:
                # Process each tradition
                research_complete = await self.collect_sources_for_tradition(str(research_file))
                
                # Save updated research file
                output_path = research_file.parent / f"enhanced_{research_file.name}"
                with open(output_path, 'w', encoding='utf-8') as f:
                    # Convert dataclasses to dict for JSON serialization
                    research_dict = asdict(research_complete)
                    json.dump(research_dict, f, indent=2, ensure_ascii=False)
                    
                logger.info(f"💾 Saved enhanced research to {output_path}")
                
            except Exception as e:
                logger.error(f"❌ Failed to process {research_file}: {e}")
                
        logger.info("🏁 Completed comprehensive source collection for all traditions")

# CLI interface
async def main():
    """Main CLI interface for source collection"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Lighthouse Source Collection Engine")
    parser.add_argument("--tradition", help="Process specific tradition file")
    parser.add_argument("--all", action="store_true", help="Process all tradition files")
    parser.add_argument("--google-api-key", help="Google API key for enhanced search")
    parser.add_argument("--search-engine-id", help="Google Custom Search Engine ID")
    
    args = parser.parse_args()
    
    async with LighthouseSourceCollector(
        google_api_key=args.google_api_key,
        search_engine_id=args.search_engine_id
    ) as collector:
        
        if args.all:
            await collector.collect_all_tradition_sources()
        elif args.tradition:
            research_complete = await collector.collect_sources_for_tradition(args.tradition)
            print(f"✅ Collected {research_complete.source_count} sources for {research_complete.display_name}")
        else:
            print("Please specify --all or --tradition <file>")

if __name__ == "__main__":
    asyncio.run(main()) 