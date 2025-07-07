"""
Tests for the visual aspects generation system.
"""

import json
import pytest
from pathlib import Path
from core.governors.profiler.interview.visual_aspects_interview import VisualAspectsInterviewer
from core.governors.profiler.schemas.visual_aspects_schema import (
    VisualAspects, FormType, ColorScheme, GeometryPattern
)

def test_generate_visual_aspects_for_abriond():
    """Test generating visual aspects for ABRIOND."""
    # Load ABRIOND's profile
    governor_path = Path("governor_dossier/ABRIOND.json")
    with open(governor_path) as f:
        governor_data = json.load(f)
    
    # Create interviewer
    interviewer = VisualAspectsInterviewer(
        governor_id="ABRIOND",
        governor_name=governor_data["governor_name"],
        governor_traits=governor_data["persona"],
        aethyr_level=3,  # POP is 3rd Aethyr
        mystical_correspondences={
            "element": governor_data["persona"]["element"],
            "zodiac": governor_data["persona"]["archetypal_correspondences"]["zodiac_sign"],
            "sephirot": governor_data["persona"]["archetypal_correspondences"]["sephirot"],
            "tarot": governor_data["persona"]["archetypal_correspondences"]["tarot"]
        }
    )
    
    # Generate profile
    profile = interviewer.generate_visual_profile()
    
    # Validate core aspects
    assert isinstance(profile, VisualAspects)
    assert profile.governor_id == "ABRIOND"
    assert profile.name == "ABRIOND"
    
    # Validate form type
    assert profile.dimensional_manifestation.base_form == FormType.GEOMETRIC
    
    # Validate color scheme (Air element = Silver)
    assert profile.color_scheme == ColorScheme.SILVER
    
    # Validate geometry patterns (Aethyr level 3 = Merkaba + Torus)
    assert GeometryPattern.MERKABA in profile.geometry_patterns
    assert GeometryPattern.TORUS in profile.geometry_patterns
    
    # Validate environmental effects
    assert "Swirling winds" in profile.environmental_effects.primary_effect
    assert profile.environmental_effects.intensity == "powerful"
    
    # Validate time variations
    assert "Mercury" in profile.time_variations.astrological_influences
    assert "Regular cycles" in profile.time_variations.cycle_description
    
    # Validate energy signature
    assert "27Hz" in profile.energy_signature.frequency  # 30 - aethyr_level
    assert profile.energy_signature.polarity == "Balanced/Neutral"
    
    # Validate symbol set
    assert "Primary Seal of ABRIOND" in profile.symbol_set.sigils
    assert "Crest of ABRIOND" in profile.symbol_set.emblems
    
    # Validate light/shadow dynamics
    assert profile.light_shadow.light_expression == "Geometric light patterns"
    assert profile.light_shadow.shadow_interaction == "Shadow harmony"
    
    # Validate scale
    assert "Mountain scale" in profile.scale_description
    assert "Variable" in profile.scale_variations["astral"]
    
    # Validate special properties
    assert any("geometric" in prop.lower() for prop in profile.special_properties)
    
    # Validate manifestation triggers
    assert "Sacred geometry activation" in profile.manifestation_triggers
    
    # Validate observer effects
    assert "Form becomes clearer" in profile.observer_effects 