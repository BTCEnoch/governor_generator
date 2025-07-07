"""
Tests for TAP Protocol Hypertoken Manager
"""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from core.onchain.protocol.hypertoken_manager import (
    HypertokenManager,
    TokenType,
    TokenState,
    QuestToken,
    WisdomToken,
    ArtifactToken
)

# Mock TAP client and TRAC indexer
@pytest.fixture
def tap_client():
    client = AsyncMock()
    client.get_block_height = AsyncMock(return_value=100)
    client.create_token = AsyncMock()
    client.update_token = AsyncMock()
    return client

@pytest.fixture
def trac_indexer():
    indexer = AsyncMock()
    indexer.get_operation_count = AsyncMock(return_value=0)
    indexer.index_token = AsyncMock()
    return indexer

@pytest.fixture
def token_manager(tap_client, trac_indexer):
    return HypertokenManager(tap_client, trac_indexer)

@pytest.mark.asyncio
async def test_create_quest_token(token_manager):
    """Test quest token creation"""
    governor_id = "TEST_GOV_001"
    quest_type = "wisdom_trial"
    difficulty = 5
    
    token = await token_manager.create_quest_token(
        governor_id=governor_id,
        quest_type=quest_type,
        difficulty=difficulty
    )
    
    assert isinstance(token, QuestToken)
    assert token.token_type == TokenType.QUEST
    assert token.creator_governor == governor_id
    assert token.current_state == TokenState.QUEST_INACTIVE
    assert token.difficulty_level == difficulty
    assert token.quest_type == quest_type
    
    # Verify TAP and TRAC calls
    token_manager.tap_client.create_token.assert_called_once()
    token_manager.trac_indexer.index_token.assert_called_once()

@pytest.mark.asyncio
async def test_create_wisdom_token(token_manager):
    """Test wisdom token creation"""
    governor_id = "TEST_GOV_001"
    wisdom_type = "elemental_wisdom"
    
    token = await token_manager.create_wisdom_token(
        governor_id=governor_id,
        wisdom_type=wisdom_type
    )
    
    assert isinstance(token, WisdomToken)
    assert token.token_type == TokenType.WISDOM
    assert token.creator_governor == governor_id
    assert token.current_state == TokenState.WISDOM_LOCKED
    assert token.wisdom_type == wisdom_type
    assert token.wisdom_level == 0
    
    token_manager.tap_client.create_token.assert_called_once()
    token_manager.trac_indexer.index_token.assert_called_once()

@pytest.mark.asyncio
async def test_create_artifact_token(token_manager):
    """Test artifact token creation"""
    governor_id = "TEST_GOV_001"
    artifact_type = "mystical_orb"
    rarity = 3
    
    token = await token_manager.create_artifact_token(
        governor_id=governor_id,
        artifact_type=artifact_type,
        rarity=rarity
    )
    
    assert isinstance(token, ArtifactToken)
    assert token.token_type == TokenType.ARTIFACT
    assert token.creator_governor == governor_id
    assert token.current_state == TokenState.ARTIFACT_DORMANT
    assert token.artifact_type == artifact_type
    assert token.rarity_level == rarity
    assert not token.activation_status
    assert token.bound_to_player is None
    
    token_manager.tap_client.create_token.assert_called_once()
    token_manager.trac_indexer.index_token.assert_called_once()

@pytest.mark.asyncio
async def test_rate_limiting(token_manager):
    """Test rate limiting functionality"""
    # Mock rate limit exceeded
    token_manager.trac_indexer.get_operation_count.return_value = 11  # Above quest limit
    
    with pytest.raises(Exception) as exc_info:
        await token_manager.create_quest_token(
            governor_id="TEST_GOV_001",
            quest_type="test",
            difficulty=1
        )
    assert "rate limit exceeded" in str(exc_info.value).lower()

@pytest.mark.asyncio
async def test_token_size_validation(token_manager):
    """Test token size validation"""
    # Create a token that would exceed size limit
    huge_data = "x" * 2000  # Exceeds all token size limits
    
    with pytest.raises(Exception) as exc_info:
        await token_manager.create_quest_token(
            governor_id=huge_data,
            quest_type=huge_data,
            difficulty=1
        )
    assert "size limit" in str(exc_info.value).lower()

@pytest.mark.asyncio
async def test_state_transitions(token_manager):
    """Test token state transition validation"""
    # Create a quest token
    token = await token_manager.create_quest_token(
        governor_id="TEST_GOV_001",
        quest_type="test",
        difficulty=1
    )
    
    # Valid transition: inactive -> active
    success = await token_manager.update_token_state(
        token.token_id,
        TokenState.QUEST_ACTIVE,
        min_reputation=0
    )
    assert success
    
    # Invalid transition: active -> completed without 100% completion
    with pytest.raises(Exception) as exc_info:
        await token_manager.update_token_state(
            token.token_id,
            TokenState.QUEST_COMPLETED,
            completion_status=50  # Not complete
        )
    assert "Invalid state transition" in str(exc_info.value)

@pytest.mark.asyncio
async def test_token_updates(token_manager):
    """Test token update functionality"""
    # Create and update a wisdom token
    token = await token_manager.create_wisdom_token(
        governor_id="TEST_GOV_001",
        wisdom_type="test"
    )
    
    # Update wisdom level
    await token_manager.update_token_state(
        token.token_id,
        TokenState.WISDOM_UNLOCKED,
        wisdom_level=1,
        mastery_progress=25.0
    )
    
    # Verify TAP and TRAC updates
    token_manager.tap_client.update_token.assert_called_once()
    assert token_manager.trac_indexer.index_token.call_count == 2  # Create + update

@pytest.mark.asyncio
async def test_error_handling(token_manager):
    """Test error handling"""
    # Test TAP client failure
    token_manager.tap_client.create_token.side_effect = Exception("TAP error")
    
    with pytest.raises(Exception) as exc_info:
        await token_manager.create_quest_token(
            governor_id="TEST_GOV_001",
            quest_type="test",
            difficulty=1
        )
    assert "TAP" in str(exc_info.value)
    
    # Test TRAC indexer failure
    token_manager.tap_client.create_token.side_effect = None  # Reset
    token_manager.trac_indexer.index_token.side_effect = Exception("TRAC error")
    
    with pytest.raises(Exception) as exc_info:
        await token_manager.create_quest_token(
            governor_id="TEST_GOV_001",
            quest_type="test",
            difficulty=1
        )
    assert "TRAC" in str(exc_info.value) 