"""
Knowledge mapper for connecting governor traits with their knowledge base entries.
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

from .loader import TraitLoader
from .schemas.trait_schemas import GovernorTraits, ElementType

logger = logging.getLogger(__name__)

@dataclass
class TraditionKnowledge:
    """Knowledge from a specific mystical tradition"""
    tradition_name: str
    core_concepts: List[str]
    practices: List[str]
    correspondences: Dict[str, List[str]]
    historical_context: str
    modern_applications: List[str]
    last_updated: float = time.time()  # For cache invalidation

    def validate(self) -> bool:
        """Validate tradition knowledge structure"""
        try:
            if not self.tradition_name or not isinstance(self.tradition_name, str):
                return False
            if not isinstance(self.core_concepts, list) or not all(isinstance(c, str) for c in self.core_concepts):
                return False
            if not isinstance(self.practices, list) or not all(isinstance(p, str) for p in self.practices):
                return False
            if not isinstance(self.correspondences, dict):
                return False
            for key, values in self.correspondences.items():
                if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
                    return False
            if not isinstance(self.historical_context, str):
                return False
            if not isinstance(self.modern_applications, list) or not all(isinstance(a, str) for a in self.modern_applications):
                return False
            return True
        except Exception as e:
            logger.error(f"Tradition validation error: {e}")
            return False

@dataclass
class GovernorKnowledge:
    """Complete knowledge profile for a governor"""
    governor_id: str
    primary_tradition: TraditionKnowledge
    secondary_traditions: List[TraditionKnowledge]
    specialized_domains: List[str]
    teaching_methods: List[str]
    ritual_practices: List[str]
    mystical_correspondences: Dict[str, List[str]]
    last_updated: float = time.time()  # For cache invalidation

    def validate(self) -> bool:
        """Validate governor knowledge structure"""
        try:
            if not self.governor_id or not isinstance(self.governor_id, str):
                return False
            if not isinstance(self.primary_tradition, TraditionKnowledge) or not self.primary_tradition.validate():
                return False
            if not isinstance(self.secondary_traditions, list):
                return False
            for tradition in self.secondary_traditions:
                if not isinstance(tradition, TraditionKnowledge) or not tradition.validate():
                    return False
            if not isinstance(self.specialized_domains, list) or not all(isinstance(d, str) for d in self.specialized_domains):
                return False
            if not isinstance(self.teaching_methods, list) or not all(isinstance(m, str) for m in self.teaching_methods):
                return False
            if not isinstance(self.ritual_practices, list) or not all(isinstance(p, str) for p in self.ritual_practices):
                return False
            if not isinstance(self.mystical_correspondences, dict):
                return False
            for key, values in self.mystical_correspondences.items():
                if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
                    return False
            return True
        except Exception as e:
            logger.error(f"Governor knowledge validation error: {e}")
            return False

class KnowledgeMapper:
    """Maps governor traits to their knowledge base entries"""
    
    # Cache invalidation time (1 hour)
    CACHE_TTL = 3600
    
    def __init__(self, data_root: Path = Path("data")):
        """Initialize the knowledge mapper"""
        self.data_root = data_root
        self.knowledge_root = data_root / "knowledge"
        self.governors_root = data_root / "governors"
        self.trait_loader = TraitLoader(self.governors_root)
        
        # Cache for loaded knowledge
        self._tradition_cache: Dict[str, TraditionKnowledge] = {}
        self._governor_cache: Dict[str, GovernorKnowledge] = {}
        
        # Thread pool for concurrent operations
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    def _is_cache_valid(self, timestamp: float) -> bool:
        """Check if cached data is still valid"""
        return (time.time() - timestamp) < self.CACHE_TTL
    
    def _invalidate_caches(self):
        """Invalidate expired cache entries"""
        current_time = time.time()
        
        # Clean tradition cache
        expired_traditions = [
            name for name, knowledge in self._tradition_cache.items()
            if not self._is_cache_valid(knowledge.last_updated)
        ]
        for name in expired_traditions:
            del self._tradition_cache[name]
            
        # Clean governor cache
        expired_governors = [
            gov_id for gov_id, knowledge in self._governor_cache.items()
            if not self._is_cache_valid(knowledge.last_updated)
        ]
        for gov_id in expired_governors:
            del self._governor_cache[gov_id]
    
    def map_governor_knowledge(self, governor_id: str, governor_number: int) -> Optional[GovernorKnowledge]:
        """Map a governor's traits to their complete knowledge profile"""
        try:
            # Invalidate old cache entries
            self._invalidate_caches()
            
            # Check cache first
            if governor_id in self._governor_cache:
                cached = self._governor_cache[governor_id]
                if self._is_cache_valid(cached.last_updated):
                    return cached
            
            # Load governor traits
            traits = self.trait_loader.load_all_traits(governor_id, governor_number)
            if not traits:
                logger.error(f"Failed to load traits for {governor_id}")
                return None
            
            # Determine primary tradition from canonical traits
            primary_tradition = self._load_tradition_knowledge(traits.canonical.domain)
            if not primary_tradition:
                logger.error(f"Failed to load primary tradition for {governor_id}")
                return None
            
            # Load secondary traditions based on mystical traits
            secondary_traditions = []
            # Get traditions from mystical correspondences
            mystical_traditions = self._get_mystical_traditions(traits)
            
            # Load secondary traditions concurrently
            future_to_tradition = {
                self._executor.submit(self._load_tradition_knowledge, tradition): tradition
                for tradition in mystical_traditions
            }
            
            for future in future_to_tradition:
                try:
                    knowledge = future.result()
                    if knowledge:
                        secondary_traditions.append(knowledge)
                except Exception as e:
                    logger.warning(f"Failed to load secondary tradition: {e}")
            
            # Create governor knowledge profile
            knowledge = GovernorKnowledge(
                governor_id=governor_id,
                primary_tradition=primary_tradition,
                secondary_traditions=secondary_traditions,
                specialized_domains=self._extract_specialized_domains(traits),
                teaching_methods=self._extract_teaching_methods(traits),
                ritual_practices=self._extract_ritual_practices(traits),
                mystical_correspondences=self._extract_correspondences(traits)
            )
            
            # Validate before caching
            if not knowledge.validate():
                logger.error(f"Invalid knowledge profile for {governor_id}")
                return None
            
            # Cache the result
            self._governor_cache[governor_id] = knowledge
            return knowledge
            
        except Exception as e:
            logger.error(f"Error mapping knowledge for {governor_id}: {e}")
            return None
    
    def _get_mystical_traditions(self, traits: GovernorTraits) -> Set[str]:
        """Extract tradition names from mystical traits"""
        traditions = set()
        
        try:
            # Add traditions based on zodiac
            if traits.mystical.zodiac:
                traditions.add("Astrology")
                
            # Add traditions based on tarot
            if traits.mystical.tarot:
                traditions.add("Tarot")
                
            # Add traditions based on sephirot
            if traits.mystical.sephirot:
                traditions.add("Kabbalah")
                
            # Add traditions based on angel
            if traits.mystical.angel:
                traditions.add("Angelology")
                
            # Add traditions based on element
            if traits.mystical.element:
                traditions.add("Elemental_Magic")
                
            return traditions
            
        except Exception as e:
            logger.error(f"Error extracting mystical traditions: {e}")
            return set()
    
    def _load_tradition_knowledge(self, tradition_name: str) -> Optional[TraditionKnowledge]:
        """Load knowledge for a specific tradition"""
        try:
            # Check cache first
            if tradition_name in self._tradition_cache:
                cached = self._tradition_cache[tradition_name]
                if self._is_cache_valid(cached.last_updated):
                    return cached
            
            # Load tradition archive
            archive_path = self.knowledge_root / "archives" / "governor_archives" / f"{tradition_name.lower()}_governor_archive.json"
            if not archive_path.exists():
                logger.error(f"No archive found for tradition: {tradition_name}")
                return None
            
            with open(archive_path) as f:
                data = json.load(f)
                
            # Create tradition knowledge
            knowledge = TraditionKnowledge(
                tradition_name=tradition_name,
                core_concepts=data.get("core_concepts", []),
                practices=data.get("practices", []),
                correspondences=data.get("correspondences", {}),
                historical_context=data.get("historical_context", ""),
                modern_applications=data.get("modern_applications", [])
            )
            
            # Validate before caching
            if not knowledge.validate():
                logger.error(f"Invalid tradition knowledge for {tradition_name}")
                return None
            
            # Cache the result
            self._tradition_cache[tradition_name] = knowledge
            return knowledge
            
        except Exception as e:
            logger.error(f"Error loading tradition knowledge for {tradition_name}: {e}")
            return None
    
    def _extract_specialized_domains(self, traits: GovernorTraits) -> List[str]:
        """Extract specialized domains from traits"""
        try:
            domains = set()
            
            # Add canonical domain
            if traits.canonical.domain:
                domains.add(traits.canonical.domain)
            
            # Add domains from enhanced traits
            for trait_name, trait_data in traits.enhanced.items():
                if isinstance(trait_data.correspondences, dict):
                    domain_list = trait_data.correspondences.get("domain", [])
                    if isinstance(domain_list, list):
                        domains.update(domain_list)
            
            # Add domains from mystical traits
            if traits.mystical.sephirot:
                domains.add(f"Sephirot: {traits.mystical.sephirot}")
            
            return list(domains)
            
        except Exception as e:
            logger.error(f"Error extracting specialized domains: {e}")
            return []
    
    def _extract_teaching_methods(self, traits: GovernorTraits) -> List[str]:
        """Extract teaching methods from traits"""
        try:
            methods = set()
            
            # Add personality-based methods
            if traits.personality.teaching_style:
                methods.add(traits.personality.teaching_style)
            
            # Add approach-based methods
            if traits.personality.approach:
                methods.add(traits.personality.approach)
            
            # Add methods from enhanced traits
            for trait_name, trait_data in traits.enhanced.items():
                if isinstance(trait_data.practical_application, str):
                    if "teaching" in trait_data.practical_application.lower():
                        methods.add(trait_data.practical_application)
            
            return list(methods)
            
        except Exception as e:
            logger.error(f"Error extracting teaching methods: {e}")
            return []
    
    def _extract_ritual_practices(self, traits: GovernorTraits) -> List[str]:
        """Extract ritual practices from traits"""
        try:
            practices = set()
            
            # Add element-based practices
            if traits.mystical.element:
                practices.add(f"{traits.mystical.element.value} rituals")
            
            # Add zodiac-based practices
            if traits.mystical.zodiac:
                practices.add(f"{traits.mystical.zodiac} workings")
            
            # Add tarot-based practices
            if traits.mystical.tarot:
                practices.add(f"{traits.mystical.tarot} meditations")
            
            # Add sephirot-based practices
            if traits.mystical.sephirot:
                practices.add(f"{traits.mystical.sephirot} invocations")
            
            # Add angelic practices
            if traits.mystical.angel:
                practices.add(f"{traits.mystical.angel} rituals")
            
            return list(practices)
            
        except Exception as e:
            logger.error(f"Error extracting ritual practices: {e}")
            return []
    
    def _extract_correspondences(self, traits: GovernorTraits) -> Dict[str, List[str]]:
        """Extract all mystical correspondences"""
        try:
            correspondences: Dict[str, Set[str]] = {}
            
            # Add elemental correspondences
            if traits.mystical.element:
                correspondences["elements"] = {traits.mystical.element.value}
            
            # Add zodiacal correspondences
            if traits.mystical.zodiac:
                correspondences["zodiac"] = {traits.mystical.zodiac}
            
            # Add tarot correspondences
            if traits.mystical.tarot:
                correspondences["tarot"] = {traits.mystical.tarot}
            
            # Add sephirotic correspondences
            if traits.mystical.sephirot:
                correspondences["sephirot"] = {traits.mystical.sephirot}
            
            # Add angelic correspondences
            if traits.mystical.angel:
                correspondences["angels"] = {traits.mystical.angel}
            
            # Add numerical correspondences
            if traits.mystical.number:
                correspondences["numbers"] = {str(traits.mystical.number)}
            
            # Add correspondences from enhanced traits
            for trait_name, trait_data in traits.enhanced.items():
                if isinstance(trait_data.correspondences, dict):
                    for key, values in trait_data.correspondences.items():
                        if isinstance(values, list):
                            if key not in correspondences:
                                correspondences[key] = set()
                            correspondences[key].update(values)
            
            # Convert sets to lists
            return {
                key: list(values)
                for key, values in correspondences.items()
            }
            
        except Exception as e:
            logger.error(f"Error extracting correspondences: {e}")
            return {}
    
    def __del__(self):
        """Clean up resources"""
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=True) 