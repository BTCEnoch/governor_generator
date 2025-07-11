"""
Migration script to reorganize governor trait data into the new standardized structure.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
from datetime import datetime

from core.governors.traits.schemas.trait_schemas import (
    GovernorTraits,
    CanonicalTraits,
    EnhancedTraits,
    MysticalTraits,
    PersonalityTraits,
    VisualTraits,
    ElementType,
    AlignmentType
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TraitMigrator:
    """Handles migration of governor trait data to new structure"""
    
    def __init__(self):
        """Initialize the migrator"""
        self.root_dir = Path("data/governors")
        self.indexes_dir = self.root_dir / "indexes"
        self.traits_dir = self.root_dir / "traits"
        
        # Ensure new directories exist
        for subdir in ["canonical", "enhanced", "mystical", "personality", "visual"]:
            (self.traits_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    def migrate_all_governors(self):
        """Migrate trait data for all governors"""
        try:
            # Load all source files
            canonical_data = self._load_json("canonical_traits.json")
            enhanced_data = self._load_json("trait_definitions.json")
            mystical_data = self._load_json("mystical_traits.json")
            personality_data = self._load_json("personality_traits.json")
            
            # Load visual data from markdown
            visual_data = self._load_visual_data()
            
            # Get list of all governor IDs
            governor_ids = self._extract_governor_ids(canonical_data)
            logger.info(f"Found {len(governor_ids)} governors to migrate")
            
            # Migrate each governor's traits
            for governor_id in governor_ids:
                logger.info(f"Migrating traits for {governor_id}")
                self.migrate_governor(
                    governor_id,
                    canonical_data,
                    enhanced_data,
                    mystical_data,
                    personality_data,
                    visual_data
                )
            
            logger.info("Migration complete")
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            raise
    
    def migrate_governor(
        self,
        governor_id: str,
        canonical_data: Dict,
        enhanced_data: Dict,
        mystical_data: Dict,
        personality_data: Dict,
        visual_data: Dict
    ):
        """Migrate trait data for a single governor"""
        try:
            # Extract traits for this governor
            canonical = self._extract_canonical_traits(governor_id, canonical_data)
            enhanced = self._extract_enhanced_traits(governor_id, enhanced_data)
            mystical = self._extract_mystical_traits(governor_id, mystical_data)
            personality = self._extract_personality_traits(governor_id, personality_data)
            visual = self._extract_visual_traits(governor_id, visual_data)
            
            # Save each trait type
            self._save_traits(governor_id, "canonical", canonical)
            self._save_traits(governor_id, "enhanced", enhanced)
            self._save_traits(governor_id, "mystical", mystical)
            self._save_traits(governor_id, "personality", personality)
            self._save_traits(governor_id, "visual", visual)
            
        except Exception as e:
            logger.error(f"Failed to migrate {governor_id}: {e}")
            raise
    
    def _load_json(self, filename: str) -> Dict:
        """Load JSON data from indexes directory"""
        try:
            with open(self.indexes_dir / filename) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load {filename}: {e}")
            return {}
            
    def _load_visual_data(self) -> Dict:
        """Load and parse visual trait data from markdown"""
        try:
            with open(self.indexes_dir / "VISUAL_TRAIT_INDEX.md") as f:
                content = f.read()
                
            # Parse markdown into structured data
            # This is a simplified version - would need proper markdown parsing
            return {
                "form_types": {
                    "ETHEREAL": {
                        "description": "Pure light and energy form",
                        "abilities": ["Phase shifting", "Energy manipulation"]
                    }
                },
                "color_schemes": {
                    "PRISMATIC": {
                        "meaning": "Universal wisdom",
                        "powers": ["All-element mastery"]
                    }
                },
                "sacred_geometry": {
                    "MERKABA": {
                        "meaning": "Divine light vehicle",
                        "value": 1
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to load visual data: {e}")
            return {}
    
    def _extract_governor_ids(self, canonical_data: Dict) -> list:
        """Extract list of governor IDs from canonical data"""
        governor_ids = []
        for aethyr in canonical_data:
            for governor in aethyr["governors"]:
                governor_ids.append(governor["name"])
        return governor_ids
    
    def _extract_canonical_traits(
        self,
        governor_id: str,
        canonical_data: Dict
    ) -> Dict:
        """Extract canonical traits for a governor"""
        for aethyr in canonical_data:
            for governor in aethyr["governors"]:
                if governor["name"] == governor_id:
                    return {
                        "name": governor["name"],
                        "aethyr": aethyr["aethyr_name"],
                        "aethyr_number": aethyr["aethyr_number"],
                        "region": governor["region"],
                        "correspondence": aethyr["correspondence"],
                        "personality": governor["canonical_traits"]["personality"],
                        "domain": governor["canonical_traits"]["domain"],
                        "visual_motif": governor["canonical_traits"]["visual_motif"],
                        "letter_influence": governor["canonical_traits"]["letter_influence"],
                        "version": "1.0.0"
                    }
        return {}
    
    def _extract_enhanced_traits(
        self,
        governor_id: str,
        enhanced_data: Dict
    ) -> Dict:
        """Extract enhanced trait definitions for a governor"""
        enhanced_traits = {}
        for trait_name, trait_data in enhanced_data.items():
            if trait_data.get("source") == governor_id:
                enhanced_traits[trait_name] = {
                    "trait_name": trait_name,
                    "definition": trait_data["definition"],
                    "source": trait_data["source"],
                    "correspondences": trait_data["correspondences"],
                    "practical_application": trait_data["practical_application"],
                    "version": "1.0.0"
                }
        return enhanced_traits
    
    def _extract_mystical_traits(
        self,
        governor_id: str,
        mystical_data: Dict
    ) -> Dict:
        """Extract mystical traits for a governor"""
        if governor_id in mystical_data:
            data = mystical_data[governor_id]
            return {
                "element": data["element"],
                "alignment": data["alignment"],
                "zodiac": data["zodiac"],
                "tarot": data["tarot"],
                "sephirot": data["sephirot"],
                "angel": data["angel"],
                "number": data["number"],
                "version": "1.0.0"
            }
        return {}
    
    def _extract_personality_traits(
        self,
        governor_id: str,
        personality_data: Dict
    ) -> Dict:
        """Extract personality traits for a governor"""
        if governor_id in personality_data:
            data = personality_data[governor_id]
            return {
                "archetype": data["archetype"],
                "primary_traits": data["primary_traits"],
                "secondary_traits": data["secondary_traits"],
                "teaching_style": data["teaching_style"],
                "approach": data["approach"],
                "tone": data["tone"],
                "version": "1.0.0"
            }
        return {}
    
    def _extract_visual_traits(
        self,
        governor_id: str,
        visual_data: Dict
    ) -> Dict:
        """Extract visual traits for a governor"""
        # For now use default values since we need proper markdown parsing
        return {
            "form_type": "ETHEREAL",
            "color_scheme": "PRISMATIC",
            "sacred_geometry": ["MERKABA"],
            "manifestation": "Pure light and energy form",
            "effects": ["Phase shifting", "Energy manipulation"],
            "version": "1.0.0"
        }
    
    def _save_traits(
        self,
        governor_id: str,
        trait_type: str,
        trait_data: Dict
    ):
        """Save trait data to new structure"""
        if not trait_data:
            return
            
        file_path = self.traits_dir / trait_type / f"{governor_id.lower()}_{trait_type}.json"
        with open(file_path, "w") as f:
            json.dump(trait_data, f, indent=2)
            logger.info(f"Saved {trait_type} traits for {governor_id}")

def main():
    """Run the trait migration"""
    migrator = TraitMigrator()
    migrator.migrate_all_governors()

if __name__ == "__main__":
    main() 