"""
Trait interpreter system for governor personality processing.
Provides semantic understanding of traits from binary representations.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class TraitUnderstanding:
    """Complete semantic understanding of a trait"""
    name: str
    definition: str
    category: str
    usage_context: str
    ai_impact: str
    related_traits: List[str]
    mystical_correspondences: Optional[Dict[str, Any]]

class TraitInterpreter:
    """Interprets binary trait data into full semantic understanding"""
    
    def __init__(self, trait_index_manager):
        self.logger = logging.getLogger(__name__)
        self.trait_index = trait_index_manager
        self.trait_cache = {}
        
    def interpret_binary_traits(self, binary_data: bytes) -> List[TraitUnderstanding]:
        """Convert binary trait data into full semantic understanding
        
        Args:
            binary_data: 16-byte binary trait representation
            
        Returns:
            List of TraitUnderstanding objects with full semantic meaning
        """
        # Extract trait flags from binary data
        trait_flags = self._decode_binary_traits(binary_data)
        
        # Look up full definitions
        understandings = []
        for trait_name in trait_flags:
            understanding = self._get_trait_understanding(trait_name)
            if understanding:
                understandings.append(understanding)
                
        return understandings
    
    def _decode_binary_traits(self, binary_data: bytes) -> List[str]:
        """Extract trait names from binary format
        
        Args:
            binary_data: 16-byte binary trait data
            
        Returns:
            List of trait names that are active
        """
        # First 4 bytes are header
        if binary_data[0:4] != b'VIS1':
            raise ValueError("Invalid trait data header")
            
        active_traits = []
        
        # Decode form type (1 byte)
        form_type = binary_data[4]
        if form_type <= 7:
            active_traits.append(f"Form_{form_type}")
            
        # Decode color scheme (1 byte)  
        color = binary_data[5]
        if color <= 7:
            active_traits.append(f"Color_{color}")
            
        # Decode geometry patterns (1 byte)
        geometry = binary_data[6]
        for i in range(8):
            if geometry & (1 << i):
                active_traits.append(f"Geometry_{i}")
                
        # Decode environmental effects (1 byte)
        effects = binary_data[7]
        for i in range(8):
            if effects & (1 << i):
                active_traits.append(f"Effect_{i}")
                
        # Continue decoding remaining bytes...
        
        return active_traits
    
    def _get_trait_understanding(self, trait_name: str) -> Optional[TraitUnderstanding]:
        """Get full semantic understanding of a trait
        
        Args:
            trait_name: Name of the trait to look up
            
        Returns:
            TraitUnderstanding if found, None if not found
        """
        # Check cache first
        if trait_name in self.trait_cache:
            return self.trait_cache[trait_name]
            
        # Look up in trait index
        trait_data = self.trait_index.get_trait_data(trait_name)
        if not trait_data:
            self.logger.warning(f"No definition found for trait: {trait_name}")
            return None
            
        # Create understanding object
        understanding = TraitUnderstanding(
            name=trait_data["name"],
            definition=trait_data["definition"],
            category=trait_data["category"],
            usage_context=trait_data["usage_context"],
            ai_impact=trait_data["ai_personality_impact"],
            related_traits=trait_data.get("related_traits", []),
            mystical_correspondences=trait_data.get("mystical_correspondences")
        )
        
        # Cache for future use
        self.trait_cache[trait_name] = understanding
        
        return understanding
        
    def get_trait_relationships(self, trait_name: str) -> Dict[str, List[str]]:
        """Get relationships between traits
        
        Args:
            trait_name: Name of trait to find relationships for
            
        Returns:
            Dictionary mapping relationship types to related trait names
        """
        understanding = self._get_trait_understanding(trait_name)
        if not understanding:
            return {}
            
        relationships = {
            "enhances": [],
            "conflicts": [],
            "requires": [],
            "suggests": []
        }
        
        # Look up relationships in trait index
        trait_data = self.trait_index.get_trait_data(trait_name)
        if trait_data and "relationships" in trait_data:
            relationships.update(trait_data["relationships"])
            
        return relationships
        
    def explain_trait_combination(self, traits: List[str]) -> str:
        """Generate explanation of how traits work together
        
        Args:
            traits: List of trait names to explain
            
        Returns:
            Natural language explanation of trait interactions
        """
        understandings: List[TraitUnderstanding] = []
        for trait in traits:
            understanding = self._get_trait_understanding(trait)
            if understanding:
                understandings.append(understanding)
                
        if not understandings:
            return "No trait information available"
            
        # Generate explanation
        explanation = ["This combination of traits creates the following effects:"]
        
        # Group by category
        by_category: Dict[str, List[TraitUnderstanding]] = {}
        for u in understandings:
            if u.category not in by_category:
                by_category[u.category] = []
            by_category[u.category].append(u)
            
        # Explain each category
        for category, category_traits in by_category.items():
            explanation.append(f"\n{category.title()}:")
            for trait in category_traits:
                explanation.append(f"- {trait.name}: {trait.definition}")
                if trait.usage_context:
                    explanation.append(f"  Context: {trait.usage_context}")
                    
        # Add interaction effects
        explanation.append("\nInteractions:")
        for i, trait1 in enumerate(understandings):
            for trait2 in understandings[i+1:]:
                relationships = self.get_trait_relationships(trait1.name)
                if trait2.name in relationships["enhances"]:
                    explanation.append(f"- {trait1.name} enhances {trait2.name}")
                if trait2.name in relationships["conflicts"]:
                    explanation.append(f"- {trait1.name} conflicts with {trait2.name}")
                    
        return "\n".join(explanation) 