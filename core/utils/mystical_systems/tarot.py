"""
Tarot System Utilities
Common functionality for tarot card operations
"""

import logging
from typing import List, Dict, Optional, Any, cast
from .base import MysticalSystem, MysticalEntity, MysticalAttribute, ValidationResult
from core.mystical_systems.tarot_system.data.tarot_cards_database import ALL_TAROT_CARDS
from core.mystical_systems.tarot_system.schemas.tarot_schemas import TarotCard, TarotSuit

logger = logging.getLogger(__name__)

class TarotSystem(MysticalSystem):
    """Tarot system implementation"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("tarot", config)
        self.cards_by_id: Dict[str, TarotCard] = {}
        self.cards_by_suit: Dict[TarotSuit, List[TarotCard]] = {}
        self._initialize_card_collections()
        
    def _initialize_card_collections(self) -> None:
        """Initialize card collections with proper type casting"""
        self.cards_by_id = {card.id: card for card in ALL_TAROT_CARDS}
        self.cards_by_suit = {}
        for card in ALL_TAROT_CARDS:
            if card.suit not in self.cards_by_suit:
                self.cards_by_suit[card.suit] = []
            self.cards_by_suit[card.suit].append(card)
    
    def get_card_by_id(self, card_id: str) -> Optional[TarotCard]:
        """Get a card by its ID"""
        return self.cards_by_id.get(card_id)
    
    def get_cards_by_suit(self, suit: TarotSuit) -> List[TarotCard]:
        """Get all cards of a specific suit"""
        return self.cards_by_suit.get(suit, [])
    
    def get_major_arcana(self) -> List[TarotCard]:
        """Get all major arcana cards"""
        return self.get_cards_by_suit(TarotSuit.MAJOR_ARCANA)
    
    def search_cards_by_keyword(self, keyword: str) -> List[TarotCard]:
        """Find cards containing keyword in upright meanings"""
        results: List[TarotCard] = []
        for card in ALL_TAROT_CARDS:
            if keyword.lower() in ' '.join(card.upright_keywords).lower():
                results.append(card)
        return results
        
    def validate_input(self, data: Any) -> ValidationResult:
        """Validate tarot-specific input data"""
        if not isinstance(data, dict):
            return ValidationResult(
                is_valid=False,
                data=data,
                errors=["Input must be a dictionary"]
            )
            
        required_fields = ['card_id']
        missing_fields = [f for f in required_fields if f not in data]
        
        if missing_fields:
            return ValidationResult(
                is_valid=False,
                data=data,
                errors=[f"Missing required fields: {', '.join(missing_fields)}"]
            )
            
        card = self.get_card_by_id(data['card_id'])
        if not card:
            return ValidationResult(
                is_valid=False,
                data=data,
                errors=[f"Invalid card ID: {data['card_id']}"]
            )
            
        return ValidationResult(is_valid=True, data=data)
        
    def format_output(self, result: Any) -> Any:
        """Format tarot-specific output data"""
        if isinstance(result, TarotCard):
            return {
                'id': result.id,
                'name': result.name,
                'suit': result.suit.value,
                'upright_keywords': result.upright_keywords,
                'reversed_keywords': result.reversed_keywords
            }
        return result
        
    def calculate_correspondences(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate tarot correspondences"""
        card = self.get_card_by_id(data.get('card_id', ''))
        if not card:
            return {}
            
        return {
            'element': card.element,
            'planet': card.planet,
            'zodiac': card.zodiac,
            'numerology': card.number
        } 