"""Schema definitions for storyline generation"""

from .governor_input_schema import (
    GovernorData,
    QuestionAnswer,
    QuestionBlock,
    VoidmakerQuestion,
    VoidmakerSection,
    KnowledgeBaseSelections,
    validate_governor_file
)

from .storyline_output_schema import (
    StorylineData,
    CanonicalElements,
    StorylineMetadata,
    ReputationTier,
    ReputationTiers,
    Choice,
    ChoiceRequirements,
    Rewards,
    NodeMechanics,
    NodeDialogue,
    NarrativeNode,
    validate_storyline_file
)

__all__ = [
    # Governor Input Schema
    "GovernorData",
    "QuestionAnswer",
    "QuestionBlock",
    "VoidmakerQuestion",
    "VoidmakerSection",
    "KnowledgeBaseSelections",
    "validate_governor_file",
    
    # Storyline Output Schema
    "StorylineData",
    "CanonicalElements",
    "StorylineMetadata",
    "ReputationTier",
    "ReputationTiers",
    "Choice",
    "ChoiceRequirements",
    "Rewards",
    "NodeMechanics",
    "NodeDialogue",
    "NarrativeNode",
    "validate_storyline_file"
] 