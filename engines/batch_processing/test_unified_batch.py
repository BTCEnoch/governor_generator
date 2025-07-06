#!/usr/bin/env python3
"""
Test Unified Batch Processor
Tests the core functionality without requiring API calls
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any

from unified_batch_processor import (
    UnifiedBatchProcessor,
    BatchJobConfig,
    BatchJobResult,
    BatchJobType,
    BatchJobStatus
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_batch_processor_initialization():
    """Test basic initialization"""
    logger.info("🧪 Testing UnifiedBatchProcessor initialization")
    
    processor = UnifiedBatchProcessor()
    
    # Check that jobs directory was created
    assert processor.jobs_directory.exists()
    assert processor.jobs_directory.is_dir()
    
    # Check that job handlers are registered
    assert len(processor.job_handlers) == 5
    assert BatchJobType.STORYLINE_GENERATION in processor.job_handlers
    assert BatchJobType.GOVERNOR_PROFILES in processor.job_handlers
    
    logger.info("✅ Initialization test passed")

def test_job_config_validation():
    """Test job configuration validation"""
    logger.info("🧪 Testing job configuration validation")
    
    processor = UnifiedBatchProcessor()
    
    # Test valid config
    valid_config = BatchJobConfig(
        job_type=BatchJobType.STORYLINE_GENERATION,
        job_id="test_job_001",
        input_data=[{"name": "ABRIOND", "element": "fire"}],
        output_directory=Path("test_output")
    )
    
    assert processor._validate_job_config(valid_config) == True
    
    # Test invalid config - empty job_id
    invalid_config = BatchJobConfig(
        job_type=BatchJobType.STORYLINE_GENERATION,
        job_id="",
        input_data=[{"name": "ABRIOND"}],
        output_directory=Path("test_output")
    )
    
    assert processor._validate_job_config(invalid_config) == False
    
    # Test invalid config - empty input_data
    invalid_config2 = BatchJobConfig(
        job_type=BatchJobType.STORYLINE_GENERATION,
        job_id="test_job_002",
        input_data=[],
        output_directory=Path("test_output")
    )
    
    assert processor._validate_job_config(invalid_config2) == False
    
    logger.info("✅ Validation test passed")

def test_storyline_request_generation():
    """Test storyline request generation"""
    logger.info("🧪 Testing storyline request generation")
    
    processor = UnifiedBatchProcessor()
    
    # Create test config
    config = BatchJobConfig(
        job_type=BatchJobType.STORYLINE_GENERATION,
        job_id="test_storyline",
        input_data=[
            {"name": "ABRIOND", "element": "fire"},
            {"name": "ZIRZIRD", "element": "water"}
        ],
        output_directory=Path("test_output")
    )
    
    # Generate requests
    requests = processor._create_storyline_requests(config)
    
    # Validate requests
    assert len(requests) == 2
    assert requests[0].custom_id == "storyline-ABRIOND"
    assert requests[1].custom_id == "storyline-ZIRZIRD"
    
    # Check request structure
    for request in requests:
        assert hasattr(request, 'custom_id')
        assert hasattr(request, 'prompt')
        assert hasattr(request, 'config')
        assert request.config.model == config.model
        assert "Governor" in request.prompt
    
    logger.info("✅ Storyline request generation test passed")

def test_job_state_persistence():
    """Test job state saving and loading"""
    logger.info("🧪 Testing job state persistence")
    
    processor = UnifiedBatchProcessor()
    
    # Create test job result
    job_result = BatchJobResult(
        job_id="test_persistence",
        status=BatchJobStatus.SUBMITTED,
        total_requests=5,
        completed_requests=2,
        failed_requests=1
    )
    
    # Save job state
    processor._save_job_state(job_result)
    
    # Load job state
    loaded_result = processor._load_job_state("test_persistence")
    
    # Validate loaded result
    assert loaded_result is not None
    assert loaded_result.job_id == "test_persistence"
    assert loaded_result.status == BatchJobStatus.SUBMITTED
    assert loaded_result.total_requests == 5
    assert loaded_result.completed_requests == 2
    assert loaded_result.failed_requests == 1
    
    logger.info("✅ Job state persistence test passed")

def test_job_listing():
    """Test job listing functionality"""
    logger.info("🧪 Testing job listing")
    
    processor = UnifiedBatchProcessor()
    
    # Create multiple test jobs
    job_results = [
        BatchJobResult(job_id="list_test_1", status=BatchJobStatus.PENDING),
        BatchJobResult(job_id="list_test_2", status=BatchJobStatus.PROCESSING),
        BatchJobResult(job_id="list_test_3", status=BatchJobStatus.COMPLETED)
    ]
    
    # Save job states
    for job_result in job_results:
        processor._save_job_state(job_result)
    
    # List jobs
    jobs = processor.list_jobs()
    
    # Validate job listing
    job_ids = [job.job_id for job in jobs]
    assert "list_test_1" in job_ids
    assert "list_test_2" in job_ids
    assert "list_test_3" in job_ids
    
    logger.info("✅ Job listing test passed")

def run_all_tests():
    """Run all tests"""
    logger.info("🚀 Starting Unified Batch Processor Tests")
    logger.info("=" * 60)
    
    try:
        test_batch_processor_initialization()
        test_job_config_validation()
        test_storyline_request_generation()
        test_job_state_persistence()
        test_job_listing()
        
        logger.info("=" * 60)
        logger.info("🎉 All tests passed! Unified Batch Processor is functional.")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1) 