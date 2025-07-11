"""
Governor Input Schema - Pydantic models for governor data validation
Validates the structure and required fields of governor JSON files
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, field_validator, ValidationInfo
import re
import logging

class QuestionAnswer(BaseModel):
    """Single question and answer pair"""
    question: str = Field(min_length=10, description="The question text")
    answer: str = Field(min_length=20, description="The answer text")

class QuestionBlock(BaseModel):
    """Block of related questions"""
    title: str = Field(description="Block title")
    questions: Dict[str, QuestionAnswer] = Field(
        description="Dictionary of question numbers to question/answer pairs"
    )

    @field_validator("questions")
    @classmethod
    def validate_question_count(cls, v: Dict[str, QuestionAnswer], info: ValidationInfo) -> Dict[str, QuestionAnswer]:
        """Validate the number of questions in a block"""
        expected = {
            "Identity & Origin": 32,
            "Cosmic Philosophy": 32,
            "Practical Mastery": 32,
            "Advanced Concepts": 31
        }
        title = info.data.get("title")
        if title in expected:
            count = len(v)
            expected_count = expected[title]
            if not (expected_count - 2 <= count <= expected_count + 2):
                raise ValueError(
                    f"Question count {count} outside expected range "
                    f"({expected_count-2}-{expected_count+2}) for {title}"
                )
        return v

class VoidmakerQuestion(BaseModel):
    """Voidmaker expansion question"""
    question: str = Field(min_length=10)
    answer: str = Field(min_length=20)

class VoidmakerSection(BaseModel):
    """Section of voidmaker questions"""
    questions: Dict[str, VoidmakerQuestion]

class KnowledgeBaseSelections(BaseModel):
    """Selected mystical traditions"""
    chosen_traditions: List[str] = Field(
        description="List of selected mystical traditions"
    )

    @field_validator("chosen_traditions")
    @classmethod
    def validate_traditions_count(cls, v: List[str], info: ValidationInfo) -> List[str]:
        if not (1 <= len(v) <= 10):
            raise ValueError("Must have between 1 and 10 chosen traditions")
        return v

class GovernorData(BaseModel):
    """Complete governor data model"""
    governor_name: str = Field(description="Governor name in all caps, 6-8 characters")
    blocks: Dict[str, QuestionBlock] = Field(
        description="Question blocks organized by topic"
    )
    voidmaker_expansion: Dict[str, VoidmakerSection] = Field(
        description="Voidmaker questions organized by philosophical domains"
    )
    knowledge_base_selections: KnowledgeBaseSelections = Field(
        description="Selected mystical traditions for this governor"
    )

    @field_validator("governor_name")
    @classmethod
    def validate_governor_name(cls, v: str, info: ValidationInfo) -> str:
        if not re.match(r"^[A-Z]{6,8}$", v):
            raise ValueError("Governor name must be 6-8 uppercase letters")
        return v

    @field_validator("blocks")
    @classmethod
    def validate_required_blocks(cls, v: Dict[str, QuestionBlock], info: ValidationInfo) -> Dict[str, QuestionBlock]:
        """Validate that all required blocks are present"""
        required_blocks = {
            "A_identity_origin",
            "B_cosmic_philosophy",
            "C_practical_mastery"
        }
        missing = required_blocks - set(v.keys())
        if missing:
            raise ValueError(f"Missing required blocks: {missing}")
        return v

    @field_validator("voidmaker_expansion")
    @classmethod
    def validate_voidmaker_questions(cls, v: Dict[str, VoidmakerSection], info: ValidationInfo) -> Dict[str, VoidmakerSection]:
        """Validate the total number of voidmaker questions"""
        if not v:
            raise ValueError("Must have at least one voidmaker section")
            
        total_questions = sum(
            len(section.questions) for section in v.values()
        )
        if not (35 <= total_questions <= 50):
            raise ValueError(
                f"Voidmaker question count {total_questions} "
                "outside expected range (35-50)"
            )
        return v

def validate_governor_file(file_path: Path) -> tuple[bool, List[str]]:
    """Validate a governor file against the schema"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = GovernorData.model_validate_json(f.read())
        return True, []
    except Exception as e:
        return False, [str(e)]

if __name__ == "__main__":
    # Test validation with a governor file
    logging.basicConfig(level=logging.INFO)
    
    test_file = Path("data/governors/ABRIOND.json")
    if test_file.exists():
        is_valid, errors = validate_governor_file(test_file)
        if is_valid:
            print("✅ Governor validation passed!")
        else:
            print("❌ Governor validation failed:")
            for error in errors:
                print(f"   - {error}")
    else:
        print("❌ Test file not found") 