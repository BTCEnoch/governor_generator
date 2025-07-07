"""Tests for visual aspects schemas."""

import pytest
from pydantic import ValidationError
from core.game_assets.visual_aspects.schemas import (
    Point3D,
    EffectSchema,
    DimensionalManifestationSchema,
    ColorSchemeSchema,
    GeometrySystemSchema,
    EnvironmentalEffectSchema,
    TimeVariationSchema,
    EnergySignatureSchema,
    SymbolSetSchema,
    LightShadowSchema,
    ScaleSystemSchema,
    VisualAspectSchema
)

def test_point3d():
    """Test Point3D schema validation"""
    # Valid data
    data = {"x": 1.0, "y": 2.0, "z": 3.0}
    point = Point3D(**data)
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 3.0

    # Invalid data
    with pytest.raises(ValidationError):
        Point3D(x=float("invalid"), y=2.0, z=3.0)

def test_effect_schema():
    """Test EffectSchema validation"""
    # Valid data
    data = {
        "type": "test",
        "intensity": 0.5,
        "duration": 60.0,
        "radius": 10.0
    }
    effect = EffectSchema(**data)
    assert effect.type == "test"
    assert effect.intensity == 0.5
    assert effect.duration == 60.0
    assert effect.radius == 10.0

    # Invalid intensity
    with pytest.raises(ValidationError):
        EffectSchema(
            type="test",
            intensity=2.0,  # Must be between 0 and 1
            duration=60.0,
            radius=10.0
        )

    # Invalid negative values
    with pytest.raises(ValidationError):
        EffectSchema(
            type="test",
            intensity=0.5,
            duration=-1.0,  # Must be positive
            radius=10.0
        )

def test_dimensional_manifestation_schema():
    """Test DimensionalManifestationSchema validation"""
    # Valid data
    data = {
        "base_form": "ETHEREAL",
        "form_description": "Test form",
        "dimensional_variations": {
            "etheric": "var1",
            "astral": "var2"
        },
        "transition_effects": ["effect1"],
        "constant_elements": ["element1"]
    }
    manifest = DimensionalManifestationSchema(**data)
    assert manifest.base_form == "ETHEREAL"
    assert len(manifest.dimensional_variations) == 2

    # Optional fields can be omitted
    minimal_data = {
        "base_form": "ETHEREAL",
        "form_description": "Test form",
        "dimensional_variations": {"etheric": "var1"}
    }
    manifest = DimensionalManifestationSchema(**minimal_data)
    assert manifest.transition_effects == []
    assert manifest.constant_elements == []

def test_color_scheme_schema():
    """Test ColorSchemeSchema validation"""
    # Valid data
    data = {
        "primary_colors": ["red", "blue"],
        "elemental_association": "fire",
        "intensity_levels": {"low": 1, "high": 2},
        "transition_effects": ["fade"]
    }
    scheme = ColorSchemeSchema(**data)
    assert len(scheme.primary_colors) == 2
    assert scheme.elemental_association == "fire"

def test_geometry_system_schema():
    """Test GeometrySystemSchema validation"""
    # Valid data
    data = {
        "pattern_type": ["MERKABA"],
        "complexity_level": 5,
        "interaction_points": [
            Point3D(x=0.0, y=0.0, z=0.0)
        ],
        "power_requirements": {"req1": 10}
    }
    system = GeometrySystemSchema(**data)
    assert system.complexity_level == 5

    # Invalid complexity level
    with pytest.raises(ValidationError):
        GeometrySystemSchema(
            pattern_type=["MERKABA"],
            complexity_level=11,  # Must be between 1 and 10
            interaction_points=[Point3D(x=0.0, y=0.0, z=0.0)],
            power_requirements={"req1": 10}
        )

def test_environmental_effect_schema():
    """Test EnvironmentalEffectSchema validation"""
    # Valid data
    data = {
        "primary_effect": "test",
        "radius": 10.0,
        "duration": "60s",
        "intensity": "high",
        "secondary_effects": ["effect1"]
    }
    effect = EnvironmentalEffectSchema(**data)
    assert effect.radius == 10.0

    # Invalid negative radius
    with pytest.raises(ValidationError):
        EnvironmentalEffectSchema(
            primary_effect="test",
            radius=-1.0,  # Must be positive
            duration="60s",
            intensity="high"
        )

def test_time_variation_schema():
    """Test TimeVariationSchema validation"""
    # Valid data
    data = {
        "astrological_influences": ["moon"],
        "cycle_description": "test cycle",
        "peak_manifestation": "peak",
        "dormant_manifestation": "dormant"
    }
    variation = TimeVariationSchema(**data)
    assert len(variation.astrological_influences) == 1

def test_energy_signature_schema():
    """Test EnergySignatureSchema validation"""
    # Valid data
    data = {
        "frequency": "high",
        "polarity": "positive",
        "intensity": "strong",
        "special_properties": ["prop1"]
    }
    signature = EnergySignatureSchema(**data)
    assert signature.frequency == "high"

def test_symbol_set_schema():
    """Test SymbolSetSchema validation"""
    # Valid data
    data = {
        "sigils": ["sigil1"],
        "emblems": ["emblem1"],
        "seals": ["seal1"],
        "scripts": ["script1"]
    }
    symbols = SymbolSetSchema(**data)
    assert len(symbols.sigils) == 1

def test_light_shadow_schema():
    """Test LightShadowSchema validation"""
    # Valid data
    data = {
        "light_expression": "bright",
        "shadow_interaction": "dark",
        "balance_point": "medium",
        "special_effects": ["effect1"]
    }
    dynamics = LightShadowSchema(**data)
    assert dynamics.light_expression == "bright"

def test_scale_system_schema():
    """Test ScaleSystemSchema validation"""
    # Valid data
    data = {
        "base_scale": "medium",
        "plane_variations": {"plane1": "large"},
        "interaction_ranges": {"range1": 10.0},
        "ritual_requirements": {"req1": "large"}
    }
    system = ScaleSystemSchema(**data)
    assert system.base_scale == "medium"

def test_visual_aspect_schema():
    """Test complete VisualAspectSchema validation"""
    # Use the example from schema_extra
    data = VisualAspectSchema.Config.schema_extra["example"]
    
    # Should validate without errors
    aspect = VisualAspectSchema(**data)
    assert aspect.governor_id == "VOANAMB"
    
    # Test required fields
    required_fields = [
        "governor_id",
        "dimensional",
        "color_scheme",
        "geometry",
        "environment",
        "time_variation",
        "energy",
        "symbols",
        "light_shadow",
        "scale"
    ]
    
    for field in required_fields:
        invalid_data = data.copy()
        del invalid_data[field]
        with pytest.raises(ValidationError):
            VisualAspectSchema(**invalid_data)

    # Test nested validation
    invalid_data = data.copy()
    invalid_data["geometry"]["complexity_level"] = 11  # Invalid value
    with pytest.raises(ValidationError):
        VisualAspectSchema(**invalid_data)

    # Test nested optional fields
    minimal_data = {
        "governor_id": "TEST",
        "dimensional": {
            "base_form": "ETHEREAL",
            "form_description": "Test form",
            "dimensional_variations": {
                "etheric": "var1",
                "astral": "var2",
                "mental": "var3",
                "causal": "var4"
            }
        },
        "color_scheme": {
            "primary_colors": ["red"],
            "elemental_association": "fire",
            "intensity_levels": {"low": 1}
        },
        "geometry": {
            "pattern_type": ["MERKABA"],
            "complexity_level": 1,
            "interaction_points": [{"x": 0.0, "y": 0.0, "z": 0.0}],
            "power_requirements": {}
        },
        "environment": {
            "primary_effect": "test",
            "radius": 1.0,
            "duration": "1s",
            "intensity": "low"
        },
        "time_variation": {
            "astrological_influences": ["sun"],
            "cycle_description": "test",
            "peak_manifestation": "peak",
            "dormant_manifestation": "dormant"
        },
        "energy": {
            "frequency": "low",
            "polarity": "neutral",
            "intensity": "weak"
        },
        "symbols": {
            "sigils": [],
            "emblems": [],
            "seals": [],
            "scripts": []
        },
        "light_shadow": {
            "light_expression": "dim",
            "shadow_interaction": "weak",
            "balance_point": "neutral"
        },
        "scale": {
            "base_scale": "small",
            "plane_variations": {},
            "interaction_ranges": {"default": 1.0},
            "ritual_requirements": {}
        }
    }
    
    # Should validate without errors
    minimal_aspect = VisualAspectSchema(**minimal_data)
    assert minimal_aspect.governor_id == "TEST" 