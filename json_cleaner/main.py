"""
Main entry point for the Universal JSON Cleaner
"""

import asyncio
import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Optional

from .cleaner import UnicodeCleaner
from .config import DEFAULT_CONFIG, get_log_path
from .utils import setup_logging

logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Universal JSON Cleaner - Clean Unicode characters from text files'
    )
    parser.add_argument(
        '--root',
        type=str,
        default='.',
        help='Root directory to process'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to custom configuration file'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Disable backup creation'
    )
    parser.add_argument(
        '--max-size',
        type=int,
        help='Maximum file size in MB to process'
    )
    parser.add_argument(
        '--concurrent',
        type=int,
        help='Maximum number of concurrent files to process'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Enable strict mode (fail on any error)'
    )
    return parser.parse_args()

def load_config(config_path: Optional[str] = None) -> Dict:
    """Load configuration from file or use defaults"""
    config = DEFAULT_CONFIG.copy()
    
    if config_path:
        try:
            with open(config_path, 'r') as f:
                custom_config = json.load(f)
                config.update(custom_config)
        except Exception as e:
            logger.error(f"Error loading config from {config_path}: {e}")
            logger.info("Using default configuration")
    
    return config

def update_config_from_args(config: Dict, args: argparse.Namespace) -> Dict:
    """Update configuration with command line arguments"""
    if args.no_backup:
        config['backup_enabled'] = False
    if args.max_size:
        config['max_file_size_mb'] = args.max_size
    if args.concurrent:
        config['max_concurrent_files'] = args.concurrent
    if args.strict:
        config['strict_mode'] = True
    return config

async def main() -> None:
    """Main entry point"""
    # Parse arguments and load configuration
    args = parse_args()
    config = load_config(args.config)
    config = update_config_from_args(config, args)
    
    # Setup logging
    setup_logging(get_log_path())
    
    try:
        # Initialize and run the cleaner
        cleaner = UnicodeCleaner(args.root, config)
        stats = await cleaner.process_directory()
        
        # Print summary
        logger.info("\nProcessing Summary:")
        logger.info(f"Start Time: {stats['start_time']}")
        logger.info(f"End Time: {stats['end_time']}")
        logger.info(f"Files Processed: {stats['files_processed']}")
        logger.info(f"Files Cleaned: {stats['files_cleaned']}")
        logger.info(f"Unicode Characters Replaced: {stats['unicode_chars_replaced']}")
        logger.info(f"Backup Files Created: {stats['backup_files_created']}")
        logger.info(f"Errors Encountered: {stats['files_errors']}")
        
        if stats['errors']:
            logger.warning("\nErrors encountered during processing:")
            for error in stats['errors']:
                logger.warning(f"{error['timestamp']}: {error['file']} - {error['error']}")
                
        # Exit with error if strict mode is enabled and errors occurred
        if config['strict_mode'] and stats['files_errors'] > 0:
            raise SystemExit(1)
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise SystemExit(1)

if __name__ == '__main__':
    asyncio.run(main()) 