"""
Progress tracking utilities for batch operations.
"""

from typing import Dict, Optional
from datetime import datetime
import time

from core.utils.custom_logging import setup_logger

logger = setup_logger(__name__)

class ProgressTracker:
    """
    Tracks progress of batch operations with timing and completion estimates.
    """
    
    def __init__(self):
        self.jobs: Dict[str, Dict] = {}
        
    def start_job(self, job_id: str, total: int) -> None:
        """Start tracking a new job"""
        self.jobs[job_id] = {
            'total': total,
            'current': 0,
            'start_time': datetime.now(),
            'last_update': time.time(),
            'completed': False
        }
        logger.info(f"📊 Started tracking job {job_id} with {total} items")
        
    def update_progress(self, job_id: str, current: int) -> None:
        """Update progress for a job"""
        if job_id not in self.jobs:
            logger.warning(f"⚠️ Attempted to update unknown job {job_id}")
            return
            
        job = self.jobs[job_id]
        job['current'] = current
        now = time.time()
        
        # Calculate progress percentage
        progress = (current / job['total']) * 100 if job['total'] > 0 else 0
        
        # Calculate speed and ETA
        elapsed = now - job['last_update']
        if elapsed >= 1.0:  # Update every second
            items_per_sec = (current - job['current']) / elapsed
            remaining = job['total'] - current
            eta_seconds = remaining / items_per_sec if items_per_sec > 0 else 0
            
            logger.info(
                f"📈 Job {job_id}: {progress:.1f}% complete "
                f"({current}/{job['total']}) "
                f"ETA: {self._format_time(eta_seconds)}"
            )
            
            job['last_update'] = now
            
    def complete_job(self, job_id: str) -> None:
        """Mark a job as completed"""
        if job_id in self.jobs:
            job = self.jobs[job_id]
            job['completed'] = True
            duration = datetime.now() - job['start_time']
            logger.info(
                f"✅ Job {job_id} completed in {duration.total_seconds():.1f}s"
            )
            
    def get_progress(self, job_id: str) -> Optional[float]:
        """Get current progress percentage for a job"""
        if job_id in self.jobs:
            job = self.jobs[job_id]
            return (job['current'] / job['total']) * 100 if job['total'] > 0 else 0
        return None
        
    def _format_time(self, seconds: float) -> str:
        """Format seconds into human readable time"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.0f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h" 