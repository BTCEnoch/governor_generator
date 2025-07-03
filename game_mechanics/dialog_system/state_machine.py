"""
Dialog State Machine
===================

This module implements the core state machine for managing dialog flow
between players and governors. It handles node transitions, requirement
checking, and state persistence.

Key Components:
- StateMachine: Core state machine logic
- TransitionValidator: Validates state transitions
- StateManager: Manages state persistence and recovery
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Callable
import logging
from enum import Enum

from .core_structures import (
    DialogNode, GovernorProfile, PlayerState, DialogResponse,
    IntentCategory, ResponseType, InteractionType
)
from .storage_schemas import DialogLibrarySchema, StorageManager


class TransitionResult(Enum):
    """Results of attempting a state transition."""
    SUCCESS = "success"
    INVALID_INTENT = "invalid_intent"
    REQUIREMENTS_NOT_MET = "requirements_not_met"
    NODE_NOT_FOUND = "node_not_found"
    RATE_LIMITED = "rate_limited"


@dataclass
class TransitionAttempt:
    """Record of a state transition attempt."""
    from_node_id: str
    to_node_id: Optional[str]
    intent: IntentCategory
    result: TransitionResult
    requirements_checked: Dict[str, bool]
    metadata: Dict[str, Any]


class TransitionValidator:
    """
    Validates state transitions based on requirements and constraints.
    
    This component ensures that players can only access content they've
    earned through proper progression and reputation building.
    """
    
    def __init__(self):
        """Initialize the transition validator."""
        self.logger = logging.getLogger(__name__)
    
    def validate_transition(self, 
                          current_node: DialogNode,
                          target_node: DialogNode,
                          player_state: PlayerState,
                          governor_profile: GovernorProfile,
                          intent: IntentCategory) -> TransitionAttempt:
        """
        Validate a proposed state transition.
        
        Args:
            current_node: Current dialog node
            target_node: Target dialog node
            player_state: Current player state
            governor_profile: Governor being interacted with
            intent: Player's classified intent
            
        Returns:
            TransitionAttempt with validation results
        """
        requirements_checked = {}
        metadata = {}
        
        # Check if current node supports this intent
        if not current_node.can_transition_to(intent):
            return TransitionAttempt(
                from_node_id=current_node.id,
                to_node_id=target_node.id,
                intent=intent,
                result=TransitionResult.INVALID_INTENT,
                requirements_checked=requirements_checked,
                metadata={"error": f"Node {current_node.id} does not support intent {intent.value}"}
            )
        
        # Check target node requirements
        requirements = target_node.requirements
        
        # Check reputation requirements
        if "min_reputation" in requirements:
            min_rep = requirements["min_reputation"]
            current_rep = player_state.get_reputation(governor_profile.governor_id)
            requirements_checked["reputation"] = current_rep >= min_rep
            
            if not requirements_checked["reputation"]:
                return TransitionAttempt(
                    from_node_id=current_node.id,
                    to_node_id=target_node.id,
                    intent=intent,
                    result=TransitionResult.REQUIREMENTS_NOT_MET,
                    requirements_checked=requirements_checked,
                    metadata={"required_reputation": min_rep, "current_reputation": current_rep}
                )
        
        # Check item requirements
        if "required_items" in requirements:
            required_items = requirements["required_items"]
            for item in required_items:
                has_item = player_state.has_item(item)
                requirements_checked[f"item_{item}"] = has_item
                
                if not has_item:
                    return TransitionAttempt(
                        from_node_id=current_node.id,
                        to_node_id=target_node.id,
                        intent=intent,
                        result=TransitionResult.REQUIREMENTS_NOT_MET,
                        requirements_checked=requirements_checked,
                        metadata={"missing_item": item}
                    )
        
        # Check story flag requirements
        if "required_flags" in requirements:
            required_flags = requirements["required_flags"]
            for flag in required_flags:
                has_flag = player_state.has_flag(flag)
                requirements_checked[f"flag_{flag}"] = has_flag
                
                if not has_flag:
                    return TransitionAttempt(
                        from_node_id=current_node.id,
                        to_node_id=target_node.id,
                        intent=intent,
                        result=TransitionResult.REQUIREMENTS_NOT_MET,
                        requirements_checked=requirements_checked,
                        metadata={"missing_flag": flag}
                    )
        
        # Check interaction cooldown
        if not player_state.can_interact_with_governor(governor_profile.governor_id):
            return TransitionAttempt(
                from_node_id=current_node.id,
                to_node_id=target_node.id,
                intent=intent,
                result=TransitionResult.RATE_LIMITED,
                requirements_checked=requirements_checked,
                metadata={"error": "Interaction rate limited"}
            )
        
        # All checks passed
        return TransitionAttempt(
            from_node_id=current_node.id,
            to_node_id=target_node.id,
            intent=intent,
            result=TransitionResult.SUCCESS,
            requirements_checked=requirements_checked,
            metadata={}
        )
    
    def check_interaction_type_compatibility(self, 
                                           governor_profile: GovernorProfile,
                                           interaction_type: InteractionType) -> bool:
        """Check if governor supports the requested interaction type."""
        return governor_profile.supports_interaction_type(interaction_type)


class StateMachine:
    """
    Core state machine for managing dialog flow.
    
    This is the central component that orchestrates dialog progression,
    validates transitions, and maintains state consistency.
    """
    
    def __init__(self, storage_manager: StorageManager):
        """
        Initialize the state machine.
        
        Args:
            storage_manager: Manager for loading dialog content
        """
        self.storage_manager = storage_manager
        self.validator = TransitionValidator()
        self.logger = logging.getLogger(__name__)
        
        # Cache for loaded dialog libraries
        self.dialog_cache: Dict[str, DialogLibrarySchema] = {}
    
    def get_dialog_library(self, governor_id: str) -> Optional[DialogLibrarySchema]:
        """
        Get dialog library for a governor, using cache when possible.
        
        Args:
            governor_id: ID of the governor
            
        Returns:
            Dialog library if available
        """
        if governor_id not in self.dialog_cache:
            library = self.storage_manager.load_dialog_library(governor_id)
            if library:
                self.dialog_cache[governor_id] = library
            else:
                return None
        
        return self.dialog_cache[governor_id]
    
    def get_current_node(self, governor_id: str, player_state: PlayerState) -> Optional[DialogNode]:
        """
        Get the current dialog node for a player-governor interaction.
        
        Args:
            governor_id: ID of the governor
            player_state: Current player state
            
        Returns:
            Current dialog node if available
        """
        library = self.get_dialog_library(governor_id)
        if not library:
            return None
        
        current_node_id = player_state.get_current_node(governor_id)
        if not current_node_id:
            # Start with default entry node
            current_node_id = f"{governor_id}_intro"
        
        return library.get_dialog_node(current_node_id)
    
    def attempt_transition(self,
                          governor_id: str,
                          player_state: PlayerState,
                          governor_profile: GovernorProfile,
                          intent: IntentCategory) -> TransitionAttempt:
        """
        Attempt to transition to a new dialog state.
        
        Args:
            governor_id: ID of the governor
            player_state: Current player state
            governor_profile: Governor profile
            intent: Classified player intent
            
        Returns:
            TransitionAttempt with results
        """
        # Get current node
        current_node = self.get_current_node(governor_id, player_state)
        if not current_node:
            return TransitionAttempt(
                from_node_id="unknown",
                to_node_id=None,
                intent=intent,
                result=TransitionResult.NODE_NOT_FOUND,
                requirements_checked={},
                metadata={"error": f"No dialog library found for governor {governor_id}"}
            )
        
        # Get target node ID from current node's transitions
        target_node_id = current_node.get_next_node_id(intent)
        if not target_node_id:
            return TransitionAttempt(
                from_node_id=current_node.id,
                to_node_id=None,
                intent=intent,
                result=TransitionResult.INVALID_INTENT,
                requirements_checked={},
                metadata={"error": f"No transition defined for intent {intent.value} from node {current_node.id}"}
            )
        
        # Get target node - fix linter error with proper null check
        library = self.get_dialog_library(governor_id)
        if not library:
            return TransitionAttempt(
                from_node_id=current_node.id,
                to_node_id=target_node_id,
                intent=intent,
                result=TransitionResult.NODE_NOT_FOUND,
                requirements_checked={},
                metadata={"error": f"Dialog library not found for governor {governor_id}"}
            )
        
        target_node = library.get_dialog_node(target_node_id)
        if not target_node:
            return TransitionAttempt(
                from_node_id=current_node.id,
                to_node_id=target_node_id,
                intent=intent,
                result=TransitionResult.NODE_NOT_FOUND,
                requirements_checked={},
                metadata={"error": f"Target node {target_node_id} not found"}
            )
        
        # Validate the transition
        return self.validator.validate_transition(
            current_node, target_node, player_state, governor_profile, intent
        )
    
    def execute_transition(self,
                          transition_attempt: TransitionAttempt,
                          player_state: PlayerState,
                          governor_id: str) -> bool:
        """
        Execute a validated state transition.
        
        Args:
            transition_attempt: The validated transition to execute
            player_state: Player state to update
            governor_id: ID of the governor
            
        Returns:
            True if transition was executed successfully
        """
        if transition_attempt.result != TransitionResult.SUCCESS:
            self.logger.warning(f"Attempted to execute failed transition: {transition_attempt.result}")
            return False
        
        if not transition_attempt.to_node_id:
            self.logger.error("Cannot execute transition without target node ID")
            return False
        
        # Update player's current node
        player_state.set_current_node(governor_id, transition_attempt.to_node_id)
        
        self.logger.info(f"Executed transition from {transition_attempt.from_node_id} to {transition_attempt.to_node_id}")
        return True


class StateManager:
    """
    Manages state persistence and recovery for the dialog system.
    
    This component handles saving and loading player dialog states,
    ensuring consistency across sessions and providing recovery mechanisms.
    """
    
    def __init__(self, storage_manager: StorageManager):
        """
        Initialize the state manager.
        
        Args:
            storage_manager: Manager for persistent storage
        """
        self.storage_manager = storage_manager
        self.logger = logging.getLogger(__name__)
        
        # Active player states
        self.active_states: Dict[str, PlayerState] = {}
    
    def get_player_state(self, player_id: str) -> PlayerState:
        """
        Get player state, loading from storage if necessary.
        
        Args:
            player_id: ID of the player
            
        Returns:
            Player state object
        """
        if player_id not in self.active_states:
            # Try to load from storage
            saved_state = self.load_player_state(player_id)
            if saved_state:
                self.active_states[player_id] = saved_state
            else:
                # Create new player state
                self.active_states[player_id] = PlayerState(player_id=player_id)
        
        return self.active_states[player_id]
    
    def save_player_state(self, player_state: PlayerState) -> bool:
        """
        Save player state to persistent storage.
        
        Args:
            player_state: Player state to save
            
        Returns:
            True if saved successfully
        """
        try:
            # In a real implementation, this would save to database or file
            # For now, we'll just update the active states
            self.active_states[player_state.player_id] = player_state
            
            self.logger.info(f"Saved state for player {player_state.player_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save state for player {player_state.player_id}: {e}")
            return False
    
    def load_player_state(self, player_id: str) -> Optional[PlayerState]:
        """
        Load player state from persistent storage.
        
        Args:
            player_id: ID of the player
            
        Returns:
            Player state if found, None otherwise
        """
        try:
            # In a real implementation, this would load from database or file
            # For now, return None to indicate no saved state
            return None
        except Exception as e:
            self.logger.error(f"Failed to load state for player {player_id}: {e}")
            return None
    
    def create_checkpoint(self, player_id: str) -> bool:
        """
        Create a checkpoint of the player's current state.
        
        Args:
            player_id: ID of the player
            
        Returns:
            True if checkpoint created successfully
        """
        player_state = self.get_player_state(player_id)
        return self.save_player_state(player_state)
    
    def restore_checkpoint(self, player_id: str) -> bool:
        """
        Restore player state from the last checkpoint.
        
        Args:
            player_id: ID of the player
            
        Returns:
            True if restored successfully
        """
        saved_state = self.load_player_state(player_id)
        if saved_state:
            self.active_states[player_id] = saved_state
            return True
        return False
    
    def cleanup_inactive_states(self, max_age_hours: int = 24) -> int:
        """
        Clean up inactive player states to free memory.
        
        Args:
            max_age_hours: Maximum age in hours for keeping states
            
        Returns:
            Number of states cleaned up
        """
        # In a real implementation, this would check last activity timestamps
        # For now, we'll just return 0
        return 0 