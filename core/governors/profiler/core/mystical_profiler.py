#!/usr/bin/env python3
"""
MysticalProfiler for generating governor profiles based on mystical traditions
"""

from typing import Dict, List, Optional
import logging
from datetime import datetime

from core.governors.profiler.schemas.mystical_schemas import (
    GovernorProfile,
    MysticalAlignment,
    Archetype,
    Trait,
    Personality,
    Specialization,
    Approach,
    Metadata
)
from core.knowledge_base.mystical_traditions import MysticalTraditions
from core.utils.validation import validate_schema

logger = logging.getLogger(__name__)

class MysticalProfiler:
    """
    Generates governor profiles using mystical tradition knowledge
    """
    
    def __init__(self):
        """Initialize the profiler with mystical tradition data"""
        self.traditions = MysticalTraditions()
        self.logger = logging.getLogger(__name__)
        
    async def generate_profile(self, governor_data: Dict) -> Dict:
        """
        Generate a complete governor profile
        
        Args:
            governor_data: Raw data about the governor
            
        Returns:
            Dict containing the complete governor profile
        """
        try:
            # Generate each component of the profile
            mystical_alignments = await self._generate_alignments(governor_data)
            archetype = await self._generate_archetype(governor_data, mystical_alignments)
            traits = await self._generate_traits(governor_data, archetype)
            personality = await self._generate_personality(governor_data, traits)
            specializations = await self._generate_specializations(governor_data, archetype)
            approaches = await self._generate_approaches(governor_data, personality)
            
            # Create the complete profile
            profile = GovernorProfile(
                name=governor_data["name"],
                number=governor_data["number"],
                mystical_alignments=mystical_alignments,
                archetype=archetype,
                traits=traits,
                personality=personality,
                specializations=specializations,
                approaches=approaches,
                metadata=Metadata(
                    generated_at=datetime.now(),
                    version="2.0",
                    processor="mystical_profiler"
                )
            )
            
            # Convert to dict and validate
            profile_dict = self._to_dict(profile)
            if not validate_schema(profile_dict, "governor_profile"):
                raise ValueError("Generated profile failed schema validation")
                
            return profile_dict
            
        except Exception as e:
            self.logger.error(f"Error generating profile: {e}")
            raise
            
    async def _generate_alignments(self, governor_data: Dict) -> MysticalAlignment:
        """Generate mystical alignments for the governor"""
        try:
            # Get alignments based on governor number and name
            alignments = await self.traditions.get_alignments(
                number=governor_data["number"],
                name=governor_data["name"]
            )
            
            return MysticalAlignment(
                element=alignments["element"],
                aethyr=alignments["aethyr"],
                direction=alignments["direction"],
                correspondence=alignments.get("correspondence")
            )
            
        except Exception as e:
            self.logger.error(f"Error generating alignments: {e}")
            raise
            
    async def _generate_archetype(
        self,
        governor_data: Dict,
        alignments: MysticalAlignment
    ) -> Archetype:
        """Generate governor archetype based on alignments"""
        try:
            # Get archetype based on alignments
            archetype_data = await self.traditions.get_archetype(
                element=alignments.element,
                aethyr=alignments.aethyr
            )
            
            return Archetype(
                primary=archetype_data["primary"],
                secondary=archetype_data.get("secondary"),
                description=archetype_data["description"]
            )
            
        except Exception as e:
            self.logger.error(f"Error generating archetype: {e}")
            raise
            
    async def _generate_traits(
        self,
        governor_data: Dict,
        archetype: Archetype
    ) -> List[Trait]:
        """Generate governor traits based on archetype"""
        try:
            # Get traits based on archetype
            trait_data = await self.traditions.get_traits(
                archetype=archetype.primary,
                secondary_archetype=archetype.secondary
            )
            
            traits = []
            for t in trait_data:
                traits.append(Trait(
                    name=t["name"],
                    category=t["category"],
                    description=t["description"],
                    strength=t.get("strength", 1)
                ))
                
            return traits
            
        except Exception as e:
            self.logger.error(f"Error generating traits: {e}")
            raise
            
    async def _generate_personality(
        self,
        governor_data: Dict,
        traits: List[Trait]
    ) -> Personality:
        """Generate governor personality based on traits"""
        try:
            # Get personality aspects based on traits
            personality_data = await self.traditions.get_personality(
                traits=[t.name for t in traits]
            )
            
            return Personality(
                primary_aspect=personality_data["primary"],
                secondary_aspect=personality_data["secondary"],
                description=personality_data["description"],
                traits=traits
            )
            
        except Exception as e:
            self.logger.error(f"Error generating personality: {e}")
            raise
            
    async def _generate_specializations(
        self,
        governor_data: Dict,
        archetype: Archetype
    ) -> List[Specialization]:
        """Generate governor specializations based on archetype"""
        try:
            # Get specializations based on archetype
            spec_data = await self.traditions.get_specializations(
                archetype=archetype.primary
            )
            
            specializations = []
            for s in spec_data:
                specializations.append(Specialization(
                    domain=s["domain"],
                    proficiency=s["proficiency"],
                    description=s["description"]
                ))
                
            return specializations
            
        except Exception as e:
            self.logger.error(f"Error generating specializations: {e}")
            raise
            
    async def _generate_approaches(
        self,
        governor_data: Dict,
        personality: Personality
    ) -> List[Approach]:
        """Generate governor approaches based on personality"""
        try:
            # Get approaches based on personality
            approach_data = await self.traditions.get_approaches(
                primary_aspect=personality.primary_aspect,
                secondary_aspect=personality.secondary_aspect
            )
            
            approaches = []
            for a in approach_data:
                approaches.append(Approach(
                    style=a["style"],
                    preference=a["preference"],
                    description=a["description"]
                ))
                
            return approaches
            
        except Exception as e:
            self.logger.error(f"Error generating approaches: {e}")
            raise
            
    def _to_dict(self, obj: any) -> Dict:
        """Convert a dataclass instance to a dictionary"""
        if hasattr(obj, "__dataclass_fields__"):
            result = {}
            for field in obj.__dataclass_fields__:
                value = getattr(obj, field)
                if isinstance(value, list):
                    result[field] = [self._to_dict(item) for item in value]
                elif hasattr(value, "__dataclass_fields__"):
                    result[field] = self._to_dict(value)
                elif isinstance(value, datetime):
                    result[field] = value.isoformat()
                else:
                    result[field] = value
            return result
        return obj
