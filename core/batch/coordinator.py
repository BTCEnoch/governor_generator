"""
Batch Operations Coordinator

Provides high-level operations for batch processing with enhanced error handling,
logging, and Bitcoin-based job tracking.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
import json

from core.utils.custom_logging import setup_logger
from core.utils.common.errors import BatchProcessingError
from core.utils.common.progress import ProgressTracker
from .processor import BatchProcessor
from .models import (
    BatchJobConfig,
    BatchJobResult,
    BatchJobType,
    BatchJobStatus
)

logger = setup_logger(__name__)

class BatchMetrics(BaseModel):
    """Metrics for batch job execution"""
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    total_items: int = 0
    processed_items: int = 0
    success_rate: float = 0.0
    error_count: int = 0
    warnings: List[str] = Field(default_factory=list)

class BatchOperationsCoordinator:
    """
    High-level coordinator for batch operations with enhanced monitoring
    and Bitcoin-based verification.
    """
    
    def __init__(self, base_path: Path = Path(".")):
        """Initialize the batch operations coordinator"""
        self.base_path = Path(base_path)
        self.processor = BatchProcessor(base_path)
        self.progress_tracker = ProgressTracker()
        self.active_metrics: Dict[str, BatchMetrics] = {}
        
        logger.info("🚀 Batch Operations Coordinator initialized")
    
    def create_storyline_batch(
        self,
        governor_files: List[Path],
        output_dir: Path = Path("storyline_batch_output"),
        job_id: Optional[str] = None,
        batch_size: int = 10
    ) -> BatchJobResult:
        """
        Create a storyline generation batch job with improved chunking
        and progress tracking.
        """
        if job_id is None:
            job_id = f"storyline_{len(governor_files)}_governors_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize metrics
        self.active_metrics[job_id] = BatchMetrics(total_items=len(governor_files))
        
        # Load and validate governor data
        governor_data = []
        for file_path in governor_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    # Basic validation
                    if not isinstance(data, dict) or 'id' not in data:
                        raise ValueError(f"Invalid governor data format in {file_path}")
                    governor_data.append(data)
            except Exception as e:
                logger.warning(f"⚠️ Failed to load {file_path}: {str(e)}")
                self.active_metrics[job_id].warnings.append(f"Failed to load {file_path}: {str(e)}")
                self.active_metrics[job_id].error_count += 1
        
        # Create batch job with chunking
        config = BatchJobConfig(
            job_type=BatchJobType.STORYLINE_GENERATION,
            job_id=job_id,
            input_data=governor_data,
            output_directory=output_dir,
            batch_size=batch_size,
            total_items=len(governor_data)
        )
        
        return self.processor.create_batch_job(config)
    
    def process_job(self, job_id: str) -> BatchJobResult:
        """Process a batch job with enhanced monitoring"""
        try:
            result = self.processor.process_batch_job(job_id)
            
            # Update metrics
            if job_id in self.active_metrics:
                metrics = self.active_metrics[job_id]
                metrics.end_time = datetime.now()
                metrics.processed_items = result.processed_items
                metrics.success_rate = (
                    (metrics.total_items - metrics.error_count) / 
                    metrics.total_items if metrics.total_items > 0 else 0.0
                )
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to process job {job_id}: {str(e)}")
            if job_id in self.active_metrics:
                self.active_metrics[job_id].error_count += 1
            raise BatchProcessingError(f"Failed to process job {job_id}: {str(e)}")
    
    def get_job_status(self, job_id: str) -> Optional[BatchJobResult]:
        """Get detailed job status with metrics"""
        status = self.processor.get_job_status(job_id)
        if status and job_id in self.active_metrics:
            # Enhance status with metrics
            metrics = self.active_metrics[job_id]
            status.metrics = {
                "duration": str(metrics.end_time - metrics.start_time) if metrics.end_time else "In Progress",
                "success_rate": f"{metrics.success_rate * 100:.2f}%",
                "error_count": metrics.error_count,
                "warnings": metrics.warnings
            }
        return status
    
    def list_all_jobs(self) -> List[BatchJobResult]:
        """List all jobs with their metrics"""
        jobs = self.processor.list_jobs()
        # Enhance job results with metrics
        for job in jobs:
            if job.job_id in self.active_metrics:
                metrics = self.active_metrics[job.job_id]
                job.metrics = {
                    "duration": str(metrics.end_time - metrics.start_time) if metrics.end_time else "In Progress",
                    "success_rate": f"{metrics.success_rate * 100:.2f}%",
                    "error_count": metrics.error_count,
                    "warnings": metrics.warnings
                }
        return jobs

    def cleanup_completed_jobs(self, older_than_days: int = 7) -> int:
        """Clean up old completed jobs and their metrics"""
        cutoff_date = datetime.now().timestamp() - (older_than_days * 24 * 60 * 60)
        cleaned = 0
        
        # Clean up metrics for old jobs
        for job_id, metrics in list(self.active_metrics.items()):
            if metrics.end_time and metrics.end_time.timestamp() < cutoff_date:
                del self.active_metrics[job_id]
                cleaned += 1
        
        return cleaned 