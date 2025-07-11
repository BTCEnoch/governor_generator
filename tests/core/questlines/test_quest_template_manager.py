"""
Tests for quest template generation system
"""

import pytest
from pathlib import Path
from datetime import datetime

from core.governors.profiles.analyzer import (
    EnhancedProfile,
    ElementalEssence,
    VoidmakerAwareness,
    WisdomFoundation,
    TeachingDoctrine
)
from core.questlines.templates.quest_template_manager import (
    QuestTemplateManager,
    QuestDifficulty,
    ChallengeType
)

@pytest.fixture
def template_manager():
    """Create quest template manager instance"""
    return QuestTemplateManager(Path("tests/data/quest_templates"))

@pytest.fixture
def mock_profile():
    """Create mock enhanced profile for testing"""
    return EnhancedProfile(
        governor_id="TEST_GOV_001",
        wisdom_foundation=WisdomFoundation(
            primary_domain="mystical arts",
            teaching_methods=["meditation", "ritual"],
            difficulty_curve=[0.2, 0.4, 0.6, 0.8]
        ),
        teaching_doctrine=TeachingDoctrine(
            preferred_methods=["direct", "experiential"],
            adaptability=0.8,
            progression_curve=[0.3, 0.5, 0.7, 0.9]
        ),
        void_awareness=VoidmakerAwareness(
            resonance=0.75,
            manifestation="Ethereal",
            void_affinity=["cosmic", "ethereal"],
            cosmic_patterns=["Pattern 1", "Pattern 2"],
            reality_influence=["Influence 1", "Influence 2"],
            integration_unity=["Unity 1", "Unity 2"]
        ),
        elemental_essence=ElementalEssence(
            ruling_element="fire",
            secondary_elements=["air", "spirit"],
            elemental_balance=0.8,
            manifestation_strength=7
        ),
        difficulty_scale=7,
        narrative_tone="mysterious",
        preferred_mechanics=["riddles", "rituals"]
    )

async def test_quest_template_generation(template_manager, mock_profile):
    """Test basic quest template generation"""
    template = template_manager.generate_quest_template(
        mock_profile,
        "wisdom_trial"
    )
    
    assert template.template_id.startswith("quest_TEST_GOV_001")
    assert template.governor_id == mock_profile.governor_id
    assert template.elemental_affinity == mock_profile.elemental_essence.ruling_element
    assert template.difficulty == QuestDifficulty.MASTER
    assert len(template.stages) == 3

async def test_quest_difficulty_calculation(template_manager, mock_profile):
    """Test quest difficulty calculation"""
    template = template_manager.generate_quest_template(
        mock_profile,
        "wisdom_trial"
    )
    
    # Profile difficulty 7 should map to MASTER
    assert template.difficulty == QuestDifficulty.MASTER
    
    # Test with different difficulty levels
    mock_profile.difficulty_scale = 2
    template = template_manager.generate_quest_template(
        mock_profile,
        "wisdom_trial"
    )
    assert template.difficulty == QuestDifficulty.NOVICE

async def test_voidmaker_tier_calculation(template_manager, mock_profile):
    """Test voidmaker tier calculation"""
    template = template_manager.generate_quest_template(
        mock_profile,
        "wisdom_trial"
    )
    
    # Default mock profile has 6 void patterns (2 each), should be tier 1
    assert template.voidmaker_tier == 1
    
    # Test with more patterns
    mock_profile.void_awareness.cosmic_patterns.extend(["Pattern 3", "Pattern 4"])
    mock_profile.void_awareness.reality_influence.extend(["Influence 3", "Influence 4"])
    mock_profile.void_awareness.integration_unity.extend(["Unity 3", "Unity 4"])
    
    template = template_manager.generate_quest_template(
        mock_profile,
        "wisdom_trial"
    )
    assert template.voidmaker_tier == 2

async def test_quest_challenge_generation(template_manager, mock_profile):
    """Test challenge generation in quests"""
    template = template_manager.generate_quest_template(
        mock_profile,
        "wisdom_trial"
    )
    
    # Check first stage challenges
    stage = template.stages[0]
    assert len(stage.challenges) >= 1
    
    challenge = stage.challenges[0]
    assert challenge.challenge_type in [
        ChallengeType.MEDITATION,
        ChallengeType.RIDDLE,
        ChallengeType.DIVINATION
    ]
    assert challenge.difficulty == QuestDifficulty.MASTER
    assert "fire" in challenge.description.lower()

async def test_quest_reward_calculation(template_manager, mock_profile):
    """Test quest reward calculations"""
    template = template_manager.generate_quest_template(
        mock_profile,
        "wisdom_trial"
    )
    
    # Check total rewards
    assert template.total_wisdom_reward > 0
    assert template.total_energy_required > 0
    
    # Check stage rewards
    for stage in template.stages:
        assert stage.reward.wisdom_tokens > 0
        assert stage.reward.reputation_gain > 0
        
        # Final stage should have artifact reward
        if stage.stage_number == len(template.stages) - 1:
            assert stage.reward.artifact_type
            assert stage.reward.artifact_rarity

async def test_quest_descriptions(template_manager, mock_profile):
    """Test quest description generation"""
    template = template_manager.generate_quest_template(
        mock_profile,
        "wisdom_trial"
    )
    
    # Check quest title and description
    assert "Fire" in template.title
    assert "mystical arts" in template.description.lower()
    
    # Check stage descriptions
    for stage in template.stages:
        assert "Fire" in stage.title
        assert mock_profile.governor_id in stage.description
        
        # Check challenge descriptions
        for challenge in stage.challenges:
            assert "fire" in challenge.description.lower()
            assert challenge.challenge_type.value in challenge.description.lower() 