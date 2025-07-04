#!/usr/bin/env python3
"""
Enhanced Storyline Generator - Core Data Loader
Handles loading and parsing of enhanced governor profiles and canonical elements
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class KnowledgeBaseSelection:
    """Structure for governor's selected wisdom traditions"""
    chosen_traditions: List[str]
    reasoning: str
    indexed_links: List[str]
    application_notes: str

@dataclass
class VoidmakerBlock:
    """Structure for voidmaker expansion content blocks"""
    block_name: str
    questions: Dict[str, Dict[str, str]]  # question_number: {"question": "...", "answer": "..."}
    themes: List[str]

@dataclass
class EnhancedGovernorProfile:
    """Complete enhanced governor profile structure"""
    governor_name: str
    governor_number: int
    profile: Dict
    interview_date: str
    confirmation: str
    
    # Enhanced elements
    knowledge_base_selections: KnowledgeBaseSelection
    blocks: Dict[str, Dict]  # Original 127 questions organized by block
    voidmaker_expansion: Dict[str, VoidmakerBlock]  # 3 voidmaker blocks
    
    # Derived attributes
    home_aethyr: Optional[str] = field(default=None)
    elemental_nature: Optional[str] = field(default=None)
    power_level: Optional[str] = field(default=None)
    tradition_depth: Optional[int] = field(default=None)

class CoreDataLoader:
    """Handles loading and validation of all data sources"""
    
    def __init__(self, base_path: Path = Path(".")):
        self.base_path = Path(base_path)
        self.governor_output_path = self.base_path / "governor_output"
        self.canonical_pack_path = self.base_path / "pack"
        self.canon_path = self.base_path / "canon"
        
        # Validate paths exist
        self._validate_paths()
        
        # Cache for loaded data
        self._canonical_cache = {}
        self._governor_cache = {}
    
    def _validate_paths(self) -> None:
        """Ensure all required directories exist"""
        required_paths = [
            self.governor_output_path,
            self.canonical_pack_path,
            self.canon_path
        ]
        
        for path in required_paths:
            if not path.exists():
                raise FileNotFoundError(f"Required path not found: {path}")
        
        logger.info("✅ All required paths validated")
    
    def load_enhanced_governor(self, governor_name: str) -> EnhancedGovernorProfile:
        """Load and parse enhanced governor profile"""
        
        # Check cache first
        if governor_name in self._governor_cache:
            logger.info(f"📋 Loading {governor_name} from cache")
            return self._governor_cache[governor_name]
        
        governor_file = self.governor_output_path / f"{governor_name}.json"
        
        if not governor_file.exists():
            raise FileNotFoundError(f"Governor file not found: {governor_file}")
        
        try:
            with open(governor_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            logger.info(f"📖 Loaded raw data for {governor_name}")
            
            # Parse into structured format
            enhanced_profile = self._parse_governor_data(raw_data)
            
            # Cache the result
            self._governor_cache[governor_name] = enhanced_profile
            
            logger.info(f"✅ Successfully loaded enhanced profile for {governor_name}")
            return enhanced_profile
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing error for {governor_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error loading {governor_name}: {e}")
            raise
    
    def _parse_governor_data(self, raw_data: Dict) -> EnhancedGovernorProfile:
        """Parse raw JSON into structured EnhancedGovernorProfile"""
        
        # Extract knowledge base selections
        kb_raw = raw_data.get("knowledge_base_selections", {})
        knowledge_base = KnowledgeBaseSelection(
            chosen_traditions=kb_raw.get("chosen_traditions", []),
            reasoning=kb_raw.get("reasoning", ""),
            indexed_links=kb_raw.get("indexed_links", []),
            application_notes=kb_raw.get("application_notes", "")
        )
        
        # Extract voidmaker expansion blocks
        vm_raw = raw_data.get("voidmaker_expansion", {})
        voidmaker_expansion = {}
        
        for block_key, block_data in vm_raw.items():
            if isinstance(block_data, dict):
                voidmaker_expansion[block_key] = VoidmakerBlock(
                    block_name=block_key,
                    questions=block_data,
                    themes=self._extract_voidmaker_themes(block_data)
                )
        
        # Create enhanced profile
        enhanced_profile = EnhancedGovernorProfile(
            governor_name=raw_data.get("governor_name", "Unknown"),
            governor_number=raw_data.get("governor_number", 0),
            profile=raw_data.get("profile", {}),
            interview_date=raw_data.get("interview_date", ""),
            confirmation=raw_data.get("confirmation", ""),
            knowledge_base_selections=knowledge_base,
            blocks=raw_data.get("blocks", {}),
            voidmaker_expansion=voidmaker_expansion
        )
        
        # Extract derived attributes
        self._extract_derived_attributes(enhanced_profile)
        
        return enhanced_profile
    
    def _extract_voidmaker_themes(self, block_data: Dict) -> List[str]:
        """Extract thematic keywords from voidmaker block content"""
        themes = []
        
        # Enhanced keyword extraction for voidmaker content
        cosmic_keywords = [
            "reality", "simulation", "consciousness", "void", "universe", 
            "entropy", "pattern", "illusion", "truth", "awareness",
            "dimensional", "geometric", "hermetic", "kabbalistic", 
            "sacred", "infinite", "unity", "dissolution", "transcendence"
        ]
        
        # Extract from actual answer content
        for q_data in block_data.values():
            if isinstance(q_data, dict) and "answer" in q_data:
                answer_lower = q_data["answer"].lower()
                for keyword in cosmic_keywords:
                    if keyword in answer_lower and keyword not in themes:
                        themes.append(keyword)
            elif isinstance(q_data, str):  # Fallback for old format
                answer_lower = q_data.lower()
                for keyword in cosmic_keywords:
                    if keyword in answer_lower and keyword not in themes:
                        themes.append(keyword)
        
        return themes[:5]  # Limit to top 5 themes
    
    def _extract_derived_attributes(self, profile: EnhancedGovernorProfile) -> None:
        """Extract and set derived attributes from profile data"""
        
        # Extract home Aethyr directly from profile or Q3 as fallback
        if isinstance(profile.profile, dict) and 'aethyr' in profile.profile:
            profile.home_aethyr = profile.profile['aethyr']
        else:
            # Fallback: Extract from Q3 if available
            identity_block = profile.blocks.get("A_identity_origin", {})
            if "3" in identity_block:
                q3_data = identity_block["3"]
                aethyr_text = q3_data if isinstance(q3_data, str) else q3_data.get("answer", "")
                # Look for Aethyr names in text
                aethyr_names = ["LIL", "ARN", "ZOM", "PAZ", "LIT", "MAZ", "DEO", "ZID", "ZIP", "ZAX", "TOR"]
                for aethyr in aethyr_names:
                    if aethyr in aethyr_text.upper():
                        profile.home_aethyr = aethyr
                        break
        
        # Extract elemental nature directly from profile
        if isinstance(profile.profile, dict) and 'element' in profile.profile:
            element = profile.profile['element'].lower()
            profile.elemental_nature = element
        else:
            # Fallback: Extract from Q6 if available
            elemental_block = profile.blocks.get("B_elemental_essence", {})
            if "6" in elemental_block:
                q6_data = elemental_block["6"]
                element_text = (q6_data if isinstance(q6_data, str) else q6_data.get("answer", "")).lower()
                if "fire" in element_text:
                    profile.elemental_nature = "fire"
                elif "water" in element_text:
                    profile.elemental_nature = "water"
                elif "air" in element_text:
                    profile.elemental_nature = "air"
                elif "earth" in element_text:
                    profile.elemental_nature = "earth"
        
        # Set tradition depth based on number of selected traditions
        profile.tradition_depth = len(profile.knowledge_base_selections.chosen_traditions)
        
        # Set power level (always formidable but approachable for seekers)
        profile.power_level = "formidable_approachable"
        
        logger.debug(f"🔍 Derived attributes for {profile.governor_name}: "
                    f"Aethyr={profile.home_aethyr}, Element={profile.elemental_nature}, "
                    f"Traditions={profile.tradition_depth}")

    def list_available_governors(self) -> List[str]:
        """Get list of all available governor names"""
        governor_files = list(self.governor_output_path.glob("*.json"))
        return [f.stem for f in governor_files]
    
    def validate_governor_completeness(self, governor_name: str) -> Dict[str, Union[bool, str]]:
        """Validate that a governor has all required enhanced sections"""
        try:
            profile = self.load_enhanced_governor(governor_name)
            
            validation: Dict[str, Union[bool, str]] = {
                "has_knowledge_base_selections": bool(profile.knowledge_base_selections.chosen_traditions),
                "has_voidmaker_expansion": bool(profile.voidmaker_expansion),
                "has_blocks": bool(profile.blocks),
                "has_derived_attributes": all([
                    profile.tradition_depth is not None,
                    profile.power_level is not None
                ])
            }
            
            validation["is_complete"] = all(v for v in validation.values() if isinstance(v, bool))
            
            return validation
            
        except Exception as e:
            logger.error(f"❌ Validation failed for {governor_name}: {e}")
            return {"is_complete": False, "error": str(e)}

# Quick validation function for testing
def test_core_loader():
    """Test the core loader with available governors"""
    try:
        loader = CoreDataLoader()
        available_governors = loader.list_available_governors()
        
        print(f"📊 Found {len(available_governors)} governors")
        
        if available_governors:
            # Test with first governor
            test_governor = available_governors[0]
            print(f"🧪 Testing with {test_governor}")
            
            profile = loader.load_enhanced_governor(test_governor)
            validation = loader.validate_governor_completeness(test_governor)
            
            print(f"✅ Successfully loaded {profile.governor_name}")
            print(f"📋 Traditions: {profile.knowledge_base_selections.chosen_traditions}")
            print(f"🌌 Voidmaker blocks: {list(profile.voidmaker_expansion.keys())}")
            print(f"🔍 Validation: {validation}")
            
            return True
        else:
            print("❌ No governors found")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_core_loader() 