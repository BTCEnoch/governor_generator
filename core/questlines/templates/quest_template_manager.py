"""
Quest Template Manager
Handles creation and management of quest templates based on governor profiles
"""

import json
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from datetime import datetime

from core.governors.profiles.analyzer import EnhancedProfile
from core.onchain.protocol.hypertoken_manager import TokenType, TokenState

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuestDifficulty(Enum):
    """Quest difficulty levels"""
    NOVICE = 1
    APPRENTICE = 2
    ADEPT = 3
    MASTER = 4
    GRANDMASTER = 5

class ChallengeType(Enum):
    """Types of challenges available in quests"""
    RITUAL = "ritual"
    PUZZLE = "puzzle"
    RIDDLE = "riddle"
    MEDITATION = "meditation"
    INVOCATION = "invocation"
    ALCHEMY = "alchemy"
    DIVINATION = "divination"
    ASTRAL = "astral"

@dataclass
class QuestReward:
    """Rewards granted for completing quest stages"""
    wisdom_tokens: int
    reputation_gain: int
    artifact_type: Optional[str] = None
    artifact_rarity: Optional[int] = None
    special_unlock: Optional[str] = None

@dataclass
class QuestChallenge:
    """Individual challenge within a quest"""
    challenge_type: ChallengeType
    difficulty: QuestDifficulty
    description: str
    success_criteria: Dict[str, Any]
    failure_conditions: Dict[str, Any]
    retry_allowed: bool
    energy_cost: int
    reward: QuestReward

@dataclass
class QuestStage:
    """Stage in a quest sequence"""
    stage_number: int
    title: str
    description: str
    challenges: List[QuestChallenge]
    required_items: List[str]
    required_reputation: int
    completion_criteria: Dict[str, Any]
    reward: QuestReward

@dataclass
class QuestTemplate:
    """Complete quest template"""
    template_id: str
    title: str
    description: str
    quest_type: str
    difficulty: QuestDifficulty
    stages: List[QuestStage]
    total_energy_required: int
    total_wisdom_reward: int
    reputation_requirement: int
    governor_id: str
    elemental_affinity: str
    voidmaker_tier: int  # 0-3, higher means more cosmic awareness content

class QuestTemplateManager:
    """
    Manages creation and customization of quest templates
    based on governor profiles and game mechanics
    """
    
    def __init__(self, template_dir: Path):
        """Initialize template manager"""
        self.template_dir = Path(template_dir)
        self.load_base_templates()
        logger.info("Initialized Quest Template Manager")
        
    def load_base_templates(self):
        """Load base quest template structures"""
        try:
            self.base_templates = {
                "wisdom_trial": {
                    "stages": 3,
                    "challenge_types": [
                        ChallengeType.MEDITATION,
                        ChallengeType.RIDDLE,
                        ChallengeType.DIVINATION
                    ],
                    "energy_scaling": 1.0
                },
                "elemental_journey": {
                    "stages": 4,
                    "challenge_types": [
                        ChallengeType.RITUAL,
                        ChallengeType.ALCHEMY,
                        ChallengeType.INVOCATION
                    ],
                    "energy_scaling": 1.2
                },
                "astral_quest": {
                    "stages": 5,
                    "challenge_types": [
                        ChallengeType.ASTRAL,
                        ChallengeType.MEDITATION,
                        ChallengeType.DIVINATION
                    ],
                    "energy_scaling": 1.5
                }
            }
            logger.info("Loaded base quest templates")
        except Exception as e:
            logger.error(f"Failed to load base templates: {e}")
            raise
            
    def generate_quest_template(
        self,
        governor_profile: EnhancedProfile,
        quest_type: str
    ) -> QuestTemplate:
        """
        Generate a quest template based on governor profile
        """
        try:
            # Validate quest type
            if quest_type not in self.base_templates:
                raise ValueError(f"Invalid quest type: {quest_type}")
                
            # Get base template
            base = self.base_templates[quest_type]
            
            # Calculate difficulty
            difficulty = self._calculate_difficulty(governor_profile)
            
            # Generate stages
            stages = self._generate_stages(
                governor_profile,
                base["challenge_types"],
                base["stages"],
                difficulty
            )
            
            # Calculate rewards and requirements
            total_energy = self._calculate_total_energy(stages, base["energy_scaling"])
            total_wisdom = self._calculate_total_wisdom(stages, difficulty)
            rep_requirement = self._calculate_reputation_requirement(difficulty)
            
            # Create template
            template = QuestTemplate(
                template_id=self._generate_template_id(governor_profile.governor_id),
                title=self._generate_title(quest_type, governor_profile),
                description=self._generate_description(quest_type, governor_profile),
                quest_type=quest_type,
                difficulty=difficulty,
                stages=stages,
                total_energy_required=total_energy,
                total_wisdom_reward=total_wisdom,
                reputation_requirement=rep_requirement,
                governor_id=governor_profile.governor_id,
                elemental_affinity=governor_profile.elemental_essence.ruling_element,
                voidmaker_tier=self._calculate_voidmaker_tier(governor_profile)
            )
            
            logger.info(f"Generated template {template.template_id} for {governor_profile.governor_id}")
            return template
            
        except Exception as e:
            logger.error(f"Failed to generate quest template: {e}")
            raise
            
    def _calculate_difficulty(self, profile: EnhancedProfile) -> QuestDifficulty:
        """Calculate quest difficulty based on profile"""
        try:
            # Map profile difficulty (1-10) to QuestDifficulty enum
            difficulty_map = {
                range(1, 3): QuestDifficulty.NOVICE,
                range(3, 5): QuestDifficulty.APPRENTICE,
                range(5, 7): QuestDifficulty.ADEPT,
                range(7, 9): QuestDifficulty.MASTER,
                range(9, 11): QuestDifficulty.GRANDMASTER
            }
            
            for diff_range, quest_diff in difficulty_map.items():
                if profile.difficulty_scale in diff_range:
                    return quest_diff
                    
            return QuestDifficulty.ADEPT  # Default to middle difficulty
            
        except Exception as e:
            logger.error(f"Failed to calculate difficulty: {e}")
            return QuestDifficulty.ADEPT
            
    def _generate_stages(
        self,
        profile: EnhancedProfile,
        challenge_types: List[ChallengeType],
        num_stages: int,
        difficulty: QuestDifficulty
    ) -> List[QuestStage]:
        """Generate quest stages based on profile"""
        try:
            stages = []
            for i in range(num_stages):
                # Create challenges for this stage
                challenges = self._generate_challenges(
                    profile,
                    challenge_types,
                    difficulty,
                    stage_number=i
                )
                
                # Create stage reward
                reward = QuestReward(
                    wisdom_tokens=5 * difficulty.value * (i + 1),
                    reputation_gain=2 * difficulty.value,
                    artifact_type="mystical_orb" if i == num_stages - 1 else None,
                    artifact_rarity=difficulty.value if i == num_stages - 1 else None
                )
                
                # Create stage
                stage = QuestStage(
                    stage_number=i,
                    title=f"Stage {i + 1}: {self._generate_stage_title(profile, i)}",
                    description=self._generate_stage_description(profile, i),
                    challenges=challenges,
                    required_items=[],  # TODO: Implement item requirements
                    required_reputation=10 * i * difficulty.value,
                    completion_criteria={"all_challenges_complete": True},
                    reward=reward
                )
                
                stages.append(stage)
                
            return stages
            
        except Exception as e:
            logger.error(f"Failed to generate stages: {e}")
            raise
            
    def _generate_challenges(
        self,
        profile: EnhancedProfile,
        challenge_types: List[ChallengeType],
        difficulty: QuestDifficulty,
        stage_number: int
    ) -> List[QuestChallenge]:
        """Generate challenges for a stage"""
        try:
            challenges = []
            num_challenges = 1 + stage_number // 2  # More challenges in later stages
            
            for i in range(num_challenges):
                challenge_type = challenge_types[i % len(challenge_types)]
                
                challenge = QuestChallenge(
                    challenge_type=challenge_type,
                    difficulty=difficulty,
                    description=self._generate_challenge_description(
                        profile,
                        challenge_type,
                        stage_number
                    ),
                    success_criteria={"completion": 100},
                    failure_conditions={"attempts_remaining": 0},
                    retry_allowed=True,
                    energy_cost=5 * difficulty.value * (stage_number + 1),
                    reward=QuestReward(
                        wisdom_tokens=2 * difficulty.value,
                        reputation_gain=1 * difficulty.value
                    )
                )
                
                challenges.append(challenge)
                
            return challenges
            
        except Exception as e:
            logger.error(f"Failed to generate challenges: {e}")
            raise
            
    def _calculate_total_energy(self, stages: List[QuestStage], scaling: float) -> int:
        """Calculate total energy cost for quest"""
        try:
            total = 0
            for stage in stages:
                for challenge in stage.challenges:
                    total += challenge.energy_cost
            return int(total * scaling)
        except Exception as e:
            logger.error(f"Failed to calculate total energy: {e}")
            return 50  # Default value
            
    def _calculate_total_wisdom(self, stages: List[QuestStage], difficulty: QuestDifficulty) -> int:
        """Calculate total wisdom reward for quest"""
        try:
            total = 0
            for stage in stages:
                total += stage.reward.wisdom_tokens
                for challenge in stage.challenges:
                    total += challenge.reward.wisdom_tokens
            return total
        except Exception as e:
            logger.error(f"Failed to calculate total wisdom: {e}")
            return 20  # Default value
            
    def _calculate_reputation_requirement(self, difficulty: QuestDifficulty) -> int:
        """Calculate reputation requirement for quest"""
        try:
            return 10 * difficulty.value
        except Exception as e:
            logger.error(f"Failed to calculate reputation requirement: {e}")
            return 10  # Default value
            
    def _calculate_voidmaker_tier(self, profile: EnhancedProfile) -> int:
        """Calculate voidmaker content tier based on profile"""
        try:
            # Count non-empty voidmaker responses
            awareness = len([x for x in profile.void_awareness.cosmic_patterns if x])
            influence = len([x for x in profile.void_awareness.reality_influence if x])
            unity = len([x for x in profile.void_awareness.integration_unity if x])
            
            total = awareness + influence + unity
            
            # Map to 0-3 tier
            if total < 5:
                return 0
            elif total < 10:
                return 1
            elif total < 15:
                return 2
            return 3
            
        except Exception as e:
            logger.error(f"Failed to calculate voidmaker tier: {e}")
            return 0  # Default to no voidmaker content
            
    def _generate_template_id(self, governor_id: str) -> str:
        """Generate unique template ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"quest_{governor_id}_{timestamp}"
        
    def _generate_title(self, quest_type: str, profile: EnhancedProfile) -> str:
        """Generate quest title"""
        element = profile.elemental_essence.ruling_element.capitalize()
        if quest_type == "wisdom_trial":
            return f"Trial of {element} Wisdom"
        elif quest_type == "elemental_journey":
            return f"Journey through the {element} Realm"
        elif quest_type == "astral_quest":
            return f"Astral Voyage of {element} Mastery"
        return f"Quest of {element} Mystery"
        
    def _generate_description(self, quest_type: str, profile: EnhancedProfile) -> str:
        """Generate quest description"""
        element = profile.elemental_essence.ruling_element.capitalize()
        domain = profile.wisdom_foundation.primary_domain.capitalize()
        return f"A {quest_type.replace('_', ' ')} of {element} mastery guided by {profile.governor_id}, master of {domain}"
        
    def _generate_stage_title(self, profile: EnhancedProfile, stage_number: int) -> str:
        """Generate stage title"""
        element = profile.elemental_essence.ruling_element.capitalize()
        return f"The {element} Path - Stage {stage_number + 1}"
        
    def _generate_stage_description(self, profile: EnhancedProfile, stage_number: int) -> str:
        """Generate stage description"""
        element = profile.elemental_essence.ruling_element.capitalize()
        return f"Stage {stage_number + 1} of your journey with {profile.governor_id} through the realm of {element}"
        
    def _generate_challenge_description(
        self,
        profile: EnhancedProfile,
        challenge_type: ChallengeType,
        stage_number: int
    ) -> str:
        """Generate challenge description"""
        element = profile.elemental_essence.ruling_element
        return f"A {challenge_type.value} challenge in the realm of {element}" 