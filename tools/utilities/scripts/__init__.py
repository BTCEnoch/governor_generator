"""
Scripts package for AI Governor Review System
"""

# Make key classes available at package level
try:
    from .ai_governor_review_system import AIGovernorReviewSystem
    __all__ = ['AIGovernorReviewSystem']
except ImportError:
    # Handle case where dependencies aren't available
    __all__ = [] 