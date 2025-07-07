"""
Interview schemas for batch governor processing.

This module defines the data structures for interview questions and responses.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class QuestionCategory(str, Enum):
    """Categories of interview questions"""
    PERSONALITY = 'personality'
    KNOWLEDGE = 'knowledge'
    MYSTICAL = 'mystical'
    INTERACTION = 'interaction'
    MANIFESTATION = 'manifestation'
    TEACHING = 'teaching'
    RITUAL = 'ritual'
    PROPHECY = 'prophecy'

@dataclass
class InterviewQuestion:
    """Structure for a single interview question"""
    id: str
    category: QuestionCategory
    question: str
    context: Optional[str] = None
    required_traits: List[str] = field(default_factory=list)
    validation_rules: List[str] = field(default_factory=list)

@dataclass
class InterviewResponse:
    """Structure for a response to an interview question"""
    question_id: str
    response_text: str
    traits_considered: List[str]
    confidence_score: float
    validation_notes: Optional[str] = None

@dataclass
class InterviewSession:
    """Structure for a complete interview session"""
    governor_name: str
    timestamp: str
    questions: List[InterviewQuestion]
    responses: Dict[str, InterviewResponse]
    session_notes: Optional[str] = None
    validation_status: bool = False 