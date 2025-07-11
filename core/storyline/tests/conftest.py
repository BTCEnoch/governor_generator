"""Pytest configuration for storyline tests"""

import pytest
import logging
from pathlib import Path

@pytest.fixture(autouse=True)
def setup_logging():
    """Configure logging for all tests"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a test data directory with common subdirectories"""
    data_dir = tmp_path / "test_data"
    
    # Create common directories
    subdirs = [
        "governor_output",
        "pack",
        "canon",
        "governor_dossier",
        "partial_results",
        "storylines"
    ]
    
    for subdir in subdirs:
        (data_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    return data_dir

@pytest.fixture
def sample_governor_data():
    """Sample governor data for testing"""
    return {
        "governor_name": "ABRIOND",
        "governor_number": 1,
        "profile": {
            "aethyr": "LIL",
            "element": "fire",
            "watchtower": "east",
            "zodiac": "aries"
        },
        "interview_date": "2025-07-09",
        "confirmation": "confirmed",
        "knowledge_base_selections": {
            "chosen_traditions": [
                "kabbalah",
                "hermeticism",
                "enochian"
            ],
            "reasoning": "Deep understanding of mystical principles",
            "indexed_links": [
                "kabbalah/tree_of_life",
                "hermeticism/emerald_tablet",
                "enochian/aethyrs"
            ],
            "application_notes": "Strong focus on practical applications"
        },
        "blocks": {
            "A_identity_origin": {
                "1": {"question": "Origin", "answer": "Born of celestial fire"},
                "2": {"question": "Purpose", "answer": "Guide seekers to wisdom"}
            },
            "B_elemental_essence": {
                "3": {"question": "Element", "answer": "Pure fire of creation"},
                "4": {"question": "Nature", "answer": "Transformative force"}
            }
        },
        "voidmaker_expansion": {
            "cosmic_insights": {
                "1": {
                    "question": "Nature of Reality",
                    "answer": "Reality is a geometric pattern of consciousness"
                },
                "2": {
                    "question": "Universal Truth",
                    "answer": "Sacred geometry reveals infinite awareness"
                }
            },
            "mystical_wisdom": {
                "1": {
                    "question": "Hidden Knowledge",
                    "answer": "Truth lies in hermetic patterns"
                },
                "2": {
                    "question": "Divine Connection",
                    "answer": "Unity through sacred understanding"
                }
            }
        }
    }

@pytest.fixture
def sample_storyline_data():
    """Sample storyline data for testing"""
    return {
        "governor_name": "ABRIOND",
        "storyline_metadata": {
            "version": "2.0.0",
            "generation_timestamp": "2025-07-09T12:00:00Z",
            "total_nodes": 25,
            "canonical_elements": {
                "aethyrs": ["LIL", "ARN", "ZOM"],
                "watchtowers": ["east", "south"],
                "elements": ["fire", "air"]
            }
        },
        "reputation_tiers": {
            "tier_1": {
                "range": "0-25",
                "level": "novice",
                "unlocked_content": ["basic_rituals", "simple_invocations"],
                "voidmaker_reveals": ["cosmic_truth_1"]
            },
            "tier_2": {
                "range": "26-50",
                "level": "apprentice",
                "unlocked_content": ["advanced_rituals", "elemental_work"],
                "voidmaker_reveals": ["cosmic_truth_2", "cosmic_truth_3"]
            },
            "tier_3": {
                "range": "51-75",
                "level": "adept",
                "unlocked_content": ["master_rituals", "aethyr_travel"],
                "voidmaker_reveals": ["cosmic_truth_4", "cosmic_truth_5", "cosmic_truth_6"]
            },
            "tier_4": {
                "range": "76-100",
                "level": "master",
                "unlocked_content": ["governor_secrets", "void_mastery"],
                "voidmaker_reveals": ["final_truth_1", "final_truth_2", "final_truth_3", "final_truth_4"]
            }
        },
        "narrative_nodes": {
            "node_1": {
                "node_id": "start",
                "title": "The First Gate",
                "content": "You stand before the celestial gate of ABRIOND...",
                "dialogue": {
                    "governor_voice": "Welcome seeker, to the threshold of wisdom...",
                    "personality_integration": True
                },
                "choices": [
                    {
                        "choice_text": "Request guidance",
                        "next_node": "node_2",
                        "requirements": {
                            "reputation_min": 0,
                            "energy_cost": 10
                        }
                    }
                ],
                "mechanics": {
                    "energy_cost": 10,
                    "reputation_gain": 5,
                    "rewards": {
                        "tokens": 100,
                        "knowledge": ["basic_wisdom"],
                        "achievements": ["first_step"]
                    }
                }
            }
        }
    } 