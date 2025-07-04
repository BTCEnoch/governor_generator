from typing import Dict, List
from engines.mystical_systems.tarot_system.schemas.tarot_schemas import TarotCard, CardPosition

class TarotCardRenderer:
    def __init__(self):
        self.card_art_path = "tarot_system/assets/card_images"
        self.card_backs_path = "tarot_system/assets/card_backs"
        
    def render_card_ascii(self, card: TarotCard, position: CardPosition) -> str:
        """Render a tarot card in ASCII art format"""
        
        if position == CardPosition.REVERSED:
            return self._render_reversed_card_ascii(card)
        
        # Upright card template
        card_art = f"""
    ┌─────────────────┐
    │  {card.name:<15} │
    │                 │
    │       {self._get_card_symbol(card):<3}       │
    │                 │
    │  {card.suit.value.title():<15} │
    │                 │
    │ {card.upright_keywords[0]:<15} │
    │ {card.upright_keywords[1] if len(card.upright_keywords) > 1 else '':<15} │
    └─────────────────┘
        """
        return card_art
    
    def _render_reversed_card_ascii(self, card: TarotCard) -> str:
        """Render a reversed tarot card"""
        card_art = f"""
    ┌─────────────────┐
    │ {card.reversed_keywords[0]:<15} │
    │ {card.reversed_keywords[1] if len(card.reversed_keywords) > 1 else '':<15} │
    │                 │
    │  {card.suit.value.title():<15} │
    │                 │
    │       {self._get_card_symbol(card):<3}       │
    │                 │
    │  {card.name:<15} │
    └─────────────────┘
    ⚠️  REVERSED  ⚠️
        """
        return card_art
    
    def _get_card_symbol(self, card: TarotCard) -> str:
        """Get symbolic representation of card"""
        symbol_map = {
            "major_arcana": "✨",
            "wands": "🔥",
            "cups": "💧", 
            "swords": "⚔️",
            "pentacles": "🪙"
        }
        return symbol_map.get(card.suit.value, "🎴")
    
    def render_spread_layout(self, cards: List[tuple], spread_type: str) -> str:
        """Render a complete tarot spread layout"""
        
        if spread_type == "three_card":
            return self._render_three_card_layout(cards)
        elif spread_type == "celtic_cross":
            return self._render_celtic_cross_layout(cards)
        
        return "Unknown spread type"
    
    def _render_three_card_layout(self, cards: List[tuple]) -> str:
        """Render three-card spread layout"""
        layout = f"""
    🌅 PAST          ⚡ PRESENT        🌟 FUTURE
    
    {cards[0][0].name}     {cards[1][0].name}     {cards[2][0].name}
    ({cards[0][1].value})   ({cards[1][1].value})   ({cards[2][1].value})
    
    {cards[0][0].upright_keywords[0]}  {cards[1][0].upright_keywords[0]}  {cards[2][0].upright_keywords[0]}
        """
        return layout

    def _render_celtic_cross_layout(self, cards: List[tuple]) -> str:
        """Render enhanced Celtic Cross spread layout"""
        if len(cards) < 10:
            return "Incomplete Celtic Cross - need 10 cards"
            
        position_names = [
            "Present Situation", "Challenge/Cross", "Distant Past/Foundation", "Recent Past",
            "Possible Outcome", "Immediate Future", "Your Approach", "External Influences", 
            "Inner Hopes/Fears", "Final Outcome"
        ]
        
        position_meanings = [
            "The heart of the matter", "What challenges or assists you", "Foundation of the situation",
            "Recent events affecting you", "What may come to pass", "What will happen next",
            "Your approach to the situation", "External factors at play",
            "Your inner state", "The final outcome"
        ]
        
        layout = """
    🔮 CELTIC CROSS SPREAD 🔮
    
    ✨ TRADITIONAL LAYOUT ✨
    
            [3] Recent Past
             |
    [7] - [1] + [0] - [4]
     Ext    Cross  Present  Future
             |
            [2] Foundation    [8] Hopes/Fears
                              [9] Final Outcome  
                              [5] Next Step
                              [6] Your Approach
    
    📋 DETAILED CARD INTERPRETATIONS:
        """
        
        for i, (card, position) in enumerate(cards):
            symbol = self._get_card_symbol(card)
            pos_indicator = "⬆️" if position.value == "upright" else "⬇️"
            
            layout += f"""
    
    {i+1}. {position_names[i]} {symbol} {pos_indicator}
       Card: {card.name} ({position.value.title()})
       Meaning: {position_meanings[i]}
       Keywords: {', '.join(card.upright_keywords[:3]) if position.value == "upright" else ', '.join(card.reversed_keywords[:3])}
       ────────────────────────────────────────────────────────────────────
    """
        
        layout += """
    
    🎯 READING SUMMARY:
    • Core Issue: Position 1 (Present) crossed by Position 2 (Challenge)
    • Timeline: Past (3,2) → Present (0,1) → Future (4,5) → Outcome (9)
    • Your Role: Approach (6) influenced by Inner State (8)
    • External Factors: Position 7 shows what's beyond your control
    • Final Guidance: Position 9 reveals the ultimate resolution
        """
        
        return layout

