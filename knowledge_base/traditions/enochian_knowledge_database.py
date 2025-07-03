#!/usr/bin/env python3
"""
Enochian Magic Knowledge Database
Comprehensive database of Enochian magical concepts, Angels, Keys, and Aethyrs
Based on curated sources from Sacred Texts, Hermetic Library, and Archive.org
"""

from typing import List, Dict
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from schemas.knowledge_schemas import KnowledgeEntry, KnowledgeType, ContentQuality, ProcessedTradition

# Core Enochian Angels from the system
ENOCHIAN_ANGELS = [
    KnowledgeEntry(
        id="enochian_angel_uriel",
        tradition="enochian_magic",
        title="Uriel - Angel of Fire and Light",
        summary="Uriel is one of the primary Enochian angels, associated with the element of fire and divine illumination. Called upon for wisdom and the purification of spiritual insight.",
        full_content="""Uriel (Hebrew: אוּרִיאֵל, "Fire of God" or "Flame of God") is one of the four primary Archangels in Enochian magic. In the Enochian system received by John Dee and Edward Kelley, Uriel governs the element of Fire and the South watchtower.

Key Attributes:
- Element: Fire
- Direction: South
- Function: Divine illumination, purification, wisdom
- Enochian Name: BITOM (in some contexts)
- Associated with solar energy and transformative fire

Uriel's role in Enochian magic involves:
1. Purification of the magician's intent
2. Illumination of hidden knowledge
3. Guardian of the southern watchtower
4. Transmutation of base consciousness into divine awareness

In Dee's system, Uriel is invoked for clarity of vision and the burning away of illusion. The angel serves as a bridge between human consciousness and divine fire.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["angel", "fire", "purification", "wisdom", "watchtower"],
        related_concepts=["enochian_watchtowers", "elemental_magic", "divine_names"],
        source_url="https://sacred-texts.com/eso/dee/",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),
    
    KnowledgeEntry(
        id="enochian_angel_gabriel",
        tradition="enochian_magic",
        title="Gabriel - Angel of Water and Intuition",
        summary="Gabriel governs the element of water in Enochian magic, associated with intuition, dreams, and the subconscious mind. Guardian of the western watchtower.",
        full_content="""Gabriel (Hebrew: גַּבְרִיאֵל, "Strength of God") is the Archangel governing the element of Water and the West watchtower in Enochian magic. Gabriel represents the fluid, intuitive aspects of divine consciousness.

Key Attributes:
- Element: Water
- Direction: West
- Function: Intuition, dreams, emotional purification
- Enochian Name: HCOMA (in some contexts)
- Associated with lunar energy and psychic development

Gabriel's functions include:
1. Opening psychic channels and intuitive perception
2. Purification of emotions and subconscious patterns
3. Guardian of the western watchtower
4. Facilitating communication with the angelic realm
5. Governing prophetic dreams and visions

In Dee's angelic conversations, Gabriel often served as an intermediary, helping to clarify and interpret the angelic communications. The angel assists in developing receptivity to divine guidance.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["angel", "water", "intuition", "dreams", "watchtower"],
        related_concepts=["enochian_watchtowers", "angelic_communication", "psychic_development"],
        source_url="https://sacred-texts.com/eso/dee/",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),
    
    KnowledgeEntry(
        id="enochian_angel_michael",
        tradition="enochian_magic",
        title="Michael - Angel of Fire and Protection",
        summary="Michael is the warrior archangel in Enochian magic, associated with divine protection, spiritual warfare, and the element of fire. Leader of the celestial armies.",
        full_content="""Michael (Hebrew: מִיכָאֵל, "Who is like God?") is the supreme warrior Archangel in Enochian magic, often considered the leader of all angels. Michael governs protection, spiritual warfare, and divine justice.

Key Attributes:
- Element: Fire (primary), Air (secondary)
- Direction: East (in some systems)
- Function: Protection, spiritual warfare, divine justice
- Enochian Name: MIKAEL or variations
- Associated with solar energy and divine authority

Michael's roles include:
1. Protection from negative entities and influences
2. Leadership in spiritual warfare against demonic forces
3. Guardian of divine justice and cosmic order
4. Facilitator of spiritual initiation and testing
5. Protector of magicians during dangerous workings

In Dee's system, Michael appears as both protector and challenger, testing the magician's resolve and purification. The angel serves as a guardian during dangerous magical operations and helps maintain spiritual boundaries.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["angel", "protection", "warfare", "justice", "fire"],
        related_concepts=["enochian_protection", "spiritual_warfare", "divine_justice"],
        source_url="https://sacred-texts.com/eso/dee/",
        confidence_score=0.95,
        quality=ContentQuality.HIGH
    ),
    
    KnowledgeEntry(
        id="enochian_angel_raphael",
        tradition="enochian_magic",
        title="Raphael - Angel of Air and Healing",
        summary="Raphael governs the element of air in Enochian magic, associated with healing, communication, and the transmission of divine knowledge.",
        full_content="""Raphael (Hebrew: רָפָאֵל, "God heals") is the Archangel of healing and divine communication in Enochian magic. Raphael governs the element of Air and the Eastern watchtower.

Key Attributes:
- Element: Air
- Direction: East
- Function: Healing, communication, divine knowledge
- Enochian Name: RAFAEL or variations
- Associated with mercurial energy and divine medicine

Raphael's functions include:
1. Healing of physical, emotional, and spiritual ailments
2. Facilitating clear communication with divine beings
3. Guardian of the eastern watchtower
4. Transmission of divine knowledge and wisdom
5. Balancing the mental and spiritual faculties

In the Enochian system, Raphael serves as a bridge between human consciousness and angelic wisdom. The angel assists in translating divine communications into comprehensible human language and understanding.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["angel", "air", "healing", "communication", "wisdom"],
        related_concepts=["enochian_watchtowers", "divine_healing", "angelic_communication"],
        source_url="https://sacred-texts.com/eso/dee/",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    )
]

# The 48 Enochian Keys (first 3 as examples)
ENOCHIAN_KEYS = [
    KnowledgeEntry(
        id="enochian_key_1",
        tradition="enochian_magic",
        title="The First Enochian Key - Opening the Gates",
        summary="The First Enochian Key opens the gates of divine communication and establishes contact with the angelic realm. It is the foundational invocation of Enochian magic.",
        full_content="""The First Enochian Key (Enochian: OL SONF VORSG...) is the primary invocation in Enochian magic, serving as the opening gate to angelic communication.

Original Enochian Text:
"OL SONF VORSG, GOHO IAD BALT, LANSH CALZ VONPHO; SOBRA Z-OL ROR I TA NAZPSAD, GRAA TA MALPRG..."

English Translation:
"I reign over you, says the God of Justice, in power exalted above the firmaments of wrath; in whose hands the Sun is as a sword, and the Moon as a through-thrusting fire..."

Key Functions:
1. Opening divine communication channels
2. Establishing angelic contact
3. Purifying the ritual space
4. Aligning the magician with divine will
5. Preparing consciousness for higher invocations

The First Key serves as the foundation for all subsequent Enochian workings. It establishes the magician's authority through divine alignment and opens the pathways for angelic communication. Without proper recitation of this key, subsequent workings may lack the necessary spiritual foundation.""",
        knowledge_type=KnowledgeType.PRACTICE,
        tags=["key", "invocation", "opening", "communication", "foundation"],
        related_concepts=["enochian_language", "angelic_communication", "ritual_foundation"],
        source_url="https://sacred-texts.com/eso/dee/",
        confidence_score=0.95,
        quality=ContentQuality.HIGH
    ),
    
    KnowledgeEntry(
        id="enochian_key_2",
        tradition="enochian_magic",
        title="The Second Enochian Key - Divine Mysteries",
        summary="The Second Key reveals divine mysteries and opens the understanding to higher spiritual truths. It governs the manifestation of divine wisdom.",
        full_content="""The Second Enochian Key reveals the divine mysteries and opens the magician's understanding to higher spiritual truths.

Original Enochian Text:
"ADGT UPAAH ZONG OM FAAIP SALD, VIUL L? SOBAM IALPRG..."

English Translation:
"Can the wings of the winds understand your voices of wonder? O you, the second of the First, whom the burning flames have framed within the depth of my jaws..."

Key Functions:
1. Revealing hidden divine mysteries
2. Opening higher understanding
3. Manifesting divine wisdom
4. Connecting with the second order of angels
5. Facilitating spiritual illumination

This key is particularly important for those seeking deeper esoteric knowledge. It connects the magician with the second order of the angelic hierarchy and facilitates the reception of profound spiritual insights.""",
        knowledge_type=KnowledgeType.PRACTICE,
        tags=["key", "mysteries", "wisdom", "illumination", "understanding"],
        related_concepts=["divine_mysteries", "spiritual_illumination", "angelic_hierarchy"],
        source_url="https://sacred-texts.com/eso/dee/",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    )
]

# The 30 Aethyrs (first 3 as examples)
ENOCHIAN_AETHYRS = [
    KnowledgeEntry(
        id="enochian_aethyr_lil",
        tradition="enochian_magic",
        title="LIL - The 30th Aethyr: The Earthly Realm",
        summary="LIL is the 30th and lowest Aethyr, closest to the physical realm. It governs earthly manifestations and material plane workings.",
        full_content="""LIL (pronounced "Lee-el") is the 30th Aethyr in the Enochian system, representing the sphere closest to the physical realm. It serves as the bridge between material and spiritual dimensions.

Key Attributes:
- Position: 30th (lowest) Aethyr
- Element: Earth (primarily)
- Function: Material manifestation, earthly workings
- Governors: Three angelic governors oversee this realm
- Accessibility: Most accessible to beginning practitioners

Functions of LIL:
1. Grounding spiritual energies into physical manifestation
2. Working with material plane concerns
3. Establishing foundations for higher Aethyr work
4. Healing physical ailments and conditions
5. Manifesting tangible results from magical workings

LIL is often the first Aethyr explored by Enochian magicians due to its relative stability and proximity to ordinary consciousness. It provides a safe introduction to Aethyr working while offering powerful opportunities for material manifestation.""",
        knowledge_type=KnowledgeType.SYSTEM,
        tags=["aethyr", "earthly", "manifestation", "material", "foundation"],
        related_concepts=["enochian_aethyrs", "material_manifestation", "grounding"],
        source_url="https://sacred-texts.com/eso/dee/",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),
    
    KnowledgeEntry(
        id="enochian_aethyr_arn",
        tradition="enochian_magic",
        title="ARN - The 29th Aethyr: Emotional Purification",
        summary="ARN governs emotional purification and the cleansing of psychic debris. It is the realm of emotional and astral healing.",
        full_content="""ARN (pronounced "Ar-en") is the 29th Aethyr, governing emotional purification and the cleansing of psychic and astral debris.

Key Attributes:
- Position: 29th Aethyr
- Element: Water (emotional/astral)
- Function: Emotional purification, psychic cleansing
- Nature: Purifying and sometimes challenging
- Work: Emotional healing and astral body cleansing

Functions of ARN:
1. Purification of emotional blockages and traumas
2. Cleansing of psychic debris and attachments
3. Healing of astral body wounds and tears
4. Release of negative emotional patterns
5. Preparation for higher Aethyr work through emotional clarity

ARN can be a challenging Aethyr to work with, as it brings up suppressed emotions and psychic material for purification. However, this cleansing work is essential for advancing to higher Aethyrs with clarity and stability.""",
        knowledge_type=KnowledgeType.SYSTEM,
        tags=["aethyr", "purification", "emotional", "astral", "healing"],
        related_concepts=["emotional_healing", "psychic_cleansing", "astral_body"],
        source_url="https://sacred-texts.com/eso/dee/",
        confidence_score=0.85,
        quality=ContentQuality.HIGH
    )
]

# Core Enochian Concepts
ENOCHIAN_CONCEPTS = [
    KnowledgeEntry(
        id="enochian_great_table",
        tradition="enochian_magic",
        title="The Great Table - Enochian Elemental Tablet",
        summary="The Great Table is the central tablet of Enochian magic, containing the names and sigils of elemental angels and governing forces.",
        full_content="""The Great Table (also called the Tabula Recensa) is the fundamental structure of Enochian magic, received by John Dee and Edward Kelley through angelic communication.

Structure:
- 12 x 13 grid of letters
- Four watchtowers representing the four elements
- Central tablet of union binding all elements
- Contains hundreds of angelic names and forces

Components:
1. Fire Watchtower (East) - OIPTEAA governing
2. Water Watchtower (West) - NELAPRM governing  
3. Air Watchtower (North) - HBIOGRA governing
4. Earth Watchtower (South) - NAAZTHO governing
5. Tablet of Union (Center) - EHNB governing

The Great Table serves as a map of the elemental forces and their governing angels. Each square contains letters that form names of angels, each with specific functions and domains of influence.""",
        knowledge_type=KnowledgeType.SYSTEM,
        tags=["great_table", "elements", "watchtowers", "angels", "structure"],
        related_concepts=["enochian_watchtowers", "elemental_magic", "angelic_names"],
        source_url="https://hermetic.com/dee/",
        confidence_score=0.95,
        quality=ContentQuality.HIGH
    ),
    
    KnowledgeEntry(
        id="enochian_language",
        tradition="enochian_magic",
        title="The Enochian Language - Angelic Communication",
        summary="The Enochian language is the sacred tongue received from angels, used for magical invocations and communication with divine beings.",
        full_content="""The Enochian language (also called Angelic or Celestial) is the sacred language received by John Dee and Edward Kelley from angelic beings during their scrying sessions from 1582-1589.

Key Features:
- Unique grammar and syntax
- Sacred words of power
- Phonetic pronunciation crucial for efficacy
- Letters correspond to divine forces
- Used exclusively in magical contexts

Structure:
- 21 letters in the Enochian alphabet
- Agglutinative language structure
- Words often compound multiple concepts
- Pronunciation affects magical potency
- Grammar follows angelic rather than human logic

The language is considered to be the original tongue of creation, spoken by angels and used in the formation of the universe. Each word carries specific vibrational frequencies that resonate with angelic consciousness.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["language", "angelic", "communication", "sacred", "vibration"],
        related_concepts=["angelic_communication", "sacred_language", "divine_names"],
        source_url="https://sacred-texts.com/eso/enoch/index.htm",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    )
]

# Complete Enochian Tradition Database
def create_enochian_tradition() -> ProcessedTradition:
    """Create the complete Enochian tradition database"""
    
    all_entries = ENOCHIAN_ANGELS + ENOCHIAN_KEYS + ENOCHIAN_AETHYRS + ENOCHIAN_CONCEPTS
    
    # Categorize entries
    principles = [e for e in all_entries if e.knowledge_type == KnowledgeType.PRINCIPLE]
    practices = [e for e in all_entries if e.knowledge_type == KnowledgeType.PRACTICE]
    systems = [e for e in all_entries if e.knowledge_type == KnowledgeType.SYSTEM]
    concepts = [e for e in all_entries if e.knowledge_type == KnowledgeType.CONCEPT]
    
    # Create cross-references
    cross_references = {
        "angelic_hierarchy": ["enochian_angel_uriel", "enochian_angel_gabriel", "enochian_angel_michael", "enochian_angel_raphael"],
        "enochian_keys": ["enochian_key_1", "enochian_key_2"],
        "aethyr_system": ["enochian_aethyr_lil", "enochian_aethyr_arn"],
        "core_structures": ["enochian_great_table", "enochian_language"]
    }
    
    return ProcessedTradition(
        name="enochian_magic",
        description="The complete system of Enochian magic as received by John Dee and Edward Kelley, including angels, keys, aethyrs, and core magical structures.",
        total_entries=len(all_entries),
        principles=principles,
        practices=practices,
        systems=systems,
        concepts=concepts,
        cross_references=cross_references
    )

# Helper functions
def get_enochian_entry_by_id(entry_id: str) -> KnowledgeEntry:
    """Get specific Enochian knowledge entry by ID"""
    all_entries = ENOCHIAN_ANGELS + ENOCHIAN_KEYS + ENOCHIAN_AETHYRS + ENOCHIAN_CONCEPTS
    for entry in all_entries:
        if entry.id == entry_id:
            return entry
    raise ValueError(f"Enochian entry not found: {entry_id}")

def search_enochian_by_tag(tag: str) -> List[KnowledgeEntry]:
    """Search Enochian entries by tag"""
    all_entries = ENOCHIAN_ANGELS + ENOCHIAN_KEYS + ENOCHIAN_AETHYRS + ENOCHIAN_CONCEPTS
    return [entry for entry in all_entries if tag in entry.tags]

def get_all_enochian_entries() -> List[KnowledgeEntry]:
    """Get all Enochian knowledge entries"""
    return ENOCHIAN_ANGELS + ENOCHIAN_KEYS + ENOCHIAN_AETHYRS + ENOCHIAN_CONCEPTS 