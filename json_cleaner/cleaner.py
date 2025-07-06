"""
Core Unicode Cleaner implementation with async support
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set
import aiofiles
from datetime import datetime

from .config import (
    DEFAULT_CONFIG,
    FILE_TYPE_CONFIG,
    UNICODE_REPLACEMENTS,
    get_backup_path,
    get_log_path
)
from .utils import (
    setup_logging,
    detect_encoding,
    is_binary_file,
    create_backup,
    validate_json,
    safe_file_read,
    safe_file_write,
    get_file_stats
)

logger = logging.getLogger(__name__)

class UnicodeCleaner:
    def __init__(self, project_root: str = ".", config: Optional[Dict] = None):
        """Initialize the Unicode Cleaner with configuration"""
        self.project_root = Path(project_root)
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.stats = self._init_stats()
        self.processed_files: Set[Path] = set()
        
        # Setup logging
        setup_logging(get_log_path())
        
    def _init_stats(self) -> Dict:
        """Initialize statistics tracking"""
        return {
            'start_time': datetime.now(),
            'files_processed': 0,
            'files_cleaned': 0,
            'files_errors': 0,
            'files_skipped': 0,
            'unicode_chars_replaced': 0,
            'backup_files_created': 0,
            'validation_failures': 0,
            'binary_files_skipped': 0,
            'file_types_processed': {},
            'encoding_types_used': {},
            'errors': []
        }
    
    async def clean_text(self, content: str) -> str:
        """Clean Unicode characters from text content"""
        cleaned = content
        replacements_made = 0
        
        for old, new in UNICODE_REPLACEMENTS.items():
            if old in cleaned:
                count = cleaned.count(old)
                cleaned = cleaned.replace(old, new)
                replacements_made += count
                
        self.stats['unicode_chars_replaced'] += replacements_made
        return cleaned
    
    async def process_file(self, file_path: Path) -> bool:
        """Process a single file asynchronously"""
        if file_path in self.processed_files:
            logger.debug(f"Skipping already processed file: {file_path}")
            return False
            
        try:
            if is_binary_file(file_path):
                logger.info(f"Skipping binary file: {file_path}")
                self.stats['binary_files_skipped'] += 1
                return False
                
            encoding = detect_encoding(file_path)
            self.stats['encoding_types_used'][encoding] = \
                self.stats['encoding_types_used'].get(encoding, 0) + 1
            
            # Create backup if enabled
            if self.config['backup_enabled']:
                backup_path = create_backup(file_path, get_backup_path())
                if backup_path:
                    self.stats['backup_files_created'] += 1
            
            # Read and clean file content
            content = safe_file_read(file_path, encoding)
            if content is None:
                raise ValueError(f"Could not read file: {file_path}")
                
            cleaned_content = await self.clean_text(content)
            
            # Validate if it's a JSON file
            if file_path.suffix.lower() == '.json' and \
               FILE_TYPE_CONFIG['json']['validate_after_clean']:
                if not validate_json(cleaned_content):
                    self.stats['validation_failures'] += 1
                    raise ValueError(f"JSON validation failed for: {file_path}")
            
            # Write cleaned content
            if safe_file_write(file_path, cleaned_content, encoding):
                self.stats['files_cleaned'] += 1
                self.processed_files.add(file_path)
                return True
            else:
                raise ValueError(f"Failed to write cleaned content to: {file_path}")
                
        except Exception as e:
            self.stats['files_errors'] += 1
            self.stats['errors'].append({
                'file': str(file_path),
                'error': str(e),
                'timestamp': datetime.now()
            })
            logger.error(f"Error processing {file_path}: {e}")
            return False
            
        finally:
            self.stats['files_processed'] += 1
    
    async def process_directory(self, directory: Optional[Path] = None) -> Dict:
        """Process all text files in a directory asynchronously"""
        if directory is None:
            directory = self.project_root
            
        try:
            tasks = []
            for file_path in directory.rglob('*'):
                if file_path.is_file() and not any(p.startswith('.') for p in file_path.parts):
                    tasks.append(self.process_file(file_path))
                    
                    # Process in chunks to avoid memory issues
                    if len(tasks) >= self.config['max_concurrent_files']:
                        await asyncio.gather(*tasks)
                        tasks = []
            
            if tasks:
                await asyncio.gather(*tasks)
                
        except Exception as e:
            logger.error(f"Error processing directory {directory}: {e}")
            self.stats['errors'].append({
                'directory': str(directory),
                'error': str(e),
                'timestamp': datetime.now()
            })
            
        self.stats['end_time'] = datetime.now()
        return self.stats
    
    def get_stats(self) -> Dict:
        """Get current processing statistics"""
        return self.stats 