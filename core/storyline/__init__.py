"""
Storyline Generation System

This package provides functionality for generating rich, interactive storylines
for Governor Angels, including:

- Governor data validation
- Storyline structure validation
- Narrative node generation
- Reputation tier management
- Game mechanics integration
- Batch processing with retry handling
"""

from .schemas import (
    # Governor Input Schema
    GovernorData,
    QuestionAnswer,
    QuestionBlock,
    VoidmakerQuestion,
    VoidmakerSection,
    KnowledgeBaseSelections,
    validate_governor_file,
    
    # Storyline Output Schema
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

from .core_loader import (
    KnowledgeBaseSelection,
    VoidmakerBlock,
    EnhancedGovernorProfile,
    CoreDataLoader
)

from .batch_retry_handler import (
    RetryStrategy,
    BatchMetadata,
    RetryStatistics,
    BatchRetryHandler
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    
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
    "validate_storyline_file",
    
    # Core Loader
    "KnowledgeBaseSelection",
    "VoidmakerBlock",
    "EnhancedGovernorProfile",
    "CoreDataLoader",
    
    # Batch Retry Handler
    "RetryStrategy",
    "BatchMetadata",
    "RetryStatistics",
    "BatchRetryHandler"
] 