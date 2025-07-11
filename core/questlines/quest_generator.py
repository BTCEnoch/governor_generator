"""
Quest Generator
Combines quest templates and story trees to generate complete quests
"""

import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from datetime import datetime

from core.questlines.templates.quest_template_manager import (
    QuestTemplateManager,
    QuestTemplate,
    QuestDifficulty,
    ChallengeType
)
from core.questlines.story_tree import (
    StoryTree,
    StoryNode,
    StoryNodeType,
    StoryNodeState,
    StoryRequirement
)
from core.governors.profiles.analyzer import EnhancedProfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuestGenerationStrategy(Enum):
    """Different strategies for generating quests"""
    SINGLE = "single"  # Single quest with no branches
    BRANCHING = "branching"  # Quest with choice-based branches
    CONDITIONAL = "conditional"  # Quest with condition-based paths
    PROGRESSIVE = "progressive"  # Series of connected quests
    COLLABORATIVE = "collaborative"  # Multi-governor quest chain

@dataclass
class QuestGenerationConfig:
    """Configuration for quest generation"""
    strategy: QuestGenerationStrategy
    min_stages: int = 3
    max_stages: int = 7
    allow_branches: bool = True
    allow_conditions: bool = True
    min_difficulty: QuestDifficulty = QuestDifficulty.NOVICE
    max_difficulty: QuestDifficulty = QuestDifficulty.GRANDMASTER
    required_challenge_types: Set[ChallengeType] = field(default_factory=set)
    required_governors: Set[str] = field(default_factory=set)
    story_title: str = ""
    story_description: str = ""

class QuestGenerator:
    """
    Generates complete quests by combining templates and story trees
    """
    
    def __init__(
        self,
        template_manager: QuestTemplateManager,
        base_dir: Path
    ):
        """Initialize quest generator"""
        self.template_manager = template_manager
        self.base_dir = Path(base_dir)
        logger.info("Initialized Quest Generator")
        
    def generate_quest_line(
        self,
        governor_profile: EnhancedProfile,
        config: QuestGenerationConfig
    ) -> StoryTree:
        """Generate a complete quest line"""
        try:
            # Create story tree
            story_tree = StoryTree(self.base_dir / "stories")
            root_id = story_tree.create_story_tree(
                config.story_title or f"Quest Line of {governor_profile.governor_id}",
                config.story_description or f"A mystical journey guided by {governor_profile.governor_id}"
            )
            
            # Generate based on strategy
            if config.strategy == QuestGenerationStrategy.SINGLE:
                self._generate_single_quest(story_tree, root_id, governor_profile, config)
            elif config.strategy == QuestGenerationStrategy.BRANCHING:
                self._generate_branching_quest(story_tree, root_id, governor_profile, config)
            elif config.strategy == QuestGenerationStrategy.CONDITIONAL:
                self._generate_conditional_quest(story_tree, root_id, governor_profile, config)
            elif config.strategy == QuestGenerationStrategy.PROGRESSIVE:
                self._generate_progressive_quest(story_tree, root_id, governor_profile, config)
            elif config.strategy == QuestGenerationStrategy.COLLABORATIVE:
                self._generate_collaborative_quest(story_tree, root_id, governor_profile, config)
                
            logger.info(f"Generated quest line for {governor_profile.governor_id}")
            return story_tree
            
        except Exception as e:
            logger.error(f"Failed to generate quest line: {e}")
            raise
            
    def _generate_single_quest(
        self,
        story_tree: StoryTree,
        parent_id: str,
        profile: EnhancedProfile,
        config: QuestGenerationConfig
    ) -> None:
        """Generate a single linear quest"""
        try:
            # Generate quest template
            template = self.template_manager.generate_quest_template(
                profile,
                "wisdom_trial"  # Simple quest type for single quests
            )
            
            # Add quest node
            quest_id = story_tree.add_quest_node(parent_id, template)
            
            # Add reward node
            story_tree.add_reward_node(
                quest_id,
                "Quest Completion",
                f"Complete {template.title}",
                {
                    "wisdom": template.total_wisdom_reward,
                    "reputation": template.reputation_requirement
                }
            )
            
            logger.info(f"Generated single quest {quest_id}")
            
        except Exception as e:
            logger.error(f"Failed to generate single quest: {e}")
            raise
            
    def _generate_branching_quest(
        self,
        story_tree: StoryTree,
        parent_id: str,
        profile: EnhancedProfile,
        config: QuestGenerationConfig
    ) -> None:
        """Generate a quest with choice-based branches"""
        try:
            # Generate initial quest
            template = self.template_manager.generate_quest_template(
                profile,
                "elemental_journey"
            )
            quest_id = story_tree.add_quest_node(parent_id, template)
            
            # Add choice node
            choices = {
                "wisdom": "Path of Wisdom",
                "power": "Path of Power",
                "balance": "Path of Balance"
            }
            choice_id = story_tree.add_choice_node(
                quest_id,
                "Choose Your Path",
                "Select the path that resonates with your spirit",
                choices
            )
            
            # Generate branch quests
            for path, description in choices.items():
                # Create quest for this path
                branch_template = self.template_manager.generate_quest_template(
                    profile,
                    "astral_quest"
                )
                
                # Add requirements based on choice
                requirements = StoryRequirement(
                    required_choices={choice_id: path}
                )
                
                # Add branch quest
                branch_id = story_tree.add_quest_node(
                    choice_id,
                    branch_template,
                    requirements
                )
                
                # Add reward for this branch
                story_tree.add_reward_node(
                    branch_id,
                    f"Rewards of the {description}",
                    f"Rewards for completing the {description}",
                    {
                        "wisdom": branch_template.total_wisdom_reward,
                        "reputation": branch_template.reputation_requirement,
                        path: 100  # Special reward for chosen path
                    }
                )
                
            logger.info(f"Generated branching quest from {quest_id}")
            
        except Exception as e:
            logger.error(f"Failed to generate branching quest: {e}")
            raise
            
    def _generate_conditional_quest(
        self,
        story_tree: StoryTree,
        parent_id: str,
        profile: EnhancedProfile,
        config: QuestGenerationConfig
    ) -> None:
        """Generate a quest with condition-based paths"""
        try:
            # Generate initial quest
            template = self.template_manager.generate_quest_template(
                profile,
                "wisdom_trial"
            )
            quest_id = story_tree.add_quest_node(parent_id, template)
            
            # Add condition node
            conditions = {
                "has_wisdom": True,
                "has_power": True,
                "has_artifact": True
            }
            condition_id = story_tree.add_condition_node(
                quest_id,
                "Path Requirements",
                "Your path will be determined by your current abilities",
                conditions
            )
            
            # Generate conditional quests
            for condition, required in conditions.items():
                # Create quest for this condition
                cond_template = self.template_manager.generate_quest_template(
                    profile,
                    "elemental_journey"
                )
                
                # Add requirements
                requirements = StoryRequirement(
                    required_quests=[quest_id]
                )
                
                # Add conditional quest
                cond_id = story_tree.add_quest_node(
                    condition_id,
                    cond_template,
                    requirements
                )
                
                # Add reward
                story_tree.add_reward_node(
                    cond_id,
                    f"Mastery of {condition.replace('_', ' ').title()}",
                    f"Rewards for mastering {condition.replace('_', ' ')}",
                    {
                        "wisdom": cond_template.total_wisdom_reward,
                        "reputation": cond_template.reputation_requirement,
                        condition: 100
                    }
                )
                
            logger.info(f"Generated conditional quest from {quest_id}")
            
        except Exception as e:
            logger.error(f"Failed to generate conditional quest: {e}")
            raise
            
    def _generate_progressive_quest(
        self,
        story_tree: StoryTree,
        parent_id: str,
        profile: EnhancedProfile,
        config: QuestGenerationConfig
    ) -> None:
        """Generate a series of connected quests"""
        try:
            prev_id = parent_id
            quest_types = ["wisdom_trial", "elemental_journey", "astral_quest"]
            
            for i, quest_type in enumerate(quest_types):
                # Generate quest template
                template = self.template_manager.generate_quest_template(
                    profile,
                    quest_type
                )
                
                # Add requirements if not first quest
                requirements = None
                if i > 0:
                    requirements = StoryRequirement(
                        required_quests=[prev_id],
                        required_reputation=10 * i
                    )
                
                # Add quest node
                quest_id = story_tree.add_quest_node(
                    parent_id,
                    template,
                    requirements
                )
                
                # Add intermediate reward
                story_tree.add_reward_node(
                    quest_id,
                    f"Stage {i + 1} Completion",
                    f"Rewards for completing {template.title}",
                    {
                        "wisdom": template.total_wisdom_reward,
                        "reputation": template.reputation_requirement,
                        "progress": (i + 1) * 33  # Progress percentage
                    }
                )
                
                prev_id = quest_id
                
            # Add final reward
            story_tree.add_reward_node(
                prev_id,
                "Journey Completion",
                "Rewards for completing the entire journey",
                {
                    "wisdom": 1000,
                    "reputation": 500,
                    "mastery": True
                }
            )
            
            logger.info(f"Generated progressive quest chain from {parent_id}")
            
        except Exception as e:
            logger.error(f"Failed to generate progressive quest: {e}")
            raise
            
    def _generate_collaborative_quest(
        self,
        story_tree: StoryTree,
        parent_id: str,
        profile: EnhancedProfile,
        config: QuestGenerationConfig
    ) -> None:
        """Generate a multi-governor quest chain"""
        try:
            if not config.required_governors:
                raise ValueError("Required governors not specified for collaborative quest")
                
            # Generate hub quest
            hub_template = self.template_manager.generate_quest_template(
                profile,
                "wisdom_trial"
            )
            hub_id = story_tree.add_quest_node(parent_id, hub_template)
            
            # Generate spoke quests for each required governor
            for governor_id in config.required_governors:
                # Create requirements
                requirements = StoryRequirement(
                    required_quests=[hub_id],
                    required_governors=[governor_id]
                )
                
                # Generate quest template
                spoke_template = self.template_manager.generate_quest_template(
                    profile,  # Use main profile but could be modified for other governors
                    "elemental_journey"
                )
                
                # Add spoke quest
                spoke_id = story_tree.add_quest_node(
                    hub_id,
                    spoke_template,
                    requirements
                )
                
                # Add reward
                story_tree.add_reward_node(
                    spoke_id,
                    f"Alliance with {governor_id}",
                    f"Rewards for completing tasks with {governor_id}",
                    {
                        "wisdom": spoke_template.total_wisdom_reward,
                        "reputation": spoke_template.reputation_requirement,
                        "alliance": 100
                    }
                )
                
            # Add final collaborative reward
            story_tree.add_reward_node(
                hub_id,
                "Grand Alliance",
                "Rewards for forging alliances with all governors",
                {
                    "wisdom": 2000,
                    "reputation": 1000,
                    "grand_alliance": True
                }
            )
            
            logger.info(f"Generated collaborative quest chain from {hub_id}")
            
        except Exception as e:
            logger.error(f"Failed to generate collaborative quest: {e}")
            raise 