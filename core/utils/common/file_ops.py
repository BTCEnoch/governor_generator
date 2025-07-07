"""
Common File Operations
Shared file handling utilities for the Governor Generation system
"""

import os
import json
import logging
import chardet
from pathlib import Path
from typing import Any, Dict, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)

def safe_file_read(file_path: Path, encoding: str = 'utf-8') -> Optional[str]:
    """
    Safely read file content with error handling and logging
    
    Args:
        file_path: Path to the file to read
        encoding: File encoding (default: utf-8)
        
    Returns:
        File content as string or None if error
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        # Try to detect encoding
        with open(file_path, 'rb') as f:
            raw = f.read()
            result = chardet.detect(raw)
            detected_encoding = result['encoding']
            
        try:
            with open(file_path, 'r', encoding=detected_encoding) as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path} with detected encoding {detected_encoding}: {e}")
            return None
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None

def safe_file_write(file_path: Path, content: str, encoding: str = 'utf-8') -> bool:
    """
    Safely write content to file with error handling and logging
    
    Args:
        file_path: Path to write to
        content: Content to write
        encoding: File encoding (default: utf-8)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        logger.error(f"Error writing file {file_path}: {e}")
        return False

def safe_json_read(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Safely read and parse JSON file
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON as dict or None if error
    """
    content = safe_file_read(file_path)
    if content is None:
        return None
        
    try:
        return json.loads(content)
    except Exception as e:
        logger.error(f"Error parsing JSON from {file_path}: {e}")
        return None

def safe_json_write(file_path: Path, data: Dict[str, Any], pretty: bool = True) -> bool:
    """
    Safely write data as JSON file
    
    Args:
        file_path: Path to write to
        data: Data to serialize
        pretty: Whether to pretty-print JSON (default: True)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        content = json.dumps(data, indent=2 if pretty else None)
        return safe_file_write(file_path, content)
    except Exception as e:
        logger.error(f"Error writing JSON to {file_path}: {e}")
        return False

def get_file_stats(file_path: Path) -> Dict[str, Any]:
    """
    Get file statistics
    
    Args:
        file_path: Path to analyze
        
    Returns:
        Dict with file stats (size, modified date, created date)
    """
    try:
        stats = os.stat(file_path)
        return {
            'size': stats.st_size,
            'modified': datetime.fromtimestamp(stats.st_mtime),
            'created': datetime.fromtimestamp(stats.st_ctime)
        }
    except Exception as e:
        logger.error(f"Error getting file stats for {file_path}: {e}")
        return {} 