#!/usr/bin/env python3
"""
Kabbalah Knowledge Database
Comprehensive database of Kabbalistic concepts, Tree of Life, and mystical practices
Based on curated sources from Sacred Texts, Sefaria, and Wikipedia
"""

from typing import List, Dict

import os

from core.lighthouse.schemas.knowledge_schemas import KnowledgeEntry, KnowledgeType, ContentQuality, ProcessedTradition

# Tree of Life Sefirot (First 5)
TREE_OF_LIFE_SEFIROT = [
    KnowledgeEntry(
        id="kabbalah_sefirah_keter",
        tradition="kabbalah",
        title="Keter - The Crown: Divine Will",
        summary="Keter is the highest Sefirah on the Tree of Life, representing the divine crown and the first emanation of the infinite Ein Sof.",
        full_content="""Keter (Hebrew: כֶּתֶר, "Crown") is the first and highest Sefirah on the Tree of Life, representing the divine will and the first emanation from the infinite Ein Sof.

Key Attributes:
- Position: 1st Sefirah (Crown)
- Divine Name: Ehyeh (אהיה - "I Am")
- Archangel: Metatron
- Heavenly Body: Primum Mobile (First Swirlings)
- Element: Pure Spirit
- Color: Brilliant White/Clear Light

Spiritual Meaning:
Keter represents the divine will and the first impulse of creation. It is the bridge between the infinite Ein Sof and the manifest creation. In Keter, there is no duality or separation - only pure divine consciousness in its most primordial state.

Functions:
1. Divine Will: The primal intention behind all creation
2. Pure Consciousness: Undifferentiated awareness before manifestation
3. Unity: The state before polarity and differentiation
4. Source: The fountainhead from which all other Sefirot flow
5. Crown: The divine crown that rules over all creation

Keter is often considered too sublime for direct human comprehension, representing the interface between the unknowable Ein Sof and the knowable Tree of Life.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["keter", "crown", "divine_will", "ein_sof", "first_emanation"],
        related_concepts=["tree_of_life", "ein_sof", "sefirot"],
        source_url="https://en.wikipedia.org/wiki/Keter",
        confidence_score=0.95,
        quality=ContentQuality.HIGH
    ),

    KnowledgeEntry(
        id="kabbalah_sefirah_chokhmah",
        tradition="kabbalah",
        title="Chokhmah - Wisdom: Divine Masculine Principle",
        summary="Chokhmah is the second Sefirah, representing divine wisdom and the masculine principle of active, penetrating consciousness.",
        full_content="""Chokhmah (Hebrew: חכמה, "Wisdom") is the second Sefirah on the Tree of Life, representing divine wisdom and the masculine principle of creation.

Key Attributes:
- Position: 2nd Sefirah (Upper Right)
- Divine Name: Yah (יה)
- Archangel: Raziel
- Heavenly Body: Zodiac/Uranus
- Element: Fire
- Color: Grey/Blue

Spiritual Meaning:
Chokhmah represents the first active principle after Keter's pure potential. It is the divine flash of inspiration, the penetrating force of consciousness that initiates creation. Chokhmah is pure wisdom - not learned knowledge, but direct, intuitive understanding.

Functions:
1. Divine Wisdom: Direct, non-rational knowing
2. Masculine Principle: Active, penetrating, initiating force
3. Inspiration: The lightning flash of creative insight
4. Beginning: The first movement from potential to actual
5. Father: The archetypal masculine, generative principle

Chokhmah works in dynamic relationship with Binah (Understanding) to create the fundamental polarity that drives all manifestation. It represents the point of pure creative energy before it takes form.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["chokhmah", "wisdom", "masculine", "inspiration", "creative_force"],
        related_concepts=["binah", "masculine_feminine", "creative_polarity"],
        source_url="https://en.wikipedia.org/wiki/Chokhmah",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),

    KnowledgeEntry(
        id="kabbalah_sefirah_binah",
        tradition="kabbalah",
        title="Binah - Understanding: Divine Feminine Principle",
        summary="Binah is the third Sefirah, representing divine understanding and the feminine principle of receptive, form-giving consciousness.",
        full_content="""Binah (Hebrew: בינה, "Understanding") is the third Sefirah on the Tree of Life, representing divine understanding and the feminine principle of creation.

Key Attributes:
- Position: 3rd Sefirah (Upper Left)
- Divine Name: Elohim (אלהים)
- Archangel: Tzaphkiel
- Heavenly Body: Saturn
- Element: Water
- Color: Black/Deep Blue

Spiritual Meaning:
Binah represents the divine feminine principle that receives the creative impulse from Chokhmah and gives it form and structure. It is the great womb of creation, the understanding that shapes raw creative energy into manifestible forms.

Functions:
1. Divine Understanding: The ability to give form to wisdom
2. Feminine Principle: Receptive, nurturing, form-giving force
3. The Great Mother: The archetypal feminine, creative matrix
4. Form-Giver: Shapes abstract concepts into concrete possibilities
5. Restriction: The loving limitation that enables manifestation

Binah is called the "Great Sea" because it contains all possibilities in potential form. It represents the understanding that organizes and structures the creative impulse from Chokhmah, making manifestation possible.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["binah", "understanding", "feminine", "form_giving", "great_mother"],
        related_concepts=["chokhmah", "feminine_principle", "creative_matrix"],
        source_url="https://en.wikipedia.org/wiki/Binah_(Kabbalah)",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),

    # Continue Tree of Life Sefirot (4-7)
TREE_OF_LIFE_SEFIROT_CONTINUED = [
    KnowledgeEntry(
        id="kabbalah_sefirah_chesed",
        tradition="kabbalah",
        title="Chesed - Mercy: Divine Love and Expansion",
        summary="Chesed is the fourth Sefirah, representing divine mercy, love, and the expansive force of creation. It embodies unconditional giving and grace.",
        full_content="""Chesed (Hebrew: חֶסֶד, "Mercy" or "Loving-kindness") is the fourth Sefirah on the Tree of Life, representing divine mercy and the expansive force of love.

Key Attributes:
- Position: 4th Sefirah (Right Pillar)
- Divine Name: El (אל)
- Archangel: Tzadkiel
- Heavenly Body: Jupiter
- Element: Water
- Color: Blue

Spiritual Meaning:
Chesed represents divine love in its most expansive form - unlimited mercy, grace, and loving-kindness. It is the force that seeks to give without restriction, to expand without boundaries, and to love without conditions.

Functions:
1. Divine Mercy: Unlimited compassion and forgiveness
2. Expansive Love: The force that seeks to include and embrace all
3. Grace: Unearned divine blessing and favor
4. Generosity: The impulse to give freely and abundantly
5. Vision: The ability to see the divine in all creation

Chesed must be balanced by Gevurah (Severity) to prevent spiritual inflation and maintain cosmic order. Together, they create the fundamental dynamic tension necessary for balanced manifestation.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["chesed", "mercy", "love", "expansion", "grace"],
        related_concepts=["gevurah", "divine_love", "balance"],
        source_url="https://en.wikipedia.org/wiki/Chesed",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),

    KnowledgeEntry(
        id="kabbalah_sefirah_gevurah",
        tradition="kabbalah",
        title="Gevurah - Severity: Divine Judgment and Restriction",
        summary="Gevurah is the fifth Sefirah, representing divine judgment, strength, and the restrictive force that provides structure and boundaries.",
        full_content="""Gevurah (Hebrew: גְּבוּרָה, "Severity" or "Strength") is the fifth Sefirah on the Tree of Life, representing divine judgment and the restrictive force that provides necessary boundaries.

Key Attributes:
- Position: 5th Sefirah (Left Pillar)
- Divine Name: Elohim Gibor (אלהים גבור)
- Archangel: Kamael (Chamuel)
- Heavenly Body: Mars
- Element: Fire
- Color: Red

Spiritual Meaning:
Gevurah represents divine judgment and the necessary force of restriction that prevents chaos and maintains cosmic order. It is not harsh judgment, but loving limitation that enables proper growth and development.

Functions:
1. Divine Judgment: Discernment between appropriate and inappropriate
2. Strength: The power to maintain boundaries and resist corruption
3. Restriction: Loving limitations that enable proper development
4. Purification: The removal of impurities through testing and trial
5. Protection: Maintaining cosmic and moral order

Gevurah works in dynamic balance with Chesed to create the fundamental polarity of expansion and contraction, mercy and judgment, that drives all manifestation and evolution.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["gevurah", "severity", "judgment", "restriction", "strength"],
        related_concepts=["chesed", "divine_judgment", "cosmic_order"],
        source_url="https://en.wikipedia.org/wiki/Gevurah",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),

    KnowledgeEntry(
        id="kabbalah_sefirah_tiferet",
        tradition="kabbalah",
        title="Tiferet - Beauty: Divine Harmony and Balance",
        summary="Tiferet is the sixth Sefirah, representing divine beauty and the harmonious balance between mercy and severity, often called the heart of the Tree of Life.",
        full_content="""Tiferet (Hebrew: תִּפְאֶרֶת, "Beauty" or "Glory") is the sixth Sefirah on the Tree of Life, representing divine beauty and the harmonious balance between all opposing forces.

Key Attributes:
- Position: 6th Sefirah (Central Pillar)
- Divine Name: YHVH (יהוה)
- Archangel: Michael
- Heavenly Body: Sun
- Element: Air
- Color: Yellow/Gold

Spiritual Meaning:
Tiferet represents the heart of the Tree of Life, the center where all forces achieve perfect balance and harmony. It is divine beauty - not merely aesthetic beauty, but the beauty of perfect proportion and harmony.

Functions:
1. Divine Beauty: The harmony that emerges from balanced opposites
2. Central Balance: The mediating force between all polarities
3. Heart Center: The emotional and spiritual center of the Tree
4. Solar Consciousness: Illuminated awareness and self-consciousness
5. Sacrifice: The willingness to give of oneself for higher purpose

Tiferet is often associated with the heart chakra and represents the development of genuine compassion and balanced love. It harmonizes the expansive mercy of Chesed with the restrictive judgment of Gevurah.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["tiferet", "beauty", "balance", "harmony", "heart_center"],
        related_concepts=["balance", "solar_consciousness", "compassion"],
        source_url="https://en.wikipedia.org/wiki/Tiferet",
        confidence_score=0.95,
        quality=ContentQuality.HIGH
    ),

    KnowledgeEntry(
        id="kabbalah_sefirah_netzach",
        tradition="kabbalah",
        title="Netzach - Victory: Divine Endurance and Persistence",
        summary="Netzach is the seventh Sefirah, representing divine victory, endurance, and the persistent force that overcomes all obstacles through faith and determination.",
        full_content="""Netzach (Hebrew: נֶצַח, "Victory" or "Endurance") is the seventh Sefirah on the Tree of Life, representing divine victory and the persistent force that achieves triumph through endurance.

Key Attributes:
- Position: 7th Sefirah (Right Pillar)
- Divine Name: YHVH Tzabaoth (יהוה צבאות)
- Archangel: Haniel
- Heavenly Body: Venus
- Element: Fire
- Color: Green

Spiritual Meaning:
Netzach represents the divine quality of persistence and endurance that overcomes all obstacles. It is the force of faith, hope, and determination that continues forward despite all challenges and setbacks.

Functions:
1. Divine Victory: The ultimate triumph of light over darkness
2. Endurance: The ability to persist through all difficulties
3. Faith: Unwavering trust in divine purpose and plan
4. Artistic Inspiration: The creative force that seeks expression
5. Group Consciousness: The formation of collective identity and purpose

Netzach works in polarity with Hod (Splendor) to create the dynamic between intuitive inspiration and rational analysis, between the poetic and the practical aspects of manifestation.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["netzach", "victory", "endurance", "persistence", "faith"],
        related_concepts=["hod", "persistence", "divine_victory"],
        source_url="https://en.wikipedia.org/wiki/Netzach",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),

    # Final Tree of Life Sefirot (8-10)
TREE_OF_LIFE_SEFIROT_FINAL = [
    KnowledgeEntry(
        id="kabbalah_sefirah_hod",
        tradition="kabbalah",
        title="Hod - Splendor: Divine Intellect and Communication",
        summary="Hod is the eighth Sefirah, representing divine splendor, intellectual analysis, and the power of communication and rational thought.",
        full_content="""Hod (Hebrew: הוד, "Splendor" or "Glory") is the eighth Sefirah on the Tree of Life, representing divine intellect and the power of analytical thought and communication.

Key Attributes:
- Position: 8th Sefirah (Left Pillar)
- Divine Name: Elohim Tzabaoth (אלהים צבאות)
- Archangel: Michael
- Heavenly Body: Mercury
- Element: Water
- Color: Orange

Spiritual Meaning:
Hod represents the divine intellect and the power of analytical thought, logic, and communication. It is the sphere of rational mind, scientific thinking, and the ability to articulate and transmit knowledge.

Functions:
1. Divine Intellect: The power of analytical and rational thought
2. Communication: The ability to articulate and transmit ideas
3. Learning: The acquisition and organization of knowledge
4. Magic and Science: The practical application of knowledge
5. Mental Flexibility: The ability to adapt thought to circumstances

Hod works in dynamic polarity with Netzach to balance rational analysis with intuitive inspiration, practical application with artistic vision, and mental precision with emotional depth.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["hod", "splendor", "intellect", "communication", "analysis"],
        related_concepts=["netzach", "rational_mind", "communication"],
        source_url="https://en.wikipedia.org/wiki/Hod_(Kabbalah)",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),

    KnowledgeEntry(
        id="kabbalah_sefirah_yesod",
        tradition="kabbalah",
        title="Yesod - Foundation: The Astral Realm and Subconscious",
        summary="Yesod is the ninth Sefirah, representing the foundation of the material world and the astral realm where all influences gather before manifestation.",
        full_content="""Yesod (Hebrew: יְסוֹד, "Foundation") is the ninth Sefirah on the Tree of Life, representing the foundation of material existence and the astral realm that bridges the spiritual and physical worlds.

Key Attributes:
- Position: 9th Sefirah (Central Pillar)
- Divine Name: Shaddai El Chai (שדי אל חי)
- Archangel: Gabriel
- Heavenly Body: Moon
- Element: Air
- Color: Purple/Violet

Spiritual Meaning:
Yesod represents the astral realm and the collective unconscious where all influences from the higher Sefirot gather and organize before manifesting in the physical world. It is the realm of dreams, imagination, and psychic phenomena.

Functions:
1. Astral Foundation: The bridge between spiritual and physical realms
2. Collective Unconscious: The shared psychic substrate of humanity
3. Dreams and Visions: The realm of symbolic and prophetic imagery
4. Sexual Energy: The fundamental creative/generative force
5. Purification: The final refining process before manifestation

Yesod is often called the "Treasure House of Images" because it contains all the archetypal forms and patterns that become manifest in Malkhut. It is governed by lunar consciousness and the rhythms of the unconscious mind.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["yesod", "foundation", "astral", "subconscious", "dreams"],
        related_concepts=["astral_realm", "collective_unconscious", "archetypal_forms"],
        source_url="https://en.wikipedia.org/wiki/Yesod",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),

    KnowledgeEntry(
        id="kabbalah_sefirah_malkhut",
        tradition="kabbalah",
        title="Malkhut - Kingdom: The Material World and Divine Presence",
        summary="Malkhut is the tenth and final Sefirah, representing the physical world and the divine presence that manifests in material creation.",
        full_content="""Malkhut (Hebrew: מַלְכוּת, "Kingdom") is the tenth and final Sefirah on the Tree of Life, representing the physical world and the culmination of the divine creative process in material manifestation.

Key Attributes:
- Position: 10th Sefirah (Central Pillar, Base)
- Divine Name: Adonai (אדני)
- Archangel: Sandalphon
- Heavenly Body: Earth
- Element: Earth
- Color: Olive, Russet, Citrine, Black

Spiritual Meaning:
Malkhut represents the physical world and the divine presence (Shekinah) that dwells within material creation. It is the final destination of the divine emanations and the starting point for their return journey up the Tree.

Functions:
1. Physical Manifestation: The material world and sensory experience
2. Divine Presence: The Shekinah dwelling within creation
3. Completion: The fulfillment of the divine creative process
4. Return Path: The beginning of the journey back to unity
5. Service: The opportunity to serve the divine through material existence

Malkhut contains sparks of all the higher Sefirot within it, making the physical world a reflection of all divine qualities. It is both the lowest point of divine emanation and the foundation for the return to divine unity.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["malkhut", "kingdom", "material_world", "shekinah", "manifestation"],
        related_concepts=["physical_world", "divine_presence", "manifestation"],
        source_url="https://en.wikipedia.org/wiki/Malkuth",
        confidence_score=0.95,
        quality=ContentQuality.HIGH
    ),

    # Combine all Tree of Life Sefirot
ALL_TREE_OF_LIFE_SEFIROT = TREE_OF_LIFE_SEFIROT + TREE_OF_LIFE_SEFIROT_CONTINUED + TREE_OF_LIFE_SEFIROT_FINAL

# Core Kabbalistic Concepts
KABBALAH_CONCEPTS = [
    KnowledgeEntry(
        id="kabbalah_ein_sof",
        tradition="kabbalah",
        title="Ein Sof - The Infinite: The Unknowable Divine Source",
        summary="Ein Sof represents the infinite, unknowable aspect of the divine that exists beyond all manifestation and conceptualization.",
        full_content="""Ein Sof (Hebrew: אין סוף, "Without End" or "Infinite") represents the infinite, unknowable aspect of the divine that exists beyond all manifestation, form, and conceptualization.

Key Attributes:
- Nature: Infinite, unlimited, beyond comprehension
- Relationship to Creation: The hidden source from which all emanates
- Knowability: Unknowable through direct experience or conceptualization
- Manifestation: Reveals itself only through the Sefirot

Spiritual Meaning:
Ein Sof is the absolute divine reality that transcends all qualities, attributes, and limitations. It is not a being or entity, but pure infinite existence beyond all categories of thought or experience.

Characteristics:
1. Infinite: Without beginning, end, or limitation
2. Unknowable: Beyond human comprehension or experience
3. Source: The hidden origin of all emanation and creation
4. Unity: Undifferentiated oneness before all manifestation
5. Transcendent: Beyond all worlds, forms, and qualities

The relationship between Ein Sof and the Sefirot is one of the central mysteries of Kabbalah - how the infinite becomes finite while remaining infinite.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["ein_sof", "infinite", "unknowable", "divine_source", "transcendent"],
        related_concepts=["sefirot", "divine_transcendence", "infinite_mystery"],
        source_url="https://en.wikipedia.org/wiki/Ein_Sof",
        confidence_score=0.95,
        quality=ContentQuality.HIGH
    ),

    KnowledgeEntry(
        id="kabbalah_gematria",
        tradition="kabbalah",
        title="Gematria - Sacred Numerology and Letter Values",
        summary="Gematria is the Kabbalistic practice of calculating the numerical values of Hebrew letters and words to discover hidden meanings and connections.",
        full_content="""Gematria (Hebrew: גִּימַטְרִיָּא) is the Kabbalistic practice of calculating the numerical values of Hebrew letters and words to discover hidden spiritual meanings and divine connections.

Basic Principles:
- Each Hebrew letter has a numerical value
- Words with equal numerical values share mystical connections
- Sacred texts contain hidden layers of meaning accessible through numerical analysis
- Divine names and concepts reveal deeper truths through gematria

Hebrew Letter Values (examples):
- Aleph (א) = 1
- Bet (ב) = 2
- Gimel (ג) = 3
- Daleth (ד) = 4
- Hey (ה) = 5

Applications:
1. Biblical Interpretation: Finding hidden meanings in sacred texts
2. Name Analysis: Understanding spiritual qualities through numerical values
3. Mystical Connections: Discovering relationships between concepts
4. Prophetic Insight: Revealing future events through numerical patterns
5. Meditation Practice: Using numbers for contemplative focus

Gematria reveals the underlying mathematical harmony of creation and the divine blueprint encoded within the Hebrew language and sacred texts.""",
        knowledge_type=KnowledgeType.PRACTICE,
        tags=["gematria", "numerology", "hebrew_letters", "hidden_meanings", "numerical_values"],
        related_concepts=["hebrew_alphabet", "sacred_mathematics", "biblical_interpretation"],
        source_url="https://en.wikipedia.org/wiki/Gematria",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),

    # Complete Kabbalah Tradition Database
def create_kabbalah_tradition() -> ProcessedTradition:
    """Create the complete Kabbalah tradition database"""
    
return [    all_entries = ALL_TREE_OF_LIFE_SEFIROT + KABBALAH_CONCEPTS
    
    # Categorize entries
    principles = [e for e in all_entries if e.knowledge_type == KnowledgeType.PRINCIPLE]
    practices = [e for e in all_entries if e.knowledge_type == KnowledgeType.PRACTICE]
    systems = [e for e in all_entries if e.knowledge_type == KnowledgeType.SYSTEM]
    concepts = [e for e in all_entries if e.knowledge_type == KnowledgeType.CONCEPT]
    
    # Create cross-references
    cross_references = {
        "tree_of_life": [
            "kabbalah_sefirah_keter", "kabbalah_sefirah_chokhmah", "kabbalah_sefirah_binah",
            "kabbalah_sefirah_chesed", "kabbalah_sefirah_gevurah", "kabbalah_sefirah_tiferet",
            "kabbalah_sefirah_netzach", "kabbalah_sefirah_hod", "kabbalah_sefirah_yesod", 
            "kabbalah_sefirah_malkhut"
        ],
        "divine_emanation": ["kabbalah_ein_sof", "kabbalah_sefirah_keter"],
        "practical_kabbalah": ["kabbalah_gematria"],
        "sacred_geometry": ["tree_of_life", "sefirot_relationships"],
        "mystical_practices": ["gematria", "meditation", "contemplation"]
    }
    
    return ProcessedTradition(
        name="kabbalah",
        description="The complete Kabbalistic tradition including the Tree of Life, Ten Sefirot, Ein Sof, Gematria, and core mystical concepts.",
        total_entries=len(all_entries),
        principles=principles,
        practices=practices,
        systems=systems,
        concepts=concepts,
        cross_references=cross_references

# Helper functions
def get_kabbalah_entry_by_id(entry_id: str) -> KnowledgeEntry:
    """Get specific Kabbalah knowledge entry by ID"""
return [    all_entries = ALL_TREE_OF_LIFE_SEFIROT + KABBALAH_CONCEPTS
    for entry in all_entries:
        if entry.id == entry_id:
            return entry
    raise ValueError(f"Kabbalah entry not found: {entry_id}")

def search_kabbalah_by_tag(tag: str) -> List[KnowledgeEntry]:
    """Search Kabbalah entries by tag"""

return [    all_entries = ALL_TREE_OF_LIFE_SEFIROT + KABBALAH_CONCEPTS
    return [entry for entry in all_entries if tag in entry.tags]

def get_all_kabbalah_entries() -> List[KnowledgeEntry]:
    """Get all Kabbalah knowledge entries"""

return [    return ALL_TREE_OF_LIFE_SEFIROT + KABBALAH_CONCEPTS

def get_ten_sefirot() -> List[KnowledgeEntry]:
    """Get the ten Sefirot in order"""

return [    return ALL_TREE_OF_LIFE_SEFIROT 
