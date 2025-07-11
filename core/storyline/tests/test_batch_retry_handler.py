"""Tests for the batch retry handler"""

import pytest
import time
from pathlib import Path
from typing import Dict, Any
from ..batch_retry_handler import (
    BatchRetryHandler,
    RetryStrategy,
    BatchMetadata,
    RetryStatistics
)

@pytest.fixture
def handler():
    """Create a batch retry handler for testing"""
    return BatchRetryHandler(max_retries=2, base_delay=0.1)

@pytest.fixture
def test_output_path(tmp_path):
    """Create a temporary output path"""
    return tmp_path / "test_output"

def test_execute_with_retry_success(handler):
    """Test successful operation execution"""
    def successful_operation():
        return "success"
    
    result = handler.execute_with_retry(successful_operation, "test_operation")
    assert result == "success"

def test_execute_with_retry_failure(handler):
    """Test failing operation with retries"""
    def failing_operation():
        raise ValueError("Test failure")
    
    with pytest.raises(ValueError, match="Test failure"):
        handler.execute_with_retry(failing_operation, "failing_test")

def test_handle_batch_failure(handler):
    """Test batch failure handling"""
    batch_id = "test_batch_1"
    failed_requests = ["gov1", "gov2", "gov3"]
    
    strategy = handler.handle_batch_failure(batch_id, failed_requests)
    
    assert isinstance(strategy, RetryStrategy)
    assert strategy.batch_id == batch_id
    assert strategy.failed_count == 3
    assert strategy.retry_candidates == failed_requests
    assert strategy.recovery_action == "create_retry_batch"
    assert strategy.priority == "normal"

def test_create_retry_batch(handler):
    """Test retry batch creation"""
    original_requests = [
        {"custom_id": "storyline-gov1", "data": "test1"},
        {"custom_id": "storyline-gov2", "data": "test2"},
        {"custom_id": "storyline-gov3", "data": "test3"}
    ]
    failed_governors = ["gov1", "gov3"]
    
    retry_batch = handler.create_retry_batch(original_requests, failed_governors)
    
    assert len(retry_batch) == 2
    assert retry_batch[0]["custom_id"] == "storyline-gov1-retry"
    assert retry_batch[1]["custom_id"] == "storyline-gov3-retry"

def test_save_and_recover_partial_results(handler, test_output_path):
    """Test saving and recovering partial results"""
    batch_id = "test_batch_2"
    successful_results = {
        "gov1": {"data": "test1"},
        "gov2": {"error": "failed"},
        "gov3": {"data": "test3"}
    }
    
    # Save results
    test_output_path.mkdir(parents=True)
    saved = handler.save_partial_results(batch_id, successful_results, test_output_path)
    assert saved is True
    
    # Recover results
    recovered = handler.recover_partial_results(test_output_path)
    assert len(recovered) == 2
    assert "gov1" in recovered
    assert "gov3" in recovered
    assert recovered["gov1"]["data"] == "test1"
    assert recovered["gov3"]["data"] == "test3"

def test_cleanup_partial_results(handler, test_output_path):
    """Test cleaning up partial results"""
    # Setup test files
    partial_dir = test_output_path / "partial_results"
    partial_dir.mkdir(parents=True)
    
    test_files = ["gov1_partial.json", "gov2_partial.json"]
    for file_name in test_files:
        (partial_dir / file_name).write_text('{"test": "data"}')
    
    # Clean up
    handler.cleanup_partial_results(test_output_path, ["gov1", "gov2"])
    
    # Verify cleanup
    remaining_files = list(partial_dir.glob("*_partial.json"))
    assert len(remaining_files) == 0

def test_get_retry_statistics(handler):
    """Test getting retry statistics"""
    # Setup some test data
    handler.failed_requests = {
        "batch1": ["gov1", "gov2"],
        "batch2": ["gov3"]
    }
    handler.partial_results = {
        "gov1": {"data": "test1"},
        "gov2": {"data": "test2"}
    }
    
    stats = handler.get_retry_statistics()
    
    assert isinstance(stats, RetryStatistics)
    assert stats.failed_batches == 2
    assert stats.total_failed_requests == 3
    assert stats.partial_results_saved == 2
    assert stats.retry_handler_active is True 