"""
Core Data Structures for Context-Aware Dialog System
===================================================

This module defines the fundamental data structures used throughout the dialog system:
- DialogNode: Represents a single state in the dialog state machine
- GovernorProfile: Encodes governor-specific preferences and behaviors
- PlayerState: Tracks player progression, reputation, and context
- DialogResponse: Represents the output of a dialog interaction
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Any, Optional, Union
from enum import Enum
import json
import hashlib
from datetime import datetime


class InteractionType(Enum):
    """Types of dialog interactions available with governors."""
    RIDDLE_KEEPER = "riddle_keeper"
    CEREMONIAL_GOVERNOR = "ceremonial_governor"
    ARCHETYPAL_MIRROR = "archetypal_mirror"
    SECRET_KEEPER = "secret_keeper"
    TRIBUTE_TAKER = "tribute_taker"
    KNOWLEDGE_SEEKER = "knowledge_seeker"
    RITUAL_GUIDE = "ritual_guide"


class IntentCategory(Enum):
    """Categories for classifying player input intent."""
    RIDDLE_ANSWER = "riddle_answer"
    FORMAL_GREETING = "formal_greeting"
    CASUAL_GREETING = "casual_greeting"
    QUESTION = "question"
    OFFERING = "offering"
    INSULT = "insult"
    PRAISE = "praise"
    SECRET_KNOWLEDGE = "secret_knowledge"
    RITUAL_PHRASE = "ritual_phrase"
    OFF_TOPIC = "off_topic"
    UNKNOWN = "unknown"


class ResponseType(Enum):
    """Types of responses the dialog system can generate."""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"
    HINT = "hint"
    REBUKE = "rebuke"
    NEUTRAL = "neutral"
    LORE_REVEAL = "lore_reveal"
    RITUAL_COMPLETE = "ritual_complete"


@dataclass
class DialogNode:
    """
    Represents a single state in the dialog state machine.
    
    Each node contains content variants, transition rules, and requirements
    for accessing the node. This forms the backbone of the dialog flow.
    """
    id: str
    content: List[str]  # Multiple response variants for variety
    transitions: Dict[str, str]  # intent_category -> next_node_id
    requirements: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate node structure after initialization."""
        if not self.id:
            raise ValueError("DialogNode must have a non-empty id")
        if not self.content:
            raise ValueError("DialogNode must have at least one content variant")
        
        # Ensure all transition targets are valid intent categories
        for intent_str in self.transitions.keys():
            try:
                IntentCategory(intent_str)
            except ValueError:
                raise ValueError(f"Invalid intent category in transitions: {intent_str}")
    
    def get_content_variant(self, entropy_source: Optional[str] = None) -> str:
        """
        Select a content variant using deterministic entropy.
        
        Args:
            entropy_source: String to use for deterministic selection (e.g., block hash)
            
        Returns:
            Selected content variant
        """
        if not entropy_source:
            return self.content[0]  # Default to first variant
        
        # Use hash of entropy source to select variant deterministically
        hash_value = int(hashlib.sha256(entropy_source.encode()).hexdigest(), 16)
        index = hash_value % len(self.content)
        return self.content[index]
    
    def can_transition_to(self, intent: IntentCategory) -> bool:
        """Check if this node can transition for the given intent."""
        return intent.value in self.transitions
    
    def get_next_node_id(self, intent: IntentCategory) -> Optional[str]:
        """Get the next node ID for the given intent."""
        return self.transitions.get(intent.value)


@dataclass
class GovernorProfile:
    """
    Encodes governor-specific preferences, traits, and interaction models.
    
    This compact representation allows the dialog system to quickly adapt
    its behavior to match each governor's unique personality and preferences.
    """
    governor_id: str
    name: str
    preferences: Dict[str, str] = field(default_factory=dict)
    traits: List[str] = field(default_factory=list)
    interaction_models: List[InteractionType] = field(default_factory=list)
    reputation_thresholds: Dict[int, str] = field(default_factory=dict)
    dialog_style: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate profile structure after initialization."""
        if not self.governor_id:
            raise ValueError("GovernorProfile must have a non-empty governor_id")
        if not self.name:
            raise ValueError("GovernorProfile must have a non-empty name")
    
    def has_trait(self, trait: str) -> bool:
        """Check if governor has a specific trait."""
        return trait.lower() in [t.lower() for t in self.traits]
    
    def get_preference(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a preference value with optional default."""
        return self.preferences.get(key, default)
    
    def supports_interaction_type(self, interaction_type: InteractionType) -> bool:
        """Check if governor supports a specific interaction type."""
        return interaction_type in self.interaction_models
    
    def get_reputation_threshold_content(self, reputation: int) -> str:
        """Get the content type available at the given reputation level."""
        available_thresholds = [thresh for thresh in self.reputation_thresholds.keys() 
                              if thresh <= reputation]
        if not available_thresholds:
            return "basic_interactions"
        
        max_threshold = max(available_thresholds)
        return self.reputation_thresholds[max_threshold]
    
    @classmethod
    def from_governor_data(cls, governor_data: Dict[str, Any]) -> 'GovernorProfile':
        """
        Create a GovernorProfile from existing governor JSON data.
        
        Args:
            governor_data: Dictionary containing governor information
            
        Returns:
            GovernorProfile instance
        """
        governor_name = governor_data.get("name", "")
        if not governor_name:
            raise ValueError("Governor data must contain a 'name' field")
            
        return cls(
            governor_id=governor_name,
            name=governor_name,
            preferences={
                "tone": governor_data.get("tone", "neutral"),
                "greeting_preference": "formal" if "formal" in str(governor_data.get("personality_traits", [])).lower() else "casual",
                "puzzle_style": "metaphor" if "mystical" in str(governor_data.get("specializations", [])).lower() else "direct"
            },
            traits=governor_data.get("personality_traits", []),
            interaction_models=[InteractionType.RIDDLE_KEEPER, InteractionType.CEREMONIAL_GOVERNOR],  # Default models
            reputation_thresholds={
                0: "basic_interactions",
                5: "intermediate_content",
                10: "advanced_content",
                15: "secret_knowledge",
                20: "master_level"
            },
            dialog_style={
                "formality_level": 0.8 if "formal" in str(governor_data.get("personality_traits", [])).lower() else 0.4,
                "mystical_language": 0.9 if "mystical" in str(governor_data.get("specializations", [])).lower() else 0.3
            }
        )


@dataclass
class PlayerState:
    """
    Tracks player progression, reputation, and context across all governors.
    
    This represents the complete state of a player's journey through the
    Enochian Governor system, including reputation with each governor,
    current dialog positions, inventory, and story flags.
    """
    player_id: str
    current_nodes: Dict[str, str] = field(default_factory=dict)  # governor_id -> current_node_id
    reputation: Dict[str, int] = field(default_factory=dict)  # governor_id -> reputation_score
    inventory: List[str] = field(default_factory=list)  # List of owned items/tokens
    story_flags: Set[str] = field(default_factory=set)  # Completed quests, discovered secrets
    interaction_history: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)  # governor_id -> interactions
    last_interaction: Dict[str, datetime] = field(default_factory=dict)  # governor_id -> timestamp
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate player state after initialization."""
        if not self.player_id:
            raise ValueError("PlayerState must have a non-empty player_id")
    
    def get_reputation(self, governor_id: str) -> int:
        """Get reputation with a specific governor."""
        return self.reputation.get(governor_id, 0)
    
    def add_reputation(self, governor_id: str, amount: int) -> None:
        """Add reputation with a specific governor."""
        current_rep = self.reputation.get(governor_id, 0)
        self.reputation[governor_id] = max(0, current_rep + amount)  # Prevent negative reputation
    
    def get_current_node(self, governor_id: str) -> Optional[str]:
        """Get current dialog node for a governor."""
        return self.current_nodes.get(governor_id)
    
    def set_current_node(self, governor_id: str, node_id: str) -> None:
        """Set current dialog node for a governor."""
        self.current_nodes[governor_id] = node_id
    
    def has_item(self, item: str) -> bool:
        """Check if player has a specific item."""
        return item in self.inventory
    
    def add_item(self, item: str) -> None:
        """Add an item to player's inventory."""
        if item not in self.inventory:
            self.inventory.append(item)
    
    def remove_item(self, item: str) -> bool:
        """Remove an item from player's inventory. Returns True if item was found and removed."""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def has_flag(self, flag: str) -> bool:
        """Check if player has a specific story flag."""
        return flag in self.story_flags
    
    def add_flag(self, flag: str) -> None:
        """Add a story flag."""
        self.story_flags.add(flag)
    
    def can_interact_with_governor(self, governor_id: str, block_limit: int = 144) -> bool:
        """
        Check if player can interact with a governor (respecting daily limits).
        
        Args:
            governor_id: The governor to check
            block_limit: Number of blocks to wait between interactions (default 144 ≈ 1 day)
            
        Returns:
            True if interaction is allowed
        """
        last_interaction = self.last_interaction.get(governor_id)
        if not last_interaction:
            return True
        
        # Use block-based time calculations for Bitcoin consensus
        return self._check_block_time_constraint(last_interaction, block_limit)
    
    def _check_block_time_constraint(self, last_interaction: datetime, block_limit: int) -> bool:
        """
        Check if enough blocks have passed since last interaction.
        
        Uses Bitcoin block time calculations with proper variance handling.
        
        Args:
            last_interaction: Timestamp of last interaction
            block_limit: Minimum blocks required between interactions
            
        Returns:
            True if enough blocks have passed
        """
        current_time = datetime.now()
        time_diff = current_time - last_interaction
        
        # Bitcoin target block time: 10 minutes (600 seconds)
        # But actual block times vary, so we use statistical modeling
        bitcoin_target_block_time = 600  # 10 minutes in seconds
        
        # Account for block time variance (Bitcoin blocks can vary ±20%)
        # Use conservative estimate: multiply by 0.8 for safety margin
        effective_block_time = bitcoin_target_block_time * 0.8
        
        # Calculate estimated blocks passed
        estimated_blocks_passed = time_diff.total_seconds() / effective_block_time
        
        # Add deterministic entropy based on interaction timestamp
        # This prevents gaming by slightly varying timing
        entropy_factor = self._calculate_time_entropy(last_interaction)
        adjusted_blocks = estimated_blocks_passed * entropy_factor
        
        return adjusted_blocks >= block_limit
    
    def _calculate_time_entropy(self, timestamp: datetime) -> float:
        """
        Calculate time-based entropy factor for block time variance.
        
        Args:
            timestamp: Reference timestamp
            
        Returns:
            Entropy factor between 0.85 and 1.15
        """
        # Use timestamp hash for deterministic randomness
        timestamp_str = timestamp.isoformat()
        hash_value = int(hashlib.sha256(timestamp_str.encode()).hexdigest()[:8], 16)
        
        # Convert to factor between 0.85 and 1.15 (±15% variance)
        normalized = (hash_value % 10000) / 10000.0  # 0.0 to 1.0
        entropy_factor = 0.85 + (normalized * 0.30)  # 0.85 to 1.15
        
        return entropy_factor
    
    def get_blocks_since_interaction(self, governor_id: str) -> Optional[float]:
        """
        Get estimated number of blocks since last interaction with governor.
        
        Args:
            governor_id: Governor to check
            
        Returns:
            Estimated blocks passed, or None if no previous interaction
        """
        last_interaction = self.last_interaction.get(governor_id)
        if not last_interaction:
            return None
        
        current_time = datetime.now()
        time_diff = current_time - last_interaction
        
        # Use same calculation as constraint check
        bitcoin_target_block_time = 600  # 10 minutes
        effective_block_time = bitcoin_target_block_time * 0.8
        estimated_blocks = time_diff.total_seconds() / effective_block_time
        
        # Apply entropy factor
        entropy_factor = self._calculate_time_entropy(last_interaction)
        return estimated_blocks * entropy_factor
    
    def record_interaction(self, governor_id: str, interaction_data: Dict[str, Any]) -> None:
        """Record an interaction with a governor."""
        if governor_id not in self.interaction_history:
            self.interaction_history[governor_id] = []
        
        interaction_data["timestamp"] = datetime.now()
        self.interaction_history[governor_id].append(interaction_data)
        self.last_interaction[governor_id] = datetime.now()


@dataclass
class DialogResponse:
    """
    Represents the complete output of a dialog interaction.
    
    This includes the response text, any reputation changes, state updates,
    and metadata about the interaction outcome.
    """
    response_text: str
    response_type: ResponseType
    reputation_change: int = 0
    next_node_id: Optional[str] = None
    items_gained: List[str] = field(default_factory=list)
    items_consumed: List[str] = field(default_factory=list)
    flags_added: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate response after initialization."""
        if not self.response_text:
            raise ValueError("DialogResponse must have non-empty response_text")
    
    def apply_to_player_state(self, player_state: PlayerState, governor_id: str) -> None:
        """
        Apply this response's effects to a player state.
        
        Args:
            player_state: The player state to modify
            governor_id: The governor this response came from
        """
        # Update reputation
        if self.reputation_change != 0:
            player_state.add_reputation(governor_id, self.reputation_change)
        
        # Update current node
        if self.next_node_id:
            player_state.set_current_node(governor_id, self.next_node_id)
        
        # Handle items
        for item in self.items_gained:
            player_state.add_item(item)
        
        for item in self.items_consumed:
            player_state.remove_item(item)
        
        # Add story flags
        for flag in self.flags_added:
            player_state.add_flag(flag)
        
        # Record the interaction
        interaction_record = {
            "response_type": self.response_type.value,
            "reputation_change": self.reputation_change,
            "items_gained": self.items_gained,
            "items_consumed": self.items_consumed,
            "flags_added": list(self.flags_added),
            "metadata": self.metadata
        }
        player_state.record_interaction(governor_id, interaction_record)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary format for serialization."""
        return {
            "response_text": self.response_text,
            "response_type": self.response_type.value,
            "reputation_change": self.reputation_change,
            "next_node_id": self.next_node_id,
            "items_gained": self.items_gained,
            "items_consumed": self.items_consumed,
            "flags_added": list(self.flags_added),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DialogResponse':
        """Create DialogResponse from dictionary data."""
        return cls(
            response_text=data["response_text"],
            response_type=ResponseType(data["response_type"]),
            reputation_change=data.get("reputation_change", 0),
            next_node_id=data.get("next_node_id"),
            items_gained=data.get("items_gained", []),
            items_consumed=data.get("items_consumed", []),
            flags_added=set(data.get("flags_added", [])),
            metadata=data.get("metadata", {})
        ) 