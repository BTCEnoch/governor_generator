"""
Tests for Visual Aspect Generator
"""

import pytest
from core.governors.visual_aspects.generator import (
    GovernorTraits,
    VisualAspectGenerator
)
from core.governors.visual_aspects.schemas.visual_aspect_schema import (
    AspectScale,
    AspectDimension,
    AspectMotion
)

def create_test_traits() -> GovernorTraits:
    """Create test governor traits"""
    return GovernorTraits(
        name="OCCODON",
        aethyrs=["LIL", "ARN"],
        elements=["fire", "air"],
        traditions=["enochian_magic", "kabbalah"],
        personality_traits=["dynamic", "harmonious"],
        mystical_domains=["cosmic", "light", "geometry"]
    )

def test_governor_traits():
    """Test governor traits creation"""
    traits = create_test_traits()
    assert traits.name == "OCCODON"
    assert "LIL" in traits.aethyrs
    assert "fire" in traits.elements
    assert "enochian_magic" in traits.traditions
    assert "dynamic" in traits.personality_traits
    assert "cosmic" in traits.mystical_domains

def test_scale_determination():
    """Test scale determination based on traits"""
    generator = VisualAspectGenerator()
    traits = create_test_traits()
    
    # Test cosmic scale
    assert generator._determine_scale(traits) == AspectScale.COSMIC
    
    # Test micro scale
    traits.mystical_domains = ["quantum", "atomic"]
    assert generator._determine_scale(traits) == AspectScale.MICRO
    
    # Test transcendent scale
    traits.mystical_domains = ["transcendent"]
    assert generator._determine_scale(traits) == AspectScale.TRANSCENDENT
    
    # Test default human scale
    traits.mystical_domains = ["nature"]
    assert generator._determine_scale(traits) == AspectScale.HUMAN

def test_dimension_determination():
    """Test dimension determination based on traits"""
    generator = VisualAspectGenerator()
    traits = create_test_traits()
    
    dimensions = generator._determine_dimensions(traits)
    assert AspectDimension.VOLUME in dimensions  # From geometry
    assert AspectDimension.LINE in dimensions    # From light
    
    # Test nature domain
    traits.mystical_domains = ["nature"]
    dimensions = generator._determine_dimensions(traits)
    assert AspectDimension.FRACTAL in dimensions
    
    # Test spirit domain
    traits.mystical_domains = ["spirit"]
    dimensions = generator._determine_dimensions(traits)
    assert AspectDimension.HYPERCUBE in dimensions

def test_motion_determination():
    """Test motion determination based on traits"""
    generator = VisualAspectGenerator()
    traits = create_test_traits()
    
    motions = generator._determine_motions(traits)
    assert AspectMotion.CHAOTIC in motions      # From dynamic
    assert AspectMotion.HARMONIC in motions     # From harmonious
    
    # Test cyclical trait
    traits.personality_traits = ["cyclical"]
    motions = generator._determine_motions(traits)
    assert AspectMotion.PERIODIC in motions
    
    # Test transformative trait
    traits.personality_traits = ["transformative"]
    motions = generator._determine_motions(traits)
    assert AspectMotion.SPIRAL in motions
    
    # Test default static motion
    traits.personality_traits = ["stable"]
    motions = generator._determine_motions(traits)
    assert AspectMotion.STATIC in motions

def test_color_selection():
    """Test color selection based on traits"""
    generator = VisualAspectGenerator()
    traits = create_test_traits()
    
    colors = generator._select_colors(traits)
    assert len(colors) >= 2  # Should have fire and air colors
    assert any(c.elemental_association == "fire" for c in colors)
    assert any(c.elemental_association == "air" for c in colors)
    
    # Test default spirit color
    traits.elements = []
    colors = generator._select_colors(traits)
    assert len(colors) == 1
    assert colors[0].elemental_association == "spirit"

def test_pattern_selection():
    """Test pattern selection based on traits"""
    generator = VisualAspectGenerator()
    traits = create_test_traits()
    
    patterns = generator._select_patterns(traits)
    assert len(patterns) >= 2  # Should have LIL and ARN patterns
    assert any("LIL" in p.aethyr_influence for p in patterns)
    assert any("ARN" in p.aethyr_influence for p in patterns)
    
    # Test default LIL pattern
    traits.aethyrs = []
    patterns = generator._select_patterns(traits)
    assert len(patterns) == 1
    assert "LIL" in patterns[0].aethyr_influence

def test_form_selection():
    """Test form selection based on traits"""
    generator = VisualAspectGenerator()
    traits = create_test_traits()
    
    primary, secondary = generator._select_forms(traits)
    assert primary is not None
    assert primary.name == "RADIANT_SYMBOLIC"  # Fire element maps to RADIANT_SYMBOLIC
    
    if secondary:
        assert secondary.name == "ETHEREAL_METAMORPHIC"  # Air element maps to ETHEREAL_METAMORPHIC
        
    # Test no elements
    traits.elements = []
    primary, secondary = generator._select_forms(traits)
    assert primary is None
    assert secondary is None

def test_aspect_generation():
    """Test complete aspect generation"""
    generator = VisualAspectGenerator()
    traits = create_test_traits()
    
    try:
        aspect = generator.generate_aspect(traits)
        assert aspect.governor_name == traits.name
        assert aspect.primary_form is not None
        assert len(aspect.colors) >= 2
        assert len(aspect.patterns) >= 2
        assert aspect.scale == AspectScale.COSMIC
        assert len(aspect.dimensions) >= 2
        assert len(aspect.motions) >= 2
    except ValueError as e:
        pytest.fail(f"Failed to generate valid aspect: {str(e)}")

def test_batch_generation():
    """Test batch aspect generation"""
    generator = VisualAspectGenerator()
    traits_list = [
        create_test_traits(),
        GovernorTraits(
            name="PASCOMB",
            aethyrs=["ZOM"],
            elements=["water", "earth"],
            traditions=["enochian_magic"],
            personality_traits=["cyclical"],
            mystical_domains=["nature"]
        )
    ]
    
    aspects = generator.generate_aspects_batch(traits_list)
    assert len(aspects) == 2
    assert "OCCODON" in aspects
    assert "PASCOMB" in aspects
    
    # Verify PASCOMB's specific traits are reflected
    pascomb = aspects["PASCOMB"]
    assert pascomb.scale == AspectScale.HUMAN
    assert AspectDimension.FRACTAL in pascomb.dimensions
    assert AspectMotion.PERIODIC in pascomb.motions 