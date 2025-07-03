import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from unified_profiler.interfaces.base_system import BaseMysticalSystem, MysticalProfile
from typing import Dict, Any, List, Optional

class TarotSystem(BaseMysticalSystem):
    """Tarot card system for mystical profiling"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config or {})
        self.system_name = "tarot"
        print("Initialized TarotSystem")
    
    def generate_profile(self, governor_data: Dict) -> MysticalProfile:
        """Generate tarot profile for a governor using actual tarot logic"""
        from mystical_systems.tarot_system.engines.governor_tarot_assigner import GovernorTarotAssigner
        
        governor_name = governor_data.get("name", "Unknown")
        
        # Use the actual tarot assignment engine
        assigner = GovernorTarotAssigner()
        tarot_profile = assigner.assign_tarot_to_governor(governor_data)
        
        # Extract card names for influences
        primary_card_name = tarot_profile.primary_card.name
        secondary_card_names = [card.name for card in tarot_profile.secondary_cards]
        shadow_card_name = tarot_profile.shadow_card.name
        
        # Create symbolic elements from actual cards
        symbolic_elements = [
            f"{primary_card_name} energy",
            f"{tarot_profile.primary_card.suit.value} suit resonance"
        ]
        
        # Generate conflict sources from shadow card
        conflict_sources = [
            f"{shadow_card_name} challenges",
            f"{tarot_profile.shadow_card.suit.value} suit tensions"
        ]
        
        # Create growth paths from card themes
        growth_paths = []
        for theme in tarot_profile.storyline_themes[:2]:
            growth_paths.append(f"mastering {theme}")
        
        # Build mystical profile using actual tarot data
        profile = MysticalProfile(
            system_name=self.system_name,
            governor_name=governor_name,
            primary_influences=[primary_card_name],
            secondary_influences=secondary_card_names,
            personality_modifiers=tarot_profile.personality_modifiers,
            storyline_themes=tarot_profile.storyline_themes,
            symbolic_elements=symbolic_elements,
            conflict_sources=conflict_sources,
            growth_paths=growth_paths if growth_paths else ["tarot mastery", "intuitive development"],
            metadata={
                "tarot_deck": "rider_waite",
                "reading_type": "governor_assignment",
                "primary_card_id": tarot_profile.primary_card.id,
                "secondary_card_ids": [card.id for card in tarot_profile.secondary_cards],
                "shadow_card_id": tarot_profile.shadow_card.id,
                "magical_affinities": tarot_profile.magical_affinities
            }
        )
        
        print(f"Generated tarot profile for {governor_name}: Primary={primary_card_name}, Shadow={shadow_card_name}")
        return profile
    
    def get_system_info(self) -> Dict[str, Any]:
        """Return tarot system metadata"""
        return {
            "name": "Tarot System",
            "version": "1.0",
            "description": "Tarot card divination and personality profiling",
            "capabilities": ["divination", "personality_analysis", "symbolic_guidance"]
        }
    
    def validate_profile(self, profile: MysticalProfile) -> bool:
        """Validate tarot profile"""
        if profile.system_name != "tarot":
            return False
        return True
    
    def _load_database(self):
        return {"cards_loaded": 78}
