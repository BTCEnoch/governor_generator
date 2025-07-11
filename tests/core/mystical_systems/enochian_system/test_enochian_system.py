"""
Tests for the Enochian Magic System
"""

import pytest
from typing import Dict, List, Any
from datetime import datetime

from core.mystical_systems.enochian_system import EnochianSystem
from core.mystical_systems.enochian_system.schemas import (
    EnochianSystemConfig,
    AethyrProfile,
    RitualPattern,
    Direction
)
from core.mystical_systems.enochian_system.ritual_mechanics import (
    RitualEngine,
    RitualPoint
)
from core.mystical_systems.enochian_system.relationships import (
    RelationshipEngine,
    GovernorConnection,
    ResonancePattern
)

@pytest.fixture
def config() -> Dict[str, Any]:
    """Test configuration"""
    return {
        "min_power": 1,
        "max_power": 10,
        "resonance_threshold": 0.7,
        "governor_influence": 1.0,
        "ritual_points_required": 3
    }

@pytest.fixture
def system(config: Dict[str, Any]) -> EnochianSystem:
    """Test Enochian system instance"""
    return EnochianSystem(config=config)

@pytest.fixture
def ritual_engine(config: Dict[str, Any]) -> RitualEngine:
    """Test ritual engine instance"""
    return RitualEngine(EnochianSystemConfig(**config))

@pytest.fixture
def relationship_engine(config: Dict[str, Any]) -> RelationshipEngine:
    """Test relationship engine instance"""
    return RelationshipEngine(EnochianSystemConfig(**config))

@pytest.mark.asyncio
async def test_system_initialization(system: EnochianSystem):
    """Test system initialization"""
    assert system is not None
    assert system.config is not None
    assert system.bitcoin is not None
    assert system.art_generator is not None
    assert system.ritual_engine is not None
    
    # Check data loading
    assert system.alphabet is not None
    assert len(system.alphabet) > 0
    assert system.aethyrs is not None
    assert len(system.aethyrs) == 30  # 30 Aethyrs
    assert all(direction in system.tables for direction in Direction)

@pytest.mark.asyncio
async def test_ritual_validation(ritual_engine: RitualEngine):
    """Test ritual point validation"""
    # Valid ritual points
    points = [
        RitualPoint(
            x=0.0,
            y=0.0,
            energy_level=1.0,
            element="fire",
            governor_influence="ABRIOND",
            aethyr_resonance="LIL"
        ),
        RitualPoint(
            x=1.0,
            y=0.0,
            energy_level=1.0,
            element="water",
            governor_influence="ADVORPT",
            aethyr_resonance="LIL"
        ),
        RitualPoint(
            x=0.5,
            y=0.866,
            energy_level=1.0,
            element="air",
            governor_influence=None,
            aethyr_resonance="LIL"
        )
    ]
    validation = ritual_engine.validate_ritual_points(points, 1)
    assert validation.is_valid
    assert not validation.errors
    
    # Invalid points (too few)
    validation = ritual_engine.validate_ritual_points([points[0]], 1)
    assert not validation.is_valid
    assert validation.errors is not None
    assert len(validation.errors) > 0
    
    # Invalid points (energy too high)
    invalid_points = [
        RitualPoint(
            x=0.0,
            y=0.0,
            energy_level=11.0,  # Invalid energy level
            element="fire",
            governor_influence="ABRIOND",
            aethyr_resonance="LIL"
        ),
        RitualPoint(
            x=1.0,
            y=0.0,
            energy_level=1.0,
            element="water",
            governor_influence="ADVORPT",
            aethyr_resonance="LIL"
        ),
        RitualPoint(
            x=0.5,
            y=0.866,
            energy_level=1.0,
            element="air",
            governor_influence=None,
            aethyr_resonance="LIL"
        )
    ]
    validation = ritual_engine.validate_ritual_points(invalid_points, 1)
    assert not validation.is_valid
    assert validation.errors is not None
    assert len(validation.errors) > 0

@pytest.mark.asyncio
async def test_energy_pattern_matching(ritual_engine: RitualEngine):
    """Test energy pattern matching"""
    # Triangle pattern
    triangle_points = [
        RitualPoint(
            x=0.0,
            y=0.0,
            energy_level=1.0,
            element="fire",
            governor_influence="ABRIOND",
            aethyr_resonance="LIL"
        ),
        RitualPoint(
            x=1.0,
            y=0.0,
            energy_level=1.0,
            element="water",
            governor_influence="ADVORPT",
            aethyr_resonance="LIL"
        ),
        RitualPoint(
            x=0.5,
            y=0.866,
            energy_level=1.0,
            element="air",
            governor_influence=None,
            aethyr_resonance="LIL"
        )
    ]
    pattern = ritual_engine.match_energy_pattern(triangle_points)
    assert pattern.pattern_type == "triangle"
    assert pattern.total_energy > 0
    
    # Square pattern
    square_points = [
        RitualPoint(
            x=0.0,
            y=0.0,
            energy_level=1.0,
            element="fire",
            governor_influence="ABRIOND",
            aethyr_resonance="LIL"
        ),
        RitualPoint(
            x=1.0,
            y=0.0,
            energy_level=1.0,
            element="water",
            governor_influence="ADVORPT",
            aethyr_resonance="LIL"
        ),
        RitualPoint(
            x=1.0,
            y=1.0,
            energy_level=1.0,
            element="air",
            governor_influence=None,
            aethyr_resonance="LIL"
        ),
        RitualPoint(
            x=0.0,
            y=1.0,
            energy_level=1.0,
            element="earth",
            governor_influence=None,
            aethyr_resonance="LIL"
        )
    ]
    pattern = ritual_engine.match_energy_pattern(square_points)
    assert pattern.pattern_type == "square"
    assert pattern.total_energy > 0

@pytest.mark.asyncio
async def test_governor_relationships(
    relationship_engine: RelationshipEngine,
    system: EnochianSystem
):
    """Test Governor relationship generation"""
    # Get test Aethyrs
    aethyrs = await system.get_all_aethyrs()
    assert len(aethyrs) > 0
    
    # Test with two Governors
    governors = ["ABRIOND", "ADVORPT"]
    profile = await relationship_engine.generate_relationship_profile(
        governors,
        aethyrs
    )
    
    assert profile is not None
    assert len(profile.connections) > 0
    assert len(profile.resonance_patterns) > 0
    assert len(profile.interaction_rules) > 0
    assert profile.visualization is not None
    assert profile.bitcoin_block_hash is not None
    
    # Verify connection properties
    for conn in profile.connections:
        assert conn.source_governor in governors
        assert conn.target_governor in governors
        assert 0 <= conn.strength <= 1
    
    # Verify pattern properties
    for pattern in profile.resonance_patterns:
        assert all(gov in governors for gov in pattern.governors)
        assert 0 <= pattern.intensity <= 1
    
    # Verify visualization
    assert profile.visualization.dimensions in [2, 3]
    assert len(profile.visualization.nodes) == len(governors)
    assert len(profile.visualization.edges) > 0

@pytest.mark.asyncio
async def test_art_generation(system: EnochianSystem, tmp_path):
    """Test ritual art generation"""
    # Create test profile data
    profile_data = {
        "connections": [
            {
                "source_governor": "ABRIOND",
                "target_governor": "ADVORPT",
                "source_x": 0.2,
                "source_y": 0.3,
                "target_x": 0.7,
                "target_y": 0.8,
                "strength": 0.9
            }
        ],
        "patterns": [
            {
                "governors": ["ABRIOND", "ADVORPT"],
                "intensity": 0.8
            }
        ],
        "visualization": {
            "nodes": {
                "ABRIOND": {"x": 0.2, "y": 0.3},
                "ADVORPT": {"x": 0.7, "y": 0.8}
            }
        },
        "bitcoin_block_hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
    }
    
    # Generate art
    output_path = str(tmp_path / "test_art.json")
    art_path = await system.generate_ritual_art(profile_data, output_path)
    
    assert art_path is not None
    assert art_path.endswith(".json")
    assert art_path.startswith(str(tmp_path)) 