"""
Tests for batch knowledge mapping script.
"""

import json
import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.batch_knowledge_mapping import (
    load_governor_index,
    save_knowledge_profile,
    process_governors,
)
from core.governors.traits.knowledge_mapper import GovernorKnowledge, TraditionKnowledge

@pytest.fixture
def test_data_dir(tmp_path):
    """Create test data directory structure"""
    data_dir = tmp_path
    
    # Create governors index
    index_dir = data_dir / "data/governors/indexes"
    index_dir.mkdir(parents=True)
    
    index_data = {
        "OCCODON": 1,
        "PASCOMB": 2,
        "VALGARS": 3
    }
    
    with open(index_dir / "governor_number_index.json", "w") as f:
        json.dump(index_data, f)
    
    return data_dir

@pytest.fixture
def test_knowledge():
    """Create test knowledge profile"""
    primary_tradition = TraditionKnowledge(
        tradition_name="Spiritual Ascension",
        core_concepts=["Wisdom", "Balance"],
        practices=["Meditation", "Ritual"],
        correspondences={"elements": ["fire", "air"]},
        historical_context="Ancient tradition",
        modern_applications=["Self-development"]
    )
    
    secondary_tradition = TraditionKnowledge(
        tradition_name="Astrology",
        core_concepts=["Celestial Influence"],
        practices=["Star Reading"],
        correspondences={"planets": ["Sun"]},
        historical_context="Astrological tradition",
        modern_applications=["Timing"]
    )
    
    return GovernorKnowledge(
        governor_id="OCCODON",
        primary_tradition=primary_tradition,
        secondary_traditions=[secondary_tradition],
        specialized_domains=["Wisdom Teaching"],
        teaching_methods=["Direct Instruction"],
        ritual_practices=["Fire Ritual"],
        mystical_correspondences={"elements": ["fire"]}
    )

def test_load_governor_index(test_data_dir, monkeypatch):
    """Test loading governor index"""
    # Patch data directory
    monkeypatch.setattr(Path, "cwd", lambda: test_data_dir)
    
    index = load_governor_index()
    assert len(index) == 3
    assert index["OCCODON"] == 1
    assert index["PASCOMB"] == 2
    assert index["VALGARS"] == 3

def test_save_knowledge_profile(test_data_dir, test_knowledge):
    """Test saving knowledge profile"""
    output_dir = test_data_dir / "output"
    save_knowledge_profile(test_knowledge, output_dir)
    
    # Check file was created
    output_file = output_dir / "occodon_knowledge.json"
    assert output_file.exists()
    
    # Check file contents
    with open(output_file) as f:
        data = json.load(f)
        
    assert data["governor_id"] == "OCCODON"
    assert data["primary_tradition"]["tradition_name"] == "Spiritual Ascension"
    assert len(data["secondary_traditions"]) == 1
    assert data["secondary_traditions"][0]["tradition_name"] == "Astrology"
    assert "Wisdom Teaching" in data["specialized_domains"]
    assert "Direct Instruction" in data["teaching_methods"]
    assert "Fire Ritual" in data["ritual_practices"]
    assert "fire" in data["mystical_correspondences"]["elements"]

def test_process_governors(test_data_dir, monkeypatch):
    """Test processing all governors"""
    # Patch data directory
    monkeypatch.setattr(Path, "cwd", lambda: test_data_dir)
    
    # Create output directory
    output_dir = test_data_dir / "output"
    
    # Process governors
    process_governors(output_dir)
    
    # Check output directory exists
    assert output_dir.exists()
    
    # Check log file was created
    log_file = test_data_dir / "logs/knowledge_mapping.log"
    assert log_file.exists()

def test_process_governors_no_index(test_data_dir, monkeypatch):
    """Test processing with missing index"""
    # Patch data directory
    monkeypatch.setattr(Path, "cwd", lambda: test_data_dir)
    
    # Remove index file
    index_file = test_data_dir / "data/governors/indexes/governor_number_index.json"
    index_file.unlink()
    
    # Process governors
    output_dir = test_data_dir / "output"
    process_governors(output_dir)
    
    # Check no output was created
    assert not output_dir.exists()

def test_process_governors_invalid_governor(test_data_dir, monkeypatch, caplog):
    """Test processing with invalid governor"""
    # Patch data directory
    monkeypatch.setattr(Path, "cwd", lambda: test_data_dir)
    
    # Create invalid governor index
    index_dir = test_data_dir / "data/governors/indexes"
    index_data = {"INVALID": 999}
    
    with open(index_dir / "governor_number_index.json", "w") as f:
        json.dump(index_data, f)
    
    # Process governors
    output_dir = test_data_dir / "output"
    process_governors(output_dir)
    
    # Check error was logged
    assert "Failed to map knowledge for INVALID" in caplog.text 