"""
Tests for Visual Aspects Generation Script
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from scripts.generate_visual_aspects import (
    load_governor_data,
    extract_governor_traits,
    serialize_aspect,
    save_visual_aspects,
    main
)
from core.governors.visual_aspects.generator import GovernorTraits
from core.governors.visual_aspects.schemas.visual_aspect_schema import (
    AspectScale,
    AspectDimension,
    AspectMotion,
    ColorDefinition,
    PatternDefinition,
    VisualAspect,
    FormDefinition
)
from core.governors.visual_aspects.catalogs.form_types import (
    BaseFormType,
    InteractionType
)

@pytest.fixture
def mock_governor_data():
    """Mock governor data for testing"""
    return {
        "name": "OCCODON",
        "aethyrs": ["LIL", "ARN"],
        "elements": ["fire", "air"],
        "traditions": ["enochian_magic"],
        "personality_traits": ["dynamic"],
        "mystical_domains": ["cosmic"]
    }

@pytest.fixture
def mock_visual_aspect():
    """Mock visual aspect for testing"""
    return VisualAspect(
        governor_name="OCCODON",
        primary_form=FormDefinition(
            name="FIRE_FORM",
            base_type=BaseFormType.FLUID,
            description="Test form",
            valid_interactions={InteractionType.FLOWING},
            tradition_origins=["enochian_magic"],
            elemental_affinities=["fire"],
            aethyr_resonance=["LIL"]
        ),
        secondary_form=None,
        scale=AspectScale.COSMIC,
        dimensions={AspectDimension.VOLUME},
        motions={AspectMotion.HARMONIC},
        colors=[ColorDefinition(
            name="Sacred Flame",
            rgb=(255, 64, 0),
            alpha=0.9,
            tradition_meaning="Divine Fire",
            elemental_association="fire"
        )],
        patterns=[PatternDefinition(
            name="Crown of LIL",
            base_geometry="Dodecahedron",
            repetition_type="Fractal",
            sacred_meaning="Supreme Unity",
            aethyr_influence=["LIL"]
        )],
        aethyr_resonances=["LIL"],
        elemental_influences=["fire"],
        tradition_alignments=["enochian_magic"]
    )

def test_load_governor_data(tmp_path):
    """Test loading governor data from files"""
    # Create mock governor files
    archives_dir = tmp_path / "data/knowledge/archives/governor_archives"
    archives_dir.mkdir(parents=True)
    
    governor1 = {"name": "OCCODON", "aethyrs": ["LIL"]}
    governor2 = {"name": "PASCOMB", "aethyrs": ["ARN"]}
    
    with open(archives_dir / "governor1.json", "w") as f:
        json.dump(governor1, f)
    with open(archives_dir / "governor2.json", "w") as f:
        json.dump(governor2, f)
        
    # Mock the Path to point to our temp directory
    with patch("scripts.generate_visual_aspects.Path") as mock_path:
        mock_path.return_value = archives_dir
        governors = load_governor_data()
        
        assert len(governors) == 2
        assert any(g["name"] == "OCCODON" for g in governors)
        assert any(g["name"] == "PASCOMB" for g in governors)

def test_extract_governor_traits(mock_governor_data):
    """Test extracting traits from governor data"""
    traits = extract_governor_traits(mock_governor_data)
    
    assert isinstance(traits, GovernorTraits)
    assert traits.name == "OCCODON"
    assert "LIL" in traits.aethyrs
    assert "fire" in traits.elements
    assert "enochian_magic" in traits.traditions
    assert "dynamic" in traits.personality_traits
    assert "cosmic" in traits.mystical_domains

def test_serialize_aspect(mock_visual_aspect):
    """Test serializing visual aspect to JSON format"""
    serialized = serialize_aspect(mock_visual_aspect)
    
    assert isinstance(serialized, dict)
    assert serialized["governor_name"] == "OCCODON"
    assert serialized["scale"] == "COSMIC"
    assert "VOLUME" in serialized["dimensions"]
    assert "HARMONIC" in serialized["motions"]
    
    # Check form serialization
    assert serialized["primary_form"]["name"] == "FIRE_FORM"
    assert serialized["primary_form"]["base_type"] == "FLUID"
    assert "FLOWING" in serialized["primary_form"]["valid_interactions"]

def test_save_visual_aspects(tmp_path, mock_visual_aspect):
    """Test saving visual aspects to files"""
    output_dir = tmp_path / "governor_dossier/visual_aspects"
    
    with patch("scripts.generate_visual_aspects.Path") as mock_path:
        mock_path.return_value = output_dir
        save_visual_aspects({"OCCODON": mock_visual_aspect})
        
        # Check that file was created
        expected_file = output_dir / "OCCODON_visual.json"
        assert expected_file.exists()
        
        # Verify file contents
        with open(expected_file) as f:
            saved_data = json.load(f)
            assert saved_data["governor_name"] == "OCCODON"
            assert saved_data["scale"] == "COSMIC"

@patch("scripts.generate_visual_aspects.load_governor_data")
@patch("scripts.generate_visual_aspects.VisualAspectGenerator")
@patch("scripts.generate_visual_aspects.save_visual_aspects")
def test_main_success(mock_save, mock_generator, mock_load, mock_governor_data):
    """Test successful execution of main function"""
    # Setup mocks
    mock_load.return_value = [mock_governor_data]
    mock_generator_instance = MagicMock()
    mock_generator.return_value = mock_generator_instance
    mock_generator_instance.generate_aspects_batch.return_value = {"OCCODON": MagicMock()}
    
    # Run main
    main()
    
    # Verify calls
    mock_load.assert_called_once()
    mock_generator_instance.generate_aspects_batch.assert_called_once()
    mock_save.assert_called_once()

@patch("scripts.generate_visual_aspects.load_governor_data")
def test_main_failure(mock_load):
    """Test handling of errors in main function"""
    mock_load.side_effect = Exception("Test error")
    
    with pytest.raises(Exception) as exc:
        main()
    assert str(exc.value) == "Test error" 