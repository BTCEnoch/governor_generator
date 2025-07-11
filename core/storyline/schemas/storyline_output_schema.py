"""
Storyline Output Schema - Pydantic models for rich storyline data validation
Validates the structure and quality of generated storyline JSON files
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, field_validator, ValidationInfo, model_validator
import re
import logging
from datetime import datetime

class CanonicalElements(BaseModel):
    """Canonical elements used in the storyline"""
    aethyrs: List[str] = Field(min_length=1, description="List of aethyrs used")
    watchtowers: List[str] = Field(min_length=1, description="List of watchtowers used")
    elements: List[str] = Field(min_length=1, description="List of elements used")

class StorylineMetadata(BaseModel):
    """Metadata about the storyline generation"""
    version: str = Field(description="Version of the storyline generator")
    generation_timestamp: datetime = Field(description="When the storyline was generated")
    total_nodes: int = Field(ge=20, le=35, description="Total number of narrative nodes")
    canonical_elements: CanonicalElements = Field(description="Canonical elements used")

class ReputationTier(BaseModel):
    """Single reputation tier definition"""
    range: str = Field(description="Reputation range for this tier")
    level: str = Field(description="Level name for this tier")
    unlocked_content: List[str] = Field(min_length=1, description="Content unlocked at this tier")
    voidmaker_reveals: List[str] = Field(description="Voidmaker content revealed at this tier")

    @field_validator("range")
    @classmethod
    def validate_range(cls, v: str, info: ValidationInfo) -> str:
        ranges = {
            "tier_1": "0-25",
            "tier_2": "26-50",
            "tier_3": "51-75",
            "tier_4": "76-100"
        }
        field_name = info.field_name
        if field_name in ranges and v != ranges[field_name]:
            raise ValueError(f"Invalid range for {field_name}: {v}")
        return v

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str, info: ValidationInfo) -> str:
        levels = {
            "tier_1": "novice",
            "tier_2": "apprentice",
            "tier_3": "adept",
            "tier_4": "master"
        }
        field_name = info.field_name
        if field_name in levels and v != levels[field_name]:
            raise ValueError(f"Invalid level for {field_name}: {v}")
        return v

class ReputationTiers(BaseModel):
    """All reputation tiers"""
    tier_1: ReputationTier
    tier_2: ReputationTier
    tier_3: ReputationTier
    tier_4: ReputationTier

    @model_validator(mode="after")
    def validate_tier_progression(self) -> "ReputationTiers":
        """Validate that higher tiers have more content"""
        tiers = [self.tier_1, self.tier_2, self.tier_3, self.tier_4]
        for i in range(len(tiers) - 1):
            current = len(tiers[i].unlocked_content)
            next_tier = len(tiers[i + 1].unlocked_content)
            if current >= next_tier:
                raise ValueError(
                    f"Tier {i+1} has same/more content ({current}) "
                    f"than tier {i+2} ({next_tier})"
                )
        return self

class ChoiceRequirements(BaseModel):
    """Requirements to select a choice"""
    reputation_min: Optional[int] = Field(default=None, description="Minimum reputation required")
    energy_cost: Optional[int] = Field(default=None, description="Energy cost to select this choice")
    cooldown: Optional[int] = Field(default=None, description="Cooldown period in minutes")

class Choice(BaseModel):
    """Single choice in a narrative node"""
    choice_text: str = Field(min_length=10, description="Text of the choice")
    next_node: str = Field(description="ID of the next node or 'end'")
    requirements: ChoiceRequirements = Field(description="Requirements for this choice")

class Rewards(BaseModel):
    """Rewards for completing a node"""
    tokens: Optional[int] = Field(default=None, description="Token reward amount")
    knowledge: Optional[List[str]] = Field(default=None, description="Knowledge rewards")
    achievements: Optional[List[str]] = Field(default=None, description="Achievement rewards")

class NodeMechanics(BaseModel):
    """Game mechanics for a node"""
    energy_cost: int = Field(ge=0, description="Energy cost to complete node")
    reputation_gain: int = Field(description="Reputation gained from node")
    rewards: Rewards = Field(description="Rewards for completing node")

class NodeDialogue(BaseModel):
    """Dialogue components of a node"""
    governor_voice: str = Field(min_length=50, description="Governor's dialogue")
    personality_integration: bool = Field(description="Whether personality is integrated")

class NarrativeNode(BaseModel):
    """Single narrative node in the storyline"""
    node_id: str = Field(description="Unique identifier for the node")
    title: str = Field(min_length=5, max_length=100, description="Node title")
    content: str = Field(min_length=100, max_length=2000, description="Node content")
    dialogue: NodeDialogue = Field(description="Node dialogue components")
    choices: List[Choice] = Field(min_length=1, max_length=4, description="Available choices")
    mechanics: NodeMechanics = Field(description="Node game mechanics")

class StorylineData(BaseModel):
    """Complete storyline data model"""
    governor_name: str = Field(description="Governor name in all caps, 6-8 characters")
    storyline_metadata: StorylineMetadata = Field(description="Storyline metadata")
    reputation_tiers: ReputationTiers = Field(description="Reputation tier definitions")
    narrative_nodes: Dict[str, NarrativeNode] = Field(
        min_length=20,
        max_length=35,
        description="Map of node IDs to narrative nodes"
    )

    @field_validator("governor_name")
    @classmethod
    def validate_governor_name(cls, v: str, info: ValidationInfo) -> str:
        if not re.match(r"^[A-Z]{6,8}$", v):
            raise ValueError("Governor name must be 6-8 uppercase letters")
        return v

    @field_validator("narrative_nodes")
    @classmethod
    def validate_node_references(cls, v: Dict[str, NarrativeNode], info: ValidationInfo) -> Dict[str, NarrativeNode]:
        """Validate that all node references exist"""
        node_ids = set(v.keys())
        for node_id, node in v.items():
            for choice in node.choices:
                next_node = choice.next_node
                if next_node != "end" and next_node not in node_ids:
                    raise ValueError(
                        f"Node {node_id} references non-existent node: {next_node}"
                    )
        return v

def validate_storyline_file(file_path: Path) -> tuple[bool, List[str]]:
    """Validate a storyline file against the schema"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = StorylineData.model_validate_json(f.read())
        return True, []
    except Exception as e:
        return False, [str(e)]

if __name__ == "__main__":
    # Test validation with a storyline file
    logging.basicConfig(level=logging.INFO)
    
    test_file = Path("data/storylines/ABRIOND_storyline.json")
    if test_file.exists():
        is_valid, errors = validate_storyline_file(test_file)
        if is_valid:
            print("✅ Storyline validation passed!")
        else:
            print("❌ Storyline validation failed:")
            for error in errors:
                print(f"   - {error}")
    else:
        print("❌ Test file not found") 