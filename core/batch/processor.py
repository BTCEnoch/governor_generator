"""
Batch Processor Implementation

Handles the core batch processing logic with enhanced error handling
and progress tracking.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

from core.utils.custom_logging import setup_logger
from core.utils.common.progress import ProgressTracker
from .models import (
    BatchJobConfig,
    BatchJobResult,
    BatchJobStatus,
    BatchJobType
)

logger = setup_logger(__name__)

class BatchProcessor:
    """
    Core batch processing implementation with enhanced monitoring
    and parallel processing capabilities.
    """
    
    def __init__(self, base_path: Path):
        """Initialize the batch processor"""
        self.base_path = Path(base_path)
        self.jobs: Dict[str, BatchJobResult] = {}
        self.configs: Dict[str, BatchJobConfig] = {}
        self.progress_tracker = ProgressTracker()
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Ensure job storage directory exists
        self.jobs_dir = self.base_path / "batch_jobs"
        self.jobs_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("📦 Batch Processor initialized")
    
    def create_batch_job(self, config: BatchJobConfig) -> BatchJobResult:
        """
        Create a new batch job from configuration
        """
        # Validate output directory
        output_dir = Path(config.output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create job result
        result = BatchJobResult(
            job_id=config.job_id,
            status=BatchJobStatus.PENDING,
            total_items=config.total_items
        )
        
        # Store job info
        self.jobs[config.job_id] = result
        self.configs[config.job_id] = config
        
        # Save job config to disk
        self._save_job_config(config)
        
        logger.info(f"✨ Created batch job: {config.job_id}")
        return result
    
    def process_batch_job(self, job_id: str) -> BatchJobResult:
        """
        Process a batch job with progress tracking and error handling
        """
        if job_id not in self.configs:
            raise ValueError(f"Job {job_id} not found")
            
        config = self.configs[job_id]
        result = self.jobs[job_id]
        
        try:
            # Update status
            result.status = BatchJobStatus.IN_PROGRESS
            result.start_time = datetime.now()
            
            # Process in batches
            total_batches = (len(config.input_data) + config.batch_size - 1) // config.batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * config.batch_size
                end_idx = min(start_idx + config.batch_size, len(config.input_data))
                batch_data = config.input_data[start_idx:end_idx]
                
                try:
                    self._process_batch(batch_data, config, result)
                    result.processed_items += len(batch_data)
                    
                    # Update progress
                    progress = (batch_idx + 1) / total_batches * 100
                    logger.info(f"📊 Job {job_id}: {progress:.1f}% complete")
                    
                except Exception as e:
                    logger.error(f"❌ Error processing batch {batch_idx}: {str(e)}")
                    result.error_messages.append(f"Batch {batch_idx}: {str(e)}")
            
            # Update final status
            result.status = BatchJobStatus.COMPLETED
            result.end_time = datetime.now()
            
            logger.info(f"✅ Completed job {job_id}")
            return result
            
        except Exception as e:
            result.status = BatchJobStatus.FAILED
            result.end_time = datetime.now()
            result.error_messages.append(str(e))
            logger.error(f"❌ Job {job_id} failed: {str(e)}")
            raise
    
    def _process_batch(
        self,
        batch_data: List[Dict[str, Any]],
        config: BatchJobConfig,
        result: BatchJobResult
    ) -> None:
        """Process a single batch of data"""
        if config.job_type == BatchJobType.STORYLINE_GENERATION:
            self._process_storyline_batch(batch_data, config, result)
        elif config.job_type == BatchJobType.TRAIT_GENERATION:
            self._process_trait_batch(batch_data, config, result)
        else:
            raise ValueError(f"Unsupported job type: {config.job_type}")
    
    def _process_storyline_batch(
        self,
        batch_data: List[Dict[str, Any]],
        config: BatchJobConfig,
        result: BatchJobResult
    ) -> None:
        """Process a batch of storyline generation data"""
        for item in batch_data:
            output_file = Path(config.output_directory) / f"{item['id']}_storyline.json"
            # Process storyline logic here
            result.output_files.append(output_file)
    
    def _process_trait_batch(
        self,
        batch_data: List[Dict[str, Any]],
        config: BatchJobConfig,
        result: BatchJobResult
    ) -> None:
        """Process a batch of trait generation data"""
        for item in batch_data:
            output_file = Path(config.output_directory) / f"{item['id']}_traits.json"
            # Process trait generation logic here
            result.output_files.append(output_file)
    
    def get_job_status(self, job_id: str) -> Optional[BatchJobResult]:
        """Get the current status of a job"""
        return self.jobs.get(job_id)
    
    def list_jobs(self) -> List[BatchJobResult]:
        """List all jobs"""
        return list(self.jobs.values())
    
    def _save_job_config(self, config: BatchJobConfig) -> None:
        """Save job configuration to disk"""
        config_file = self.jobs_dir / f"{config.job_id}_config.json"
        with open(config_file, 'w') as f:
            json.dump(config.dict(), f, indent=2, default=str)
    
    def _load_job_config(self, job_id: str) -> Optional[BatchJobConfig]:
        """Load job configuration from disk"""
        config_file = self.jobs_dir / f"{job_id}_config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                data = json.load(f)
                return BatchJobConfig(**data)
        return None 