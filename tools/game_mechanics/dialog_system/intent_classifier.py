"""
Intent Classification Engine
============================

This module implements a lightweight intent classification system that combines
token matching with semantic similarity for robust player input understanding.

Key Components:
- IntentClassifier: Main classification engine
- ClassificationResult: Result of intent classification
- FallbackHandler: Handles unmatched or ambiguous inputs
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
import logging

from .core_structures import IntentCategory
from .nlu_engine import TokenMatcher, MatchResult, EntityRecognizer
from .similarity_engine import SimpleEmbedding, SimilarityMatcher

@dataclass
class ClassificationResult:
    """Result of intent classification with confidence and metadata."""
    intent: IntentCategory
    confidence: float
    method: str  # How the classification was made
    matched_tokens: List[str]
    entities: Dict[str, List[str]]
    alternatives: List[Tuple[IntentCategory, float]]  # Alternative intents with confidence
    metadata: Dict[str, Any]

class IntentClassifier:
    """
    Main intent classification engine combining multiple approaches.
    
    This classifier uses both exact token matching and semantic similarity
    to provide robust intent recognition for player inputs.
    """
    
    def __init__(self):
        """Initialize the intent classifier."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize component systems
        self.token_matcher = TokenMatcher()
        self.embedding_system = SimpleEmbedding()
        self.similarity_matcher = SimilarityMatcher(self.embedding_system)
        self.entity_recognizer = EntityRecognizer()
        
        # Classification thresholds
        self.high_confidence_threshold = 0.8
        self.medium_confidence_threshold = 0.5
        self.low_confidence_threshold = 0.3
    
    def classify(self, text: str) -> ClassificationResult:
        """
        Classify player input text to determine intent.
        
        Args:
            text: Player input text
            
        Returns:
            ClassificationResult with intent and confidence
        """
        if not text or not text.strip():
            return self._create_unknown_result("Empty input")
        
        # Step 1: Try exact token matching first (fastest)
        token_matches = self.token_matcher.classify_intent(text)
        
        # Step 2: Extract entities
        entities = self.entity_recognizer.extract_entities(text)
        
        # Step 3: If we have high-confidence token matches, use them
        if token_matches and token_matches[0].confidence >= self.high_confidence_threshold:
            best_match = token_matches[0]
            alternatives = [(m.intent, m.confidence) for m in token_matches[1:3]]
            
            return ClassificationResult(
                intent=best_match.intent,
                confidence=best_match.confidence,
                method="token_matching",
                matched_tokens=best_match.matched_tokens,
                entities=entities,
                alternatives=alternatives,
                metadata=best_match.metadata
            )
        
        # Step 4: Try semantic similarity for medium confidence
        semantic_result = self._semantic_classification(text, entities)
        if semantic_result and semantic_result.confidence >= self.medium_confidence_threshold:
            return semantic_result
        
        # Step 5: Use best token match if above low threshold
        if token_matches and token_matches[0].confidence >= self.low_confidence_threshold:
            best_match = token_matches[0]
            alternatives = [(m.intent, m.confidence) for m in token_matches[1:3]]
            
            return ClassificationResult(
                intent=best_match.intent,
                confidence=best_match.confidence,
                method="token_matching_low_confidence",
                matched_tokens=best_match.matched_tokens,
                entities=entities,
                alternatives=alternatives,
                metadata=best_match.metadata
            )
        
        # Step 6: Fallback to unknown intent
        return self._create_unknown_result("No confident matches found", entities)
    
    def _semantic_classification(self, text: str, entities: Dict[str, List[str]]) -> Optional[ClassificationResult]:
        """
        Perform semantic classification using embeddings.
        
        Args:
            text: Input text
            entities: Already extracted entities
            
        Returns:
            ClassificationResult if confident match found
        """
        tokens = self.token_matcher.tokenize(text)
        if not tokens:
            return None
        
        # Try semantic matching against known patterns
        best_intent = None
        best_confidence = 0.0
        best_matched_tokens = []
        alternatives = []
        
        # Check each intent category's patterns
        for intent, patterns in self.token_matcher.intent_patterns.items():
            for pattern in patterns:
                # Use semantic similarity to match against pattern tokens
                required_similarity, required_matches = self.similarity_matcher.semantic_match_tokens(
                    tokens, pattern.required_tokens
                )
                
                optional_similarity, optional_matches = self.similarity_matcher.semantic_match_tokens(
                    tokens, pattern.optional_tokens
                )
                
                # Calculate combined confidence
                if required_similarity > 0:  # Must have some required token match
                    combined_confidence = (
                        required_similarity * 0.8 + 
                        optional_similarity * 0.2
                    ) * pattern.confidence_weight * 0.9  # Slight penalty for semantic vs exact
                    
                    if combined_confidence > best_confidence:
                        best_intent = intent
                        best_confidence = combined_confidence
                        best_matched_tokens = required_matches + optional_matches
                    elif combined_confidence > self.low_confidence_threshold:
                        alternatives.append((intent, combined_confidence))
        
        if best_intent and best_confidence >= self.medium_confidence_threshold:
            # Sort alternatives by confidence
            alternatives.sort(key=lambda x: x[1], reverse=True)
            
            return ClassificationResult(
                intent=best_intent,
                confidence=best_confidence,
                method="semantic_similarity",
                matched_tokens=best_matched_tokens,
                entities=entities,
                alternatives=alternatives[:3],  # Top 3 alternatives
                metadata={"semantic_match": True}
            )
        
        return None
    
    def _create_unknown_result(self, reason: str, entities: Optional[Dict[str, List[str]]] = None) -> ClassificationResult:
        """Create a result for unknown/unmatched input."""
        return ClassificationResult(
            intent=IntentCategory.UNKNOWN,
            confidence=0.0,
            method="fallback",
            matched_tokens=[],
            entities=entities or {},
            alternatives=[],
            metadata={"reason": reason}
        ) 