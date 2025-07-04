#!/usr/bin/env python3
"""
🏛️ THE LIGHTHOUSE PROJECT: SACRED WISDOM RESEARCH AUTOMATION
Comprehensive source link index and research orchestration for all wisdom traditions

This script automates the research process for building The Lighthouse knowledge base,
organizing source collection into optimized API call sequences.
"""

import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
# import aiohttp  # Will add when implementing async functionality

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("LighthouseResearch")

class TraditionPriority(Enum):
    CRITICAL = "critical"      # Must complete immediately
    HIGH = "high"             # Core Western magic foundations  
    MEDIUM = "medium"         # Complementary systems
    SPECIALIZED = "specialized" # Specialized/regional traditions

class ResearchComplexity(Enum):
    LOW = "low"               # Well-documented, clear sources
    MEDIUM = "medium"         # Moderate research needed
    HIGH = "high"            # Complex theology/philosophy
    EXPERT = "expert"        # Requires specialist knowledge

@dataclass
class SourceLink:
    url: str
    title: str
    type: str  # "wikipedia", "academic", "primary_text", "encyclopedia", "archive"
    quality: str  # "excellent", "good", "reference"
    description: str
    subcategory: str  # Which aspect of tradition this covers

@dataclass
class TraditionResearch:
    name: str
    display_name: str
    priority: TraditionPriority
    complexity: ResearchComplexity
    estimated_entries: int
    subcategories: List[str]
    primary_sources: List[SourceLink]
    wikipedia_sources: List[SourceLink]
    academic_sources: List[SourceLink]
    archive_sources: List[SourceLink]
    research_keywords: List[str]
    cross_references: List[str]  # Related traditions

# 🏛️ THE LIGHTHOUSE RESEARCH REGISTRY
LIGHTHOUSE_TRADITIONS = {
    
    # 🔥 PRIORITY 1: CRITICAL FOUNDATIONS
    "golden_dawn": TraditionResearch(
        name="golden_dawn",
        display_name="Hermetic Order of the Golden Dawn",
        priority=TraditionPriority.CRITICAL,
        complexity=ResearchComplexity.MEDIUM,
        estimated_entries=12,
        subcategories=[
            "Middle Pillar Technique", "Elemental Magic System", "Pathworking Practice",
            "Watchtower Magic", "Egyptian Godforms", "Skrying and Vision Work",
            "Invocation and Evocation", "Initiation Grade System", "Neophyte Rituals",
            "Adeptus Minor Teachings", "Rose Cross Ritual", "Hexagram Rituals"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Hermetic_Order_of_the_Golden_Dawn", 
                      "Golden Dawn - Wikipedia", "wikipedia", "excellent",
                      "Comprehensive overview of the order, history, and practices", "overview"),
            SourceLink("https://en.wikipedia.org/wiki/Lesser_banishing_ritual_of_the_pentagram",
                      "Lesser Banishing Ritual of Pentagram - Wikipedia", "wikipedia", "excellent", 
                      "Detailed LBRP instructions and theory", "ritual_practice"),
            SourceLink("https://en.wikipedia.org/wiki/Middle_Pillar_(Kabbalah)",
                      "Middle Pillar - Wikipedia", "wikipedia", "good",
                      "Kabbalistic foundation for Golden Dawn practice", "middle_pillar")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Samuel_Liddell_MacGregor_Mathers",
                      "MacGregor Mathers - Wikipedia", "wikipedia", "good",
                      "Key founding figure and teachings", "historical_figures"),
            SourceLink("https://en.wikipedia.org/wiki/William_Wynn_Westcott", 
                      "William Westcott - Wikipedia", "wikipedia", "good",
                      "Co-founder and Rosicrucian connections", "historical_figures"),
            SourceLink("https://en.wikipedia.org/wiki/Aleister_Crowley",
                      "Aleister Crowley - Wikipedia", "wikipedia", "excellent",
                      "Golden Dawn member who founded Thelema", "historical_figures")
        ],
        academic_sources=[],  # To be populated
        archive_sources=[],   # To be populated  
        research_keywords=[
            "golden dawn magic", "LBRP ritual", "middle pillar", "tree of life pathworking",
            "elemental magic", "egyptian godforms", "hermetic kabbalah", "enochian watchtowers"
        ],
        cross_references=["kabbalah", "hermetic", "enochian", "thelema", "egyptian_magic"]
    ),

    "thelema": TraditionResearch(
        name="thelema", 
        display_name="Thelema",
        priority=TraditionPriority.CRITICAL,
        complexity=ResearchComplexity.HIGH,
        estimated_entries=12,
        subcategories=[
            "True Will Philosophy", "Love Under Will Ethics", "Knowledge and Conversation HGA",
            "Aeon of Horus", "Liber Resh Solar Adorations", "Star Ruby Ritual", 
            "Star Sapphire Ritual", "Gnostic Mass", "Book of the Law", "A∴A∴ Grade System",
            "Book of Thoth Tarot", "Vision and the Voice", "Thelemic Calendar"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Thelema",
                      "Thelema - Wikipedia", "wikipedia", "excellent", 
                      "Comprehensive overview of Thelemic philosophy and practice", "overview"),
            SourceLink("https://en.wikipedia.org/wiki/The_Book_of_the_Law",
                      "The Book of the Law - Wikipedia", "wikipedia", "excellent",
                      "Central Thelemic text received by Crowley", "core_text"),
            SourceLink("https://en.wikipedia.org/wiki/True_Will", 
                      "True Will - Wikipedia", "wikipedia", "excellent",
                      "Core Thelemic concept of authentic purpose", "philosophy")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/A%E2%88%B4A%E2%88%B4",
                      "A∴A∴ - Wikipedia", "wikipedia", "good",
                      "Thelemic magical order and grade system", "organizations"),
            SourceLink("https://en.wikipedia.org/wiki/Ordo_Templi_Orientis",
                      "Ordo Templi Orientis - Wikipedia", "wikipedia", "good", 
                      "International Thelemic fraternal organization", "organizations"),
            SourceLink("https://en.wikipedia.org/wiki/Holy_Guardian_Angel",
                      "Holy Guardian Angel - Wikipedia", "wikipedia", "excellent",
                      "Central concept in Thelemic attainment", "concepts")
        ],
        academic_sources=[],
        archive_sources=[],
        research_keywords=[
            "thelema philosophy", "true will", "do what thou wilt", "book of law",
            "aleister crowley", "holy guardian angel", "aeon horus", "thelemic ritual"
        ],
        cross_references=["golden_dawn", "kabbalah", "enochian", "egyptian_magic", "gnostic_traditions"]
    ),

    "egyptian_magic": TraditionResearch(
        name="egyptian_magic",
        display_name="Ancient Egyptian Magic",
        priority=TraditionPriority.HIGH,
        complexity=ResearchComplexity.MEDIUM,
        estimated_entries=13,
        subcategories=[
            "Ma'at Cosmic Order", "Neteru Divine Principles", "Heka Magical Force",
            "Ka Ba Akh Soul Complex", "Divine Pharaoh Concept", "Solar Worship Ra",
            "Mummification Rites", "Canopic Magic Four Sons Horus", "Amulet Creation",
            "Opening of the Mouth", "Book of the Dead", "Egyptian Pantheon", 
            "Hieroglyphic Magic", "Temple Architecture Sacred Geometry"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Ancient_Egyptian_religion",
                      "Ancient Egyptian Religion - Wikipedia", "wikipedia", "excellent",
                      "Comprehensive overview of Egyptian religious practices", "overview"),
            SourceLink("https://en.wikipedia.org/wiki/Egyptian_mythology", 
                      "Egyptian Mythology - Wikipedia", "wikipedia", "excellent",
                      "Complete pantheon and mythological system", "mythology"), 
            SourceLink("https://en.wikipedia.org/wiki/Ancient_Egyptian_concept_of_the_soul",
                      "Egyptian Soul Concept - Wikipedia", "wikipedia", "excellent",
                      "Ka, Ba, Akh and other soul components", "soul_concepts")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Heka_(god)",
                      "Heka (Magic) - Wikipedia", "wikipedia", "excellent", 
                      "Egyptian magical force and deity", "magic_concepts"),
            SourceLink("https://en.wikipedia.org/wiki/Maat",
                      "Ma'at - Wikipedia", "wikipedia", "excellent",
                      "Goddess and concept of cosmic order", "cosmic_principles"),
            SourceLink("https://en.wikipedia.org/wiki/Book_of_the_Dead",
                      "Book of the Dead - Wikipedia", "wikipedia", "excellent",
                      "Egyptian funerary texts and afterlife navigation", "sacred_texts")
        ],
        academic_sources=[],
        archive_sources=[],
        research_keywords=[
            "ancient egyptian magic", "maat cosmic order", "heka magical force", 
            "egyptian gods neteru", "book of the dead", "hieroglyphic magic", "pharaoh divine"
        ],
        cross_references=["golden_dawn", "thelema", "sacred_geometry", "hermetic"]
    ),

    # 📈 PRIORITY 2: COMPLEMENTARY SYSTEMS
    "gnostic_traditions": TraditionResearch(
        name="gnostic_traditions",
        display_name="Gnostic Traditions",
        priority=TraditionPriority.HIGH,
        complexity=ResearchComplexity.HIGH,
        estimated_entries=11,
        subcategories=[
            "Divine Spark Pneuma", "Demiurge False Creator", "Gnosis Direct Knowledge",
            "Pleroma Divine Fullness", "Sophia Myth Wisdom Fall", "Aeons Divine Emanations",
            "Archons Material Rulers", "Pistis Sophia Advanced Cosmology", 
            "Nag Hammadi Library", "Valentinian School", "Sethian Gnosticism"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Gnosticism",
                      "Gnosticism - Wikipedia", "wikipedia", "excellent",
                      "Comprehensive overview of Gnostic movements and beliefs", "overview"),
            SourceLink("https://en.wikipedia.org/wiki/Nag_Hammadi_library",
                      "Nag Hammadi Library - Wikipedia", "wikipedia", "excellent",
                      "Primary source collection of Gnostic texts", "primary_texts"),
            SourceLink("https://en.wikipedia.org/wiki/Sophia_(Gnosticism)",
                      "Sophia (Gnosticism) - Wikipedia", "wikipedia", "excellent",
                      "Divine wisdom figure in Gnostic mythology", "cosmology")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Demiurge",
                      "Demiurge - Wikipedia", "wikipedia", "excellent",
                      "Creator deity in Gnostic and Platonic thought", "cosmology"),
            SourceLink("https://en.wikipedia.org/wiki/Pleroma",
                      "Pleroma - Wikipedia", "wikipedia", "good",
                      "Divine fullness in Gnostic cosmology", "cosmology"),
            SourceLink("https://en.wikipedia.org/wiki/Archon_(Gnosticism)",
                      "Archon (Gnosticism) - Wikipedia", "wikipedia", "good",
                      "Rulers of the material world in Gnosticism", "cosmology"),
            SourceLink("https://en.wikipedia.org/wiki/Valentinianism",
                      "Valentinianism - Wikipedia", "wikipedia", "good",
                      "Major school of Gnostic thought", "schools_of_thought")
        ],
        academic_sources=[],
        archive_sources=[],
        research_keywords=[
            "gnosticism", "divine spark", "demiurge", "pleroma", "sophia myth",
            "nag hammadi", "valentinian gnostic", "archons", "pistis sophia"
        ],
        cross_references=["classical_philosophy", "hermetic", "kabbalah", "christian_mysticism"]
    ),

    "tarot_knowledge": TraditionResearch(
        name="tarot_knowledge", 
        display_name="Tarot Divination System",
        priority=TraditionPriority.MEDIUM,
        complexity=ResearchComplexity.MEDIUM,
        estimated_entries=12,
        subcategories=[
            "Major Arcana 22 Cards", "Minor Arcana 56 Cards", "Fool's Journey Path",
            "Court Card Psychology", "Elemental Correspondences", "Celtic Cross Spread",
            "Daily Card Draw Practice", "Pathworking Meditation", "Astrological Associations",
            "Kabbalistic Tree Mapping", "Numerological Meanings", "Symbolic Interpretation"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Tarot",
                      "Tarot - Wikipedia", "wikipedia", "excellent",
                      "Complete overview of tarot cards and systems", "overview"),
            SourceLink("https://en.wikipedia.org/wiki/Major_Arcana",
                      "Major Arcana - Wikipedia", "wikipedia", "excellent", 
                      "22 trump cards representing major life themes", "major_arcana"),
            SourceLink("https://en.wikipedia.org/wiki/Minor_Arcana",
                      "Minor Arcana - Wikipedia", "wikipedia", "excellent",
                      "56 suit cards for daily situations", "minor_arcana")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Rider%E2%80%93Waite_Tarot",
                      "Rider-Waite Tarot - Wikipedia", "wikipedia", "excellent",
                      "Most influential modern tarot deck", "tarot_decks"),
            SourceLink("https://en.wikipedia.org/wiki/Thoth_tarot_deck", 
                      "Thoth Tarot Deck - Wikipedia", "wikipedia", "good",
                      "Aleister Crowley's esoteric tarot system", "tarot_decks"),
            SourceLink("https://en.wikipedia.org/wiki/Tarot_card_reading",
                      "Tarot Card Reading - Wikipedia", "wikipedia", "good",
                      "Methods and practices of tarot divination", "divination_practice"),
            SourceLink("https://en.wikipedia.org/wiki/The_Fool_(Tarot_card)",
                      "The Fool (Tarot) - Wikipedia", "wikipedia", "good",
                      "Beginning of the Fool's Journey", "individual_cards")
        ],
        academic_sources=[],
        archive_sources=[],
        research_keywords=[
            "tarot cards", "major arcana", "minor arcana", "tarot reading",
            "rider waite tarot", "celtic cross spread", "fool's journey", "tarot symbolism"
        ],
        cross_references=["golden_dawn", "thelema", "kabbalah", "astrology", "numerology"]
    ),

    "sacred_geometry": TraditionResearch(
        name="sacred_geometry",
        display_name="Sacred Geometry",
        priority=TraditionPriority.MEDIUM,
        complexity=ResearchComplexity.MEDIUM,
        estimated_entries=11,
        subcategories=[
            "Golden Ratio Phi", "Flower of Life Pattern", "Platonic Solids Five Elements",
            "Vesica Piscis Sacred Intersection", "Fibonacci Sequence Nature Spirals",
            "Sacred Architecture Proportions", "Mandala Construction Circles",
            "Crystal Geometry Structures", "Merkaba Sacred Form", "Seed of Life Genesis"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Sacred_geometry",
                      "Sacred Geometry - Wikipedia", "wikipedia", "excellent",
                      "Mathematical principles in spiritual and religious contexts", "overview"),
            SourceLink("https://en.wikipedia.org/wiki/Golden_ratio",
                      "Golden Ratio - Wikipedia", "wikipedia", "excellent",
                      "Divine proportion found throughout nature", "mathematical_principles"),
            SourceLink("https://en.wikipedia.org/wiki/Platonic_solid",
                      "Platonic Solids - Wikipedia", "wikipedia", "excellent",
                      "Five perfect 3D geometric forms", "geometric_forms")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Flower_of_Life",
                      "Flower of Life - Wikipedia", "wikipedia", "excellent",
                      "Overlapping circles pattern with mystical significance", "sacred_patterns"),
            SourceLink("https://en.wikipedia.org/wiki/Vesica_piscis", 
                      "Vesica Piscis - Wikipedia", "wikipedia", "good",
                      "Sacred intersection of two circles", "sacred_patterns"),
            SourceLink("https://en.wikipedia.org/wiki/Fibonacci_number",
                      "Fibonacci Numbers - Wikipedia", "wikipedia", "excellent",
                      "Mathematical sequence appearing in nature", "mathematical_principles"),
            SourceLink("https://en.wikipedia.org/wiki/Mandala",
                      "Mandala - Wikipedia", "wikipedia", "excellent", 
                      "Circular sacred art and meditation focus", "sacred_art")
        ],
        academic_sources=[],
        archive_sources=[],
        research_keywords=[
            "sacred geometry", "golden ratio", "flower of life", "platonic solids",
            "vesica piscis", "fibonacci sequence", "mandala sacred", "geometric symbolism"
        ],
        cross_references=["classical_philosophy", "egyptian_magic", "hinduism", "buddhism"]
    ),

    "classical_philosophy": TraditionResearch(
        name="classical_philosophy",
        display_name="Classical Greek Philosophy", 
        priority=TraditionPriority.MEDIUM,
        complexity=ResearchComplexity.HIGH,
        estimated_entries=11,
        subcategories=[
            "Platonic Forms Theory", "Aristotelian Logic Golden Mean", "Pythagorean Mathematics Harmony",
            "Stoic Virtue Ethics", "Logos Divine Reason", "Socratic Method Questioning",
            "Platonic Dialectic Truth", "Aristotelian Categories", "Stoic Daily Practice",
            "Nous Divine Mind", "Theory of Knowledge Epistemology"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Ancient_Greek_philosophy",
                      "Ancient Greek Philosophy - Wikipedia", "wikipedia", "excellent",
                      "Comprehensive overview of Greek philosophical traditions", "overview"),
            SourceLink("https://en.wikipedia.org/wiki/Plato",
                      "Plato - Wikipedia", "wikipedia", "excellent",
                      "Founder of the Academy and theory of Forms", "philosophers"),
            SourceLink("https://en.wikipedia.org/wiki/Aristotle", 
                      "Aristotle - Wikipedia", "wikipedia", "excellent",
                      "Student of Plato, systematic philosopher", "philosophers")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Theory_of_forms",
                      "Theory of Forms - Wikipedia", "wikipedia", "excellent",
                      "Plato's theory of eternal perfect templates", "platonic_concepts"),
            SourceLink("https://en.wikipedia.org/wiki/Stoicism",
                      "Stoicism - Wikipedia", "wikipedia", "excellent", 
                      "School of Hellenistic philosophy emphasizing virtue", "philosophical_schools"),
            SourceLink("https://en.wikipedia.org/wiki/Pythagoreanism",
                      "Pythagoreanism - Wikipedia", "wikipedia", "good",
                      "Mathematical mysticism and number philosophy", "philosophical_schools"),
            SourceLink("https://en.wikipedia.org/wiki/Socratic_method",
                      "Socratic Method - Wikipedia", "wikipedia", "excellent",
                      "Questioning technique to discover truth", "methods"),
            SourceLink("https://en.wikipedia.org/wiki/Logos",
                      "Logos - Wikipedia", "wikipedia", "excellent",
                      "Divine reason governing the cosmos", "concepts")
        ],
        academic_sources=[],
        archive_sources=[],
        research_keywords=[
            "plato philosophy", "aristotle logic", "stoicism virtue", "pythagorean mathematics",
            "socratic method", "theory of forms", "logos divine reason", "classical philosophy"
        ],
        cross_references=["sacred_geometry", "gnostic_traditions", "hermetic", "neoplatonism"]
    ),

    "taoism": TraditionResearch(
        name="taoism",
        display_name="Taoism (Daoism)",
        priority=TraditionPriority.MEDIUM,
        complexity=ResearchComplexity.MEDIUM,
        estimated_entries=12,
        subcategories=[
            "Tao The Way Principle", "Wu Wei Effortless Action", "Yin Yang Complementary Opposites",
            "Te Virtue Natural Power", "Ziran Naturalness Spontaneity", "Qigong Energy Cultivation",
            "Tai Chi Moving Meditation", "Meditation Stillness Practice", "Feng Shui Harmony",
            "Internal Alchemy Spiritual", "Five Elements System", "Three Treasures Jing Qi Shen"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Taoism",
                      "Taoism - Wikipedia", "wikipedia", "excellent",
                      "Comprehensive overview of Taoist philosophy and practice", "overview"),
            SourceLink("https://en.wikipedia.org/wiki/Tao",
                      "Tao - Wikipedia", "wikipedia", "excellent", 
                      "The Way - central concept in Taoism", "core_concepts"),
            SourceLink("https://en.wikipedia.org/wiki/Wu_wei",
                      "Wu Wei - Wikipedia", "wikipedia", "excellent",
                      "Effortless action in accordance with natural flow", "core_concepts")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Yin_and_yang",
                      "Yin and Yang - Wikipedia", "wikipedia", "excellent",
                      "Complementary opposites in dynamic balance", "core_concepts"),
            SourceLink("https://en.wikipedia.org/wiki/Qigong", 
                      "Qigong - Wikipedia", "wikipedia", "excellent",
                      "Chinese practice of energy cultivation", "practices"),
            SourceLink("https://en.wikipedia.org/wiki/Tai_chi",
                      "Tai Chi - Wikipedia", "wikipedia", "excellent",
                      "Internal martial art and moving meditation", "practices"),
            SourceLink("https://en.wikipedia.org/wiki/Taoist_meditation",
                      "Taoist Meditation - Wikipedia", "wikipedia", "good",
                      "Contemplative practices in Taoism", "practices"),
            SourceLink("https://en.wikipedia.org/wiki/Wuxing_(Chinese_philosophy)",
                      "Five Elements (Wu Xing) - Wikipedia", "wikipedia", "excellent",
                      "Fundamental Taoist cosmological system", "cosmology")
        ], 
        academic_sources=[],
        archive_sources=[],
        research_keywords=[
            "taoism", "tao the way", "wu wei", "yin yang", "qigong", "tai chi",
            "five elements wuxing", "taoist meditation", "feng shui", "taoism philosophy"
        ],
        cross_references=["i_ching", "sacred_geometry", "meditation", "chinese_philosophy"]
    ),

    "i_ching": TraditionResearch(
        name="i_ching",
        display_name="I-Ching (Book of Changes)",
        priority=TraditionPriority.MEDIUM,
        complexity=ResearchComplexity.HIGH,
        estimated_entries=11,
        subcategories=[
            "64 Hexagrams Complete System", "Eight Trigrams Foundation", "Changing Lines Transformation",
            "Consultation Methods Divination", "Wilhelm Translation Standard", "Book of Changes Philosophy",
            "Superior Person Ideal", "Time and Timing Wisdom", "Cosmic Correspondence Patterns",
            "Hexagram Divination Practice", "Judgment and Image Study"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/I_Ching",
                      "I Ching - Wikipedia", "wikipedia", "excellent",
                      "Ancient Chinese divination text and philosophy", "overview"),
            SourceLink("https://en.wikipedia.org/wiki/Hexagram_(I_Ching)",
                      "I Ching Hexagrams - Wikipedia", "wikipedia", "excellent",
                      "64 six-line symbols for divination", "hexagram_system"),
            SourceLink("https://en.wikipedia.org/wiki/Bagua",
                      "Bagua (Eight Trigrams) - Wikipedia", "wikipedia", "excellent", 
                      "Foundation elements of I Ching system", "trigram_system")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/King_Wen_of_Zhou",
                      "King Wen of Zhou - Wikipedia", "wikipedia", "good",
                      "Traditional author of I Ching hexagram sequence", "historical_figures"),
            SourceLink("https://en.wikipedia.org/wiki/Confucius",
                      "Confucius - Wikipedia", "wikipedia", "excellent",
                      "Traditional commentator on I Ching", "historical_figures"),
            SourceLink("https://en.wikipedia.org/wiki/Richard_Wilhelm_(sinologist)",
                      "Richard Wilhelm - Wikipedia", "wikipedia", "good",
                      "German translator of definitive I Ching edition", "translators"),
            SourceLink("https://en.wikipedia.org/wiki/Yarrow_stalk_divination",
                      "Yarrow Stalk Divination - Wikipedia", "wikipedia", "good",
                      "Traditional method of I Ching consultation", "divination_methods")
        ],
        academic_sources=[],
        archive_sources=[],
        research_keywords=[
            "i ching", "book of changes", "64 hexagrams", "eight trigrams bagua",
            "chinese divination", "wilhelm translation", "yarrow stalks", "changing lines"
        ],
        cross_references=["taoism", "confucianism", "chinese_philosophy", "divination"]
    ),

    # 🔬 PRIORITY 3: SPECIALIZED TRADITIONS
    "kuji_kiri": TraditionResearch(
        name="kuji_kiri",
        display_name="Kuji-kiri (Nine Symbolic Cuts)",
        priority=TraditionPriority.SPECIALIZED,
        complexity=ResearchComplexity.MEDIUM,
        estimated_entries=10,
        subcategories=[
            "Nine Symbolic Cuts Foundation", "Mudra Power Hand Gestures", "Energy Direction Ki Chi",
            "Protection Magic Methods", "Rin Strength Mudra", "Pyo Energy Direction",
            "Toh Harmony Balance", "Sha Healing Restoration", "Kai Intuition Perception",
            "Mantra Integration Vocal", "Meditation Applications Spiritual"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Kuji-kiri",
                      "Kuji-kiri - Wikipedia", "wikipedia", "good",
                      "Japanese esoteric Buddhist hand gesture system", "overview"),
            SourceLink("https://en.wikipedia.org/wiki/Mudra",
                      "Mudra - Wikipedia", "wikipedia", "excellent",
                      "Sacred hand gestures in spiritual traditions", "hand_gestures"),
            SourceLink("https://en.wikipedia.org/wiki/Shugend%C5%8D",
                      "Shugendō - Wikipedia", "wikipedia", "good",
                      "Japanese mountain asceticism and esoteric Buddhism", "japanese_esotericism")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Ninja",
                      "Ninja - Wikipedia", "wikipedia", "excellent", 
                      "Historical practitioners of kuji-kiri techniques", "historical_context"),
            SourceLink("https://en.wikipedia.org/wiki/Esoteric_Buddhism",
                      "Esoteric Buddhism - Wikipedia", "wikipedia", "excellent",
                      "Buddhist tantric traditions including mudra practice", "buddhist_context"),
            SourceLink("https://en.wikipedia.org/wiki/Onmy%C5%8Dd%C5%8D",
                      "Onmyōdō - Wikipedia", "wikipedia", "good",
                      "Japanese esoteric cosmology and magic", "japanese_magic")
        ],
        academic_sources=[],
        archive_sources=[],
        research_keywords=[
            "kuji kiri", "nine cuts", "ninja mudra", "japanese mudra", "shugendo",
            "esoteric buddhism", "hand seals", "ninja magic", "japanese esotericism"
        ],
        cross_references=["buddhism", "taoism", "meditation", "energy_work"]
    ),

    "chaos_magic": TraditionResearch(
        name="chaos_magic", 
        display_name="Chaos Magic",
        priority=TraditionPriority.SPECIALIZED,
        complexity=ResearchComplexity.MEDIUM,
        estimated_entries=10,
        subcategories=[
            "Paradigm Shifting Belief Tools", "Results Based Practice", "Gnosis States Altered Consciousness",
            "Reality Hacking Consensus", "Sigil Magic Austin Spare", "Servitor Creation Thoughtforms",
            "Paradigm Adoption Temporary", "Gnosis Induction Methods", "Discordian Techniques Humor",
            "Nothing True Everything Permitted", "Belief as Tool Pragmatic"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Chaos_magic",
                      "Chaos Magic - Wikipedia", "wikipedia", "excellent",
                      "Modern experimental magical approach", "overview"),
            SourceLink("https://en.wikipedia.org/wiki/Austin_Osman_Spare",
                      "Austin Osman Spare - Wikipedia", "wikipedia", "excellent",
                      "Artist and magician who developed sigil magic", "founders"),
            SourceLink("https://en.wikipedia.org/wiki/Sigil",
                      "Sigil - Wikipedia", "wikipedia", "excellent",
                      "Magical symbols for encoding desire", "techniques")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Peter_J._Carroll",
                      "Peter J. Carroll - Wikipedia", "wikipedia", "good",
                      "Key modern chaos magic theorist", "modern_practitioners"),
            SourceLink("https://en.wikipedia.org/wiki/Ray_Sherwin",
                      "Ray Sherwin - Wikipedia", "wikipedia", "good", 
                      "Co-founder of modern chaos magic movement", "modern_practitioners"),
            SourceLink("https://en.wikipedia.org/wiki/Discordianism",
                      "Discordianism - Wikipedia", "wikipedia", "good",
                      "Religion/philosophy influencing chaos magic", "influences")
        ],
        academic_sources=[],
        archive_sources=[],
        research_keywords=[
            "chaos magic", "sigil magic", "austin osman spare", "peter carroll",
            "paradigm shifting", "reality hacking", "servitor creation", "gnosis states"
        ],
        cross_references=["golden_dawn", "thelema", "postmodernism", "psychology"]
    ),

    "norse_traditions": TraditionResearch(
        name="norse_traditions",
        display_name="Norse/Germanic Traditions",
        priority=TraditionPriority.SPECIALIZED, 
        complexity=ResearchComplexity.MEDIUM,
        estimated_entries=12,
        subcategories=[
            "Wyrd Web of Fate", "Honor Personal Integrity", "Ragnarok Cyclical Renewal",
            "Nine Worlds Yggdrasil", "Ancestor Veneration", "Runic Divination Elder Futhark",
            "Galdr Vocal Magic", "Blót Offering Rituals", "Utiseta Sitting Out Visions",
            "Seidr Shamanic Practices", "Norse Pantheon Aesir Vanir", "Nine Noble Virtues"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Norse_mythology",
                      "Norse Mythology - Wikipedia", "wikipedia", "excellent",
                      "Comprehensive overview of Norse mythological system", "overview"),
            SourceLink("https://en.wikipedia.org/wiki/Germanic_paganism",
                      "Germanic Paganism - Wikipedia", "wikipedia", "excellent",
                      "Pre-Christian Germanic religious practices", "historical_context"),
            SourceLink("https://en.wikipedia.org/wiki/Runes",
                      "Runes - Wikipedia", "wikipedia", "excellent",
                      "Germanic alphabetic script with magical significance", "runic_system")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Elder_Futhark",
                      "Elder Futhark - Wikipedia", "wikipedia", "excellent",
                      "Oldest form of runic alphabet", "runic_alphabets"),
            SourceLink("https://en.wikipedia.org/wiki/Yggdrasil",
                      "Yggdrasil - Wikipedia", "wikipedia", "excellent",
                      "World Tree in Norse cosmology", "cosmology"),
            SourceLink("https://en.wikipedia.org/wiki/Seid",
                      "Seidr - Wikipedia", "wikipedia", "good",
                      "Norse shamanic and magical practices", "magical_practices"),
            SourceLink("https://en.wikipedia.org/wiki/Blót",
                      "Blót - Wikipedia", "wikipedia", "good",
                      "Norse sacrificial and offering rituals", "ritual_practices")
        ],
        academic_sources=[],
        archive_sources=[],
        research_keywords=[
            "norse mythology", "elder futhark", "runes divination", "seidr magic",
            "yggdrasil world tree", "norse gods", "blot ritual", "galdr", "wyrd fate"
        ],
        cross_references=["shamanism", "divination", "ancestor_worship", "european_paganism"]
    ),

    "sufi_mysticism": TraditionResearch(
        name="sufi_mysticism",
        display_name="Sufi Mysticism",
        priority=TraditionPriority.SPECIALIZED,
        complexity=ResearchComplexity.MEDIUM,
        estimated_entries=11,
        subcategories=[
            "Fana Passing Away Ego", "Baqa Subsistence God", "Dhikr Remembrance Allah",
            "Tariqah Sufi Order Path", "Hal vs Maqam States", "Sohbet Spiritual Conversation",
            "Sama Sacred Music Dance", "Muraqaba Meditation Contemplation", "Breath Work Sacred",
            "Service Others Worship", "Beloved Divine Love", "Whirling Dance Spiritual"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Sufism",
                      "Sufism - Wikipedia", "wikipedia", "excellent",
                      "Islamic mystical tradition and practices", "overview"),  
            SourceLink("https://en.wikipedia.org/wiki/Rumi",
                      "Rumi - Wikipedia", "wikipedia", "excellent",
                      "Greatest Sufi poet and mystic", "sufi_masters"),
            SourceLink("https://en.wikipedia.org/wiki/Dhikr",
                      "Dhikr - Wikipedia", "wikipedia", "excellent", 
                      "Remembrance of Allah through repetition", "practices")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Whirling_dervishes",
                      "Whirling Dervishes - Wikipedia", "wikipedia", "excellent",
                      "Mevlevi order spinning meditation practice", "practices"),
            SourceLink("https://en.wikipedia.org/wiki/Tariqa",
                      "Tariqa - Wikipedia", "wikipedia", "good",
                      "Sufi orders and spiritual paths", "sufi_orders"),
            SourceLink("https://en.wikipedia.org/wiki/Ibn_Arabi", 
                      "Ibn Arabi - Wikipedia", "wikipedia", "excellent",
                      "Great Sufi metaphysician and mystic", "sufi_masters"),
            SourceLink("https://en.wikipedia.org/wiki/Al-Hallaj",
                      "Al-Hallaj - Wikipedia", "wikipedia", "good",
                      "Controversial early Sufi mystic", "sufi_masters")
        ],
        academic_sources=[],
        archive_sources=[],
        research_keywords=[
            "sufism", "sufi mysticism", "rumi poetry", "whirling dervish", "dhikr remembrance",
            "fana baqa", "sufi masters", "islamic mysticism", "tariqa orders"
        ],
        cross_references=["islamic_mysticism", "meditation", "sacred_dance", "mystical_poetry"]
    ),

    "celtic_druidic": TraditionResearch(
        name="celtic_druidic",
        display_name="Celtic Druidic Traditions",
        priority=TraditionPriority.SPECIALIZED,
        complexity=ResearchComplexity.MEDIUM,
        estimated_entries=11,
        subcategories=[
            "Awen Divine Inspiration", "Otherworld Parallel Realm", "Land Connection Sacred",
            "Seasonal Cycles Eight Festivals", "Tree Wisdom Species Knowledge", "Ogham Tree Alphabet",
            "Seasonal Celebrations Wheel Year", "Land Working Spirit Place", "Bardic Arts Poetry Music",
            "Herb Craft Plant Medicine", "Celtic Pantheon Deities", "Sacred Sites Stone Circles"
        ],
        primary_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Druidry_(modern)",
                      "Modern Druidry - Wikipedia", "wikipedia", "excellent",
                      "Contemporary Celtic spiritual revival", "modern_druidry"),
            SourceLink("https://en.wikipedia.org/wiki/Celtic_mythology",
                      "Celtic Mythology - Wikipedia", "wikipedia", "excellent", 
                      "Mythological traditions of Celtic peoples", "mythology"),
            SourceLink("https://en.wikipedia.org/wiki/Ogham",
                      "Ogham - Wikipedia", "wikipedia", "excellent",
                      "Ancient Celtic tree alphabet", "ogham_alphabet")
        ],
        wikipedia_sources=[
            SourceLink("https://en.wikipedia.org/wiki/Wheel_of_the_Year",
                      "Wheel of the Year - Wikipedia", "wikipedia", "excellent",
                      "Eight seasonal festivals in modern paganism", "seasonal_festivals"),
            SourceLink("https://en.wikipedia.org/wiki/Celtic_calendar",
                      "Celtic Calendar - Wikipedia", "wikipedia", "good",
                      "Ancient Celtic time-keeping systems", "calendar_systems"),
            SourceLink("https://en.wikipedia.org/wiki/Celtic_deities", 
                      "Celtic Deities - Wikipedia", "wikipedia", "excellent",
                      "Gods and goddesses of Celtic pantheon", "celtic_pantheon"),
            SourceLink("https://en.wikipedia.org/wiki/Awen",
                      "Awen - Wikipedia", "wikipedia", "good",
                      "Celtic concept of divine inspiration", "concepts")
        ],
        academic_sources=[],
        archive_sources=[],
        research_keywords=[
            "celtic druid", "ogham alphabet", "wheel of year", "celtic mythology",
            "seasonal festivals", "tree wisdom", "awen inspiration", "celtic deities"
        ],
        cross_references=["nature_worship", "seasonal_celebrations", "tree_magic", "european_paganism"]
    )
} 

# 🔍 RESEARCH AUTOMATION CLASSES

class LighthouseResearchOrchestrator:
    """
    Orchestrates research collection for all wisdom traditions
    Integrates Google Search API, Academic API, and wiki parsing
    """
    
    def __init__(self, google_api_key: str, use_semantic_scholar: bool = True):
        self.google_api_key = google_api_key
        self.use_semantic_scholar = use_semantic_scholar
        self.semantic_scholar_base_url = "https://api.semanticscholar.org/graph/v1"
        self.session_results = {}
        
        logger.info("🏛️ Lighthouse Research Orchestrator initialized with Semantic Scholar")
    
    def get_research_blocks(self) -> List[Dict]:
        """
        Break research into optimized blocks for Claude API calls
        Each block contains 3-4 traditions max for manageable processing
        """
        blocks = []
        
        # Block 1: Critical Foundations
        blocks.append({
            "block_id": "critical_foundations",
            "priority": "CRITICAL",
            "traditions": ["golden_dawn", "thelema", "egyptian_magic"],
            "estimated_api_calls": 3,
            "focus": "Complete foundational Western magical traditions"
        })
        
        # Block 2: Eastern Wisdom Systems
        blocks.append({
            "block_id": "eastern_wisdom",
            "priority": "HIGH",
            "traditions": ["taoism", "i_ching", "kuji_kiri"],
            "estimated_api_calls": 3,
            "focus": "Chinese and Japanese wisdom traditions"
        })
        
        # Block 3: Classical & Gnostic Philosophy
        blocks.append({
            "block_id": "classical_gnostic",
            "priority": "HIGH", 
            "traditions": ["classical_philosophy", "gnostic_traditions"],
            "estimated_api_calls": 2,
            "focus": "Philosophical foundations and early Christian mysticism"
        })
        
        # Block 4: Divination & Sacred Systems
        blocks.append({
            "block_id": "divination_sacred",
            "priority": "MEDIUM",
            "traditions": ["tarot_knowledge", "sacred_geometry"],
            "estimated_api_calls": 2,
            "focus": "Symbolic systems and mathematical mysticism"
        })
        
        # Block 5: Modern & Experimental
        blocks.append({
            "block_id": "modern_experimental", 
            "priority": "SPECIALIZED",
            "traditions": ["chaos_magic", "norse_traditions"],
            "estimated_api_calls": 2,
            "focus": "Modern magical experimentation and Norse wisdom"
        })
        
        # Block 6: Mystical Traditions
        blocks.append({
            "block_id": "mystical_traditions",
            "priority": "SPECIALIZED",
            "traditions": ["sufi_mysticism", "celtic_druidic"],
            "estimated_api_calls": 2,
            "focus": "Islamic and Celtic mystical paths"
        })
        
        logger.info(f"📋 Created {len(blocks)} research blocks covering {sum(len(b['traditions']) for b in blocks)} traditions")
        return blocks
    
    def generate_enhanced_search_queries(self, tradition_name: str) -> List[str]:
        """
        Generate comprehensive search queries for each tradition
        Focus on wiki sources, academic resources, and fan wikis
        """
        tradition = LIGHTHOUSE_TRADITIONS[tradition_name]
        queries = []
        
        # Primary overview queries
        queries.extend([
            f"{tradition.display_name} wikipedia",
            f"{tradition.display_name} academic research",
            f"{tradition.display_name} scholarly articles",
            f"{tradition.display_name} encyclopedia britannica"
        ])
        
        # Subcategory-specific queries
        for subcategory in tradition.subcategories[:6]:  # Top 6 subcategories
            queries.extend([
                f'"{subcategory}" wikipedia',
                f'"{subcategory}" academic wiki',
                f'"{subcategory}" scholarly source'
            ])
        
        # Specialized wiki queries
        if tradition_name in ["thelema", "golden_dawn", "chaos_magic"]:
            queries.extend([
                f"{tradition.display_name} thelemapedia",
                f"{tradition.display_name} occult wiki",
                f"{tradition.display_name} hermetic library"
            ])
        
        if tradition_name in ["norse_traditions", "celtic_druidic"]:
            queries.extend([
                f"{tradition.display_name} mythology wiki",
                f"{tradition.display_name} folklore database",
                f"{tradition.display_name} historical sources"
            ])
        
        if tradition_name in ["taoism", "i_ching", "kuji_kiri"]:
            queries.extend([
                f"{tradition.display_name} eastern wisdom wiki",
                f"{tradition.display_name} buddhist encyclopedia",
                f"{tradition.display_name} chinese philosophy"
            ])
        
        logger.info(f"🔍 Generated {len(queries)} search queries for {tradition_name}")
        return queries[:20]  # Limit to top 20 queries
    
    async def search_google_api(self, query: str, tradition_name: str) -> List[SourceLink]:
        """
        Search using Google Custom Search API
        Focus on wiki sources and academic content
        """
        # This would integrate with actual Google API
        # For now, return structured placeholder results
        
        wiki_domains = [
            "wikipedia.org", "wikimedia.org", "britannica.com",
            "thelemapedia.org", "occult-world.com", "hermetic.com",
            "stanford.edu", "plato.stanford.edu", "academia.edu"
        ]
        
        results = []
        
        # Simulate API response parsing
        for domain in wiki_domains[:3]:  # Top 3 domains per query
            source = SourceLink(
                url=f"https://{domain}/search?q={query.replace(' ', '+')}", 
                title=f"{query.title()} - {domain.split('.')[0].title()}",
                type="wikipedia" if "wiki" in domain else "academic",
                quality="excellent" if domain in ["wikipedia.org", "britannica.com", "stanford.edu"] else "good",
                description=f"Comprehensive {query} information from {domain}",
                subcategory=self._categorize_query(query, tradition_name)
            )
            results.append(source)
        
        logger.info(f"🌐 Found {len(results)} sources for query: {query}")
        return results
    
    async def search_semantic_scholar_api(self, tradition_name: str) -> List[SourceLink]:
        """
        Search Semantic Scholar API for academic papers on wisdom traditions
        Free API from AI2 with great coverage of philosophy, religion, mysticism
        """
        tradition = LIGHTHOUSE_TRADITIONS[tradition_name]
        academic_results = []
        
        # Semantic Scholar search queries
        scholar_queries = [
            f'"{tradition.display_name}" religious studies',
            f'"{tradition.display_name}" comparative religion', 
            f'"{tradition.display_name}" mysticism',
            f'"{tradition.display_name}" philosophy religion',
            f'"{tradition.display_name}" esoteric tradition'
        ]
        
        for query in scholar_queries[:3]:  # Top 3 academic queries
            # Semantic Scholar API endpoint for paper search
            api_url = f"{self.semantic_scholar_base_url}/paper/search"
            
            # Simulate API response - in real implementation would make HTTP request
            for i in range(2):  # 2 papers per query
                paper_source = SourceLink(
                    url=f"{api_url}?query={query.replace(' ', '+')}&limit=10",
                    title=f"Academic Research: {query}",
                    type="academic_paper",
                    quality="excellent", 
                    description=f"Semantic Scholar academic papers on {query}",
                    subcategory="academic_research"
                )
                academic_results.append(paper_source)
        
        logger.info(f"🎓 Found {len(academic_results)} Semantic Scholar sources for {tradition_name}")
        return academic_results
    
    def _categorize_query(self, query: str, tradition_name: str) -> str:
        """
        Categorize search query into subcategory type
        """
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["philosophy", "principle", "concept", "theory"]):
            return "philosophy_concepts"
        elif any(word in query_lower for word in ["practice", "ritual", "technique", "method"]):
            return "practices_rituals"
        elif any(word in query_lower for word in ["history", "historical", "ancient", "origin"]):
            return "historical_context"
        elif any(word in query_lower for word in ["system", "structure", "organization", "order"]):
            return "systems_structures"
        else:
            return "general_overview"

    async def execute_research_block(self, block: Dict) -> Dict:
        """
        Execute complete research for one tradition block
        Returns comprehensive source collection ready for Claude API
        """
        block_id = block["block_id"]
        traditions = block["traditions"]
        
        logger.info(f"🔬 Executing research block: {block_id}")
        
        block_results = {
            "block_id": block_id,
            "priority": block["priority"],
            "traditions_researched": {},
            "total_sources": 0,
            "claude_api_ready": True
        }
        
        for tradition_name in traditions:
            tradition_sources = await self._research_single_tradition(tradition_name)
            block_results["traditions_researched"][tradition_name] = tradition_sources
            block_results["total_sources"] += len(tradition_sources["all_sources"])
        
        logger.info(f"✅ Block {block_id} complete: {block_results['total_sources']} sources across {len(traditions)} traditions")
        return block_results
    
    async def _research_single_tradition(self, tradition_name: str) -> Dict:
        """
        Complete research pipeline for single tradition
        """
        logger.info(f"📚 Researching tradition: {tradition_name}")
        
        # Generate search queries
        search_queries = self.generate_enhanced_search_queries(tradition_name)
        
        # Collect sources from multiple APIs
        google_sources = []
        for query in search_queries[:10]:  # Top 10 queries for Google
            sources = await self.search_google_api(query, tradition_name)
            google_sources.extend(sources)
        
        academic_sources = await self.search_semantic_scholar_api(tradition_name)
        
        # Combine and deduplicate sources
        all_sources = google_sources + academic_sources
        unique_sources = self._deduplicate_sources(all_sources)
        
        # Categorize sources by type
        categorized_sources = self._categorize_sources(unique_sources)
        
        tradition_results = {
            "tradition_name": tradition_name,
            "display_name": LIGHTHOUSE_TRADITIONS[tradition_name].display_name,
            "search_queries_used": search_queries,
            "all_sources": unique_sources,
            "categorized_sources": categorized_sources,
            "source_count": len(unique_sources),
            "research_quality": self._assess_research_quality(unique_sources)
        }
        
        logger.info(f"📖 {tradition_name} research complete: {len(unique_sources)} unique sources")
        return tradition_results
    
    def _deduplicate_sources(self, sources: List[SourceLink]) -> List[SourceLink]:
        """
        Remove duplicate sources based on URL and title similarity
        """
        unique_sources = []
        seen_urls = set()
        seen_titles = set()
        
        for source in sources:
            # Check URL uniqueness
            if source.url in seen_urls:
                continue
                
            # Check title similarity (basic deduplication)
            title_words = set(source.title.lower().split())
            is_similar = False
            
            for seen_title in seen_titles:
                seen_words = set(seen_title.lower().split())
                overlap = len(title_words & seen_words) / len(title_words | seen_words)
                if overlap > 0.7:  # 70% similarity threshold
                    is_similar = True
                    break
            
            if not is_similar:
                unique_sources.append(source)
                seen_urls.add(source.url)
                seen_titles.add(source.title)
        
        return unique_sources
    
    def _categorize_sources(self, sources: List[SourceLink]) -> Dict[str, List[SourceLink]]:
        """
        Organize sources by type and quality for easy access
        """
        categorized = {
            "wikipedia_excellent": [],
            "wikipedia_good": [],
            "academic_excellent": [],
            "academic_good": [],
            "specialized_wikis": [],
            "reference_sources": []
        }
        
        for source in sources:
            if source.type == "wikipedia":
                if source.quality == "excellent":
                    categorized["wikipedia_excellent"].append(source)
                else:
                    categorized["wikipedia_good"].append(source)
            elif source.type == "academic":
                if source.quality == "excellent":
                    categorized["academic_excellent"].append(source)
                else:
                    categorized["academic_good"].append(source)
            elif "wiki" in source.url.lower() or "pedia" in source.url.lower():
                categorized["specialized_wikis"].append(source)
            else:
                categorized["reference_sources"].append(source)
        
        return categorized
    
    def _assess_research_quality(self, sources: List[SourceLink]) -> str:
        """
        Assess overall quality of research sources collected
        """
        if not sources:
            return "INSUFFICIENT"
        
        excellent_count = len([s for s in sources if s.quality == "excellent"])
        total_count = len(sources)
        excellent_ratio = excellent_count / total_count
        
        if excellent_ratio >= 0.6 and total_count >= 15:
            return "EXCELLENT"
        elif excellent_ratio >= 0.4 and total_count >= 10:
            return "GOOD"
        elif total_count >= 8:
            return "ADEQUATE"
        else:
            return "NEEDS_IMPROVEMENT"

class ClaudeAPIIntegration:
    """
    Integrates research results with Claude API for knowledge entry generation
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        logger.info("🤖 Claude API Integration initialized")
    
    def create_knowledge_generation_prompt(self, tradition_research: Dict) -> str:
        """
        Create comprehensive prompt for Claude to generate knowledge entries
        """
        tradition_name = tradition_research["tradition_name"]
        tradition_data = LIGHTHOUSE_TRADITIONS[tradition_name]
        sources = tradition_research["categorized_sources"]
        
        prompt = f"""
🏛️ THE LIGHTHOUSE PROJECT: KNOWLEDGE ENTRY GENERATION

You are The Lighthouse Chronicler, tasked with creating comprehensive knowledge entries for humanity's sacred wisdom preservation system. This knowledge will be inscribed on-chain for eternal preservation.

## TRADITION: {tradition_data.display_name}

### RESEARCH CONTEXT:
- Total Sources: {tradition_research['source_count']}
- Research Quality: {tradition_research['research_quality']}
- Priority Level: {tradition_data.priority.value}
- Complexity: {tradition_data.complexity.value}

### SUBCATEGORIES TO COVER:
{chr(10).join([f"- {cat}" for cat in tradition_data.subcategories])}

### SOURCE MATERIALS AVAILABLE:
**Wikipedia (Excellent):** {len(sources['wikipedia_excellent'])} sources
**Academic (Excellent):** {len(sources['academic_excellent'])} sources  
**Specialized Wikis:** {len(sources['specialized_wikis'])} sources

### KEY RESEARCH AREAS:
{chr(10).join([f"- {kw}" for kw in tradition_data.research_keywords])}

### CROSS-REFERENCES:
Connected to: {', '.join(tradition_data.cross_references)}

## YOUR TASK:
Create {tradition_data.estimated_entries} comprehensive KnowledgeEntry objects for this tradition.

## QUALITY REQUIREMENTS:
- BLOCKCHAIN-READY: 500-1000 words per entry, optimized for permanent storage
- CULTURAL AUTHENTICITY: Respectful treatment of sacred concepts
- PRIMARY SOURCE ACCURACY: Verify claims against provided sources
- PRACTICAL APPLICATION: Include modern relevance and usage
- CROSS-TRADITION CONNECTIONS: Link to related concepts in other traditions

## OUTPUT FORMAT:
```python
TRADITION_KNOWLEDGE_ENTRIES = [
    KnowledgeEntry(
        id="{tradition_name}_principle_001",
        tradition="{tradition_name}",
        title="Clear Descriptive Title",
        summary="2-3 sentence overview for quick reference",
        full_content=\"\"\"
        Detailed 500-1000 word explanation covering:
        - Historical context and origins
        - Core principles and meanings
        - Practical applications and methods
        - Cross-references to related concepts
        - Modern interpretations and relevance
        \"\"\",
        knowledge_type=KnowledgeType.PRINCIPLE,
        tags=["relevant", "searchable", "keywords"],
        related_concepts=["cross_tradition_references"],
        source_url="primary_wikipedia_or_academic_source",
        confidence_score=0.90,
        quality=ContentQuality.HIGH,
        preservation_priority="critical"
    ),
    # ... continue for all {tradition_data.estimated_entries} entries
]
```

Generate comprehensive, authentic knowledge entries ready for The Lighthouse eternal preservation system.
"""
        
        return prompt.strip()

# 🚀 MAIN EXECUTION FUNCTIONS

async def execute_lighthouse_research_pipeline():
    """
    Main execution function for complete Lighthouse research automation
    """
    
    logger.info("🏛️ LIGHTHOUSE RESEARCH PIPELINE STARTING")
    logger.info("=" * 60)
    
    # Initialize research orchestrator with Semantic Scholar
    # Get API key from environment variables
    import os
    google_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_SEARCH_API_KEY environment variable is required")
    
    orchestrator = LighthouseResearchOrchestrator(
        google_api_key=google_api_key,
        use_semantic_scholar=True
    )
    
    # Get research blocks for optimized processing
    research_blocks = orchestrator.get_research_blocks()
    
    # Execute research for each block
    all_block_results = []
    
    for i, block in enumerate(research_blocks, 1):
        logger.info(f"📋 Processing Block {i}/{len(research_blocks)}: {block['block_id']}")
        
        block_results = await orchestrator.execute_research_block(block)
        all_block_results.append(block_results)
        
        # Log block completion
        logger.info(f"✅ Block {block['block_id']} complete")
        logger.info(f"   Sources collected: {block_results['total_sources']}")
        logger.info(f"   Traditions researched: {len(block_results['traditions_researched'])}")
        logger.info("-" * 40)
    
    # Generate summary report
    summary_report = generate_research_summary(all_block_results)
    
    # Save results to JSON for Claude API processing
    save_research_results(all_block_results, summary_report)
    
    logger.info("🎉 LIGHTHOUSE RESEARCH PIPELINE COMPLETE")
    return all_block_results, summary_report

def generate_research_summary(all_block_results: List[Dict]) -> Dict:
    """
    Generate comprehensive summary of research collection
    """
    
    total_traditions = sum(len(block["traditions_researched"]) for block in all_block_results)
    total_sources = sum(block["total_sources"] for block in all_block_results)
    
    # Analyze source quality distribution
    quality_distribution = {"EXCELLENT": 0, "GOOD": 0, "ADEQUATE": 0, "NEEDS_IMPROVEMENT": 0}
    tradition_details = {}
    
    for block in all_block_results:
        for tradition_name, tradition_data in block["traditions_researched"].items():
            quality = tradition_data["research_quality"] 
            quality_distribution[quality] += 1
            
            tradition_details[tradition_name] = {
                "display_name": tradition_data["display_name"],
                "source_count": tradition_data["source_count"],
                "research_quality": quality,
                "estimated_entries": LIGHTHOUSE_TRADITIONS[tradition_name].estimated_entries,
                "priority": LIGHTHOUSE_TRADITIONS[tradition_name].priority.value
            }
    
    summary = {
        "pipeline_completion": "SUCCESS",
        "total_traditions_researched": total_traditions,
        "total_sources_collected": total_sources,
        "average_sources_per_tradition": round(total_sources / total_traditions, 1),
        "research_quality_distribution": quality_distribution,
        "tradition_details": tradition_details,
        "blocks_processed": len(all_block_results),
        "claude_api_calls_needed": sum(len(block["traditions_researched"]) for block in all_block_results),
        "estimated_knowledge_entries": sum(
            LIGHTHOUSE_TRADITIONS[name].estimated_entries 
            for block in all_block_results 
            for name in block["traditions_researched"]
        )
    }
    
    # Log summary
    logger.info("📊 RESEARCH SUMMARY GENERATED")
    logger.info(f"   Traditions: {summary['total_traditions_researched']}")
    logger.info(f"   Sources: {summary['total_sources_collected']}")
    logger.info(f"   Avg Sources/Tradition: {summary['average_sources_per_tradition']}")
    logger.info(f"   Quality Distribution: {summary['research_quality_distribution']}")
    logger.info(f"   Est. Knowledge Entries: {summary['estimated_knowledge_entries']}")
    
    return summary

def save_research_results(all_block_results: List[Dict], summary: Dict):
    """
    Save research results to JSON files for Claude API processing
    """
    
    # Save complete results
    complete_results = {
        "research_summary": summary,
        "research_blocks": all_block_results,
        "lighthouse_traditions_registry": {
            name: asdict(tradition) for name, tradition in LIGHTHOUSE_TRADITIONS.items()
        }
    }
    
    with open("lighthouse_research_results.json", "w") as f:
        json.dump(complete_results, f, indent=2, default=str)
    
    # Save individual tradition files for easier processing
    for block in all_block_results:
        for tradition_name, tradition_data in block["traditions_researched"].items():
            filename = f"research_{tradition_name}.json"
            with open(filename, "w") as f:
                json.dump(tradition_data, f, indent=2, default=str)
    
    logger.info("💾 Research results saved to JSON files")
    logger.info("   Complete results: lighthouse_research_results.json")
    logger.info("   Individual traditions: research_[tradition_name].json")

def print_tradition_source_index():
    """
    Print comprehensive source index for all traditions
    """
    
    print("\n🏛️ THE LIGHTHOUSE PROJECT: COMPREHENSIVE SOURCE INDEX")
    print("=" * 80)
    
    for priority_level in [TraditionPriority.CRITICAL, TraditionPriority.HIGH, 
                          TraditionPriority.MEDIUM, TraditionPriority.SPECIALIZED]:
        
        traditions_in_priority = [
            (name, tradition) for name, tradition in LIGHTHOUSE_TRADITIONS.items()
            if tradition.priority == priority_level
        ]
        
        if not traditions_in_priority:
            continue
            
        print(f"\n🔥 {priority_level.value.upper()} PRIORITY ({len(traditions_in_priority)} traditions)")
        print("-" * 60)
        
        for tradition_name, tradition_data in traditions_in_priority:
            print(f"\n📚 {tradition_data.display_name}")
            print(f"   Complexity: {tradition_data.complexity.value}")
            print(f"   Est. Entries: {tradition_data.estimated_entries}")
            print(f"   Subcategories: {len(tradition_data.subcategories)}")
            
            print(f"\n   📖 Primary Sources ({len(tradition_data.primary_sources)}):")
            for source in tradition_data.primary_sources:
                print(f"      • {source.title} - {source.quality}")
                print(f"        {source.url}")
            
            print(f"\n   🔍 Research Keywords:")
            print(f"      {', '.join(tradition_data.research_keywords)}")
            
            print(f"\n   🔗 Cross-References:")
            print(f"      {', '.join(tradition_data.cross_references)}")
            print()
    
    # Summary statistics
    total_traditions = len(LIGHTHOUSE_TRADITIONS)
    total_subcategories = sum(len(t.subcategories) for t in LIGHTHOUSE_TRADITIONS.values())
    total_estimated_entries = sum(t.estimated_entries for t in LIGHTHOUSE_TRADITIONS.values())
    total_sources = sum(
        len(t.primary_sources) + len(t.wikipedia_sources) 
        for t in LIGHTHOUSE_TRADITIONS.values()
    )
    
    print("\n📊 LIGHTHOUSE PROJECT STATISTICS")
    print("=" * 40)
    print(f"Total Traditions: {total_traditions}")
    print(f"Total Subcategories: {total_subcategories}")
    print(f"Estimated Knowledge Entries: {total_estimated_entries}")
    print(f"Predefined Sources: {total_sources}")
    print(f"Research Complexity: Mixed (Low to Expert)")
    print(f"Claude API Calls Needed: ~{total_traditions}")
    print(f"Estimated Implementation Time: 15-20 sessions")

if __name__ == "__main__":
    # Print source index
    print_tradition_source_index()
    
    # Uncomment to run full research pipeline
    # asyncio.run(execute_lighthouse_research_pipeline()) 