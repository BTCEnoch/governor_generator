"""
Configuration file for the Universal JSON Cleaner
"""

from typing import Dict, Any
from pathlib import Path

# Base configuration
DEFAULT_CONFIG = {
    'project_root': '.',
    'backup_enabled': True,
    'max_file_size_mb': 100,
    'chunk_size': 8192,
    'max_concurrent_files': 10,
    'validation_enabled': True,
    'strict_mode': False,
    'log_level': 'INFO',
}

# File type configurations
FILE_TYPE_CONFIG = {
    'json': {
        'validate_after_clean': True,
        'preserve_structure': True,
        'indent': 2
    },
    'text': {
        'validate_after_clean': False,
        'preserve_structure': False,
        'line_ending': '\n'
    }
}

# Comprehensive Unicode replacement dictionary
UNICODE_REPLACEMENTS: Dict[str, str] = {
    # Emoji replacements
    '🧙‍♂️': '[WIZARD]',
    '🎭': '[THEATER]',
    '🔮': '[CRYSTAL_BALL]',
    '⚡': '[LIGHTNING]',
    '🌟': '[STAR]',
    '✨': '[SPARKLES]',
    '🌙': '[MOON]',
    '☀️': '[SUN]',
    '🌈': '[RAINBOW]',
    '🔥': '[FIRE]',
    '💫': '[DIZZY]',
    
    # Smart quotes and punctuation
    ''': "'",  # Left single quotation mark
    ''': "'",  # Right single quotation mark
    '"': '"',  # Left double quotation mark
    '"': '"',  # Right double quotation mark
    
    # Dashes and hyphens
    '–': '-',   # En dash
    '—': '--',  # Em dash
    '―': '--',  # Horizontal bar
    
    # Spaces and special characters
    ' ': ' ',   # Non-breaking space
    '​': '',    # Zero width space
    '‌': '',    # Zero width non-joiner
    '‍': '',    # Zero width joiner
    
    # Ellipsis and dots
    '…': '...',  # Horizontal ellipsis
    '⋯': '...',  # Midline horizontal ellipsis
}

def get_log_path() -> Path:
    """Get the path to the log directory"""
    return Path(__file__).parent / "logs"

def get_backup_path() -> Path:
    """Get the path to store backup files"""
    return Path(__file__).parent / "backups" 