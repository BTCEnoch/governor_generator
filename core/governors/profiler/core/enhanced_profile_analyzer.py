"""
Enhanced Governor Profile Analyzer
Extracts and structures governor data for quest/storyline generation
"""

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WisdomFoundation:
    """Core wisdom data extracted from knowledge base"""
    chosen_traditions: List[str]
    philosophical_alignment: str
    indexed_links: List[str]
    application_notes: str

@dataclass
class ElementalEssence:
    """Governor's elemental nature and correspondences"""
    ruling_element: str
    manifestation: Dict[str, str]  # color, motion, scent
    tarot_key: str
    sephirah: str
    constellation: str
    
@dataclass
class TeachingDoctrine:
    """Governor's teaching approach and methods"""
    core_lesson: str
    urgency_reason: str
    misconception: str
    instruction_stages: List[str]
    enochian_terms: List[str]

@dataclass
class VoidmakerAwareness:
    """Governor's cosmic awareness and reality manipulation"""
    cosmic_patterns: List[str]
    reality_influence: List[str]
    integration_unity: List[str]
    cryptic_knowledge: List[str]

@dataclass
class EnhancedGovernorProfile:
    """Complete enhanced profile for quest generation"""
    governor_id: str
    wisdom_foundation: WisdomFoundation
    elemental_essence: ElementalEssence
    teaching_doctrine: TeachingDoctrine
    voidmaker_awareness: VoidmakerAwareness
    preferred_utilities: List[str]
    narrative_tone: str
    difficulty_scale: int  # 1-10

class EnhancedProfileAnalyzer:
    """
    Analyzes governor profiles to extract structured data for quest generation
    """
    
    def __init__(self, governor_output_dir: Path):
        """Initialize the analyzer"""
        self.governor_dir = Path(governor_output_dir)
        self.knowledge_base = {}  # Load from knowledge base
        logger.info(f"Initialized Enhanced Profile Analyzer with dir: {self.governor_dir}")
        
    def load_governor_data(self, governor_id: str) -> Dict:
        """Load raw governor data from JSON"""
        file_path = self.governor_dir / f"{governor_id}.json"
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            logger.info(f"Loaded governor data for {governor_id}")
            return data
        except Exception as e:
            logger.error(f"Failed to load governor {governor_id}: {e}")
            raise
            
    def extract_wisdom_foundation(self, data: Dict) -> WisdomFoundation:
        """Extract wisdom tradition data"""
        try:
            knowledge_base = data.get('knowledge_base_selections', {})
            return WisdomFoundation(
                chosen_traditions=knowledge_base.get('chosen_traditions', []),
                philosophical_alignment=knowledge_base.get('reasoning', ''),
                indexed_links=knowledge_base.get('indexed_links', []),
                application_notes=knowledge_base.get('application_notes', '')
            )
        except Exception as e:
            logger.error(f"Failed to extract wisdom foundation: {e}")
            raise
            
    def extract_elemental_essence(self, data: Dict) -> ElementalEssence:
        """Extract elemental nature and correspondences"""
        try:
            block_b = data.get('block_b', {})
            manifestation = {
                'color': block_b.get('q6_color', ''),
                'motion': block_b.get('q6_motion', ''),
                'scent': block_b.get('q6_scent', '')
            }
            return ElementalEssence(
                ruling_element=block_b.get('q6_element', ''),
                manifestation=manifestation,
                tarot_key=block_b.get('q7_tarot', ''),
                sephirah=block_b.get('q8_sephirah', ''),
                constellation=block_b.get('q9_constellation', '')
            )
        except Exception as e:
            logger.error(f"Failed to extract elemental essence: {e}")
            raise
            
    def extract_teaching_doctrine(self, data: Dict) -> TeachingDoctrine:
        """Extract teaching approach and methods"""
        try:
            block_d = data.get('block_d', {})
            return TeachingDoctrine(
                core_lesson=block_d.get('q16_core_teaching', ''),
                urgency_reason=block_d.get('q17_urgency', ''),
                misconception=block_d.get('q18_misconception', ''),
                instruction_stages=block_d.get('q19_stages', []),
                enochian_terms=block_d.get('q20_enochian_terms', [])
            )
        except Exception as e:
            logger.error(f"Failed to extract teaching doctrine: {e}")
            raise
            
    def extract_voidmaker_awareness(self, data: Dict) -> VoidmakerAwareness:
        """Extract cosmic awareness and reality manipulation capabilities"""
        try:
            voidmaker = data.get('voidmaker_expansion', {})
            return VoidmakerAwareness(
                cosmic_patterns=voidmaker.get('cosmic_awareness_block', []),
                reality_influence=voidmaker.get('reality_influence_block', []),
                integration_unity=voidmaker.get('integration_unity_block', []),
                cryptic_knowledge=voidmaker.get('cryptic_knowledge', [])
            )
        except Exception as e:
            logger.error(f"Failed to extract voidmaker awareness: {e}")
            raise
            
    def determine_narrative_tone(self, data: Dict) -> str:
        """Analyze personality to determine narrative tone"""
        try:
            block_c = data.get('block_c', {})
            virtues = block_c.get('q11_virtues', [])
            flaws = block_c.get('q12_flaws', '')
            
            # Simple tone mapping based on virtues/flaws
            if 'patient' in virtues or 'wise' in virtues:
                return 'measured and philosophical'
            elif 'stern' in virtues or 'harsh' in flaws:
                return 'demanding and direct'
            elif 'mysterious' in virtues:
                return 'cryptic and enigmatic'
            return 'balanced and neutral'
            
        except Exception as e:
            logger.error(f"Failed to determine narrative tone: {e}")
            raise
            
    def calculate_difficulty_scale(self, data: Dict) -> int:
        """Calculate 1-10 difficulty scale based on profile"""
        try:
            # Factors that increase difficulty:
            difficulty = 5  # Start at medium
            
            block_c = data.get('block_c', {})
            if 'harsh' in block_c.get('q12_flaws', '').lower():
                difficulty += 2
                
            block_d = data.get('block_d', {})
            if len(block_d.get('q19_stages', [])) > 3:  # Complex instruction
                difficulty += 1
                
            # Cap between 1-10
            return max(1, min(10, difficulty))
            
        except Exception as e:
            logger.error(f"Failed to calculate difficulty: {e}")
            return 5  # Default to medium
            
    def analyze_governor(self, governor_id: str) -> EnhancedGovernorProfile:
        """
        Perform complete analysis of a governor's profile
        Returns structured data for quest generation
        """
        try:
            logger.info(f"Starting analysis for governor {governor_id}")
            
            # Load raw data
            data = self.load_governor_data(governor_id)
            
            # Extract components
            wisdom = self.extract_wisdom_foundation(data)
            elemental = self.extract_elemental_essence(data)
            teaching = self.extract_teaching_doctrine(data)
            voidmaker = self.extract_voidmaker_awareness(data)
            
            # Determine characteristics
            tone = self.determine_narrative_tone(data)
            difficulty = self.calculate_difficulty_scale(data)
            
            # Get preferred utilities from game mechanics block
            block_j = data.get('block_j', {})
            utilities = block_j.get('q46_preferred_mechanics', [])
            
            # Construct complete profile
            profile = EnhancedGovernorProfile(
                governor_id=governor_id,
                wisdom_foundation=wisdom,
                elemental_essence=elemental,
                teaching_doctrine=teaching,
                voidmaker_awareness=voidmaker,
                preferred_utilities=utilities,
                narrative_tone=tone,
                difficulty_scale=difficulty
            )
            
            logger.info(f"Completed analysis for {governor_id}")
            logger.info(f"Tone: {tone}, Difficulty: {difficulty}")
            return profile
            
        except Exception as e:
            logger.error(f"Failed complete analysis for {governor_id}: {e}")
            raise
            
    def batch_analyze_governors(self, governor_ids: List[str]) -> Dict[str, EnhancedGovernorProfile]:
        """
        Analyze multiple governors in batch
        Returns map of governor_id to enhanced profile
        """
        results = {}
        for gov_id in governor_ids:
            try:
                profile = self.analyze_governor(gov_id)
                results[gov_id] = profile
            except Exception as e:
                logger.error(f"Failed analysis for {gov_id}: {e}")
                continue
        return results 