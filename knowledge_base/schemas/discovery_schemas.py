from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class SourceCandidate:
    """Potential replacement URL with quality metrics"""
    url: str
    tradition: str
    title: str
    estimated_word_count: int
    content_quality_score: float  # 0.0-1.0
    source_type: str  # "sacred_texts", "archive_org", "hermetic", "google_search", "semantic_scholar"
    discovery_method: str
    test_timestamp: str
    is_accessible: bool = True
    content_preview: str = ""
    metadata: Dict = field(default_factory=dict)

@dataclass 
class ReplacementPlan:
    """Complete URL replacement strategy for a tradition"""
    tradition_name: str
    current_broken_urls: List[str]
    replacement_candidates: List[SourceCandidate]
    recommended_replacements: List[SourceCandidate]
    total_estimated_words: int
    confidence_score: float

@dataclass
class DiscoverySession:
    """Complete discovery session results"""
    session_id: str
    timestamp: str
    traditions_processed: List[str]
    total_candidates_found: int
    replacement_plans: List[ReplacementPlan]
    success_rate_improvement: float

@dataclass
class GoogleSearchResult:
    """Result from Google Custom Search API"""
    title: str
    url: str
    snippet: str
    display_url: str
    relevance_score: float = 0.0

@dataclass
class SemanticScholarPaper:
    """Academic paper from Semantic Scholar"""
    paper_id: str
    title: str
    abstract: str
    authors: List[str]
    year: Optional[int]
    url: str
    citation_count: int
    relevance_score: float = 0.0 