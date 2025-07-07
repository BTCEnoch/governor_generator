"""
Text Processing Utilities
Common text manipulation and formatting functions
"""

import re
import logging
from typing import List, Dict, Optional, Union
from pathlib import Path

logger = logging.getLogger(__name__)

def normalize_text(text: str) -> str:
    """
    Normalize text by removing extra whitespace and converting to lowercase
    
    Args:
        text: Text to normalize
        
    Returns:
        Normalized text
    """
    return ' '.join(text.lower().split())

def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extract keywords from text
    
    Args:
        text: Text to process
        min_length: Minimum keyword length (default: 3)
        
    Returns:
        List of keywords
    """
    # Remove special characters and normalize
    cleaned = re.sub(r'[^\w\s]', ' ', text.lower())
    words = cleaned.split()
    
    # Filter words by length and remove duplicates
    return list(set(word for word in words if len(word) >= min_length))

def format_list(items: List[str], separator: str = ', ', last_separator: str = ' and ') -> str:
    """
    Format a list of items into a human-readable string
    
    Args:
        items: List of items to format
        separator: Separator between items (default: ', ')
        last_separator: Separator before last item (default: ' and ')
        
    Returns:
        Formatted string
    """
    if not items:
        return ''
    if len(items) == 1:
        return str(items[0])
    return f"{separator.join(str(item) for item in items[:-1])}{last_separator}{items[-1]}"

def truncate_text(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated (default: '...')
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def slugify(text: str) -> str:
    """
    Convert text to URL-friendly slug
    
    Args:
        text: Text to convert
        
    Returns:
        URL-friendly slug
    """
    # Convert to lowercase and normalize unicode
    text = text.lower().strip()
    
    # Replace spaces with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    
    # Remove special characters
    text = re.sub(r'[^\w\-]', '', text)
    
    # Remove duplicate hyphens
    text = re.sub(r'-+', '-', text)
    
    return text.strip('-') 