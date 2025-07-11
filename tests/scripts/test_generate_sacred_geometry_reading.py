"""
Tests for Sacred Geometry Reading Generator CLI
"""

import json
import os
import pytest
from unittest.mock import Mock, patch, AsyncMock

from scripts.generate_sacred_geometry_reading import (
    parse_args,
    load_config,
    save_reading,
    main
)

@pytest.fixture
def mock_system():
    """Mock Sacred Geometry system"""
    with patch("scripts.generate_sacred_geometry_reading.SacredGeometrySystem") as mock:
        mock_instance = Mock()
        mock_instance.generate_profile = AsyncMock(return_value={
            "primary_form": "hexagon",
            "secondary_forms": ["triangle", "circle"],
            "patterns": [],
            "dominant_proportion": "phi",
            "power_centers": [],
            "resonance_score": 0.8,
            "ritual_complexity": 5,
            "governor_alignment": 0.7,
            "timestamp": "2024-01-01T00:00:00Z",
            "bitcoin_block_hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
        })
        mock_instance.format_output.return_value = {
            "primary_form": "hexagon",
            "primary_form_data": {
                "name": "Hexagon",
                "symbolism": "Harmony, Balance, Communication"
            }
        }
        mock_instance.generate_art = AsyncMock(return_value="test_art.png")
        mock.return_value = mock_instance
        yield mock_instance

def test_parse_args():
    """Test argument parsing"""
    with patch("sys.argv", ["script.py", "--complexity", "5"]):
        args = parse_args()
        assert args.complexity == 5
        assert args.txid is None
        assert args.output == "sacred_geometry_reading.json"
        assert args.art_output is None
        assert args.config is None

def test_load_config_default():
    """Test loading default configuration"""
    config = load_config()
    assert config["min_complexity"] == 1
    assert config["max_complexity"] == 10
    assert config["resonance_threshold"] == 0.7
    assert config["power_scale"] == 100
    assert config["ritual_points_required"] == 3

def test_load_config_custom(tmp_path):
    """Test loading custom configuration"""
    config_path = tmp_path / "config.json"
    custom_config = {
        "min_complexity": 2,
        "max_complexity": 8,
        "resonance_threshold": 0.8,
        "power_scale": 50,
        "ritual_points_required": 4
    }
    
    with open(config_path, "w") as f:
        json.dump(custom_config, f)
    
    loaded_config = load_config(str(config_path))
    assert loaded_config == custom_config

def test_save_reading(tmp_path):
    """Test saving reading to file"""
    output_path = tmp_path / "output" / "reading.json"
    reading = {"test": "data"}
    
    save_reading(reading, str(output_path))
    
    assert output_path.exists()
    with open(output_path) as f:
        loaded = json.load(f)
        assert loaded == reading

@pytest.mark.asyncio
async def test_main_basic(mock_system, tmp_path):
    """Test basic main functionality"""
    output_path = tmp_path / "reading.json"
    
    with patch("sys.argv", [
        "script.py",
        "--complexity", "5",
        "--output", str(output_path)
    ]):
        await main()
    
    assert output_path.exists()
    mock_system.generate_profile.assert_called_once_with(
        txid=None,
        complexity=5
    )
    mock_system.format_output.assert_called_once()

@pytest.mark.asyncio
async def test_main_with_art(mock_system, tmp_path):
    """Test main functionality with art generation"""
    output_path = tmp_path / "reading.json"
    art_path = tmp_path / "art.png"
    
    with patch("sys.argv", [
        "script.py",
        "--complexity", "5",
        "--output", str(output_path),
        "--art-output", str(art_path)
    ]):
        await main()
    
    assert output_path.exists()
    mock_system.generate_art.assert_called_once()

@pytest.mark.asyncio
async def test_main_with_config(mock_system, tmp_path):
    """Test main functionality with custom config"""
    output_path = tmp_path / "reading.json"
    config_path = tmp_path / "config.json"
    
    config = {
        "min_complexity": 2,
        "max_complexity": 8,
        "resonance_threshold": 0.8,
        "power_scale": 50,
        "ritual_points_required": 4
    }
    
    with open(config_path, "w") as f:
        json.dump(config, f)
    
    with patch("sys.argv", [
        "script.py",
        "--complexity", "5",
        "--output", str(output_path),
        "--config", str(config_path)
    ]):
        await main()
    
    assert output_path.exists()
    mock_system.assert_called_once_with(config)

@pytest.mark.asyncio
async def test_main_error_handling(mock_system):
    """Test error handling in main"""
    mock_system.generate_profile.side_effect = Exception("Test error")
    
    with patch("sys.argv", ["script.py"]), pytest.raises(Exception):
        await main() 