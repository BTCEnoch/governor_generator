"""
Tests for the Form Types Catalog
"""

import pytest
from core.governors.visual_aspects.catalogs.form_types import (
    BaseFormType,
    InteractionType,
    FormDefinition,
    FormCombinationRules,
    FormTypeRegistry
)

def test_base_form_types():
    """Test that all base form types are properly defined"""
    assert len(BaseFormType) == 10
    assert BaseFormType.FLUID.name == "FLUID"
    assert BaseFormType.CRYSTALLINE.name == "CRYSTALLINE"
    assert BaseFormType.RADIANT.name == "RADIANT"

def test_interaction_types():
    """Test that all interaction types are properly defined"""
    assert len(InteractionType) == 10
    assert InteractionType.EMANATING.name == "EMANATING"
    assert InteractionType.ABSORBING.name == "ABSORBING"
    assert InteractionType.REFLECTING.name == "REFLECTING"

def test_form_combination_rules():
    """Test form combination validation"""
    # Test valid combinations
    assert FormCombinationRules.can_combine(BaseFormType.FLUID, BaseFormType.ETHEREAL)
    assert FormCombinationRules.can_combine(BaseFormType.CRYSTALLINE, BaseFormType.PRISMATIC)
    
    # Test invalid combinations
    assert not FormCombinationRules.can_combine(BaseFormType.FLUID, BaseFormType.CRYSTALLINE)
    assert not FormCombinationRules.can_combine(BaseFormType.RADIANT, BaseFormType.ORGANIC)

def test_form_definition():
    """Test form definition creation and validation"""
    form = FormDefinition(
        name="TEST_FORM",
        base_type=BaseFormType.FLUID,
        description="Test form description",
        valid_interactions={InteractionType.FLOWING, InteractionType.RESONATING},
        tradition_origins=["enochian_magic"],
        elemental_affinities=["water"],
        aethyr_resonance=["LIL"]
    )
    
    assert form.name == "TEST_FORM"
    assert form.base_type == BaseFormType.FLUID
    assert len(form.valid_interactions) == 2
    assert "enochian_magic" in form.tradition_origins

def test_form_registry():
    """Test form registry loading and validation"""
    registry = FormTypeRegistry()
    
    # Test loading predefined forms
    fluid_crystalline = registry.get_form("FLUID_CRYSTALLINE")
    assert fluid_crystalline is not None
    assert fluid_crystalline.base_type == BaseFormType.FLUID
    
    # Test form combination validation
    assert registry.validate_form_combination("FLUID_CRYSTALLINE", "ETHEREAL_METAMORPHIC")
    assert not registry.validate_form_combination("FLUID_CRYSTALLINE", "RADIANT_SYMBOLIC")

def test_form_traditions():
    """Test tradition origins validation"""
    registry = FormTypeRegistry()
    fluid_crystalline = registry.get_form("FLUID_CRYSTALLINE")
    assert fluid_crystalline is not None, "FLUID_CRYSTALLINE form should exist"
    
    assert "enochian_magic" in fluid_crystalline.tradition_origins
    assert "hermetic_alchemy" in fluid_crystalline.tradition_origins
    assert "egyptian_magic" in fluid_crystalline.tradition_origins

def test_form_elements():
    """Test elemental affinities validation"""
    registry = FormTypeRegistry()
    fluid_crystalline = registry.get_form("FLUID_CRYSTALLINE")
    assert fluid_crystalline is not None, "FLUID_CRYSTALLINE form should exist"
    
    assert "water" in fluid_crystalline.elemental_affinities
    assert "aether" in fluid_crystalline.elemental_affinities

def test_form_aethyrs():
    """Test aethyr resonance validation"""
    registry = FormTypeRegistry()
    fluid_crystalline = registry.get_form("FLUID_CRYSTALLINE")
    assert fluid_crystalline is not None, "FLUID_CRYSTALLINE form should exist"
    
    assert "LIL" in fluid_crystalline.aethyr_resonance
    assert "ARN" in fluid_crystalline.aethyr_resonance
    assert "ZOM" in fluid_crystalline.aethyr_resonance

def test_invalid_forms():
    """Test handling of invalid form requests"""
    registry = FormTypeRegistry()
    
    assert registry.get_form("NONEXISTENT_FORM") is None
    assert not registry.validate_form_combination("INVALID_FORM_1", "INVALID_FORM_2") 