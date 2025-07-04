#!/usr/bin/env python3
"""
Canonical Trait Registry - Access canonical governor traits
Small focused registry for the Governor Engine
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class CanonicalTraits:
    """Canonical traits for a governor"""
    personality: List[str]
    domain: str
    visual_motif: str
    letter_influence: List[str]

@dataclass
class GovernorCanonical:
    """Canonical governor data"""
    name: str
    region: str
    aethyr_number: int
    aethyr_name: str
    correspondence: str
    canonical_traits: CanonicalTraits

class CanonicalTraitRegistry:
    """Registry for accessing canonical governor traits"""
    
    def __init__(self, base_path: Path = Path(".")):
        self.base_path = base_path
        self.traits_file = base_path / "governor_indexes" / "canonical_traits.json"
        self._canonical_data = None
        self._governor_lookup = {}
    
    def load_canonical_data(self) -> bool:
        """Load canonical traits data"""
        try:
            if not self.traits_file.exists():
                logger.error(f"Canonical traits file not found: {self.traits_file}")
                return False
            
            with open(self.traits_file, 'r', encoding='utf-8') as f:
                self._canonical_data = json.load(f)
            
            # Build governor lookup index
            self._build_governor_lookup()
            
            logger.info(f"Loaded {len(self._governor_lookup)} canonical governors")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load canonical data: {e}")
            return False
    
    def _build_governor_lookup(self):
        """Build fast lookup index by governor name"""
        if not self._canonical_data:
            return
        
        for aethyr in self._canonical_data:
            aethyr_num = aethyr["aethyr_number"]
            aethyr_name = aethyr["aethyr_name"]
            correspondence = aethyr["correspondence"]
            
            for gov_data in aethyr["governors"]:
                canonical_traits = CanonicalTraits(
                    personality=gov_data["canonical_traits"]["personality"],
                    domain=gov_data["canonical_traits"]["domain"],
                    visual_motif=gov_data["canonical_traits"]["visual_motif"],
                    letter_influence=gov_data["canonical_traits"]["letter_influence"]
                )
                
                governor = GovernorCanonical(
                    name=gov_data["name"],
                    region=gov_data["region"],
                    aethyr_number=aethyr_num,
                    aethyr_name=aethyr_name,
                    correspondence=correspondence,
                    canonical_traits=canonical_traits
                )
                
                self._governor_lookup[gov_data["name"]] = governor
    
    def get_governor_canonical(self, governor_name: str) -> Optional[GovernorCanonical]:
        """Get canonical data for a governor"""
        if not self._canonical_data:
            self.load_canonical_data()
        
        return self._governor_lookup.get(governor_name)
    
    def list_available_governors(self) -> List[str]:
        """List all governors with canonical data"""
        if not self._canonical_data:
            self.load_canonical_data()
        
        return list(self._governor_lookup.keys())
    
    def get_governors_by_aethyr(self, aethyr_number: int) -> List[GovernorCanonical]:
        """Get all governors from a specific aethyr"""
        if not self._canonical_data:
            self.load_canonical_data()
        
        return [gov for gov in self._governor_lookup.values() 
                if gov.aethyr_number == aethyr_number]

def test_canonical_registry():
    """Simple test of canonical registry"""
    try:
        print("🧪 Testing Canonical Trait Registry...")
        
        registry = CanonicalTraitRegistry()
        
        if not registry.load_canonical_data():
            print("❌ Failed to load canonical data")
            return False
        
        governors = registry.list_available_governors()
        print(f"📊 Found {len(governors)} governors: {governors}")
        
        if governors:
            test_gov = governors[0]
            canonical = registry.get_governor_canonical(test_gov)
            
            if canonical:
                print(f"✅ Retrieved canonical data for {canonical.name}")
                print(f"   Region: {canonical.region}")
                print(f"   Domain: {canonical.canonical_traits.domain}")
                print(f"   Personality: {canonical.canonical_traits.personality}")
                print(f"   Aethyr: {canonical.aethyr_number} ({canonical.aethyr_name})")
                return True
        
        print("❌ No canonical data found")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_canonical_registry() 