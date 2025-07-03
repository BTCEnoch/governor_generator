#!/usr/bin/env python3
"""
Governor Engine - Creates complete archetypal governor beings
Combines canonical traits + interview data + knowledge integration
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from canonical_trait_registry import CanonicalTraitRegistry, GovernorCanonical
from semantic_knowledge_integrator import SemanticKnowledgeIntegrator

logger = logging.getLogger(__name__)

@dataclass
class ArchetypalGovernor:
    """Complete archetypal governor being"""
    name: str
    # Canonical foundation
    canonical_personality: List[str]
    canonical_domain: str
    canonical_visual: str
    canonical_letters: List[str]
    aethyr_info: str
    region: str
    
    # Knowledge-base derived personality
    knowledge_selections: List[str]
    wisdom_traditions: List[str]
    formed_personality: List[str]
    
    # Synthesized archetypal essence
    archetypal_essence: Dict[str, Any]
    unique_signature: str

class GovernorEngine:
    """Engine for creating complete archetypal governor beings"""
    
    def __init__(self, base_path: Path = Path(".")):
        self.base_path = base_path
        self.canonical_registry = CanonicalTraitRegistry(base_path)
        self.governor_output_path = base_path / "governor_output"
        self.semantic_integrator = SemanticKnowledgeIntegrator(base_path / "knowledge_base")
        
    def create_archetypal_governor(self, governor_name: str) -> Optional[ArchetypalGovernor]:
        """Create complete archetypal governor by combining all data sources"""
        
        # 1. Get canonical foundation
        canonical = self.canonical_registry.get_governor_canonical(governor_name)
        if not canonical:
            logger.error(f"No canonical data found for {governor_name}")
            return None
        
        # 2. Get knowledge base selections (from Knowledge Engine)
        knowledge_selections = self._get_knowledge_selections(canonical)
        wisdom_traditions = self._determine_wisdom_traditions(canonical, knowledge_selections)
        
        # 3. Form personality from canonical + knowledge
        formed_personality = self._form_personality(canonical, knowledge_selections)
        
        # 4. Synthesize archetypal essence
        archetypal_essence = self._synthesize_archetypal_essence(canonical, knowledge_selections)
        
        # 5. Create unique signature
        unique_signature = self._create_unique_signature(canonical, knowledge_selections)
        
        # 6. Build complete archetypal governor
        archetypal_governor = ArchetypalGovernor(
            name=governor_name,
            # Canonical foundation
            canonical_personality=canonical.canonical_traits.personality,
            canonical_domain=canonical.canonical_traits.domain,
            canonical_visual=canonical.canonical_traits.visual_motif,
            canonical_letters=canonical.canonical_traits.letter_influence,
            aethyr_info=f"{canonical.aethyr_number} ({canonical.aethyr_name}) - {canonical.correspondence}",
            region=canonical.region,
            
            # Knowledge-derived personality
            knowledge_selections=knowledge_selections,
            wisdom_traditions=wisdom_traditions,
            formed_personality=formed_personality,
            
            # Synthesized essence
            archetypal_essence=archetypal_essence,
            unique_signature=unique_signature
        )
        
        return archetypal_governor
    
    def _get_knowledge_selections(self, canonical: GovernorCanonical) -> List[str]:
        """Get knowledge base selections using semantic knowledge retrieval"""
        try:
            # Convert canonical data to dictionary format for semantic integrator
            canonical_data = {
                "name": canonical.name,
                "aethyr_name": canonical.aethyr_name,
                "correspondence": canonical.correspondence,
                "canonical_traits": {
                    "domain": canonical.canonical_traits.domain,
                    "personality": canonical.canonical_traits.personality,
                    "visual_motif": canonical.canonical_traits.visual_motif,
                    "letter_influence": canonical.canonical_traits.letter_influence
                }
            }
            
            # Generate semantic knowledge profile
            knowledge_profile = self.semantic_integrator.get_semantic_knowledge_profile(canonical_data)
            
            # Extract knowledge selections from semantic matches
            selections = []
            
            # Add primary traditions
            selections.extend(knowledge_profile.primary_traditions)
            
            # Add top knowledge concepts (limited to prevent overwhelm)
            selections.extend(knowledge_profile.knowledge_concepts[:5])
            
            # Add wisdom elements
            selections.extend(knowledge_profile.wisdom_elements[:3])
            
            # Remove duplicates and return
            return list(set(selections))
            
        except Exception as e:
            logger.warning(f"Semantic knowledge retrieval failed for {canonical.name}: {e}")
            logger.info("Falling back to simple mapping")
            
                         # Fallback to simple mapping if semantic retrieval fails
            return self._get_knowledge_selections_fallback(canonical)
    
    def _get_knowledge_selections_fallback(self, canonical: GovernorCanonical) -> List[str]:
        """Fallback knowledge selection using simple mapping"""
        selections = []
        domain = canonical.canonical_traits.domain.lower()
        personality = [p.lower() for p in canonical.canonical_traits.personality]
        letters = [l.lower() for l in canonical.canonical_traits.letter_influence]
        
        # Map domain to knowledge areas
        if "spiritual" in domain:
            selections.extend(["hermetic_tradition", "mystical_philosophy"])
        if "leadership" in domain:
            selections.extend(["sacred_geometry", "classical_philosophy"])
        if "psychic" in domain or "emotional" in domain:
            selections.extend(["tarot_knowledge", "intuitive_wisdom"])
        if "cosmic" in domain or "order" in domain:
            selections.extend(["kabbalah", "sacred_mathematics"])
        
        # Map personality traits to knowledge
        if any("wise" in p for p in personality):
            selections.append("wisdom_traditions")
        if any("mysterious" in p for p in personality):
            selections.append("esoteric_knowledge")
        if any("protective" in p for p in personality):
            selections.append("guardian_wisdom")
        
        # Map letter influences to knowledge
        if any("transformation" in l for l in letters):
            selections.append("transformation_mysteries")
        if any("wisdom" in l for l in letters):
            selections.append("ancient_wisdom")
        if any("love" in l for l in letters):
            selections.append("compassion_teachings")
            
        return list(set(selections))  # Remove duplicates
    
    def _determine_wisdom_traditions(self, canonical: GovernorCanonical, knowledge_selections: List[str]) -> List[str]:
        """Determine which wisdom traditions this governor embodies"""
        traditions = []
        
        # Map knowledge selections to wisdom traditions
        for selection in knowledge_selections:
            if "hermetic" in selection:
                traditions.append("Hermetic Tradition")
            elif "kabbalah" in selection:
                traditions.append("Kabbalah")
            elif "tarot" in selection:
                traditions.append("Tarot Wisdom")
            elif "sacred_geometry" in selection or "mathematics" in selection:
                traditions.append("Sacred Geometry")
            elif "classical" in selection:
                traditions.append("Classical Philosophy")
            elif "mystical" in selection:
                traditions.append("Mystical Philosophy")
        
        # Ensure at least one tradition per governor
        if not traditions:
            traditions.append("Universal Wisdom")
            
        return traditions[:3]  # Limit to 3 primary traditions
    
    def _form_personality(self, canonical: GovernorCanonical, knowledge_selections: List[str]) -> List[str]:
        """Form complete personality from canonical traits + knowledge selections"""
        # Start with canonical personality as foundation
        formed = canonical.canonical_traits.personality.copy()
        
        # Add personality traits based on knowledge selections
        for selection in knowledge_selections:
            if "wisdom" in selection and "wise" not in formed:
                formed.append("knowledgeable")
            elif "mystical" in selection and "mystical" not in formed:
                formed.append("mystical")
            elif "sacred" in selection and "sacred" not in formed:
                formed.append("reverent")
            elif "transformation" in selection and "transformative" not in formed:
                formed.append("transformative")
        
        return formed[:5]  # Limit to 5 key personality traits
    
    def _load_interview_data(self, governor_name: str) -> Optional[Dict]:
        """Load interview data if available"""
        interview_file = self.governor_output_path / f"{governor_name}.json"
        
        if not interview_file.exists():
            return None
        
        try:
            with open(interview_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load interview data for {governor_name}: {e}")
            return None
    
    def _extract_interview_personality(self, interview_data: Dict) -> List[str]:
        """Extract personality traits from interview data"""
        if not interview_data:
            return []
        
        # Look for personality indicators in various blocks
        personality_traits = []
        
        # Check blocks for personality indicators
        blocks = interview_data.get("blocks", {})
        for block_name, block_data in blocks.items():
            if "personality" in block_name.lower():
                # Extract traits from personality-related blocks
                if isinstance(block_data, dict):
                    for q_num, q_data in block_data.items():
                        if isinstance(q_data, dict) and "answer" in q_data:
                            # Extract personality indicators from answers
                            answer = q_data["answer"].lower()
                            if "wisdom" in answer:
                                personality_traits.append("wisdom-focused")
                            if "compassion" in answer:
                                personality_traits.append("compassionate")
                            if "strength" in answer:
                                personality_traits.append("strong-willed")
        
        return personality_traits[:3]  # Limit to top 3
    
    def _extract_wisdom_traditions(self, interview_data: Dict) -> List[str]:
        """Extract wisdom traditions from interview data"""
        if not interview_data:
            return []
        
        # Look for tradition mentions
        traditions = interview_data.get("wisdom_traditions", [])
        if isinstance(traditions, list):
            return traditions
        
        return []
    
    def _synthesize_archetypal_essence(self, canonical: GovernorCanonical, knowledge_selections: List[str]) -> Dict:
        """Synthesize the unique archetypal essence of this governor"""
        
        essence = {
            "primary_archetype": canonical.canonical_traits.domain,
            "personality_synthesis": {
                "canonical_base": canonical.canonical_traits.personality,
                "knowledge_influences": knowledge_selections,
                "formed_personality": self._form_personality(canonical, knowledge_selections)
            },
            "power_manifestation": {
                "canonical_domain": canonical.canonical_traits.domain,
                "letter_influences": canonical.canonical_traits.letter_influence,
                "visual_presence": canonical.canonical_traits.visual_motif
            },
            "wisdom_integration": {
                "knowledge_selections": knowledge_selections,
                "wisdom_traditions": self._determine_wisdom_traditions(canonical, knowledge_selections)
            }
        }
        
        return essence
    
    def _merge_personality_traits(self, canonical_traits: List[str], interview_traits: List[str]) -> List[str]:
        """Merge canonical and interview personality traits"""
        # Canonical traits are the foundation
        merged = canonical_traits.copy()
        
        # Add non-conflicting interview traits
        for trait in interview_traits:
            if trait not in merged and len(merged) < 6:  # Limit to 6 total traits
                merged.append(trait)
        
        return merged
    
    def _create_unique_signature(self, canonical: GovernorCanonical, knowledge_selections: List[str]) -> str:
        """Create unique archetypal signature"""
        
        # Combine key elements for unique signature
        elements = [
            canonical.aethyr_name,
            canonical.canonical_traits.domain.replace(" ", "_"),
            canonical.region.replace(" ", "_"),
            "-".join(canonical.canonical_traits.letter_influence)
        ]
        
        # Add primary knowledge selection if available
        if knowledge_selections:
            primary_knowledge = knowledge_selections[0].replace("_", "-")
            elements.append(primary_knowledge)
        
        signature = "_".join(elements).upper()
        return signature

def test_governor_engine():
    """Test the Governor Engine"""
    try:
        print("🏛️ Testing Governor Engine...")
        
        engine = GovernorEngine()
        
        # Get available governors
        available = engine.canonical_registry.list_available_governors()
        print(f"📊 Available governors: {available}")
        
        if available:
            test_gov = available[0]  # Test with first available
            print(f"🧪 Creating archetypal governor for {test_gov}")
            
            archetypal = engine.create_archetypal_governor(test_gov)
            
            if archetypal:
                print(f"✅ Created archetypal governor: {archetypal.name}")
                print(f"   Canonical Domain: {archetypal.canonical_domain}")
                print(f"   Canonical Personality: {archetypal.canonical_personality}")
                print(f"   Letter Influences: {archetypal.canonical_letters}")
                print(f"   Aethyr: {archetypal.aethyr_info}")
                print(f"   Region: {archetypal.region}")
                print(f"   Unique Signature: {archetypal.unique_signature}")
                print(f"   Primary Archetype: {archetypal.archetypal_essence['primary_archetype']}")
                return True
            else:
                print(f"❌ Failed to create archetypal governor for {test_gov}")
                return False
        else:
            print("❌ No governors available for testing")
            return False
            
    except Exception as e:
        print(f"❌ Governor Engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_governor_engine() 