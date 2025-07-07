"""
Tests for Quest Generator
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from core.questlines.quest_generator import (
    QuestGenerator,
    QuestGenerationStrategy,
    QuestGenerationConfig
)

from core.questlines.templates.quest_template_manager import (
    QuestTemplateManager,
    QuestTemplate,
    QuestDifficulty,
    ChallengeType
)

from core.questlines.story_tree import (
    StoryTree,
    StoryNodeType,
    StoryNodeState
)

from core.governors.profiler.core.enhanced_profile_analyzer import (
    EnhancedGovernorProfile,
    WisdomFoundation,
    ElementalEssence,
    TeachingDoctrine,
    VoidmakerAwareness
)

# Test fixtures
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

@pytest.fixture
def quest_generator(template_manager):
    """Create quest generator instance"""
    return QuestGenerator(template_manager, Path("/mock/path"))

def test_generate_single_quest(quest_generator, mock_governor_profile):
    """Test generating a single quest"""
    config = QuestGenerationConfig(
        strategy=QuestGenerationStrategy.SINGLE,
        min_stages=3,
        max_stages=5
    )
    
    story_tree = quest_generator.generate_quest_line(
        mock_governor_profile,
        config
    )
    
    # Verify story tree structure
    assert story_tree.root_node is not None
    root = story_tree.nodes[story_tree.root_node]
    assert len(root.children) == 1
    
    # Verify quest node
    quest_node = story_tree.nodes[root.children[0]]
    assert quest_node.node_type == StoryNodeType.QUEST
    assert quest_node.quest_template is not None
    assert quest_node.state == StoryNodeState.LOCKED
    
    # Verify reward node
    reward_nodes = [
        node for node in story_tree.nodes.values()
        if node.node_type == StoryNodeType.REWARD
    ]
    assert len(reward_nodes) == 1
    assert "wisdom" in reward_nodes[0].rewards
    assert "reputation" in reward_nodes[0].rewards

def test_generate_branching_quest(quest_generator, mock_governor_profile):
    """Test generating a branching quest"""
    config = QuestGenerationConfig(
        strategy=QuestGenerationStrategy.BRANCHING,
        allow_branches=True
    )
    
    story_tree = quest_generator.generate_quest_line(
        mock_governor_profile,
        config
    )
    
    # Verify initial quest
    root = story_tree.nodes[story_tree.root_node]
    assert len(root.children) == 1
    initial_quest = story_tree.nodes[root.children[0]]
    assert initial_quest.node_type == StoryNodeType.QUEST
    
    # Verify choice node
    choice_nodes = [
        node for node in story_tree.nodes.values()
        if node.node_type == StoryNodeType.CHOICE
    ]
    assert len(choice_nodes) == 1
    choice_node = choice_nodes[0]
    assert len(choice_node.choices) == 3  # wisdom, power, balance
    
    # Verify branch quests
    branch_quests = [
        node for node in story_tree.nodes.values()
        if node.node_type == StoryNodeType.QUEST and node.parent == choice_node.node_id
    ]
    assert len(branch_quests) == 3
    
    # Verify rewards
    reward_nodes = [
        node for node in story_tree.nodes.values()
        if node.node_type == StoryNodeType.REWARD
    ]
    assert len(reward_nodes) == 3  # One for each branch

def test_generate_conditional_quest(quest_generator, mock_governor_profile):
    """Test generating a conditional quest"""
    config = QuestGenerationConfig(
        strategy=QuestGenerationStrategy.CONDITIONAL,
        allow_conditions=True
    )
    
    story_tree = quest_generator.generate_quest_line(
        mock_governor_profile,
        config
    )
    
    # Verify initial quest
    root = story_tree.nodes[story_tree.root_node]
    assert len(root.children) == 1
    initial_quest = story_tree.nodes[root.children[0]]
    assert initial_quest.node_type == StoryNodeType.QUEST
    
    # Verify condition node
    condition_nodes = [
        node for node in story_tree.nodes.values()
        if node.node_type == StoryNodeType.CONDITION
    ]
    assert len(condition_nodes) == 1
    condition_node = condition_nodes[0]
    assert len(condition_node.conditions) == 3  # wisdom, power, artifact
    
    # Verify conditional quests
    conditional_quests = [
        node for node in story_tree.nodes.values()
        if node.node_type == StoryNodeType.QUEST and node.parent == condition_node.node_id
    ]
    assert len(conditional_quests) == 3
    
    # Verify rewards
    reward_nodes = [
        node for node in story_tree.nodes.values()
        if node.node_type == StoryNodeType.REWARD
    ]
    assert len(reward_nodes) == 3  # One for each condition

def test_generate_progressive_quest(quest_generator, mock_governor_profile):
    """Test generating a progressive quest"""
    config = QuestGenerationConfig(
        strategy=QuestGenerationStrategy.PROGRESSIVE,
        min_stages=3,
        max_stages=3
    )
    
    story_tree = quest_generator.generate_quest_line(
        mock_governor_profile,
        config
    )
    
    # Verify quest chain
    quest_nodes = [
        node for node in story_tree.nodes.values()
        if node.node_type == StoryNodeType.QUEST
    ]
    assert len(quest_nodes) == 3  # Three stages
    
    # Verify progression requirements
    for i, quest in enumerate(quest_nodes[1:], 1):  # Skip first quest
        assert quest.requirements.required_quests
        assert quest.requirements.required_reputation > 0
    
    # Verify rewards
    reward_nodes = [
        node for node in story_tree.nodes.values()
        if node.node_type == StoryNodeType.REWARD
    ]
    assert len(reward_nodes) == 4  # Three stage rewards + final reward
    
    # Verify final reward
    final_reward = [
        node for node in reward_nodes
        if "mastery" in node.rewards
    ][0]
    assert final_reward.rewards["mastery"] is True

def test_generate_collaborative_quest(quest_generator, mock_governor_profile):
    """Test generating a collaborative quest"""
    config = QuestGenerationConfig(
        strategy=QuestGenerationStrategy.COLLABORATIVE,
        required_governors={"GOV_001", "GOV_002", "GOV_003"}
    )
    
    story_tree = quest_generator.generate_quest_line(
        mock_governor_profile,
        config
    )
    
    # Verify hub quest
    root = story_tree.nodes[story_tree.root_node]
    assert len(root.children) == 1
    hub_quest = story_tree.nodes[root.children[0]]
    assert hub_quest.node_type == StoryNodeType.QUEST
    
    # Verify spoke quests
    spoke_quests = [
        node for node in story_tree.nodes.values()
        if node.node_type == StoryNodeType.QUEST and node.parent == hub_quest.node_id
    ]
    assert len(spoke_quests) == 3  # One for each required governor
    
    # Verify governor requirements
    for quest in spoke_quests:
        assert quest.requirements.required_governors
        assert len(quest.requirements.required_governors) == 1
    
    # Verify rewards
    reward_nodes = [
        node for node in story_tree.nodes.values()
        if node.node_type == StoryNodeType.REWARD
    ]
    assert len(reward_nodes) == 4  # Three spoke rewards + final reward
    
    # Verify final reward
    final_reward = [
        node for node in reward_nodes
        if "grand_alliance" in node.rewards
    ][0]
    assert final_reward.rewards["grand_alliance"] is True

def test_invalid_strategy(quest_generator, mock_governor_profile):
    """Test handling invalid generation strategy"""
    config = QuestGenerationConfig(
        strategy="invalid_strategy"  # type: ignore
    )
    
    with pytest.raises(ValueError):
        quest_generator.generate_quest_line(mock_governor_profile, config)

def test_collaborative_without_governors(quest_generator, mock_governor_profile):
    """Test collaborative quest without required governors"""
    config = QuestGenerationConfig(
        strategy=QuestGenerationStrategy.COLLABORATIVE
    )
    
    with pytest.raises(ValueError):
        quest_generator.generate_quest_line(mock_governor_profile, config) 