"""Tests for the core data loader"""

import pytest
from pathlib import Path
from typing import Dict, Any
from ..core_loader import (
    CoreDataLoader,
    KnowledgeBaseSelection,
    VoidmakerBlock,
    EnhancedGovernorProfile
)

@pytest.fixture
def test_base_path(tmp_path):
    """Create a test directory structure"""
    # Create required directories
    (tmp_path / "governor_output").mkdir()
    (tmp_path / "pack").mkdir()
    (tmp_path / "canon").mkdir()
    (tmp_path / "governor_dossier").mkdir()
    
    return tmp_path

@pytest.fixture
def test_governor_data() -> Dict[str, Any]:
    """Create test governor data"""
    return {
        "governor_name": "ABRIOND",
        "governor_number": 1,
        "profile": {
            "aethyr": "LIL",
            "element": "fire"
        },
        "interview_date": "2025-07-09",
        "confirmation": "confirmed",
        "knowledge_base_selections": {
            "chosen_traditions": ["kabbalah", "hermeticism"],
            "reasoning": "Test reasoning",
            "indexed_links": ["link1", "link2"],
            "application_notes": "Test notes"
        },
        "blocks": {
            "A_identity_origin": {
                "1": {"question": "Q1", "answer": "A1"},
                "2": {"question": "Q2", "answer": "A2"}
            }
        },
        "voidmaker_expansion": {
            "block1": {
                "1": {"question": "VQ1", "answer": "Reality is an illusion"},
                "2": {"question": "VQ2", "answer": "Consciousness is infinite"}
            }
        }
    }

@pytest.fixture
def loader(test_base_path):
    """Create a CoreDataLoader instance"""
    return CoreDataLoader(test_base_path)

def test_loader_initialization(test_base_path):
    """Test loader initialization"""
    loader = CoreDataLoader(test_base_path)
    assert loader.base_path == test_base_path
    assert loader.governor_output_path == test_base_path / "governor_output"
    assert loader.canonical_pack_path == test_base_path / "pack"
    assert loader.canon_path == test_base_path / "canon"

def test_validate_paths(test_base_path):
    """Test path validation"""
    # Should work with valid paths
    loader = CoreDataLoader(test_base_path)
    loader._validate_paths()  # Should not raise
    
    # Should fail with invalid path
    invalid_path = test_base_path / "nonexistent"
    with pytest.raises(FileNotFoundError):
        CoreDataLoader(invalid_path)

def test_load_enhanced_governor(loader, test_base_path, test_governor_data):
    """Test loading enhanced governor profile"""
    # Create test governor file
    governor_file = test_base_path / "governor_dossier" / "ABRIOND.json"
    governor_file.write_text(str(test_governor_data))
    
    # Test loading
    with pytest.raises(FileNotFoundError):
        loader.load_enhanced_governor("NONEXISTENT")
    
    profile = loader.load_enhanced_governor("ABRIOND")
    assert isinstance(profile, EnhancedGovernorProfile)
    assert profile.governor_name == "ABRIOND"
    assert profile.governor_number == 1
    assert profile.home_aethyr == "LIL"
    assert profile.elemental_nature == "fire"
    assert len(profile.knowledge_base_selections.chosen_traditions) == 2

def test_parse_governor_data(loader, test_governor_data):
    """Test parsing governor data"""
    profile = loader._parse_governor_data(test_governor_data)
    
    assert isinstance(profile, EnhancedGovernorProfile)
    assert isinstance(profile.knowledge_base_selections, KnowledgeBaseSelection)
    assert isinstance(profile.voidmaker_expansion["block1"], VoidmakerBlock)
    
    # Check derived attributes
    assert profile.tradition_depth == 2
    assert profile.power_level == "formidable_approachable"

def test_extract_voidmaker_themes(loader):
    """Test voidmaker theme extraction"""
    block_data = {
        "1": {"question": "Q1", "answer": "Reality is an illusion of consciousness"},
        "2": {"question": "Q2", "answer": "Sacred geometry reveals universal patterns"}
    }
    
    themes = loader._extract_voidmaker_themes(block_data)
    assert isinstance(themes, list)
    assert "reality" in themes
    assert "consciousness" in themes
    assert "sacred" in themes
    assert "pattern" in themes

def test_extract_derived_attributes(loader):
    """Test derived attribute extraction"""
    profile = EnhancedGovernorProfile(
        governor_name="ABRIOND",
        governor_number=1,
        profile={"aethyr": "LIL", "element": "fire"},
        interview_date="2025-07-09",
        confirmation="confirmed",
        knowledge_base_selections=KnowledgeBaseSelection(
            chosen_traditions=["kabbalah", "hermeticism"],
            reasoning="Test",
            indexed_links=[],
            application_notes=""
        ),
        blocks={},
        voidmaker_expansion={}
    )
    
    loader._extract_derived_attributes(profile)
    
    assert profile.home_aethyr == "LIL"
    assert profile.elemental_nature == "fire"
    assert profile.tradition_depth == 2
    assert profile.power_level == "formidable_approachable"

def test_list_available_governors(loader, test_base_path):
    """Test listing available governors"""
    # Create test files
    (test_base_path / "governor_output" / "GOV1.json").touch()
    (test_base_path / "governor_output" / "GOV2.json").touch()
    
    governors = loader.list_available_governors()
    assert len(governors) == 2
    assert "GOV1" in governors
    assert "GOV2" in governors

def test_validate_governor_completeness(loader, test_base_path, test_governor_data):
    """Test governor completeness validation"""
    # Create test file
    governor_file = test_base_path / "governor_dossier" / "ABRIOND.json"
    governor_file.write_text(str(test_governor_data))
    
    validation = loader.validate_governor_completeness("ABRIOND")
    assert validation["is_complete"] is True
    assert validation["has_knowledge_base_selections"] is True
    assert validation["has_voidmaker_expansion"] is True
    assert validation["has_blocks"] is True
    assert validation["has_derived_attributes"] is True 