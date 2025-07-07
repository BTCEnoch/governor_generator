"""
Tests for Quest State Manager
"""

import pytest
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch

from core.questlines.state_manager import (
    QuestStateManager,
    QuestProgress,
    StageProgress,
    ChallengeProgress,
    QuestProgressState
)

from core.questlines.story_tree import (
    StoryTree,
    StoryNode,
    StoryNodeType,
    StoryNodeState,
    StoryRequirement
)

from core.questlines.templates.quest_template_manager import (
    QuestTemplate,
    QuestStage,
    QuestChallenge,
    QuestDifficulty,
    ChallengeType,
    QuestReward
)

# Test fixtures
@pytest.fixture
def state_dir(tmp_path):
    """Create temporary directory for state files"""
    return tmp_path

@pytest.fixture
def state_manager(state_dir):
    """Create state manager instance"""
    return QuestStateManager(state_dir)

@pytest.fixture
def mock_quest_template():
    """Create mock quest template"""
    return QuestTemplate(
        template_id="test_template_001",
        title="Test Quest",
        description="A test quest",
        quest_type="wisdom_trial",
        difficulty=QuestDifficulty.ADEPT,
        stages=[
            QuestStage(
                stage_number=0,
                title="Test Stage 1",
                description="First test stage",
                challenges=[
                    QuestChallenge(
                        challenge_type=ChallengeType.RITUAL,
                        difficulty=QuestDifficulty.ADEPT,
                        description="Test Challenge",
                        success_criteria={"completion": 100},
                        failure_conditions={"attempts": 0},
                        retry_allowed=True,
                        energy_cost=10,
                        reward=QuestReward(
                            wisdom_tokens=5,
                            reputation_gain=2
                        )
                    )
                ],
                required_items=[],
                required_reputation=0,
                completion_criteria={"all_challenges_complete": True},
                reward=QuestReward(
                    wisdom_tokens=10,
                    reputation_gain=5
                )
            )
        ],
        total_energy_required=100,
        total_wisdom_reward=50,
        reputation_requirement=10,
        governor_id="TEST_GOV_001",
        elemental_affinity="water",
        voidmaker_tier=1
    )

@pytest.fixture
def mock_story_tree(mock_quest_template):
    """Create mock story tree"""
    tree = StoryTree(Path("/mock/path"))
    root_id = tree.create_story_tree("Test Story", "A test story")
    quest_id = tree.add_quest_node(root_id, mock_quest_template)
    return tree, quest_id

def test_load_story_tree(state_manager, mock_story_tree):
    """Test loading story tree"""
    tree, _ = mock_story_tree
    state_manager.load_story_tree("test_tree", tree)
    assert "test_tree" in state_manager.story_trees

def test_start_quest(state_manager, mock_story_tree):
    """Test starting a quest"""
    tree, quest_id = mock_story_tree
    state_manager.load_story_tree("test_tree", tree)
    
    progress = state_manager.start_quest("test_tree", quest_id, 200)
    
    assert progress.quest_id == quest_id
    assert progress.current_stage == 0
    assert progress.state == QuestProgressState.REQUIREMENTS_CHECK
    assert progress.start_timestamp is not None
    assert len(progress.stages_progress) == 1
    assert progress.total_energy_spent == 0

def test_start_quest_insufficient_energy(state_manager, mock_story_tree):
    """Test starting quest with insufficient energy"""
    tree, quest_id = mock_story_tree
    state_manager.load_story_tree("test_tree", tree)
    
    with pytest.raises(ValueError):
        state_manager.start_quest("test_tree", quest_id, 50)

def test_start_challenge(state_manager, mock_story_tree):
    """Test starting a challenge"""
    tree, quest_id = mock_story_tree
    state_manager.load_story_tree("test_tree", tree)
    
    # Start quest
    progress = state_manager.start_quest("test_tree", quest_id, 200)
    
    # Start challenge
    challenge_id = "0_ritual"
    challenge_progress = state_manager.start_challenge(
        quest_id,
        0,
        challenge_id,
        100
    )
    
    assert challenge_progress.challenge_id == challenge_id
    assert challenge_progress.state == QuestProgressState.CHALLENGE_ACTIVE
    assert challenge_progress.attempts_remaining == 3
    assert challenge_progress.current_progress == 0

def test_update_challenge_progress(state_manager, mock_story_tree):
    """Test updating challenge progress"""
    tree, quest_id = mock_story_tree
    state_manager.load_story_tree("test_tree", tree)
    
    # Start quest and challenge
    state_manager.start_quest("test_tree", quest_id, 200)
    challenge_id = "0_ritual"
    state_manager.start_challenge(quest_id, 0, challenge_id, 100)
    
    # Update progress
    challenge_progress = state_manager.update_challenge_progress(
        quest_id,
        0,
        challenge_id,
        50,
        5
    )
    
    assert challenge_progress.current_progress == 50
    assert challenge_progress.energy_spent == 5
    assert challenge_progress.state == QuestProgressState.CHALLENGE_ACTIVE

def test_complete_challenge(state_manager, mock_story_tree):
    """Test completing a challenge"""
    tree, quest_id = mock_story_tree
    state_manager.load_story_tree("test_tree", tree)
    
    # Start quest and challenge
    state_manager.start_quest("test_tree", quest_id, 200)
    challenge_id = "0_ritual"
    state_manager.start_challenge(quest_id, 0, challenge_id, 100)
    
    # Complete challenge
    challenge_progress = state_manager.update_challenge_progress(
        quest_id,
        0,
        challenge_id,
        100,
        10
    )
    
    assert challenge_progress.state == QuestProgressState.CHALLENGE_COMPLETE
    assert challenge_progress.completion_timestamp is not None

def test_fail_challenge(state_manager, mock_story_tree):
    """Test failing a challenge"""
    tree, quest_id = mock_story_tree
    state_manager.load_story_tree("test_tree", tree)
    
    # Start quest and challenge
    state_manager.start_quest("test_tree", quest_id, 200)
    challenge_id = "0_ritual"
    state_manager.start_challenge(quest_id, 0, challenge_id, 100)
    
    # Fail challenge
    challenge_progress = state_manager.fail_challenge(
        quest_id,
        0,
        challenge_id
    )
    
    assert challenge_progress.state == QuestProgressState.FAILED
    assert challenge_progress.attempts_remaining == 2
    assert challenge_progress.failure_timestamp is not None

def test_complete_quest(state_manager, mock_story_tree):
    """Test completing a quest"""
    tree, quest_id = mock_story_tree
    state_manager.load_story_tree("test_tree", tree)
    
    # Start quest and challenge
    state_manager.start_quest("test_tree", quest_id, 200)
    challenge_id = "0_ritual"
    state_manager.start_challenge(quest_id, 0, challenge_id, 100)
    
    # Complete challenge and stage
    state_manager.update_challenge_progress(
        quest_id,
        0,
        challenge_id,
        100,
        10
    )
    
    # Complete quest
    quest_progress = state_manager.complete_quest(quest_id)
    
    assert quest_progress.state == QuestProgressState.COMPLETED
    assert quest_progress.completion_timestamp is not None

def test_save_and_load_progress(state_manager, mock_story_tree, state_dir):
    """Test saving and loading progress"""
    tree, quest_id = mock_story_tree
    state_manager.load_story_tree("test_tree", tree)
    
    # Create some progress
    state_manager.start_quest("test_tree", quest_id, 200)
    challenge_id = "0_ritual"
    state_manager.start_challenge(quest_id, 0, challenge_id, 100)
    state_manager.update_challenge_progress(
        quest_id,
        0,
        challenge_id,
        50,
        5
    )
    
    # Save progress
    state_manager.save_progress("test_progress.json")
    
    # Create new manager and load progress
    new_manager = QuestStateManager(state_dir)
    new_manager.load_progress("test_progress.json")
    
    # Verify loaded progress
    assert quest_id in new_manager.active_quests
    loaded_progress = new_manager.active_quests[quest_id]
    assert loaded_progress.current_stage == 0
    assert loaded_progress.total_energy_spent == 5
    
    challenge_progress = loaded_progress.stages_progress[0].challenges_progress[challenge_id]
    assert challenge_progress.current_progress == 50
    assert challenge_progress.energy_spent == 5

def test_invalid_story_tree(state_manager):
    """Test handling invalid story tree"""
    with pytest.raises(ValueError):
        state_manager.start_quest("invalid_tree", "quest_id", 100)

def test_invalid_quest(state_manager, mock_story_tree):
    """Test handling invalid quest"""
    tree, _ = mock_story_tree
    state_manager.load_story_tree("test_tree", tree)
    
    with pytest.raises(ValueError):
        state_manager.start_quest("test_tree", "invalid_quest", 100)

def test_invalid_challenge(state_manager, mock_story_tree):
    """Test handling invalid challenge"""
    tree, quest_id = mock_story_tree
    state_manager.load_story_tree("test_tree", tree)
    state_manager.start_quest("test_tree", quest_id, 200)
    
    with pytest.raises(ValueError):
        state_manager.start_challenge(quest_id, 0, "invalid_challenge", 100) 