"""Script to process governor interview content into procedural templates."""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

from core.governors.profiler.interview.content_processor import ContentProcessor
from core.utils.custom_logging.custom_logger import setup_logger

# Setup logging
logger = setup_logger(__name__)

def main():
    """Run the content processing."""
    try:
        # Get project root directory
        project_root = Path(__file__).parent.parent
        
        # Get latest interview output directory
        interview_dir = project_root / "interview_output"
        if not interview_dir.exists():
            raise FileNotFoundError(
                "Interview output directory not found. Run interviews first."
            )
            
        # Get latest interview results
        output_dirs = sorted(
            [d for d in interview_dir.iterdir() if d.is_dir()],
            key=lambda d: d.name,
            reverse=True
        )
        if not output_dirs:
            raise FileNotFoundError(
                "No interview results found. Run interviews first."
            )
        latest_output = output_dirs[0]
        
        # Setup output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        templates_dir = project_root / "templates_output" / timestamp
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Starting content processing")
        logger.info(f"Reading interviews from: {latest_output}")
        logger.info(f"Writing templates to: {templates_dir}")
        
        # Create processor
        processor = ContentProcessor(latest_output, templates_dir)
        
        # Process content
        processor.process_all_content()
        
        logger.info("Content processing completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Error processing content: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 