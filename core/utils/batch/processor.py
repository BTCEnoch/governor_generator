"""
Batch Processing Utilities
Common functionality for batch operations
"""

import logging
from typing import Any, Dict, List, Optional, Union, Callable, TypeVar
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from ..data.validation import ValidationResult, validate_required_fields, validate_numeric_range
from ..custom_logging import get_batch_logger

T = TypeVar('T')
U = TypeVar('U')

@dataclass
class BatchConfig:
    """Configuration for batch processing"""
    job_id: str
    batch_size: int = 100
    max_retries: int = 3
    timeout: int = 300
    parallel: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BatchItem:
    """An item to be processed in a batch"""
    id: str
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BatchResult:
    """Result of processing a single batch item"""
    item_id: str
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    retries: int = 0
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BatchJobResult:
    """Result of processing an entire batch job"""
    job_id: str
    total_items: int
    successful_items: int = 0
    failed_items: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    results: List[BatchResult] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class BatchProcessor:
    """Processes items in batches"""
    def __init__(self, config: BatchConfig):
        """Initialize the batch processor"""
        # Validate configuration
        if not config.job_id:
            raise ValueError("Invalid configuration: job_id cannot be empty")
        if config.batch_size < 1:
            raise ValueError("Batch size must be positive")
        if config.max_retries < 0:
            raise ValueError("Max retries cannot be negative")
        if config.timeout < 0:
            raise ValueError("Timeout cannot be negative")
        
        self.config = config
        self.logger = get_batch_logger(config.job_id)
    
    def _create_batches(self, items: List[BatchItem]) -> List[List[BatchItem]]:
        """Split items into batches"""
        batches = []
        for i in range(0, len(items), self.config.batch_size):
            batch = items[i:i + self.config.batch_size]
            batches.append(batch)
        return batches
    
    def process_batch(
        self,
        items: List[BatchItem],
        processor: Callable[[BatchItem], Dict[str, Any]]
    ) -> BatchJobResult:
        """Process a batch of items"""
        job_result = BatchJobResult(
            job_id=self.config.job_id,
            total_items=len(items)
        )
        
        batches = self._create_batches(items)
        self.logger.info(f"Starting batch job {self.config.job_id}")
        
        for batch_idx, batch in enumerate(batches):
            for item in batch:
                result = self._process_item(item, processor)
                job_result.results.append(result)
                
                if result.success:
                    job_result.successful_items += 1
                else:
                    job_result.failed_items += 1
        
        job_result.end_time = datetime.now()
        duration = (job_result.end_time - job_result.start_time).total_seconds()
        self.logger.info(
            f"Completed batch job {self.config.job_id} in {duration:.2f}s: "
            f"{job_result.successful_items} succeeded, "
            f"{job_result.failed_items} failed"
        )
        return job_result
    
    def _process_item(
        self,
        item: BatchItem,
        processor: Callable[[BatchItem], Dict[str, Any]]
    ) -> BatchResult:
        """Process a single item with retries"""
        start_time = datetime.now()
        last_error = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                result = processor(item)
                duration = (datetime.now() - start_time).total_seconds()
                return BatchResult(
                    item_id=item.id,
                    success=True,
                    result=result,
                    retries=attempt,
                    duration=duration
                )
            except Exception as e:
                last_error = str(e)
                if attempt < self.config.max_retries:
                    self.logger.warning(
                        f"Retry {attempt + 1}/{self.config.max_retries} "
                        f"for item {item.id}: {str(e)}"
                    )
        
        # If we get here, all attempts failed
        self.logger.error(
            f"Failed to process item {item.id}: {last_error}"
        )
        duration = (datetime.now() - start_time).total_seconds()
        return BatchResult(
            item_id=item.id,
            success=False,
            error=last_error,
            retries=self.config.max_retries,
            duration=duration
        ) 