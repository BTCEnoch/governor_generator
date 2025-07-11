"""
Governor Trait Generation System

This module handles the generation and management of governor traits,
integrating mystical correspondences, personality aspects, and visual
manifestations with Bitcoin-based randomness.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
from pathlib import Path
import random
from dataclasses import asdict

from core.utils.custom_logging import setup_logger
from core.utils.mystical.bitcoin_integration import get_bitcoin_entropy
from .schemas.core_schemas import TraitIndex, TraitEntry, TraitMetadata
from .schemas.trait_schemas import (
    ElementType,
    AlignmentType,
    CanonicalTraits,
    EnhancedTraits,
    MysticalTraits,
    PersonalityTraits,
    VisualTraits,
    GovernorTraits
)

logger = setup_logger(__name__)

class TraitGenerator:
    """
    Generates and manages governor traits using mystical correspondences
    and Bitcoin-based randomness.
    """
    
    def __init__(self, data_path: Path = Path("data/traits")):
        """Initialize the trait generator"""
        self.data_path = Path(data_path)
        self.trait_index = self._load_trait_index()
        self.correspondences = self._load_correspondences()
        
        logger.info("🎭 Trait Generator initialized")
        
    def generate_governor_traits(
        self,
        governor_id: str,
        governor_number: int,
        seed_data: Optional[Dict] = None
    ) -> GovernorTraits:
        """
        Generate a complete set of traits for a governor
        
        Args:
            governor_id: Unique identifier for the governor
            governor_number: Governor's numerical designation (1-91)
            seed_data: Optional seed data to influence trait generation
            
        Returns:
            Complete set of governor traits
        """
        # Get Bitcoin-based entropy for randomization
        entropy = get_bitcoin_entropy(governor_id)
        
        # Generate canonical traits
        canonical = self._generate_canonical_traits(
            governor_number,
            entropy,
            seed_data
        )
        
        # Generate enhanced trait definitions
        enhanced = self._generate_enhanced_traits(
            canonical.personality,
            entropy
        )
        
        # Generate mystical alignments
        mystical = self._generate_mystical_traits(
            governor_number,
            canonical,
            entropy
        )
        
        # Generate personality aspects
        personality = self._generate_personality_traits(
            canonical,
            mystical,
            entropy
        )
        
        # Generate visual manifestation
        visual = self._generate_visual_traits(
            canonical,
            mystical,
            entropy
        )
        
        # Combine all traits
        traits = GovernorTraits(
            governor_id=governor_id,
            governor_number=governor_number,
            canonical=canonical,
            enhanced=enhanced,
            mystical=mystical,
            personality=personality,
            visual=visual,
            last_updated=datetime.now().isoformat()
        )
        
        logger.info(f"✨ Generated traits for Governor {governor_number}")
        return traits
        
    def _generate_canonical_traits(
        self,
        governor_number: int,
        entropy: str,
        seed_data: Optional[Dict]
    ) -> CanonicalTraits:
        """Generate core canonical traits"""
        # Use seed data if provided, otherwise generate
        if seed_data and 'canonical' in seed_data:
            return CanonicalTraits(**seed_data['canonical'])
            
        # Calculate Aethyr correspondence
        aethyr_num = ((governor_number - 1) // 3) + 1
        aethyr = f"LIL{aethyr_num:02d}"
        
        # Select region and correspondence
        region = self._select_with_entropy(
            self.correspondences['regions'],
            entropy[:8]
        )
        correspondence = self._select_with_entropy(
            self.correspondences['correspondences'],
            entropy[8:16]
        )
        
        # Generate personality traits
        personality = self._select_multiple_with_entropy(
            self.trait_index.entries,
            3,  # Select 3 primary personality traits
            entropy[16:24]
        )
        
        return CanonicalTraits(
            name=f"Governor_{governor_number}",  # Placeholder
            aethyr=aethyr,
            aethyr_number=aethyr_num,
            region=region,
            correspondence=correspondence,
            personality=[p.name for p in personality],
            domain=self._generate_domain(personality),
            visual_motif=self._generate_motif(personality),
            letter_influence=self._select_letters(governor_number)
        )
        
    def _generate_enhanced_traits(
        self,
        base_traits: List[str],
        entropy: str
    ) -> Dict[str, EnhancedTraits]:
        """Generate enhanced trait definitions"""
        enhanced = {}
        for trait in base_traits:
            # Find base trait entry
            base_entry = next(
                (e for e in self.trait_index.entries if e.name == trait),
                None
            )
            if base_entry:
                enhanced[trait] = EnhancedTraits(
                    trait_name=trait,
                    definition=base_entry.definition,
                    source=base_entry.metadata.source,
                    correspondences=base_entry.correspondences or [],
                    practical_application=self._generate_application(base_entry)
                )
        return enhanced
        
    def _generate_mystical_traits(
        self,
        governor_number: int,
        canonical: CanonicalTraits,
        entropy: str
    ) -> MysticalTraits:
        """Generate mystical alignments"""
        # Calculate elemental affinity
        element = self._calculate_element(governor_number, entropy[:8])
        
        # Determine alignment based on traits and number
        alignment = self._calculate_alignment(
            canonical.personality,
            entropy[8:16]
        )
        
        # Calculate zodiac correspondence
        zodiac = self._calculate_zodiac(governor_number)
        
        return MysticalTraits(
            element=element,
            alignment=alignment,
            zodiac=zodiac,
            tarot=self._calculate_tarot(governor_number),
            sephirot=self._calculate_sephirot(governor_number),
            angel=self._calculate_angel(governor_number),
            number=governor_number
        )
        
    def _generate_personality_traits(
        self,
        canonical: CanonicalTraits,
        mystical: MysticalTraits,
        entropy: str
    ) -> PersonalityTraits:
        """Generate personality characteristics"""
        # Determine archetype based on traits and alignments
        archetype = self._determine_archetype(
            canonical.personality,
            mystical.element,
            mystical.alignment
        )
        
        # Select teaching style based on archetype
        teaching_style = self._select_teaching_style(
            archetype,
            entropy[:8]
        )
        
        return PersonalityTraits(
            archetype=archetype,
            primary_traits=canonical.personality[:2],
            secondary_traits=canonical.personality[2:],
            teaching_style=teaching_style,
            approach=self._determine_approach(mystical.element),
            tone=self._determine_tone(mystical.alignment)
        )
        
    def _generate_visual_traits(
        self,
        canonical: CanonicalTraits,
        mystical: MysticalTraits,
        entropy: str
    ) -> VisualTraits:
        """Generate visual manifestation aspects"""
        # Determine base form from element and traits
        form = self._determine_form(
            mystical.element,
            canonical.personality
        )
        
        # Generate color scheme from correspondences
        colors = self._generate_colors(
            mystical.element,
            mystical.alignment,
            entropy[:8]
        )
        
        return VisualTraits(
            form_type=form,
            color_scheme=colors,
            sacred_geometry=self._select_sacred_geometry(mystical.number),
            manifestation=self._generate_manifestation(form, colors),
            effects=self._generate_visual_effects(mystical.element)
        )
        
    def _load_trait_index(self) -> TraitIndex:
        """Load the trait index from file"""
        index_path = self.data_path / "trait_index.json"
        return TraitIndex.load_from_file(str(index_path))  # Convert Path to str
        
    def _load_correspondences(self) -> Dict:
        """Load correspondence tables"""
        corresp_path = self.data_path / "correspondences.json"
        with open(corresp_path) as f:
            return json.load(f)
            
    def _select_with_entropy(self, options: List[str], entropy: str) -> str:
        """Select an option using Bitcoin-derived entropy"""
        index = int(entropy[:8], 16) % len(options)
        return options[index]
        
    def _select_multiple_with_entropy(
        self,
        options: List[TraitEntry],
        count: int,
        entropy: str
    ) -> List[TraitEntry]:
        """Select multiple options using entropy"""
        # Use entropy to shuffle
        random.seed(int(entropy[:8], 16))
        shuffled = list(options)
        random.shuffle(shuffled)
        return shuffled[:count]
        
    def _generate_domain(self, traits: List[TraitEntry]) -> str:
        """Generate domain of influence from traits"""
        domains = [t.category for t in traits]
        return " & ".join(sorted(set(domains)))
        
    def _generate_motif(self, traits: List[TraitEntry]) -> str:
        """Generate visual motif from traits"""
        elements = []
        for trait in traits:
            if trait.subcategory:
                elements.append(trait.subcategory)
        return " with ".join(elements) if elements else "Abstract Form"
        
    def _select_letters(self, number: int) -> List[str]:
        """Select Enochian letter influences"""
        # Implementation depends on Enochian letter system
        return [f"Letter_{number}"]  # Placeholder
        
    def _generate_application(self, trait: TraitEntry) -> str:
        """Generate practical application description"""
        return f"Application of {trait.name} in {trait.category}"
        
    def _calculate_element(
        self,
        number: int,
        entropy: str
    ) -> ElementType:
        """Calculate elemental affinity"""
        elements = list(ElementType)
        index = (number + int(entropy[:2], 16)) % len(elements)
        return elements[index]
        
    def _calculate_alignment(
        self,
        traits: List[str],
        entropy: str
    ) -> AlignmentType:
        """Calculate moral/ethical alignment"""
        alignments = list(AlignmentType)
        index = int(entropy[:4], 16) % len(alignments)
        return alignments[index]
        
    def _calculate_zodiac(self, number: int) -> str:
        """Calculate zodiac correspondence"""
        signs = [
            "Aries", "Taurus", "Gemini", "Cancer",
            "Leo", "Virgo", "Libra", "Scorpio",
            "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        return signs[(number - 1) % 12]
        
    def _calculate_tarot(self, number: int) -> str:
        """Calculate tarot correspondence"""
        return f"Major_{number % 22}"  # Placeholder
        
    def _calculate_sephirot(self, number: int) -> str:
        """Calculate sephirotic correspondence"""
        sephirot = [
            "Kether", "Chokmah", "Binah", "Chesed",
            "Geburah", "Tiphareth", "Netzach", "Hod",
            "Yesod", "Malkuth"
        ]
        return sephirot[(number - 1) % 10]
        
    def _calculate_angel(self, number: int) -> str:
        """Calculate angelic correspondence"""
        return f"Angel_{number}"  # Placeholder
        
    def _determine_archetype(
        self,
        traits: List[str],
        element: ElementType,
        alignment: AlignmentType
    ) -> str:
        """Determine governor's archetypal pattern"""
        # Complex archetype determination logic here
        return f"Archetype_{element.value}_{alignment.value}"
        
    def _select_teaching_style(self, archetype: str, entropy: str) -> str:
        """Select teaching style based on archetype"""
        styles = [
            "Direct Instruction",
            "Mystical Revelation",
            "Symbolic Teaching",
            "Experiential Learning",
            "Riddles and Puzzles"
        ]
        index = int(entropy[:4], 16) % len(styles)
        return styles[index]
        
    def _determine_approach(self, element: ElementType) -> str:
        """Determine interaction approach based on element"""
        approaches = {
            ElementType.FIRE: "Dynamic and Energetic",
            ElementType.WATER: "Flowing and Adaptive",
            ElementType.AIR: "Intellectual and Communicative",
            ElementType.EARTH: "Practical and Grounded",
            ElementType.SPIRIT: "Mystical and Transformative"
        }
        return approaches[element]
        
    def _determine_tone(self, alignment: AlignmentType) -> str:
        """Determine communication tone based on alignment"""
        # Implementation based on alignment type
        return f"Tone_{alignment.value}"
        
    def _determine_form(
        self,
        element: ElementType,
        traits: List[str]
    ) -> str:
        """Determine base manifestation form"""
        # Implementation based on element and traits
        return f"Form_{element.value}"
        
    def _generate_colors(
        self,
        element: ElementType,
        alignment: AlignmentType,
        entropy: str
    ) -> str:
        """Generate color scheme"""
        # Implementation based on element and alignment
        return f"Colors_{element.value}_{alignment.value}"
        
    def _select_sacred_geometry(self, number: int) -> List[str]:
        """Select sacred geometry patterns"""
        patterns = [
            "Circle",
            "Triangle",
            "Square",
            "Pentagram",
            "Hexagram",
            "Septagram",
            "Octagram",
            "Enneagram",
            "Decagram"
        ]
        return [patterns[(number - 1) % len(patterns)]]
        
    def _generate_manifestation(
        self,
        form: str,
        colors: str
    ) -> str:
        """Generate manifestation description"""
        return f"{form} with {colors}"
        
    def _generate_visual_effects(
        self,
        element: ElementType
    ) -> List[str]:
        """Generate visual effects based on element"""
        effects = {
            ElementType.FIRE: ["Flames", "Sparks", "Radiance"],
            ElementType.WATER: ["Ripples", "Mist", "Flow"],
            ElementType.AIR: ["Swirls", "Currents", "Whisps"],
            ElementType.EARTH: ["Crystals", "Patterns", "Growth"],
            ElementType.SPIRIT: ["Light", "Shadows", "Transformation"]
        }
        return effects[element] 