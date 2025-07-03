from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import json
from datetime import datetime

class KnowledgeType(Enum):
    PRINCIPLE = "principle"
    PRACTICE = "practice" 
    SYSTEM = "system"
    CONCEPT = "concept"
    HISTORICAL = "historical"
    PRACTICAL = "practical"

class ContentQuality(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class ExtractedContent:
    """Raw content extracted from web sources"""
    url: str
    title: str
    content: str
    tradition: str
    content_type: str
    word_count: int
    extraction_date: str
    success: bool = True
    error_message: Optional[str] = None

@dataclass
class KnowledgeEntry:
    """Processed, structured knowledge entry"""
    id: str
    tradition: str
    title: str
    summary: str  # 2-3 sentence summary
    full_content: str  # Complete content
    knowledge_type: KnowledgeType
    tags: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None
    source_url: str = ""
    confidence_score: float = 0.0
    quality: ContentQuality = ContentQuality.MEDIUM
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'tradition': self.tradition,
            'title': self.title,
            'summary': self.summary,
            'full_content': self.full_content,
            'knowledge_type': self.knowledge_type.value,
            'tags': self.tags,
            'related_concepts': self.related_concepts,
            'embedding': self.embedding,
            'source_url': self.source_url,
            'confidence_score': self.confidence_score,
            'quality': self.quality.value,
            'created_date': self.created_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'KnowledgeEntry':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            tradition=data['tradition'],
            title=data['title'],
            summary=data['summary'],
            full_content=data['full_content'],
            knowledge_type=KnowledgeType(data['knowledge_type']),
            tags=data.get('tags', []),
            related_concepts=data.get('related_concepts', []),
            embedding=data.get('embedding'),
            source_url=data.get('source_url', ''),
            confidence_score=data.get('confidence_score', 0.0),
            quality=ContentQuality(data.get('quality', 'medium')),
            created_date=data.get('created_date', datetime.now().isoformat())
        )

@dataclass
class ProcessedTradition:
    """Complete processed tradition with all its knowledge"""
    name: str
    description: str
    total_entries: int
    principles: List[KnowledgeEntry] = field(default_factory=list)
    practices: List[KnowledgeEntry] = field(default_factory=list)
    systems: List[KnowledgeEntry] = field(default_factory=list)
    concepts: List[KnowledgeEntry] = field(default_factory=list)
    cross_references: Dict[str, List[str]] = field(default_factory=dict)
    
    def get_all_entries(self) -> List[KnowledgeEntry]:
        """Get all knowledge entries regardless of type"""
        return self.principles + self.practices + self.systems + self.concepts
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'description': self.description,
            'total_entries': self.total_entries,
            'principles': [entry.to_dict() for entry in self.principles],
            'practices': [entry.to_dict() for entry in self.practices],
            'systems': [entry.to_dict() for entry in self.systems],
            'concepts': [entry.to_dict() for entry in self.concepts],
            'cross_references': self.cross_references
        }

@dataclass
class ExtractionStats:
    """Statistics for extraction process"""
    tradition: str
    total_urls: int
    successful_extractions: int
    failed_extractions: int
    total_words: int
    average_words_per_source: float
    extraction_time_seconds: float
    
    @property
    def success_rate(self) -> float:
        return (self.successful_extractions / self.total_urls) * 100 if self.total_urls > 0 else 0.0 