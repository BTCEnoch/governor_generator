#!/usr/bin/env python3
"""
Complete Sefirot Database - The Ten Emanations of the Kabbalistic Tree of Life
Each Sefirah represents a different aspect of divine energy and human consciousness
"""

from unified_profiler.schemas.mystical_schemas import Sefirah, SefirotPosition

# The Ten Sefirot - Complete Database
ALL_SEFIROT = [
    Sefirah(
        position=SefirotPosition.KETER,
        name="Keter",
        hebrew_name="כֶּתֶר",
        number=1,
        wikipedia_url="https://en.wikipedia.org/wiki/Sefirot#Keter",
        divine_attribute="Crown of Creation",
        human_attribute="Pure Will",
        spiritual_meaning="The highest divine emanation, representing pure being and infinite potential",
        practical_meaning="Transcendent consciousness, unity with the divine, spiritual crown",
        shadow_aspect="Disconnection from higher purpose, spiritual emptiness",
        element="Pure Light",
        planet="Neptune",
        influence_categories={
            "spirituality": 0.95,
            "transcendence": 0.9,
            "unity": 0.85,
            "wisdom": 0.8,
            "leadership": 0.7
        }
    ),
    
    Sefirah(
        position=SefirotPosition.CHOKHMAH,
        name="Chokhmah",
        hebrew_name="חָכְמָה",
        number=2,
        wikipedia_url="https://en.wikipedia.org/wiki/Sefirot#Chokhmah",
        divine_attribute="Divine Wisdom",
        human_attribute="Intuitive Insight",
        spiritual_meaning="Pure wisdom and the flash of divine inspiration",
        practical_meaning="Intuitive knowledge, creative inspiration, spontaneous understanding",
        shadow_aspect="Impulsiveness without consideration, scattered thinking",
        element="Fire",
        planet="Uranus",
        influence_categories={
            "wisdom": 0.95,
            "intuition": 0.9,
            "creativity": 0.85,
            "innovation": 0.8,
            "inspiration": 0.85
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
            "foundation": 0.95,
            "intuition": 0.9,
            "subconscious": 0.85,
            "connection": 0.8,
            "dreams": 0.75
        }
    ),
    
    Sefirah(
        position=SefirotPosition.MALKHUT,
        name="Malkhut",
        hebrew_name="מַלְכוּת",
        number=10,
        wikipedia_url="https://en.wikipedia.org/wiki/Sefirot#Malkhut",
        divine_attribute="Divine Kingdom",
        human_attribute="Material Manifestation",
        spiritual_meaning="The divine kingdom manifested in the physical world",
        practical_meaning="Material world, practical action, earthly sovereignty",
        shadow_aspect="Materialism, disconnection from spirit, earthly obsession",
        element="Earth",
        planet="Earth",
        influence_categories={
            "manifestation": 0.95,
            "sovereignty": 0.9,
            "practicality": 0.85,
            "grounding": 0.9,
            "material_success": 0.8
        }
    )
]

# Helper functions for working with Sefirot
def get_sefirah_by_position(position: SefirotPosition) -> Sefirah:
    """Get a specific Sefirah by its position"""
    for sefirah in ALL_SEFIROT:
        if sefirah.position == position:
            return sefirah
    raise ValueError(f"Sefirah not found for position: {position}")

def get_sefirah_by_number(number: int) -> Sefirah:
    """Get a specific Sefirah by its number (1-10)"""
    for sefirah in ALL_SEFIROT:
        if sefirah.number == number:
            return sefirah
    raise ValueError(f"Sefirah not found for number: {number}")

def get_sefirot_by_element(element: str) -> list[Sefirah]:
    """Get all Sefirot associated with a specific element"""
    return [s for s in ALL_SEFIROT if s.element and s.element.lower() == element.lower()]

def get_sefirot_by_planet(planet: str) -> list[Sefirah]:
    """Get all Sefirot associated with a specific planet"""
    return [s for s in ALL_SEFIROT if s.planet and s.planet.lower() == planet.lower()] 