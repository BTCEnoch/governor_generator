"""Tests for the visual aspects base classes."""

import pytest
from datetime import datetime
from core.game_assets.visual_aspects.base import (
    FormType,
    ColorScheme,
    GeometryPattern,
    Point,
    Effect,
    PlayerState,
    DimensionalManifestation,
    VisualColorScheme,
    GeometrySystem,
    EnvironmentalEffect,
    TimeVariation,
    EnergySignature,
    SymbolSet,
    LightShadowDynamics,
    ScaleSystem,
    VisualAspectSystem
)

def test_point():
    """Test Point dataclass"""
    point = Point(1.0, 2.0, 3.0)
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 3.0

def test_effect():
    """Test Effect dataclass"""
    effect = Effect("test", 1.0, 60.0, 10.0)
    assert effect.type == "test"
    assert effect.intensity == 1.0
    assert effect.duration == 60.0
    assert effect.radius == 10.0

def test_player_state():
    """Test PlayerState dataclass"""
    pos = Point(0.0, 0.0, 0.0)
    effect = Effect("test", 1.0, 60.0, 10.0)
    state = PlayerState(
        reputation=10,
        energy=100,
        position=pos,
        active_effects=[effect],
        inventory=["item1"],
        completed_quests=["quest1"]
    )
    assert state.reputation == 10
    assert state.energy == 100
    assert state.position == pos
    assert len(state.active_effects) == 1
    assert state.active_effects[0] == effect
    assert state.inventory == ["item1"]
    assert state.completed_quests == ["quest1"]

def test_dimensional_manifestation():
    """Test DimensionalManifestation class"""
    manifest = DimensionalManifestation(
        base_form=FormType.ETHEREAL,
        form_description="Test form",
        dimensional_variations={
            "etheric": "var1",
            "astral": "var2",
            "mental": "var3",
            "causal": "var4"
        },
        transition_effects=["effect1"],
        constant_elements=["element1"]
    )
    assert manifest.validate() is True
    assert manifest.base_form == FormType.ETHEREAL
    assert len(manifest.dimensional_variations) == 4
    assert "etheric" in manifest.dimensional_variations

def test_visual_color_scheme():
    """Test VisualColorScheme class"""
    scheme = VisualColorScheme(
        primary_colors=["red", "blue"],
        elemental_association="fire",
        intensity_levels={"low": 1, "high": 2},
        transition_effects=["fade"]
    )
    state = PlayerState(
        reputation=15,
        energy=100,
        position=Point(0.0, 0.0, 0.0),
        active_effects=[],
        inventory=[],
        completed_quests=[]
    )
    assert scheme.get_color_for_state(state) == "blue"

def test_geometry_system():
    """Test GeometrySystem class"""
    system = GeometrySystem(
        pattern_type=[GeometryPattern.MERKABA],
        complexity_level=1,
        interaction_points=[Point(0.0, 0.0, 0.0)],
        power_requirements={"req1": 10}
    )
    assert system.validate_ritual_pattern([Point(0.0, 0.0, 0.0)]) is False

def test_environmental_effect():
    """Test EnvironmentalEffect class"""
    effect = EnvironmentalEffect(
        primary_effect="test",
        radius=10.0,
        duration="60s",
        intensity="high",
        secondary_effects=["effect1"]
    )
    effects = effect.apply_to_position(
        Point(0.0, 0.0, 0.0),
        Point(1.0, 1.0, 1.0)
    )
    assert isinstance(effects, list)
    assert len(effects) == 0

def test_time_variation():
    """Test TimeVariation class"""
    variation = TimeVariation(
        astrological_influences=["moon"],
        cycle_description="test cycle",
        peak_manifestation="peak",
        dormant_manifestation="dormant"
    )
    assert variation.is_available(datetime.now()) is True

def test_energy_signature():
    """Test EnergySignature class"""
    signature = EnergySignature(
        frequency="high",
        polarity="positive",
        intensity="strong",
        special_properties=["prop1"]
    )
    state = PlayerState(
        reputation=10,
        energy=100,
        position=Point(0.0, 0.0, 0.0),
        active_effects=[],
        inventory=[],
        completed_quests=[]
    )
    assert signature.calculate_resonance(state) == 0.0

def test_symbol_set():
    """Test SymbolSet class"""
    symbols = SymbolSet(
        sigils=["sigil1"],
        emblems=["emblem1"],
        seals=["seal1"],
        scripts=["script1"]
    )
    assert symbols.validate_sequence(["sigil1"]) is False

def test_light_shadow_dynamics():
    """Test LightShadowDynamics class"""
    dynamics = LightShadowDynamics(
        light_expression="bright",
        shadow_interaction="dark",
        balance_point="medium",
        special_effects=["effect1"]
    )
    assert dynamics.calculate_visibility(0.5) == 0.0

def test_scale_system():
    """Test ScaleSystem class"""
    system = ScaleSystem(
        base_scale="medium",
        plane_variations={"plane1": "large"},
        interaction_ranges={"range1": 10.0},
        ritual_requirements={"req1": "large"}
    )
    assert system.get_scale_for_plane("plane1") == 1.0

def test_visual_aspect_system():
    """Test VisualAspectSystem class"""
    system = VisualAspectSystem("test_governor")
    
    # Test initialization
    assert system.governor_id == "test_governor"
    assert isinstance(system.dimensional, DimensionalManifestation)
    assert isinstance(system.color_scheme, VisualColorScheme)
    assert isinstance(system.geometry, GeometrySystem)
    assert isinstance(system.environment, EnvironmentalEffect)
    assert isinstance(system.time_variation, TimeVariation)
    assert isinstance(system.energy, EnergySignature)
    assert isinstance(system.symbols, SymbolSet)
    assert isinstance(system.light_shadow, LightShadowDynamics)
    assert isinstance(system.scale, ScaleSystem)

    # Test methods
    assert system.validate_ritual_requirements("test") is False
    assert system.get_puzzle_parameters("test") == {}
    assert system.apply_environmental_effects(Point(0.0, 0.0, 0.0)) == []
    assert system.check_interaction_availability(
        datetime.now(),
        PlayerState(
            reputation=10,
            energy=100,
            position=Point(0.0, 0.0, 0.0),
            active_effects=[],
            inventory=[],
            completed_quests=[]
        )
    ) is False

    # Test serialization
    data = system.to_dict()
    assert isinstance(data, dict)
    assert "governor_id" in data
    assert data["governor_id"] == "test_governor"

    # Test deserialization
    new_system = VisualAspectSystem.from_dict(data)
    assert new_system.governor_id == system.governor_id 