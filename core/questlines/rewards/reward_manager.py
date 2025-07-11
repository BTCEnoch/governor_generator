"""
Quest Reward Manager
Handles reward generation, scaling, and distribution for quests
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Any
from datetime import datetime

from core.questlines.templates.quest_template_manager import (
    QuestDifficulty,
    QuestChallenge,
    ChallengeType,
    QuestReward as TemplateQuestReward
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RewardType(Enum):
    """Types of rewards that can be granted"""
    ENERGY = "energy"  # Base energy currency
    KNOWLEDGE = "knowledge"  # Mystical knowledge/wisdom
    ARTIFACT = "artifact"  # Special items/relics
    INFLUENCE = "influence"  # Standing with governors
    MASTERY = "mastery"  # Skill/ability improvements
    TOKEN = "token"  # Special blockchain tokens

@dataclass
class QuestReward:
    """Represents a single reward instance"""
    reward_type: RewardType
    amount: int
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    claimed: bool = False

@dataclass
class RewardPool:
    """Collection of possible rewards for a quest"""
    base_rewards: List[QuestReward]
    bonus_rewards: List[QuestReward] = field(default_factory=list)
    challenge_rewards: Dict[str, List[QuestReward]] = field(default_factory=dict)
    completion_threshold: float = 0.7  # 70% completion needed for base rewards
    bonus_threshold: float = 0.9  # 90% completion needed for bonus rewards

class RewardManager:
    """Manages quest reward generation and distribution"""
    
    def __init__(self):
        self._difficulty_multipliers = {
            QuestDifficulty.NOVICE: 1.0,
            QuestDifficulty.ADEPT: 1.5,
            QuestDifficulty.MASTER: 2.0,
            QuestDifficulty.GRANDMASTER: 3.0
        }
        
        self._challenge_bonuses = {
            ChallengeType.RITUAL: 0.3,  # 30% bonus for ritual challenges
            ChallengeType.PUZZLE: 0.2,
            ChallengeType.RIDDLE: 0.25,
            ChallengeType.MEDITATION: 0.2,
            ChallengeType.INVOCATION: 0.25,
            ChallengeType.ALCHEMY: 0.2,
            ChallengeType.DIVINATION: 0.15,
            ChallengeType.ASTRAL: 0.3
        }
        
        # Base reward templates by difficulty
        self._base_reward_templates = self._initialize_reward_templates()
        
    def _initialize_reward_templates(self) -> Dict[QuestDifficulty, RewardPool]:
        """Initialize base reward templates for each difficulty level"""
        templates = {}
        
        # NOVICE rewards
        templates[QuestDifficulty.NOVICE] = RewardPool(
            base_rewards=[
                QuestReward(
                    reward_type=RewardType.ENERGY,
                    amount=100,
                    description="Basic energy reward"
                ),
                QuestReward(
                    reward_type=RewardType.KNOWLEDGE,
                    amount=1,
                    description="Fundamental mystical insight"
                )
            ],
            bonus_rewards=[
                QuestReward(
                    reward_type=RewardType.INFLUENCE,
                    amount=50,
                    description="Minor governor influence"
                )
            ]
        )
        
        # ADEPT rewards
        templates[QuestDifficulty.ADEPT] = RewardPool(
            base_rewards=[
                QuestReward(
                    reward_type=RewardType.ENERGY,
                    amount=250,
                    description="Enhanced energy reward"
                ),
                QuestReward(
                    reward_type=RewardType.KNOWLEDGE,
                    amount=2,
                    description="Advanced mystical knowledge"
                ),
                QuestReward(
                    reward_type=RewardType.INFLUENCE,
                    amount=100,
                    description="Moderate governor influence"
                )
            ],
            bonus_rewards=[
                QuestReward(
                    reward_type=RewardType.ARTIFACT,
                    amount=1,
                    description="Minor mystical artifact"
                )
            ]
        )
        
        # MASTER rewards
        templates[QuestDifficulty.MASTER] = RewardPool(
            base_rewards=[
                QuestReward(
                    reward_type=RewardType.ENERGY,
                    amount=500,
                    description="Substantial energy reward"
                ),
                QuestReward(
                    reward_type=RewardType.KNOWLEDGE,
                    amount=3,
                    description="Master-level mystical secrets"
                ),
                QuestReward(
                    reward_type=RewardType.INFLUENCE,
                    amount=200,
                    description="Significant governor influence"
                ),
                QuestReward(
                    reward_type=RewardType.MASTERY,
                    amount=1,
                    description="Mystical ability mastery"
                )
            ],
            bonus_rewards=[
                QuestReward(
                    reward_type=RewardType.ARTIFACT,
                    amount=1,
                    description="Powerful mystical artifact"
                ),
                QuestReward(
                    reward_type=RewardType.TOKEN,
                    amount=1,
                    description="Rare mystical token"
                )
            ]
        )
        
        # GRANDMASTER rewards
        templates[QuestDifficulty.GRANDMASTER] = RewardPool(
            base_rewards=[
                QuestReward(
                    reward_type=RewardType.ENERGY,
                    amount=1000,
                    description="Exceptional energy reward"
                ),
                QuestReward(
                    reward_type=RewardType.KNOWLEDGE,
                    amount=5,
                    description="Grandmaster mystical revelations"
                ),
                QuestReward(
                    reward_type=RewardType.INFLUENCE,
                    amount=500,
                    description="Major governor influence"
                ),
                QuestReward(
                    reward_type=RewardType.MASTERY,
                    amount=2,
                    description="Advanced mystical mastery"
                ),
                QuestReward(
                    reward_type=RewardType.TOKEN,
                    amount=2,
                    description="Exceptional mystical tokens"
                )
            ],
            bonus_rewards=[
                QuestReward(
                    reward_type=RewardType.ARTIFACT,
                    amount=2,
                    description="Legendary mystical artifacts"
                ),
                QuestReward(
                    reward_type=RewardType.TOKEN,
                    amount=1,
                    description="Unique mystical token"
                )
            ]
        )
        
        return templates
    
    def generate_reward_pool(
        self,
        difficulty: QuestDifficulty,
        challenges: List[QuestChallenge],
        governor_influence: float = 1.0
    ) -> RewardPool:
        """
        Generate a reward pool for a quest based on difficulty and challenges
        
        Args:
            difficulty: Quest difficulty level
            challenges: List of challenges in the quest
            governor_influence: Reward multiplier based on governor influence (0.5-2.0)
        
        Returns:
            RewardPool: Generated rewards for the quest
        """
        # Get base template
        base_template = self._base_reward_templates[difficulty]
        
        # Apply difficulty multiplier
        diff_multiplier = self._difficulty_multipliers[difficulty]
        
        # Calculate challenge bonus
        challenge_multiplier = 1.0
        for challenge in challenges:
            challenge_multiplier += self._challenge_bonuses.get(challenge.challenge_type, 0)
            
        # Apply governor influence (capped between 0.5 and 2.0)
        governor_multiplier = max(0.5, min(2.0, governor_influence))
        
        # Calculate final multiplier
        final_multiplier = diff_multiplier * challenge_multiplier * governor_multiplier
        
        # Generate scaled rewards
        scaled_rewards = self._scale_rewards(base_template, final_multiplier)
        
        # Add challenge-specific rewards
        challenge_rewards = self._generate_challenge_rewards(challenges, difficulty)
        scaled_rewards.challenge_rewards = challenge_rewards
        
        return scaled_rewards
    
    def _scale_rewards(self, template: RewardPool, multiplier: float) -> RewardPool:
        """Scale rewards based on the calculated multiplier"""
        scaled_base = []
        scaled_bonus = []
        
        # Scale base rewards
        for reward in template.base_rewards:
            # Round after all multiplications to maintain exact ratios
            scaled_amount = round(reward.amount * multiplier)
            scaled_reward = QuestReward(
                reward_type=reward.reward_type,
                amount=scaled_amount,
                description=reward.description,
                metadata=reward.metadata.copy()
            )
            scaled_base.append(scaled_reward)
            
        # Scale bonus rewards
        for reward in template.bonus_rewards:
            # Round after all multiplications to maintain exact ratios
            scaled_amount = round(reward.amount * multiplier)
            scaled_reward = QuestReward(
                reward_type=reward.reward_type,
                amount=scaled_amount,
                description=reward.description,
                metadata=reward.metadata.copy()
            )
            scaled_bonus.append(scaled_reward)
            
        return RewardPool(
            base_rewards=scaled_base,
            bonus_rewards=scaled_bonus,
            completion_threshold=template.completion_threshold,
            bonus_threshold=template.bonus_threshold
        )
    
    def _generate_challenge_rewards(
        self,
        challenges: List[QuestChallenge],
        difficulty: QuestDifficulty
    ) -> Dict[str, List[QuestReward]]:
        """Generate additional rewards specific to challenge types"""
        challenge_rewards = {}
        
        for challenge in challenges:
            rewards = []
            challenge_type = challenge.challenge_type
            
            if challenge_type == ChallengeType.RITUAL:
                # Ritual challenges grant knowledge and artifacts
                rewards.extend([
                    QuestReward(
                        reward_type=RewardType.KNOWLEDGE,
                        amount=difficulty.value,  # Scales with difficulty
                        description="Ritual knowledge reward"
                    ),
                    QuestReward(
                        reward_type=RewardType.ARTIFACT,
                        amount=1,
                        description="Ritual completion artifact"
                    )
                ])
                
            elif challenge_type == ChallengeType.PUZZLE:
                # Puzzles grant energy and mastery
                rewards.extend([
                    QuestReward(
                        reward_type=RewardType.ENERGY,
                        amount=100 * difficulty.value,
                        description="Puzzle completion energy"
                    ),
                    QuestReward(
                        reward_type=RewardType.MASTERY,
                        amount=1,
                        description="Puzzle-solving mastery"
                    )
                ])
                
            elif challenge_type == ChallengeType.RIDDLE:
                # Riddles grant knowledge and influence
                rewards.extend([
                    QuestReward(
                        reward_type=RewardType.KNOWLEDGE,
                        amount=difficulty.value + 1,
                        description="Riddle wisdom reward"
                    ),
                    QuestReward(
                        reward_type=RewardType.INFLUENCE,
                        amount=50 * difficulty.value,
                        description="Riddle-master influence"
                    )
                ])
                
            challenge_rewards[challenge_type.value] = rewards
            
        return challenge_rewards
    
    def calculate_rewards(
        self,
        reward_pool: RewardPool,
        completion_percentage: float,
        challenges_completed: Set[str]
    ) -> List[QuestReward]:
        """
        Calculate final rewards based on completion percentage and challenges
        
        Args:
            reward_pool: Available rewards for the quest
            completion_percentage: Overall quest completion (0.0-1.0)
            challenges_completed: Set of completed challenge IDs
            
        Returns:
            List[QuestReward]: Earned rewards
        """
        earned_rewards = []
        
        # Check base completion threshold
        if completion_percentage >= reward_pool.completion_threshold:
            earned_rewards.extend(reward_pool.base_rewards)
            
            # Check bonus threshold
            if completion_percentage >= reward_pool.bonus_threshold:
                earned_rewards.extend(reward_pool.bonus_rewards)
                
        # Add rewards for completed challenges
        for challenge_id in challenges_completed:
            if challenge_id in reward_pool.challenge_rewards:
                earned_rewards.extend(reward_pool.challenge_rewards[challenge_id])
                
        # Mark rewards as claimed
        for reward in earned_rewards:
            reward.claimed = True
            reward.timestamp = datetime.now()
            
        return earned_rewards 