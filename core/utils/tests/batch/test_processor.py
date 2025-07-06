"""
Tests for batch processing utilities
"""

import pytest
from datetime import datetime
from typing import List, Dict, Any
from core.utils.batch.processor import (
    BatchConfig,
    BatchItem,
    BatchResult,
    BatchJobResult,
    BatchProcessor
)

@pytest.fixture
def sample_config():
    """Create a sample batch configuration"""
    return BatchConfig(
        job_id="test_job",
        batch_size=2,
        max_retries=1,
        timeout=60,
        parallel=False
    )

@pytest.fixture
def sample_items():
    """Create sample batch items"""
    return [
        BatchItem(id="item1", data={"value": 1}),
        BatchItem(id="item2", data={"value": 2}),
        BatchItem(id="item3", data={"value": 3}),
        BatchItem(id="item4", data={"value": 4})
    ]

def test_batch_config():
    """Test batch configuration"""
    # Test default values
    config = BatchConfig(job_id="test")
    assert config.job_id == "test"
    assert config.batch_size == 100
    assert config.max_retries == 3
    assert config.timeout == 300
    assert config.parallel is False
    
    # Test custom values
    config = BatchConfig(
        job_id="custom",
        batch_size=50,
        max_retries=2,
        timeout=120,
        parallel=True
    )
    assert config.job_id == "custom"
    assert config.batch_size == 50
    assert config.max_retries == 2
    assert config.timeout == 120
    assert config.parallel is True

def test_batch_item():
    """Test batch item functionality"""
    # Test basic item
    item = BatchItem(id="test", data={"key": "value"})
    assert item.id == "test"
    assert item.data["key"] == "value"
    assert item.metadata == {}
    
    # Test with metadata
    item = BatchItem(
        id="test",
        data={"key": "value"},
        metadata={"source": "test"}
    )
    assert item.metadata["source"] == "test"

def test_batch_result():
    """Test batch result functionality"""
    # Test successful result
    result = BatchResult(
        item_id="test",
        success=True,
        result={"output": "value"},
        retries=0
    )
    assert result.item_id == "test"
    assert result.success is True
    assert result.result is not None and result.result["output"] == "value"
    assert result.error is None
    assert result.retries == 0
    
    # Test failed result
    result = BatchResult(
        item_id="test",
        success=False,
        error="Processing failed",
        retries=2
    )
    assert result.success is False
    assert result.result is None
    assert result.error == "Processing failed"
    assert result.retries == 2

def test_batch_job_result():
    """Test batch job result functionality"""
    start_time = datetime.now()
    
    # Test initial state
    job_result = BatchJobResult(
        job_id="test_job",
        total_items=4,
        successful_items=0,
        failed_items=0,
        start_time=start_time
    )
    assert job_result.job_id == "test_job"
    assert job_result.total_items == 4
    assert job_result.successful_items == 0
    assert job_result.failed_items == 0
    assert isinstance(job_result.start_time, datetime)
    assert job_result.end_time is None
    assert job_result.results == []
    
    # Test with results
    results = [
        BatchResult(item_id="item1", success=True),
        BatchResult(item_id="item2", success=False)
    ]
    job_result = BatchJobResult(
        job_id="test_job",
        total_items=2,
        successful_items=1,
        failed_items=1,
        start_time=start_time,
        results=results
    )
    assert job_result.successful_items == 1
    assert job_result.failed_items == 1
    assert len(job_result.results) == 2

def test_batch_processor_validation():
    """Test batch processor validation"""
    # Test empty job_id
    with pytest.raises(ValueError) as exc:
        BatchProcessor(BatchConfig(job_id=""))
    assert "job_id cannot be empty" in str(exc.value)
    
    # Test invalid batch_size
    with pytest.raises(ValueError) as exc:
        BatchProcessor(BatchConfig(job_id="test", batch_size=0))
    assert "Batch size must be positive" in str(exc.value)
    
    with pytest.raises(ValueError) as exc:
        BatchProcessor(BatchConfig(job_id="test", batch_size=-1))
    assert "Batch size must be positive" in str(exc.value)
    
    # Test invalid max_retries
    with pytest.raises(ValueError) as exc:
        BatchProcessor(BatchConfig(job_id="test", max_retries=-1))
    assert "Max retries cannot be negative" in str(exc.value)
    
    # Test invalid timeout
    with pytest.raises(ValueError) as exc:
        BatchProcessor(BatchConfig(job_id="test", timeout=-1))
    assert "Timeout cannot be negative" in str(exc.value)

def test_batch_processor_basic(sample_config, sample_items):
    """Test basic batch processor functionality"""
    processor = BatchProcessor(sample_config)
    
    def process_item(item: BatchItem) -> Dict[str, Any]:
        return {"result": item.data["value"] * 2}
    
    result = processor.process_batch(sample_items, process_item)
    
    assert result.job_id == "test_job"
    assert result.total_items == 4
    assert result.successful_items == 4
    assert result.failed_items == 0
    assert len(result.results) == 4
    assert all(r.success for r in result.results)
    
    # Check results are not None before accessing
    for i, r in enumerate(result.results):
        assert r.result is not None
        assert r.result["result"] == (i + 1) * 2

def test_batch_processor_error_handling(sample_config, sample_items):
    """Test batch processor error handling"""
    processor = BatchProcessor(sample_config)
    
    def failing_processor(item: BatchItem) -> Dict[str, Any]:
        if item.data["value"] % 2 == 0:
            raise ValueError(f"Cannot process even value: {item.data['value']}")
        return {"result": item.data["value"] * 2}
    
    result = processor.process_batch(sample_items, failing_processor)
    
    assert result.total_items == 4
    assert result.successful_items == 2
    assert result.failed_items == 2
    
    # Check successful items
    success_results = [r for r in result.results if r.success]
    assert len(success_results) == 2
    for r in success_results:
        assert r.result is not None
        assert r.result["result"] in [2, 6]  # Values 1 and 3 doubled
    
    # Check failed items
    failed_results = [r for r in result.results if not r.success]
    assert len(failed_results) == 2
    for r in failed_results:
        assert r.error is not None
        assert "Cannot process even value:" in r.error
    assert all(r.retries == sample_config.max_retries for r in failed_results)

def test_batch_processor_retries(sample_config):
    """Test batch processor retry functionality"""
    processor = BatchProcessor(sample_config)
    
    # Create an item that will fail once then succeed
    attempts = {"count": 0}
    
    def flaky_processor(item: BatchItem) -> Dict[str, Any]:
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise ValueError("First attempt fails")
        return {"result": "success"}
    
    result = processor.process_batch(
        [BatchItem(id="test", data={"value": 1})],
        flaky_processor
    )
    
    assert result.successful_items == 1
    assert result.failed_items == 0
    assert result.results[0].retries == 1
    assert result.results[0].result is not None
    assert result.results[0].result["result"] == "success"

def test_batch_processor_all_retries_fail(sample_config):
    """Test batch processor when all retries fail"""
    processor = BatchProcessor(sample_config)
    
    def always_fails(item: BatchItem) -> Dict[str, Any]:
        raise ValueError("Processing always fails")
    
    result = processor.process_batch(
        [BatchItem(id="test", data={"value": 1})],
        always_fails
    )
    
    assert result.successful_items == 0
    assert result.failed_items == 1
    assert result.results[0].retries == sample_config.max_retries
    assert result.results[0].error is not None
    assert "Processing always fails" in result.results[0].error 