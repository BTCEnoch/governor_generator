#!/usr/bin/env python3
"""
Persona Extractor - Analyzes governor personalities
Extracts key traits, teaching style, and voidmaker integration level
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from core_loader import CoreDataLoader, EnhancedGovernorProfile

logger = logging.getLogger(__name__)

@dataclass
class PersonaProfile:
    """Simplified persona analysis"""
    governor_name: str
    tone: str
    traits: List[str]
    power_level: str
    tradition_count: int
    primary_element: Optional[str]
    voidmaker_themes: List[str]
    teaching_style: str

class PersonaExtractor:
    """Extracts personality traits from enhanced governor profiles"""
    
    def __init__(self):
        self.loader = CoreDataLoader()
    
    def extract_persona(self, governor_name: str) -> PersonaProfile:
        """Extract persona profile from enhanced governor data"""
        
        profile = self.loader.load_enhanced_governor(governor_name)
        
        # Extract basic traits
        tone = self._determine_tone(profile)
        traits = self._extract_traits(profile)
        teaching_style = self._determine_teaching_style(profile)
        
        # Extract voidmaker themes
        voidmaker_themes = []
        for block in profile.voidmaker_expansion.values():
            voidmaker_themes.extend(block.themes)
        
        # Remove duplicates
        voidmaker_themes = list(set(voidmaker_themes))[:5]
        
        return PersonaProfile(
            governor_name=profile.governor_name,
            tone=tone,
            traits=traits,
            power_level=profile.power_level or "formidable_approachable",
            tradition_count=profile.tradition_depth or 0,
            primary_element=profile.elemental_nature,
            voidmaker_themes=voidmaker_themes,
            teaching_style=teaching_style
        )
    
    def _determine_tone(self, profile: EnhancedGovernorProfile) -> str:
        """Determine overall tone from personality blocks"""
        
        # Look at virtues (Q11) and flaws (Q12)
        personality_block = profile.blocks.get("C_personality", {})
        
        if "11" in personality_block:
            virtues = personality_block["11"].lower()
            if "wise" in virtues or "patient" in virtues:
                return "wise_patient"
            elif "fierce" in virtues or "power" in virtues:
                return "fierce_powerful"
            elif "merciful" in virtues or "gentle" in virtues:
                return "merciful_gentle"
        
        return "balanced_authority"
    
    def _extract_traits(self, profile: EnhancedGovernorProfile) -> List[str]:
        """Extract key personality traits"""
        
        traits = []
        
        # Add elemental nature
        if profile.elemental_nature:
            traits.append(f"{profile.elemental_nature}_elemental")
        
        # Add tradition influence
        if profile.tradition_depth:
            if profile.tradition_depth >= 3:
                traits.append("tradition_rich")
            else:
                traits.append("tradition_focused")
        
        # Add personality markers from blocks
        personality_block = profile.blocks.get("C_personality", {})
        if "12" in personality_block:
            flaw = personality_block["12"].lower()
            if "impatient" in flaw:
                traits.append("demanding")
            elif "proud" in flaw:
                traits.append("noble")
        
        return traits[:4]  # Limit to 4 key traits
    
    def _determine_teaching_style(self, profile: EnhancedGovernorProfile) -> str:
        """Determine teaching approach"""
        
        # Look at testing style (Q21-25)
        ordeal_block = profile.blocks.get("E_sacred_ordeal", {})
        
        if "25" in ordeal_block:
            mercy = ordeal_block["25"].lower()
            if "harsh" in mercy or "strict" in mercy:
                return "strict_traditional"
            elif "gentle" in mercy or "kind" in mercy:
                return "gentle_guiding"
        
        return "balanced_testing"

def test_persona_extractor():
    """Simple test"""
    try:
        print("🧪 Starting persona extractor test...")
        extractor = PersonaExtractor()
        print("✅ Created persona extractor")
        
        # Test with first available governor
        available = extractor.loader.list_available_governors()
        print(f"📊 Found {len(available)} governors")
        
        if available:
            test_gov = available[0]
            print(f"🧪 Testing with {test_gov}")
            
            persona = extractor.extract_persona(test_gov)
            
            print(f"✅ Extracted persona for {persona.governor_name}")
            print(f"   Tone: {persona.tone}")
            print(f"   Traits: {persona.traits}")
            print(f"   Element: {persona.primary_element}")
            print(f"   Traditions: {persona.tradition_count}")
            print(f"   Voidmaker themes: {persona.voidmaker_themes}")
            print(f"   Teaching style: {persona.teaching_style}")
            
            return True
        else:
            print("❌ No governors available")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_persona_extractor() 