"""
Progress Tracking Utilities
Common progress tracking and reporting functions
"""

import logging
import time
from typing import Any, Dict, List, Optional, Callable, Iterator
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@dataclass
class ProgressStats:
    """Statistics for progress tracking"""
    total: int
    completed: int
    failed: int
    start_time: datetime
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        return self.completed / self.total if self.total > 0 else 0
        
    @property
    def elapsed_time(self) -> timedelta:
        """Calculate elapsed time"""
        return datetime.now() - self.start_time
        
    @property
    def items_per_second(self) -> float:
        """Calculate processing rate"""
        elapsed = self.elapsed_time.total_seconds()
        return self.completed / elapsed if elapsed > 0 else 0

class ProgressTracker:
    """Track progress of batch operations"""
    
    def __init__(self, total: int, update_interval: float = 1.0):
        self.total = total
        self.completed = 0
        self.failed = 0
        self.start_time = datetime.now()
        self.last_update = time.time()
        self.update_interval = update_interval
        
    def update(self, success: bool = True) -> None:
        """
        Update progress
        
        Args:
            success: Whether the operation succeeded
        """
        if success:
            self.completed += 1
        else:
            self.failed += 1
            
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            self.log_progress()
            self.last_update = current_time
            
    def log_progress(self) -> None:
        """Log current progress"""
        stats = self.get_stats()
        logger.info(
            f"Progress: {stats.completed}/{stats.total} "
            f"({stats.success_rate:.1%}) - "
            f"Rate: {stats.items_per_second:.1f} items/sec"
        )
        
    def get_stats(self) -> ProgressStats:
        """Get current statistics"""
        return ProgressStats(
            total=self.total,
            completed=self.completed,
            failed=self.failed,
            start_time=self.start_time
        )

def track_progress(
    items: List[Any],
    operation: Callable[[Any], Any],
    update_interval: float = 1.0
) -> Iterator[Any]:
    """
    Generator that tracks progress while processing items
    
    Args:
        items: Items to process
        operation: Function to apply to each item
        update_interval: Progress update interval in seconds
        
    Yields:
        Operation results
    """
    tracker = ProgressTracker(len(items), update_interval)
    
    for item in items:
        try:
            result = operation(item)
            tracker.update(success=True)
            yield result
        except Exception as e:
            logger.error(f"Error processing item: {e}")
            tracker.update(success=False)
            
    # Final progress update
    tracker.log_progress() 