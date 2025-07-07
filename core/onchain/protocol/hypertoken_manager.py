"""
TAP Protocol Hypertoken Manager
Handles creation and management of quest, wisdom, and artifact tokens
"""

import json
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TokenState(Enum):
    """Valid states for different token types"""
    # Quest States
    QUEST_INACTIVE = "inactive"
    QUEST_ACTIVE = "active"
    QUEST_COMPLETED = "completed"
    QUEST_FAILED = "failed"
    
    # Wisdom States
    WISDOM_LOCKED = "locked"
    WISDOM_UNLOCKED = "unlocked"
    WISDOM_MASTERED = "mastered"
    
    # Artifact States
    ARTIFACT_DORMANT = "dormant"
    ARTIFACT_ACTIVE = "active"
    ARTIFACT_BOUND = "bound"

@dataclass
class TokenTransition:
    """Represents a valid state transition"""
    from_state: TokenState
    to_state: TokenState
    conditions: Dict[str, any]
    
class TokenType(Enum):
    """Types of hypertokens in the system"""
    QUEST = "quest"
    WISDOM = "wisdom"
    ARTIFACT = "artifact"

@dataclass
class HypertokenMetadata:
    """Base metadata for all hypertokens"""
    token_id: str
    token_type: TokenType
    creation_block: int
    creator_governor: str
    current_state: TokenState
    
@dataclass
class QuestToken(HypertokenMetadata):
    """Quest-specific token data"""
    completion_status: float  # 0-100%
    current_stage: int
    player_progress: Dict[str, any]
    wisdom_gained: int
    difficulty_level: int
    quest_type: str

@dataclass
class WisdomToken(HypertokenMetadata):
    """Wisdom-specific token data"""
    wisdom_level: int
    unlocked_teachings: List[str]
    mastery_progress: float  # 0-100%
    wisdom_type: str
    
@dataclass
class ArtifactToken(HypertokenMetadata):
    """Artifact-specific token data"""
    power_level: int
    activation_status: bool
    bound_to_player: Optional[str]
    artifact_type: str
    rarity_level: int

class HypertokenManager:
    """
    Manages creation, updates, and validation of hypertokens
    Enforces TAP Protocol constraints and TRAC indexing
    """
    
    def __init__(self, tap_client, trac_indexer):
        """Initialize with TAP and TRAC connections"""
        self.tap_client = tap_client
        self.trac_indexer = trac_indexer
        self.load_protocol_constraints()
        
    def load_protocol_constraints(self):
        """Load TAP Protocol constraints from config"""
        self.storage_limits = {
            TokenType.QUEST: 1024,    # bytes
            TokenType.WISDOM: 512,    # bytes
            TokenType.ARTIFACT: 768   # bytes
        }
        
        self.rate_limits = {
            "quests_per_block": 10,
            "wisdom_transfers_per_block": 20,
            "artifact_creations_per_day": 100
        }
        
        self.valid_transitions = {
            TokenType.QUEST: [
                TokenTransition(
                    TokenState.QUEST_INACTIVE,
                    TokenState.QUEST_ACTIVE,
                    {"min_reputation": 0}
                ),
                TokenTransition(
                    TokenState.QUEST_ACTIVE,
                    TokenState.QUEST_COMPLETED,
                    {"completion_status": 100}
                ),
                TokenTransition(
                    TokenState.QUEST_ACTIVE,
                    TokenState.QUEST_FAILED,
                    {"attempts_remaining": 0}
                ),
                TokenTransition(
                    TokenState.QUEST_FAILED,
                    TokenState.QUEST_INACTIVE,
                    {"governor_permission": True}
                )
            ],
            # Add transitions for other token types...
        }
        
    async def create_quest_token(
        self,
        governor_id: str,
        quest_type: str,
        difficulty: int
    ) -> QuestToken:
        """Create a new quest token"""
        try:
            # Check rate limits
            if not await self._check_rate_limit("quests_per_block"):
                raise Exception("Quest creation rate limit exceeded")
                
            # Generate token ID
            token_id = self._generate_token_id(TokenType.QUEST)
            
            # Create base token
            quest_token = QuestToken(
                token_id=token_id,
                token_type=TokenType.QUEST,
                creation_block=await self._get_current_block(),
                creator_governor=governor_id,
                current_state=TokenState.QUEST_INACTIVE,
                completion_status=0,
                current_stage=0,
                player_progress={},
                wisdom_gained=0,
                difficulty_level=difficulty,
                quest_type=quest_type
            )
            
            # Validate size
            if not self._validate_token_size(quest_token):
                raise Exception("Quest token exceeds size limit")
                
            # Create on TAP Protocol
            await self._create_tap_token(quest_token)
            
            # Index with TRAC
            await self._index_token(quest_token)
            
            logger.info(f"Created quest token {token_id} for governor {governor_id}")
            return quest_token
            
        except Exception as e:
            logger.error(f"Failed to create quest token: {e}")
            raise
            
    async def create_wisdom_token(
        self,
        governor_id: str,
        wisdom_type: str
    ) -> WisdomToken:
        """Create a new wisdom token"""
        try:
            if not await self._check_rate_limit("wisdom_transfers_per_block"):
                raise Exception("Wisdom creation rate limit exceeded")
                
            token_id = self._generate_token_id(TokenType.WISDOM)
            
            wisdom_token = WisdomToken(
                token_id=token_id,
                token_type=TokenType.WISDOM,
                creation_block=await self._get_current_block(),
                creator_governor=governor_id,
                current_state=TokenState.WISDOM_LOCKED,
                wisdom_level=0,
                unlocked_teachings=[],
                mastery_progress=0,
                wisdom_type=wisdom_type
            )
            
            if not self._validate_token_size(wisdom_token):
                raise Exception("Wisdom token exceeds size limit")
                
            await self._create_tap_token(wisdom_token)
            await self._index_token(wisdom_token)
            
            logger.info(f"Created wisdom token {token_id} for governor {governor_id}")
            return wisdom_token
            
        except Exception as e:
            logger.error(f"Failed to create wisdom token: {e}")
            raise
            
    async def create_artifact_token(
        self,
        governor_id: str,
        artifact_type: str,
        rarity: int
    ) -> ArtifactToken:
        """Create a new artifact token"""
        try:
            if not await self._check_rate_limit("artifact_creations_per_day"):
                raise Exception("Artifact creation rate limit exceeded")
                
            token_id = self._generate_token_id(TokenType.ARTIFACT)
            
            artifact_token = ArtifactToken(
                token_id=token_id,
                token_type=TokenType.ARTIFACT,
                creation_block=await self._get_current_block(),
                creator_governor=governor_id,
                current_state=TokenState.ARTIFACT_DORMANT,
                power_level=1,
                activation_status=False,
                bound_to_player=None,
                artifact_type=artifact_type,
                rarity_level=rarity
            )
            
            if not self._validate_token_size(artifact_token):
                raise Exception("Artifact token exceeds size limit")
                
            await self._create_tap_token(artifact_token)
            await self._index_token(artifact_token)
            
            logger.info(f"Created artifact token {token_id} for governor {governor_id}")
            return artifact_token
            
        except Exception as e:
            logger.error(f"Failed to create artifact token: {e}")
            raise
            
    async def update_token_state(
        self,
        token_id: str,
        new_state: TokenState,
        **kwargs
    ) -> bool:
        """Update token state if transition is valid"""
        try:
            # Get current token
            token = await self._get_token(token_id)
            if not token:
                raise Exception(f"Token {token_id} not found")
                
            # Validate transition
            if not self._validate_state_transition(token, new_state, **kwargs):
                raise Exception("Invalid state transition")
                
            # Update state
            token.current_state = new_state
            
            # Update additional fields
            for key, value in kwargs.items():
                if hasattr(token, key):
                    setattr(token, key, value)
                    
            # Validate size after updates
            if not self._validate_token_size(token):
                raise Exception("Token size limit exceeded after update")
                
            # Update on TAP Protocol
            await self._update_tap_token(token)
            
            # Update index
            await self._index_token(token)
            
            logger.info(f"Updated token {token_id} state to {new_state}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update token state: {e}")
            raise
            
    def _validate_token_size(self, token: Union[QuestToken, WisdomToken, ArtifactToken]) -> bool:
        """Check if token size is within limits"""
        try:
            token_json = json.dumps(token.__dict__)
            size = len(token_json.encode('utf-8'))
            return size <= self.storage_limits[token.token_type]
        except Exception as e:
            logger.error(f"Token size validation failed: {e}")
            return False
            
    def _validate_state_transition(
        self,
        token: Union[QuestToken, WisdomToken, ArtifactToken],
        new_state: TokenState,
        **kwargs
    ) -> bool:
        """Check if state transition is valid"""
        try:
            valid_transitions = self.valid_transitions[token.token_type]
            
            # Find matching transition
            for transition in valid_transitions:
                if (transition.from_state == token.current_state and
                    transition.to_state == new_state):
                    # Check conditions
                    for condition, required_value in transition.conditions.items():
                        if condition not in kwargs or kwargs[condition] != required_value:
                            return False
                    return True
            return False
            
        except Exception as e:
            logger.error(f"State transition validation failed: {e}")
            return False
            
    async def _check_rate_limit(self, limit_type: str) -> bool:
        """Check if operation is within rate limits"""
        try:
            current_block = await self._get_current_block()
            count = await self.trac_indexer.get_operation_count(limit_type, current_block)
            return count < self.rate_limits[limit_type]
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            return False
            
    async def _create_tap_token(self, token: Union[QuestToken, WisdomToken, ArtifactToken]):
        """Create token on TAP Protocol"""
        try:
            await self.tap_client.create_token(
                token_id=token.token_id,
                metadata=token.__dict__
            )
        except Exception as e:
            logger.error(f"TAP token creation failed: {e}")
            raise
            
    async def _update_tap_token(self, token: Union[QuestToken, WisdomToken, ArtifactToken]):
        """Update token on TAP Protocol"""
        try:
            await self.tap_client.update_token(
                token_id=token.token_id,
                metadata=token.__dict__
            )
        except Exception as e:
            logger.error(f"TAP token update failed: {e}")
            raise
            
    async def _index_token(self, token: Union[QuestToken, WisdomToken, ArtifactToken]):
        """Index token with TRAC"""
        try:
            await self.trac_indexer.index_token(
                token_id=token.token_id,
                token_type=token.token_type.value,
                metadata=token.__dict__
            )
        except Exception as e:
            logger.error(f"TRAC indexing failed: {e}")
            raise
            
    async def _get_current_block(self) -> int:
        """Get current Bitcoin block height"""
        try:
            return await self.tap_client.get_block_height()
        except Exception as e:
            logger.error(f"Failed to get current block: {e}")
            raise
            
    def _generate_token_id(self, token_type: TokenType) -> str:
        """Generate unique token ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{token_type.value}_{timestamp}" 