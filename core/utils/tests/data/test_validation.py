"""
Tests for data validation utilities
"""

import pytest
from pathlib import Path
from typing import Dict, Any
from core.utils.data.validation import (
    ValidationResult,
    validate_required_fields,
    validate_numeric_range,
    validate_file_path,
    validate_string_length,
    validate_list_length
)

def test_validation_result_initialization():
    """Test ValidationResult initialization and defaults"""
    # Test with minimal args
    result = ValidationResult(is_valid=True)
    assert result.is_valid is True
    assert result.data is None
    assert result.errors == []
    assert result.warnings == []
    
    # Test with all args
    result = ValidationResult(
        is_valid=False,
        data="test",
        errors=["error1"],
        warnings=["warning1"]
    )
    assert result.is_valid is False
    assert result.data == "test"
    assert result.errors == ["error1"]
    assert result.warnings == ["warning1"]

def test_validate_required_fields():
    """Test required fields validation"""
    # Test valid case
    data: Dict[str, Any] = {
        "name": "test",
        "value": 42,
        "optional": None
    }
    result = validate_required_fields(data, ["name", "value"])
    assert result.is_valid is True
    assert result.data == data
    assert not result.errors
    
    # Test missing field
    result = validate_required_fields(data, ["name", "missing"])
    assert result.is_valid is False
    assert "missing" in result.errors[0]
    
    # Test None value
    result = validate_required_fields(data, ["name", "optional"])
    assert result.is_valid is False
    assert "optional" in result.errors[0]

def test_validate_numeric_range():
    """Test numeric range validation"""
    # Test valid cases
    result = validate_numeric_range(5, min_value=0, max_value=10)
    assert result.is_valid is True
    assert result.data == 5
    
    result = validate_numeric_range(0, min_value=0)
    assert result.is_valid is True
    
    result = validate_numeric_range(10, max_value=10)
    assert result.is_valid is True
    
    # Test invalid cases
    result = validate_numeric_range(-1, min_value=0)
    assert result.is_valid is False
    assert "must be >=" in result.errors[0]
    
    result = validate_numeric_range(11, max_value=10)
    assert result.is_valid is False
    assert "must be <=" in result.errors[0]

def test_validate_file_path(tmp_path):
    """Test file path validation"""
    # Create test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("test")
    
    # Test valid cases
    result = validate_file_path(test_file)
    assert result.is_valid is True
    assert result.data == test_file
    
    result = validate_file_path(test_file, file_type="txt")
    assert result.is_valid is True
    
    # Test non-existent file
    result = validate_file_path(tmp_path / "missing.txt")
    assert result.is_valid is False
    assert "does not exist" in result.errors[0]
    
    # Test wrong file type
    result = validate_file_path(test_file, file_type="json")
    assert result.is_valid is False
    assert "must be a json file" in result.errors[0]
    
    # Test relative path warning
    result = validate_file_path("relative/path.txt", must_exist=False)
    assert result.is_valid is True
    assert "relative path" in result.warnings[0]

def test_validate_string_length():
    """Test string length validation"""
    # Test valid cases
    result = validate_string_length("test", min_length=2, max_length=10)
    assert result.is_valid is True
    assert result.data == "test"
    
    result = validate_string_length("a", min_length=1)
    assert result.is_valid is True
    
    result = validate_string_length("abc", max_length=3)
    assert result.is_valid is True
    
    # Test invalid cases
    result = validate_string_length("a", min_length=2)
    assert result.is_valid is False
    assert "at least 2" in result.errors[0]
    
    result = validate_string_length("test", max_length=3)
    assert result.is_valid is False
    assert "at most 3" in result.errors[0]

def test_validate_list_length():
    """Test list length validation"""
    # Test valid cases
    result = validate_list_length([1, 2, 3], min_length=2, max_length=5)
    assert result.is_valid is True
    assert result.data == [1, 2, 3]
    
    result = validate_list_length([1], min_length=1)
    assert result.is_valid is True
    
    result = validate_list_length([1, 2, 3], max_length=3)
    assert result.is_valid is True
    
    # Test invalid cases
    result = validate_list_length([1], min_length=2)
    assert result.is_valid is False
    assert "at least 2" in result.errors[0]
    
    result = validate_list_length([1, 2, 3, 4], max_length=3)
    assert result.is_valid is False
    assert "at most 3" in result.errors[0] 