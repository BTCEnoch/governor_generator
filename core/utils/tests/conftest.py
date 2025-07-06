"""
Common test configuration and fixtures
"""

import os
import sys
import pytest
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture
def test_data_dir():
    """Return the path to the test data directory"""
    return Path(__file__).parent / "data"

@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for test files"""
    test_dir = tmp_path / "test_files"
    test_dir.mkdir()
    return test_dir

@pytest.fixture
def sample_json_data():
    """Return sample JSON data for testing"""
    return {
        "id": "test_id",
        "name": "Test Name",
        "attributes": {
            "wisdom": 42,
            "power": 100
        },
        "metadata": {
            "source": "test",
            "version": "1.0"
        }
    }

@pytest.fixture
def sample_file_paths(temp_dir):
    """Create sample files for testing"""
    # Create test files
    files = {
        "json": temp_dir / "test.json",
        "text": temp_dir / "test.txt",
        "python": temp_dir / "test.py",
        "markdown": temp_dir / "test.md"
    }
    
    # Write sample content
    files["json"].write_text('{"test": "data"}')
    files["text"].write_text("Test content")
    files["python"].write_text("def test(): pass")
    files["markdown"].write_text("# Test")
    
    return files 