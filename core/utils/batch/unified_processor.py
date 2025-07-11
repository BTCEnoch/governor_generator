"""
Unified Batch Processor
Combines functionality from all existing batch processors into a single, robust implementation
"""

from typing import List, Any, Dict, Optional
from dataclasses import dataclass
from queue import Queue, Empty
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class BatchConfig:
    """Configuration for batch processing"""
    max_retries: int = 3
    retry_delay: float = 1.0  # seconds
    batch_size: int = 100
    timeout: float = 30.0  # seconds
    parallel: bool = True
    validation_schema: Optional[Dict] = None

@dataclass
class BatchResult:
    """Results from batch processing"""
    successful: List[Any]
    failed: List[Any]
    stats: Dict[str, Any]
    start_time: datetime
    end_time: datetime
    total_processed: int

@dataclass
class RetryResult:
    """Results from retry operations"""
    recovered: List[Any]
    permanent_failures: List[Any]
    retry_count: int

@dataclass
class ProgressStatus:
    """Current progress of batch processing"""
    total_items: int
    processed: int
    successful: int
    failed: int
    in_progress: int
    percent_complete: float
    eta: Optional[float]

class ErrorHandler:
    """Handles errors during batch processing"""
    
    def __init__(self):
        self.error_log = []
        
    def handle_error(self, item: Any, error: Exception) -> bool:
        """
        Handle an error during processing
        Returns True if item should be retried, False if permanent failure
        """
        self.error_log.append({
            "item": item,
            "error": str(error),
            "timestamp": datetime.now(),
            "type": type(error).__name__
        })
        
        # Determine if error is recoverable
        if isinstance(error, (TimeoutError, ConnectionError)):
            return True
        return False

class UnifiedBatchProcessor:
    """
    Unified batch processing system combining features from all existing processors
    """
    def __init__(self, config: Optional[BatchConfig] = None):
        self.config = config or BatchConfig()
        self.job_queue = Queue()
        self.results = {}
        self.error_handler = ErrorHandler()
        self.start_time = None
        self.processed_count = 0
        
    async def process_batch(self, items: List[Any], config: Optional[BatchConfig] = None) -> BatchResult:
        """Process a batch of items with advanced error handling and retries"""
        if config:
            self.config = config
            
        self.start_time = datetime.now()
        
        # Initialize tracking
        successful = []
        failed = []
        stats = {
            "retries": 0,
            "validation_errors": 0,
            "processing_errors": 0
        }
        
        # Add items to queue
        for item in items:
            self.job_queue.put(item)
            
        # Process items
        if self.config.parallel:
            # Create processing tasks
            tasks = []
            for _ in range(min(self.config.batch_size, len(items))):
                tasks.append(asyncio.create_task(self._process_queue()))
            
            # Wait for all tasks to complete
            await asyncio.gather(*tasks)
        else:
            # Process sequentially
            while not self.job_queue.empty():
                await self._process_queue()
                
        # Collect results
        for item_id, result in self.results.items():
            if result.get('status') == 'success':
                successful.append(result)
            else:
                failed.append(result)
                stats["processing_errors"] += 1
                
        # Handle retries for failed items
        if failed and self.config.max_retries > 0:
            retry_result = await self.handle_retries(failed)
            successful.extend(retry_result.recovered)
            failed = retry_result.permanent_failures
            stats["retries"] = retry_result.retry_count
            
        end_time = datetime.now()
        
        return BatchResult(
            successful=successful,
            failed=failed,
            stats=stats,
            start_time=self.start_time,
            end_time=end_time,
            total_processed=len(items)
        )
    
    async def _process_queue(self) -> None:
        """Process items from the queue"""
        while not self.job_queue.empty():
            try:
                item = self.job_queue.get_nowait()
            except Empty:
                break
                
            try:
                # Process the item
                result = await self._process_item(item)
                self.results[id(item)] = result
                self.processed_count += 1
            except Exception as e:
                logger.error(f"Error processing item: {e}")
                if self.error_handler.handle_error(item, e):
                    # Will be retried
                    self.job_queue.put(item)
                else:
                    # Permanent failure
                    self.results[id(item)] = {"status": "failed", "error": str(e)}
                    
    async def _process_item(self, item: Any) -> Dict:
        """Process a single item"""
        # Validate if schema provided
        if self.config.validation_schema:
            if not self._validate_item(item):
                raise ValueError("Item failed validation")
                
        # Process item (to be implemented by subclasses)
        raise NotImplementedError("Subclasses must implement _process_item")
    
    def _validate_item(self, item: Any) -> bool:
        """Validate an item against the schema"""
        if not self.config.validation_schema:
            return True
            
        try:
            schema = self.config.validation_schema
            
            # Check required fields
            if "required" in schema:
                for field in schema["required"]:
                    if field not in item:
                        logger.error(f"Missing required field: {field}")
                        return False
                        
            # Check types
            if "types" in schema:
                for field, expected_type in schema["types"].items():
                    if field in item and not isinstance(item[field], expected_type):
                        logger.error(f"Invalid type for {field}: expected {expected_type}, got {type(item[field])}")
                        return False
                        
            return True
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
    
    async def handle_retries(self, failed_items: List[Any]) -> RetryResult:
        """Handle failed items with exponential backoff"""
        retry_count = 0
        recovered = []
        still_failed = failed_items
        
        for attempt in range(self.config.max_retries):
            if not still_failed:
                break
                
            # Exponential backoff
            await asyncio.sleep(self.config.retry_delay * (2 ** attempt))
            
            retry_count += 1
            retry_batch = still_failed
            still_failed = []
            
            # Try processing failed items again
            for item in retry_batch:
                try:
                    result = await self._process_item(item)
                    if result.get('status') == 'success':
                        recovered.append(result)
                    else:
                        still_failed.append(item)
                except Exception:
                    still_failed.append(item)
                    
        return RetryResult(
            recovered=recovered,
            permanent_failures=still_failed,
            retry_count=retry_count
        )
        
    def track_progress(self) -> ProgressStatus:
        """Get current processing progress"""
        if not self.start_time:
            return ProgressStatus(
                total_items=0,
                processed=0,
                successful=0,
                failed=0,
                in_progress=0,
                percent_complete=0.0,
                eta=None
            )
            
        total = self.job_queue.qsize() + self.processed_count
        successful = len([r for r in self.results.values() if r.get('status') == 'success'])
        failed = len([r for r in self.results.values() if r.get('status') == 'failed'])
        in_progress = total - successful - failed
        
        percent = (self.processed_count / total * 100) if total > 0 else 0
        
        # Calculate ETA
        if self.processed_count > 0:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            rate = self.processed_count / elapsed
            remaining = (total - self.processed_count) / rate if rate > 0 else None
        else:
            remaining = None
            
        return ProgressStatus(
            total_items=total,
            processed=self.processed_count,
            successful=successful,
            failed=failed,
            in_progress=in_progress,
            percent_complete=percent,
            eta=remaining
        ) 