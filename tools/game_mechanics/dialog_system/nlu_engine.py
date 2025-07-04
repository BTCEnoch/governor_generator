"""
Natural Language Understanding Engine
====================================

This module implements lightweight NLU components for processing player inputs
in the dialog system. It uses token matching, regex patterns, and simple
classification to understand player intents without requiring large models.

Key Components:
- TokenMatcher: Simple token-based pattern matching
- RegexClassifier: Regex-based intent classification
- IntentExtractor: Extracts intents from player input
- EntityRecognizer: Recognizes named entities and game objects
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum
import logging

from .core_structures import IntentCategory, InteractionType

@dataclass
class MatchResult:
    """Result of pattern matching on player input."""
    intent: IntentCategory
    confidence: float
    matched_tokens: List[str]
    extracted_entities: Dict[str, Any]
    metadata: Dict[str, Any]

class PatternType(Enum):
    """Types of patterns used for matching."""
    EXACT_MATCH = "exact_match"
    TOKEN_MATCH = "token_match"
    REGEX_MATCH = "regex_match"
    FUZZY_MATCH = "fuzzy_match"

@dataclass
class IntentPattern:
    """Pattern definition for intent recognition."""
    intent: IntentCategory
    pattern_type: PatternType
    pattern: str
    required_tokens: List[str]
    optional_tokens: List[str]
    confidence_weight: float = 1.0
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class TokenMatcher:
    """
    Simple token-based pattern matcher for player inputs.
    
    This component uses predefined token patterns to quickly identify
    common player intents without requiring complex NLP models.
    """
    
    def __init__(self):
        """Initialize the token matcher."""
        self.logger = logging.getLogger(__name__)
        self.intent_patterns: Dict[IntentCategory, List[IntentPattern]] = {}
        self.stopwords: Set[str] = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'were', 'will', 'with', 'i', 'you', 'me', 'my', 'your'
        }
        
        # Initialize default patterns
        self._initialize_default_patterns()
    
    def _initialize_default_patterns(self):
        """Initialize default intent patterns."""
        # Formal greeting patterns
        self.add_pattern(IntentPattern(
            intent=IntentCategory.FORMAL_GREETING,
            pattern_type=PatternType.TOKEN_MATCH,
            pattern="formal_greeting",
            required_tokens=["greetings", "hail", "salutations"],
            optional_tokens=["governor", "master", "wise", "honored"],
            confidence_weight=0.9
        ))
        
        # Casual greeting patterns
        self.add_pattern(IntentPattern(
            intent=IntentCategory.CASUAL_GREETING,
            pattern_type=PatternType.TOKEN_MATCH,
            pattern="casual_greeting",
            required_tokens=["hello", "hi", "hey"],
            optional_tokens=["there", "friend"],
            confidence_weight=0.8
        ))
        
        # Question patterns
        self.add_pattern(IntentPattern(
            intent=IntentCategory.QUESTION,
            pattern_type=PatternType.TOKEN_MATCH,
            pattern="question",
            required_tokens=["what", "how", "why", "when", "where", "who"],
            optional_tokens=["is", "are", "do", "does", "can", "will"],
            confidence_weight=0.8
        ))
        
        # Riddle answer patterns
        self.add_pattern(IntentPattern(
            intent=IntentCategory.RIDDLE_ANSWER,
            pattern_type=PatternType.TOKEN_MATCH,
            pattern="riddle_answer",
            required_tokens=["answer", "solution", "riddle"],
            optional_tokens=["is", "the", "my"],
            confidence_weight=0.9
        ))
        
        # Praise patterns
        self.add_pattern(IntentPattern(
            intent=IntentCategory.PRAISE,
            pattern_type=PatternType.TOKEN_MATCH,
            pattern="praise",
            required_tokens=["wise", "brilliant", "excellent", "wonderful"],
            optional_tokens=["very", "truly", "indeed"],
            confidence_weight=0.8
        ))
        
        # Offering patterns
        self.add_pattern(IntentPattern(
            intent=IntentCategory.OFFERING,
            pattern_type=PatternType.TOKEN_MATCH,
            pattern="offering",
            required_tokens=["offer", "give", "present", "tribute"],
            optional_tokens=["you", "this", "my"],
            confidence_weight=0.8
        ))
    
    def add_pattern(self, pattern: IntentPattern):
        """Add a new intent pattern."""
        if pattern.intent not in self.intent_patterns:
            self.intent_patterns[pattern.intent] = []
        self.intent_patterns[pattern.intent].append(pattern)
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize input text into normalized tokens.
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List of normalized tokens
        """
        # Convert to lowercase and split on whitespace and punctuation
        tokens = re.findall(r'\b\w+\b', text.lower())
        
        # Remove stopwords
        filtered_tokens = [token for token in tokens if token not in self.stopwords]
        
        return filtered_tokens
    
    def match_pattern(self, tokens: List[str], pattern: IntentPattern) -> Optional[MatchResult]:
        """
        Match tokens against a specific pattern.
        
        Args:
            tokens: List of tokens to match
            pattern: Pattern to match against
            
        Returns:
            MatchResult if pattern matches, None otherwise
        """
        if pattern.pattern_type == PatternType.TOKEN_MATCH:
            return self._match_token_pattern(tokens, pattern)
        elif pattern.pattern_type == PatternType.REGEX_MATCH:
            return self._match_regex_pattern(tokens, pattern)
        elif pattern.pattern_type == PatternType.EXACT_MATCH:
            return self._match_exact_pattern(tokens, pattern)
        else:
            return None
    
    def _match_token_pattern(self, tokens: List[str], pattern: IntentPattern) -> Optional[MatchResult]:
        """Match tokens against a token-based pattern."""
        token_set = set(tokens)
        
        # Check if any required tokens are present
        required_matches = [token for token in pattern.required_tokens if token in token_set]
        if not required_matches:
            return None
        
        # Count optional token matches
        optional_matches = [token for token in pattern.optional_tokens if token in token_set]
        
        # Calculate confidence based on matches
        required_ratio = len(required_matches) / len(pattern.required_tokens) if pattern.required_tokens else 1.0
        optional_ratio = len(optional_matches) / len(pattern.optional_tokens) if pattern.optional_tokens else 0.0
        
        confidence = (required_ratio * 0.8 + optional_ratio * 0.2) * pattern.confidence_weight
        
        # Only return match if confidence is above threshold
        if confidence < 0.3:
            return None
        
        return MatchResult(
            intent=pattern.intent,
            confidence=confidence,
            matched_tokens=required_matches + optional_matches,
            extracted_entities={},
            metadata={"pattern_type": pattern.pattern_type.value}
        )
    
    def _match_regex_pattern(self, tokens: List[str], pattern: IntentPattern) -> Optional[MatchResult]:
        """Match tokens against a regex pattern."""
        text = " ".join(tokens)
        match = re.search(pattern.pattern, text, re.IGNORECASE)
        
        if match:
            confidence = pattern.confidence_weight
            matched_tokens = tokens  # For simplicity, include all tokens
            
            return MatchResult(
                intent=pattern.intent,
                confidence=confidence,
                matched_tokens=matched_tokens,
                extracted_entities={},
                metadata={"pattern_type": pattern.pattern_type.value, "regex_match": match.group()}
            )
        
        return None
    
    def _match_exact_pattern(self, tokens: List[str], pattern: IntentPattern) -> Optional[MatchResult]:
        """Match tokens against an exact pattern."""
        text = " ".join(tokens)
        pattern_tokens = pattern.pattern.lower().split()
        
        if tokens == pattern_tokens:
            return MatchResult(
                intent=pattern.intent,
                confidence=pattern.confidence_weight,
                matched_tokens=tokens,
                extracted_entities={},
                metadata={"pattern_type": pattern.pattern_type.value}
            )
        
        return None
    
    def classify_intent(self, text: str) -> List[MatchResult]:
        """
        Classify the intent of input text.
        
        Args:
            text: Input text to classify
            
        Returns:
            List of MatchResult objects sorted by confidence
        """
        tokens = self.tokenize(text)
        if not tokens:
            return []
        
        matches = []
        
        # Try to match against all patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = self.match_pattern(tokens, pattern)
                if match:
                    matches.append(match)
        
        # Sort by confidence (highest first)
        matches.sort(key=lambda x: x.confidence, reverse=True)
        
        return matches
    
    def get_best_intent(self, text: str) -> Optional[IntentCategory]:
        """
        Get the best matching intent for input text.
        
        Args:
            text: Input text to classify
            
        Returns:
            Best matching intent or None if no match
        """
        matches = self.classify_intent(text)
        return matches[0].intent if matches else None

class EntityRecognizer:
    """
    Recognizes named entities and game objects in player input.
    
    This component identifies governor names, mystical terms, items,
    and other game-specific entities to enhance dialog understanding.
    """
    
    def __init__(self):
        """Initialize the entity recognizer."""
        self.logger = logging.getLogger(__name__)
        
        # Entity patterns for different types
        self.entity_patterns = {
            "governor_names": [
                r"\b(occodon|pascomb|valgars|doagnis|pacasna|dialoia|samapha)\b",
                r"\b(virooli|andispi|thotanp|axxiarg|pothnir|lazdixi|nocamal)\b",
                r"\b(tiarpax|saxtomp|vauaamp|zirzird|opmacas|genadol|aspiaon)\b"
            ],
            "mystical_terms": [
                r"\b(aethyr|enochian|sigil|pentagram|hexagram|invocation)\b",
                r"\b(scrying|divination|oracle|prophecy|vision|revelation)\b",
                r"\b(ritual|ceremony|rite|sacrament|offering|tribute)\b"
            ],
            "items": [
                r"\b(crystal|wand|chalice|pentacle|sword|dagger)\b",
                r"\b(scroll|tome|grimoire|tablet|stone|ring)\b",
                r"\b(incense|candle|oil|herb|powder|elixir)\b"
            ]
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities from input text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary mapping entity types to found entities
        """
        entities = {}
        text_lower = text.lower()
        
        for entity_type, patterns in self.entity_patterns.items():
            found_entities = []
            
            for pattern in patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                found_entities.extend(matches)
            
            if found_entities:
                entities[entity_type] = list(set(found_entities))  # Remove duplicates
        
        return entities 