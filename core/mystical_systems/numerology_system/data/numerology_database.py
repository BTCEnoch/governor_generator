#!/usr/bin/env python3
"""
Numerology System Database and Calculations
"""

from datetime import datetime
from typing import Dict, Any
from ..schemas import NumerologySystem

def reduce_to_single_digit(number: int) -> int:
    """Reduce a number to a single digit (1-9)"""
    while number > 9:
        number = sum(int(d) for d in str(number))
    return number

def calculate_life_path_number(birthdate: str, system: NumerologySystem = NumerologySystem.PYTHAGOREAN) -> int:
    """Calculate life path number from birthdate"""
    try:
        date = datetime.strptime(birthdate, "%Y-%m-%d")
        year_sum = sum(int(d) for d in str(date.year))
        month_sum = sum(int(d) for d in str(date.month))
        day_sum = sum(int(d) for d in str(date.day))
        total = year_sum + month_sum + day_sum
        return reduce_to_single_digit(total)
    except Exception:
        return 0

def calculate_destiny_number(name: str, system: NumerologySystem = NumerologySystem.PYTHAGOREAN) -> int:
    """Calculate destiny/expression number from name"""
    try:
        # Remove spaces and convert to uppercase
        name = name.replace(" ", "").upper()
        
        # Pythagorean number system
        if system == NumerologySystem.PYTHAGOREAN:
            number_map = {
                'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
                'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
                'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
            }
        # Chaldean number system
        elif system == NumerologySystem.CHALDEAN:
            number_map = {
                'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 5, 'I': 1,
                'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8, 'Q': 1, 'R': 2,
                'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 5, 'Y': 1, 'Z': 7
            }
        # Kabbalah number system
        else:
            number_map = {
                'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
                'J': 600, 'K': 20, 'L': 30, 'M': 40, 'N': 50, 'O': 60, 'P': 70, 'Q': 80,
                'R': 200, 'S': 300, 'T': 400, 'U': 6, 'V': 6, 'W': 6, 'X': 60, 'Y': 10,
                'Z': 7
            }
            
        total = sum(number_map.get(c, 0) for c in name)
        return reduce_to_single_digit(total)
    except Exception:
        return 0

def calculate_soul_urge_number(name: str, system: NumerologySystem = NumerologySystem.PYTHAGOREAN) -> int:
    """Calculate soul urge/heart's desire number from name vowels"""
    try:
        # Remove spaces and convert to uppercase
        name = name.replace(" ", "").upper()
        vowels = 'AEIOU'
        
        # Pythagorean number system
        if system == NumerologySystem.PYTHAGOREAN:
            number_map = {'A': 1, 'E': 5, 'I': 9, 'O': 6, 'U': 3}
        # Chaldean number system
        elif system == NumerologySystem.CHALDEAN:
            number_map = {'A': 1, 'E': 5, 'I': 1, 'O': 7, 'U': 6}
        # Kabbalah number system
        else:
            number_map = {'A': 1, 'E': 5, 'I': 9, 'O': 60, 'U': 6}
            
        total = sum(number_map.get(c, 0) for c in name if c in vowels)
        return reduce_to_single_digit(total)
    except Exception:
        return 0

def calculate_personality_number(name: str, system: NumerologySystem = NumerologySystem.PYTHAGOREAN) -> int:
    """Calculate personality number from name consonants"""
    try:
        # Remove spaces and convert to uppercase
        name = name.replace(" ", "").upper()
        consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
        
        # Pythagorean number system
        if system == NumerologySystem.PYTHAGOREAN:
            number_map = {
                'B': 2, 'C': 3, 'D': 4, 'F': 6, 'G': 7, 'H': 8,
                'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5,
                'P': 7, 'Q': 8, 'R': 9, 'S': 1, 'T': 2,
                'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
            }
        # Chaldean number system
        elif system == NumerologySystem.CHALDEAN:
            number_map = {
                'B': 2, 'C': 3, 'D': 4, 'F': 8, 'G': 3, 'H': 5,
                'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5,
                'P': 8, 'Q': 1, 'R': 2, 'S': 3, 'T': 4,
                'V': 6, 'W': 6, 'X': 5, 'Y': 1, 'Z': 7
            }
        # Kabbalah number system
        else:
            number_map = {
                'B': 2, 'C': 3, 'D': 4, 'F': 6, 'G': 7, 'H': 8,
                'J': 600, 'K': 20, 'L': 30, 'M': 40, 'N': 50,
                'P': 70, 'Q': 80, 'R': 200, 'S': 300, 'T': 400,
                'V': 6, 'W': 6, 'X': 60, 'Y': 10, 'Z': 7
            }
            
        total = sum(number_map.get(c, 0) for c in name if c in consonants)
        return reduce_to_single_digit(total)
    except Exception:
        return 0

def calculate_birth_day_number(birthdate: str, system: NumerologySystem = NumerologySystem.PYTHAGOREAN) -> int:
    """Calculate birth day number"""
    try:
        date = datetime.strptime(birthdate, "%Y-%m-%d")
        return reduce_to_single_digit(date.day)
    except Exception:
        return 0

def calculate_current_year_number(birthdate: str, system: NumerologySystem = NumerologySystem.PYTHAGOREAN) -> int:
    """Calculate current year personal number"""
    try:
        date = datetime.strptime(birthdate, "%Y-%m-%d")
        current_year = datetime.now().year
        month_day = date.month + date.day
        total = current_year + month_day
        return reduce_to_single_digit(total)
    except Exception:
        return 0 