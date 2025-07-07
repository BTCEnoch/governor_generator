"""
Tests for Enhanced Governor Profile Analyzer
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

from core.governors.profiler.core.enhanced_profile_analyzer import (
    EnhancedProfileAnalyzer,
    WisdomFoundation,
    ElementalEssence,
    TeachingDoctrine,
    VoidmakerAwareness,
    EnhancedGovernorProfile
)

# Sample test data
SAMPLE_GOVERNOR_DATA = {
    "knowledge_base_selections": {
        "chosen_traditions": ["hermetic", "kabbalah"],
        "reasoning": "Alignment with mystical wisdom",
        "indexed_links": ["link1", "link2"],
        "application_notes": "Apply with care"
    },
    "block_b": {
        "q6_element": "water",
        "q6_color": "blue",
        "q6_motion": "flowing",
        "q6_scent": "ocean",
        "q7_tarot": "The Star",
        "q8_sephirah": "Binah",
        "q9_constellation": "Pisces"
    },
    "block_c": {
        "q11_virtues": ["patient", "wise", "gentle"],
        "q12_flaws": "Sometimes too hesitant"
    },
    "block_d": {
        "q16_core_teaching": "Flow like water",
        "q17_urgency": "Time of great change",
        "q18_misconception": "Force over flow",
        "q19_stages": ["observe", "adapt", "flow"],
        "q20_enochian_terms": ["ZONG", "GRAA"]
    },
    "block_j": {
        "q46_preferred_mechanics": ["ritual", "puzzle"]
    },
    "voidmaker_expansion": {
        "cosmic_awareness_block": ["pattern1", "pattern2"],
        "reality_influence_block": ["influence1", "influence2"],
        "integration_unity_block": ["unity1", "unity2"],
        "cryptic_knowledge": ["secret1", "secret2"]
    }
}

@pytest.fixture
def analyzer():
    """Create analyzer instance with mocked directory"""
    return EnhancedProfileAnalyzer(Path("/mock/path"))

@pytest.fixture
def mock_governor_file(monkeypatch):
    """Mock governor file reading"""
    def mock_open_file(*args, **kwargs):
        return mock_open(read_data=json.dumps(SAMPLE_GOVERNOR_DATA))()
    monkeypatch.setattr("builtins.open", mock_open_file)

def test_load_governor_data(analyzer, mock_governor_file):
    """Test loading governor data from file"""
    data = analyzer.load_governor_data("TEST001")
    assert data == SAMPLE_GOVERNOR_DATA
    assert "knowledge_base_selections" in data
    assert "block_b" in data

def test_extract_wisdom_foundation(analyzer):
    """Test wisdom foundation extraction"""
    wisdom = analyzer.extract_wisdom_foundation(SAMPLE_GOVERNOR_DATA)
    assert isinstance(wisdom, WisdomFoundation)
    assert "hermetic" in wisdom.chosen_traditions
    assert wisdom.philosophical_alignment == "Alignment with mystical wisdom"
    assert len(wisdom.indexed_links) == 2

def test_extract_elemental_essence(analyzer):
    """Test elemental essence extraction"""
    elemental = analyzer.extract_elemental_essence(SAMPLE_GOVERNOR_DATA)
    assert isinstance(elemental, ElementalEssence)
    assert elemental.ruling_element == "water"
    assert elemental.manifestation["color"] == "blue"
    assert elemental.tarot_key == "The Star"
    assert elemental.sephirah == "Binah"

def test_extract_teaching_doctrine(analyzer):
    """Test teaching doctrine extraction"""
    teaching = analyzer.extract_teaching_doctrine(SAMPLE_GOVERNOR_DATA)
    assert isinstance(teaching, TeachingDoctrine)
    assert teaching.core_lesson == "Flow like water"
    assert len(teaching.instruction_stages) == 3
    assert len(teaching.enochian_terms) == 2

def test_extract_voidmaker_awareness(analyzer):
    """Test voidmaker awareness extraction"""
    voidmaker = analyzer.extract_voidmaker_awareness(SAMPLE_GOVERNOR_DATA)
    assert isinstance(voidmaker, VoidmakerAwareness)
    assert len(voidmaker.cosmic_patterns) == 2
    assert len(voidmaker.reality_influence) == 2
    assert len(voidmaker.integration_unity) == 2

def test_determine_narrative_tone(analyzer):
    """Test narrative tone determination"""
    tone = analyzer.determine_narrative_tone(SAMPLE_GOVERNOR_DATA)
    assert isinstance(tone, str)
    assert tone == "measured and philosophical"  # Based on patient/wise virtues

def test_calculate_difficulty_scale(analyzer):
    """Test difficulty scale calculation"""
    difficulty = analyzer.calculate_difficulty_scale(SAMPLE_GOVERNOR_DATA)
    assert isinstance(difficulty, int)
    assert 1 <= difficulty <= 10

def test_analyze_governor_complete(analyzer, mock_governor_file):
    """Test complete governor analysis"""
    profile = analyzer.analyze_governor("TEST001")
    assert isinstance(profile, EnhancedGovernorProfile)
    assert profile.governor_id == "TEST001"
    assert profile.narrative_tone == "measured and philosophical"
    assert 1 <= profile.difficulty_scale <= 10
    assert len(profile.preferred_utilities) == 2
    assert "ritual" in profile.preferred_utilities

def test_batch_analyze_governors(analyzer, mock_governor_file):
    """Test batch analysis of multiple governors"""
    results = analyzer.batch_analyze_governors(["TEST001", "TEST002"])
    assert isinstance(results, dict)
    assert "TEST001" in results
    assert isinstance(results["TEST001"], EnhancedGovernorProfile)

def test_error_handling_missing_data(analyzer):
    """Test handling of missing or malformed data"""
    with pytest.raises(Exception):
        analyzer.extract_wisdom_foundation({})  # Empty data

def test_error_handling_invalid_governor(analyzer):
    """Test handling of invalid governor ID"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(Exception):
            analyzer.load_governor_data("INVALID_ID") 