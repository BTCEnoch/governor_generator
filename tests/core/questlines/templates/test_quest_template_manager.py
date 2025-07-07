"""
Tests for Quest Template Manager
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime

from core.questlines.templates.quest_template_manager import (
    QuestTemplateManager,
    QuestTemplate,
    QuestStage,
    QuestChallenge,
    QuestReward,
    QuestDifficulty,
    ChallengeType
)

from core.governors.profiler.core.enhanced_profile_analyzer import (
    EnhancedGovernorProfile,
    WisdomFoundation,
    ElementalEssence,
    TeachingDoctrine,
    VoidmakerAwareness
)

# Sample test data
@pytest.fixture
def mock_governor_profile():
    """Create a mock governor profile for testing"""
    return EnhancedGovernorProfile(
        governor_id="TEST_GOV_001",
        wisdom_foundation=WisdomFoundation(
            chosen_traditions=["hermetic", "kabbalah"],
            philosophical_alignment="test alignment",
            indexed_links=["link1", "link2"],
            application_notes="test notes"
        ),
        elemental_essence=ElementalEssence(
            ruling_element="water",
            manifestation={"color": "blue", "motion": "flowing", "scent": "ocean"},
            tarot_key="The Star",
            sephirah="Binah",
            constellation="Pisces"
        ),
        teaching_doctrine=TeachingDoctrine(
            core_lesson="Flow like water",
            urgency_reason="Time of change",
            misconception="Force over flow",
            instruction_stages=["observe", "adapt", "flow"],
            enochian_terms=["ZONG", "GRAA"]
        ),
        voidmaker_awareness=VoidmakerAwareness(
            cosmic_patterns=["pattern1", "pattern2"],
            reality_influence=["influence1", "influence2"],
            integration_unity=["unity1", "unity2"],
            cryptic_knowledge=["secret1", "secret2"]
        ),
        preferred_utilities=["ritual", "puzzle"],
        narrative_tone="measured and philosophical",
        difficulty_scale=5
    )

@pytest.fixture
def template_manager():
    """Create template manager instance"""
    return QuestTemplateManager(Path("/mock/path"))

def test_init_template_manager(template_manager):
    """Test template manager initialization"""
    assert template_manager is not None
    assert hasattr(template_manager, "base_templates")
    assert "wisdom_trial" in template_manager.base_templates
    assert "elemental_journey" in template_manager.base_templates
    assert "astral_quest" in template_manager.base_templates

def test_calculate_difficulty(template_manager, mock_governor_profile):
    """Test difficulty calculation"""
    difficulty = template_manager._calculate_difficulty(mock_governor_profile)
    assert isinstance(difficulty, QuestDifficulty)
    assert difficulty == QuestDifficulty.ADEPT  # Based on difficulty_scale=5

def test_calculate_voidmaker_tier(template_manager, mock_governor_profile):
    """Test voidmaker tier calculation"""
    tier = template_manager._calculate_voidmaker_tier(mock_governor_profile)
    assert isinstance(tier, int)
    assert 0 <= tier <= 3
    assert tier > 0  # Should be > 0 given the mock data has voidmaker content

def test_generate_quest_template(template_manager, mock_governor_profile):
    """Test complete quest template generation"""
    template = template_manager.generate_quest_template(
        mock_governor_profile,
        "wisdom_trial"
    )
    
    assert isinstance(template, QuestTemplate)
    assert template.governor_id == mock_governor_profile.governor_id
    assert template.elemental_affinity == "water"
    assert len(template.stages) == template_manager.base_templates["wisdom_trial"]["stages"]
    assert template.total_energy_required > 0
    assert template.total_wisdom_reward > 0
    assert template.reputation_requirement > 0

def test_generate_stages(template_manager, mock_governor_profile):
    """Test stage generation"""
    difficulty = template_manager._calculate_difficulty(mock_governor_profile)
    challenge_types = [ChallengeType.RITUAL, ChallengeType.PUZZLE]
    
    stages = template_manager._generate_stages(
        mock_governor_profile,
        challenge_types,
        3,  # num_stages
        difficulty
    )
    
    assert isinstance(stages, list)
    assert len(stages) == 3
    for stage in stages:
        assert isinstance(stage, QuestStage)
        assert stage.challenges
        assert stage.reward
        assert stage.required_reputation >= 0

def test_generate_challenges(template_manager, mock_governor_profile):
    """Test challenge generation"""
    difficulty = template_manager._calculate_difficulty(mock_governor_profile)
    challenge_types = [ChallengeType.RITUAL, ChallengeType.PUZZLE]
    
    challenges = template_manager._generate_challenges(
        mock_governor_profile,
        challenge_types,
        difficulty,
        stage_number=0
    )
    
    assert isinstance(challenges, list)
    assert len(challenges) > 0
    for challenge in challenges:
        assert isinstance(challenge, QuestChallenge)
        assert challenge.energy_cost > 0
        assert challenge.reward.wisdom_tokens > 0
        assert challenge.reward.reputation_gain > 0

def test_calculate_total_energy(template_manager):
    """Test energy calculation"""
    stages = [
        QuestStage(
            stage_number=0,
            title="Test Stage",
            description="Test Description",
            challenges=[
                QuestChallenge(
                    challenge_type=ChallengeType.RITUAL,
                    difficulty=QuestDifficulty.ADEPT,
                    description="Test Challenge",
                    success_criteria={},
                    failure_conditions={},
                    retry_allowed=True,
                    energy_cost=10,
                    reward=QuestReward(wisdom_tokens=5, reputation_gain=2)
                )
            ],
            required_items=[],
            required_reputation=0,
            completion_criteria={},
            reward=QuestReward(wisdom_tokens=10, reputation_gain=5)
        )
    ]
    
    total = template_manager._calculate_total_energy(stages, 1.0)
    assert total == 10  # One challenge with cost 10, scaling 1.0

def test_calculate_total_wisdom(template_manager):
    """Test wisdom calculation"""
    stages = [
        QuestStage(
            stage_number=0,
            title="Test Stage",
            description="Test Description",
            challenges=[
                QuestChallenge(
                    challenge_type=ChallengeType.RITUAL,
                    difficulty=QuestDifficulty.ADEPT,
                    description="Test Challenge",
                    success_criteria={},
                    failure_conditions={},
                    retry_allowed=True,
                    energy_cost=10,
                    reward=QuestReward(wisdom_tokens=5, reputation_gain=2)
                )
            ],
            required_items=[],
            required_reputation=0,
            completion_criteria={},
            reward=QuestReward(wisdom_tokens=10, reputation_gain=5)
        )
    ]
    
    total = template_manager._calculate_total_wisdom(stages, QuestDifficulty.ADEPT)
    assert total == 15  # Stage reward (10) + challenge reward (5)

def test_invalid_quest_type(template_manager, mock_governor_profile):
    """Test handling of invalid quest type"""
    with pytest.raises(ValueError):
        template_manager.generate_quest_template(
            mock_governor_profile,
            "invalid_quest_type"
        )

def test_generate_template_id(template_manager):
    """Test template ID generation"""
    template_id = template_manager._generate_template_id("TEST_GOV_001")
    assert isinstance(template_id, str)
    assert "quest_TEST_GOV_001" in template_id
    assert datetime.now().strftime("%Y%m%d") in template_id

def test_title_generation(template_manager, mock_governor_profile):
    """Test quest title generation"""
    title = template_manager._generate_title("wisdom_trial", mock_governor_profile)
    assert isinstance(title, str)
    assert "Water" in title  # Should include elemental affinity
    assert "Trial" in title  # Should include quest type reference 