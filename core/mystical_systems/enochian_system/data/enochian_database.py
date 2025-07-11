"""
Database functions for the Enochian Magic System
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, cast

from core.utils.custom_logging import setup_logger
from ..schemas import (
    EnochianLetter,
    EnochianLetterType,
    AethyrProfile,
    EnochianTable,
    Direction
)

logger = setup_logger("enochian_database")

def load_json_data(filename: str) -> Dict[str, Any]:
    """Load JSON data from game assets"""
    try:
        file_path = Path("core/game_assets/pack") / filename
        with open(file_path, 'r', encoding='utf-8') as f:
            return cast(Dict[str, Any], json.load(f))
    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
        return {}

def get_enochian_alphabet() -> List[EnochianLetter]:
    """Get the complete Enochian alphabet with correspondences"""
    try:
        data = load_json_data("enochian_alphabet.json")
        letters = []
        
        # Map basic letters from data
        alphabet = cast(List[str], data.get("alphabet", []))
        for letter_data in alphabet:
            letter = EnochianLetter(
                name=letter_data,
                glyph=f"[{letter_data}]",  # Placeholder for actual glyphs
                type=EnochianLetterType.REGULAR,
                numeric_value=len(letters) + 1,
                element="fire" if len(letters) % 4 == 0 else
                        "water" if len(letters) % 4 == 1 else
                        "air" if len(letters) % 4 == 2 else "earth",
                power_level=((len(letters) % 10) + 1)
            )
            letters.append(letter)
            
        return letters
        
    except Exception as e:
        logger.error(f"Error getting Enochian alphabet: {e}")
        return []

def get_aethyr_data() -> List[AethyrProfile]:
    """Get data for all 30 Aethyrs"""
    try:
        data = load_json_data("aethyrs.json")
        aethyrs = []
        
        for aethyr_data in cast(List[Dict[str, Any]], data):
            governors = [
                cast(Dict[str, Any], gov)["name"]
                for gov in cast(List[Dict[str, Any]], aethyr_data.get("governors", []))
            ]
            
            aethyr = AethyrProfile(
                name=cast(str, aethyr_data["name"]),
                number=cast(int, aethyr_data["number"]),
                governors=governors,
                correspondence=cast(str, aethyr_data["correspondence"]),
                description=f"The {cast(int, aethyr_data['number'])}th Aethyr",  # Placeholder
                ritual_requirements=[
                    "Sacred space",
                    "Proper timing",
                    "Governor invocation"
                ],
                influence=0.7  # Default influence level
            )
            aethyrs.append(aethyr)
            
        return aethyrs
        
    except Exception as e:
        logger.error(f"Error getting Aethyr data: {e}")
        return []

def get_watchtower_table(direction: Direction) -> Optional[EnochianTable]:
    """Get Watchtower table for a specific direction"""
    try:
        # Placeholder - implement actual table loading
        elements = {
            Direction.EAST: "air",
            Direction.SOUTH: "fire",
            Direction.WEST: "water",
            Direction.NORTH: "earth"
        }
        
        return EnochianTable(
            direction=direction,
            element=elements[direction],
            king_name=f"{direction.value.title()} King",
            senior_names=[f"Senior {i+1}" for i in range(6)],
            kerubic_angels=[f"Kerub {i+1}" for i in range(4)],
            servient_angels=[f"Servient {i+1}" for i in range(16)],
            grid=[[" " for _ in range(13)] for _ in range(12)]
        )
        
    except Exception as e:
        logger.error(f"Error getting Watchtower table: {e}")
        return None

def get_ritual_correspondences(governor_name: str) -> Dict[str, Any]:
    """Get ritual correspondences for a Governor"""
    try:
        data = load_json_data("aethyrs.json")
        
        for aethyr in cast(List[Dict[str, Any]], data):
            for gov in cast(List[Dict[str, Any]], aethyr.get("governors", [])):
                if cast(str, gov["name"]) == governor_name:
                    return {
                        "region": cast(str, gov["region"]),
                        "traits": cast(Dict[str, Any], gov["traits"]),
                        "aethyr": cast(str, aethyr["name"]),
                        "correspondence": cast(str, aethyr["correspondence"])
                    }
        
        return {}
        
    except Exception as e:
        logger.error(f"Error getting ritual correspondences: {e}")
        return {} 