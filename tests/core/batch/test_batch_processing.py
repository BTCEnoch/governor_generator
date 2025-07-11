"""
Tests for the batch processing system
"""

import pytest
from pathlib import Path
from datetime import datetime
import json

from core.batch.models import (
    BatchJobType,
    BatchJobStatus,
    BatchJobConfig,
    BatchJobResult
)
from core.batch.processor import BatchProcessor
from core.batch.coordinator import BatchOperationsCoordinator
from core.utils.common.errors import BatchProcessingError

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory for test data"""
    return tmp_path / "test_data"

@pytest.fixture
def test_output_dir(tmp_path):
    """Create a temporary directory for test output"""
    return tmp_path / "test_output"

@pytest.fixture
def sample_governor_data():
    """Sample governor data for testing"""
    return [
        {
            "id": "GOV001",
            "name": "Test Governor 1",
            "traits": ["wise", "patient"],
            "mystical_attributes": {"wisdom": 0.8}
        },
        {
            "id": "GOV002",
            "name": "Test Governor 2",
            "traits": ["powerful", "decisive"],
            "mystical_attributes": {"power": 0.9}
        }
    ]

@pytest.fixture
def batch_processor(test_data_dir):
    """Create a BatchProcessor instance"""
    return BatchProcessor(test_data_dir)

@pytest.fixture
def batch_coordinator(test_data_dir):
    """Create a BatchOperationsCoordinator instance"""
    return BatchOperationsCoordinator(test_data_dir)

def test_create_batch_job(batch_processor, test_output_dir, sample_governor_data):
    """Test creating a new batch job"""
    config = BatchJobConfig(
        job_type=BatchJobType.STORYLINE_GENERATION,
        job_id="test_job_001",
        input_data=sample_governor_data,
        output_directory=test_output_dir,
        batch_size=1,
        total_items=len(sample_governor_data)
    )
    
    result = batch_processor.create_batch_job(config)
    
    assert result.job_id == "test_job_001"
    assert result.status == BatchJobStatus.PENDING
    assert result.total_items == len(sample_governor_data)

def test_process_batch_job(batch_processor, test_output_dir, sample_governor_data):
    """Test processing a batch job"""
    config = BatchJobConfig(
        job_type=BatchJobType.STORYLINE_GENERATION,
        job_id="test_job_002",
        input_data=sample_governor_data,
        output_directory=test_output_dir,
        batch_size=1,
        total_items=len(sample_governor_data)
    )
    
    batch_processor.create_batch_job(config)
    result = batch_processor.process_batch_job("test_job_002")
    
    assert result.status == BatchJobStatus.COMPLETED
    assert result.processed_items == len(sample_governor_data)
    assert len(result.error_messages) == 0

def test_batch_coordinator_create_storyline(
    batch_coordinator,
    test_data_dir,
    test_output_dir,
    sample_governor_data
):
    """Test creating a storyline batch through the coordinator"""
    # Create test governor files
    governor_files = []
    for gov_data in sample_governor_data:
        file_path = test_data_dir / f"{gov_data['id']}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(gov_data, f)
        governor_files.append(file_path)
    
    result = batch_coordinator.create_storyline_batch(
        governor_files=governor_files,
        output_dir=test_output_dir
    )
    
    assert result.status == BatchJobStatus.PENDING
    assert result.total_items == len(sample_governor_data)

def test_batch_coordinator_process_job(
    batch_coordinator,
    test_data_dir,
    test_output_dir,
    sample_governor_data
):
    """Test processing a job through the coordinator"""
    # Create test governor files
    governor_files = []
    for gov_data in sample_governor_data:
        file_path = test_data_dir / f"{gov_data['id']}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(gov_data, f)
        governor_files.append(file_path)
    
    # Create and process job
    result = batch_coordinator.create_storyline_batch(
        governor_files=governor_files,
        output_dir=test_output_dir,
        job_id="test_coord_job"
    )
    
    processed = batch_coordinator.process_job("test_coord_job")
    
    assert processed.status == BatchJobStatus.COMPLETED
    assert processed.processed_items == len(sample_governor_data)
    assert "duration" in processed.metrics
    assert "success_rate" in processed.metrics

def test_invalid_job_handling(batch_coordinator):
    """Test handling of invalid job IDs"""
    with pytest.raises(ValueError):
        batch_coordinator.process_job("nonexistent_job")

def test_batch_metrics(
    batch_coordinator,
    test_data_dir,
    test_output_dir,
    sample_governor_data
):
    """Test batch processing metrics"""
    # Create test governor files
    governor_files = []
    for gov_data in sample_governor_data:
        file_path = test_data_dir / f"{gov_data['id']}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(gov_data, f)
        governor_files.append(file_path)
    
    # Create and process job
    result = batch_coordinator.create_storyline_batch(
        governor_files=governor_files,
        output_dir=test_output_dir,
        job_id="test_metrics_job"
    )
    
    processed = batch_coordinator.process_job("test_metrics_job")
    status = batch_coordinator.get_job_status("test_metrics_job")
    
    assert status.metrics is not None
    assert float(status.metrics["success_rate"].rstrip("%")) == 100.0
    assert status.metrics["error_count"] == 0 