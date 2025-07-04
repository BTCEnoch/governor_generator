#!/usr/bin/env python3
"""
Hermetic Tradition Knowledge Database
Comprehensive database of Hermetic principles, practices, and concepts
Based on curated sources from Sacred Texts, Hermetic Library, and Archive.org
"""

from typing import List, Dict

import os

from core.lighthouse.schemas.knowledge_schemas import KnowledgeEntry, KnowledgeType, ContentQuality, ProcessedTradition

# The Seven Hermetic Principles
HERMETIC_PRINCIPLES = [
    KnowledgeEntry(
        id="hermetic_principle_mentalism",
        tradition="hermetic_tradition",
        title="The Principle of Mentalism - All is Mind",
        summary="The first Hermetic principle states that 'The All is Mind; the Universe is Mental.' Reality is fundamentally mental in nature, created by universal consciousness.",
        full_content="""The Principle of Mentalism is the foundational teaching of Hermeticism, establishing that all of reality is mental in nature.

Core Teaching: "THE ALL IS MIND; The Universe is Mental."

Key Concepts:
1. Universal Mind: The source of all creation and manifestation
2. Mental Universe: All phenomena exist as thoughts in the Universal Mind
3. Individual Minds: Finite expressions of the infinite Universal Mind
4. Mental Creation: Thoughts and beliefs create reality at all levels
5. Consciousness Primary: Mind precedes and creates matter, not vice versa

Practical Applications:
- Mental transmutation through changing thought patterns
- Understanding that external conditions reflect internal states
- Working with visualization and mental imagery for manifestation
- Recognizing the power of belief and mental conditioning
- Developing higher states of consciousness

This principle forms the foundation for all other Hermetic teachings and magical practices. By understanding the mental nature of reality, the practitioner gains the ability to work with the fundamental forces of creation.""",
        knowledge_type=KnowledgeType.PRINCIPLE,
        tags=["mentalism", "mind", "consciousness", "reality", "foundation"],
        related_concepts=["universal_mind", "mental_transmutation", "consciousness"],
        source_url="https://sacred-texts.com/eso/kyb/",
        confidence_score=0.95,
        quality=ContentQuality.HIGH
    ),

    KnowledgeEntry(
        id="hermetic_principle_correspondence",
        tradition="hermetic_tradition",
        title="The Principle of Correspondence - As Above, So Below",
        summary="The second principle teaches the correspondence between different planes of existence: macrocosm and microcosm, higher and lower realms.",
        full_content="""The Principle of Correspondence reveals the harmony and relationship between the various planes of Being and Life.

Core Teaching: "As above, so below; as below, so above."

Key Concepts:
1. Macrocosm-Microcosm: The universe is reflected in each individual
2. Three Planes: Mental, Astral, and Physical planes of existence
3. Pattern Recognition: Similar patterns repeat at all levels of existence
4. Analogical Thinking: Understanding higher mysteries through lower manifestations
5. Universal Laws: Same laws operate on all planes, though with different expressions

The Three Planes:
- Mental Plane: Realm of pure thought and consciousness
- Astral Plane: Realm of emotions, desires, and psychic phenomena  
- Physical Plane: Realm of material manifestation and sensory experience

Practical Applications:
- Using earthly analogies to understand cosmic truths
- Working with symbols and correspondences in magic
- Understanding psychological states through physical symptoms
- Applying universal laws at personal and cosmic levels
- Recognizing patterns across different scales of existence

This principle is essential for magical practice, as it allows the practitioner to work on one plane to effect changes on another.""",
        knowledge_type=KnowledgeType.PRINCIPLE,
        tags=["correspondence", "as_above_so_below", "planes", "patterns", "analogies"],
        related_concepts=["three_planes", "macrocosm_microcosm", "universal_laws"],
        source_url="https://sacred-texts.com/eso/kyb/",
        confidence_score=0.95,
        quality=ContentQuality.HIGH
    ),

    KnowledgeEntry(
        id="hermetic_principle_vibration",
        tradition="hermetic_tradition",
        title="The Principle of Vibration - Nothing Rests",
        summary="The third principle states that everything is in constant motion and vibration. Matter, energy, mind, and spirit are all manifestations of vibration.",
        full_content="""The Principle of Vibration reveals that everything in the universe is in constant motion and vibrational activity.

Core Teaching: "Nothing rests; everything moves; everything vibrates."

Key Concepts:
1. Universal Motion: Everything from atoms to planets is in constant motion
2. Vibrational Rates: Different manifestations correspond to different vibrational frequencies
3. Scale of Vibration: From gross matter to pure spirit, all is vibration at different rates
4. Mental Vibrations: Thoughts and emotions have specific vibrational qualities
5. Vibrational Affinity: Like vibrations attract and resonate with each other

Vibrational Scale (from lowest to highest):
- Gross Matter: Dense, slow vibrations
- Subtle Matter: Finer, faster vibrations  
- Energy: Higher vibrational states
- Mental Phenomena: Thoughts, emotions, consciousness
- Spiritual Realms: Highest vibrational frequencies

Practical Applications:
- Raising personal vibration through spiritual practices
- Using sound, color, and symbols for vibrational alignment
- Understanding how thoughts and emotions affect reality
- Working with resonance and sympathetic vibration in magic
- Recognizing vibrational compatibility in relationships and environments

This principle explains how mental transmutation is possible - by changing one's mental vibration, one can influence all other levels of being.""",
        knowledge_type=KnowledgeType.PRINCIPLE,
        tags=["vibration", "motion", "frequency", "resonance", "transmutation"],
        related_concepts=["vibrational_scale", "mental_vibration", "resonance"],
        source_url="https://sacred-texts.com/eso/kyb/",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),

    KnowledgeEntry(
        id="hermetic_principle_polarity",
        tradition="hermetic_tradition",
        title="The Principle of Polarity - Everything is Dual",
        summary="The fourth principle reveals that everything has its pairs of opposites, which are actually identical in nature but different in degree.",
        full_content="""The Principle of Polarity demonstrates that apparent opposites are actually two extremes of the same thing.

Core Teaching: "Everything is Dual; everything has poles; everything has its pair of opposites."

Key Concepts:
1. Identical Opposites: Opposites are the same in nature, differing only in degree
2. Graduated Scale: All opposites exist on a continuous scale or spectrum
3. Mental Transmutation: Movement between poles is possible through will and understanding
4. Paradox Resolution: Apparent contradictions are reconciled through polarity
5. Dynamic Balance: True harmony comes from balancing opposing forces

Examples of Polarity:
- Hot and Cold (degrees of temperature)
- Light and Dark (degrees of illumination)
- Love and Hate (degrees of emotional feeling)
- Good and Evil (degrees of moral valuation)
- Spirit and Matter (degrees of manifestation)

Practical Applications:
- Transforming negative emotions into positive ones
- Finding the middle path between extremes
- Understanding that problems contain their own solutions
- Using opposing forces to create dynamic balance
- Transmuting undesirable mental states through conscious effort

This principle is fundamental to the art of Mental Alchemy, allowing the practitioner to transmute one mental state into another by understanding their polar relationship.""",
        knowledge_type=KnowledgeType.PRINCIPLE,
        tags=["polarity", "opposites", "duality", "transmutation", "balance"],
        related_concepts=["mental_alchemy", "transmutation", "dynamic_balance"],
        source_url="https://sacred-texts.com/eso/kyb/",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),

    # Complete the Seven Hermetic Principles
HERMETIC_PRINCIPLES_CONTINUED = [
    KnowledgeEntry(
        id="hermetic_principle_rhythm",
        tradition="hermetic_tradition",
        title="The Principle of Rhythm - Everything Flows",
        summary="The fifth principle reveals that everything has its tides, cycles, and rhythmic movement between opposing poles.",
        full_content="""The Principle of Rhythm demonstrates the cyclical nature of all phenomena and the pendulum-like swing between polar opposites.

Core Teaching: "Everything flows, out and in; everything has its tides; all things rise and fall."

Key Concepts:
1. Universal Rhythm: All phenomena exhibit cyclical patterns and rhythmic movement
2. Pendulum Swing: Movement between polar opposites follows predictable patterns
3. Compensation: The swing in one direction determines the swing in the other
4. Cycles Within Cycles: Multiple rhythmic patterns operate simultaneously
5. Natural Flow: Resistance to natural rhythms creates friction and imbalance

Examples of Rhythm:
- Seasons: Spring/Summer/Autumn/Winter cycles
- Life Cycles: Birth, growth, maturity, decline, death, rebirth
- Emotional States: Joy and sorrow, activity and rest
- Economic Cycles: Expansion and contraction, boom and bust
- Consciousness: Waking and sleeping, focused and relaxed states

Practical Applications:
- Working with natural cycles rather than against them
- Understanding that difficulties are temporary and cyclical
- Using knowledge of rhythms for timing magical operations
- Recognizing personal and collective cycles
- Maintaining balance during extremes by understanding their temporary nature

The wise practitioner learns to ride the rhythm rather than be dominated by it.""",
        knowledge_type=KnowledgeType.PRINCIPLE,
        tags=["rhythm", "cycles", "flow", "pendulum", "timing"],
        related_concepts=["natural_cycles", "timing", "balance"],
        source_url="https://sacred-texts.com/eso/kyb/",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),

    KnowledgeEntry(
        id="hermetic_principle_cause_effect",
        tradition="hermetic_tradition",
        title="The Principle of Cause and Effect - Every Cause has its Effect",
        summary="The sixth principle states that every cause has an effect and every effect has a cause. Nothing happens by pure chance - all is governed by law.",
        full_content="""The Principle of Cause and Effect reveals that there is no such thing as pure chance - everything happens according to universal law.

Core Teaching: "Every Cause has its Effect; every Effect has its Cause; everything happens according to Law."

Key Concepts:
1. Universal Causation: Nothing occurs without a preceding cause
2. Chain of Causation: Effects become causes for subsequent effects
3. Multiple Causation: Most phenomena result from multiple interacting causes
4. Mental Causation: Thoughts and intentions are powerful causes
5. Conscious Causation: Humans can become conscious causes rather than mere effects

Levels of Causation:
- Physical: Material causes and effects in the physical realm
- Mental: Thoughts, beliefs, and mental patterns as causes
- Spiritual: Higher spiritual principles operating as ultimate causes
- Karmic: Actions and their consequences across time and space
- Collective: Mass consciousness and social causation

Practical Applications:
- Taking responsibility for one's conditions and circumstances
- Understanding that present effects result from past causes
- Creating desired effects through conscious causation
- Breaking negative patterns by addressing their root causes
- Working with synchronicity and meaningful coincidence

The advanced practitioner becomes a conscious cause rather than an unconscious effect.""",
        knowledge_type=KnowledgeType.PRINCIPLE,
        tags=["cause_effect", "causation", "law", "responsibility", "synchronicity"],
        related_concepts=["karma", "responsibility", "conscious_causation"],
        source_url="https://sacred-texts.com/eso/kyb/",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),

    KnowledgeEntry(
        id="hermetic_principle_gender",
        tradition="hermetic_tradition",
        title="The Principle of Gender - Gender is in Everything",
        summary="The seventh principle reveals that masculine and feminine principles exist in everything and are necessary for creation and manifestation.",
        full_content="""The Principle of Gender demonstrates that masculine and feminine principles operate on all planes of existence and are essential for creation.

Core Teaching: "Gender is in everything; everything has its Masculine and Feminine Principles."

Key Concepts:
1. Universal Gender: Masculine and feminine principles exist at all levels
2. Creative Polarity: Both principles are necessary for generation and creation
3. Mental Gender: Masculine (objective) and feminine (subjective) aspects of mind
4. Dynamic Interaction: Creation occurs through the interaction of opposing gender principles
5. Balance and Harmony: Optimal function requires balance between both principles

The Two Principles:
Masculine Principle:
- Active, projective, initiating
- Logic, reason, analysis
- Will, determination, action
- Solar, electric, positive polarity

Feminine Principle:
- Receptive, nurturing, gestating  
- Intuition, feeling, synthesis
- Imagination, receptivity, wisdom
- Lunar, magnetic, negative polarity

Practical Applications:
- Balancing active and receptive aspects in magical work
- Understanding the interplay of will and imagination in manifestation
- Recognizing gender imbalances in personal development
- Working with both analytical and intuitive faculties
- Creating through the union of complementary opposites

True mastery involves the conscious integration and balance of both gender principles.""",
        knowledge_type=KnowledgeType.PRINCIPLE,
        tags=["gender", "masculine", "feminine", "polarity", "creation"],
        related_concepts=["creative_polarity", "balance", "manifestation"],
        source_url="https://sacred-texts.com/eso/kyb/",
        confidence_score=0.9,
        quality=ContentQuality.HIGH
    ),

    # Core Hermetic Concepts
HERMETIC_CONCEPTS = [
    KnowledgeEntry(
        id="hermetic_emerald_tablet",
        tradition="hermetic_tradition",
        title="The Emerald Tablet - Fundamental Alchemical Text",
        summary="The Emerald Tablet is the most famous Hermetic text, containing the fundamental principles of alchemy and transformation attributed to Hermes Trismegistus.",
        full_content="""The Emerald Tablet (Tabula Smaragdina) is the foundational text of Hermetic philosophy and alchemy, traditionally attributed to Hermes Trismegistus.

The Complete Text (traditional translation):
"True it is without falsehood, certain and most true. That which is above is like that which is below, and that which is below is like that which is above, to accomplish the miracles of the one thing. And as all things were by contemplation of one, so all things arose from this one thing by a single act of adaptation. The Sun is its father, the Moon its mother, the Wind carried it in its womb, the Earth is its nurse. Here is the father of all perfection, or consummation of the whole world. Its power is integrating, if it be turned into earth. Separate the earth from fire, the subtle from the gross, gently and with great industry. It ascends from earth to heaven and descends again to earth, and receives the power of the superiors and of the inferiors. So thou hast the glory of the whole world; therefore let all obscurity flee before thee. This is the strong fortitude of all fortitude, for it will overcome every subtle thing and penetrate every solid thing. So the world was created. Hence there will be marvelous adaptations achieved, of which the manner is this. For this reason I am called Hermes Trismegistus, because I hold three parts of the wisdom of the whole world. That which I had to say about the operation of the Sun is completed."

Key Teachings:
1. Correspondence: "As above, so below" - the fundamental hermetic axiom
2. Unity: All things arise from one source through divine contemplation
3. Transformation: The process of spiritual and material transmutation
4. Elements: The interplay of the four elements in creation
5. The Great Work: The ultimate goal of alchemical transformation

The Emerald Tablet serves as both a practical guide for alchemical operations and a spiritual blueprint for inner transformation.""",
        knowledge_type=KnowledgeType.CONCEPT,
        tags=["emerald_tablet", "alchemy", "transformation", "hermes_trismegistus", "fundamental"],
        related_concepts=["alchemy", "great_work", "transformation"],
        source_url="https://sacred-texts.com/alc/emerald.htm",
        confidence_score=0.95,
        quality=ContentQuality.HIGH
    ),

    # Combine all Hermetic principles
ALL_HERMETIC_PRINCIPLES = HERMETIC_PRINCIPLES + HERMETIC_PRINCIPLES_CONTINUED

# Combine all Hermetic concepts
ALL_HERMETIC_CONCEPTS = HERMETIC_CONCEPTS

# Complete Hermetic Tradition Database
def create_hermetic_tradition() -> ProcessedTradition:
    """Create the complete Hermetic tradition database"""
    
return [    all_entries = ALL_HERMETIC_PRINCIPLES + ALL_HERMETIC_CONCEPTS
    
    # Categorize entries
    principles = [e for e in all_entries if e.knowledge_type == KnowledgeType.PRINCIPLE]
    practices = [e for e in all_entries if e.knowledge_type == KnowledgeType.PRACTICE]
    systems = [e for e in all_entries if e.knowledge_type == KnowledgeType.SYSTEM]
    concepts = [e for e in all_entries if e.knowledge_type == KnowledgeType.CONCEPT]
    
    # Create cross-references
    cross_references = {
        "seven_principles": [
            "hermetic_principle_mentalism", "hermetic_principle_correspondence", 
            "hermetic_principle_vibration", "hermetic_principle_polarity",
            "hermetic_principle_rhythm", "hermetic_principle_cause_effect",
            "hermetic_principle_gender"
        ],
        "foundational_texts": ["hermetic_emerald_tablet"],
        "core_concepts": ["mental_transmutation", "as_above_so_below", "universal_laws"],
        "practical_applications": ["alchemy", "manifestation", "spiritual_development"]
    }
    
    return ProcessedTradition(
        name="hermetic_tradition",
        description="The complete Hermetic tradition including the Seven Hermetic Principles, the Emerald Tablet, and core alchemical and philosophical concepts.",
        total_entries=len(all_entries),
        principles=principles,
        practices=practices,
        systems=systems,
        concepts=concepts,
        cross_references=cross_references

# Helper functions
def get_hermetic_entry_by_id(entry_id: str) -> KnowledgeEntry:
    """Get specific Hermetic knowledge entry by ID"""
return [    all_entries = ALL_HERMETIC_PRINCIPLES + ALL_HERMETIC_CONCEPTS
    for entry in all_entries:
        if entry.id == entry_id:
            return entry
    raise ValueError(f"Hermetic entry not found: {entry_id}")

def search_hermetic_by_tag(tag: str) -> List[KnowledgeEntry]:
    """Search Hermetic entries by tag"""

return [    all_entries = ALL_HERMETIC_PRINCIPLES + ALL_HERMETIC_CONCEPTS
    return [entry for entry in all_entries if tag in entry.tags]

def get_all_hermetic_entries() -> List[KnowledgeEntry]:
    """Get all Hermetic knowledge entries"""

return [    return ALL_HERMETIC_PRINCIPLES + ALL_HERMETIC_CONCEPTS

def get_seven_principles() -> List[KnowledgeEntry]:
    """Get the seven Hermetic principles in order"""

return [    return ALL_HERMETIC_PRINCIPLES 
