"""
Tests for Visual Aspect Schema
"""

import pytest
from core.governors.visual_aspects.schemas.visual_aspect_schema import (
    AspectScale,
    AspectDimension,
    AspectMotion,
    ColorDefinition,
    PatternDefinition,
    VisualAspect,
    VisualAspectValidator
)
from core.governors.visual_aspects.catalogs.form_types import (
    BaseFormType,
    FormDefinition,
    InteractionType
)

def create_test_color() -> ColorDefinition:
    """Create a test color definition"""
    return ColorDefinition(
        name="Celestial Blue",
        rgb=(64, 128, 255),
        alpha=0.8,
        tradition_meaning="Divine Wisdom",
        elemental_association="Air"
    )

def create_test_pattern() -> PatternDefinition:
    """Create a test pattern definition"""
    return PatternDefinition(
        name="Sacred Pentagram",
        base_geometry="Five-pointed star",
        repetition_type="Fractal",
        sacred_meaning="Divine Protection",
        aethyr_influence=["LIL", "ARN"]
    )

def create_test_form() -> FormDefinition:
    """Create a test form definition"""
    return FormDefinition(
        name="TEST_FORM",
        base_type=BaseFormType.FLUID,
        description="Test form",
        valid_interactions={InteractionType.FLOWING},
        tradition_origins=["enochian_magic"],
        elemental_affinities=["water"],
        aethyr_resonance=["LIL"]
    )

def test_color_validation():
    """Test color definition validation"""
    # Test valid color
    valid_color = create_test_color()
    assert VisualAspectValidator.validate_color(valid_color)

    # Test invalid RGB values
    invalid_color = ColorDefinition(
        name="Invalid",
        rgb=(300, -1, 128),
        alpha=0.5,
        tradition_meaning="Test",
        elemental_association="Fire"
    )
    assert not VisualAspectValidator.validate_color(invalid_color)

    # Test invalid alpha
    invalid_alpha = ColorDefinition(
        name="Invalid",
        rgb=(128, 128, 128),
        alpha=2.0,
        tradition_meaning="Test",
        elemental_association="Fire"
    )
    assert not VisualAspectValidator.validate_color(invalid_alpha)

def test_pattern_validation():
    """Test pattern definition validation"""
    # Test valid pattern
    valid_pattern = create_test_pattern()
    assert VisualAspectValidator.validate_pattern(valid_pattern)

    # Test invalid pattern (missing name)
    invalid_pattern = PatternDefinition(
        name="",
        base_geometry="Circle",
        repetition_type="Linear",
        sacred_meaning="Test",
        aethyr_influence=["LIL"]
    )
    assert not VisualAspectValidator.validate_pattern(invalid_pattern)

    # Test invalid pattern (no aethyr influence)
    invalid_pattern = PatternDefinition(
        name="Test Pattern",
        base_geometry="Circle",
        repetition_type="Linear",
        sacred_meaning="Test",
        aethyr_influence=[]
    )
    assert not VisualAspectValidator.validate_pattern(invalid_pattern)

def test_visual_aspect_validation():
    """Test complete visual aspect validation"""
    # Create valid visual aspect
    valid_aspect = VisualAspect(
        governor_name="OCCODON",
        primary_form=create_test_form(),
        secondary_form=None,
        scale=AspectScale.HUMAN,
        dimensions={AspectDimension.VOLUME},
        motions={AspectMotion.HARMONIC},
        colors=[create_test_color()],
        patterns=[create_test_pattern()],
        aethyr_resonances=["LIL", "ARN"],
        elemental_influences=["water", "air"],
        tradition_alignments=["enochian_magic"]
    )
    assert VisualAspectValidator.validate_aspect(valid_aspect)

    # Test invalid aspect (no primary form)
    invalid_aspect = VisualAspect(
        governor_name="INVALID",
        primary_form=None,
        secondary_form=None,
        scale=AspectScale.HUMAN,
        dimensions={AspectDimension.VOLUME},
        motions={AspectMotion.HARMONIC},
        colors=[create_test_color()],
        patterns=[create_test_pattern()],
        aethyr_resonances=["LIL"],
        elemental_influences=["water"],
        tradition_alignments=["enochian_magic"]
    )
    assert not VisualAspectValidator.validate_aspect(invalid_aspect)

def test_aspect_combination():
    """Test visual aspect combination validation"""
    aspect1 = VisualAspect(
        governor_name="TEST1",
        primary_form=create_test_form(),
        secondary_form=None,
        scale=AspectScale.MICRO,
        dimensions={AspectDimension.POINT},
        motions={AspectMotion.STATIC},
        colors=[create_test_color()],
        patterns=[create_test_pattern()],
        aethyr_resonances=["LIL"],
        elemental_influences=["water"],
        tradition_alignments=["enochian_magic"]
    )

    aspect2 = VisualAspect(
        governor_name="TEST2",
        primary_form=create_test_form(),
        secondary_form=None,
        scale=AspectScale.COSMIC,
        dimensions={AspectDimension.VOLUME},
        motions={AspectMotion.HARMONIC},
        colors=[create_test_color()],
        patterns=[create_test_pattern()],
        aethyr_resonances=["ARN"],
        elemental_influences=["air"],
        tradition_alignments=["kabbalah"]
    )

    # Test valid combination
    assert VisualAspectValidator.validate_aspect_combination(aspect1, aspect2)

    # Test invalid combination (same scale)
    aspect2.scale = AspectScale.MICRO
    assert not VisualAspectValidator.validate_aspect_combination(aspect1, aspect2)

    # Test invalid combination (overlapping dimensions)
    aspect2.scale = AspectScale.COSMIC
    aspect2.dimensions = {AspectDimension.POINT}
    assert not VisualAspectValidator.validate_aspect_combination(aspect1, aspect2)

    # Test invalid combination (overlapping motions)
    aspect2.dimensions = {AspectDimension.VOLUME}
    aspect2.motions = {AspectMotion.STATIC}
    assert not VisualAspectValidator.validate_aspect_combination(aspect1, aspect2) 