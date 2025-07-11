"""
Tests for the I Ching System
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from core.mystical_systems.iching_system import IChingSystem
from core.mystical_systems.iching_system.schemas import (
    IChingHexagram,
    IChingProfile,
    LineChange
)

@pytest.fixture
def mock_bitcoin_integration():
    """Mock BitcoinIntegration for testing"""
    with patch("core.mystical_systems.iching_system.iching_system.BitcoinIntegration") as mock:
        mock_instance = MagicMock()
        mock_instance.generate_number.return_value = 6  # Default to changing yin
        mock_instance.validate_bitcoin_data.return_value = True
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_wikipedia_iching():
    """Mock WikipediaIChing for testing"""
    with patch("core.mystical_systems.iching_system.iching_system.WikipediaIChing") as mock:
        mock_instance = AsyncMock()
        mock_instance.get_hexagram_data.return_value = {
            "unicode": "䷀",
            "name": "Test Hexagram",
            "description": "Test Description",
            "judgment": "Test Judgment",
            "image": "Test Image",
            "line_meanings": {
                "1": "First line meaning",
                "2": "Second line meaning",
                "3": "Third line meaning",
                "4": "Fourth line meaning",
                "5": "Fifth line meaning",
                "6": "Sixth line meaning"
            }
        }
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def iching_system(mock_bitcoin_integration, mock_wikipedia_iching):
    """Create an I Ching system instance for testing"""
    return IChingSystem()

@pytest.mark.asyncio
async def test_generate_profile_basic(iching_system):
    """Test basic profile generation"""
    data = {"question": "Test question"}
    
    async with iching_system:
        profile = await iching_system.generate_profile(data)
        
    assert isinstance(profile, IChingProfile)
    assert "Test question" in profile.name
    assert profile.initial_hexagram.number >= 1
    assert profile.initial_hexagram.number <= 64
    assert len(profile.initial_hexagram.lines) == 6
    assert all(line.position >= 1 and line.position <= 6 for line in profile.initial_hexagram.lines)

@pytest.mark.asyncio
async def test_generate_profile_with_bitcoin(iching_system):
    """Test profile generation with Bitcoin integration"""
    data = {
        "question": "Test question",
        "txid": "1234567890abcdef"
    }
    
    async with iching_system:
        profile = await iching_system.generate_profile(data)
        
    assert isinstance(profile, IChingProfile)
    assert profile.bitcoin_resonance is not None
    assert len(profile.attributes) > 0

@pytest.mark.asyncio
async def test_generate_profile_with_changing_lines(iching_system, mock_bitcoin_integration):
    """Test profile generation with changing lines"""
    # Set up mock to generate changing lines
    mock_bitcoin_integration.generate_number.side_effect = [6, 7, 8, 9, 6, 7]
    
    data = {"question": "Test question"}
    
    async with iching_system:
        profile = await iching_system.generate_profile(data)
        
    assert isinstance(profile, IChingProfile)
    assert profile.transformed_hexagram is not None
    assert len(profile.changing_line_meanings) > 0
    assert profile.initial_hexagram.number != profile.transformed_hexagram.number

@pytest.mark.asyncio
async def test_generate_profile_validation(iching_system):
    """Test input validation"""
    # Test missing required fields
    with pytest.raises(ValueError) as exc_info:
        async with iching_system:
            await iching_system.generate_profile({})
    assert "Invalid input data" in str(exc_info.value)
    
    # Test invalid Bitcoin data
    data = {
        "question": "Test question",
        "txid": "invalid"
    }
    with patch("core.mystical_systems.iching_system.iching_system.BitcoinIntegration") as mock:
        mock_instance = MagicMock()
        mock_instance.validate_bitcoin_data.return_value = False
        mock.return_value = mock_instance
        
        system = IChingSystem()
        with pytest.raises(ValueError) as exc_info:
            async with system:
                await system.generate_profile(data)
    assert "Invalid input data" in str(exc_info.value)

@pytest.mark.asyncio
async def test_line_generation(iching_system, mock_bitcoin_integration):
    """Test line generation mechanics"""
    # Test all possible line values
    test_values = [
        (6, (0, LineChange.YIN_TO_YANG)),
        (7, (0, LineChange.STABLE_YIN)),
        (8, (1, LineChange.STABLE_YANG)),
        (9, (1, LineChange.YANG_TO_YIN))
    ]
    
    for value, expected in test_values:
        mock_bitcoin_integration.generate_number.return_value = value
        result = iching_system._generate_line("test_seed")
        assert result == expected

@pytest.mark.asyncio
async def test_hexagram_conversion(iching_system):
    """Test binary to hexagram number conversion"""
    test_cases = [
        ([0, 0, 0, 0, 0, 0], 1),  # All yin
        ([1, 1, 1, 1, 1, 1], 64),  # All yang
        ([1, 0, 1, 0, 1, 0], 43)  # Alternating
    ]
    
    for lines, expected_number in test_cases:
        result = iching_system._lines_to_number(lines)
        assert result == expected_number 