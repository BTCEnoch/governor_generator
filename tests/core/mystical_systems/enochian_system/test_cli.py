"""
Tests for the Enochian System CLI
"""

import json
import pytest
from pathlib import Path
from click.testing import CliRunner

from core.mystical_systems.enochian_system.cli import cli

@pytest.fixture
def runner():
    """Test CLI runner"""
    return CliRunner()

@pytest.fixture
def config_file(tmp_path):
    """Create test config file"""
    config = {
        "min_power": 1,
        "max_power": 10,
        "resonance_threshold": 0.7,
        "governor_influence": 1.0,
        "ritual_points_required": 3
    }
    config_path = tmp_path / "test_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f)
    return str(config_path)

@pytest.fixture
def ritual_points_file(tmp_path):
    """Create test ritual points file"""
    points = {
        "points": [
            {
                "x": 0.0,
                "y": 0.0,
                "energy_level": 1.0,
                "element": "fire",
                "governor_influence": "ABRIOND",
                "aethyr_resonance": "LIL"
            },
            {
                "x": 1.0,
                "y": 0.0,
                "energy_level": 1.0,
                "element": "water",
                "governor_influence": "ADVORPT",
                "aethyr_resonance": "LIL"
            },
            {
                "x": 0.5,
                "y": 0.866,
                "energy_level": 1.0,
                "element": "air",
                "governor_influence": None,
                "aethyr_resonance": "LIL"
            }
        ],
        "required_power": 1,
        "aethyr": "LIL",
        "active_governors": ["ABRIOND", "ADVORPT"]
    }
    points_path = tmp_path / "test_points.json"
    with open(points_path, "w") as f:
        json.dump(points, f)
    return str(points_path)

@pytest.fixture
def profile_file(tmp_path):
    """Create test relationship profile file"""
    profile = {
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
    profile_path = tmp_path / "test_profile.json"
    with open(profile_path, "w") as f:
        json.dump(profile, f)
    return str(profile_path)

def test_analyze_relationships(runner, config_file):
    """Test analyze_relationships command"""
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "analyze-relationships",
                "--config", config_file,
                "--output", "relationships.json",
                "ABRIOND", "ADVORPT"
            ]
        )
        assert result.exit_code == 0
        assert Path("relationships.json").exists()
        
        # Verify output structure
        with open("relationships.json") as f:
            data = json.load(f)
        assert "governors" in data
        assert "connections" in data
        assert "patterns" in data
        assert "rules" in data
        assert "visualization" in data
        assert "bitcoin_verification" in data

def test_validate_ritual(runner, config_file, ritual_points_file):
    """Test validate_ritual command"""
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "validate-ritual",
                "--config", config_file,
                "--output", "validation.json",
                ritual_points_file
            ]
        )
        assert result.exit_code == 0
        assert Path("validation.json").exists()
        
        # Verify output structure
        with open("validation.json") as f:
            data = json.load(f)
        assert "validation" in data
        assert "pattern" in data
        assert "resonance" in data
        assert data["validation"]["is_valid"]

def test_generate_art(runner, config_file, profile_file):
    """Test generate_art command"""
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "generate-art",
                "--config", config_file,
                "--output", "art.json",
                profile_file
            ]
        )
        assert result.exit_code == 0
        assert Path("art.json").exists()
        assert "art.json" in result.output

def test_invalid_config(runner, tmp_path):
    """Test CLI with invalid config"""
    config = {
        "min_power": -1,  # Invalid value
        "max_power": 10,
        "resonance_threshold": 0.7,
        "governor_influence": 1.0,
        "ritual_points_required": 3
    }
    config_path = tmp_path / "invalid_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f)
    
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "analyze-relationships",
                "--config", str(config_path),
                "ABRIOND", "ADVORPT"
            ]
        )
        assert result.exit_code != 0
        assert "error" in result.output.lower()

def test_invalid_ritual_points(runner, config_file):
    """Test CLI with invalid ritual points"""
    points = {
        "points": [
            {
                "x": 0.0,
                "y": 0.0,
                "energy_level": 11.0,  # Invalid energy level
                "element": "fire",
                "governor_influence": "ABRIOND",
                "aethyr_resonance": "LIL"
            }
        ]
    }
    
    with runner.isolated_filesystem():
        points_path = "invalid_points.json"
        with open(points_path, "w") as f:
            json.dump(points, f)
        
        result = runner.invoke(
            cli,
            [
                "validate-ritual",
                "--config", config_file,
                points_path
            ]
        )
        assert result.exit_code != 0
        assert "error" in result.output.lower()

def test_invalid_profile(runner, config_file):
    """Test CLI with invalid profile"""
    profile = {
        "connections": [],  # Missing required connections
        "patterns": [],
        "visualization": {}
    }
    
    with runner.isolated_filesystem():
        profile_path = "invalid_profile.json"
        with open(profile_path, "w") as f:
            json.dump(profile, f)
        
        result = runner.invoke(
            cli,
            [
                "generate-art",
                "--config", config_file,
                profile_path
            ]
        )
        assert result.exit_code != 0
        assert "error" in result.output.lower() 