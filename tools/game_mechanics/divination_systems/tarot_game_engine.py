import random
from typing import List, Tuple, Optional
from datetime import datetime
from engines.mystical_systems.tarot_system.schemas.tarot_schemas import TarotCard, CardPosition, TarotReading
from engines.mystical_systems.tarot_system.utils.tarot_utils import TarotDatabase

class TarotGameEngine:
    def __init__(self):
        self.tarot_db = TarotDatabase()
        self.deck = list(self.tarot_db.cards_by_id.values())
        self.current_reading: Optional[TarotReading] = None
        
    def shuffle_deck(self) -> None:
        """Shuffle the 78-card deck"""
        random.shuffle(self.deck)
        print("🔀 Deck shuffled with mystical energy...")
    
    def draw_cards(self, count: int) -> List[Tuple[TarotCard, CardPosition]]:
        """Draw cards with random upright/reversed positions"""
        if len(self.deck) < count:
            self.reset_deck()
        
        drawn_cards = []
        for _ in range(count):
            card = self.deck.pop()
            # 80% chance upright, 20% chance reversed
            position = CardPosition.UPRIGHT if random.random() < 0.8 else CardPosition.REVERSED
            drawn_cards.append((card, position))
        
        return drawn_cards
    
    def reset_deck(self) -> None:
        """Reset and reshuffle the deck"""
        self.deck = list(self.tarot_db.cards_by_id.values())
        self.shuffle_deck()
    
    def create_three_card_reading(self, question: Optional[str] = None) -> TarotReading:
        """Generate a Past-Present-Future three-card reading"""
        cards = self.draw_cards(3)
        
        # Interpret the cards
        past_card, past_pos = cards[0]
        present_card, present_pos = cards[1] 
        future_card, future_pos = cards[2]
        
        interpretation = self._interpret_three_card_spread(cards, question)
        themes = self._extract_reading_themes(cards)
        advice = self._generate_advice(cards)
        
        reading = TarotReading(
            spread_type="three_card",
            cards_drawn=cards,
            interpretation=interpretation,
            themes=themes,
            advice=advice,
            timestamp=datetime.now().isoformat()
        )
        
        self.current_reading = reading
        return reading
    
    def create_celtic_cross_reading(self, question: Optional[str] = None) -> TarotReading:
        """Generate a 10-card Celtic Cross spread"""
        cards = self.draw_cards(10)
        
        # Celtic Cross positions:
        # 0: Present situation, 1: Challenge, 2: Distant past, 3: Recent past
        # 4: Possible outcome, 5: Immediate future, 6: Your approach
        # 7: External influences, 8: Hopes/fears, 9: Final outcome
        
        interpretation = self._interpret_celtic_cross_spread(cards, question)
        themes = self._extract_reading_themes(cards)
        advice = self._generate_advice(cards)
        
        reading = TarotReading(
            spread_type="celtic_cross",
            cards_drawn=cards,
            interpretation=interpretation,
            themes=themes,
            advice=advice,
            timestamp=datetime.now().isoformat()
        )
        
        self.current_reading = reading
        return reading
    
    def _interpret_three_card_spread(self, cards: List[Tuple[TarotCard, CardPosition]], question: Optional[str]) -> str:
        """Generate narrative interpretation for three-card spread"""
        past_card, past_pos = cards[0]
        present_card, present_pos = cards[1]
        future_card, future_pos = cards[2]
        
        past_meaning = past_card.upright_meaning if past_pos == CardPosition.UPRIGHT else past_card.reversed_meaning
        present_meaning = present_card.upright_meaning if present_pos == CardPosition.UPRIGHT else present_card.reversed_meaning
        future_meaning = future_card.upright_meaning if future_pos == CardPosition.UPRIGHT else future_card.reversed_meaning
        
        interpretation = f"""
        🔮 THREE-CARD READING INTERPRETATION
        
        {'Question: ' + question if question else 'General Life Reading'}
        
        🌅 PAST - {past_card.name} ({past_pos.value.title()}):
        {past_meaning}
        
        ⚡ PRESENT - {present_card.name} ({present_pos.value.title()}):
        {present_meaning}
        
        🌟 FUTURE - {future_card.name} ({future_pos.value.title()}):
        {future_meaning}
        
        🔗 OVERALL NARRATIVE:
        Your journey from {past_card.name} through {present_card.name} leads toward {future_card.name}. 
        The cards suggest a progression from {past_card.upright_keywords[0]} energy through current 
        {present_card.upright_keywords[0]} influences, culminating in {future_card.upright_keywords[0]} potential.
        """
        
        return interpretation.strip()

    def _interpret_celtic_cross_spread(self, cards: List[Tuple[TarotCard, CardPosition]], question: Optional[str]) -> str:
        """Generate narrative interpretation for Celtic Cross spread"""
        position_names = [
            "Present Situation", "Challenge", "Distant Past", "Recent Past",
            "Possible Outcome", "Immediate Future", "Your Approach", 
            "External Influences", "Hopes/Fears", "Final Outcome"
        ]
        
        interpretation = f"""
        🔮 CELTIC CROSS READING INTERPRETATION
        
        {'Question: ' + question if question else 'General Life Reading'}
        
        """
        
        for i, (card, position) in enumerate(cards):
            meaning = card.upright_meaning if position == CardPosition.UPRIGHT else card.reversed_meaning
            interpretation += f"""
        {i+1}. {position_names[i]} - {card.name} ({position.value.title()}):
        {meaning[:150]}...
        """
        
        interpretation += """
        
        🔗 OVERALL NARRATIVE:
        This comprehensive reading reveals the complex web of influences surrounding your situation.
        The past foundations lead through current challenges toward multiple possible futures.
        """
        
        return interpretation.strip()

    def _extract_reading_themes(self, cards: List[Tuple[TarotCard, CardPosition]]) -> List[str]:
        """Extract key themes from the reading"""
        themes = []
        
        for card, position in cards:
            if position == CardPosition.UPRIGHT:
                themes.extend(card.upright_keywords[:2])  # Take first 2 keywords
            else:
                themes.extend(card.reversed_keywords[:2])  # Take first 2 reversed keywords
        
        # Remove duplicates and return unique themes
        unique_themes = list(set(themes))
        return unique_themes[:6]  # Limit to 6 themes max

    def _generate_advice(self, cards: List[Tuple[TarotCard, CardPosition]]) -> str:
        """Generate advice based on the cards drawn"""
        advice_templates = [
            "Focus on embracing {theme} while remaining mindful of {challenge}.",
            "The cards suggest that {theme} will be key to navigating the current situation.",
            "Consider how {theme} and {challenge} can work together rather than in opposition.",
            "Trust in the process of {theme} as it unfolds in your life.",
            "Balance is needed between {theme} and {challenge} for optimal outcomes."
        ]
        
        themes = self._extract_reading_themes(cards)
        
        if len(themes) >= 2:
            theme = themes[0]
            challenge = themes[1]
            advice = random.choice(advice_templates).format(theme=theme, challenge=challenge)
        elif len(themes) >= 1:
            theme = themes[0]
            advice = f"The cards strongly emphasize {theme} as a guiding force in this situation."
        else:
            advice = "The cards suggest a time of reflection and inner wisdom. Trust your intuition."
        
        return advice

