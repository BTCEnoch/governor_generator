import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from core.mystical_systems.iching import IChing
from core.utils.mystical.bitcoin_integration import BitcoinEntropy

@pytest.fixture
def mock_bitcoin_entropy():
    """Mock BitcoinEntropy for deterministic testing."""
    mock = MagicMock(spec=BitcoinEntropy)
    # Set up deterministic line generation
    mock.generate_number.side_effect = [
        6,  # Line 1: changing yin (0)
        7,  # Line 2: stable yin (0)
        8,  # Line 3: stable yang (1)
        9,  # Line 4: changing yang (1)
        7,  # Line 5: stable yin (0)
        8,  # Line 6: stable yang (1)
    ]
    return mock

@pytest.fixture
def mock_wikipedia_iching():
    """Mock WikipediaIChing for testing."""
    mock = AsyncMock()
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = None
    
    # Mock hexagram data
    mock.get_hexagram_data.side_effect = lambda num: {
        "number": num,
        "unicode_char": chr(0x4DC0 + num - 1),
        "title": f"Test Hexagram {num}",
        "sections": {
            "interpretation": "Test interpretation",
            "the judgment": "Test judgment",
            "the image": "Test image",
            "the lines": "Test lines"
        }
    }
    return mock

@pytest.fixture
async def iching(mock_bitcoin_entropy, mock_wikipedia_iching):
    """Create IChing instance with mocked dependencies."""
    with patch("core.mystical_systems.iching.BitcoinEntropy", return_value=mock_bitcoin_entropy):
        with patch("core.mystical_systems.iching.WikipediaIChing", return_value=mock_wikipedia_iching):
            async with IChing() as instance:
                yield instance

@pytest.mark.asyncio
async def test_generate_line(iching):
    """Test single line generation."""
    line_value, is_changing = iching._generate_line("test_seed")
    assert line_value == 0  # yin
    assert is_changing == True  # changing (6)

@pytest.mark.asyncio
async def test_generate_hexagram(iching):
    """Test complete hexagram generation."""
    lines, changing_lines = iching.generate_hexagram("test_seed")
    
    # Verify line values based on mock sequence
    assert lines == [0, 0, 1, 1, 0, 1]  # bottom to top
    assert changing_lines == [True, False, False, True, False, False]

@pytest.mark.asyncio
async def test_lines_to_number(iching):
    """Test conversion of lines to hexagram number."""
    lines = [1, 0, 1, 0, 1, 0]  # Example lines
    number = iching._lines_to_number(lines)
    assert 1 <= number <= 64  # Valid hexagram number

@pytest.mark.asyncio
async def test_cast_hexagram(iching):
    """Test complete hexagram casting with changing lines."""
    result = await iching.cast_hexagram("test_seed")
    
    assert "initial_hexagram" in result
    assert "changing_hexagram" in result
    assert "changing_lines" in result
    
    # Verify changing lines are detected
    assert any(result["changing_lines"])
    
    # Verify both hexagrams have valid data
    assert result["initial_hexagram"]["number"] >= 1
    assert result["initial_hexagram"]["number"] <= 64
    assert "title" in result["initial_hexagram"]
    
    if result["changing_hexagram"]:
        assert result["changing_hexagram"]["number"] >= 1
        assert result["changing_hexagram"]["number"] <= 64
        assert "title" in result["changing_hexagram"] 