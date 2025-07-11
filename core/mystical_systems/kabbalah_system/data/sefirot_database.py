#!/usr/bin/env python3
"""
Sefirot Database - Tree of Life Data
"""

from typing import Dict, List, Optional
from functools import lru_cache
from ..schemas import Sefirah, SefirotPosition

# Complete Sefirot database with all correspondences
ALL_SEFIROT = [
    Sefirah(
        position=SefirotPosition.KETER,
        name="Crown",
        hebrew_name="כתר",
        number=1,
        wikipedia_url="https://en.wikipedia.org/wiki/Keter",
        divine_attribute="Supreme Will",
        human_attribute="Higher Self",
        spiritual_meaning="Unity with Divine",
        practical_meaning="Enlightenment",
        shadow_aspect="Ego Dissolution",
        element="Pure Light",
        planet="Primum Mobile",
        influence_categories={
            "enlightenment": 0.95,
            "unity": 0.9,
            "transcendence": 0.85,
            "divine_will": 0.8
        },
        keywords=[
            "unity",
            "transcendence",
            "divine will",
            "enlightenment",
            "crown",
            "supreme"
        ],
        correspondences={
            "colors": ["pure white", "pure light"],
            "archangel": ["Metatron"],
            "order": ["Chayot Ha Kodesh"],
            "symbols": ["point", "crown", "swastika"],
            "tarot": ["Aces"]
        }
    ),
    
    Sefirah(
        position=SefirotPosition.CHOKHMAH,
        name="Wisdom",
        hebrew_name="חכמה",
        number=2,
        wikipedia_url="https://en.wikipedia.org/wiki/Chokhmah_(Kabbalah)",
        divine_attribute="Divine Wisdom",
        human_attribute="Insight",
        spiritual_meaning="Divine Inspiration",
        practical_meaning="Creative Insight",
        shadow_aspect="Intellectual Pride",
        element="Fire",
        planet="Zodiac",
        influence_categories={
            "wisdom": 0.95,
            "insight": 0.9,
            "creativity": 0.85,
            "inspiration": 0.8
        },
        keywords=[
            "wisdom",
            "insight",
            "father",
            "beginning",
            "inspiration",
            "creativity"
        ],
        correspondences={
            "colors": ["grey", "pure white"],
            "archangel": ["Ratziel"],
            "order": ["Ophanim"],
            "symbols": ["phallus", "straight line", "yod"],
            "tarot": ["Twos"]
        }
    ),
    
    Sefirah(
        position=SefirotPosition.BINAH,
        name="Binah",
        hebrew_name="בִּינָה",
        number=3,
        wikipedia_url="https://en.wikipedia.org/wiki/Sefirot#Binah",
        divine_attribute="Divine Understanding",
        human_attribute="Contemplative Reason",
        spiritual_meaning="Understanding that gives form to wisdom, the divine mother",
        practical_meaning="Deep contemplation, structured thinking, nurturing wisdom",
        shadow_aspect="Over-analysis, restrictive thinking, excessive control",
        element="Water",
        planet="Saturn",
        influence_categories={
            "understanding": 0.95,
            "contemplation": 0.9,
            "structure": 0.85,
            "nurturing": 0.8,
            "discipline": 0.75
        }
    ),
    
    Sefirah(
        position=SefirotPosition.CHESED,
        name="Chesed",
        hebrew_name="חֶסֶד",
        number=4,
        wikipedia_url="https://en.wikipedia.org/wiki/Sefirot#Chesed",
        divine_attribute="Divine Mercy",
        human_attribute="Loving Kindness",
        spiritual_meaning="Unlimited love and mercy, divine grace",
        practical_meaning="Compassion, generosity, unconditional love, expansion",
        shadow_aspect="Excessive permissiveness, lack of boundaries, naive generosity",
        element="Water",
        planet="Jupiter",
        influence_categories={
            "compassion": 0.95,
            "generosity": 0.9,
            "love": 0.95,
            "expansion": 0.85,
            "mercy": 0.9
        }
    ),
    
    Sefirah(
        position=SefirotPosition.GEVURAH,
        name="Gevurah",
        hebrew_name="גְּבוּרָה",
        number=5,
        wikipedia_url="https://en.wikipedia.org/wiki/Sefirot#Gevurah",
        divine_attribute="Divine Strength",
        human_attribute="Disciplined Power",
        spiritual_meaning="Divine strength and judgment, necessary restriction",
        practical_meaning="Discipline, boundaries, justice, focused power",
        shadow_aspect="Excessive harshness, destructive anger, ruthless judgment",
        element="Fire",
        planet="Mars",
        influence_categories={
            "strength": 0.95,
            "discipline": 0.9,
            "justice": 0.85,
            "boundaries": 0.8,
            "determination": 0.9
        }
    ),
    
    Sefirah(
        position=SefirotPosition.TIFERET,
        name="Tiferet",
        hebrew_name="תִּפְאֶרֶת",
        number=6,
        wikipedia_url="https://en.wikipedia.org/wiki/Sefirot#Tiferet",
        divine_attribute="Divine Beauty",
        human_attribute="Harmonious Balance",
        spiritual_meaning="Perfect harmony between mercy and severity, divine beauty",
        practical_meaning="Balance, harmony, beauty, integration of opposites",
        shadow_aspect="Superficial beauty, vanity, indecision between extremes",
        element="Air",
        planet="Sun",
        influence_categories={
            "harmony": 0.95,
            "beauty": 0.9,
            "balance": 0.95,
            "integration": 0.85,
            "centeredness": 0.8
        }
    ),
    
    Sefirah(
        position=SefirotPosition.NETZACH,
        name="Netzach",
        hebrew_name="נֶצַח",
        number=7,
        wikipedia_url="https://en.wikipedia.org/wiki/Sefirot#Netzach",
        divine_attribute="Divine Victory",
        human_attribute="Enduring Passion",
        spiritual_meaning="Eternity and endurance, divine victory over limitation",
        practical_meaning="Persistence, passion, artistic expression, emotional drive",
        shadow_aspect="Excessive emotionalism, lack of restraint, overwhelming passion",
        element="Fire",
        planet="Venus",
        influence_categories={
            "persistence": 0.9,
            "passion": 0.95,
            "creativity": 0.85,
            "emotion": 0.9,
            "victory": 0.8
        }
    ),
    
    Sefirah(
        position=SefirotPosition.HOD,
        name="Hod",
        hebrew_name="הוֹד",
        number=8,
        wikipedia_url="https://en.wikipedia.org/wiki/Sefirot#Hod",
        divine_attribute="Divine Glory",
        human_attribute="Intellectual Glory",
        spiritual_meaning="Divine splendor expressed through form and intellect",
        practical_meaning="Intellectual power, communication, analytical thinking, glory",
        shadow_aspect="Over-intellectualization, disconnection from emotion, arrogance",
        element="Air",
        planet="Mercury",
        influence_categories={
            "intellect": 0.95,
            "communication": 0.9,
            "analysis": 0.85,
            "glory": 0.8,
            "precision": 0.85
        }
    ),
    
    Sefirah(
        position=SefirotPosition.YESOD,
        name="Yesod",
        hebrew_name="יְסוֹד",
        number=9,
        wikipedia_url="https://en.wikipedia.org/wiki/Sefirot#Yesod",
        divine_attribute="Divine Foundation",
        human_attribute="Subconscious Foundation",
        spiritual_meaning="The foundation that connects the spiritual with the material",
        practical_meaning="Subconscious mind, dreams, intuition, connection to astral",
        shadow_aspect="Illusion, deception, unstable foundation, fantasy",
        element="Air",
        planet="Moon",
        influence_categories={
            "intuition": 0.95,
            "dreams": 0.9,
            "foundation": 0.85,
            "connection": 0.8,
            "subconscious": 0.85
        }
    ),
    
    Sefirah(
        position=SefirotPosition.MALKUTH,
        name="Malkuth",
        hebrew_name="מַלְכוּת",
        number=10,
        wikipedia_url="https://en.wikipedia.org/wiki/Sefirot#Malkuth",
        divine_attribute="Divine Kingdom",
        human_attribute="Physical Manifestation",
        spiritual_meaning="The physical world as a manifestation of divine energy",
        practical_meaning="Grounding, manifestation, physical reality, completion",
        shadow_aspect="Materialism, stagnation, disconnection from spirit",
        element="Earth",
        planet="Earth",
        influence_categories={
            "manifestation": 0.95,
            "grounding": 0.9,
            "completion": 0.85,
            "stability": 0.8,
            "physicality": 0.85
        }
    )
]

# Create lookup dictionaries for faster access
SEFIRAH_BY_POSITION: Dict[SefirotPosition, Sefirah] = {
    sefirah.position: sefirah for sefirah in ALL_SEFIROT
}
SEFIRAH_BY_NUMBER: Dict[int, Sefirah] = {
    sefirah.number: sefirah for sefirah in ALL_SEFIROT
}
SEFIROT_BY_ELEMENT: Dict[str, List[Sefirah]] = {}
for sefirah in ALL_SEFIROT:
    SEFIROT_BY_ELEMENT.setdefault(sefirah.element.lower(), []).append(sefirah)

SEFIROT_BY_PLANET: Dict[str, List[Sefirah]] = {}
for sefirah in ALL_SEFIROT:
    SEFIROT_BY_PLANET.setdefault(sefirah.planet.lower(), []).append(sefirah)

@lru_cache(maxsize=32)
def get_sefirah_by_position(position: SefirotPosition) -> Optional[Sefirah]:
    """Get Sefirah by position on the Tree of Life"""
    return SEFIRAH_BY_POSITION.get(position)

@lru_cache(maxsize=32)
def get_sefirah_by_number(number: int) -> Optional[Sefirah]:
    """Get Sefirah by numerical value"""
    return SEFIRAH_BY_NUMBER.get(number)

@lru_cache(maxsize=32)
def get_sefirot_by_element(element: str) -> List[Sefirah]:
    """Get all Sefirot associated with a given element (case-insensitive)"""
    return SEFIROT_BY_ELEMENT.get(element.lower(), [])

@lru_cache(maxsize=32)
def get_sefirot_by_planet(planet: str) -> List[Sefirah]:
    """Get all Sefirot associated with a given planet (case-insensitive)"""
    return SEFIROT_BY_PLANET.get(planet.lower(), []) 