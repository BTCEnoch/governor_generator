"""
Tests for Story Tree Implementation
"""

import pytest
import json
from pathlib import Path
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
    QuestDifficulty
)

# Test fixtures
@pytest.fixture
def story_dir(tmp_path):
    """Create temporary directory for story files"""
    return tmp_path

@pytest.fixture
def story_tree(story_dir):
    """Create story tree instance"""
    return StoryTree(story_dir)

@pytest.fixture
def mock_quest_template():
    """Create mock quest template"""
    return QuestTemplate(
        template_id="test_template_001",
        title="Test Quest",
        description="A test quest",
        quest_type="wisdom_trial",
        difficulty=QuestDifficulty.ADEPT,
        stages=[],
        total_energy_required=100,
        total_wisdom_reward=50,
        reputation_requirement=10,
        governor_id="TEST_GOV_001",
        elemental_affinity="water",
        voidmaker_tier=1
    )

def test_create_story_tree(story_tree):
    """Test story tree creation"""
    root_id = story_tree.create_story_tree(
        "Test Story",
        "A test story tree"
    )
    
    assert root_id is not None
    assert root_id in story_tree.nodes
    assert story_tree.root_node == root_id
    assert story_tree.nodes[root_id].node_type == StoryNodeType.ROOT
    assert story_tree.nodes[root_id].state == StoryNodeState.AVAILABLE

def test_add_quest_node(story_tree, mock_quest_template):
    """Test adding quest node"""
    # Create root
    root_id = story_tree.create_story_tree("Test Story", "Description")
    
    # Add quest node
    quest_id = story_tree.add_quest_node(
        root_id,
        mock_quest_template
    )
    
    assert quest_id in story_tree.nodes
    assert quest_id in story_tree.nodes[root_id].children
    assert story_tree.nodes[quest_id].node_type == StoryNodeType.QUEST
    assert story_tree.nodes[quest_id].quest_template == mock_quest_template

def test_add_choice_node(story_tree):
    """Test adding choice node"""
    # Create root
    root_id = story_tree.create_story_tree("Test Story", "Description")
    
    # Add choice node
    choices = {"A": "Option A", "B": "Option B"}
    choice_id = story_tree.add_choice_node(
        root_id,
        "Test Choice",
        "Make a choice",
        choices
    )
    
    assert choice_id in story_tree.nodes
    assert choice_id in story_tree.nodes[root_id].children
    assert story_tree.nodes[choice_id].node_type == StoryNodeType.CHOICE
    assert story_tree.nodes[choice_id].choices == choices

def test_add_condition_node(story_tree):
    """Test adding condition node"""
    # Create root
    root_id = story_tree.create_story_tree("Test Story", "Description")
    
    # Add condition node
    conditions = {"has_item": True, "has_wisdom": False}
    condition_id = story_tree.add_condition_node(
        root_id,
        "Test Condition",
        "Check conditions",
        conditions
    )
    
    assert condition_id in story_tree.nodes
    assert condition_id in story_tree.nodes[root_id].children
    assert story_tree.nodes[condition_id].node_type == StoryNodeType.CONDITION
    assert story_tree.nodes[condition_id].conditions == conditions

def test_add_reward_node(story_tree):
    """Test adding reward node"""
    # Create root
    root_id = story_tree.create_story_tree("Test Story", "Description")
    
    # Add reward node
    rewards = {"wisdom": 100, "reputation": 50}
    reward_id = story_tree.add_reward_node(
        root_id,
        "Test Reward",
        "Claim rewards",
        rewards
    )
    
    assert reward_id in story_tree.nodes
    assert reward_id in story_tree.nodes[root_id].children
    assert story_tree.nodes[reward_id].node_type == StoryNodeType.REWARD
    assert story_tree.nodes[reward_id].rewards == rewards

def test_add_ending_node(story_tree):
    """Test adding ending node"""
    # Create root
    root_id = story_tree.create_story_tree("Test Story", "Description")
    
    # Add ending node
    ending_id = story_tree.add_ending_node(
        root_id,
        "Test Ending",
        "The end"
    )
    
    assert ending_id in story_tree.nodes
    assert ending_id in story_tree.nodes[root_id].children
    assert story_tree.nodes[ending_id].node_type == StoryNodeType.ENDING

def test_update_node_state(story_tree, mock_quest_template):
    """Test updating node state"""
    # Create root and quest
    root_id = story_tree.create_story_tree("Test Story", "Description")
    quest_id = story_tree.add_quest_node(root_id, mock_quest_template)
    
    # Update state
    story_tree.update_node_state(quest_id, StoryNodeState.IN_PROGRESS)
    assert story_tree.nodes[quest_id].state == StoryNodeState.IN_PROGRESS

def test_state_cascade(story_tree, mock_quest_template):
    """Test state cascading to children"""
    # Create nodes
    root_id = story_tree.create_story_tree("Test Story", "Description")
    quest1_id = story_tree.add_quest_node(root_id, mock_quest_template)
    quest2_id = story_tree.add_quest_node(quest1_id, mock_quest_template)
    
    # Update parent state
    story_tree.update_node_state(quest1_id, StoryNodeState.COMPLETED, True)
    
    # Check child state
    assert story_tree.nodes[quest2_id].state == StoryNodeState.AVAILABLE

def test_get_available_nodes(story_tree, mock_quest_template):
    """Test getting available nodes"""
    # Create nodes
    root_id = story_tree.create_story_tree("Test Story", "Description")
    quest1_id = story_tree.add_quest_node(root_id, mock_quest_template)
    quest2_id = story_tree.add_quest_node(root_id, mock_quest_template)
    
    # Set states
    story_tree.update_node_state(quest1_id, StoryNodeState.AVAILABLE)
    story_tree.update_node_state(quest2_id, StoryNodeState.LOCKED)
    
    # Get available nodes
    available = story_tree.get_available_nodes()
    assert len(available) == 2  # root + quest1
    assert any(node.node_id == root_id for node in available)
    assert any(node.node_id == quest1_id for node in available)

def test_get_active_quests(story_tree, mock_quest_template):
    """Test getting active quests"""
    # Create nodes
    root_id = story_tree.create_story_tree("Test Story", "Description")
    quest1_id = story_tree.add_quest_node(root_id, mock_quest_template)
    quest2_id = story_tree.add_quest_node(root_id, mock_quest_template)
    
    # Set states
    story_tree.update_node_state(quest1_id, StoryNodeState.IN_PROGRESS)
    story_tree.update_node_state(quest2_id, StoryNodeState.AVAILABLE)
    
    # Get active quests
    active = story_tree.get_active_quests()
    assert len(active) == 1
    assert active[0].node_id == quest1_id

def test_get_completed_nodes(story_tree, mock_quest_template):
    """Test getting completed nodes"""
    # Create nodes
    root_id = story_tree.create_story_tree("Test Story", "Description")
    quest1_id = story_tree.add_quest_node(root_id, mock_quest_template)
    quest2_id = story_tree.add_quest_node(root_id, mock_quest_template)
    
    # Set states
    story_tree.update_node_state(quest1_id, StoryNodeState.COMPLETED)
    story_tree.update_node_state(quest2_id, StoryNodeState.IN_PROGRESS)
    
    # Get completed nodes
    completed = story_tree.get_completed_nodes()
    assert len(completed) == 1
    assert completed[0].node_id == quest1_id

def test_get_node_path(story_tree, mock_quest_template):
    """Test getting path to node"""
    # Create nodes
    root_id = story_tree.create_story_tree("Test Story", "Description")
    quest1_id = story_tree.add_quest_node(root_id, mock_quest_template)
    quest2_id = story_tree.add_quest_node(quest1_id, mock_quest_template)
    
    # Get path
    path = story_tree.get_node_path(quest2_id)
    assert path == [root_id, quest1_id, quest2_id]

def test_check_requirements(story_tree, mock_quest_template):
    """Test checking node requirements"""
    # Create nodes
    root_id = story_tree.create_story_tree("Test Story", "Description")
    quest1_id = story_tree.add_quest_node(root_id, mock_quest_template)
    
    # Create requirements
    reqs = StoryRequirement(
        required_quests=[quest1_id]
    )
    
    quest2_id = story_tree.add_quest_node(
        root_id,
        mock_quest_template,
        requirements=reqs
    )
    
    # Check requirements (should fail)
    assert not story_tree._check_requirements(quest2_id)
    
    # Complete required quest
    story_tree.update_node_state(quest1_id, StoryNodeState.COMPLETED)
    
    # Check requirements (should pass)
    assert story_tree._check_requirements(quest2_id)

def test_save_and_load(story_tree, mock_quest_template, story_dir):
    """Test saving and loading story tree"""
    # Create story tree
    root_id = story_tree.create_story_tree("Test Story", "Description")
    quest_id = story_tree.add_quest_node(root_id, mock_quest_template)
    
    # Save to file
    story_tree.save_to_file("test_story.json")
    
    # Create new story tree and load
    new_tree = StoryTree(story_dir)
    new_tree.load_from_file("test_story.json")
    
    # Verify loaded data
    assert new_tree.root_node == root_id
    assert quest_id in new_tree.nodes
    assert new_tree.nodes[quest_id].quest_template.template_id == mock_quest_template.template_id

def test_invalid_parent_node(story_tree, mock_quest_template):
    """Test adding node with invalid parent"""
    with pytest.raises(ValueError):
        story_tree.add_quest_node("invalid_id", mock_quest_template)

def test_invalid_node_for_state_update(story_tree):
    """Test updating state of invalid node"""
    with pytest.raises(ValueError):
        story_tree.update_node_state("invalid_id", StoryNodeState.COMPLETED) 