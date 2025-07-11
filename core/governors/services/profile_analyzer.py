"""
Governor Profile Analyzer Module
"""

from typing import Dict, Any, List, Optional, Union, cast
from pydantic import BaseModel, Field
import json
import os
from pathlib import Path

from core.utils.custom_logging import setup_logger
from core.mystical_systems.kabbalah_system.schemas import KabbalahProfile
from core.mystical_systems.zodiac_system.schemas import ZodiacProfile
from core.mystical_systems.numerology_system.schemas import NumerologyProfile

logger = setup_logger("profile_analyzer")

class ProfileAnalysisModel(BaseModel):
    """Analysis results for a governor profile"""
    governor_id: str = Field(..., description="Governor identifier")
    name: str = Field(..., description="Governor name")
    mystical_alignments: Dict[str, Any] = Field(
        default_factory=dict,
        description="Mystical system alignments"
    )
    trait_analysis: Dict[str, float] = Field(
        default_factory=dict,
        description="Trait analysis scores"
    )
    bitcoin_resonance: Optional[float] = Field(
        None,
        description="Overall Bitcoin resonance"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Recommendations for profile enhancement"
    )

class ProfileAnalyzer:
    """Analyzes governor profiles to extract insights and patterns"""
    
    def __init__(self):
        self.trait_cache = {}
        
    def analyze_profile(self, profile_data: Dict) -> ProfileAnalysisModel:
        """
        Analyze a governor profile to extract insights
        
        Args:
            profile_data: Dictionary containing profile data
            
        Returns:
            ProfileAnalysisModel object with extracted insights
        """
        traits = profile_data.get('traits', [])
        mystical_attrs = profile_data.get('mystical_attributes', {})
        
        # Analyze trait frequencies
        trait_frequencies = self._analyze_trait_frequencies(traits)
        
        # Find common patterns
        patterns = self._identify_patterns(traits, mystical_attrs)
        
        # Extract unique elements
        unique_elements = self._extract_unique_elements(profile_data)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            trait_frequencies,
            patterns,
            unique_elements
        )
        
        return ProfileAnalysisModel(
            governor_id=profile_data.get('id', ''),
            name=profile_data.get('name', ''),
            mystical_alignments=mystical_attrs,
            trait_analysis={
                'frequency_score': len(trait_frequencies),
                'pattern_score': len(patterns),
                'uniqueness_score': len(unique_elements)
            },
            bitcoin_resonance=self._calculate_bitcoin_resonance(profile_data),
            recommendations=recommendations
        )
    
    def _analyze_trait_frequencies(self, traits: List[str]) -> Dict[str, int]:
        """Count frequency of each trait"""
        frequencies = {}
        for trait in traits:
            frequencies[trait] = frequencies.get(trait, 0) + 1
        return frequencies
    
    def _identify_patterns(
        self,
        traits: List[str],
        mystical_attrs: Dict
    ) -> List[str]:
        """Identify common patterns in traits and attributes"""
        patterns = []
        
        # Look for repeated elements
        seen = set()
        for trait in traits:
            if trait in seen:
                patterns.append(f"Repeated trait: {trait}")
            seen.add(trait)
            
        # Check mystical attribute patterns
        if mystical_attrs:
            for attr, value in mystical_attrs.items():
                if isinstance(value, (int, float)) and value > 0.7:
                    patterns.append(f"Strong {attr}: {value}")
                    
        return patterns
    
    def _extract_unique_elements(self, profile_data: Dict) -> List[str]:
        """Extract unique/distinctive elements from the profile"""
        unique_elements = []
        
        # Check for rare traits
        if 'traits' in profile_data:
            for trait in profile_data['traits']:
                if trait not in self.trait_cache:
                    unique_elements.append(f"Unique trait: {trait}")
                    self.trait_cache[trait] = 1
                    
        # Check for unique attribute combinations
        if 'mystical_attributes' in profile_data:
            attrs = profile_data['mystical_attributes']
            if len(attrs) >= 3:
                unique_elements.append("Complex attribute combination")
                
        return unique_elements
    
    def _generate_recommendations(
        self,
        frequencies: Dict[str, int],
        patterns: List[str],
        unique_elements: List[str]
    ) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Check trait balance
        if len(frequencies) < 3:
            recommendations.append("Consider adding more diverse traits")
            
        # Check for patterns
        if len(patterns) > 3:
            recommendations.append("Profile shows strong thematic consistency")
        
        # Check uniqueness
        if len(unique_elements) > 2:
            recommendations.append("Profile has distinctive characteristics")
            
        return recommendations

    def _calculate_bitcoin_resonance(self, profile_data: Dict) -> float:
        """Calculate Bitcoin resonance score based on profile attributes"""
        score = 0.0
        
        # Check for Bitcoin-related traits
        bitcoin_traits = {'decentralized', 'cryptographic', 'immutable', 'trustless'}
        profile_traits = set(profile_data.get('traits', []))
        trait_overlap = len(bitcoin_traits.intersection(profile_traits))
        score += trait_overlap * 0.2  # 20% per matching trait
        
        # Check mystical attributes that align with Bitcoin
        mystical_attrs = profile_data.get('mystical_attributes', {})
        if mystical_attrs.get('digital_sovereignty', 0) > 0.5:
            score += 0.2
            
        return min(score, 1.0)  # Cap at 1.0 