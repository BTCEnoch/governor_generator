#!/usr/bin/env python3
"""
Golden Dawn Knowledge Database
Comprehensive database of Golden Dawn magical concepts, rituals, and correspondences
Based on curated sources from canon/canon_sources_index.json
"""

from typing import List, Dict
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from schemas.knowledge_schemas import KnowledgeEntry, KnowledgeType, ContentQuality, ProcessedTradition

# LOGGING SETUP (VITAL for debugging)
import logging
logger = logging.getLogger("KnowledgeDB.GoldenDawn")

# Core Golden Dawn Knowledge Entries
GOLDEN_DAWN_KNOWLEDGE_ENTRIES = [
    KnowledgeEntry(
        id="golden_dawn_practice_001",
        tradition="golden_dawn",
        title="Lesser Banishing Ritual of the Pentagram (LBRP)",
        summary="The foundational daily ritual of the Golden Dawn system for clearing negative energies and establishing sacred space. Uses Hebrew divine names and archangelic invocations with pentagram formations.",
        full_content="""The Lesser Banishing Ritual of the Pentagram (LBRP) is the cornerstone practice of Golden Dawn magic, performed daily for spiritual hygiene and magical preparation.

Key Attributes:
- Purpose: Banishing negative influences, centering consciousness, establishing sacred space
- Elements: Four pentagrams drawn in cardinal directions with specific divine names
- Duration: Approximately 5-10 minutes when performed properly
- Frequency: Traditionally performed twice daily (morning and evening)

Ritual Structure:
1. Kabbalistic Cross - Establishing the Tree of Life in the body using Hebrew phrases
2. Pentagram Formation - Drawing banishing pentagrams in each cardinal direction
3. Divine Name Invocation - YHVH, ADNI, AHIH, AGLA spoken with each pentagram
4. Archangelic Evocation - Calling upon Raphael (East), Michael (South), Gabriel (West), Uriel (North)
5. Closing Cross - Reaffirming the divine connection established in opening

The LBRP serves multiple functions: it clears the aura of unwanted influences, establishes proper magical polarity, connects the practitioner with divine forces, and prepares consciousness for higher magical work. Regular practice develops spiritual discrimination and strengthens the will.""",
        knowledge_type=KnowledgeType.PRACTICE,
        tags=["ritual", "banishing", "daily_practice", "pentagrams", "divine_names"],
        related_concepts=["middle_pillar", "tree_of_life", "archangels", "kabbalistic_cross"],
        source_url="https://hermetic.com/golden-dawn/",
        confidence_score=0.95,
        quality=ContentQuality.HIGH
    ),
    
    KnowledgeEntry(
        id="golden_dawn_system_002",
        tradition="golden_dawn",
        title="Tree of Life as Magical Map",
        summary="The Kabbalistic Tree of Life serves as the central organizing principle of Golden Dawn magic, providing correspondences for all magical operations and a map of consciousness development.",
        full_content="""The Tree of Life in Golden Dawn practice represents the complete structure of creation, consciousness, and magical correspondence. It serves as the foundational framework for all Golden Dawn magical operations.

Key Attributes:
- Structure: Ten Sefirot (divine emanations) connected by 22 paths
- Function: Map of consciousness, magical correspondence system, initiation guide
- Applications: Pathworking, ritual design, divination, meditation
- Correspondences: Each sefirah has specific planetary, elemental, and divine associations

The Ten Sefirot:
1. Kether (Crown) - Divine source, pure being
2. Chokmah (Wisdom) - Dynamic force, masculine principle
3. Binah (Understanding) - Form-giving, feminine principle
4. Chesed (Mercy) - Loving-kindness, expansion
5. Geburah (Severity) - Strength, restriction, judgment
6. Tiphereth (Beauty) - Harmony, consciousness, the Higher Self
7. Netzach (Victory) - Instinct, emotion, nature forces
8. Hod (Glory) - Intellect, communication, magical arts
9. Yesod (Foundation) - Astral plane, unconscious, lunar sphere
10. Malkuth (Kingdom) - Physical manifestation, material world

In Golden Dawn practice, the Tree provides the template for ritual design, assigns correspondences to tarot cards, and maps the initiate's spiritual development through the grades.""",
        knowledge_type=KnowledgeType.SYSTEM,
        tags=["tree_of_life", "sefirot", "correspondences", "kabbalah", "magical_map"],
        related_concepts=["pathworking", "initiation", "divine_names", "astral_projection"],
        source_url="https://www.golden-dawn.com/eu/displaycontent.aspx?pageid=145-tree-of-life",
        confidence_score=0.95,
        quality=ContentQuality.HIGH
    )
] 