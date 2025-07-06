"""
Unified Knowledge Processor
Combines functionality from all knowledge extraction and processing scripts
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class ProcessingStats:
    """Statistics about the processed content"""
    total_traditions: int = 0
    total_concepts: int = 0
    total_teachings: int = 0
    total_frameworks: int = 0
    total_personality_traits: int = 0
    total_interaction_patterns: int = 0
    processing_timestamp: str = ""

@dataclass
class TraditionContent:
    """Content extracted from a mystical tradition"""
    tradition_name: str
    display_name: str
    overview: str
    core_concepts: List[str]
    wisdom_teachings: List[str]
    decision_frameworks: List[str]
    personality_traits: List[str]
    interaction_patterns: List[str]
    quality_rating: float
    source_count: int
    metadata: Dict

class UnifiedKnowledgeProcessor:
    """
    Unified processor for extracting and processing mystical knowledge
    """
    
    def __init__(self, source_dir: str = "source_traditions"):
        self.source_dir = Path(source_dir)
        self.stats = ProcessingStats()
        self.traditions: Dict[str, TraditionContent] = {}
        self.concept_index: Dict[str, Set[str]] = {}  # concept -> traditions
        self.teaching_index: Dict[str, Set[str]] = {}  # teaching -> traditions
        self.framework_index: Dict[str, Set[str]] = {}  # framework -> traditions
        self.trait_index: Dict[str, Set[str]] = {}  # trait -> traditions
        self.pattern_index: Dict[str, Set[str]] = {}  # pattern -> traditions
        
    def process_traditions(self) -> Dict:
        """
        Process all tradition source files and generate knowledge base
        
        Returns:
            Dict containing the complete processed knowledge base
        """
        logger.info("🔄 Processing mystical traditions...")
        
        # Reset state
        self._reset_state()
        
        # Process all source files
        self._process_source_files()
        
        # Compile knowledge base
        knowledge_base = self._compile_knowledge_base()
        
        # Save knowledge base
        self._save_knowledge_base(knowledge_base)
        
        logger.info(f"✅ Processed {self.stats.total_traditions} traditions")
        logger.info(f"📚 Extracted {self.stats.total_concepts} concepts")
        logger.info(f"🎓 Captured {self.stats.total_teachings} teachings")
        
        return knowledge_base
        
    def _reset_state(self):
        """Reset all internal state before processing"""
        self.stats = ProcessingStats(processing_timestamp=datetime.now().isoformat())
        self.traditions.clear()
        self.concept_index.clear()
        self.teaching_index.clear()
        self.framework_index.clear()
        self.trait_index.clear()
        self.pattern_index.clear()
        
    def _process_source_files(self):
        """Process all source files in the source directory"""
        if not self.source_dir.exists():
            logger.error(f"Source directory not found: {self.source_dir}")
            return
            
        for source_file in self.source_dir.glob("*.json"):
            try:
                self._process_single_source(source_file)
            except Exception as e:
                logger.error(f"⚠️ Failed to process {source_file}: {e}")
                
    def _process_single_source(self, source_file: Path):
        """
        Process a single tradition source file
        
        Args:
            source_file: Path to the source file to process
        """
        logger.info(f"Processing source: {source_file}")
        
        with open(source_file, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
            
        # Extract core content
        tradition_content = self._extract_tradition_content(source_data)
        
        # Store tradition content
        self.traditions[tradition_content.tradition_name] = tradition_content
        
        # Update indices
        self._update_concept_index(tradition_content)
        self._update_teaching_index(tradition_content)
        self._update_framework_index(tradition_content)
        self._update_trait_index(tradition_content)
        self._update_pattern_index(tradition_content)
        
        # Update stats
        self.stats.total_traditions += 1
        self.stats.total_concepts += len(tradition_content.core_concepts)
        self.stats.total_teachings += len(tradition_content.wisdom_teachings)
        self.stats.total_frameworks += len(tradition_content.decision_frameworks)
        self.stats.total_personality_traits += len(tradition_content.personality_traits)
        self.stats.total_interaction_patterns += len(tradition_content.interaction_patterns)
        
    def _extract_tradition_content(self, source_data: Dict) -> TraditionContent:
        """
        Extract structured content from source data
        
        Args:
            source_data: Raw source data
            
        Returns:
            TraditionContent containing extracted and structured content
        """
        return TraditionContent(
            tradition_name=source_data["tradition_name"],
            display_name=source_data["display_name"],
            overview=source_data["overview"],
            core_concepts=self._extract_concepts(source_data),
            wisdom_teachings=self._extract_teachings(source_data),
            decision_frameworks=self._extract_frameworks(source_data),
            personality_traits=source_data.get("personality_traits", []),
            interaction_patterns=source_data.get("interaction_patterns", []),
            quality_rating=source_data.get("quality_rating", 0.0),
            source_count=source_data.get("source_count", 0),
            metadata=self._extract_metadata(source_data)
        )
        
    def _extract_concepts(self, source_data: Dict) -> List[str]:
        """Extract and normalize core concepts"""
        concepts = []
        for concept in source_data.get("core_concepts", []):
            normalized = self._normalize_text(concept)
            if normalized:
                concepts.append(normalized)
        return concepts
        
    def _extract_teachings(self, source_data: Dict) -> List[str]:
        """Extract and normalize wisdom teachings"""
        teachings = []
        for teaching in source_data.get("wisdom_teachings", []):
            normalized = self._normalize_text(teaching)
            if normalized:
                teachings.append(normalized)
        return teachings
        
    def _extract_frameworks(self, source_data: Dict) -> List[str]:
        """Extract and normalize decision frameworks"""
        frameworks = []
        for framework in source_data.get("decision_frameworks", []):
            normalized = self._normalize_text(framework)
            if normalized:
                frameworks.append(normalized)
        return frameworks
        
    def _extract_metadata(self, source_data: Dict) -> Dict:
        """Extract and structure metadata"""
        return {
            "processed_at": datetime.now().isoformat(),
            "version": "2.0",
            "source_file": source_data.get("source_file", "unknown"),
            "last_updated": source_data.get("last_updated"),
            "contributors": source_data.get("contributors", []),
            "tags": source_data.get("tags", [])
        }
        
    def _normalize_text(self, text: str) -> str:
        """Normalize text content"""
        if not text:
            return ""
        return text.strip().lower()
        
    def _update_concept_index(self, tradition: TraditionContent):
        """Update concept index"""
        for concept in tradition.core_concepts:
            if concept not in self.concept_index:
                self.concept_index[concept] = set()
            self.concept_index[concept].add(tradition.tradition_name)
            
    def _update_teaching_index(self, tradition: TraditionContent):
        """Update teaching index"""
        for teaching in tradition.wisdom_teachings:
            if teaching not in self.teaching_index:
                self.teaching_index[teaching] = set()
            self.teaching_index[teaching].add(tradition.tradition_name)
            
    def _update_framework_index(self, tradition: TraditionContent):
        """Update framework index"""
        for framework in tradition.decision_frameworks:
            if framework not in self.framework_index:
                self.framework_index[framework] = set()
            self.framework_index[framework].add(tradition.tradition_name)
            
    def _update_trait_index(self, tradition: TraditionContent):
        """Update trait index"""
        for trait in tradition.personality_traits:
            if trait not in self.trait_index:
                self.trait_index[trait] = set()
            self.trait_index[trait].add(tradition.tradition_name)
            
    def _update_pattern_index(self, tradition: TraditionContent):
        """Update pattern index"""
        for pattern in tradition.interaction_patterns:
            if pattern not in self.pattern_index:
                self.pattern_index[pattern] = set()
            self.pattern_index[pattern].add(tradition.tradition_name)
            
    def _compile_knowledge_base(self) -> Dict:
        """
        Compile the complete knowledge base
        
        Returns:
            Dict containing the complete knowledge base structure
        """
        return {
            "processing_summary": asdict(self.stats),
            "traditions": {
                name: asdict(content)
                for name, content in self.traditions.items()
            },
            "indices": {
                "concepts": {
                    concept: list(traditions)
                    for concept, traditions in self.concept_index.items()
                },
                "teachings": {
                    teaching: list(traditions)
                    for teaching, traditions in self.teaching_index.items()
                },
                "frameworks": {
                    framework: list(traditions)
                    for framework, traditions in self.framework_index.items()
                },
                "personality_traits": {
                    trait: list(traditions)
                    for trait, traditions in self.trait_index.items()
                },
                "interaction_patterns": {
                    pattern: list(traditions)
                    for pattern, traditions in self.pattern_index.items()
                }
            }
        }
        
    def _save_knowledge_base(self, knowledge_base: Dict):
        """
        Save the knowledge base to disk
        
        Args:
            knowledge_base: The complete knowledge base to save
        """
        output_file = Path("knowledge_base.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
            
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run processor
    processor = UnifiedKnowledgeProcessor()
    processor.process_traditions() 