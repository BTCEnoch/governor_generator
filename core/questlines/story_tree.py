"""
Story Tree Implementation
Manages quest storylines and progression paths
"""

import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime

from core.questlines.templates.quest_template_manager import QuestTemplate, QuestDifficulty

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoryNodeType(Enum):
    """Types of nodes in the story tree"""
    ROOT = "root"
    QUEST = "quest"
    CHOICE = "choice"
    CONDITION = "condition"
    REWARD = "reward"
    ENDING = "ending"

class StoryNodeState(Enum):
    """Possible states for story nodes"""
    LOCKED = "locked"
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class StoryRequirement:
    """Requirements for unlocking story nodes"""
    required_quests: List[str] = field(default_factory=list)
    required_reputation: int = 0
    required_wisdom: int = 0
    required_items: List[str] = field(default_factory=list)
    required_governors: List[str] = field(default_factory=list)
    required_choices: Dict[str, str] = field(default_factory=dict)

@dataclass
class StoryNode:
    """Node in the story tree"""
    node_id: str
    node_type: StoryNodeType
    title: str
    description: str
    state: StoryNodeState = StoryNodeState.LOCKED
    requirements: StoryRequirement = field(default_factory=StoryRequirement)
    children: List[str] = field(default_factory=list)
    parent: Optional[str] = None
    quest_template: Optional[QuestTemplate] = None
    choices: Dict[str, str] = field(default_factory=dict)
    conditions: Dict[str, bool] = field(default_factory=dict)
    rewards: Dict[str, int] = field(default_factory=dict)

class StoryTree:
    """
    Manages a tree of story nodes representing quest progression
    and narrative branches
    """
    
    def __init__(self, story_dir: Path):
        """Initialize story tree"""
        self.story_dir = Path(story_dir)
        self.nodes: Dict[str, StoryNode] = {}
        self.root_node: Optional[str] = None
        logger.info("Initialized Story Tree")
        
    def create_story_tree(
        self,
        root_title: str,
        root_description: str
    ) -> str:
        """Create a new story tree with root node"""
        try:
            # Generate root node ID
            root_id = f"root_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Create root node
            root_node = StoryNode(
                node_id=root_id,
                node_type=StoryNodeType.ROOT,
                title=root_title,
                description=root_description,
                state=StoryNodeState.AVAILABLE
            )
            
            # Add to nodes dictionary
            self.nodes[root_id] = root_node
            self.root_node = root_id
            
            logger.info(f"Created story tree with root node {root_id}")
            return root_id
            
        except Exception as e:
            logger.error(f"Failed to create story tree: {e}")
            raise
            
    def add_quest_node(
        self,
        parent_id: str,
        quest_template: QuestTemplate,
        requirements: Optional[StoryRequirement] = None
    ) -> str:
        """Add a quest node to the story tree"""
        try:
            # Validate parent exists
            if parent_id not in self.nodes:
                raise ValueError(f"Parent node {parent_id} not found")
                
            # Generate node ID
            node_id = f"quest_{quest_template.template_id}"
            
            # Create node
            node = StoryNode(
                node_id=node_id,
                node_type=StoryNodeType.QUEST,
                title=quest_template.title,
                description=quest_template.description,
                state=StoryNodeState.LOCKED,
                requirements=requirements or StoryRequirement(),
                parent=parent_id,
                quest_template=quest_template
            )
            
            # Add to nodes dictionary and parent's children
            self.nodes[node_id] = node
            self.nodes[parent_id].children.append(node_id)
            
            logger.info(f"Added quest node {node_id} to parent {parent_id}")
            return node_id
            
        except Exception as e:
            logger.error(f"Failed to add quest node: {e}")
            raise
            
    def add_choice_node(
        self,
        parent_id: str,
        title: str,
        description: str,
        choices: Dict[str, str],
        requirements: Optional[StoryRequirement] = None
    ) -> str:
        """Add a choice node to the story tree"""
        try:
            # Validate parent exists
            if parent_id not in self.nodes:
                raise ValueError(f"Parent node {parent_id} not found")
                
            # Generate node ID
            node_id = f"choice_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Create node
            node = StoryNode(
                node_id=node_id,
                node_type=StoryNodeType.CHOICE,
                title=title,
                description=description,
                state=StoryNodeState.LOCKED,
                requirements=requirements or StoryRequirement(),
                parent=parent_id,
                choices=choices
            )
            
            # Add to nodes dictionary and parent's children
            self.nodes[node_id] = node
            self.nodes[parent_id].children.append(node_id)
            
            logger.info(f"Added choice node {node_id} to parent {parent_id}")
            return node_id
            
        except Exception as e:
            logger.error(f"Failed to add choice node: {e}")
            raise
            
    def add_condition_node(
        self,
        parent_id: str,
        title: str,
        description: str,
        conditions: Dict[str, bool],
        requirements: Optional[StoryRequirement] = None
    ) -> str:
        """Add a condition node to the story tree"""
        try:
            # Validate parent exists
            if parent_id not in self.nodes:
                raise ValueError(f"Parent node {parent_id} not found")
                
            # Generate node ID
            node_id = f"condition_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Create node
            node = StoryNode(
                node_id=node_id,
                node_type=StoryNodeType.CONDITION,
                title=title,
                description=description,
                state=StoryNodeState.LOCKED,
                requirements=requirements or StoryRequirement(),
                parent=parent_id,
                conditions=conditions
            )
            
            # Add to nodes dictionary and parent's children
            self.nodes[node_id] = node
            self.nodes[parent_id].children.append(node_id)
            
            logger.info(f"Added condition node {node_id} to parent {parent_id}")
            return node_id
            
        except Exception as e:
            logger.error(f"Failed to add condition node: {e}")
            raise
            
    def add_reward_node(
        self,
        parent_id: str,
        title: str,
        description: str,
        rewards: Dict[str, int],
        requirements: Optional[StoryRequirement] = None
    ) -> str:
        """Add a reward node to the story tree"""
        try:
            # Validate parent exists
            if parent_id not in self.nodes:
                raise ValueError(f"Parent node {parent_id} not found")
                
            # Generate node ID
            node_id = f"reward_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Create node
            node = StoryNode(
                node_id=node_id,
                node_type=StoryNodeType.REWARD,
                title=title,
                description=description,
                state=StoryNodeState.LOCKED,
                requirements=requirements or StoryRequirement(),
                parent=parent_id,
                rewards=rewards
            )
            
            # Add to nodes dictionary and parent's children
            self.nodes[node_id] = node
            self.nodes[parent_id].children.append(node_id)
            
            logger.info(f"Added reward node {node_id} to parent {parent_id}")
            return node_id
            
        except Exception as e:
            logger.error(f"Failed to add reward node: {e}")
            raise
            
    def add_ending_node(
        self,
        parent_id: str,
        title: str,
        description: str,
        requirements: Optional[StoryRequirement] = None
    ) -> str:
        """Add an ending node to the story tree"""
        try:
            # Validate parent exists
            if parent_id not in self.nodes:
                raise ValueError(f"Parent node {parent_id} not found")
                
            # Generate node ID
            node_id = f"ending_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Create node
            node = StoryNode(
                node_id=node_id,
                node_type=StoryNodeType.ENDING,
                title=title,
                description=description,
                state=StoryNodeState.LOCKED,
                requirements=requirements or StoryRequirement(),
                parent=parent_id
            )
            
            # Add to nodes dictionary and parent's children
            self.nodes[node_id] = node
            self.nodes[parent_id].children.append(node_id)
            
            logger.info(f"Added ending node {node_id} to parent {parent_id}")
            return node_id
            
        except Exception as e:
            logger.error(f"Failed to add ending node: {e}")
            raise
            
    def update_node_state(
        self,
        node_id: str,
        new_state: StoryNodeState,
        cascade: bool = True
    ) -> None:
        """Update node state and optionally cascade to children"""
        try:
            # Validate node exists
            if node_id not in self.nodes:
                raise ValueError(f"Node {node_id} not found")
                
            # Update state
            self.nodes[node_id].state = new_state
            logger.info(f"Updated node {node_id} state to {new_state}")
            
            # Cascade if requested
            if cascade:
                for child_id in self.nodes[node_id].children:
                    if new_state == StoryNodeState.COMPLETED:
                        # Check if child requirements are met
                        if self._check_requirements(child_id):
                            self.update_node_state(child_id, StoryNodeState.AVAILABLE, False)
                    else:
                        self.update_node_state(child_id, new_state, True)
                        
        except Exception as e:
            logger.error(f"Failed to update node state: {e}")
            raise
            
    def get_available_nodes(self) -> List[StoryNode]:
        """Get all nodes in AVAILABLE state"""
        try:
            return [
                node for node in self.nodes.values()
                if node.state == StoryNodeState.AVAILABLE
            ]
        except Exception as e:
            logger.error(f"Failed to get available nodes: {e}")
            raise
            
    def get_active_quests(self) -> List[StoryNode]:
        """Get all quest nodes in IN_PROGRESS state"""
        try:
            return [
                node for node in self.nodes.values()
                if node.node_type == StoryNodeType.QUEST
                and node.state == StoryNodeState.IN_PROGRESS
            ]
        except Exception as e:
            logger.error(f"Failed to get active quests: {e}")
            raise
            
    def get_completed_nodes(self) -> List[StoryNode]:
        """Get all nodes in COMPLETED state"""
        try:
            return [
                node for node in self.nodes.values()
                if node.state == StoryNodeState.COMPLETED
            ]
        except Exception as e:
            logger.error(f"Failed to get completed nodes: {e}")
            raise
            
    def get_node_path(self, node_id: str) -> List[str]:
        """Get path from root to specified node"""
        try:
            path = []
            current = node_id
            
            while current is not None:
                path.append(current)
                current = self.nodes[current].parent
                
            return list(reversed(path))
            
        except Exception as e:
            logger.error(f"Failed to get node path: {e}")
            raise
            
    def _check_requirements(self, node_id: str) -> bool:
        """Check if node requirements are met"""
        try:
            node = self.nodes[node_id]
            reqs = node.requirements
            
            # Check quest requirements
            for quest_id in reqs.required_quests:
                if quest_id not in self.nodes:
                    return False
                if self.nodes[quest_id].state != StoryNodeState.COMPLETED:
                    return False
                    
            # Check choice requirements
            for choice_id, choice_value in reqs.required_choices.items():
                if choice_id not in self.nodes:
                    return False
                if self.nodes[choice_id].choices.get("selected") != choice_value:
                    return False
                    
            # Other requirements would be checked against player state
            # which is not implemented in this base class
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to check requirements: {e}")
            return False
            
    def save_to_file(self, filename: str) -> None:
        """Save story tree to file"""
        try:
            path = self.story_dir / filename
            
            # Convert to serializable format
            data = {
                "root_node": self.root_node,
                "nodes": {
                    node_id: {
                        "node_id": node.node_id,
                        "node_type": node.node_type.value,
                        "title": node.title,
                        "description": node.description,
                        "state": node.state.value,
                        "requirements": vars(node.requirements),
                        "children": node.children,
                        "parent": node.parent,
                        "quest_template": vars(node.quest_template) if node.quest_template else None,
                        "choices": node.choices,
                        "conditions": node.conditions,
                        "rewards": node.rewards
                    }
                    for node_id, node in self.nodes.items()
                }
            }
            
            # Save to file
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Saved story tree to {path}")
            
        except Exception as e:
            logger.error(f"Failed to save story tree: {e}")
            raise
            
    def load_from_file(self, filename: str) -> None:
        """Load story tree from file"""
        try:
            path = self.story_dir / filename
            
            # Load from file
            with open(path, 'r') as f:
                data = json.load(f)
                
            # Clear existing data
            self.nodes.clear()
            self.root_node = None
            
            # Set root node
            self.root_node = data["root_node"]
            
            # Reconstruct nodes
            for node_id, node_data in data["nodes"].items():
                # Create requirements
                requirements = StoryRequirement(**node_data["requirements"])
                
                # Create quest template if present
                quest_template = None
                if node_data["quest_template"]:
                    quest_template = QuestTemplate(**node_data["quest_template"])
                    
                # Create node
                node = StoryNode(
                    node_id=node_data["node_id"],
                    node_type=StoryNodeType(node_data["node_type"]),
                    title=node_data["title"],
                    description=node_data["description"],
                    state=StoryNodeState(node_data["state"]),
                    requirements=requirements,
                    children=node_data["children"],
                    parent=node_data["parent"],
                    quest_template=quest_template,
                    choices=node_data["choices"],
                    conditions=node_data["conditions"],
                    rewards=node_data["rewards"]
                )
                
                self.nodes[node_id] = node
                
            logger.info(f"Loaded story tree from {path}")
            
        except Exception as e:
            logger.error(f"Failed to load story tree: {e}")
            raise 