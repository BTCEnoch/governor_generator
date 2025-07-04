#!/usr/bin/env python3
"""
Governor Input Schema - JSON Schema validation for governor data
Validates the structure and required fields of governor JSON files
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from jsonschema import validate, ValidationError
import logging

class GovernorInputValidator:
    """Validates governor JSON input data against schema"""
    
    def __init__(self):
        self.schema = self._create_governor_schema()
        logging.info("🔍 Governor input validator initialized")
    
    def _create_governor_schema(self) -> Dict:
        """Create comprehensive JSON schema for governor data"""
        
        return {
            "type": "object",
            "required": ["governor_name", "blocks", "voidmaker_expansion", "knowledge_base_selections"],
            "properties": {
                "governor_name": {
                    "type": "string",
                    "pattern": "^[A-Z]{6,8}$",
                    "description": "Governor name in all caps, 6-8 characters"
                },
                "blocks": {
                    "type": "object",
                    "required": ["A_identity_origin", "B_cosmic_philosophy", "C_practical_mastery"],
                    "properties": {
                        "A_identity_origin": self._create_block_schema("Identity & Origin", 32),
                        "B_cosmic_philosophy": self._create_block_schema("Cosmic Philosophy", 32), 
                        "C_practical_mastery": self._create_block_schema("Practical Mastery", 32),
                        "D_advanced_concepts": self._create_block_schema("Advanced Concepts", 31)
                    }
                },
                "voidmaker_expansion": {
                    "type": "object",
                    "minProperties": 1,
                    "description": "Voidmaker questions organized by philosophical domains"
                },
                "knowledge_base_selections": {
                    "type": "object",
                    "required": ["chosen_traditions"],
                    "properties": {
                        "chosen_traditions": {
                            "type": "array",
                            "minItems": 1,
                            "maxItems": 10,
                            "items": {"type": "string"}
                        }
                    }
                }
            }
        }
    
    def _create_block_schema(self, block_title: str, expected_questions: int) -> Dict:
        """Create schema for individual question blocks"""
        
        return {
            "type": "object",
            "required": ["title", "questions"],
            "properties": {
                "title": {
                    "type": "string",
                    "enum": [block_title]
                },
                "questions": {
                    "type": "object",
                    "minProperties": expected_questions - 2,  # Allow some flexibility
                    "maxProperties": expected_questions + 2,
                    "patternProperties": {
                        "^[0-9]+$": {
                            "type": "object",
                            "required": ["question", "answer"],
                            "properties": {
                                "question": {
                                    "type": "string",
                                    "minLength": 10
                                },
                                "answer": {
                                    "type": "string", 
                                    "minLength": 20
                                }
                            }
                        }
                    }
                }
            }
        }
    
    def validate_governor_data(self, governor_data: Dict) -> Tuple[bool, List[str]]:
        """Validate governor data against schema"""
        
        errors = []
        
        try:
            validate(instance=governor_data, schema=self.schema)
            
            # Additional semantic validations
            semantic_errors = self._validate_semantic_requirements(governor_data)
            errors.extend(semantic_errors)
            
            is_valid = len(errors) == 0
            
            if is_valid:
                logging.info("✅ Governor data validation passed")
            else:
                logging.warning(f"❌ Governor data validation failed: {len(errors)} errors")
                
            return is_valid, errors
            
        except ValidationError as e:
            error_msg = f"Schema validation failed: {e.message}"
            errors.append(error_msg)
            logging.error(f"❌ {error_msg}")
            return False, errors
    
    def _validate_semantic_requirements(self, governor_data: Dict) -> List[str]:
        """Additional semantic validation beyond JSON schema"""
        
        errors = []
        
        # Check question count consistency
        blocks = governor_data.get("blocks", {})
        total_questions = 0
        
        for block_name, block_data in blocks.items():
            if isinstance(block_data, dict) and "questions" in block_data:
                question_count = len(block_data["questions"])
                total_questions += question_count
        
        # Should have around 127 total questions
        if total_questions < 120 or total_questions > 135:
            errors.append(f"Total question count {total_questions} outside expected range (120-135)")
        
        # Check voidmaker expansion
        voidmaker = governor_data.get("voidmaker_expansion", {})
        voidmaker_questions = 0
        
        for section_data in voidmaker.values():
            if isinstance(section_data, dict) and "questions" in section_data:
                voidmaker_questions += len(section_data["questions"])
        
        # Should have around 42 voidmaker questions
        if voidmaker_questions < 35 or voidmaker_questions > 50:
            errors.append(f"Voidmaker question count {voidmaker_questions} outside expected range (35-50)")
        
        return errors

def validate_governor_file(file_path: Path) -> Tuple[bool, List[str]]:
    """Convenience function to validate a governor file"""
    
    validator = GovernorInputValidator()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            governor_data = json.load(f)
        
        return validator.validate_governor_data(governor_data)
        
    except Exception as e:
        return False, [f"File loading error: {str(e)}"]

if __name__ == "__main__":
    # Test validation with a governor file
    logging.basicConfig(level=logging.INFO)
    
    test_file = Path("../governor_output/ABRIOND.json")
    if test_file.exists():
        is_valid, errors = validate_governor_file(test_file)
        
        if is_valid:
            print("✅ Governor validation passed!")
        else:
            print(f"❌ Governor validation failed:")
            for error in errors:
                print(f"   - {error}")
    else:
        print("❌ Test file not found") 