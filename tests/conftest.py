"""
Shared test fixtures and configuration
"""

import os
import json
import logging
import pytest
from pathlib import Path
from typing import Dict, Any, Generator
from core.utils.custom_logging.custom_logger import setup_logger
from core.utils.mystical.base import MysticalSystem
from core.utils.data.validation import ValidationResult

# Configure logging for tests
@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """Configure logging for test session"""
    setup_logger(
        name="test_logger",
        log_file=Path("logs/test.log"),
        level=logging.DEBUG,
        format_string="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

# Test data directory
@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Get test data directory"""
    return Path(__file__).parent / "data"

# Sample JSON data
@pytest.fixture
def sample_json_data() -> Dict[str, Any]:
    """Get sample JSON data for testing"""
    return {
        "id": "test_123",
        "name": "Test Entity",
        "attributes": [
            {"name": "attr1", "value": "value1"},
            {"name": "attr2", "value": "value2"}
        ],
        "metadata": {
            "created": "2024-01-01",
            "version": "1.0"
        }
    }

# Temporary file
@pytest.fixture
def temp_file(tmp_path) -> Generator[Path, None, None]:
    """Create temporary file for testing"""
    file_path = tmp_path / "test.json"
    with open(file_path, "w") as f:
        json.dump({"test": "data"}, f)
    yield file_path
    if file_path.exists():
        file_path.unlink()

# Mock mystical system
@pytest.fixture
def mock_mystical_system() -> MysticalSystem:
    """Create mock mystical system for testing"""
    class MockSystem(MysticalSystem):
        def validate_input(self, data: Any) -> ValidationResult:
            return ValidationResult(is_valid=True, data=data)
            
        def format_output(self, result: Any) -> Any:
            return result
            
        def calculate_correspondences(self, data: Dict[str, Any]) -> Dict[str, Any]:
            return {"test": "correspondence"}
            
    return MockSystem(id="mock_system_001", name="Mock System", description="Test mock system")

# Sample validation data
@pytest.fixture
def sample_validation_data() -> Dict[str, Any]:
    """Get sample data for validation testing"""
    return {
        "required_field": "value",
        "numeric_field": 42,
        "string_field": "test string",
        "nested": {
            "field1": "value1",
            "field2": "value2"
        }
    }

# Sample error data
@pytest.fixture
def sample_error_data() -> Dict[str, Any]:
    """Get sample error data for testing"""
    return {
        "error_type": "ValidationError",
        "message": "Test error message",
        "details": {
            "field": "test_field",
            "reason": "invalid value"
        }
    }

# Sample progress data
@pytest.fixture
def sample_progress_data() -> Dict[str, Any]:
    """Get sample progress tracking data"""
    return {
        "total": 100,
        "completed": 42,
        "failed": 8,
        "success_rate": 0.84,
        "items_per_second": 10.5
    } 