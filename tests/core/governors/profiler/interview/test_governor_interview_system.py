"""Tests for the governor interview system."""

import json
import pytest
from pathlib import Path
from datetime import datetime
from core.governors.profiler.interview.governor_interview_system import (
    GovernorInterviewSystem, InterviewSession, ContentLibrary
)

@pytest.fixture
def output_dir(tmp_path):
    """Create temporary output directory"""
    return tmp_path / "interview_output"

@pytest.fixture
def test_traits():
    """Create test trait data"""
    return {
        "name": "TESTGOV",
        "traits": {
            "wisdom": {
                "level": 5,
                "focus": "mystical_insight"
            },
            "compassion": {
                "level": 4,
                "focus": "healing"
            }
        },
        "specializations": ["teaching", "guidance"],
        "mystical_traditions": ["hermetic", "buddhist"]
    }

@pytest.fixture
def interview_system(output_dir):
    """Create interview system instance"""
    return GovernorInterviewSystem(output_dir)

def test_conduct_full_interview_series(interview_system, test_traits):
    """Test conducting full interview series"""
    # Conduct interviews
    library = interview_system.conduct_full_interview_series("TESTGOV", test_traits)
    
    # Verify library was created
    assert library.governor_name == "TESTGOV"
    assert library.traits == test_traits
    
    # Verify all components were generated
    assert library.dialog_trees
    assert library.story_patterns
    assert library.knowledge_base
    assert library.interaction_rules
    assert library.procedural_templates

def test_conduct_topic_interview(interview_system, test_traits):
    """Test conducting single topic interview"""
    # Conduct personality interview
    session = interview_system._conduct_topic_interview(
        "TESTGOV", "personality", test_traits
    )
    
    # Verify session data
    assert session.governor_name == "TESTGOV"
    assert "personality" in session.topics_covered
    assert session.questions_asked
    assert session.responses
    assert session.generated_content
    assert session.insights_gained

def test_integrate_session_content(interview_system, test_traits):
    """Test integrating session content into library"""
    # Create test session
    session = InterviewSession(
        session_id="test_session",
        timestamp=datetime.now().isoformat(),
        governor_name="TESTGOV",
        topics_covered=["personality"],
        questions_asked=["How do you teach?"],
        responses=[{
            "question": "How do you teach?",
            "response": "With wisdom and patience",
            "context": str(test_traits)
        }],
        generated_content={
            "dialog_teaching": {
                "patterns": ["Explains with analogies", "Uses examples"]
            },
            "story_lesson": {
                "elements": ["Challenge", "Insight", "Resolution"]
            }
        },
        insights_gained=["Prefers interactive teaching"]
    )
    
    # Initialize library
    interview_system.current_library = ContentLibrary(
        governor_name="TESTGOV",
        traits=test_traits,
        dialog_trees={},
        story_patterns={},
        knowledge_base={},
        interaction_rules={},
        procedural_templates={}
    )
    
    # Integrate content
    interview_system._integrate_session_content(session)
    
    # Verify content was integrated
    assert "dialog_teaching" in interview_system.current_library.dialog_trees
    assert "story_lesson" in interview_system.current_library.story_patterns

def test_generate_procedural_content(interview_system, test_traits):
    """Test generating procedural content"""
    # Initialize library with test content
    interview_system.current_library = ContentLibrary(
        governor_name="TESTGOV",
        traits=test_traits,
        dialog_trees={
            "dialog_greeting": {
                "patterns": ["Welcomes warmly", "Acknowledges seeker"]
            }
        },
        story_patterns={
            "story_quest": {
                "elements": ["Challenge", "Journey", "Discovery"]
            }
        },
        knowledge_base={},
        interaction_rules={
            "rule_teaching": {
                "conditions": ["seeker_ready", "topic_relevant"]
            }
        },
        procedural_templates={}
    )
    
    # Generate templates
    interview_system._generate_procedural_content()
    
    # Verify templates were generated
    templates = interview_system.current_library.procedural_templates
    assert "dialog" in templates
    assert "story" in templates
    assert "interaction" in templates

def test_save_content_library(interview_system, test_traits, output_dir):
    """Test saving content library"""
    # Create test library
    interview_system.current_library = ContentLibrary(
        governor_name="TESTGOV",
        traits=test_traits,
        dialog_trees={"test": "data"},
        story_patterns={"test": "data"},
        knowledge_base={"test": "data"},
        interaction_rules={"test": "data"},
        procedural_templates={"test": "data"}
    )
    
    # Add test session
    interview_system.sessions.append(
        InterviewSession(
            session_id="test_session",
            timestamp=datetime.now().isoformat(),
            governor_name="TESTGOV",
            topics_covered=["test"],
            questions_asked=["test"],
            responses=[{"test": "data"}],
            generated_content={"test": "data"},
            insights_gained=["test"]
        )
    )
    
    # Save library
    interview_system._save_content_library()
    
    # Verify files were created
    governor_dir = output_dir / "TESTGOV"
    assert governor_dir.exists()
    
    library_file = governor_dir / "content_library.json"
    assert library_file.exists()
    
    sessions_dir = governor_dir / "interview_sessions"
    assert sessions_dir.exists()
    assert list(sessions_dir.glob("*.json"))

def test_load_interview_questions(interview_system):
    """Test loading interview questions"""
    questions = interview_system._load_interview_questions()
    
    # Verify question categories
    assert "personality" in questions
    assert "knowledge" in questions
    assert "teaching" in questions
    assert "challenges" in questions
    
    # Verify questions exist
    for category in questions.values():
        assert category  # Not empty
        assert all(isinstance(q, str) for q in category)

def test_load_interview_topics(interview_system):
    """Test loading interview topics"""
    topics = interview_system._load_interview_topics()
    
    # Verify core topics exist
    assert "personality" in topics
    assert "knowledge" in topics
    assert "teaching" in topics
    assert "challenges" in topics 