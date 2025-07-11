"""
Sacred Geometry Database

This module contains the core data for sacred geometric forms and their correspondences.
"""

from typing import Dict, List

FORM_DATA = {
    "point": {
        "name": "Point",
        "dimension": 0,
        "symbolism": "Unity, Source, Origin",
        "elements": ["Spirit"],
        "ritual_uses": ["Centering", "Focus", "Meditation"],
        "governor_aspects": ["Divine Spark", "Core Essence", "Primal Being"]
    },
    "line": {
        "name": "Line",
        "dimension": 1,
        "symbolism": "Duality, Connection, Path",
        "elements": ["Air"],
        "ritual_uses": ["Connection", "Direction", "Movement"],
        "governor_aspects": ["Communication", "Journey", "Growth"]
    },
    "triangle": {
        "name": "Triangle",
        "dimension": 2,
        "symbolism": "Dynamic Force, Creation, Action",
        "elements": ["Fire"],
        "ritual_uses": ["Manifestation", "Transformation", "Power"],
        "governor_aspects": ["Will", "Action", "Change"]
    },
    "square": {
        "name": "Square",
        "dimension": 2,
        "symbolism": "Stability, Matter, Foundation",
        "elements": ["Earth"],
        "ritual_uses": ["Grounding", "Protection", "Stability"],
        "governor_aspects": ["Structure", "Order", "Manifestation"]
    },
    "pentagon": {
        "name": "Pentagon",
        "dimension": 2,
        "symbolism": "Life Force, Protection, Power",
        "elements": ["All"],
        "ritual_uses": ["Protection", "Life Magic", "Empowerment"],
        "governor_aspects": ["Defense", "Vitality", "Strength"]
    },
    "hexagon": {
        "name": "Hexagon",
        "dimension": 2,
        "symbolism": "Harmony, Balance, Communication",
        "elements": ["Air", "Earth"],
        "ritual_uses": ["Harmony", "Balance", "Integration"],
        "governor_aspects": ["Wisdom", "Teaching", "Understanding"]
    },
    "circle": {
        "name": "Circle",
        "dimension": 2,
        "symbolism": "Wholeness, Infinity, Cycles",
        "elements": ["Spirit"],
        "ritual_uses": ["Protection", "Cycles", "Completion"],
        "governor_aspects": ["Perfection", "Eternity", "Unity"]
    },
    "vesica_piscis": {
        "name": "Vesica Piscis",
        "dimension": 2,
        "symbolism": "Sacred Birth, Intersection, Gateway",
        "elements": ["Water", "Air"],
        "ritual_uses": ["Creation", "Doorways", "Vision"],
        "governor_aspects": ["Birth", "Revelation", "Insight"]
    },
    "seed_of_life": {
        "name": "Seed of Life",
        "dimension": 2,
        "symbolism": "Creation Pattern, Genesis, Beginning",
        "elements": ["All"],
        "ritual_uses": ["Creation", "Growth", "Genesis"],
        "governor_aspects": ["Creation", "Pattern", "Origin"]
    },
    "flower_of_life": {
        "name": "Flower of Life",
        "dimension": 2,
        "symbolism": "Universal Pattern, Sacred Creation",
        "elements": ["All"],
        "ritual_uses": ["Universal Magic", "Creation", "Life"],
        "governor_aspects": ["Universe", "Pattern", "Life"]
    },
    "metatrons_cube": {
        "name": "Metatron's Cube",
        "dimension": 3,
        "symbolism": "Sacred Architecture, Divine Plan",
        "elements": ["All"],
        "ritual_uses": ["Sacred Geometry", "Divine Connection"],
        "governor_aspects": ["Divine Plan", "Structure", "Order"]
    },
    "tetrahedron": {
        "name": "Tetrahedron",
        "dimension": 3,
        "symbolism": "Fire Element, Dynamic Energy",
        "elements": ["Fire"],
        "ritual_uses": ["Fire Magic", "Energy Work", "Action"],
        "governor_aspects": ["Energy", "Action", "Force"]
    },
    "cube": {
        "name": "Cube",
        "dimension": 3,
        "symbolism": "Earth Element, Material World",
        "elements": ["Earth"],
        "ritual_uses": ["Grounding", "Manifestation", "Stability"],
        "governor_aspects": ["Form", "Matter", "Structure"]
    },
    "octahedron": {
        "name": "Octahedron",
        "dimension": 3,
        "symbolism": "Air Element, Thought, Mind",
        "elements": ["Air"],
        "ritual_uses": ["Air Magic", "Mental Work", "Thought"],
        "governor_aspects": ["Mind", "Thought", "Connection"]
    },
    "dodecahedron": {
        "name": "Dodecahedron",
        "dimension": 3,
        "symbolism": "Aether Element, Universe, Spirit",
        "elements": ["Spirit"],
        "ritual_uses": ["Spirit Work", "Universal Magic", "Cosmos"],
        "governor_aspects": ["Universe", "Spirit", "Cosmos"]
    },
    "icosahedron": {
        "name": "Icosahedron",
        "dimension": 3,
        "symbolism": "Water Element, Flow, Emotion",
        "elements": ["Water"],
        "ritual_uses": ["Water Magic", "Emotional Work", "Flow"],
        "governor_aspects": ["Flow", "Emotion", "Adaptation"]
    }
}

PROPORTION_DATA = {
    "phi": {
        "name": "Golden Ratio (Phi)",
        "value": 1.618033988749895,
        "symbolism": "Divine Proportion, Natural Growth",
        "ritual_uses": ["Harmony", "Growth", "Beauty"],
        "governor_aspects": ["Divine Order", "Natural Law", "Beauty"]
    },
    "pi": {
        "name": "Pi",
        "value": 3.141592653589793,
        "symbolism": "Cycles, Circles, Wholeness",
        "ritual_uses": ["Cycles", "Completion", "Unity"],
        "governor_aspects": ["Cycles", "Completion", "Wholeness"]
    },
    "sqrt2": {
        "name": "Square Root of 2",
        "value": 1.4142135623730951,
        "symbolism": "Dynamic Growth, Sacred Measure",
        "ritual_uses": ["Growth", "Expansion", "Balance"],
        "governor_aspects": ["Growth", "Balance", "Measure"]
    },
    "sqrt3": {
        "name": "Square Root of 3",
        "value": 1.7320508075688772,
        "symbolism": "Divine Triangle, Harmony",
        "ritual_uses": ["Harmony", "Trinity", "Balance"],
        "governor_aspects": ["Trinity", "Harmony", "Balance"]
    },
    "sqrt5": {
        "name": "Square Root of 5",
        "value": 2.236067977499790,
        "symbolism": "Life Force, Natural Power",
        "ritual_uses": ["Life Force", "Power", "Nature"],
        "governor_aspects": ["Life Force", "Power", "Nature"]
    }
}

def get_form_data(form_name: str) -> Dict:
    """Get data for a specific geometric form"""
    return FORM_DATA.get(form_name, {})

def get_proportion_data(proportion_name: str) -> Dict:
    """Get data for a specific sacred proportion"""
    return PROPORTION_DATA.get(proportion_name, {})

def get_form_elements(form_name: str) -> List[str]:
    """Get elemental associations for a geometric form"""
    form_data = get_form_data(form_name)
    return form_data.get("elements", []) 