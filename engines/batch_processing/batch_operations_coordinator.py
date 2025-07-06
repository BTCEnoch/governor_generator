#!/usr/bin/env python3
"""
Batch Operations Coordinator
Provides high-level operations for batch processing
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

from unified_batch_processor import (
    UnifiedBatchProcessor,
    BatchJobConfig,
    BatchJobResult,
    BatchJobType,
    BatchJobStatus
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BatchOperationsCoordinator:
    """
    High-level coordinator for batch operations
    """
    
    def __init__(self, base_path: Path = Path(".")):
        """Initialize the batch operations coordinator"""
        self.base_path = Path(base_path)
        self.processor = UnifiedBatchProcessor(base_path)
        
        logger.info("🚀 Batch Operations Coordinator initialized")
    
    def create_storyline_batch(self, 
                             governor_files: List[Path],
                             output_dir: Path = Path("storyline_batch_output"),
                             job_id: Optional[str] = None) -> BatchJobResult:
        """Create a storyline generation batch job"""
        
        if job_id is None:
            job_id = f"storyline_{len(governor_files)}_governors"
        
        # Load governor data
        governor_data = []
        for file_path in governor_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    governor_data.append(data)
            except Exception as e:
                logger.warning(f"⚠️ Failed to load {file_path}: {str(e)}")
        
        # Create batch job
        config = BatchJobConfig(
            job_type=BatchJobType.STORYLINE_GENERATION,
            job_id=job_id,
            input_data=governor_data,
            output_directory=output_dir
        )
        
        return self.processor.create_batch_job(config)
    
    def process_job(self, job_id: str) -> BatchJobResult:
        """Process a batch job"""
        return self.processor.process_batch_job(job_id)
    
    def get_job_status(self, job_id: str) -> Optional[BatchJobResult]:
        """Get job status"""
        return self.processor.get_job_status(job_id)
    
    def list_all_jobs(self) -> List[BatchJobResult]:
        """List all jobs"""
        return self.processor.list_jobs()

if __name__ == "__main__":
    # Example usage
    coordinator = BatchOperationsCoordinator()
    
    # List existing jobs
    jobs = coordinator.list_all_jobs()
    logger.info(f"📋 Found {len(jobs)} jobs")
    
    for job in jobs:
        logger.info(f"   - {job.job_id}: {job.status.value}")
    
    logger.info("✅ Batch Operations Coordinator test complete") 