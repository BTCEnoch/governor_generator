#!/usr/bin/env python3
"""
Simple Numerology Database - Life Path Numbers 1-9
Based on Pythagorean numerology system
"""

from core.governors.profiler.schemas.mystical_schemas import NumerologyProfile, NumerologySystem

# Life Path Numbers 1-9 Database
LIFE_PATH_NUMBERS = [
    NumerologyProfile(
        life_path_number=1,
        system=NumerologySystem.PYTHAGOREAN,
        wikipedia_url="https://en.wikipedia.org/wiki/Life_path_number",
        positive_traits=["leadership", "independence", "innovation", "pioneering"],
        negative_traits=["selfishness", "impatience", "arrogance", "domineering"],
        life_purpose="To lead and pioneer new paths",
        spiritual_meaning="The individual soul beginning its journey",
        compatible_numbers=[3, 5, 6],
        challenging_numbers=[4, 8, 9],
        influence_categories={
            "leadership": 0.95,
            "independence": 0.9,
            "innovation": 0.85,
            "confidence": 0.8
        }
    ),
    
    NumerologyProfile(
        life_path_number=2,
        system=NumerologySystem.PYTHAGOREAN,
        wikipedia_url="https://en.wikipedia.org/wiki/Life_path_number",
        positive_traits=["cooperation", "diplomacy", "sensitivity", "peace-making"],
        negative_traits=["indecision", "oversensitivity", "timidity", "dependency"],
        life_purpose="To bring harmony and cooperation",
        spiritual_meaning="The soul learning partnership and balance",
        compatible_numbers=[1, 4, 8],
        challenging_numbers=[5, 7],
        influence_categories={
            "cooperation": 0.95,
            "diplomacy": 0.9,
            "sensitivity": 0.85,
            "harmony": 0.8
        }
    ),
    
    NumerologyProfile(
        life_path_number=3,
        system=NumerologySystem.PYTHAGOREAN,
        wikipedia_url="https://en.wikipedia.org/wiki/Life_path_number",
        positive_traits=["creativity", "communication", "optimism", "artistic"],
        negative_traits=["superficiality", "scattered energy", "gossip", "criticism"],
        life_purpose="To inspire and create beauty",
        spiritual_meaning="The soul expressing divine creativity",
        compatible_numbers=[1, 5, 9],
        challenging_numbers=[4, 6],
        influence_categories={
            "creativity": 0.95,
            "communication": 0.9,
            "optimism": 0.85,
            "artistic": 0.8
        }
    ),
    
    NumerologyProfile(
        life_path_number=4,
        system=NumerologySystem.PYTHAGOREAN,
        wikipedia_url="https://en.wikipedia.org/wiki/Life_path_number",
        positive_traits=["stability", "hard work", "practicality", "organization"],
        negative_traits=["rigidity", "stubbornness", "narrow-mindedness", "dullness"],
        life_purpose="To build solid foundations",
        spiritual_meaning="The soul learning discipline and structure",
        compatible_numbers=[2, 6, 8],
        challenging_numbers=[1, 3, 5],
        influence_categories={
            "stability": 0.95,
            "practicality": 0.9,
            "organization": 0.85,
            "discipline": 0.8
        }
    ),
    
    NumerologyProfile(
        life_path_number=5,
        system=NumerologySystem.PYTHAGOREAN,
        wikipedia_url="https://en.wikipedia.org/wiki/Life_path_number",
        positive_traits=["freedom", "adventure", "versatility", "progressive"],
        negative_traits=["restlessness", "irresponsibility", "impatience", "addiction"],
        life_purpose="To experience freedom and teach others",
        spiritual_meaning="The soul seeking variety and experience",
        compatible_numbers=[1, 3, 7],
        challenging_numbers=[2, 4, 6],
        influence_categories={
            "freedom": 0.95,
            "adventure": 0.9,
            "versatility": 0.85,
            "change": 0.8
        }
    ),
    
    NumerologyProfile(
        life_path_number=6,
        system=NumerologySystem.PYTHAGOREAN,
        wikipedia_url="https://en.wikipedia.org/wiki/Life_path_number",
        positive_traits=["nurturing", "responsibility", "healing", "service"],
        negative_traits=["perfectionism", "interference", "self-righteousness", "worry"],
        life_purpose="To nurture and heal others",
        spiritual_meaning="The soul learning compassion and service",
        compatible_numbers=[2, 4, 9],
        challenging_numbers=[1, 5, 7],
        influence_categories={
            "nurturing": 0.95,
            "responsibility": 0.9,
            "healing": 0.85,
            "service": 0.8
        }
    ),
    
    NumerologyProfile(
        life_path_number=7,
        system=NumerologySystem.PYTHAGOREAN,
        wikipedia_url="https://en.wikipedia.org/wiki/Life_path_number",
        positive_traits=["spirituality", "analysis", "intuition", "wisdom"],
        negative_traits=["aloofness", "pessimism", "secretiveness", "skepticism"],
        life_purpose="To seek truth and spiritual understanding",
        spiritual_meaning="The soul on a quest for deeper meaning",
        compatible_numbers=[3, 5, 9],
        challenging_numbers=[2, 4, 6],
        influence_categories={
            "spirituality": 0.95,
            "analysis": 0.9,
            "intuition": 0.85,
            "wisdom": 0.8
        }
    ),
    
    NumerologyProfile(
        life_path_number=8,
        system=NumerologySystem.PYTHAGOREAN,
        wikipedia_url="https://en.wikipedia.org/wiki/Life_path_number",
        positive_traits=["achievement", "material success", "authority", "ambition"],
        negative_traits=["materialism", "impatience", "ruthlessness", "stress"],
        life_purpose="To achieve material and spiritual mastery",
        spiritual_meaning="The soul learning balance between material and spiritual",
        compatible_numbers=[2, 4, 6],
        challenging_numbers=[1, 3, 7],
        influence_categories={
            "achievement": 0.95,
            "authority": 0.9,
            "material_success": 0.85,
            "ambition": 0.8
        }
    ),
    
    NumerologyProfile(
        life_path_number=9,
        system=NumerologySystem.PYTHAGOREAN,
        wikipedia_url="https://en.wikipedia.org/wiki/Life_path_number",
        positive_traits=["humanitarianism", "generosity", "wisdom", "completion"],
        negative_traits=["self-pity", "moodiness", "resentment", "impracticality"],
        life_purpose="To serve humanity and bring completion",
        spiritual_meaning="The soul completing its earthly lessons",
        compatible_numbers=[3, 6, 7],
        challenging_numbers=[1, 4, 8],
        influence_categories={
            "humanitarianism": 0.95,
            "generosity": 0.9,
            "wisdom": 0.85,
            "completion": 0.8
        }
    )
]

def get_life_path_number(birthdate_sum: int) -> int:
    """Calculate life path number from birthdate sum"""
    while birthdate_sum > 9:
        digits = [int(d) for d in str(birthdate_sum)]
        birthdate_sum = sum(digits)
    return birthdate_sum

def get_numerology_profile(life_path_number: int) -> NumerologyProfile:
    """Get numerology profile by life path number"""
    for profile in LIFE_PATH_NUMBERS:
        if profile.life_path_number == life_path_number:
            return profile
    raise ValueError(f"Profile not found for life path number: {life_path_number}")

def calculate_name_numerology(name: str) -> int:
    """Simple name number calculation using Pythagorean system"""
    letter_values = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }
    
    total = sum(letter_values.get(char.upper(), 0) for char in name if char.isalpha())
    return get_life_path_number(total) 