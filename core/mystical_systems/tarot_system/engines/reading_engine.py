"""
Tarot Reading Engine

This module handles the generation and interpretation of tarot readings
using defined spreads and the tarot system.
"""

import random
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Mapping
from datetime import datetime
from pathlib import Path

from core.utils.common.file_ops import safe_json_read
from ..spreads.spread_definitions import (
    SpreadType,
    SpreadDefinition,
    SPREAD_DEFINITIONS
)

@dataclass
class CardInPosition:
    """A card placed in a specific position in a spread"""
    card_id: str
    card_name: str
    position_name: str
    position_meaning: str
    upright: bool
    element: str
    astrological: str
    interpretation: str
    governor_aspects: List[str]
    elemental_resonance: float = 0.0
    governor_resonance: float = 0.0

@dataclass
class TarotReading:
    """Complete tarot reading with all cards and interpretations"""
    id: str
    timestamp: datetime
    spread_type: SpreadType
    spread_name: str
    question: Optional[str]
    cards: List[CardInPosition]
    overall_theme: str
    elemental_balance: Dict[str, float]
    governor_influences: Dict[str, float]
    narrative_summary: str
    guidance_points: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

class ReadingEngine:
    """Engine for generating and interpreting tarot readings"""
    
    def __init__(self, tarot_system):
        self.tarot_system = tarot_system
        self.card_data = self._load_card_data()
    
    def _load_card_data(self) -> Dict[str, Any]:
        """Load card definitions from the tarot tradition data"""
        tradition_path = Path("data/knowledge/archives/governor_archives/tarot_tradition.json")
        tarot_data = safe_json_read(tradition_path)
        if not tarot_data:
            raise ValueError("Failed to load tarot tradition data")
        
        # Create a flat dictionary of all cards for easy lookup
        cards = {}
        for system in tarot_data["core_systems"]:
            for card in system.get("cards", []):
                cards[card["id"]] = card
        return cards
    
    def generate_reading(
        self,
        spread_type: SpreadType,
        question: Optional[str] = None,
        governor_data: Optional[Dict] = None,
        seed: Optional[str] = None
    ) -> TarotReading:
        """Generate a complete tarot reading"""
        # Get spread definition
        spread = SPREAD_DEFINITIONS[spread_type]
        
        # Generate unique reading ID using Bitcoin-derived randomness if available
        reading_id = self._generate_reading_id(seed)
        
        # Draw cards for each position
        cards = self._draw_cards_for_spread(spread, seed)
        
        # Calculate elemental balance
        elemental_balance = self._calculate_elemental_balance(cards, spread)
        
        # Calculate governor influences
        governor_influences = self._calculate_governor_influences(
            cards, spread, governor_data
        )
        
        # Generate narrative interpretation
        narrative = self._generate_narrative(
            cards, spread, question, governor_data
        )
        
        # Create guidance points
        guidance = self._generate_guidance_points(
            cards, spread, governor_data
        )
        
        # Build complete reading
        reading = TarotReading(
            id=reading_id,
            timestamp=datetime.now(),
            spread_type=spread_type,
            spread_name=spread.name,
            question=question,
            cards=cards,
            overall_theme=self._determine_overall_theme(cards, spread),
            elemental_balance=elemental_balance,
            governor_influences=governor_influences,
            narrative_summary=narrative,
            guidance_points=guidance,
            metadata={
                "governor_influenced": bool(governor_data),
                "bitcoin_derived": bool(seed),
                "spread_positions": len(spread.positions)
            }
        )
        
        return reading
    
    def _generate_reading_id(self, seed: Optional[str] = None) -> str:
        """Generate unique reading ID, using Bitcoin-derived randomness if available"""
        import uuid
        if seed:
            # Use seed for deterministic ID generation
            import hashlib
            hash_input = f"{seed}_{datetime.now().isoformat()}"
            reading_id = hashlib.sha256(hash_input.encode()).hexdigest()[:12]
            return f"reading_{reading_id}"
        return f"reading_{uuid.uuid4().hex[:12]}"
    
    def _draw_cards_for_spread(
        self,
        spread: SpreadDefinition,
        seed: Optional[str] = None
    ) -> List[CardInPosition]:
        """Draw cards for each position in the spread"""
        if seed:
            # Use seed for deterministic card selection
            random.seed(seed)
        
        # Get all available cards
        available_cards = list(self.card_data.keys())
        drawn_cards = []
        
        for position in spread.positions:
            # Select card
            card_id = random.choice(available_cards)
            available_cards.remove(card_id)  # Prevent duplicate draws
            card = self.card_data[card_id]
            
            # Determine if card is upright or reversed
            upright = random.random() > 0.5
            
            # Calculate resonances
            elemental_resonance = self._calculate_elemental_resonance(
                card["element"],
                position.element_influence,
                spread.elemental_influences
            )
            
            governor_resonance = self._calculate_governor_resonance(
                card.get("governor_associations", []),
                position.governor_aspect,
                spread.governor_resonance
            )
            
            # Generate position-specific interpretation
            interpretation = self._interpret_card_in_position(
                card, position, upright
            )
            
            drawn_cards.append(CardInPosition(
                card_id=card_id,
                card_name=card["name"],
                position_name=position.name,
                position_meaning=position.meaning,
                upright=upright,
                element=card["element"],
                astrological=card.get("astrological", ""),
                interpretation=interpretation,
                governor_aspects=card.get("governor_associations", []),
                elemental_resonance=elemental_resonance,
                governor_resonance=governor_resonance
            ))
        
        return drawn_cards
    
    def _calculate_elemental_resonance(
        self,
        card_element: str,
        position_element: Optional[str],
        spread_influences: Dict[str, float]
    ) -> float:
        """Calculate how well a card's element resonates with its position"""
        if not position_element:
            return 0.5  # Neutral resonance
        
        # Base resonance from direct match
        base_resonance = 1.0 if card_element == position_element else 0.3
        
        # Modify by spread's elemental influence
        influence = spread_influences.get(card_element, 0.2)
        
        return base_resonance * influence
    
    def _calculate_governor_resonance(
        self,
        card_governors: List[str],
        position_aspect: Optional[str],
        spread_resonance: Dict[str, float]
    ) -> float:
        """Calculate how well a card's governor aspects resonate with its position"""
        if not position_aspect or not card_governors:
            return 0.5  # Neutral resonance
        
        # Check for direct aspect matches
        aspect_matches = sum(
            1 for gov in card_governors
            if position_aspect.lower() in gov.lower()
        )
        
        # Base resonance from matches
        base_resonance = 0.3 + (0.7 * (aspect_matches / len(card_governors)))
        
        # Modify by spread's governor resonance
        influence = spread_resonance.get(
            position_aspect.split()[0],  # Use first word as key
            0.2
        )
        
        return base_resonance * influence
    
    def _interpret_card_in_position(
        self,
        card: Dict[str, Any],
        position: Any,
        upright: bool
    ) -> str:
        """Generate specific interpretation for a card in its position"""
        # Get base meaning
        if isinstance(card.get("meanings", {}), dict):
            meanings = card["meanings"]["upright" if upright else "reversed"]
            base_meaning = random.choice(meanings)
        else:
            base_meaning = (
                card.get("upright_meaning" if upright else "reversed_meaning", "")
            )
        
        # Combine with position meaning
        interpretation = (
            f"In the position of {position.name}, representing {position.meaning}, "
            f"the {card['name']} {'upright ' if upright else 'reversed '}"
            f"suggests {base_meaning}. "
        )
        
        # Add elemental insight
        if position.element_influence:
            interpretation += (
                f"The {card['element']} energy of the card "
                f"interacts with the {position.element_influence} influence "
                f"of this position, "
            )
            if card["element"] == position.element_influence:
                interpretation += "creating a powerful resonance. "
            else:
                interpretation += "creating an interesting dynamic. "
        
        # Add governor aspect if available
        if position.governor_aspect and card.get("governor_associations"):
            interpretation += (
                f"The governor aspects of {', '.join(card['governor_associations'])} "
                f"provide guidance through {position.governor_aspect}. "
            )
        
        return interpretation
    
    def _calculate_elemental_balance(
        self,
        cards: List[CardInPosition],
        spread: SpreadDefinition
    ) -> Dict[str, float]:
        """Calculate the overall elemental balance of the reading"""
        elements: Dict[str, float] = {
            "Fire": 0.0,
            "Water": 0.0,
            "Air": 0.0,
            "Earth": 0.0,
            "Spirit": 0.0
        }
        
        # Count card elements
        for card in cards:
            elements[card.element] = elements.get(card.element, 0.0) + 1.0
        
        # Normalize to percentages
        total = sum(elements.values())
        if total > 0:
            elements = {k: v/total for k, v in elements.items()}
        
        # Weight by spread's elemental influences
        for element, value in elements.items():
            spread_influence = spread.elemental_influences.get(element, 0.2)
            elements[element] = value * spread_influence
        
        return elements
    
    def _calculate_governor_influences(
        self,
        cards: List[CardInPosition],
        spread: SpreadDefinition,
        governor_data: Optional[Dict]
    ) -> Dict[str, float]:
        """Calculate the influence of different governor aspects"""
        influences = {}
        
        # Gather all governor aspects
        for card in cards:
            for aspect in card.governor_aspects:
                influences[aspect] = influences.get(aspect, 0) + 1
        
        # Normalize to percentages
        total = sum(influences.values())
        if total > 0:
            influences = {k: v/total for k, v in influences.items()}
        
        # Weight by spread's governor resonance
        for aspect, value in influences.items():
            resonance = spread.governor_resonance.get(
                aspect.split()[0],  # Use first word as key
                0.2
            )
            influences[aspect] = value * resonance
        
        # If governor data provided, adjust influences
        if governor_data:
            governor_name = governor_data.get("name", "")
            for aspect, value in influences.items():
                if governor_name.lower() in aspect.lower():
                    influences[aspect] *= 1.5  # Boost matching aspects
        
        return influences
    
    def _determine_overall_theme(
        self,
        cards: List[CardInPosition],
        spread: SpreadDefinition
    ) -> str:
        """Determine the overall theme of the reading"""
        # Analyze elemental balance
        elements = self._calculate_elemental_balance(cards, spread)
        dominant_element = max(elements.items(), key=lambda x: x[1])[0]
        
        # Look at first and last cards
        first_card = cards[0]
        last_card = cards[-1]
        
        # Generate theme based on analysis
        theme = f"A {dominant_element}-focused journey from "
        theme += f"{first_card.card_name} to {last_card.card_name}, "
        
        # Add spread-specific theme
        if spread.spread_type == SpreadType.GOVERNORS_GUIDANCE:
            theme += "guided by divine wisdom and governor influence"
        elif spread.spread_type == SpreadType.CELTIC_CROSS:
            theme += "revealing deep insights and potential transformations"
        else:
            theme += "showing the path of development and change"
        
        return theme
    
    def _generate_narrative(
        self,
        cards: List[CardInPosition],
        spread: SpreadDefinition,
        question: Optional[str],
        governor_data: Optional[Dict]
    ) -> str:
        """Generate a narrative summary of the reading"""
        narrative = []
        
        # Start with the question if provided
        if question:
            narrative.append(f"Regarding the question: {question}")
        
        # Add spread introduction
        narrative.append(
            f"This {spread.name} reading reveals a journey through "
            f"{len(cards)} aspects of the situation."
        )
        
        # Add governor context if available
        if governor_data:
            narrative.append(
                f"The reading is influenced by the governor {governor_data['name']}, "
                "bringing their unique wisdom and guidance."
            )
        
        # Summarize the story through the positions
        for card in cards:
            narrative.append(card.interpretation)
        
        # Add overall theme
        narrative.append(
            f"\nThe overall theme of this reading is: "
            f"{self._determine_overall_theme(cards, spread)}"
        )
        
        return " ".join(narrative)
    
    def _generate_guidance_points(
        self,
        cards: List[CardInPosition],
        spread: SpreadDefinition,
        governor_data: Optional[Dict]
    ) -> List[str]:
        """Generate specific guidance points from the reading"""
        guidance = []
        
        # Add card-specific guidance
        for card in cards:
            point = f"From {card.position_name}: "
            if card.upright:
                point += f"Embrace the energy of {card.card_name} "
            else:
                point += f"Be mindful of {card.card_name}'s challenges "
            point += f"as it relates to {card.position_meaning.lower()}"
            guidance.append(point)
        
        # Add elemental guidance
        elements = self._calculate_elemental_balance(cards, spread)
        dominant_element = max(elements.items(), key=lambda x: x[1])[0]
        guidance.append(
            f"Work with the dominant {dominant_element} energy "
            "to achieve your goals"
        )
        
        # Add governor-specific guidance if available
        if governor_data:
            influences = self._calculate_governor_influences(
                cards, spread, governor_data
            )
            top_influence = max(influences.items(), key=lambda x: x[1])[0]
            guidance.append(
                f"Seek guidance from the governor aspect of {top_influence} "
                "for additional insight and support"
            )
        
        return guidance 