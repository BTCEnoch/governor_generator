"""
Utility functions for the Universal JSON Cleaner
"""

import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
import chardet
from datetime import datetime

logger = logging.getLogger(__name__)

def setup_logging(log_dir: Path) -> None:
    """Setup logging with proper path handling"""
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"cleaning_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def detect_encoding(file_path: Path) -> str:
    """Detect file encoding using chardet"""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            if raw_data.startswith(b'\xef\xbb\xbf'):
                return 'utf-8-sig'
            elif not raw_data:
                return 'utf-8'
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'
    except Exception as e:
        logger.warning(f"Error detecting encoding for {file_path}: {e}")
        return 'utf-8'

def is_binary_file(file_path: Path) -> bool:
    """Check if a file is binary"""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(8192)
            return b'\0' in chunk
    except Exception as e:
        logger.error(f"Error checking if file is binary {file_path}: {e}")
        return True

def create_backup(file_path: Path, backup_dir: Path) -> Optional[Path]:
    """Create a backup of the file"""
    try:
        backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = backup_dir / f"{file_path.name}.{timestamp}.bak"
        import shutil
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        logger.error(f"Error creating backup for {file_path}: {e}")
        return None

def validate_json(content: str) -> bool:
    """Validate JSON content"""
    try:
        json.loads(content)
        return True
    except json.JSONDecodeError as e:
        logger.error(f"JSON validation failed: {e}")
        return False

def safe_file_read(file_path: Path, encoding: str = 'utf-8') -> Optional[str]:
    """Safely read file content"""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None

def safe_file_write(file_path: Path, content: str, encoding: str = 'utf-8') -> bool:
    """Safely write content to file"""
    try:
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        logger.error(f"Error writing file {file_path}: {e}")
        return False

def get_file_stats(file_path: Path) -> Dict[str, Any]:
    """Get file statistics"""
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