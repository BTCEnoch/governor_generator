"""
Artifact Manager
Generates and manages game artifacts based on governor personalities and contexts
"""

import random
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from .schemas.asset_schemas import (
    GameAsset, AssetType, AssetRarity, ElementalAffinity, 
    AssetSource, AssetEffect, AssetRequirement, AssetTemplate
)

logger = logging.getLogger(__name__)

class ArtifactManager:
    """
    Manages the creation and properties of game artifacts
    """
    
    def __init__(self):
        """Initialize the artifact manager with templates and patterns"""
        self.artifact_templates = self._load_artifact_templates()
        self.name_components = self._load_name_components()
        self.effect_library = self._load_effect_library()
        
        logger.info("ArtifactManager initialized")
    
    def create_artifact(self,
                       rarity: AssetRarity,
                       elemental_affinity: Optional[ElementalAffinity] = None,
                       source: Optional[AssetSource] = None,
                       creator_governor: Optional[str] = None,
                       context: Optional[Dict[str, Any]] = None) -> GameAsset:
        """
        Create a new artifact with specified parameters
        
        Args:
            rarity: Rarity level of the artifact
            elemental_affinity: Elemental affinity (optional)
            source: How the artifact was obtained
            creator_governor: Governor who created/blessed the artifact
            context: Additional context for generation (questline, theme, etc.)
            
        Returns:
            Generated GameAsset artifact
        """
        logger.info(f"Creating {rarity.value} artifact")
        
        # Generate base properties
        name = self._generate_artifact_name(rarity, elemental_affinity, creator_governor, context)
        description = self._generate_artifact_description(name, rarity, elemental_affinity, creator_governor, context)
        
        # Create base artifact
        artifact = GameAsset(
            id="",  # Auto-generated
            name=name,
            description=description,
            type=AssetType.ARTIFACT,
            rarity=rarity,
            elemental_affinity=elemental_affinity,
            created_by_governor=creator_governor,
            base_value=self._calculate_base_value(rarity),
            lore_text=self._generate_lore_text(name, creator_governor, context),
            flavor_text=self._generate_flavor_text(rarity, elemental_affinity)
        )
        
        # Add effects based on rarity and affinity
        artifact.effects = self._generate_artifact_effects(rarity, elemental_affinity, context)
        
        # Add requirements based on rarity
        artifact.requirements = self._generate_artifact_requirements(rarity, elemental_affinity)
        
        # Set sources
        if source:
            artifact.sources = [source]
        else:
            artifact.sources = self._determine_likely_sources(rarity, elemental_affinity)
        
        # Generate tags
        artifact.tags = self._generate_artifact_tags(artifact)
        
        logger.info(f"Created artifact: {name} ({rarity.value})")
        return artifact
    
    def create_artifact_for_governor(self, 
                                    governor_data: Dict[str, Any],
                                    rarity: AssetRarity,
                                    context: Optional[Dict[str, Any]] = None) -> GameAsset:
        """
        Create an artifact specifically themed for a governor
        
        Args:
            governor_data: Complete governor profile
            rarity: Desired rarity level
            context: Additional context
            
        Returns:
            Governor-themed artifact
        """
        governor_name = governor_data.get('name', 'Unknown')
        element = governor_data.get('element', 'Spirit')
        
        # Convert element string to ElementalAffinity
        elemental_affinity = None
        try:
            elemental_affinity = ElementalAffinity(element.lower())
        except ValueError:
            elemental_affinity = ElementalAffinity.SPIRIT
        
        # Create context with governor information
        governor_context = {
            'governor': governor_name,
            'element': element,
            'wisdom_domains': governor_data.get('wisdom_domains', []),
            'personality_traits': governor_data.get('personality_traits', {}),
            **(context or {})
        }
        
        return self.create_artifact(
            rarity=rarity,
            elemental_affinity=elemental_affinity,
            source=AssetSource.GOVERNOR_GIFT,
            creator_governor=governor_name,
            context=governor_context
        )
    
    def _generate_artifact_name(self, 
                               rarity: AssetRarity,
                               elemental_affinity: Optional[ElementalAffinity],
                               creator_governor: Optional[str],
                               context: Optional[Dict[str, Any]]) -> str:
        """Generate an appropriate name for the artifact"""
        
        # Base name components by rarity
        rarity_prefixes = {
            AssetRarity.COMMON: ["Simple", "Basic", "Plain", "Common"],
            AssetRarity.UNCOMMON: ["Refined", "Quality", "Improved", "Enhanced"],
            AssetRarity.RARE: ["Exceptional", "Masterwork", "Superior", "Rare"],
            AssetRarity.EPIC: ["Legendary", "Epic", "Magnificent", "Extraordinary"],
            AssetRarity.LEGENDARY: ["Mythical", "Legendary", "Fabled", "Renowned"],
            AssetRarity.MYTHIC: ["Ancient", "Primordial", "Mythic", "Eternal"],
            AssetRarity.DIVINE: ["Divine", "Sacred", "Celestial", "Transcendent"]
        }
        
        # Elemental descriptors
        elemental_descriptors = {
            ElementalAffinity.FIRE: ["Flame", "Ember", "Blaze", "Inferno", "Solar"],
            ElementalAffinity.WATER: ["Wave", "Tide", "Flow", "Deep", "Aqueous"],
            ElementalAffinity.AIR: ["Wind", "Storm", "Breeze", "Gale", "Ethereal"],
            ElementalAffinity.EARTH: ["Stone", "Crystal", "Mountain", "Root", "Granite"],
            ElementalAffinity.SPIRIT: ["Soul", "Essence", "Spirit", "Astral", "Divine"],
            ElementalAffinity.VOID: ["Void", "Shadow", "Dark", "Null", "Abyssal"],
            ElementalAffinity.BALANCE: ["Harmony", "Balance", "Unity", "Equilibrium", "Centered"]
        }
        
        # Artifact types
        artifact_types = [
            "Amulet", "Ring", "Crown", "Staff", "Orb", "Crystal", "Tome", 
            "Chalice", "Blade", "Shield", "Cloak", "Medallion", "Rune", 
            "Scepter", "Mirror", "Pendant", "Bracelet", "Circlet"
        ]
        
        # Build name
        parts = []
        
        # Add rarity prefix
        parts.append(random.choice(rarity_prefixes[rarity]))
        
        # Add elemental descriptor if applicable
        if elemental_affinity and elemental_affinity != ElementalAffinity.BALANCE:
            parts.append(random.choice(elemental_descriptors[elemental_affinity]))
        
        # Add artifact type
        parts.append(random.choice(artifact_types))
        
        # Add governor suffix if created by governor
        if creator_governor and rarity in [AssetRarity.LEGENDARY, AssetRarity.MYTHIC, AssetRarity.DIVINE]:
            parts.append(f"of {creator_governor}")
        
        return " ".join(parts)
    
    def _generate_artifact_description(self,
                                     name: str,
                                     rarity: AssetRarity,
                                     elemental_affinity: Optional[ElementalAffinity],
                                     creator_governor: Optional[str],
                                     context: Optional[Dict[str, Any]]) -> str:
        """Generate a description for the artifact"""
        
        base_descriptions = {
            AssetRarity.COMMON: f"A {name.lower()} crafted with basic techniques.",
            AssetRarity.UNCOMMON: f"A well-made {name.lower()} showing skilled craftsmanship.",
            AssetRarity.RARE: f"An exceptional {name.lower()} imbued with mystical properties.",
            AssetRarity.EPIC: f"A magnificent {name.lower()} radiating powerful energy.",
            AssetRarity.LEGENDARY: f"A legendary {name.lower()} spoken of in ancient tales.",
            AssetRarity.MYTHIC: f"A mythical {name.lower()} from the dawn of creation.",
            AssetRarity.DIVINE: f"A divine {name.lower()} blessed by celestial forces."
        }
        
        description = base_descriptions[rarity]
        
        # Add elemental description
        if elemental_affinity:
            elemental_text = {
                ElementalAffinity.FIRE: " It pulses with inner flame and warmth.",
                ElementalAffinity.WATER: " It flows with the essence of pure water.",
                ElementalAffinity.AIR: " It seems to float on invisible currents.",
                ElementalAffinity.EARTH: " It feels solid and eternal as stone.",
                ElementalAffinity.SPIRIT: " It resonates with spiritual energy.",
                ElementalAffinity.VOID: " It absorbs light and shadow alike.",
                ElementalAffinity.BALANCE: " It harmonizes all elemental forces."
            }
            description += elemental_text.get(elemental_affinity, "")
        
        # Add governor information
        if creator_governor:
            description += f" Created by the governor {creator_governor}."
        
        return description
    
    def _generate_artifact_effects(self,
                                 rarity: AssetRarity,
                                 elemental_affinity: Optional[ElementalAffinity],
                                 context: Optional[Dict[str, Any]]) -> List[AssetEffect]:
        """Generate effects for the artifact based on rarity and affinity"""
        
        effects = []
        
        # Number of effects based on rarity
        effect_counts = {
            AssetRarity.COMMON: 1,
            AssetRarity.UNCOMMON: 1,
            AssetRarity.RARE: 2,
            AssetRarity.EPIC: 2,
            AssetRarity.LEGENDARY: 3,
            AssetRarity.MYTHIC: 3,
            AssetRarity.DIVINE: 4
        }
        
        num_effects = effect_counts[rarity]
        
        for i in range(num_effects):
            effect = self._create_random_effect(rarity, elemental_affinity, i == 0)
            effects.append(effect)
        
        return effects
    
    def _create_random_effect(self,
                            rarity: AssetRarity,
                            elemental_affinity: Optional[ElementalAffinity],
                            is_primary: bool) -> AssetEffect:
        """Create a random effect appropriate for the artifact"""
        
        # Effect magnitudes by rarity
        magnitude_ranges = {
            AssetRarity.COMMON: (0.1, 0.3),
            AssetRarity.UNCOMMON: (0.2, 0.5),
            AssetRarity.RARE: (0.4, 0.8),
            AssetRarity.EPIC: (0.7, 1.2),
            AssetRarity.LEGENDARY: (1.0, 2.0),
            AssetRarity.MYTHIC: (1.5, 3.0),
            AssetRarity.DIVINE: (2.0, 5.0)
        }
        
        min_mag, max_mag = magnitude_ranges[rarity]
        magnitude = round(random.uniform(min_mag, max_mag), 2)
        
        # Effect types based on elemental affinity
        if elemental_affinity == ElementalAffinity.FIRE:
            effect_names = ["Fire Resistance", "Flame Boost", "Burning Strike", "Heat Aura"]
        elif elemental_affinity == ElementalAffinity.WATER:
            effect_names = ["Water Mastery", "Healing Flow", "Cleansing", "Tide Control"]
        elif elemental_affinity == ElementalAffinity.AIR:
            effect_names = ["Wind Walker", "Lightning Speed", "Storm Call", "Levitation"]
        elif elemental_affinity == ElementalAffinity.EARTH:
            effect_names = ["Stone Skin", "Crystal Sight", "Earth Bond", "Mountain's Endurance"]
        elif elemental_affinity == ElementalAffinity.SPIRIT:
            effect_names = ["Spirit Sight", "Astral Projection", "Divine Grace", "Soul Shield"]
        else:
            effect_names = ["Wisdom Boost", "Insight", "Clarity", "Focus"]
        
        effect_name = random.choice(effect_names)
        
        return AssetEffect(
            type="stat_boost" if is_primary else random.choice(["enhancement", "protection", "ability_grant"]),
            name=effect_name,
            description=f"Provides {effect_name.lower()} with magnitude {magnitude}",
            magnitude=magnitude,
            duration=None if rarity.value in ["legendary", "mythic", "divine"] else random.randint(30, 120)
        )
    
    # Helper methods (basic implementations)
    def _load_artifact_templates(self) -> Dict[str, AssetTemplate]:
        """Load artifact templates - placeholder for now"""
        return {}
    
    def _load_name_components(self) -> Dict[str, List[str]]:
        """Load name components - placeholder for now"""
        return {}
    
    def _load_effect_library(self) -> Dict[str, List[AssetEffect]]:
        """Load effect library - placeholder for now"""
        return {}
    
    def _calculate_base_value(self, rarity: AssetRarity) -> int:
        """Calculate base value based on rarity"""
        value_map = {
            AssetRarity.COMMON: 100,
            AssetRarity.UNCOMMON: 250,
            AssetRarity.RARE: 500,
            AssetRarity.EPIC: 1000,
            AssetRarity.LEGENDARY: 2500,
            AssetRarity.MYTHIC: 5000,
            AssetRarity.DIVINE: 10000
        }
        return value_map.get(rarity, 100)
    
    def _generate_lore_text(self, name: str, creator_governor: Optional[str], context: Optional[Dict[str, Any]]) -> str:
        """Generate lore text for artifact"""
        if creator_governor:
            return f"This {name.lower()} was crafted by {creator_governor} during ancient times."
        return f"The origins of this {name.lower()} are shrouded in mystery."
    
    def _generate_flavor_text(self, rarity: AssetRarity, elemental_affinity: Optional[ElementalAffinity]) -> str:
        """Generate flavor text for artifact"""
        return f"A {rarity.value} artifact that resonates with power."
    
    def _generate_artifact_requirements(self, rarity: AssetRarity, elemental_affinity: Optional[ElementalAffinity]) -> List[AssetRequirement]:
        """Generate requirements for artifact use"""
        requirements = []
        
        # Level requirements based on rarity
        level_req = {
            AssetRarity.COMMON: 1,
            AssetRarity.UNCOMMON: 5,
            AssetRarity.RARE: 10,
            AssetRarity.EPIC: 20,
            AssetRarity.LEGENDARY: 30,
            AssetRarity.MYTHIC: 40,
            AssetRarity.DIVINE: 50
        }
        
        requirements.append(AssetRequirement(
            type="level",
            value=level_req[rarity],
            description=f"Requires level {level_req[rarity]} to use"
        ))
        
        return requirements
    
    def _determine_likely_sources(self, rarity: AssetRarity, elemental_affinity: Optional[ElementalAffinity]) -> List[AssetSource]:
        """Determine likely sources for artifact"""
        sources = [AssetSource.QUESTLINE_REWARD, AssetSource.DISCOVERY]
        
        if rarity in [AssetRarity.LEGENDARY, AssetRarity.MYTHIC, AssetRarity.DIVINE]:
            sources.append(AssetSource.GOVERNOR_GIFT)
        
        return sources
    
    def _generate_artifact_tags(self, artifact: GameAsset) -> List[str]:
        """Generate tags for artifact"""
        tags = [
            artifact.type.value,
            artifact.rarity.value
        ]
        
        if artifact.elemental_affinity:
            tags.append(artifact.elemental_affinity.value)
        
        if artifact.created_by_governor:
            tags.append(f"governor_{artifact.created_by_governor.lower()}")
        
        return tags 