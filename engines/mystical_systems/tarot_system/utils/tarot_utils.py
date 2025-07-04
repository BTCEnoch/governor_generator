from typing import List, Dict, Optional
from engines.mystical_systems.tarot_system.data.tarot_cards_database import ALL_TAROT_CARDS
from engines.mystical_systems.tarot_system.schemas.tarot_schemas import TarotCard, TarotSuit

class TarotDatabase:
    def __init__(self):
        self.cards_by_id = {card.id: card for card in ALL_TAROT_CARDS}
        self.cards_by_suit = self._group_by_suit()
        
    def _group_by_suit(self) -> Dict[TarotSuit, List[TarotCard]]:
        suits = {}
        for card in ALL_TAROT_CARDS:
            if card.suit not in suits:
                suits[card.suit] = []
            suits[card.suit].append(card)
        return suits
    
    def get_card_by_id(self, card_id: str) -> Optional[TarotCard]:
        return self.cards_by_id.get(card_id)
    
    def get_cards_by_suit(self, suit: TarotSuit) -> List[TarotCard]:
        return self.cards_by_suit.get(suit, [])
    
    def get_major_arcana(self) -> List[TarotCard]:
        return self.get_cards_by_suit(TarotSuit.MAJOR_ARCANA)
    
    def search_cards_by_keyword(self, keyword: str) -> List[TarotCard]:
        """Find cards containing keyword in upright meanings"""
        results = []
        for card in ALL_TAROT_CARDS:
            if keyword.lower() in ' '.join(card.upright_keywords).lower():
                results.append(card)
        return results

