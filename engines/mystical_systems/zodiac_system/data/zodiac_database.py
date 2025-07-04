#!/usr/bin/env python3
"""
Simple Western Zodiac Database - 12 Zodiac Signs
Traditional Western astrology with basic traits and correspondences
"""

from core.governors.profiler.schemas.mystical_schemas import ZodiacSign, ZodiacElement, ZodiacModality

# Zodiac Signs Database Part 1 (Aries - Virgo)
ZODIAC_SIGNS_PART1 = [
    ZodiacSign(
        name="Aries",
        symbol="♈",
        dates="March 21 - April 19",
        element=ZodiacElement.FIRE,
        modality=ZodiacModality.CARDINAL,
        ruling_planet="Mars",
        wikipedia_url="https://en.wikipedia.org/wiki/Aries_(astrology)",
        positive_traits=["pioneering", "energetic", "courageous", "confident"],
        negative_traits=["impatient", "aggressive", "impulsive", "selfish"],
        keywords=["initiative", "leadership", "action", "new beginnings"],
        tarot_correspondence="The Emperor",
        body_parts=["head", "brain", "eyes"],
        colors=["red", "orange", "bright yellow"],
        stones=["diamond", "ruby", "garnet"],
        influence_categories={
            "leadership": 0.9,
            "courage": 0.95,
            "initiative": 0.9,
            "energy": 0.85
        }
    ),
    
    ZodiacSign(
        name="Taurus",
        symbol="♉",
        dates="April 20 - May 20",
        element=ZodiacElement.EARTH,
        modality=ZodiacModality.FIXED,
        ruling_planet="Venus",
        wikipedia_url="https://en.wikipedia.org/wiki/Taurus_(astrology)",
        positive_traits=["reliable", "patient", "practical", "devoted"],
        negative_traits=["stubborn", "possessive", "materialistic", "inflexible"],
        keywords=["stability", "security", "sensuality", "persistence"],
        tarot_correspondence="The Hierophant",
        body_parts=["neck", "throat", "thyroid"],
        colors=["green", "pink", "earth tones"],
        stones=["emerald", "rose quartz", "sapphire"],
        influence_categories={
            "stability": 0.95,
            "persistence": 0.9,
            "practicality": 0.85,
            "sensuality": 0.8
        }
    ),
    
    ZodiacSign(
        name="Gemini",
        symbol="♊",
        dates="May 21 - June 20",
        element=ZodiacElement.AIR,
        modality=ZodiacModality.MUTABLE,
        ruling_planet="Mercury",
        wikipedia_url="https://en.wikipedia.org/wiki/Gemini_(astrology)",
        positive_traits=["adaptable", "curious", "communicative", "witty"],
        negative_traits=["inconsistent", "superficial", "indecisive", "nervous"],
        keywords=["communication", "duality", "versatility", "learning"],
        tarot_correspondence="The Lovers",
        body_parts=["arms", "hands", "lungs", "nervous system"],
        colors=["yellow", "light blue", "silver"],
        stones=["agate", "citrine", "aquamarine"],
        influence_categories={
            "communication": 0.95,
            "adaptability": 0.9,
            "curiosity": 0.85,
            "versatility": 0.8
        }
    ),
    
    ZodiacSign(
        name="Cancer",
        symbol="♋",
        dates="June 21 - July 22",
        element=ZodiacElement.WATER,
        modality=ZodiacModality.CARDINAL,
        ruling_planet="Moon",
        wikipedia_url="https://en.wikipedia.org/wiki/Cancer_(astrology)",
        positive_traits=["nurturing", "intuitive", "protective", "empathetic"],
        negative_traits=["moody", "clingy", "pessimistic", "manipulative"],
        keywords=["emotions", "home", "family", "nurturing"],
        tarot_correspondence="The Chariot",
        body_parts=["chest", "breasts", "stomach"],
        colors=["silver", "white", "sea green"],
        stones=["moonstone", "pearl", "ruby"],
        influence_categories={
            "nurturing": 0.95,
            "intuition": 0.9,
            "emotion": 0.95,
            "protection": 0.85
        }
    ),
    
    ZodiacSign(
        name="Leo",
        symbol="♌",
        dates="July 23 - August 22",
        element=ZodiacElement.FIRE,
        modality=ZodiacModality.FIXED,
        ruling_planet="Sun",
        wikipedia_url="https://en.wikipedia.org/wiki/Leo_(astrology)",
        positive_traits=["confident", "generous", "creative", "charismatic"],
        negative_traits=["arrogant", "domineering", "attention-seeking", "stubborn"],
        keywords=["creativity", "self-expression", "leadership", "drama"],
        tarot_correspondence="Strength",
        body_parts=["heart", "spine", "upper back"],
        colors=["gold", "orange", "bright yellow"],
        stones=["peridot", "citrine", "carnelian"],
        influence_categories={
            "creativity": 0.95,
            "confidence": 0.9,
            "leadership": 0.85,
            "charisma": 0.9
        }
    ),
    
    ZodiacSign(
        name="Virgo",
        symbol="♍",
        dates="August 23 - September 22",
        element=ZodiacElement.EARTH,
        modality=ZodiacModality.MUTABLE,
        ruling_planet="Mercury",
        wikipedia_url="https://en.wikipedia.org/wiki/Virgo_(astrology)",
        positive_traits=["analytical", "practical", "reliable", "helpful"],
        negative_traits=["critical", "perfectionist", "worrying", "overly cautious"],
        keywords=["service", "perfection", "analysis", "health"],
        tarot_correspondence="The Hermit",
        body_parts=["digestive system", "intestines", "spleen"],
        colors=["navy blue", "grey", "brown"],
        stones=["sapphire", "carnelian", "jade"],
        influence_categories={
            "analysis": 0.95,
            "service": 0.9,
            "perfection": 0.85,
            "practicality": 0.8
        }
    )
] 

# Zodiac Signs Database Part 2 (Libra - Pisces)
ZODIAC_SIGNS_PART2 = [
    ZodiacSign(
        name="Libra",
        symbol="♎",
        dates="September 23 - October 22",
        element=ZodiacElement.AIR,
        modality=ZodiacModality.CARDINAL,
        ruling_planet="Venus",
        wikipedia_url="https://en.wikipedia.org/wiki/Libra_(astrology)",
        positive_traits=["diplomatic", "fair-minded", "social", "artistic"],
        negative_traits=["indecisive", "superficial", "vain", "people-pleasing"],
        keywords=["balance", "harmony", "justice", "partnerships"],
        tarot_correspondence="Justice",
        body_parts=["kidneys", "lower back", "skin"],
        colors=["pink", "light blue", "lavender"],
        stones=["opal", "tourmaline", "lapis lazuli"],
        influence_categories={
            "diplomacy": 0.95,
            "balance": 0.9,
            "harmony": 0.95,
            "social": 0.85
        }
    ),
    
    ZodiacSign(
        name="Scorpio",
        symbol="♏",
        dates="October 23 - November 21",
        element=ZodiacElement.WATER,
        modality=ZodiacModality.FIXED,
        ruling_planet="Pluto",
        wikipedia_url="https://en.wikipedia.org/wiki/Scorpio_(astrology)",
        positive_traits=["passionate", "resourceful", "brave", "loyal"],
        negative_traits=["jealous", "secretive", "resentful", "controlling"],
        keywords=["transformation", "intensity", "mystery", "depth"],
        tarot_correspondence="Death",
        body_parts=["reproductive organs", "pelvis", "urinary tract"],
        colors=["deep red", "black", "maroon"],
        stones=["topaz", "garnet", "obsidian"],
        influence_categories={
            "intensity": 0.95,
            "transformation": 0.9,
            "passion": 0.95,
            "mystery": 0.85
        }
    ),
    
    ZodiacSign(
        name="Sagittarius",
        symbol="♐",
        dates="November 22 - December 21",
        element=ZodiacElement.FIRE,
        modality=ZodiacModality.MUTABLE,
        ruling_planet="Jupiter",
        wikipedia_url="https://en.wikipedia.org/wiki/Sagittarius_(astrology)",
        positive_traits=["optimistic", "adventurous", "philosophical", "honest"],
        negative_traits=["impatient", "tactless", "restless", "careless"],
        keywords=["freedom", "adventure", "philosophy", "expansion"],
        tarot_correspondence="Temperance",
        body_parts=["hips", "thighs", "liver"],
        colors=["purple", "turquoise", "bright blue"],
        stones=["turquoise", "amethyst", "sodalite"],
        influence_categories={
            "adventure": 0.95,
            "optimism": 0.9,
            "philosophy": 0.85,
            "freedom": 0.9
        }
    )
]

# Complete zodiac database
ALL_ZODIAC_SIGNS = ZODIAC_SIGNS_PART1 + ZODIAC_SIGNS_PART2 + [
    ZodiacSign(
        name="Capricorn",
        symbol="♑",
        dates="December 22 - January 19",
        element=ZodiacElement.EARTH,
        modality=ZodiacModality.CARDINAL,
        ruling_planet="Saturn",
        wikipedia_url="https://en.wikipedia.org/wiki/Capricorn_(astrology)",
        positive_traits=["ambitious", "disciplined", "practical", "responsible"],
        negative_traits=["pessimistic", "stubborn", "unforgiving", "condescending"],
        keywords=["achievement", "authority", "structure", "tradition"],
        tarot_correspondence="The Devil",
        body_parts=["knees", "bones", "teeth"],
        colors=["black", "brown", "dark green"],
        stones=["garnet", "onyx", "jet"],
        influence_categories={
            "ambition": 0.95,
            "discipline": 0.9,
            "authority": 0.85,
            "structure": 0.9
        }
    ),
    
    ZodiacSign(
        name="Aquarius",
        symbol="♒",
        dates="January 20 - February 18",
        element=ZodiacElement.AIR,
        modality=ZodiacModality.FIXED,
        ruling_planet="Uranus",
        wikipedia_url="https://en.wikipedia.org/wiki/Aquarius_(astrology)",
        positive_traits=["independent", "original", "humanitarian", "intellectual"],
        negative_traits=["detached", "stubborn", "aloof", "unpredictable"],
        keywords=["innovation", "humanity", "friendship", "rebellion"],
        tarot_correspondence="The Star",
        body_parts=["ankles", "calves", "circulatory system"],
        colors=["electric blue", "silver", "aqua"],
        stones=["amethyst", "garnet", "hematite"],
        influence_categories={
            "innovation": 0.95,
            "independence": 0.9,
            "humanitarian": 0.85,
            "originality": 0.9
        }
    ),
    
    ZodiacSign(
        name="Pisces",
        symbol="♓",
        dates="February 19 - March 20",
        element=ZodiacElement.WATER,
        modality=ZodiacModality.MUTABLE,
        ruling_planet="Neptune",
        wikipedia_url="https://en.wikipedia.org/wiki/Pisces_(astrology)",
        positive_traits=["compassionate", "artistic", "intuitive", "gentle"],
        negative_traits=["overly emotional", "fearful", "naive", "victim mentality"],
        keywords=["spirituality", "compassion", "imagination", "sacrifice"],
        tarot_correspondence="The Moon",
        body_parts=["feet", "toes", "lymphatic system"],
        colors=["sea green", "lavender", "silver"],
        stones=["aquamarine", "bloodstone", "jade"],
        influence_categories={
            "compassion": 0.95,
            "intuition": 0.9,
            "spirituality": 0.85,
            "imagination": 0.9
        }
    )
]

def get_zodiac_sign_by_name(name: str) -> ZodiacSign:
    """Get zodiac sign by name"""
    for sign in ALL_ZODIAC_SIGNS:
        if sign.name.lower() == name.lower():
            return sign
    raise ValueError(f"Zodiac sign not found: {name}")

def get_zodiac_signs_by_element(element: ZodiacElement) -> list[ZodiacSign]:
    """Get all zodiac signs for a specific element"""
    return [sign for sign in ALL_ZODIAC_SIGNS if sign.element == element] 