"""
Tests for the UnifiedBatchProcessor
"""

import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any

from .unified_processor import (
    UnifiedBatchProcessor,
    BatchConfig,
    BatchResult,
    RetryResult,
    ProgressStatus
)

class TestProcessor(UnifiedBatchProcessor):
    """Test implementation of UnifiedBatchProcessor"""
    
    async def _process_item(self, item: Any) -> Dict:
        """Test implementation that processes items based on their value"""
        if item == "fail":
            raise ValueError("Test failure")
        if item == "retry":
            raise TimeoutError("Test timeout")
        return {"status": "success", "value": item}

@pytest.fixture
def processor():
    """Create a test processor instance"""
    return TestProcessor()

@pytest.mark.asyncio
async def test_successful_processing():
    """Test successful batch processing"""
    processor = TestProcessor()
    items = ["item1", "item2", "item3"]
    
    result = await processor.process_batch(items)
    
    assert len(result.successful) == 3
    assert len(result.failed) == 0
    assert result.total_processed == 3
    assert isinstance(result.start_time, datetime)
    assert isinstance(result.end_time, datetime)

@pytest.mark.asyncio
async def test_failed_processing():
    """Test handling of failed items"""
    processor = TestProcessor()
    items = ["item1", "fail", "item3"]
    
    result = await processor.process_batch(items)
    
    assert len(result.successful) == 2
    assert len(result.failed) == 1
    assert result.stats["processing_errors"] > 0

@pytest.mark.asyncio
async def test_retry_handling():
    """Test retry mechanism for recoverable errors"""
    processor = TestProcessor()
    items = ["item1", "retry", "item3"]
    config = BatchConfig(max_retries=2, retry_delay=0.1)
    
    result = await processor.process_batch(items, config)
    
    assert len(result.successful) == 3
    assert len(result.failed) == 0
    assert result.stats["retries"] > 0

@pytest.mark.asyncio
async def test_parallel_processing():
    """Test parallel processing of items"""
    processor = TestProcessor()
    items = ["item1", "item2", "item3", "item4", "item5"]
    config = BatchConfig(parallel=True, batch_size=2)
    
    result = await processor.process_batch(items, config)
    
    assert len(result.successful) == 5
    assert result.total_processed == 5

@pytest.mark.asyncio
async def test_sequential_processing():
    """Test sequential processing of items"""
    processor = TestProcessor()
    items = ["item1", "item2", "item3"]
    config = BatchConfig(parallel=False)
    
    result = await processor.process_batch(items, config)
    
    assert len(result.successful) == 3
    assert result.total_processed == 3

@pytest.mark.asyncio
async def test_progress_tracking():
    """Test progress tracking functionality"""
    processor = TestProcessor()
    items = ["item1", "item2", "fail", "item4"]
    
    # Start processing
    process_task = asyncio.create_task(processor.process_batch(items))
    
    # Check progress
    await asyncio.sleep(0.1)  # Give some time for processing to start
    progress = processor.track_progress()
    
    assert isinstance(progress, ProgressStatus)
    assert progress.total_items == 4
    assert progress.percent_complete >= 0
    
    # Wait for completion
    await process_task

@pytest.mark.asyncio
async def test_validation():
    """Test item validation"""
    processor = TestProcessor()
    config = BatchConfig(
        validation_schema={
            "type": "object",
            "properties": {
                "value": {"type": "string"}
            }
        }
    )
    items = [{"value": "valid"}, {"value": 123}]  # Second item should fail validation
    
    result = await processor.process_batch(items, config)
    
    assert len(result.successful) == 1
    assert len(result.failed) == 1
    assert result.stats["validation_errors"] > 0

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handler functionality"""
    processor = TestProcessor()
    items = ["item1", "fail", "retry", "item4"]
    
    result = await processor.process_batch(items)
    
    assert len(processor.error_handler.error_log) > 0
    error_entry = processor.error_handler.error_log[0]
    assert "timestamp" in error_entry
    assert "error" in error_entry
    assert "type" in error_entry 