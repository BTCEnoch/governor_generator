"""
Quest State Manager
Handles runtime state and progression of quests
"""

import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from datetime import datetime

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
    QuestDifficulty
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuestProgressState(Enum):
    """Detailed states for quest progress tracking"""
    NOT_STARTED = "not_started"
    REQUIREMENTS_CHECK = "requirements_check"
    STAGE_IN_PROGRESS = "stage_in_progress"
    CHALLENGE_ACTIVE = "challenge_active"
    CHALLENGE_COMPLETE = "challenge_complete"
    STAGE_COMPLETE = "stage_complete"
    REWARDS_PENDING = "rewards_pending"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class ChallengeProgress:
    """Tracks progress of an individual challenge"""
    challenge_id: str
    attempts_remaining: int
    current_progress: int
    energy_spent: int
    state: QuestProgressState
    completion_timestamp: Optional[datetime] = None
    failure_timestamp: Optional[datetime] = None

@dataclass
class StageProgress:
    """Tracks progress of a quest stage"""
    stage_number: int
    challenges_progress: Dict[str, ChallengeProgress] = field(default_factory=dict)
    state: QuestProgressState = QuestProgressState.NOT_STARTED
    start_timestamp: Optional[datetime] = None
    completion_timestamp: Optional[datetime] = None

@dataclass
class QuestProgress:
    """Tracks overall quest progress"""
    quest_id: str
    current_stage: int
    total_energy_spent: int
    stages_progress: Dict[int, StageProgress] = field(default_factory=dict)
    state: QuestProgressState = QuestProgressState.NOT_STARTED
    start_timestamp: Optional[datetime] = None
    completion_timestamp: Optional[datetime] = None

class QuestStateManager:
    """
    Manages the runtime state and progression of quests
    """
    
    def __init__(self, state_dir: Path):
        """Initialize state manager"""
        self.state_dir = Path(state_dir)
        self.active_quests: Dict[str, QuestProgress] = {}
        self.story_trees: Dict[str, StoryTree] = {}
        logger.info("Initialized Quest State Manager")
        
    def load_story_tree(self, tree_id: str, story_tree: StoryTree) -> None:
        """Load a story tree for state management"""
        try:
            self.story_trees[tree_id] = story_tree
            logger.info(f"Loaded story tree {tree_id}")
        except Exception as e:
            logger.error(f"Failed to load story tree: {e}")
            raise
            
    def start_quest(
        self,
        tree_id: str,
        quest_id: str,
        energy_available: int
    ) -> QuestProgress:
        """Start a new quest"""
        try:
            # Validate story tree exists
            if tree_id not in self.story_trees:
                raise ValueError(f"Story tree {tree_id} not found")
                
            story_tree = self.story_trees[tree_id]
            
            # Validate quest exists
            if quest_id not in story_tree.nodes:
                raise ValueError(f"Quest {quest_id} not found")
                
            quest_node = story_tree.nodes[quest_id]
            if quest_node.node_type != StoryNodeType.QUEST:
                raise ValueError(f"Node {quest_id} is not a quest")
                
            # Validate quest template exists
            if not quest_node.quest_template:
                raise ValueError(f"Quest {quest_id} has no template")
                
            # Check energy requirements
            if energy_available < quest_node.quest_template.total_energy_required:
                raise ValueError(
                    f"Insufficient energy. Required: {quest_node.quest_template.total_energy_required}, "
                    f"Available: {energy_available}"
                )
                
            # Create progress tracker
            progress = QuestProgress(
                quest_id=quest_id,
                current_stage=0,
                total_energy_spent=0,
                state=QuestProgressState.REQUIREMENTS_CHECK,
                start_timestamp=datetime.now()
            )
            
            # Initialize stage progress
            if not quest_node.quest_template.stages:
                raise ValueError(f"Quest {quest_id} template has no stages")
                
            for stage in quest_node.quest_template.stages:
                if not stage:
                    continue
                    
                stage_progress = StageProgress(stage_number=stage.stage_number)
                
                # Initialize challenge progress
                for challenge in stage.challenges:
                    if not challenge:
                        continue
                        
                    challenge_progress = ChallengeProgress(
                        challenge_id=f"{stage.stage_number}_{challenge.challenge_type.value}",
                        attempts_remaining=3,  # Default 3 attempts
                        current_progress=0,
                        energy_spent=0,
                        state=QuestProgressState.NOT_STARTED
                    )
                    stage_progress.challenges_progress[challenge_progress.challenge_id] = challenge_progress
                    
                progress.stages_progress[stage.stage_number] = stage_progress
                
            # Validate at least one stage was initialized
            if not progress.stages_progress:
                raise ValueError(f"Quest {quest_id} has no valid stages")
                
            # Add to active quests
            self.active_quests[quest_id] = progress
            
            # Update story tree state
            story_tree.update_node_state(quest_id, StoryNodeState.IN_PROGRESS)
            
            logger.info(f"Started quest {quest_id}")
            return progress
            
        except Exception as e:
            logger.error(f"Failed to start quest: {e}")
            raise
            
    def start_challenge(
        self,
        quest_id: str,
        stage_number: int,
        challenge_id: str,
        energy_available: int
    ) -> ChallengeProgress:
        """Start a challenge within a quest stage"""
        try:
            # Validate quest is active
            if quest_id not in self.active_quests:
                raise ValueError(f"Quest {quest_id} not active")
                
            quest_progress = self.active_quests[quest_id]
            
            # Validate stage
            if stage_number not in quest_progress.stages_progress:
                raise ValueError(f"Stage {stage_number} not found")
                
            stage_progress = quest_progress.stages_progress[stage_number]
            
            # Validate challenge
            if challenge_id not in stage_progress.challenges_progress:
                raise ValueError(f"Challenge {challenge_id} not found")
                
            challenge_progress = stage_progress.challenges_progress[challenge_id]
            
            # Check challenge can be started
            if challenge_progress.state not in [
                QuestProgressState.NOT_STARTED,
                QuestProgressState.FAILED
            ]:
                raise ValueError(f"Challenge {challenge_id} cannot be started")
                
            # Check attempts remaining
            if challenge_progress.attempts_remaining <= 0:
                raise ValueError(f"No attempts remaining for challenge {challenge_id}")
                
            # Update states
            challenge_progress.state = QuestProgressState.CHALLENGE_ACTIVE
            stage_progress.state = QuestProgressState.STAGE_IN_PROGRESS
            quest_progress.state = QuestProgressState.STAGE_IN_PROGRESS
            
            if not stage_progress.start_timestamp:
                stage_progress.start_timestamp = datetime.now()
                
            logger.info(f"Started challenge {challenge_id} in quest {quest_id}")
            return challenge_progress
            
        except Exception as e:
            logger.error(f"Failed to start challenge: {e}")
            raise
            
    def update_challenge_progress(
        self,
        quest_id: str,
        stage_number: int,
        challenge_id: str,
        progress_amount: int,
        energy_spent: int
    ) -> ChallengeProgress:
        """Update progress of an active challenge"""
        try:
            # Validate quest is active
            if quest_id not in self.active_quests:
                raise ValueError(f"Quest {quest_id} not active")
                
            quest_progress = self.active_quests[quest_id]
            
            # Validate stage
            if stage_number not in quest_progress.stages_progress:
                raise ValueError(f"Stage {stage_number} not found")
                
            stage_progress = quest_progress.stages_progress[stage_number]
            
            # Validate challenge
            if challenge_id not in stage_progress.challenges_progress:
                raise ValueError(f"Challenge {challenge_id} not found")
                
            challenge_progress = stage_progress.challenges_progress[challenge_id]
            
            # Check challenge is active
            if challenge_progress.state != QuestProgressState.CHALLENGE_ACTIVE:
                raise ValueError(f"Challenge {challenge_id} not active")
                
            # Update progress
            challenge_progress.current_progress += progress_amount
            challenge_progress.energy_spent += energy_spent
            quest_progress.total_energy_spent += energy_spent
            
            # Check for completion
            if challenge_progress.current_progress >= 100:
                challenge_progress.state = QuestProgressState.CHALLENGE_COMPLETE
                challenge_progress.completion_timestamp = datetime.now()
                
                # Check if stage is complete
                if all(
                    c.state == QuestProgressState.CHALLENGE_COMPLETE
                    for c in stage_progress.challenges_progress.values()
                ):
                    stage_progress.state = QuestProgressState.STAGE_COMPLETE
                    stage_progress.completion_timestamp = datetime.now()
                    
                    # Move to next stage or complete quest
                    if stage_number == len(quest_progress.stages_progress) - 1:
                        quest_progress.state = QuestProgressState.REWARDS_PENDING
                        quest_progress.completion_timestamp = datetime.now()
                    else:
                        quest_progress.current_stage += 1
                        
            logger.info(
                f"Updated challenge {challenge_id} progress: {challenge_progress.current_progress}%"
            )
            return challenge_progress
            
        except Exception as e:
            logger.error(f"Failed to update challenge progress: {e}")
            raise
            
    def fail_challenge(
        self,
        quest_id: str,
        stage_number: int,
        challenge_id: str
    ) -> ChallengeProgress:
        """Mark a challenge as failed"""
        try:
            # Validate quest is active
            if quest_id not in self.active_quests:
                raise ValueError(f"Quest {quest_id} not active")
                
            quest_progress = self.active_quests[quest_id]
            
            # Validate stage
            if stage_number not in quest_progress.stages_progress:
                raise ValueError(f"Stage {stage_number} not found")
                
            stage_progress = quest_progress.stages_progress[stage_number]
            
            # Validate challenge
            if challenge_id not in stage_progress.challenges_progress:
                raise ValueError(f"Challenge {challenge_id} not found")
                
            challenge_progress = stage_progress.challenges_progress[challenge_id]
            
            # Update challenge state
            challenge_progress.attempts_remaining -= 1
            challenge_progress.state = QuestProgressState.FAILED
            challenge_progress.failure_timestamp = datetime.now()
            
            # Check if quest fails
            if challenge_progress.attempts_remaining <= 0:
                quest_progress.state = QuestProgressState.FAILED
                
                # Update story tree state
                for tree in self.story_trees.values():
                    if quest_id in tree.nodes:
                        tree.update_node_state(quest_id, StoryNodeState.FAILED)
                        break
                        
            logger.info(f"Failed challenge {challenge_id} in quest {quest_id}")
            return challenge_progress
            
        except Exception as e:
            logger.error(f"Failed to fail challenge: {e}")
            raise
            
    def complete_quest(self, quest_id: str) -> QuestProgress:
        """Complete a quest and grant rewards"""
        try:
            # Validate quest is active
            if quest_id not in self.active_quests:
                raise ValueError(f"Quest {quest_id} not active")
                
            quest_progress = self.active_quests[quest_id]
            
            # Check quest is ready for completion
            if quest_progress.state != QuestProgressState.REWARDS_PENDING:
                raise ValueError(f"Quest {quest_id} not ready for completion")
                
            # Update quest state
            quest_progress.state = QuestProgressState.COMPLETED
            
            # Update story tree state
            for tree in self.story_trees.values():
                if quest_id in tree.nodes:
                    tree.update_node_state(quest_id, StoryNodeState.COMPLETED)
                    break
                    
            logger.info(f"Completed quest {quest_id}")
            return quest_progress
            
        except Exception as e:
            logger.error(f"Failed to complete quest: {e}")
            raise
            
    def save_progress(self, filename: str) -> None:
        """Save quest progress to file"""
        try:
            path = self.state_dir / filename
            
            # Convert to serializable format
            data = {
                quest_id: {
                    "quest_id": progress.quest_id,
                    "current_stage": progress.current_stage,
                    "total_energy_spent": progress.total_energy_spent,
                    "state": progress.state.value,
                    "start_timestamp": progress.start_timestamp.isoformat() if progress.start_timestamp else None,
                    "completion_timestamp": progress.completion_timestamp.isoformat() if progress.completion_timestamp else None,
                    "stages_progress": {
                        stage_num: {
                            "stage_number": stage.stage_number,
                            "state": stage.state.value,
                            "start_timestamp": stage.start_timestamp.isoformat() if stage.start_timestamp else None,
                            "completion_timestamp": stage.completion_timestamp.isoformat() if stage.completion_timestamp else None,
                            "challenges_progress": {
                                challenge_id: {
                                    "challenge_id": challenge.challenge_id,
                                    "attempts_remaining": challenge.attempts_remaining,
                                    "current_progress": challenge.current_progress,
                                    "energy_spent": challenge.energy_spent,
                                    "state": challenge.state.value,
                                    "completion_timestamp": challenge.completion_timestamp.isoformat() if challenge.completion_timestamp else None,
                                    "failure_timestamp": challenge.failure_timestamp.isoformat() if challenge.failure_timestamp else None
                                }
                                for challenge_id, challenge in stage.challenges_progress.items()
                            }
                        }
                        for stage_num, stage in progress.stages_progress.items()
                    }
                }
                for quest_id, progress in self.active_quests.items()
            }
            
            # Save to file
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Saved quest progress to {path}")
            
        except Exception as e:
            logger.error(f"Failed to save progress: {e}")
            raise
            
    def load_progress(self, filename: str) -> None:
        """Load quest progress from file"""
        try:
            path = self.state_dir / filename
            
            # Load from file
            with open(path, 'r') as f:
                data = json.load(f)
                
            # Clear existing progress
            self.active_quests.clear()
            
            # Reconstruct progress objects
            for quest_id, quest_data in data.items():
                # Create quest progress
                quest_progress = QuestProgress(
                    quest_id=quest_data["quest_id"],
                    current_stage=quest_data["current_stage"],
                    total_energy_spent=quest_data["total_energy_spent"],
                    state=QuestProgressState(quest_data["state"]),
                    start_timestamp=datetime.fromisoformat(quest_data["start_timestamp"]) if quest_data["start_timestamp"] else None,
                    completion_timestamp=datetime.fromisoformat(quest_data["completion_timestamp"]) if quest_data["completion_timestamp"] else None
                )
                
                # Reconstruct stages
                for stage_num, stage_data in quest_data["stages_progress"].items():
                    stage_progress = StageProgress(
                        stage_number=stage_data["stage_number"],
                        state=QuestProgressState(stage_data["state"]),
                        start_timestamp=datetime.fromisoformat(stage_data["start_timestamp"]) if stage_data["start_timestamp"] else None,
                        completion_timestamp=datetime.fromisoformat(stage_data["completion_timestamp"]) if stage_data["completion_timestamp"] else None
                    )
                    
                    # Reconstruct challenges
                    for challenge_id, challenge_data in stage_data["challenges_progress"].items():
                        challenge_progress = ChallengeProgress(
                            challenge_id=challenge_data["challenge_id"],
                            attempts_remaining=challenge_data["attempts_remaining"],
                            current_progress=challenge_data["current_progress"],
                            energy_spent=challenge_data["energy_spent"],
                            state=QuestProgressState(challenge_data["state"]),
                            completion_timestamp=datetime.fromisoformat(challenge_data["completion_timestamp"]) if challenge_data["completion_timestamp"] else None,
                            failure_timestamp=datetime.fromisoformat(challenge_data["failure_timestamp"]) if challenge_data["failure_timestamp"] else None
                        )
                        stage_progress.challenges_progress[challenge_id] = challenge_progress
                        
                    quest_progress.stages_progress[int(stage_num)] = stage_progress
                    
                self.active_quests[quest_id] = quest_progress
                
            logger.info(f"Loaded quest progress from {path}")
            
        except Exception as e:
            logger.error(f"Failed to load progress: {e}")
            raise 