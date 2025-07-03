#!/usr/bin/env python3
"""
Semantic Knowledge Integrator
============================

Integrates the Lighthouse Knowledge Engine with the storyline engine
to provide semantic knowledge retrieval and vector search capabilities.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

# Add knowledge_base to path for imports
sys.path.append(str(Path(__file__).parent.parent / "knowledge_base"))

try:
    # Try direct import from knowledge_base package
    sys.path.append(str(Path(__file__).parent.parent))
    from knowledge_base.traditions.unified_knowledge_retriever import UnifiedKnowledgeRetriever
    from knowledge_base.retrievers.focused_mystical_retriever import FocusedMysticalRetriever
except ImportError as e:
    # Fallback if imports fail
    UnifiedKnowledgeRetriever = None
    FocusedMysticalRetriever = None

logger = logging.getLogger(__name__)


@dataclass
class SemanticKnowledgeMatch:
    """Represents a semantic knowledge match"""
    tradition: str
    concept: str
    relevance_score: float
    wisdom_element: str
    source: str
    context: Dict[str, Any]


@dataclass
class GovernorKnowledgeProfile:
    """Complete knowledge profile for a governor"""
    governor_name: str
    primary_traditions: List[str]
    knowledge_concepts: List[str]
    wisdom_elements: List[str]
    semantic_matches: List[SemanticKnowledgeMatch]
    relevance_scores: Dict[str, float]
    integration_summary: str


class SemanticKnowledgeIntegrator:
    """
    Semantic knowledge integrator for the storyline engine.
    
    Provides vector search and semantic retrieval capabilities
    by connecting to the Lighthouse Knowledge Engine.
    """
    
    def __init__(self, knowledge_base_path: Optional[Path] = None):
        """
        Initialize semantic knowledge integrator.
        
        Args:
            knowledge_base_path: Path to knowledge base directory
        """
        self.knowledge_base_path = knowledge_base_path or Path(__file__).parent.parent / "knowledge_base"
        
        # Initialize retrievers
        self.unified_retriever = None
        self.focused_retriever = None
        
        # Knowledge mappings
        self.tradition_mappings = self._load_tradition_mappings()
        self.concept_embeddings = {}  # For vector search (placeholder)
        
        # Initialize retrievers if available
        self._initialize_retrievers()
        
        logger.info("SemanticKnowledgeIntegrator initialized")
    
    def _initialize_retrievers(self) -> None:
        """Initialize knowledge retrievers if available"""
        try:
            if UnifiedKnowledgeRetriever:
                self.unified_retriever = UnifiedKnowledgeRetriever()
                logger.info("Unified knowledge retriever initialized")
            
            if FocusedMysticalRetriever:
                self.focused_retriever = FocusedMysticalRetriever()
                logger.info("Focused mystical retriever initialized")
                
        except Exception as e:
            logger.warning(f"Failed to initialize retrievers: {e}")
    
    def _load_tradition_mappings(self) -> Dict[str, List[str]]:
        """Load tradition to concept mappings"""
        return {
            "hermetic_tradition": [
                "as above so below", "correspondence", "vibration", "polarity",
                "rhythm", "cause and effect", "gender", "mental transmutation"
            ],
            "kabbalah": [
                "sefirot", "tree of life", "paths", "emanation", "divine names",
                "gematria", "qabalah", "mystical union"
            ],
            "tarot_knowledge": [
                "major arcana", "minor arcana", "fool's journey", "divination",
                "symbolism", "archetypal wisdom", "card meanings"
            ],
            "sacred_geometry": [
                "golden ratio", "sacred proportions", "platonic solids",
                "flower of life", "geometric patterns", "divine mathematics"
            ],
            "classical_philosophy": [
                "stoicism", "platonism", "aristotelian", "virtue ethics",
                "dialectic", "metaphysics", "natural philosophy"
            ],
            "mystical_philosophy": [
                "gnosis", "mystical experience", "contemplation", "meditation",
                "spiritual transformation", "divine union"
            ],
            "chaos_magic": [
                "belief as tool", "sigil magic", "paradigm shifting",
                "results-focused", "eclectic approach"
            ],
            "thelema": [
                "true will", "do what thou wilt", "aeon", "holy guardian angel",
                "magick", "ceremonial practice"
            ]
        }
    
    def get_semantic_knowledge_profile(self, canonical_data: Dict) -> GovernorKnowledgeProfile:
        """
        Generate semantic knowledge profile for a governor.
        
        Args:
            canonical_data: Governor canonical data
            
        Returns:
            Complete knowledge profile with semantic matches
        """
        governor_name = canonical_data.get("name", "Unknown")
        
        # Extract semantic features
        semantic_features = self._extract_semantic_features(canonical_data)
        
        # Perform semantic retrieval
        semantic_matches = self._perform_semantic_retrieval(semantic_features)
        
        # Generate knowledge profile
        profile = self._build_knowledge_profile(
            governor_name, 
            canonical_data, 
            semantic_features, 
            semantic_matches
        )
        
        logger.info(f"Generated semantic knowledge profile for {governor_name}")
        return profile
    
    def _extract_semantic_features(self, canonical_data: Dict) -> Dict[str, List[str]]:
        """Extract semantic features from canonical data"""
        features = {
            "domain_keywords": [],
            "personality_keywords": [],
            "visual_keywords": [],
            "letter_keywords": [],
            "aethyr_keywords": []
        }
        
        # Extract from canonical traits
        canonical_traits = canonical_data.get("canonical_traits", {})
        
        # Domain keywords
        domain = canonical_traits.get("domain", "").lower()
        features["domain_keywords"] = self._extract_keywords_from_text(domain)
        
        # Personality keywords
        personality = canonical_traits.get("personality", [])
        for trait in personality:
            features["personality_keywords"].extend(
                self._extract_keywords_from_text(trait.lower())
            )
        
        # Visual keywords
        visual = canonical_traits.get("visual_motif", "").lower()
        features["visual_keywords"] = self._extract_keywords_from_text(visual)
        
        # Letter influence keywords
        letters = canonical_traits.get("letter_influence", [])
        for letter in letters:
            features["letter_keywords"].extend(
                self._extract_keywords_from_text(letter.lower())
            )
        
        # Aethyr keywords
        aethyr_name = canonical_data.get("aethyr_name", "").lower()
        correspondence = canonical_data.get("correspondence", "").lower()
        features["aethyr_keywords"] = (
            self._extract_keywords_from_text(aethyr_name) +
            self._extract_keywords_from_text(correspondence)
        )
        
        return features
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        if not text:
            return []
        
        # Simple keyword extraction (can be enhanced with NLP)
        words = text.replace("-", " ").replace("_", " ").split()
        keywords = []
        
        # Filter meaningful words
        stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        
        for word in words:
            word = word.strip().lower()
            if len(word) > 2 and word not in stopwords:
                keywords.append(word)
        
        return keywords
    
    def _perform_semantic_retrieval(self, semantic_features: Dict[str, List[str]]) -> List[SemanticKnowledgeMatch]:
        """Perform semantic retrieval using vector search"""
        matches = []
        
        # If retrievers are available, use them
        if self.unified_retriever or self.focused_retriever:
            matches.extend(self._retriever_based_search(semantic_features))
        
        # Always add tradition-based semantic matching as fallback
        matches.extend(self._tradition_based_semantic_matching(semantic_features))
        
        # Sort by relevance score
        matches.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return matches[:20]  # Top 20 matches
    
    def _retriever_based_search(self, semantic_features: Dict[str, List[str]]) -> List[SemanticKnowledgeMatch]:
        """Use knowledge retrievers for semantic search"""
        matches = []
        
        try:
            # Combine all keywords for query
            all_keywords = []
            for feature_type, keywords in semantic_features.items():
                all_keywords.extend(keywords)
            
            query = " ".join(all_keywords)
            
            # Use unified retriever if available
            if self.unified_retriever:
                try:
                    # Use search_by_keywords method that actually exists
                    keywords = [str(word) for word in query.split()]
                    results = self.unified_retriever.search_by_keywords(keywords)
                    
                    for result in results[:5]:
                        match = SemanticKnowledgeMatch(
                            tradition=result.tradition,
                            concept=result.title,
                            relevance_score=0.7,
                            wisdom_element=result.summary[:50] + "...",
                            source="unified_retriever",
                            context={"entry_id": result.id, "knowledge_type": result.knowledge_type.value}
                        )
                        matches.append(match)
                        
                except Exception as e:
                    logger.warning(f"Unified retriever search failed: {e}")
            
            # Use focused retriever if available
            if self.focused_retriever:
                try:
                    # Use retrieve_governor_knowledge method that actually exists
                    knowledge_selections = all_keywords[:5]  # Use top keywords
                    results = self.focused_retriever.retrieve_governor_knowledge(knowledge_selections)
                    
                    # Extract knowledge from results
                    for domain, knowledge in results.get("knowledge_profiles", {}).items():
                        match = SemanticKnowledgeMatch(
                            tradition="mystical_philosophy",
                            concept=domain,
                            relevance_score=0.6,
                            wisdom_element=knowledge.get("core_teachings", ["mystical insight"])[0] if knowledge.get("core_teachings") else "mystical insight",
                            source="focused_retriever",
                            context={"domain": domain, "knowledge": knowledge}
                        )
                        matches.append(match)
                        
                except Exception as e:
                    logger.warning(f"Focused retriever search failed: {e}")
                    
        except Exception as e:
            logger.error(f"Retriever-based search failed: {e}")
        
        return matches
    
    def _tradition_based_semantic_matching(self, semantic_features: Dict[str, List[str]]) -> List[SemanticKnowledgeMatch]:
        """Perform tradition-based semantic matching as fallback"""
        matches = []
        
        # Combine all keywords
        all_keywords = []
        for feature_type, keywords in semantic_features.items():
            all_keywords.extend(keywords)
        
        # Score against each tradition
        for tradition, concepts in self.tradition_mappings.items():
            relevance_score = self._calculate_semantic_similarity(all_keywords, concepts)
            
            if relevance_score > 0.1:  # Minimum threshold
                # Find best matching concept
                best_concept = self._find_best_concept_match(all_keywords, concepts)
                
                match = SemanticKnowledgeMatch(
                    tradition=tradition,
                    concept=best_concept,
                    relevance_score=relevance_score,
                    wisdom_element=f"{tradition} wisdom",
                    source="tradition_mapping",
                    context={"matched_keywords": all_keywords, "tradition_concepts": concepts}
                )
                matches.append(match)
        
        return matches
    
    def _calculate_semantic_similarity(self, keywords: List[str], concepts: List[str]) -> float:
        """Calculate semantic similarity between keywords and concepts"""
        if not keywords or not concepts:
            return 0.0
        
        # Simple overlap-based similarity (can be enhanced with embeddings)
        keyword_set = set(keywords)
        concept_words = set()
        
        for concept in concepts:
            concept_words.update(concept.replace("-", " ").replace("_", " ").split())
        
        # Calculate Jaccard similarity
        intersection = keyword_set.intersection(concept_words)
        union = keyword_set.union(concept_words)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def _find_best_concept_match(self, keywords: List[str], concepts: List[str]) -> str:
        """Find the best matching concept for given keywords"""
        best_concept = concepts[0] if concepts else "universal wisdom"
        best_score = 0.0
        
        for concept in concepts:
            concept_words = concept.replace("-", " ").replace("_", " ").split()
            score = self._calculate_semantic_similarity(keywords, concept_words)
            
            if score > best_score:
                best_score = score
                best_concept = concept
        
        return best_concept
    
    def _build_knowledge_profile(self, governor_name: str, canonical_data: Dict,
                               semantic_features: Dict, semantic_matches: List[SemanticKnowledgeMatch]) -> GovernorKnowledgeProfile:
        """Build complete knowledge profile"""
        
        # Extract primary traditions (top 3)
        tradition_scores = {}
        for match in semantic_matches:
            tradition = match.tradition
            if tradition not in tradition_scores:
                tradition_scores[tradition] = 0.0
            tradition_scores[tradition] += match.relevance_score
        
        primary_traditions = sorted(tradition_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        primary_traditions = [t[0] for t in primary_traditions]
        
        # Extract knowledge concepts (top 10)
        knowledge_concepts = [match.concept for match in semantic_matches[:10]]
        
        # Extract wisdom elements
        wisdom_elements = list(set([match.wisdom_element for match in semantic_matches[:10]]))
        
        # Generate integration summary
        integration_summary = self._generate_integration_summary(
            governor_name, primary_traditions, semantic_matches[:5]
        )
        
        return GovernorKnowledgeProfile(
            governor_name=governor_name,
            primary_traditions=primary_traditions,
            knowledge_concepts=knowledge_concepts,
            wisdom_elements=wisdom_elements,
            semantic_matches=semantic_matches,
            relevance_scores=tradition_scores,
            integration_summary=integration_summary
        )
    
    def _generate_integration_summary(self, governor_name: str, traditions: List[str], 
                                    top_matches: List[SemanticKnowledgeMatch]) -> str:
        """Generate human-readable integration summary"""
        if not traditions or not top_matches:
            return f"{governor_name} embodies universal wisdom and archetypal knowledge."
        
        primary_tradition = traditions[0].replace("_", " ").title()
        top_concept = top_matches[0].concept if top_matches else "wisdom"
        
        summary = f"{governor_name} is primarily aligned with {primary_tradition}, "
        summary += f"with deep resonance in {top_concept}. "
        
        if len(traditions) > 1:
            other_traditions = ", ".join([t.replace("_", " ").title() for t in traditions[1:]])
            summary += f"Secondary influences include {other_traditions}. "
        
        summary += f"This governor serves as a bridge between mystical knowledge and practical wisdom."
        
        return summary 