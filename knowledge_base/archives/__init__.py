"""
Knowledge Base Archives Package
==============================

Contains archived tools and templates for knowledge processing and governor review.
"""

# Import key archive components for easy access
from .governor_review_template import (
    GovernorReviewTemplateGenerator,
    GovernorReviewTemplate,
    ReviewSection
)

__all__ = [
    'GovernorReviewTemplateGenerator',
    'GovernorReviewTemplate', 
    'ReviewSection'
] 