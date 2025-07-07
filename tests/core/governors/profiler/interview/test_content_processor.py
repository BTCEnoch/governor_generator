"""Tests for the content processor."""

import json
import pytest
from pathlib import Path
from core.governors.profiler.interview.content_processor import (
    ContentProcessor, DialogTemplate, StoryTemplate, InteractionTemplate
)

@pytest.fixture
def input_dir(tmp_path):
    """Create temporary input directory with test content."""
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    
    # Create test governor directory
    gov_dir = input_dir / "TESTGOV"
    gov_dir.mkdir()
    
    # Create test content library
    library = {
        "governor_name": "TESTGOV",
        "traits": {
            "wisdom": {"level": 5},
            "teaching": {"level": 4}
        },
        "dialog_trees": {
            "greeting": {
                "pattern": "Hello, {seeker_name}. I am {governor_name}.",
                "variables": {
                    "seeker_name": ["student", "initiate", "seeker"],
                    "governor_name": ["TESTGOV"]
                },
                "conditions": {
                    "first_meeting": True
                },
                "weights": {
                    "formal": 0.7,
                    "casual": 0.3
                }
            }
        },
        "story_patterns": {
            "quest": {
                "structure": ["introduction", "challenge", "resolution"],
                "elements": {
                    "introduction": ["You seek wisdom", "A test awaits"],
                    "challenge": ["Solve the riddle", "Face your fear"],
                    "resolution": ["Truth revealed", "Wisdom gained"]
                },
                "transitions": {
                    "introduction_to_challenge": ["And so", "But first"],
                    "challenge_to_resolution": ["Finally", "At last"]
                },
                "conditions": {
                    "seeker_level": "beginner"
                }
            }
        },
        "interaction_rules": {
            "teaching": {
                "trigger": "ask_for_wisdom",
                "responses": [
                    "Let me share a teaching",
                    "Here is what you must know"
                ],
                "effects": {
                    "increase_wisdom": 1,
                    "deepen_understanding": True
                },
                "conditions": {
                    "seeker_ready": True,
                    "has_prerequisite": True
                }
            }
        }
    }
    
    library_file = gov_dir / "content_library.json"
    with library_file.open('w', encoding='utf-8') as f:
        json.dump(library, f)
        
    return input_dir

@pytest.fixture
def output_dir(tmp_path):
    """Create temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir

@pytest.fixture
def processor(input_dir, output_dir):
    """Create content processor instance."""
    return ContentProcessor(input_dir, output_dir)

def test_process_all_content(processor):
    """Test processing all content."""
    # Process content
    processor.process_all_content()
    
    # Check output files exist
    gov_dir = processor.output_dir / "TESTGOV"
    assert gov_dir.exists()
    
    assert (gov_dir / "dialog_templates.json").exists()
    assert (gov_dir / "story_templates.json").exists()
    assert (gov_dir / "interaction_templates.json").exists()

def test_process_dialog_content(processor):
    """Test processing dialog content."""
    # Load test library
    library_file = processor.input_dir / "TESTGOV" / "content_library.json"
    with library_file.open('r', encoding='utf-8') as f:
        library = json.load(f)
        
    # Process dialog content
    templates = processor._process_dialog_content(library)
    
    # Verify templates
    assert "greeting" in templates
    template = templates["greeting"]
    assert isinstance(template, DialogTemplate)
    assert template.pattern
    assert template.variables
    assert template.conditions
    assert template.weights

def test_process_story_content(processor):
    """Test processing story content."""
    # Load test library
    library_file = processor.input_dir / "TESTGOV" / "content_library.json"
    with library_file.open('r', encoding='utf-8') as f:
        library = json.load(f)
        
    # Process story content
    templates = processor._process_story_content(library)
    
    # Verify templates
    assert "quest" in templates
    template = templates["quest"]
    assert isinstance(template, StoryTemplate)
    assert template.structure
    assert template.elements
    assert template.transitions
    assert template.conditions

def test_process_interaction_content(processor):
    """Test processing interaction content."""
    # Load test library
    library_file = processor.input_dir / "TESTGOV" / "content_library.json"
    with library_file.open('r', encoding='utf-8') as f:
        library = json.load(f)
        
    # Process interaction content
    templates = processor._process_interaction_content(library)
    
    # Verify templates
    assert "teaching" in templates
    template = templates["teaching"]
    assert isinstance(template, InteractionTemplate)
    assert template.trigger
    assert template.responses
    assert template.effects
    assert template.conditions

def test_extract_dialog_template(processor):
    """Test extracting dialog template."""
    dialog_tree = {
        "pattern": "Hello, {seeker_name}",
        "variables": {"seeker_name": ["student"]},
        "conditions": {"first_meeting": True},
        "weights": {"formal": 0.7}
    }
    
    template = processor._extract_dialog_template(dialog_tree)
    
    assert template
    assert isinstance(template, DialogTemplate)
    assert template.pattern == "Hello, {seeker_name}"
    assert "seeker_name" in template.variables
    assert template.conditions["first_meeting"]
    assert template.weights["formal"] == 0.7

def test_extract_story_template(processor):
    """Test extracting story template."""
    story_pattern = {
        "structure": ["intro", "end"],
        "elements": {"intro": ["Begin"]},
        "transitions": {"intro_to_end": ["Finally"]},
        "conditions": {"ready": True}
    }
    
    template = processor._extract_story_template(story_pattern)
    
    assert template
    assert isinstance(template, StoryTemplate)
    assert "intro" in template.structure
    assert "intro" in template.elements
    assert "intro_to_end" in template.transitions
    assert template.conditions["ready"]

def test_extract_interaction_template(processor):
    """Test extracting interaction template."""
    interaction_rule = {
        "trigger": "ask",
        "responses": ["Answer"],
        "effects": {"learn": True},
        "conditions": {"ready": True}
    }
    
    template = processor._extract_interaction_template(interaction_rule)
    
    assert template
    assert isinstance(template, InteractionTemplate)
    assert template.trigger == "ask"
    assert "Answer" in template.responses
    assert template.effects["learn"]
    assert template.conditions["ready"]

def test_save_templates(processor):
    """Test saving templates."""
    templates = {
        "dialog": {
            "greeting": DialogTemplate(
                pattern="Hello",
                variables={},
                conditions={},
                weights={}
            )
        },
        "story": {
            "quest": StoryTemplate(
                structure=[],
                elements={},
                transitions={},
                conditions={}
            )
        },
        "interaction": {
            "teaching": InteractionTemplate(
                trigger="",
                responses=[],
                effects={},
                conditions={}
            )
        }
    }
    
    # Save templates
    processor._save_templates("TESTGOV", templates)
    
    # Verify files
    gov_dir = processor.output_dir / "TESTGOV"
    assert gov_dir.exists()
    
    for template_type in templates:
        template_file = gov_dir / f"{template_type}_templates.json"
        assert template_file.exists()
        
        # Verify content can be loaded
        with template_file.open('r', encoding='utf-8') as f:
            loaded = json.load(f)
            assert loaded  # Not empty 