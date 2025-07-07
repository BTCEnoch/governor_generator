"""Script to run visual aspects interviews for all governors."""

import argparse
import logging
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
from tqdm import tqdm

# Add project root to PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.utils.custom_logging.custom_logger import setup_logger
from core.governors.profiler.interview.visual_aspects_interview import (
    process_governor_visual_aspects
)

logger = setup_logger(__name__)

def process_governors(
    governors_dir: Path,
    questions_file: Path,
    max_workers: Optional[int] = None
) -> None:
    """Process visual aspects interviews for all governors.
    
    Args:
        governors_dir: Directory containing governor files
        questions_file: Path to questions JSON file
        max_workers: Maximum number of parallel workers
    """
    logger.info("Starting visual aspects interviews")
    
    # Get list of governor files
    governor_files = list(governors_dir.glob("*.json"))
    total_governors = len(governor_files)
    
    logger.info(f"Found {total_governors} governors to process")
    
    # Process in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_governor = {
            executor.submit(
                process_governor_visual_aspects,
                gov_file,
                questions_file
            ): gov_file
            for gov_file in governor_files
        }
        
        # Process results as they complete
        with tqdm(total=total_governors, desc="Processing Governors") as pbar:
            for future in as_completed(future_to_governor):
                governor_file = future_to_governor[future]
                try:
                    future.result()
                    logger.info(
                        f"Completed processing {governor_file.name}"
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to process {governor_file.name}: {str(e)}"
                    )
                pbar.update(1)
                
    logger.info("Visual aspects interviews complete")

def main():
    """Run the visual aspects interview process."""
    parser = argparse.ArgumentParser(
        description="Run visual aspects interviews for all governors"
    )
    parser.add_argument(
        "--governors-dir",
        type=str,
        default="governor_dossier",
        help="Directory containing governor files"
    )
    parser.add_argument(
        "--questions-file",
        type=str,
        default="core/governors/profiler/data/visual_aspects_questions.json",
        help="Path to questions JSON file"
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        help="Maximum number of parallel workers"
    )
    
    args = parser.parse_args()
    
    try:
        # Convert paths
        governors_dir = Path(args.governors_dir)
        questions_file = Path(args.questions_file)
        
        # Validate paths
        if not governors_dir.exists():
            raise FileNotFoundError(
                f"Governors directory not found: {governors_dir}"
            )
        if not questions_file.exists():
            raise FileNotFoundError(
                f"Questions file not found: {questions_file}"
            )
            
        # Run processing
        process_governors(
            governors_dir,
            questions_file,
            max_workers=args.max_workers
        )
        
        logger.info("Process completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Error running visual aspects interviews: {str(e)}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main()) 