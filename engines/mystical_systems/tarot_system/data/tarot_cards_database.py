# tarot_system/data/tarot_cards_database.py
from engines.mystical_systems.tarot_system.schemas.tarot_schemas import TarotCard, TarotSuit

# Major Arcana (22 cards)
MAJOR_ARCANA = [
    TarotCard(
        id="fool",
        name="The Fool",
        suit=TarotSuit.MAJOR_ARCANA,
        number=0,
        wikipedia_url="https://en.wikipedia.org/wiki/The_Fool_(Tarot_card)",
        upright_keywords=["new beginnings", "innocence", "spontaneity", "free spirit"],
        reversed_keywords=["recklessness", "carelessness", "risk-taking", "foolishness"],
        upright_meaning="The Fool represents new beginnings, having faith in the future, being inexperienced, not knowing what to expect, having beginner's luck, improvisation and believing in the universe.",
        reversed_meaning="The Fool reversed represents recklessness, carelessness, distraction, poor judgment, lack of fun and routine.",
        element="Air",
        planet="Uranus", 
        hebrew_letter="Aleph",
        tree_of_life_path=11,
        influence_categories={
            "innovation": 0.9,
            "risk_taking": 0.8, 
            "spirituality": 0.7,
            "leadership": 0.3
        }
    ),
    TarotCard(
        id="magician",
        name="The Magician", 
        suit=TarotSuit.MAJOR_ARCANA,
        number=1,
        wikipedia_url="https://en.wikipedia.org/wiki/The_Magician_(Tarot_card)",
        upright_keywords=["manifestation", "resourcefulness", "power", "inspired action"],
        reversed_keywords=["manipulation", "poor planning", "untapped talents", "greed"],
        upright_meaning="The Magician represents manifestation, resourcefulness, power, inspired action and having the tools and resources to achieve your goals.",
        reversed_meaning="The Magician reversed represents manipulation, poor planning, latent talents and greed.",
        element="Air",
        planet="Mercury",
        hebrew_letter="Beth", 
        tree_of_life_path=12,
        influence_categories={
            "manifestation": 0.95,
            "leadership": 0.85,
            "knowledge": 0.9,
            "communication": 0.8
        }
    ),
    TarotCard(
        id="high_priestess",
        name="The High Priestess",
        suit=TarotSuit.MAJOR_ARCANA,
        number=2,
        wikipedia_url="https://en.wikipedia.org/wiki/The_High_Priestess",
        upright_keywords=["intuition", "sacred knowledge", "divine feminine", "subconscious mind"],
        reversed_keywords=["secrets", "disconnected from intuition", "withdrawal", "silence"],
        upright_meaning="The High Priestess represents intuition, sacred knowledge, divine feminine and the subconscious mind.",
        reversed_meaning="The High Priestess reversed represents secrets, disconnected from intuition, withdrawal and silence.",
        element="Water",
        planet="Moon",
        hebrew_letter="Gimel",
        tree_of_life_path=13,
        influence_categories={
            "intuition": 0.95,
            "spirituality": 0.9,
            "wisdom": 0.85,
            "mystery": 0.8
        }
    ),
    TarotCard(
        id="empress",
        name="The Empress",
        suit=TarotSuit.MAJOR_ARCANA,
        number=3,
        wikipedia_url="https://en.wikipedia.org/wiki/The_Empress_(Tarot_card)",
        upright_keywords=["femininity", "beauty", "nature", "nurturing", "abundance"],
        reversed_keywords=["creative block", "dependence on others", "smothering", "lack of growth"],
        upright_meaning="The Empress represents femininity, beauty, nature, nurturing and abundance.",
        reversed_meaning="The Empress reversed represents creative block, dependence on others, smothering and lack of growth.",
        element="Earth",
        planet="Venus",
        hebrew_letter="Daleth",
        tree_of_life_path=14,
        influence_categories={
            "creativity": 0.9,
            "nurturing": 0.95,
            "abundance": 0.85,
            "nature": 0.8
        }
    ),
    TarotCard(
        id="emperor",
        name="The Emperor",
        suit=TarotSuit.MAJOR_ARCANA,
        number=4,
        wikipedia_url="https://en.wikipedia.org/wiki/The_Emperor_(Tarot_card)",
        upright_keywords=["authority", "establishment", "structure", "father figure"],
        reversed_keywords=["tyranny", "rigidity", "coldness", "domination"],
        upright_meaning="The Emperor represents authority, establishment, structure and being a father figure.",
        reversed_meaning="The Emperor reversed represents tyranny, rigidity, coldness and domination.",
        element="Fire",
        planet="Aries",
        hebrew_letter="Heh",
        tree_of_life_path=15,
        influence_categories={
            "leadership": 0.95,
            "authority": 0.9,
            "structure": 0.85,
            "discipline": 0.8
        }
    )
    # Adding 5 major arcana cards for now - can expand later
]

# Minor Arcana - Wands (Fire)
WANDS_SUIT = [
    TarotCard(
        id="ace_of_wands",
        name="Ace of Wands",
        suit=TarotSuit.WANDS,
        number=1,
        wikipedia_url="https://en.wikipedia.org/wiki/Ace_of_Wands",
        upright_keywords=["inspiration", "new opportunities", "growth", "potential"],
        reversed_keywords=["lack of energy", "delays", "setbacks", "lack of direction"],
        upright_meaning="The Ace of Wands represents inspiration, new opportunities, growth and potential in creative or career endeavors.",
        reversed_meaning="The Ace of Wands reversed represents lack of energy, delays, setbacks and lack of direction.",
        element="Fire",
        influence_categories={
            "creativity": 0.9,
            "initiative": 0.85,
            "passion": 0.8,
            "leadership": 0.7
        }
    ),
    TarotCard(
        id="two_of_wands",
        name="Two of Wands",
        suit=TarotSuit.WANDS,
        number=2,
        wikipedia_url="https://en.wikipedia.org/wiki/Two_of_Wands",
        upright_keywords=["planning", "making decisions", "leaving comfort zone", "taking control"],
        reversed_keywords=["lack of planning", "disorganized", "playing it safe", "bad timing"],
        upright_meaning="The Two of Wands represents planning, making decisions, leaving comfort zone and taking control.",
        reversed_meaning="The Two of Wands reversed represents lack of planning, disorganized, playing it safe and bad timing.",
        element="Fire",
        influence_categories={
            "planning": 0.8,
            "decision_making": 0.85,
            "control": 0.7,
            "vision": 0.75
        }
    )
]

# Minor Arcana - Cups (Water) 
CUPS_SUIT = [
    TarotCard(
        id="ace_of_cups",
        name="Ace of Cups",
        suit=TarotSuit.CUPS,
        number=1,
        wikipedia_url="https://en.wikipedia.org/wiki/Ace_of_Cups",
        upright_keywords=["love", "new relationships", "compassion", "creativity"],
        reversed_keywords=["self-love", "intuition", "repressed emotions", "emptiness"],
        upright_meaning="The Ace of Cups represents love, new relationships, compassion and creativity.",
        reversed_meaning="The Ace of Cups reversed represents self-love, intuition, repressed emotions and emptiness.",
        element="Water",
        influence_categories={
            "emotion": 0.9,
            "love": 0.95,
            "compassion": 0.85,
            "creativity": 0.8
        }
    ),
    TarotCard(
        id="two_of_cups",
        name="Two of Cups",
        suit=TarotSuit.CUPS,
        number=2,
        wikipedia_url="https://en.wikipedia.org/wiki/Two_of_Cups",
        upright_keywords=["unified love", "partnership", "mutual attraction", "relationships"],
        reversed_keywords=["self-love", "break-ups", "disharmony", "trust issues"],
        upright_meaning="The Two of Cups represents unified love, partnership, mutual attraction and relationships.",
        reversed_meaning="The Two of Cups reversed represents self-love, break-ups, disharmony and trust issues.",
        element="Water",
        influence_categories={
            "partnership": 0.9,
            "harmony": 0.85,
            "attraction": 0.8,
            "cooperation": 0.75
        }
    )
]

# Minor Arcana - Swords (Air)
SWORDS_SUIT = [
    TarotCard(
        id="ace_of_swords",
        name="Ace of Swords",
        suit=TarotSuit.SWORDS,
        number=1,
        wikipedia_url="https://en.wikipedia.org/wiki/Ace_of_Swords",
        upright_keywords=["clarity", "breakthrough", "new ideas", "mental clarity"],
        reversed_keywords=["confusion", "lack of clarity", "missed opportunities", "chaos"],
        upright_meaning="The Ace of Swords represents clarity, breakthrough, new ideas and mental clarity.",
        reversed_meaning="The Ace of Swords reversed represents confusion, lack of clarity, missed opportunities and chaos.",
        element="Air",
        influence_categories={
            "clarity": 0.95,
            "intellect": 0.9,
            "communication": 0.85,
            "truth": 0.8
        }
    ),
    TarotCard(
        id="two_of_swords",
        name="Two of Swords",
        suit=TarotSuit.SWORDS,
        number=2,
        wikipedia_url="https://en.wikipedia.org/wiki/Two_of_Swords",
        upright_keywords=["difficult decisions", "weighing options", "indecision", "stalemate"],
        reversed_keywords=["indecision", "confusion", "information overload", "postponing decisions"],
        upright_meaning="The Two of Swords represents difficult decisions, weighing options, indecision and stalemate.",
        reversed_meaning="The Two of Swords reversed represents indecision, confusion, information overload and postponing decisions.",
        element="Air",
        influence_categories={
            "decision_making": 0.8,
            "balance": 0.75,
            "analysis": 0.85,
            "contemplation": 0.8
        }
    )
]

# Minor Arcana - Pentacles (Earth)
PENTACLES_SUIT = [
    TarotCard(
        id="ace_of_pentacles",
        name="Ace of Pentacles",
        suit=TarotSuit.PENTACLES,
        number=1,
        wikipedia_url="https://en.wikipedia.org/wiki/Ace_of_Pentacles",
        upright_keywords=["manifestation", "new financial opportunity", "abundance", "prosperity"],
        reversed_keywords=["lost opportunity", "lack of planning", "poor financial decisions", "scarcity"],
        upright_meaning="The Ace of Pentacles represents manifestation, new financial opportunity, abundance and prosperity.",
        reversed_meaning="The Ace of Pentacles reversed represents lost opportunity, lack of planning, poor financial decisions and scarcity.",
        element="Earth",
        influence_categories={
            "manifestation": 0.9,
            "prosperity": 0.95,
            "opportunity": 0.85,
            "material_success": 0.8
        }
    ),
    TarotCard(
        id="two_of_pentacles",
        name="Two of Pentacles",
        suit=TarotSuit.PENTACLES,
        number=2,
        wikipedia_url="https://en.wikipedia.org/wiki/Two_of_Pentacles",
        upright_keywords=["balance", "adaptability", "time management", "prioritization"],
        reversed_keywords=["imbalance", "disorganization", "overwhelmed", "poor time management"],
        upright_meaning="The Two of Pentacles represents balance, adaptability, time management and prioritization.",
        reversed_meaning="The Two of Pentacles reversed represents imbalance, disorganization, overwhelmed and poor time management.",
        element="Earth",
        influence_categories={
            "balance": 0.9,
            "adaptability": 0.85,
            "organization": 0.8,
            "flexibility": 0.75
        }
    )
]

# Complete database (for now with sample cards - can be expanded)
ALL_TAROT_CARDS = MAJOR_ARCANA + WANDS_SUIT + CUPS_SUIT + SWORDS_SUIT + PENTACLES_SUIT
