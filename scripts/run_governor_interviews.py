"""Script to run governor interviews and generate content libraries."""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

from core.governors.profiler.interview.batch_interview_processor import (
    run_batch_interviews
)
from core.utils.custom_logging.custom_logger import setup_logger

# Setup logging
logger = setup_logger(__name__)

def main():
    """Run the governor interview process."""
    try:
        # Get project root directory
        project_root = Path(__file__).parent.parent
        
        # Setup directories
        governors_dir = project_root / "governor_dossier"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = project_root / "interview_output" / timestamp
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Starting governor interview process")
        logger.info(f"Reading governors from: {governors_dir}")
        logger.info(f"Writing output to: {output_dir}")
        
        # Run interviews
        run_batch_interviews(
            governors_dir=str(governors_dir),
            output_dir=str(output_dir),
            max_workers=os.cpu_count()
        )
        
        logger.info("Governor interview process completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Error running governor interviews: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 