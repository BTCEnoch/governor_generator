"""Script to update governor traits with clear definitions from knowledge base and external sources."""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, TypedDict, cast
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Add project root to PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.utils.custom_logging.custom_logger import setup_logger

logger = setup_logger(__name__)

class CanonicalTrait(TypedDict):
    personality: List[str]
    domain: str
    visual_motif: str
    letter_influence: List[str]

class Governor(TypedDict):
    name: str
    region: str
    canonical_traits: CanonicalTrait

class Aethyr(TypedDict):
    aethyr_number: int
    aethyr_name: str
    correspondence: str
    governors: List[Governor]

class EnochianConcept(TypedDict):
    name: str
    practical_wisdom: str
    interaction_triggers: List[str]

class EnochianArchive(TypedDict):
    key_concepts: List[EnochianConcept]

class TraitDefinition(TypedDict):
    name: str
    definition: str
    source: str
    correspondences: List[str]
    practical_application: str

class GovernorTraitUpdater:
    """Updates governor traits with clear definitions from knowledge base."""
    
    def __init__(self):
        self.canonical_traits: List[Aethyr] = self._load_canonical_traits()
        self.enochian_archive: EnochianArchive = self._load_enochian_archive()
        self.trait_definitions = self._initialize_trait_definitions()
        
    def _load_canonical_traits(self) -> List[Aethyr]:
        """Load canonical traits from JSON."""
        with open(project_root / "data/governors/indexes/canonical_traits.json") as f:
            return cast(List[Aethyr], json.load(f))
            
    def _load_enochian_archive(self) -> EnochianArchive:
        """Load Enochian knowledge archive."""
        with open(project_root / "data/knowledge/archives/governor_archives/enochian_magic_governor_archive.json") as f:
            return cast(EnochianArchive, json.load(f))
            
    def _initialize_trait_definitions(self) -> Dict[str, TraitDefinition]:
        """Initialize expanded trait definitions."""
        definitions: Dict[str, TraitDefinition] = {}
        
        # Add definitions from canonical traits
        for aethyr in self.canonical_traits:
            for governor in aethyr["governors"]:
                for trait in governor["canonical_traits"]["personality"]:
                    if trait not in definitions:
                        definitions[trait] = {
                            "name": trait,
                            "definition": f"A trait associated with {governor['name']} of {aethyr['aethyr_name']} Aethyr",
                            "source": "Canonical Traits",
                            "correspondences": [
                                aethyr["correspondence"],
                                governor["canonical_traits"]["domain"],
                                governor["region"]
                            ],
                            "practical_application": f"Manifests through {governor['canonical_traits']['visual_motif']}"
                        }
                        
        # Enhance with Enochian archive knowledge
        for concept in self.enochian_archive["key_concepts"]:
            related_traits = [
                trait for trait in definitions.keys()
                if trait.lower() in concept["practical_wisdom"].lower()
            ]
            for trait in related_traits:
                if trait in definitions:
                    definitions[trait]["definition"] += f"\n\nEnochian Context: {concept['practical_wisdom']}"
                    definitions[trait]["correspondences"].extend(concept["interaction_triggers"])
                    
        return definitions
        
    def update_trait_definitions_file(self) -> None:
        """Save expanded trait definitions to file."""
        output_file = project_root / "data/governors/indexes/trait_definitions.json"
        with open(output_file, 'w') as f:
            json.dump(self.trait_definitions, f, indent=2)
        logger.info(f"Updated trait definitions saved to {output_file}")
            
def main():
    """Main function to update trait definitions."""
    updater = GovernorTraitUpdater()
    updater.update_trait_definitions_file()
            
if __name__ == "__main__":
    main() 