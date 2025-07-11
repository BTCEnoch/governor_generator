"""
Tarot Spread Definitions

This module defines the structure and meaning of various tarot spreads.
Each spread is defined with its positions and their meanings.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class SpreadType(Enum):
    """Types of available tarot spreads"""
    CELTIC_CROSS = "celtic_cross"
    THREE_CARD = "three_card"
    HORSESHOE = "horseshoe"
    RELATIONSHIP = "relationship"
    CAREER_PATH = "career_path"
    SPIRITUAL_JOURNEY = "spiritual_journey"
    GOVERNORS_GUIDANCE = "governors_guidance"  # Custom spread for governor insights

@dataclass
class CardPosition:
    """Defines a position in a tarot spread"""
    name: str
    meaning: str
    element_influence: Optional[str] = None
    governor_aspect: Optional[str] = None
    position_number: int = 0
    modifiers: Dict[str, float] = field(default_factory=dict)

@dataclass
class SpreadDefinition:
    """Defines a complete tarot spread structure"""
    spread_type: SpreadType
    name: str
    description: str
    positions: List[CardPosition]
    total_cards: int
    elemental_influences: Dict[str, float] = field(default_factory=dict)
    governor_resonance: Dict[str, float] = field(default_factory=dict)
    
    def validate(self) -> bool:
        """Validate spread definition"""
        return (
            len(self.positions) == self.total_cards and
            all(pos.position_number < self.total_cards for pos in self.positions)
        )

# Define standard spreads
THREE_CARD_SPREAD = SpreadDefinition(
    spread_type=SpreadType.THREE_CARD,
    name="Three Card Spread",
    description="A simple spread showing past, present, and future influences",
    total_cards=3,
    positions=[
        CardPosition(
            name="Past",
            meaning="Past influences affecting the current situation",
            position_number=0,
            element_influence="Air",
            governor_aspect="Historical Knowledge"
        ),
        CardPosition(
            name="Present",
            meaning="Current energies and immediate influences",
            position_number=1,
            element_influence="Fire",
            governor_aspect="Active Influence"
        ),
        CardPosition(
            name="Future",
            meaning="Potential outcomes and future developments",
            position_number=2,
            element_influence="Water",
            governor_aspect="Prophetic Vision"
        )
    ],
    elemental_influences={
        "Air": 0.33,
        "Fire": 0.33,
        "Water": 0.34
    },
    governor_resonance={
        "Historical": 0.3,
        "Present": 0.4,
        "Future": 0.3
    }
)

CELTIC_CROSS_SPREAD = SpreadDefinition(
    spread_type=SpreadType.CELTIC_CROSS,
    name="Celtic Cross",
    description="A comprehensive spread for deep insight into a situation",
    total_cards=10,
    positions=[
        CardPosition(
            name="Present",
            meaning="The current situation or question",
            position_number=0,
            element_influence="Fire",
            governor_aspect="Current State"
        ),
        CardPosition(
            name="Challenge",
            meaning="Immediate challenge or crossing influence",
            position_number=1,
            element_influence="Air",
            governor_aspect="Opposition"
        ),
        CardPosition(
            name="Foundation",
            meaning="Foundation or root of the situation",
            position_number=2,
            element_influence="Earth",
            governor_aspect="Base Energy"
        ),
        CardPosition(
            name="Recent Past",
            meaning="Recent past influences",
            position_number=3,
            element_influence="Water",
            governor_aspect="Memory"
        ),
        CardPosition(
            name="Potential",
            meaning="Highest potential or best outcome",
            position_number=4,
            element_influence="Spirit",
            governor_aspect="Aspiration"
        ),
        CardPosition(
            name="Near Future",
            meaning="Immediate future developments",
            position_number=5,
            element_influence="Air",
            governor_aspect="Coming Change"
        ),
        CardPosition(
            name="Self",
            meaning="Your attitude or approach",
            position_number=6,
            element_influence="Fire",
            governor_aspect="Self-Image"
        ),
        CardPosition(
            name="Environment",
            meaning="Environmental influences and others' attitudes",
            position_number=7,
            element_influence="Earth",
            governor_aspect="External Forces"
        ),
        CardPosition(
            name="Hopes/Fears",
            meaning="Hopes, fears, and expectations",
            position_number=8,
            element_influence="Water",
            governor_aspect="Emotional Core"
        ),
        CardPosition(
            name="Outcome",
            meaning="Final outcome or resolution",
            position_number=9,
            element_influence="Spirit",
            governor_aspect="Destiny"
        )
    ],
    elemental_influences={
        "Fire": 0.2,
        "Air": 0.2,
        "Water": 0.2,
        "Earth": 0.2,
        "Spirit": 0.2
    },
    governor_resonance={
        "Present": 0.15,
        "Challenge": 0.15,
        "Foundation": 0.1,
        "Past": 0.1,
        "Future": 0.2,
        "Environment": 0.15,
        "Outcome": 0.15
    }
)

GOVERNORS_GUIDANCE_SPREAD = SpreadDefinition(
    spread_type=SpreadType.GOVERNORS_GUIDANCE,
    name="Governor's Guidance",
    description="A specialized spread for receiving guidance from the Governor Angels",
    total_cards=7,
    positions=[
        CardPosition(
            name="Governor's Influence",
            meaning="The primary Governor Angel's current influence",
            position_number=0,
            element_influence="Spirit",
            governor_aspect="Primary Influence"
        ),
        CardPosition(
            name="Spiritual Challenge",
            meaning="The main spiritual challenge or lesson",
            position_number=1,
            element_influence="Fire",
            governor_aspect="Challenge"
        ),
        CardPosition(
            name="Divine Wisdom",
            meaning="Wisdom or knowledge being offered",
            position_number=2,
            element_influence="Air",
            governor_aspect="Teaching"
        ),
        CardPosition(
            name="Emotional Journey",
            meaning="The emotional or inner path to follow",
            position_number=3,
            element_influence="Water",
            governor_aspect="Inner Path"
        ),
        CardPosition(
            name="Physical Action",
            meaning="Practical steps or actions to take",
            position_number=4,
            element_influence="Earth",
            governor_aspect="Manifestation"
        ),
        CardPosition(
            name="Spiritual Allies",
            meaning="Other Governor Angels offering support",
            position_number=5,
            element_influence="Spirit",
            governor_aspect="Alliance"
        ),
        CardPosition(
            name="Ultimate Outcome",
            meaning="The highest spiritual outcome possible",
            position_number=6,
            element_influence="Spirit",
            governor_aspect="Destiny"
        )
    ],
    elemental_influences={
        "Spirit": 0.4,
        "Fire": 0.15,
        "Air": 0.15,
        "Water": 0.15,
        "Earth": 0.15
    },
    governor_resonance={
        "Primary": 0.25,
        "Challenge": 0.15,
        "Wisdom": 0.15,
        "Action": 0.15,
        "Allies": 0.15,
        "Outcome": 0.15
    }
)

# Dictionary of all available spreads
SPREAD_DEFINITIONS = {
    SpreadType.THREE_CARD: THREE_CARD_SPREAD,
    SpreadType.CELTIC_CROSS: CELTIC_CROSS_SPREAD,
    SpreadType.GOVERNORS_GUIDANCE: GOVERNORS_GUIDANCE_SPREAD
} 