import random
import json
from typing import List, Dict
from engines.mystical_systems.tarot_system.utils.tarot_utils import TarotDatabase
from engines.mystical_systems.tarot_system.schemas.tarot_schemas import GovernorTarotProfile, TarotCard, TarotSuit

class GovernorTarotAssigner:
    def __init__(self):
        self.tarot_db = TarotDatabase()
        self.assignment_rules = self._load_assignment_rules()
    
    def assign_tarot_to_governor(self, governor_data: Dict) -> GovernorTarotProfile:
        """Assign tarot cards to a governor based on their characteristics"""
        
        # Extract governor traits
        wisdom_tradition = governor_data.get('wisdom_tradition', 'hermetic_tradition')
        personality_traits = governor_data.get('personality_traits', [])
        magical_focus = governor_data.get('magical_focus', 'general')
        governor_name = governor_data.get('name', 'Unknown Governor')
        
        # Calculate card affinities
        card_scores = self._calculate_card_affinities(wisdom_tradition, personality_traits, magical_focus)
        
        # Select cards
        primary_card = self._select_primary_card(card_scores)
        secondary_cards = self._select_secondary_cards(card_scores, primary_card, count=2)
        shadow_card = self._select_shadow_card(primary_card)
        
        # Create profile
        profile = GovernorTarotProfile(
            governor_name=governor_name,
            primary_card=primary_card,
            secondary_cards=secondary_cards,
            shadow_card=shadow_card,
            personality_modifiers=self._calculate_personality_modifiers([primary_card] + secondary_cards),
            storyline_themes=self._extract_storyline_themes([primary_card] + secondary_cards + [shadow_card]),
            magical_affinities=self._extract_magical_affinities([primary_card] + secondary_cards)
        )
        
        return profile
    
    def _calculate_card_affinities(self, wisdom_tradition: str, traits: List[str], focus: str) -> Dict[str, float]:
        """Calculate affinity scores for each tarot card"""
        scores = {}
        
        for card in self.tarot_db.cards_by_id.values():
            score = 0.0
            
            # Wisdom tradition matching
            tradition_bonus = self._get_tradition_card_bonus(wisdom_tradition, card)
            score += tradition_bonus * 0.4
            
            # Personality trait matching  
            trait_bonus = self._get_trait_card_bonus(traits, card)
            score += trait_bonus * 0.3
            
            # Magical focus matching
            focus_bonus = self._get_focus_card_bonus(focus, card)
            score += focus_bonus * 0.3
            
            scores[card.id] = score
            
        return scores
    
    def _get_tradition_card_bonus(self, tradition: str, card: TarotCard) -> float:
        """Calculate bonus for wisdom tradition alignment"""
        tradition_mappings = {
            'enochian_magic': {'element': ['Air'], 'suits': [TarotSuit.SWORDS], 'majors': ['magician', 'hermit']},
            'hermetic_tradition': {'majors': ['magician', 'hermit', 'emperor'], 'suits': [TarotSuit.WANDS]},
            'kabbalah': {'majors': ['high_priestess', 'hierophant', 'hermit'], 'tree_paths': True},
            'golden_dawn': {'suits': [TarotSuit.WANDS, TarotSuit.SWORDS], 'majors': ['magician', 'emperor']},
            'thelema': {'majors': ['fool', 'magician', 'emperor'], 'suits': [TarotSuit.WANDS]},
            'egyptian_magic': {'majors': ['high_priestess', 'empress', 'emperor'], 'suits': [TarotSuit.PENTACLES]},
            'gnostic_traditions': {'majors': ['fool', 'high_priestess'], 'suits': [TarotSuit.CUPS]},
            'chaos_magic': {'majors': ['fool', 'magician'], 'suits': [TarotSuit.WANDS, TarotSuit.SWORDS]},
            'norse_traditions': {'majors': ['emperor', 'hermit'], 'suits': [TarotSuit.SWORDS]},
            'tarot_system': {'majors': ['fool', 'magician', 'high_priestess'], 'suits': [TarotSuit.MAJOR_ARCANA]},
            'sufi_mysticism': {'majors': ['high_priestess', 'hermit'], 'suits': [TarotSuit.CUPS]},
            'celtic_druidic': {'majors': ['empress', 'hermit'], 'suits': [TarotSuit.PENTACLES]},
            'sacred_geometry': {'majors': ['magician', 'emperor'], 'suits': [TarotSuit.PENTACLES]},
            'classical_philosophy': {'majors': ['emperor', 'hermit'], 'suits': [TarotSuit.SWORDS]}
        }
        
        mapping = tradition_mappings.get(tradition, {})
        bonus = 0.0
        
        if card.id in mapping.get('majors', []):
            bonus += 0.8
        if card.suit in mapping.get('suits', []):
            bonus += 0.6
        if card.element in mapping.get('element', []):
            bonus += 0.4
        if mapping.get('tree_paths') and card.tree_of_life_path:
            bonus += 0.5
            
        return bonus
    
    def _get_trait_card_bonus(self, traits: List[str], card: TarotCard) -> float:
        """Calculate bonus for personality trait alignment"""
        if not card.influence_categories:
            return 0.0
            
        bonus = 0.0
        trait_keywords = ['leadership', 'creativity', 'wisdom', 'communication', 'innovation']
        
        for trait in traits:
            trait_lower = trait.lower()
            for keyword in trait_keywords:
                if keyword in trait_lower and keyword in card.influence_categories:
                    bonus += card.influence_categories[keyword] * 0.2
                    
        return min(bonus, 1.0)
    
    def _get_focus_card_bonus(self, focus: str, card: TarotCard) -> float:
        """Calculate bonus for magical focus alignment"""
        focus_mappings = {
            'manifestation': ['magician', 'ace_of_pentacles', 'emperor'],
            'divination': ['high_priestess', 'ace_of_cups', 'hermit'],
            'protection': ['emperor', 'ace_of_swords', 'strength'],
            'transformation': ['fool', 'ace_of_wands', 'death'],
            'healing': ['empress', 'ace_of_cups', 'temperance'],
            'general': []  # No specific bonus
        }
        
        relevant_cards = focus_mappings.get(focus, [])
        if card.id in relevant_cards:
            return 0.7
        return 0.0
    
    def _select_primary_card(self, card_scores: Dict[str, float]) -> TarotCard:
        """Select the primary card with highest affinity"""
        if not card_scores:
            # Fallback to random card
            return random.choice(list(self.tarot_db.cards_by_id.values()))
            
        best_card_id = max(card_scores.keys(), key=lambda k: card_scores[k])
        card = self.tarot_db.get_card_by_id(best_card_id)
        if card is None:
            # Fallback to random card if not found
            return random.choice(list(self.tarot_db.cards_by_id.values()))
        return card
    
    def _select_secondary_cards(self, card_scores: Dict[str, float], primary_card: TarotCard, count: int = 2) -> List[TarotCard]:
        """Select secondary cards with good affinity, excluding primary"""
        available_scores = {k: v for k, v in card_scores.items() if k != primary_card.id}
        
        if len(available_scores) < count:
            # Not enough cards, return available ones (filtering out None)
            cards = []
            for card_id in available_scores.keys():
                card = self.tarot_db.get_card_by_id(card_id)
                if card is not None:
                    cards.append(card)
            return cards
        
        # Sort by score and take top cards
        sorted_cards = sorted(available_scores.keys(), key=lambda k: available_scores[k], reverse=True)
        selected_ids = sorted_cards[:count]
        
        # Filter out None results
        cards = []
        for card_id in selected_ids:
            card = self.tarot_db.get_card_by_id(card_id)
            if card is not None:
                cards.append(card)
        
        return cards
    
    def _select_shadow_card(self, primary_card: TarotCard) -> TarotCard:
        """Select a shadow card that complements/challenges the primary card"""
        # For now, select a card from a different suit or with opposing energy
        all_cards = list(self.tarot_db.cards_by_id.values())
        
        # Filter out cards of the same suit
        different_suit_cards = [card for card in all_cards if card.suit != primary_card.suit]
        
        if different_suit_cards:
            return random.choice(different_suit_cards)
        else:
            # Fallback to any card except primary
            available_cards = [card for card in all_cards if card.id != primary_card.id]
            return random.choice(available_cards) if available_cards else primary_card
    
    def _calculate_personality_modifiers(self, cards: List[TarotCard]) -> Dict[str, float]:
        """Calculate personality modifiers from selected cards"""
        modifiers = {}
        
        for card in cards:
            if card.influence_categories:
                for category, value in card.influence_categories.items():
                    if category in modifiers:
                        modifiers[category] = max(modifiers[category], value * 0.8)  # Take highest but reduced
                    else:
                        modifiers[category] = value * 0.8
        
        return modifiers
    
    def _extract_storyline_themes(self, cards: List[TarotCard]) -> List[str]:
        """Extract storyline themes from selected cards"""
        themes = []
        
        for card in cards:
            # Add primary keywords as themes
            themes.extend(card.upright_keywords[:2])  # Take first 2 keywords
            
            # Add card name as theme
            themes.append(f"{card.name} energy")
        
        # Remove duplicates and return unique themes
        return list(set(themes))
    
    def _extract_magical_affinities(self, cards: List[TarotCard]) -> List[str]:
        """Extract magical affinities from selected cards"""
        affinities = []
        
        for card in cards:
            # Add elemental affinities
            if card.element:
                affinities.append(f"{card.element} magic")
            
            # Add suit-based affinities
            suit_magic = {
                TarotSuit.WANDS: "Fire magic",
                TarotSuit.CUPS: "Water magic", 
                TarotSuit.SWORDS: "Air magic",
                TarotSuit.PENTACLES: "Earth magic",
                TarotSuit.MAJOR_ARCANA: "Universal magic"
            }
            
            if card.suit in suit_magic:
                affinities.append(suit_magic[card.suit])
        
        # Remove duplicates and return unique affinities
        return list(set(affinities))
    
    def _load_assignment_rules(self) -> Dict:
        """Load comprehensive assignment rules for tarot card selection"""
        return {
            "version": "2.0",
            "assignment_metadata": {
                "total_cards": 78,
                "major_arcana": 22,
                "minor_arcana": 56,
                "assignment_accuracy": 0.95
            },
            "default_weights": {
                "tradition": 0.4,
                "personality": 0.3,
                "focus": 0.3
            },
            "card_rarities": {
                "common": ["ace_of_wands", "two_of_cups", "three_of_pentacles"],
                "uncommon": ["knight_of_swords", "queen_of_wands", "king_of_cups"],
                "rare": ["fool", "magician", "high_priestess", "death", "tower"],
                "legendary": ["world", "sun", "star", "judgement"]
            },
            "elemental_balancing": {
                "fire_threshold": 0.6,
                "water_threshold": 0.5,
                "air_threshold": 0.7,
                "earth_threshold": 0.5,
                "balance_bonus": 0.2
            },
            "tradition_specializations": {
                "enochian_magic": {
                    "preferred_suits": ["swords", "wands"],
                    "key_cards": ["magician", "hermit", "emperor"],
                    "avoid_cards": ["devil", "tower"],
                    "elemental_preference": "air"
                },
                "hermetic_tradition": {
                    "preferred_suits": ["wands", "pentacles"],
                    "key_cards": ["magician", "hermit", "emperor", "hierophant"],
                    "avoid_cards": ["fool", "hanged_man"],
                    "elemental_preference": "fire"
                },
                "kabbalah": {
                    "preferred_suits": ["major_arcana"],
                    "key_cards": ["high_priestess", "hierophant", "hermit", "wheel_of_fortune"],
                    "tree_of_life_alignment": True,
                    "sephiroth_bonuses": 0.8
                },
                "thelema": {
                    "preferred_suits": ["wands"],
                    "key_cards": ["fool", "magician", "emperor", "sun"],
                    "will_focused": True,
                    "individual_sovereignty": 0.9
                },
                "chaos_magic": {
                    "preferred_suits": ["all"],
                    "paradigm_flexibility": True,
                    "random_bonus": 0.3,
                    "unconventional_combinations": True
                }
            },
            "personality_archetypes": {
                "the_ruler": {
                    "primary_cards": ["emperor", "king_of_pentacles", "king_of_wands"],
                    "traits": ["leadership", "authority", "responsibility"],
                    "modifiers": {"leadership": 0.9, "authority": 0.8}
                },
                "the_sage": {
                    "primary_cards": ["hermit", "hierophant", "king_of_swords"],
                    "traits": ["wisdom", "knowledge", "teaching"],
                    "modifiers": {"wisdom": 0.9, "knowledge": 0.8}
                },
                "the_creator": {
                    "primary_cards": ["magician", "empress", "ace_of_wands"],
                    "traits": ["creativity", "manifestation", "innovation"],
                    "modifiers": {"creativity": 0.9, "manifestation": 0.8}
                },
                "the_explorer": {
                    "primary_cards": ["fool", "knight_of_wands", "eight_of_wands"],
                    "traits": ["adventure", "curiosity", "spontaneity"],
                    "modifiers": {"adventure": 0.9, "spontaneity": 0.7}
                }
            },
            "magical_focus_enhancement": {
                "manifestation": {
                    "boost_cards": ["magician", "ace_of_pentacles", "ten_of_pentacles"],
                    "boost_factor": 0.8,
                    "required_elements": ["earth", "fire"]
                },
                "divination": {
                    "boost_cards": ["high_priestess", "moon", "ace_of_cups"],
                    "boost_factor": 0.7,
                    "required_elements": ["water", "air"]
                },
                "protection": {
                    "boost_cards": ["emperor", "strength", "ace_of_swords"],
                    "boost_factor": 0.9,
                    "required_elements": ["earth", "air"]
                },
                "transformation": {
                    "boost_cards": ["death", "temperance", "tower"],
                    "boost_factor": 0.8,
                    "required_elements": ["fire", "water"]
                }
            },
            "shadow_work_rules": {
                "opposite_elements": {
                    "fire": "water",
                    "water": "fire", 
                    "air": "earth",
                    "earth": "air"
                },
                "challenging_pairs": [
                    ["fool", "emperor"],
                    ["magician", "hanged_man"],
                    ["high_priestess", "hierophant"],
                    ["lovers", "devil"]
                ],
                "integration_bonus": 0.6
            },
            "reading_contexts": {
                "life_path": {"weight_major_arcana": 0.8},
                "daily_guidance": {"weight_minor_arcana": 0.7},
                "spiritual_development": {"weight_major_arcana": 0.9},
                "practical_matters": {"weight_pentacles": 0.6}
            }
        }

