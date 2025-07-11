"""
Validation utilities for data structures
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Result of schema validation"""
    is_valid: bool
    data: Any
    errors: Optional[List[str]] = None

def validate_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> ValidationResult:
    """
    Validate data against a schema
    
    Args:
        data: Data to validate
        schema: Schema to validate against
        
    Returns:
        ValidationResult with validation status and errors
    """
    errors = []
    
    # Check required fields
    for field, field_schema in schema.items():
        if field_schema.get("required", False) and field not in data:
            errors.append(f"Missing required field: {field}")
            continue
            
        if field in data:
            # Validate field type
            expected_type = field_schema.get("type")
            if expected_type and not isinstance(data[field], expected_type):
                errors.append(f"Invalid type for {field}: expected {expected_type.__name__}, got {type(data[field]).__name__}")
                
            # Validate field constraints
            constraints = field_schema.get("constraints", {})
            for constraint, value in constraints.items():
                if constraint == "min_length" and len(data[field]) < value:
                    errors.append(f"Field {field} is too short: minimum length is {value}")
                elif constraint == "max_length" and len(data[field]) > value:
                    errors.append(f"Field {field} is too long: maximum length is {value}")
                elif constraint == "min_value" and data[field] < value:
                    errors.append(f"Field {field} is too small: minimum value is {value}")
                elif constraint == "max_value" and data[field] > value:
                    errors.append(f"Field {field} is too large: maximum value is {value}")
                elif constraint == "pattern" and not value.match(data[field]):
                    errors.append(f"Field {field} does not match pattern: {value.pattern}")
                elif constraint == "enum" and data[field] not in value:
                    errors.append(f"Invalid value for {field}: must be one of {value}")
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        data=data,
        errors=errors if errors else None
    ) 