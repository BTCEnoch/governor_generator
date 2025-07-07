"""
Batch Interview Processor

This module handles running interviews for all governors in batch,
processing responses and ensuring consistency with governor profiles.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from core.governors.profiler.schemas.interview_schema import (
    InterviewQuestion, InterviewResponse, InterviewSession, QuestionCategory
)
from core.utils.custom_logging.custom_logger import setup_logger
from core.governors.profiler.interview.governor_interview_system import (
    GovernorInterviewSystem, ContentLibrary
)
from core.utils.common.progress import ProgressTracker

logger = setup_logger(__name__)

class BatchInterviewProcessor:
    """Processes interviews for all governors in parallel."""
    
    def __init__(
        self,
        governors_dir: Path,
        output_dir: Path,
        max_workers: Optional[int] = None
    ):
        """Initialize the batch processor.
        
        Args:
            governors_dir: Directory containing governor trait files
            output_dir: Directory to save interview results
            max_workers: Maximum number of parallel workers
        """
        self.logger = logging.getLogger(__name__)
        self.governors_dir = governors_dir
        self.output_dir = output_dir
        self.max_workers = max_workers
        
        # Create interview system
        self.interview_system = GovernorInterviewSystem(output_dir)
        
        # Get total number of governors
        governor_files = list(self.governors_dir.glob("*.json"))
        total_governors = len(governor_files)
        
        # Initialize progress tracking
        self.progress = ProgressTracker(total=total_governors)
        
    def process_all_governors(self) -> Dict[str, ContentLibrary]:
        """Process interviews for all governors.
        
        Returns:
            Dict mapping governor names to their content libraries
        """
        self.logger.info("Starting batch interview processing")
        
        # Get list of governor files
        governor_files = list(self.governors_dir.glob("*.json"))
        total_governors = len(governor_files)
        
        self.logger.info(f"Found {total_governors} governors to process")
        
        # Initialize results
        results: Dict[str, ContentLibrary] = {}
        
        # Process in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_governor = {
                executor.submit(self._process_governor, gov_file): gov_file
                for gov_file in governor_files
            }
            
            # Process results as they complete
            with tqdm(total=total_governors, desc="Processing Governors") as pbar:
                for future in as_completed(future_to_governor):
                    governor_file = future_to_governor[future]
                    try:
                        library = future.result()
                        results[library.governor_name] = library
                        self.logger.info(
                            f"Completed processing {library.governor_name}"
                        )
                    except Exception as e:
                        self.logger.error(
                            f"Failed to process {governor_file.name}: {str(e)}"
                        )
                    pbar.update(1)
                    
        self.logger.info(
            f"Completed batch processing. Processed {len(results)} governors"
        )
        return results
        
    def _process_governor(self, governor_file: Path) -> ContentLibrary:
        """Process interviews for a single governor.
        
        Args:
            governor_file: Path to governor's trait file
            
        Returns:
            Generated content library
        """
        # Load governor traits
        with governor_file.open('r', encoding='utf-8') as f:
            traits = json.load(f)
            
        governor_name = governor_file.stem
        self.logger.info(f"Processing governor {governor_name}")
        
        # Conduct interviews
        try:
            library = self.interview_system.conduct_full_interview_series(
                governor_name, traits
            )
            return library
        except Exception as e:
            self.logger.error(
                f"Error processing {governor_name}: {str(e)}"
            )
            raise
            
def run_batch_interviews(
    governors_dir: str,
    output_dir: str,
    max_workers: Optional[int] = None
) -> None:
    """Run batch interview processing.
    
    Args:
        governors_dir: Directory containing governor trait files
        output_dir: Directory to save interview results
        max_workers: Maximum number of parallel workers
    """
    # Convert paths
    governors_path = Path(governors_dir)
    output_path = Path(output_dir)
    
    # Create processor
    processor = BatchInterviewProcessor(
        governors_path,
        output_path,
        max_workers=max_workers
    )
    
    # Run processing
    processor.process_all_governors()
    
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run batch governor interviews"
    )
    parser.add_argument(
        "--governors-dir",
        required=True,
        help="Directory containing governor trait files"
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory to save interview results"
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        help="Maximum number of parallel workers"
    )
    
    args = parser.parse_args()
    
    run_batch_interviews(
        args.governors_dir,
        args.output_dir,
        max_workers=args.max_workers
    ) 