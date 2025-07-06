"""
Tests for the Universal JSON Cleaner
"""

import json
import pytest
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from .cleaner import JSONCleaner

@pytest.fixture
def cleaner():
    """Create a test cleaner instance"""
    return JSONCleaner(log_dir="test_logs")

@pytest.fixture
def cleanup():
    """Clean up test files after tests"""
    yield
    # Remove test files
    test_files = [
        "test_logs/cleaning_log.txt",
        "test_input.json",
        "test_output.json"
    ]
    for file in test_files:
        path = Path(file)
        if path.exists():
            path.unlink()
    
    # Remove test directory
    test_log_dir = Path("test_logs")
    if test_log_dir.exists():
        test_log_dir.rmdir()

def test_clean_string(cleaner):
    """Test string cleaning"""
    # Test control characters
    assert cleaner._clean_string("Hello\x00World") == "Hello World"
    
    # Test whitespace
    assert cleaner._clean_string("Hello   World  ") == "Hello World"
    
    # Test smart quotes
    assert cleaner._clean_string(""Hello World"") == '"Hello World"'
    assert cleaner._clean_string("'Hello World'") == "'Hello World'"
    
    # Test special characters
    assert cleaner._clean_string("Hello—World") == "Hello-World"
    assert cleaner._clean_string("Hello…World") == "Hello...World"

def test_clean_dict(cleaner):
    """Test dictionary cleaning"""
    dirty_dict = {
        "key\x00": "value\x00",
        "nested": {
            "key": "value   with   spaces"
        },
        "list": ["item\x00", {"key": "value\x00"}]
    }
    
    cleaned = cleaner._clean_dict(dirty_dict)
    
    assert "key" in cleaned
    assert cleaned["key"] == "value"
    assert cleaned["nested"]["key"] == "value with spaces"
    assert cleaned["list"][0] == "item"
    assert cleaned["list"][1]["key"] == "value"

def test_clean_list(cleaner):
    """Test list cleaning"""
    dirty_list = [
        "item\x00",
        {"key\x00": "value\x00"},
        ["nested\x00", "items\x00"]
    ]
    
    cleaned = cleaner._clean_list(dirty_list)
    
    assert cleaned[0] == "item"
    assert cleaned[1]["key"] == "value"
    assert cleaned[2] == ["nested", "items"]

def test_clean_file(cleaner, cleanup):
    """Test file cleaning"""
    # Create test input file
    input_data = {
        "key\x00": "value\x00",
        "nested": {
            "key": "value   with   spaces"
        }
    }
    
    input_file = Path("test_input.json")
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(input_data, f)
    
    # Clean file
    output_file = Path("test_output.json")
    result = cleaner.clean_file(input_file, output_file)
    
    # Verify output
    assert result == output_file
    assert output_file.exists()
    
    with open(output_file, 'r', encoding='utf-8') as f:
        cleaned_data = json.load(f)
        
    assert "key" in cleaned_data
    assert cleaned_data["key"] == "value"
    assert cleaned_data["nested"]["key"] == "value with spaces"

def test_validate_json(cleaner):
    """Test JSON validation"""
    # Valid JSON
    valid_data = {
        "key": "value",
        "number": 42,
        "list": [1, 2, 3]
    }
    assert cleaner.validate_json(valid_data) is True
    
    # Invalid JSON (cannot be serialized)
    invalid_data = {
        "key": object()
    }
    assert cleaner.validate_json(invalid_data) is False
    
    # Test with schema
    schema = {
        "type": "object",
        "properties": {
            "key": {"type": "string"},
            "number": {"type": "number"},
            "list": {
                "type": "array",
                "items": {"type": "number"}
            }
        },
        "required": ["key", "number", "list"]
    }
    
    assert cleaner.validate_json(valid_data, schema) is True
    
    # Invalid against schema
    invalid_schema_data = {
        "key": 123,  # Should be string
        "number": "42",  # Should be number
        "list": [1, "2", 3]  # All items should be numbers
    }
    assert cleaner.validate_json(invalid_schema_data, schema) is False

def test_normalize_json(cleaner):
    """Test JSON normalization"""
    # Test dictionary key sorting
    unsorted = {
        "c": 3,
        "a": 1,
        "b": 2
    }
    normalized = cleaner.normalize_json(unsorted)
    assert list(normalized.keys()) == ["a", "b", "c"]
    
    # Test nested structures
    nested = {
        "b": {
            "y": 2,
            "x": 1
        },
        "a": [2, 1, 3]
    }
    normalized = cleaner.normalize_json(nested)
    assert list(normalized.keys()) == ["a", "b"]
    assert list(normalized["b"].keys()) == ["x", "y"]
    
    # Test string normalization
    with_strings = {
        "text": "Hello   World",
        "nested": {
            "text": ""Quoted""
        }
    }
    normalized = cleaner.normalize_json(with_strings)
    assert normalized["text"] == "Hello World"
    assert normalized["nested"]["text"] == '"Quoted"'

def test_error_logging(cleaner, cleanup):
    """Test error logging"""
    # Create invalid JSON file
    input_file = Path("test_input.json")
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write("invalid json")
    
    # Try to clean file (should fail)
    with pytest.raises(Exception):
        cleaner.clean_file(input_file, "test_output.json")
    
    # Check log file
    log_file = Path("test_logs/cleaning_log.txt")
    assert log_file.exists()
    
    with open(log_file, 'r', encoding='utf-8') as f:
        log_content = f.read()
        assert "ERROR" in log_content
        assert str(input_file) in log_content 