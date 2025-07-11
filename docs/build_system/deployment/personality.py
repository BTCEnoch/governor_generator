"""
Personality Traits Generator

Handles generation of personality aspects for governor profiles using
deterministic generation from Bitcoin block data.
"""

from typing import Dict, List, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class PersonalityCore:
    """Core personality traits"""
    archetype: str
    primary_traits: List[str]
    secondary_traits: List[str]
    disposition: str

@dataclass
class TeachingStyle:
    """Teaching approach and methods"""
    primary_method: str
    secondary_methods: List[str]
    difficulty: float
    adaptability: float

class PersonalityTraits:
    """
    Generates personality traits using deterministic methods
    """
    
    def __init__(self):
        """Initialize personality trait generation system"""
        self.archetypes = [
            "Sage",
            "Warrior",
            "Healer",
            "Teacher",
            "Guardian"
        ]
        self.teaching_methods = [
            "Direct Instruction",
            "Guided Discovery",
            "Metaphorical",
            "Experiential",
            "Challenge-Based"
        ]
        
    async def generate(
        self,
        governor_number: int,
        block_hash: str
    ) -> Dict:
        """
        Generate personality profile aspects
        
        Args:
            governor_number: The governor's number (1-91)
            block_hash: Bitcoin block hash for deterministic generation
            
        Returns:
            Dict containing personality profile aspects
        """
        try:
            # Generate core components
            core = self._generate_core(governor_number, block_hash)
            teaching = self._generate_teaching(governor_number, block_hash)
            
            return {
                "core": {
                    "archetype": core.archetype,
                    "primary_traits": core.primary_traits,
                    "secondary_traits": core.secondary_traits,
                    "disposition": core.disposition
                },
                "teaching": {
                    "primary_method": teaching.primary_method,
                    "secondary_methods": teaching.secondary_methods,
                    "difficulty": teaching.difficulty,
                    "adaptability": teaching.adaptability
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating personality traits: {e}")
            raise
            
    def _generate_core(
        self,
        governor_number: int,
        block_hash: str
    ) -> PersonalityCore:
        """Generate core personality aspects"""
        # TODO: Implement proper deterministic generation
        return PersonalityCore(
            archetype=self.archetypes[0],
            primary_traits=["Wise", "Patient"],
            secondary_traits=["Mysterious", "Contemplative"],
            disposition="Balanced"
        )
        
    def _generate_teaching(
        self,
        governor_number: int,
        block_hash: str
    ) -> TeachingStyle:
        """Generate teaching style aspects"""
        # TODO: Implement proper deterministic generation
        return TeachingStyle(
            primary_method=self.teaching_methods[0],
            secondary_methods=self.teaching_methods[1:3],
            difficulty=0.6,
            adaptability=0.8
        )
        
    def validate(self, profile: Dict) -> bool:
        """
        Validate personality profile aspects
        
        Args:
            profile: Personality profile to validate
            
        Returns:
            bool indicating if profile is valid
        """
        try:
            # Check required sections
            if "core" not in profile or "teaching" not in profile:
                return False
                
            # Validate core
            core = profile["core"]
            if not all(key in core for key in [
                "archetype",
                "primary_traits",
                "secondary_traits",
                "disposition"
            ]):
                return False
                
            # Validate teaching
            teaching = profile["teaching"]
            if not all(key in teaching for key in [
                "primary_method",
                "secondary_methods",
                "difficulty",
                "adaptability"
            ]):
                return False
                
            # Validate archetype
            if core["archetype"] not in self.archetypes:
                return False
                
            # Validate teaching methods
            if teaching["primary_method"] not in self.teaching_methods:
                return False
                
            if not all(method in self.teaching_methods 
                      for method in teaching["secondary_methods"]):
                return False
                
            # Validate numeric ranges
            if not 0 <= teaching["difficulty"] <= 1:
                return False
                
            if not 0 <= teaching["adaptability"] <= 1:
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error validating personality profile: {e}")
            return False 