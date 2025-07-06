"""
Data Validation Utilities
Common validation functions for the Governor Generation system
"""

import logging
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic
from dataclasses import dataclass, field
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

T = TypeVar('T')

@dataclass
class ValidationResult(Generic[T]):
    """Result of a validation operation"""
    is_valid: bool
    data: Optional[T] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def __post_init__(self):
        # No need for post_init since we use default_factory
        pass

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> ValidationResult:
    """Validate that all required fields are present and not None"""
    errors = []
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif data[field] is None:
            errors.append(f"Required field cannot be None: {field}")
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        data=data if len(errors) == 0 else None,
        errors=errors
    )

def validate_numeric_range(value: Union[int, float], min_value: Optional[Union[int, float]] = None,
                         max_value: Optional[Union[int, float]] = None,
                         field_name: str = "value") -> ValidationResult:
    """Validate that a numeric value is within the specified range"""
    errors = []
    
    if min_value is not None and value < min_value:
        errors.append(f"{field_name} must be >= {min_value}")
    
    if max_value is not None and value > max_value:
        errors.append(f"{field_name} must be <= {max_value}")
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        data=value if len(errors) == 0 else None,
        errors=errors
    )

def validate_file_path(path: Union[str, Path], must_exist: bool = True,
                      file_type: Optional[str] = None) -> ValidationResult:
    """Validate a file path"""
    errors = []
    warnings = []
    
    # Convert to Path if string
    if isinstance(path, str):
        path = Path(path)
    
    # Check existence if required
    if must_exist and not path.exists():
        errors.append(f"File does not exist: {path}")
    
    # Check file type if specified
    if file_type and path.suffix.lower() != f".{file_type.lower()}":
        errors.append(f"File must be a {file_type} file: {path}")
    
    # Check if path is absolute
    if not path.is_absolute():
        warnings.append(f"Using relative path: {path}")
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        data=path if len(errors) == 0 else None,
        errors=errors,
        warnings=warnings
    )

def validate_string_length(value: str, min_length: Optional[int] = None,
                         max_length: Optional[int] = None,
                         field_name: str = "value") -> ValidationResult:
    """Validate string length is within specified range"""
    errors = []
    
    if min_length is not None and len(value) < min_length:
        errors.append(f"{field_name} must be at least {min_length} characters")
    
    if max_length is not None and len(value) > max_length:
        errors.append(f"{field_name} must be at most {max_length} characters")
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        data=value if len(errors) == 0 else None,
        errors=errors
    )

def validate_list_length(values: List[Any], min_length: Optional[int] = None,
                       max_length: Optional[int] = None,
                       field_name: str = "list") -> ValidationResult:
    """Validate list length is within specified range"""
    errors = []
    
    if min_length is not None and len(values) < min_length:
        errors.append(f"{field_name} must have at least {min_length} items")
    
    if max_length is not None and len(values) > max_length:
        errors.append(f"{field_name} must have at most {max_length} items")
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        data=values if len(errors) == 0 else None,
        errors=errors
    ) 