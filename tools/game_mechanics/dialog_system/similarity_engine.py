"""
Embedding Similarity Engine
===========================

This module implements lightweight word embedding similarity for semantic
matching of player inputs. Uses simple pre-computed embeddings and cosine
similarity for efficient on-chain compatible processing.

Key Components:
- SimpleEmbedding: Basic word embedding representation
- SimilarityMatcher: Semantic similarity matching
- SemanticClassifier: Intent classification using embeddings
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple
import logging

from .core_structures import IntentCategory
from .nlu_engine import MatchResult

@dataclass
class WordEmbedding:
    """Simple word embedding representation."""
    word: str
    vector: List[float]
    
    def __post_init__(self):
        """Validate embedding after initialization."""
        if not self.word:
            raise ValueError("WordEmbedding must have a non-empty word")
        if not self.vector:
            raise ValueError("WordEmbedding must have a non-empty vector")

class SimpleEmbedding:
    """
    Simple word embedding system using pre-computed vectors.
    
    This provides basic semantic similarity without requiring
    large language models or external APIs.
    """
    
    def __init__(self):
        """Initialize the embedding system."""
        self.logger = logging.getLogger(__name__)
        self.embeddings: Dict[str, List[float]] = {}
        self.vector_size = 50  # Small vector size for efficiency
        
        # Initialize with basic mystical/dialog vocabulary
        self._initialize_basic_embeddings()
    
    def _initialize_basic_embeddings(self):
        """Initialize basic embeddings for common dialog terms."""
        # Greeting-related terms (similar vectors)
        greeting_base = [0.8, 0.2, 0.1, 0.0, 0.3] + [0.0] * 45
        self.embeddings["hello"] = greeting_base
        self.embeddings["hi"] = [x + 0.1 for x in greeting_base[:5]] + [0.0] * 45
        self.embeddings["greetings"] = [x + 0.2 for x in greeting_base[:5]] + [0.0] * 45
        self.embeddings["hail"] = [x + 0.15 for x in greeting_base[:5]] + [0.0] * 45
        
        # Question-related terms
        question_base = [0.1, 0.8, 0.3, 0.2, 0.1] + [0.0] * 45
        self.embeddings["what"] = question_base
        self.embeddings["how"] = [x + 0.1 for x in question_base[:5]] + [0.0] * 45
        self.embeddings["why"] = [x + 0.15 for x in question_base[:5]] + [0.0] * 45
        self.embeddings["where"] = [x + 0.12 for x in question_base[:5]] + [0.0] * 45
        
        # Mystical terms
        mystical_base = [0.2, 0.1, 0.8, 0.4, 0.6] + [0.0] * 45
        self.embeddings["wisdom"] = mystical_base
        self.embeddings["knowledge"] = [x + 0.1 for x in mystical_base[:5]] + [0.0] * 45
        self.embeddings["mystery"] = [x + 0.15 for x in mystical_base[:5]] + [0.0] * 45
        self.embeddings["secret"] = [x + 0.2 for x in mystical_base[:5]] + [0.0] * 45
        
        # Normalize all vectors
        for word in self.embeddings:
            self.embeddings[word] = self._normalize_vector(self.embeddings[word])
    
    def _normalize_vector(self, vector: List[float]) -> List[float]:
        """Normalize a vector to unit length."""
        magnitude = math.sqrt(sum(x * x for x in vector))
        if magnitude == 0:
            return vector
        return [x / magnitude for x in vector]
    
    def get_embedding(self, word: str) -> Optional[List[float]]:
        """Get embedding for a word."""
        return self.embeddings.get(word.lower())
    
    def add_embedding(self, word: str, vector: List[float]) -> None:
        """Add a new word embedding."""
        if len(vector) != self.vector_size:
            raise ValueError(f"Vector must be of size {self.vector_size}")
        self.embeddings[word.lower()] = self._normalize_vector(vector)
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        return max(0.0, min(1.0, dot_product))  # Clamp to [0, 1]
    
    def word_similarity(self, word1: str, word2: str) -> float:
        """Calculate similarity between two words."""
        emb1 = self.get_embedding(word1)
        emb2 = self.get_embedding(word2)
        
        if emb1 is None or emb2 is None:
            return 1.0 if word1.lower() == word2.lower() else 0.0
        
        return self.cosine_similarity(emb1, emb2)

class SimilarityMatcher:
    """
    Semantic similarity matcher for player inputs.
    
    Uses word embeddings to find semantic matches even when
    exact tokens don't match the patterns.
    """
    
    def __init__(self, embedding_system: SimpleEmbedding):
        """Initialize with an embedding system."""
        self.embedding_system = embedding_system
        self.logger = logging.getLogger(__name__)
        self.similarity_threshold = 0.6  # Minimum similarity for matches
    
    def semantic_match_tokens(self, input_tokens: List[str], pattern_tokens: List[str]) -> Tuple[float, List[str]]:
        """
        Find semantic matches between input and pattern tokens.
        
        Args:
            input_tokens: Tokens from player input
            pattern_tokens: Tokens from intent pattern
            
        Returns:
            Tuple of (similarity_score, matched_tokens)
        """
        if not input_tokens or not pattern_tokens:
            return 0.0, []
        
        matched_tokens = []
        total_similarity = 0.0
        
        for pattern_token in pattern_tokens:
            best_similarity = 0.0
            best_match = None
            
            for input_token in input_tokens:
                similarity = self.embedding_system.word_similarity(input_token, pattern_token)
                if similarity > best_similarity and similarity >= self.similarity_threshold:
                    best_similarity = similarity
                    best_match = input_token
            
            if best_match:
                matched_tokens.append(best_match)
                total_similarity += best_similarity
        
        # Average similarity across pattern tokens
        avg_similarity = total_similarity / len(pattern_tokens) if pattern_tokens else 0.0
        
        return avg_similarity, matched_tokens 