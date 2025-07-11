"""
Tests for the Sacred Geometry System
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from core.mystical_systems.sacred_geometry_system import SacredGeometrySystem
from core.mystical_systems.sacred_geometry_system.schemas import (
    GeometricForm,
    GeometryPattern,
    SacredGeometryProfile,
    SacredGeometrySystemConfig,
    SacredProportion
)
from pydantic import ValidationError

@pytest.fixture
def mock_bitcoin():
    """Mock Bitcoin integration"""
    with patch("core.utils.mystical.BitcoinIntegration") as mock:
        mock_instance = Mock()
        mock_instance.generate_number.return_value = 5
        mock_instance.get_latest_block_hash.return_value = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_art_generator():
    """Mock art generator"""
    with patch("core.utils.mystical.bitcoin_integration.BitcoinArtGenerator") as mock:
        mock_instance = Mock()
        mock_instance.generate_sacred_geometry.return_value = "test_output.png"
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def system(mock_bitcoin, mock_art_generator):
    """Create a Sacred Geometry system instance"""
    config = {
        "min_complexity": 1,
        "max_complexity": 10,
        "resonance_threshold": 0.7,
        "power_scale": 100,
        "ritual_points_required": 3
    }
    return SacredGeometrySystem(config)

async def test_generate_profile(system):
    """Test generating a sacred geometry profile"""
    profile = await system.generate_profile()
    
    assert isinstance(profile, SacredGeometryProfile)
    assert isinstance(profile.primary_form, GeometricForm)
    assert len(profile.secondary_forms) >= 2
    assert len(profile.patterns) >= 1
    assert isinstance(profile.dominant_proportion, SacredProportion)
    assert len(profile.power_centers) >= 1
    assert 0 <= profile.resonance_score <= 1
    assert 1 <= profile.ritual_complexity <= 10
    assert 0 <= profile.governor_alignment <= 1
    assert profile.bitcoin_block_hash

async def test_generate_art(system):
    """Test generating sacred geometry art"""
    profile = await system.generate_profile()
    output_path = await system.generate_art(profile, "test_output.png")
    assert output_path == "test_output.png"

def test_calculate_resonance(system):
    """Test resonance calculation"""
    resonance = system._calculate_resonance(
        GeometricForm.CIRCLE,
        "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
    )
    assert 0 <= resonance <= 1

def test_generate_ritual_points(system):
    """Test ritual point generation"""
    points = system._generate_ritual_points(
        GeometricForm.TRIANGLE,
        5,
        "test_seed"
    )
    assert len(points) == min(5 * 2, 12)
    for point in points:
        assert "x" in point
        assert "y" in point
        assert "z" in point
        assert -1 <= point["x"] <= 1
        assert -1 <= point["y"] <= 1
        assert -1 <= point["z"] <= 1

def test_generate_pattern(system):
    """Test pattern generation"""
    pattern = system._generate_pattern(
        GeometricForm.HEXAGON,
        "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
        5
    )
    assert isinstance(pattern, GeometryPattern)
    assert pattern.form == GeometricForm.HEXAGON
    assert len(pattern.proportions) >= 1
    assert 1 <= pattern.complexity <= 10
    assert 0 <= pattern.dimensions <= 3
    assert pattern.symmetry_order > 0
    assert len(pattern.ritual_points) > 0
    assert 1 <= pattern.power_level <= 100
    assert 0 <= pattern.resonance <= 1

def test_validate_ritual_pattern(system):
    """Test ritual pattern validation"""
    # Create a test pattern
    pattern = system._generate_pattern(
        GeometricForm.TRIANGLE,
        "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
        3
    )
    
    # Test with exact points
    assert system.validate_ritual_pattern(
        pattern.ritual_points,
        pattern
    )
    
    # Test with slightly offset points
    offset_points = []
    for point in pattern.ritual_points:
        offset_point = point.copy()
        offset_point["x"] += 0.05  # Small offset within tolerance
        offset_points.append(offset_point)
    
    assert system.validate_ritual_pattern(
        offset_points,
        pattern
    )
    
    # Test with points outside tolerance
    invalid_points = []
    for point in pattern.ritual_points:
        invalid_point = point.copy()
        invalid_point["x"] += 0.5  # Large offset outside tolerance
        invalid_points.append(invalid_point)
    
    assert not system.validate_ritual_pattern(
        invalid_points,
        pattern
    )

def test_system_config():
    """Test system configuration"""
    config = SacredGeometrySystemConfig(
        min_complexity=1,
        max_complexity=10,
        resonance_threshold=0.7,
        power_scale=100,
        ritual_points_required=3
    )
    
    assert config.min_complexity == 1
    assert config.max_complexity == 10
    assert config.resonance_threshold == 0.7
    assert config.power_scale == 100
    assert config.ritual_points_required == 3

def test_invalid_config():
    """Test invalid configuration handling"""
    with pytest.raises(ValidationError):
        SacredGeometrySystemConfig(
            min_complexity=0,  # Invalid: must be >= 1
            max_complexity=10,
            resonance_threshold=0.7,
            power_scale=100,
            ritual_points_required=3
        )
    
    with pytest.raises(ValidationError):
        SacredGeometrySystemConfig(
            min_complexity=1,
            max_complexity=11,  # Invalid: must be <= 10
            resonance_threshold=0.7,
            power_scale=100,
            ritual_points_required=3
        ) 