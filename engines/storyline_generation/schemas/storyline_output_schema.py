#!/usr/bin/env python3
"""
Storyline Output Schema - JSON Schema validation for rich storyline data
Validates the structure and quality of generated storyline JSON files
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from jsonschema import validate, ValidationError
import logging

class StorylineOutputValidator:
    """Validates storyline JSON output data against schema"""
    
    def __init__(self):
        self.schema = self._create_storyline_schema()
        logging.info("🔍 Storyline output validator initialized")
    
    def _create_storyline_schema(self) -> Dict:
        """Create comprehensive JSON schema for storyline data"""
        
        return {
            "type": "object",
            "required": ["governor_name", "storyline_metadata", "reputation_tiers", "narrative_nodes"],
            "properties": {
                "governor_name": {
                    "type": "string",
                    "pattern": "^[A-Z]{6,8}$"
                },
                "storyline_metadata": {
                    "type": "object",
                    "required": ["version", "generation_timestamp", "total_nodes", "canonical_elements"],
                    "properties": {
                        "version": {"type": "string"},
                        "generation_timestamp": {"type": "string"},
                        "total_nodes": {
                            "type": "integer",
                            "minimum": 20,
                            "maximum": 35
                        },
                        "canonical_elements": {
                            "type": "object",
                            "required": ["aethyrs", "watchtowers", "elements"],
                            "properties": {
                                "aethyrs": {"type": "array", "minItems": 1},
                                "watchtowers": {"type": "array", "minItems": 1},
                                "elements": {"type": "array", "minItems": 1}
                            }
                        }
                    }
                },
                "reputation_tiers": {
                    "type": "object",
                    "required": ["tier_1", "tier_2", "tier_3", "tier_4"],
                    "properties": {
                        "tier_1": self._create_tier_schema("0-25", "novice"),
                        "tier_2": self._create_tier_schema("26-50", "apprentice"),
                        "tier_3": self._create_tier_schema("51-75", "adept"),
                        "tier_4": self._create_tier_schema("76-100", "master")
                    }
                },
                "narrative_nodes": {
                    "type": "object",
                    "minProperties": 20,
                    "maxProperties": 35,
                    "patternProperties": {
                        "^node_[0-9]+$": self._create_node_schema()
                    }
                }
            }
        }
    
    def _create_tier_schema(self, range_str: str, level: str) -> Dict:
        """Create schema for reputation tier structure"""
        
        return {
            "type": "object",
            "required": ["range", "level", "unlocked_content", "voidmaker_reveals"],
            "properties": {
                "range": {"type": "string", "enum": [range_str]},
                "level": {"type": "string", "enum": [level]},
                "unlocked_content": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string"}
                },
                "voidmaker_reveals": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
    
    def _create_node_schema(self) -> Dict:
        """Create schema for individual narrative nodes"""
        
        return {
            "type": "object",
            "required": ["node_id", "title", "content", "dialogue", "choices", "mechanics"],
            "properties": {
                "node_id": {"type": "string"},
                "title": {
                    "type": "string",
                    "minLength": 5,
                    "maxLength": 100
                },
                "content": {
                    "type": "string",
                    "minLength": 100,
                    "maxLength": 2000
                },
                "dialogue": {
                    "type": "object",
                    "required": ["governor_voice", "personality_integration"],
                    "properties": {
                        "governor_voice": {
                            "type": "string",
                            "minLength": 50
                        },
                        "personality_integration": {
                            "type": "boolean"
                        }
                    }
                },
                "choices": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 4,
                    "items": {
                        "type": "object",
                        "required": ["choice_text", "next_node", "requirements"],
                        "properties": {
                            "choice_text": {"type": "string", "minLength": 10},
                            "next_node": {"type": "string"},
                            "requirements": {
                                "type": "object",
                                "properties": {
                                    "reputation_min": {"type": "integer"},
                                    "energy_cost": {"type": "integer"},
                                    "cooldown": {"type": "integer"}
                                }
                            }
                        }
                    }
                },
                "mechanics": {
                    "type": "object",
                    "required": ["energy_cost", "reputation_gain", "rewards"],
                    "properties": {
                        "energy_cost": {"type": "integer", "minimum": 0},
                        "reputation_gain": {"type": "integer"},
                        "rewards": {
                            "type": "object",
                            "properties": {
                                "tokens": {"type": "integer"},
                                "knowledge": {"type": "array"},
                                "achievements": {"type": "array"}
                            }
                        }
                    }
                }
            }
        }
    
    def validate_storyline_data(self, storyline_data: Dict) -> Tuple[bool, List[str]]:
        """Validate storyline data against schema"""
        
        errors = []
        
        try:
            validate(instance=storyline_data, schema=self.schema)
            
            # Additional quality validations
            quality_errors = self._validate_storyline_quality(storyline_data)
            errors.extend(quality_errors)
            
            is_valid = len(errors) == 0
            
            if is_valid:
                logging.info("✅ Storyline data validation passed")
            else:
                logging.warning(f"❌ Storyline validation failed: {len(errors)} errors")
                
            return is_valid, errors
            
        except ValidationError as e:
            error_msg = f"Schema validation failed: {e.message}"
            errors.append(error_msg)
            logging.error(f"❌ {error_msg}")
            return False, errors
    
    def _validate_storyline_quality(self, storyline_data: Dict) -> List[str]:
        """Additional quality validation beyond JSON schema"""
        
        errors = []
        
        # Check node connectivity
        nodes = storyline_data.get("narrative_nodes", {})
        node_ids = set(nodes.keys())
        
        # Validate node references
        for node_id, node_data in nodes.items():
            choices = node_data.get("choices", [])
            for choice in choices:
                next_node = choice.get("next_node")
                if next_node and next_node not in node_ids and next_node != "end":
                    errors.append(f"Node {node_id} references non-existent node: {next_node}")
        
        # Check reputation tier progression
        tiers = storyline_data.get("reputation_tiers", {})
        tier_content_counts = {}
        
        for tier_name, tier_data in tiers.items():
            content_count = len(tier_data.get("unlocked_content", []))
            tier_content_counts[tier_name] = content_count
        
        # Higher tiers should have more content
        expected_progression = ["tier_1", "tier_2", "tier_3", "tier_4"]
        for i in range(len(expected_progression) - 1):
            current_tier = expected_progression[i]
            next_tier = expected_progression[i + 1]
            
            if (current_tier in tier_content_counts and 
                next_tier in tier_content_counts and
                tier_content_counts[current_tier] >= tier_content_counts[next_tier]):
                errors.append(f"Tier progression issue: {current_tier} has same/more content than {next_tier}")
        
        return errors

def validate_storyline_file(file_path: Path) -> Tuple[bool, List[str]]:
    """Convenience function to validate a storyline file"""
    
    validator = StorylineOutputValidator()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            storyline_data = json.load(f)
        
        return validator.validate_storyline_data(storyline_data)
        
    except Exception as e:
        return False, [f"File loading error: {str(e)}"]

if __name__ == "__main__":
    # Test validation with a storyline file
    logging.basicConfig(level=logging.INFO)
    
    test_files = [
        Path("../storyline_output_v2/ABRIOND_enhanced_v2.json"),
        Path("../storyline_output/ABRIOND_storyline.json")
    ]
    
    for test_file in test_files:
        if test_file.exists():
            print(f"\n🧪 Testing: {test_file.name}")
            is_valid, errors = validate_storyline_file(test_file)
            
            if is_valid:
                print("✅ Storyline validation passed!")
            else:
                print(f"❌ Storyline validation failed:")
                for error in errors[:5]:  # Show first 5 errors
                    print(f"   - {error}")
            break
    else:
        print("❌ No test files found") 