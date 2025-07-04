#!/usr/bin/env python3
"""
Unified Mystical Profiler
Assigns Tarot, Sefirot, Numerology, and Zodiac influences to governors
"""

import random
import hashlib
from typing import Dict, List
from datetime import datetime

# Import all systems
from engines.mystical_systems.tarot_system.engines.governor_tarot_assigner import GovernorTarotAssigner
from engines.mystical_systems.kabbalah_system.data.sefirot_database import ALL_SEFIROT, get_sefirah_by_number
from engines.mystical_systems.numerology_system.data.numerology_database import get_numerology_profile, calculate_name_numerology
from engines.mystical_systems.zodiac_system.data.zodiac_database import ALL_ZODIAC_SIGNS, get_zodiac_sign_by_name
from core.governors.profiler.schemas.mystical_schemas import CompleteMysticalProfile, ZodiacElement

class UnifiedMysticalProfiler:
    def __init__(self):
        self.tarot_assigner = GovernorTarotAssigner()
    
    def create_complete_profile(self, governor_data: Dict) -> CompleteMysticalProfile:
        """Create complete mystical profile for a governor"""
        
        governor_name = governor_data.get('name', 'Unknown Governor')
        
        # 1. Assign Tarot Profile (existing system)
        tarot_profile = self.tarot_assigner.assign_tarot_to_governor(governor_data)
        
        # 2. Assign Sefirot Influences
        sefirot_influences = self._assign_sefirot_influences(governor_data)
        
        # 3. Assign Numerology Profile
        numerology_profile = self._assign_numerology_profile(governor_data)
        
        # 4. Assign Zodiac Sign
        zodiac_sign = self._assign_zodiac_sign(governor_data)
        
        # 5. Calculate Unified Influences
        combined_modifiers = self._combine_personality_modifiers(
            tarot_profile, sefirot_influences, numerology_profile, zodiac_sign
        )
        
        unified_themes = self._extract_unified_themes(
            tarot_profile, sefirot_influences, numerology_profile, zodiac_sign
        )
        
        mystical_synthesis = self._generate_mystical_synthesis(
            tarot_profile, sefirot_influences, numerology_profile, zodiac_sign
        )
        
        elemental_balance = self._calculate_elemental_balance(
            tarot_profile, sefirot_influences, zodiac_sign
        )
        
        planetary_influences = self._extract_planetary_influences(
            tarot_profile, sefirot_influences, zodiac_sign
        )
        
        archetypal_themes = self._extract_archetypal_themes(
            tarot_profile, sefirot_influences, numerology_profile, zodiac_sign
        )
        
        # Create complete profile
        complete_profile = CompleteMysticalProfile(
            governor_name=governor_name,
            tarot_profile=tarot_profile,
            sefirot_influences=sefirot_influences,
            numerology_profile=numerology_profile,
            zodiac_sign=zodiac_sign,
            combined_personality_modifiers=combined_modifiers,
            unified_storyline_themes=unified_themes,
            mystical_synthesis=mystical_synthesis,
            elemental_balance=elemental_balance,
            planetary_influences=planetary_influences,
            archetypal_themes=archetypal_themes
        )
        
        return complete_profile
    
    def _assign_sefirot_influences(self, governor_data: Dict) -> List:
        """Assign primary and secondary Sefirot based on governor traits"""
        
        # Use governor name for consistent assignment
        name = governor_data.get('name', 'default')
        name_hash = int(hashlib.md5(name.encode()).hexdigest()[:8], 16)
        
        # Primary Sefirah (based on wisdom tradition and name)
        tradition = governor_data.get('wisdom_tradition', 'hermetic_tradition')
        
        tradition_sefirot_map = {
            'kabbalah': [1, 2, 3],  # Keter, Chokhmah, Binah
            'hermetic_tradition': [6, 4, 8],  # Tiferet, Chesed, Hod
            'thelema': [1, 6, 9],  # Keter, Tiferet, Yesod
            'golden_dawn': [6, 8, 9],  # Tiferet, Hod, Yesod
            'enochian_magic': [2, 8, 10]  # Chokhmah, Hod, Malkhut
        }
        
        preferred_numbers = tradition_sefirot_map.get(tradition, [1, 6, 10])
        primary_num = preferred_numbers[name_hash % len(preferred_numbers)]
        primary_sefirah = get_sefirah_by_number(primary_num)
        
        # Secondary Sefirah (complementary)
        secondary_candidates = [s for s in ALL_SEFIROT if s.number != primary_num]
        secondary_sefirah = secondary_candidates[name_hash % len(secondary_candidates)]
        
        return [primary_sefirah, secondary_sefirah]
    
    def _assign_numerology_profile(self, governor_data: Dict):
        """Assign numerology profile based on governor name"""
        name = governor_data.get('name', 'default')
        life_path_number = calculate_name_numerology(name)
        return get_numerology_profile(life_path_number)
    
    def _assign_zodiac_sign(self, governor_data: Dict):
        """Assign zodiac sign based on governor characteristics"""
        
        # Use governor name for consistent assignment
        name = governor_data.get('name', 'default')
        name_hash = int(hashlib.md5(name.encode()).hexdigest()[:8], 16)
        
        # Get zodiac sign based on hash
        zodiac_index = name_hash % len(ALL_ZODIAC_SIGNS)
        return ALL_ZODIAC_SIGNS[zodiac_index]
    
    def _combine_personality_modifiers(self, tarot_profile, sefirot_influences, numerology_profile, zodiac_sign) -> Dict[str, float]:
        """Combine personality modifiers from all systems"""
        combined = {}
        
        # Add tarot modifiers
        for trait, value in tarot_profile.personality_modifiers.items():
            combined[trait] = value
        
        # Add sefirot modifiers
        for sefirah in sefirot_influences:
            if sefirah.influence_categories:
                for trait, value in sefirah.influence_categories.items():
                    combined[trait] = max(combined.get(trait, 0), value * 0.8)
        
        # Add numerology modifiers
        if numerology_profile.influence_categories:
            for trait, value in numerology_profile.influence_categories.items():
                combined[trait] = max(combined.get(trait, 0), value * 0.7)
        
        # Add zodiac modifiers
        if zodiac_sign.influence_categories:
            for trait, value in zodiac_sign.influence_categories.items():
                combined[trait] = max(combined.get(trait, 0), value * 0.6)
        
        return combined
    
    def _extract_unified_themes(self, tarot_profile, sefirot_influences, numerology_profile, zodiac_sign) -> List[str]:
        """Extract unified themes from all systems"""
        themes = []
        
        # Tarot themes
        themes.extend(tarot_profile.storyline_themes[:3])
        
        # Sefirot themes
        for sefirah in sefirot_influences:
            themes.append(f"{sefirah.name} energy")
        
        # Numerology themes
        themes.append(f"Life Path {numerology_profile.life_path_number}")
        themes.extend(numerology_profile.positive_traits[:2])
        
        # Zodiac themes
        themes.append(f"{zodiac_sign.name} influence")
        themes.extend(zodiac_sign.keywords[:2])
        
        return list(set(themes))  # Remove duplicates
    
    def _generate_mystical_synthesis(self, tarot_profile, sefirot_influences, numerology_profile, zodiac_sign) -> str:
        """Generate synthesis of how all systems work together"""
        
        primary_sefirah = sefirot_influences[0]
        
        synthesis = f"""
        MYSTICAL SYNTHESIS: {tarot_profile.governor_name}
        
        🎴 TAROT: Primary influence of {tarot_profile.primary_card.name} guides their magical approach
        🌳 KABBALAH: {primary_sefirah.name} provides divine attribute of {primary_sefirah.divine_attribute}
        🔢 NUMEROLOGY: Life Path {numerology_profile.life_path_number} - {numerology_profile.life_purpose}
        ⭐ ZODIAC: {zodiac_sign.name} ({zodiac_sign.element.value.title()}) brings {zodiac_sign.positive_traits[0]} energy
        
        UNIFIED PATTERN: A governor who embodies {tarot_profile.primary_card.name} wisdom through 
        {primary_sefirah.name} consciousness, following Life Path {numerology_profile.life_path_number} 
        with {zodiac_sign.name}'s {zodiac_sign.element.value} nature.
        """
        
        return synthesis.strip()
    
    def _calculate_elemental_balance(self, tarot_profile, sefirot_influences, zodiac_sign) -> Dict[str, float]:
        """Calculate elemental balance across all systems"""
        elements = {"fire": 0.0, "water": 0.0, "air": 0.0, "earth": 0.0}
        
        # Tarot elemental influences
        if tarot_profile.primary_card.element:
            element = tarot_profile.primary_card.element.lower()
            if element in elements:
                elements[element] += 0.4
        
        # Sefirot elemental influences
        for sefirah in sefirot_influences:
            if sefirah.element:
                element = sefirah.element.lower()
                if element in elements:
                    elements[element] += 0.3
        
        # Zodiac elemental influence
        zodiac_element = zodiac_sign.element.value.lower()
        if zodiac_element in elements:
            elements[zodiac_element] += 0.5
        
        return elements
    
    def _extract_planetary_influences(self, tarot_profile, sefirot_influences, zodiac_sign) -> List[str]:
        """Extract all planetary influences"""
        planets = []
        
        # Tarot planetary influences
        if tarot_profile.primary_card.planet:
            planets.append(tarot_profile.primary_card.planet)
        
        # Sefirot planetary influences
        for sefirah in sefirot_influences:
            if sefirah.planet:
                planets.append(sefirah.planet)
        
        # Zodiac planetary influence
        planets.append(zodiac_sign.ruling_planet)
        
        return list(set(planets))  # Remove duplicates
    
    def _extract_archetypal_themes(self, tarot_profile, sefirot_influences, numerology_profile, zodiac_sign) -> List[str]:
        """Extract unified archetypal themes"""
        archetypes = []
        
        # Major archetypal themes
        archetypes.append(f"The {tarot_profile.primary_card.name}")
        archetypes.append(f"The {sefirot_influences[0].name} Emanation")
        archetypes.append(f"The Life Path {numerology_profile.life_path_number} Journey")
        archetypes.append(f"The {zodiac_sign.name} Archetype")
        
        return archetypes 
