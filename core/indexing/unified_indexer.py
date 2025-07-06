"""
Unified Indexer System
Combines all indexing functionality into a single, maintainable system
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class IndexStats:
    """Statistics about the indexed content"""
    total_traditions: int = 0
    total_concepts: int = 0
    total_teachings: int = 0
    total_frameworks: int = 0
    total_personality_traits: int = 0
    total_interaction_patterns: int = 0
    extraction_timestamp: str = ""

@dataclass
class TraditionIndex:
    """Index entry for a mystical tradition"""
    tradition_name: str
    display_name: str
    overview: str
    concept_count: int
    quality_rating: float
    source_count: int
    personality_traits: List[str]
    interaction_patterns: List[str]
    core_concepts: List[str]
    wisdom_teachings: List[str]
    decision_frameworks: List[str]

class UnifiedIndexer:
    """
    Unified indexing system that combines all indexing functionality
    """
    
    def __init__(self, archives_dir: str = "governor_archives"):
        self.archives_dir = Path(archives_dir)
        self.stats = IndexStats()
        self.traditions: Dict[str, TraditionIndex] = {}
        self.personality_traits_index: Dict[str, Set[str]] = {}  # trait -> traditions
        self.interaction_patterns_index: Dict[str, Set[str]] = {}  # pattern -> traditions
        self.concepts_index: Dict[str, Set[str]] = {}  # concept -> traditions
        self.teachings_index: Dict[str, Set[str]] = {}  # teaching -> traditions
        self.frameworks_index: Dict[str, Set[str]] = {}  # framework -> traditions
        
    def create_unified_index(self) -> Dict:
        """
        Create a unified index of all knowledge base content
        
        Returns:
            Dict containing the complete unified index
        """
        logger.info("📇 Creating unified knowledge index...")
        
        # Reset state
        self._reset_state()
        
        # Process all archive files
        self._process_archive_files()
        
        # Compile the complete index
        unified_index = self._compile_index()
        
        # Save the index
        self._save_index(unified_index)
        
        logger.info(f"✅ Unified index created with {self.stats.total_traditions} traditions")
        logger.info(f"📊 Total unique personality traits: {len(self.personality_traits_index)}")
        logger.info(f"💬 Total interaction patterns: {len(self.interaction_patterns_index)}")
        
        return unified_index
        
    def _reset_state(self):
        """Reset all internal state before indexing"""
        self.stats = IndexStats(extraction_timestamp=datetime.now().isoformat())
        self.traditions.clear()
        self.personality_traits_index.clear()
        self.interaction_patterns_index.clear()
        self.concepts_index.clear()
        self.teachings_index.clear()
        self.frameworks_index.clear()
        
    def _process_archive_files(self):
        """Process all archive files in the archives directory"""
        if not self.archives_dir.exists():
            logger.error(f"Archives directory not found: {self.archives_dir}")
            return
            
        for archive_file in self.archives_dir.glob("*_archive.json"):
            try:
                self._process_single_archive(archive_file)
            except Exception as e:
                logger.error(f"⚠️ Failed to process {archive_file}: {e}")
                
    def _process_single_archive(self, archive_file: Path):
        """
        Process a single archive file
        
        Args:
            archive_file: Path to the archive file to process
        """
        logger.info(f"Processing archive: {archive_file}")
        
        with open(archive_file, 'r', encoding='utf-8') as f:
            archive_data = json.load(f)
            
        tradition_name = archive_data['tradition_name']
        
        # Create tradition index entry
        tradition_index = TraditionIndex(
            tradition_name=tradition_name,
            display_name=archive_data['display_name'],
            overview=self._truncate_overview(archive_data['overview']),
            concept_count=len(archive_data['core_concepts']),
            quality_rating=archive_data['quality_rating'],
            source_count=archive_data['source_count'],
            personality_traits=archive_data['personality_traits'],
            interaction_patterns=archive_data['interaction_patterns'],
            core_concepts=archive_data['core_concepts'],
            wisdom_teachings=archive_data.get('wisdom_teachings', []),
            decision_frameworks=archive_data.get('decision_frameworks', [])
        )
        
        self.traditions[tradition_name] = tradition_index
        
        # Update indices
        self._update_trait_index(tradition_name, archive_data['personality_traits'])
        self._update_pattern_index(tradition_name, archive_data['interaction_patterns'])
        self._update_concept_index(tradition_name, archive_data['core_concepts'])
        self._update_teaching_index(tradition_name, archive_data.get('wisdom_teachings', []))
        self._update_framework_index(tradition_name, archive_data.get('decision_frameworks', []))
        
        # Update stats
        self.stats.total_traditions += 1
        self.stats.total_concepts += len(archive_data['core_concepts'])
        self.stats.total_teachings += len(archive_data.get('wisdom_teachings', []))
        self.stats.total_frameworks += len(archive_data.get('decision_frameworks', []))
        
    def _truncate_overview(self, overview: str, max_length: int = 200) -> str:
        """Truncate overview text to specified length"""
        if len(overview) > max_length:
            return overview[:max_length] + "..."
        return overview
        
    def _update_trait_index(self, tradition: str, traits: List[str]):
        """Update personality traits index"""
        for trait in traits:
            if trait not in self.personality_traits_index:
                self.personality_traits_index[trait] = set()
            self.personality_traits_index[trait].add(tradition)
            
    def _update_pattern_index(self, tradition: str, patterns: List[str]):
        """Update interaction patterns index"""
        for pattern in patterns:
            if pattern not in self.interaction_patterns_index:
                self.interaction_patterns_index[pattern] = set()
            self.interaction_patterns_index[pattern].add(tradition)
            
    def _update_concept_index(self, tradition: str, concepts: List[str]):
        """Update concepts index"""
        for concept in concepts:
            if concept not in self.concepts_index:
                self.concepts_index[concept] = set()
            self.concepts_index[concept].add(tradition)
            
    def _update_teaching_index(self, tradition: str, teachings: List[str]):
        """Update teachings index"""
        for teaching in teachings:
            if teaching not in self.teachings_index:
                self.teachings_index[teaching] = set()
            self.teachings_index[teaching].add(tradition)
            
    def _update_framework_index(self, tradition: str, frameworks: List[str]):
        """Update frameworks index"""
        for framework in frameworks:
            if framework not in self.frameworks_index:
                self.frameworks_index[framework] = set()
            self.frameworks_index[framework].add(tradition)
            
    def _compile_index(self) -> Dict:
        """
        Compile the complete unified index
        
        Returns:
            Dict containing the complete index structure
        """
        return {
            "extraction_summary": asdict(self.stats),
            "traditions": {name: asdict(index) for name, index in self.traditions.items()},
            "indices": {
                "personality_traits": {
                    trait: list(traditions)
                    for trait, traditions in self.personality_traits_index.items()
                },
                "interaction_patterns": {
                    pattern: list(traditions)
                    for pattern, traditions in self.interaction_patterns_index.items()
                },
                "concepts": {
                    concept: list(traditions)
                    for concept, traditions in self.concepts_index.items()
                },
                "teachings": {
                    teaching: list(traditions)
                    for teaching, traditions in self.teachings_index.items()
                },
                "frameworks": {
                    framework: list(traditions)
                    for framework, traditions in self.frameworks_index.items()
                }
            }
        }
        
    def _save_index(self, index: Dict):
        """
        Save the unified index to disk
        
        Args:
            index: The complete index to save
        """
        index_file = Path("unified_knowledge_index.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
            
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run indexer
    indexer = UnifiedIndexer()
    indexer.create_unified_index() 