"""
Questline Schemas
Data structures for questlines, events, and encounters
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Literal
from enum import Enum
import uuid
from datetime import datetime

class QuestlineType(Enum):
    """Types of questlines governors can create"""
    WISDOM_TRIAL = "wisdom_trial"
    ELEMENTAL_JOURNEY = "elemental_journey"
    MYSTERY_INVESTIGATION = "mystery_investigation"
    SPIRITUAL_ASCENSION = "spiritual_ascension"
    ARTIFACT_QUEST = "artifact_quest"
    GOVERNOR_ENCOUNTER = "governor_encounter"
    RITUAL_COMPLETION = "ritual_completion"
    KNOWLEDGE_SEEKING = "knowledge_seeking"

class DifficultyLevel(Enum):
    """Difficulty levels for questlines and encounters"""
    NOVICE = "novice"
    APPRENTICE = "apprentice"
    ADEPT = "adept"
    MASTER = "master"
    GRANDMASTER = "grandmaster"

class EncounterType(Enum):
    """Types of encounters within questlines"""
    RIDDLE = "riddle"
    TRIAL = "trial"
    DIALOGUE = "dialogue"
    CHOICE = "choice"
    REVELATION = "revelation"
    CHALLENGE = "challenge"
    TEACHING = "teaching"
    TRANSFORMATION = "transformation"

@dataclass
class QuestlineReward:
    """Rewards for completing questlines"""
    type: Literal["wisdom", "artifact", "power", "knowledge", "token"]
    name: str
    description: str
    value: int
    rarity: Literal["common", "uncommon", "rare", "legendary", "mythic"]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EncounterChoice:
    """A choice available in an encounter"""
    id: str
    text: str
    consequence: str
    leads_to: Optional[str] = None  # Next encounter ID
    wisdom_gained: int = 0
    artifact_gained: Optional[str] = None
    governor_reaction: Optional[str] = None

@dataclass
class Encounter:
    """Individual encounter within a questline"""
    id: str
    type: EncounterType
    title: str
    description: str
    governor_dialogue: str
    choices: List[EncounterChoice] = field(default_factory=list)
    requirements: Dict[str, Any] = field(default_factory=dict)
    rewards: List[QuestlineReward] = field(default_factory=list)
    difficulty: DifficultyLevel = DifficultyLevel.NOVICE
    estimated_time: int = 5  # minutes
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class QuestlineProgress:
    """Tracks a user's progress through a questline"""
    questline_id: str
    user_id: str
    current_encounter: str
    encounters_completed: List[str] = field(default_factory=list)
    choices_made: Dict[str, str] = field(default_factory=dict)
    rewards_earned: List[QuestlineReward] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    status: Literal["in_progress", "completed", "abandoned"] = "in_progress"

@dataclass
class Questline:
    """Complete questline created by a governor"""
    id: str
    creator_governor: str  # Governor name who created this
    title: str
    description: str
    type: QuestlineType
    difficulty: DifficultyLevel
    estimated_duration: int  # minutes
    
    # Story structure
    encounters: List[Encounter] = field(default_factory=list)
    encounter_flow: Dict[str, str] = field(default_factory=dict)  # encounter_id -> next_encounter_id
    
    # Rewards and requirements
    completion_rewards: List[QuestlineReward] = field(default_factory=list)
    prerequisites: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    wisdom_themes: List[str] = field(default_factory=list)
    elemental_alignment: Optional[str] = None
    
    # Statistics
    completion_count: int = 0
    average_rating: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Generate ID if not provided"""
        if not self.id:
            self.id = str(uuid.uuid4())

@dataclass
class QuestlineTemplate:
    """Template for generating questlines"""
    type: QuestlineType
    title_patterns: List[str]
    description_patterns: List[str]
    encounter_templates: List[Dict[str, Any]]
    reward_templates: List[Dict[str, Any]]
    wisdom_themes: List[str]
    difficulty_scaling: Dict[str, Any]
    estimated_encounters: int = 5 