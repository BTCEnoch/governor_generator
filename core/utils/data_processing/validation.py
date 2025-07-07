"""
Data Validation Utilities
Common validation functions for data processing
"""

import logging
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

T = TypeVar('T')

@dataclass
class ValidationResult(Generic[T]):
    """Result of a validation operation"""
    is_valid: bool
    data: Optional[T] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> ValidationResult:
    """
    Validate that required fields are present in data
    
    Args:
        data: Data to validate
        required_fields: List of required field names
        
    Returns:
        ValidationResult with validation status and errors
    """
    errors = []
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
            
    return ValidationResult(
        is_valid=len(errors) == 0,
        data=data if len(errors) == 0 else None,
        errors=errors
    )

def validate_numeric_range(
    value: Union[int, float],
    min_value: Optional[Union[int, float]] = None,
    max_value: Optional[Union[int, float]] = None
) -> ValidationResult:
    """
    Validate that a numeric value is within range
    
    Args:
        value: Value to validate
        min_value: Minimum allowed value (optional)
        max_value: Maximum allowed value (optional)
        
    Returns:
        ValidationResult with validation status and errors
    """
    errors = []
    
    if min_value is not None and value < min_value:
        errors.append(f"Value {value} is less than minimum {min_value}")
        
    if max_value is not None and value > max_value:
        errors.append(f"Value {value} is greater than maximum {max_value}")
        
    return ValidationResult(
        is_valid=len(errors) == 0,
        data=value if len(errors) == 0 else None,
        errors=errors
    )

def validate_string_length(
    value: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None
) -> ValidationResult:
    """
    Validate string length
    
    Args:
        value: String to validate
        min_length: Minimum allowed length (optional)
        max_length: Maximum allowed length (optional)
        
    Returns:
        ValidationResult with validation status and errors
    """
    errors = []
    
    if min_length is not None and len(value) < min_length:
        errors.append(f"String length {len(value)} is less than minimum {min_length}")
        
    if max_length is not None and len(value) > max_length:
        errors.append(f"String length {len(value)} is greater than maximum {max_length}")
        
    return ValidationResult(
        is_valid=len(errors) == 0,
        data=value if len(errors) == 0 else None,
        errors=errors
    )

def validate_file_path(path: Union[str, Path], must_exist: bool = True) -> ValidationResult:
    """
    Validate a file path
    
    Args:
        path: Path to validate
        must_exist: Whether the file must exist (default: True)
        
    Returns:
        ValidationResult with validation status and errors
    """
    errors = []
    path_obj = Path(path)
    
    if must_exist and not path_obj.exists():
        errors.append(f"File does not exist: {path}")
        
    return ValidationResult(
        is_valid=len(errors) == 0,
        data=path_obj if len(errors) == 0 else None,
        errors=errors
    ) 