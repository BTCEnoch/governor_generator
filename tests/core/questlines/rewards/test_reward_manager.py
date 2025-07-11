"""
Tests for Quest Reward Manager
"""

import pytest
from datetime import datetime
from core.questlines.rewards.reward_manager import (
    RewardManager,
    RewardType,
    QuestReward,
    RewardPool
)
from core.questlines.templates.quest_template_manager import (
    QuestDifficulty,
    QuestChallenge,
    ChallengeType,
    QuestReward as TemplateQuestReward
)

@pytest.fixture
def reward_manager():
    """Create reward manager instance for testing"""
    return RewardManager()

@pytest.fixture
def template_quest_reward():
    """Create a template quest reward for testing"""
    return TemplateQuestReward(
        wisdom_tokens=100,
        reputation_gain=50
    )

@pytest.fixture
def quest_challenge(template_quest_reward):
    """Create a quest challenge for testing"""
    def _create_challenge(challenge_type: ChallengeType, difficulty: QuestDifficulty):
        return QuestChallenge(
            challenge_type=challenge_type,
            difficulty=difficulty,
            description=f"Test {challenge_type.value} challenge",
            success_criteria={"condition": "test"},
            failure_conditions={"condition": "test"},
            retry_allowed=True,
            energy_cost=100,
            reward=template_quest_reward
        )
    return _create_challenge

def test_reward_types():
    """Test reward type enumeration"""
    assert RewardType.ENERGY.value == "energy"
    assert RewardType.KNOWLEDGE.value == "knowledge"
    assert RewardType.ARTIFACT.value == "artifact"
    assert RewardType.INFLUENCE.value == "influence"
    assert RewardType.MASTERY.value == "mastery"
    assert RewardType.TOKEN.value == "token"

def test_quest_reward_creation():
    """Test creation of individual rewards"""
    reward = QuestReward(
        reward_type=RewardType.ENERGY,
        amount=100,
        description="Test reward"
    )
    
    assert reward.reward_type == RewardType.ENERGY
    assert reward.amount == 100
    assert reward.description == "Test reward"
    assert not reward.claimed
    assert isinstance(reward.timestamp, datetime)

def test_reward_pool_creation():
    """Test creation of reward pools"""
    base_rewards = [
        QuestReward(RewardType.ENERGY, 100, "Base energy"),
        QuestReward(RewardType.KNOWLEDGE, 1, "Base knowledge")
    ]
    
    bonus_rewards = [
        QuestReward(RewardType.ARTIFACT, 1, "Bonus artifact")
    ]
    
    pool = RewardPool(
        base_rewards=base_rewards,
        bonus_rewards=bonus_rewards
    )
    
    assert len(pool.base_rewards) == 2
    assert len(pool.bonus_rewards) == 1
    assert pool.completion_threshold == 0.7
    assert pool.bonus_threshold == 0.9

def test_generate_reward_pool_novice(reward_manager, quest_challenge):
    """Test reward generation for novice difficulty"""
    challenges = [
        quest_challenge(ChallengeType.RITUAL, QuestDifficulty.NOVICE),
        quest_challenge(ChallengeType.PUZZLE, QuestDifficulty.NOVICE)
    ]
    
    pool = reward_manager.generate_reward_pool(
        difficulty=QuestDifficulty.NOVICE,
        challenges=challenges
    )
    
    # Verify base rewards exist
    assert any(r.reward_type == RewardType.ENERGY for r in pool.base_rewards)
    assert any(r.reward_type == RewardType.KNOWLEDGE for r in pool.base_rewards)
    
    # Verify challenge rewards
    assert ChallengeType.RITUAL.value in pool.challenge_rewards
    assert ChallengeType.PUZZLE.value in pool.challenge_rewards

def test_generate_reward_pool_grandmaster(reward_manager, quest_challenge):
    """Test reward generation for grandmaster difficulty"""
    challenges = [
        quest_challenge(ChallengeType.RITUAL, QuestDifficulty.GRANDMASTER),
        quest_challenge(ChallengeType.RIDDLE, QuestDifficulty.GRANDMASTER)
    ]
    
    pool = reward_manager.generate_reward_pool(
        difficulty=QuestDifficulty.GRANDMASTER,
        challenges=challenges,
        governor_influence=1.5
    )
    
    # Verify increased rewards for grandmaster
    energy_reward = next(r for r in pool.base_rewards if r.reward_type == RewardType.ENERGY)
    assert energy_reward.amount >= 1000  # Base amount for grandmaster
    
    # Verify bonus rewards
    assert any(r.reward_type == RewardType.ARTIFACT for r in pool.bonus_rewards)
    assert any(r.reward_type == RewardType.TOKEN for r in pool.bonus_rewards)

def test_reward_scaling(reward_manager, quest_challenge):
    """Test reward scaling based on difficulty and governor influence"""
    # Test with different governor influences
    pool_normal = reward_manager.generate_reward_pool(
        difficulty=QuestDifficulty.ADEPT,
        challenges=[quest_challenge(ChallengeType.MEDITATION, QuestDifficulty.ADEPT)],
        governor_influence=1.0
    )
    
    pool_high = reward_manager.generate_reward_pool(
        difficulty=QuestDifficulty.ADEPT,
        challenges=[quest_challenge(ChallengeType.MEDITATION, QuestDifficulty.ADEPT)],
        governor_influence=2.0
    )
    
    # High influence should give more rewards
    energy_normal = next(r for r in pool_normal.base_rewards if r.reward_type == RewardType.ENERGY)
    energy_high = next(r for r in pool_high.base_rewards if r.reward_type == RewardType.ENERGY)
    assert energy_high.amount > energy_normal.amount

def test_calculate_rewards(reward_manager, quest_challenge):
    """Test reward calculation based on completion"""
    challenges = [
        quest_challenge(ChallengeType.RITUAL, QuestDifficulty.MASTER),
        quest_challenge(ChallengeType.PUZZLE, QuestDifficulty.MASTER)
    ]
    
    pool = reward_manager.generate_reward_pool(
        difficulty=QuestDifficulty.MASTER,
        challenges=challenges
    )
    
    # Test partial completion (below threshold)
    partial_rewards = reward_manager.calculate_rewards(
        reward_pool=pool,
        completion_percentage=0.5,
        challenges_completed=set()
    )
    assert len(partial_rewards) == 0
    
    # Test base completion
    base_rewards = reward_manager.calculate_rewards(
        reward_pool=pool,
        completion_percentage=0.8,
        challenges_completed={ChallengeType.RITUAL.value}
    )
    assert len(base_rewards) > 0
    assert all(r.claimed for r in base_rewards)
    
    # Test full completion with all challenges
    full_rewards = reward_manager.calculate_rewards(
        reward_pool=pool,
        completion_percentage=1.0,
        challenges_completed={
            ChallengeType.RITUAL.value,
            ChallengeType.PUZZLE.value
        }
    )
    assert len(full_rewards) > len(base_rewards)

def test_challenge_specific_rewards(reward_manager, quest_challenge):
    """Test generation of challenge-specific rewards"""
    # Test ritual challenges
    pool = reward_manager.generate_reward_pool(
        difficulty=QuestDifficulty.MASTER,
        challenges=[quest_challenge(ChallengeType.RITUAL, QuestDifficulty.MASTER)]
    )
    
    ritual_rewards = pool.challenge_rewards[ChallengeType.RITUAL.value]
    assert any(r.reward_type == RewardType.KNOWLEDGE for r in ritual_rewards)
    assert any(r.reward_type == RewardType.ARTIFACT for r in ritual_rewards)
    
    # Test puzzle challenges
    pool = reward_manager.generate_reward_pool(
        difficulty=QuestDifficulty.MASTER,
        challenges=[quest_challenge(ChallengeType.PUZZLE, QuestDifficulty.MASTER)]
    )
    
    puzzle_rewards = pool.challenge_rewards[ChallengeType.PUZZLE.value]
    assert any(r.reward_type == RewardType.ENERGY for r in puzzle_rewards)
    assert any(r.reward_type == RewardType.MASTERY for r in puzzle_rewards)

def test_governor_influence_bounds(reward_manager, quest_challenge):
    """Test that governor influence is properly bounded"""
    challenge = quest_challenge(ChallengeType.MEDITATION, QuestDifficulty.ADEPT)
    
    # Test lower bound
    pool_low = reward_manager.generate_reward_pool(
        difficulty=QuestDifficulty.ADEPT,
        challenges=[challenge],
        governor_influence=0.1  # Should be capped at 0.5
    )
    
    # Test upper bound
    pool_high = reward_manager.generate_reward_pool(
        difficulty=QuestDifficulty.ADEPT,
        challenges=[challenge],
        governor_influence=3.0  # Should be capped at 2.0
    )
    
    energy_low = next(r for r in pool_low.base_rewards if r.reward_type == RewardType.ENERGY)
    energy_high = next(r for r in pool_high.base_rewards if r.reward_type == RewardType.ENERGY)
    
    # High influence (2.0) vs low influence (0.5) should give 4x difference
    # But we also need to account for challenge bonus (0.2 for MEDITATION)
    # So ratio is (1.5 * 1.2 * 2.0) / (1.5 * 1.2 * 0.5) = 4.0
    assert abs(energy_high.amount / energy_low.amount - 4.0) < 0.01  # Allow for rounding 