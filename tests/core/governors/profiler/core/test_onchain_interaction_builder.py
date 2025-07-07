"""Tests for the on-chain interaction builder system."""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock
from core.governors.profiler.core.onchain_interaction_builder import (
    OnchainInteractionBuilder, InteractionPattern, KnowledgeFragment
)
from core.governors.profiler.core.trait_interpreter import TraitUnderstanding

@pytest.fixture
def trait_interpreter():
    """Create a mock trait interpreter"""
    interpreter = Mock()
    
    # Create test trait understandings
    test_traits = [
        TraitUnderstanding(
            name="Wisdom",
            definition="Deep understanding of mystical truths",
            category="virtues",
            usage_context="When wisdom manifests, profound insights emerge",
            ai_impact="Influences responses to show deep understanding",
            related_traits=["Knowledge", "Insight"],
            mystical_correspondences={"tradition": "Hermetic", "element": "Air"}
        ),
        TraitUnderstanding(
            name="Compassion",
            definition="Empathy for all beings",
            category="virtues",
            usage_context="When compassion flows, healing occurs",
            ai_impact="Creates nurturing, supportive responses",
            related_traits=["Kindness", "Healing"],
            mystical_correspondences={"tradition": "Buddhist", "element": "Water"}
        )
    ]
    
    interpreter.interpret_binary_traits.return_value = test_traits
    return interpreter

@pytest.fixture
def output_dir(tmp_path):
    """Create temporary output directory"""
    return tmp_path / "interaction_libraries"

@pytest.fixture
def builder(trait_interpreter, output_dir):
    """Create interaction builder instance"""
    return OnchainInteractionBuilder(trait_interpreter, output_dir)

def test_build_basic_patterns(builder, trait_interpreter):
    """Test building basic interaction patterns"""
    # Create test binary data
    binary_traits = b'VIS1' + bytes([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    # Build patterns
    builder.build_interaction_library("TESTGOV", binary_traits)
    
    # Verify patterns were created
    assert "greet_Wisdom" in builder.patterns
    assert "teach_Wisdom" in builder.patterns
    assert "greet_Compassion" in builder.patterns
    assert "teach_Compassion" in builder.patterns
    
    # Verify pattern content
    wisdom_greet = builder.patterns["greet_Wisdom"]
    assert "first_interaction" in wisdom_greet.trigger_conditions
    assert any("Wisdom" in template for template in wisdom_greet.response_templates)
    assert "Wisdom" in wisdom_greet.trait_requirements

def test_build_knowledge_fragments(builder, trait_interpreter):
    """Test building knowledge fragments"""
    # Create test binary data
    binary_traits = b'VIS1' + bytes([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    # Build knowledge
    builder.build_interaction_library("TESTGOV", binary_traits)
    
    # Verify knowledge fragments were created
    assert "nature_of_wisdom" in builder.knowledge
    assert "using_wisdom" in builder.knowledge
    assert "nature_of_compassion" in builder.knowledge
    assert "using_compassion" in builder.knowledge
    
    # Verify fragment content
    wisdom_nature = builder.knowledge["nature_of_wisdom"]
    assert "Deep understanding" in wisdom_nature.content
    assert "virtues" in wisdom_nature.tags
    assert "Hermetic" == wisdom_nature.source_tradition

def test_generate_response_templates(builder, trait_interpreter):
    """Test generating response templates"""
    # Create test binary data
    binary_traits = b'VIS1' + bytes([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    # Build templates
    builder.build_interaction_library("TESTGOV", binary_traits)
    
    # Verify combination patterns were created
    pattern_id = "combine_Wisdom_Compassion"
    assert pattern_id in builder.patterns
    
    # Verify pattern content
    pattern = builder.patterns[pattern_id]
    assert "Wisdom" in pattern.trait_requirements
    assert "Compassion" in pattern.trait_requirements
    assert any("work together" in template for template in pattern.response_templates)

def test_build_search_index(builder, trait_interpreter):
    """Test building search index"""
    # Create test binary data
    binary_traits = b'VIS1' + bytes([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    # Build library
    library = builder.build_interaction_library("TESTGOV", binary_traits)
    
    # Verify index structure
    index = library["index"]
    assert "by_trait" in index
    assert "by_tag" in index
    assert "by_tradition" in index
    
    # Verify trait indexing
    assert "Wisdom" in index["by_trait"]
    assert "patterns" in index["by_trait"]["Wisdom"]
    assert "knowledge" in index["by_trait"]["Wisdom"]
    
    # Verify tag indexing
    assert "virtues" in index["by_tag"]
    assert "basic_knowledge" in index["by_tag"]
    
    # Verify tradition indexing
    assert "Hermetic" in index["by_tradition"]
    assert "Buddhist" in index["by_tradition"]

def test_save_library(builder, trait_interpreter, output_dir):
    """Test saving interaction library"""
    # Create test binary data
    binary_traits = b'VIS1' + bytes([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    # Build and save library
    builder.build_interaction_library("TESTGOV", binary_traits)
    
    # Verify file was created
    output_file = output_dir / "TESTGOV_interactions.json"
    assert output_file.exists()
    
    # Verify file content
    with output_file.open('r', encoding='utf-8') as f:
        library = json.load(f)
        
    assert library["governor"] == "TESTGOV"
    assert "traits" in library
    assert "patterns" in library
    assert "knowledge" in library
    assert "index" in library 