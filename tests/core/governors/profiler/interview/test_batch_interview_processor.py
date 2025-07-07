"""Tests for the batch interview processor."""

import json
import pytest
from pathlib import Path
from core.governors.profiler.interview.batch_interview_processor import (
    BatchInterviewProcessor
)

@pytest.fixture
def governors_dir(tmp_path):
    """Create temporary governors directory with test files"""
    gov_dir = tmp_path / "governors"
    gov_dir.mkdir()
    
    # Create test governor files
    governors = [
        {
            "name": "GOV1",
            "traits": {
                "wisdom": {"level": 5},
                "teaching": {"level": 4}
            }
        },
        {
            "name": "GOV2",
            "traits": {
                "insight": {"level": 4},
                "guidance": {"level": 5}
            }
        }
    ]
    
    for gov in governors:
        gov_file = gov_dir / f"{gov['name']}.json"
        with gov_file.open('w', encoding='utf-8') as f:
            json.dump(gov, f)
            
    return gov_dir

@pytest.fixture
def output_dir(tmp_path):
    """Create temporary output directory"""
    out_dir = tmp_path / "output"
    out_dir.mkdir()
    return out_dir

@pytest.fixture
def processor(governors_dir, output_dir):
    """Create batch processor instance"""
    return BatchInterviewProcessor(governors_dir, output_dir)

def test_process_all_governors(processor):
    """Test processing all governors"""
    # Process governors
    results = processor.process_all_governors()
    
    # Verify results
    assert len(results) == 2
    assert "GOV1" in results
    assert "GOV2" in results
    
    # Verify content libraries
    for library in results.values():
        assert library.dialog_trees
        assert library.story_patterns
        assert library.knowledge_base
        assert library.interaction_rules
        assert library.procedural_templates

def test_process_governor(processor, governors_dir):
    """Test processing single governor"""
    # Process one governor
    gov_file = governors_dir / "GOV1.json"
    library = processor._process_governor(gov_file)
    
    # Verify library
    assert library.governor_name == "GOV1"
    assert library.traits["name"] == "GOV1"
    assert library.dialog_trees
    assert library.story_patterns
    assert library.knowledge_base
    assert library.interaction_rules
    assert library.procedural_templates

def test_output_files_created(processor):
    """Test output files are created"""
    # Process governors
    processor.process_all_governors()
    
    # Check output directories exist
    gov1_dir = processor.output_dir / "GOV1"
    gov2_dir = processor.output_dir / "GOV2"
    assert gov1_dir.exists()
    assert gov2_dir.exists()
    
    # Check library files exist
    assert (gov1_dir / "content_library.json").exists()
    assert (gov2_dir / "content_library.json").exists()
    
    # Check session directories exist
    assert (gov1_dir / "interview_sessions").exists()
    assert (gov2_dir / "interview_sessions").exists()
    
    # Check session files exist
    assert list((gov1_dir / "interview_sessions").glob("*.json"))
    assert list((gov2_dir / "interview_sessions").glob("*.json"))

def test_error_handling(processor, governors_dir):
    """Test error handling for invalid files"""
    # Create invalid governor file
    invalid_file = governors_dir / "INVALID.json"
    with invalid_file.open('w') as f:
        f.write("invalid json")
        
    # Process should continue despite error
    results = processor.process_all_governors()
    
    # Valid governors should still be processed
    assert len(results) == 2
    assert "GOV1" in results
    assert "GOV2" in results

def test_parallel_processing(governors_dir, output_dir):
    """Test parallel processing with multiple workers"""
    # Create processor with 2 workers
    processor = BatchInterviewProcessor(
        governors_dir,
        output_dir,
        max_workers=2
    )
    
    # Process governors
    results = processor.process_all_governors()
    
    # Verify results
    assert len(results) == 2
    assert "GOV1" in results
    assert "GOV2" in results 