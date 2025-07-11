"""
Loads governor traits from dossier files into standardized trait structures.
"""

import json
from pathlib import Path
from typing import Dict, Optional
import logging

from .trait_index import (
    GovernorTraits,
    PersonaTraits,
    KnowledgeBase,
    ArchetypalCorrespondences,
    PolarTraits,
    Approaches,
    Tones,
    VisualAspects,
    VisualForm,
    VisualGeometry,
    VisualEnvironment,
    Element
)

logger = logging.getLogger(__name__)

class DossierLoader:
    """Loads and validates governor traits from dossier files"""
    
    def __init__(self, dossier_path: str = "governor_dossier"):
        self.dossier_path = Path(dossier_path)
        if not self.dossier_path.exists():
            raise ValueError(f"Dossier path {dossier_path} does not exist")
            
    def load_governor_traits(self, governor_id: str) -> Optional[GovernorTraits]:
        """Load traits for a specific governor from their dossier"""
        dossier_file = self.dossier_path / f"{governor_id}.json"
        if not dossier_file.exists():
            logger.error(f"No dossier found for governor {governor_id}")
            return None
            
        try:
            with open(dossier_file) as f:
                data = json.load(f)
                
            # Extract persona traits
            persona = PersonaTraits(
                name=data["persona"]["name"],
                title=data["persona"]["title"],
                element=Element(data["persona"]["element"]),
                aethyr=data["persona"]["aethyr"],
                essence=data["persona"]["essence"],
                angelic_role=data["persona"]["angelic_role"]
            )
            
            # Extract knowledge base
            knowledge = KnowledgeBase(
                traditions=data["persona"]["knowledge_base"]
            )
            
            # Extract archetypal correspondences
            correspondences = ArchetypalCorrespondences(
                tarot=data["persona"]["archetypal_correspondences"]["tarot"],
                sephirot=data["persona"]["archetypal_correspondences"]["sephirot"],
                zodiac_sign=data["persona"]["archetypal_correspondences"]["zodiac_sign"],
                zodiac_angel=data["persona"]["archetypal_correspondences"]["zodiac_angel"],
                numerology=data["persona"]["archetypal_correspondences"]["numerology"]
            )
            
            # Extract polar traits
            polar = PolarTraits(
                baseline_approach=data["persona"]["polar_traits"]["baseline_approach"],
                baseline_tone=data["persona"]["polar_traits"]["baseline_tone"],
                motive_alignment=data["persona"]["polar_traits"]["motive_alignment"],
                role_archetype=data["persona"]["polar_traits"]["role_archetype"],
                orientation=data["persona"]["polar_traits"]["orientation"],
                polarity=data["persona"]["polar_traits"]["polarity"],
                self_regard=data["persona"]["polar_traits"]["self_regard"],
                virtues=data["persona"]["polar_traits"]["virtues"],
                flaws=data["persona"]["polar_traits"]["flaws"]
            )
            
            # Extract approaches
            approaches = Approaches(
                bad=data["persona"]["approaches"]["bad"],
                average=data["persona"]["approaches"]["average"],
                good=data["persona"]["approaches"]["good"]
            )
            
            # Extract tones
            tones = Tones(
                bad=data["persona"]["tones"]["bad"],
                average=data["persona"]["tones"]["average"],
                good=data["persona"]["tones"]["good"]
            )
            
            # Extract visual aspects
            visual = VisualAspects(
                form=VisualForm(
                    name=data["visual_aspects"]["form"]["name"],
                    description=data["visual_aspects"]["form"]["description"]
                ),
                color=data["visual_aspects"]["color"],
                geometry=VisualGeometry(
                    patterns=data["visual_aspects"]["geometry"]["patterns"],
                    complexity=data["visual_aspects"]["geometry"]["complexity"]
                ),
                environment=VisualEnvironment(
                    effect_type=data["visual_aspects"]["environment"]["effect_type"],
                    radius=data["visual_aspects"]["environment"]["radius"],
                    intensity=data["visual_aspects"]["environment"]["intensity"]
                ),
                time_variations=data["visual_aspects"]["time_variations"],
                energy_signature=data["visual_aspects"]["energy_signature"],
                symbol_set=data["visual_aspects"]["symbol_set"],
                light_shadow=data["visual_aspects"]["light_shadow"],
                special_properties=data["visual_aspects"]["special_properties"]
            )
            
            # Create complete governor traits
            return GovernorTraits(
                governor_name=data["governor_name"],
                governor_id=data["governor_id"],
                persona=persona,
                knowledge_base=knowledge,
                archetypal_correspondences=correspondences,
                polar_traits=polar,
                approaches=approaches,
                tones=tones,
                visual_aspects=visual
            )
            
        except Exception as e:
            logger.error(f"Error loading traits for {governor_id}: {str(e)}")
            return None
            
    def load_all_governors(self) -> Dict[str, GovernorTraits]:
        """Load traits for all governors from dossiers"""
        governors = {}
        for dossier_file in self.dossier_path.glob("*.json"):
            if dossier_file.stem == "visual_aspects_generation_results":
                continue
            governor_id = dossier_file.stem
            traits = self.load_governor_traits(governor_id)
            if traits:
                governors[governor_id] = traits
        return governors 