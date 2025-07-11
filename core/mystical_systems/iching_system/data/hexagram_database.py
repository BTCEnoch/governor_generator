"""
I Ching Hexagram Database

Contains basic hexagram data and lookup functions.
"""

from typing import Dict, Optional

# Basic hexagram data - will be expanded with more details
HEXAGRAM_DATA: Dict[int, Dict[str, str]] = {
    1: {
        "name": "Qian (The Creative)",
        "unicode": "䷀",
        "description": "Pure Yang, Heaven, The Creative Principle",
        "judgment": "The Creative works sublime success, furthering through perseverance.",
        "image": "The movement of heaven is full of power."
    },
    2: {
        "name": "Kun (The Receptive)",
        "unicode": "䷁",
        "description": "Pure Yin, Earth, The Receptive Principle",
        "judgment": "The Receptive brings about sublime success, furthering through the perseverance of a mare.",
        "image": "The earth's condition is receptive devotion."
    }
    # Additional hexagrams will be added here
}

def get_hexagram_data(number: int) -> Optional[Dict[str, str]]:
    """
    Get data for a specific hexagram by number.
    
    Args:
        number: Hexagram number (1-64)
        
    Returns:
        Dictionary of hexagram data or None if not found
    """
    return HEXAGRAM_DATA.get(number) 