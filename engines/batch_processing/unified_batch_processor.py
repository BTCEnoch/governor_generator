#!/usr/bin/env python3
"""
Unified Batch Processor
Centralizes all batch operations for the Governor Generation system
"""

import json
import os
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import anthropic
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BatchJobType(str, Enum):
    """Enum for different types of batch jobs"""
    STORYLINES = "storylines"
    GOVERNOR_PROFILES = "governor_profiles"
    KNOWLEDGE_ENTRIES = "knowledge_entries"
    TRAIT_ASSIGNMENTS = "trait_assignments"

class BatchJobStatus(Enum):
    """Status of batch jobs"""
    PENDING = "pending"
    SUBMITTED = "submitted"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class BatchJobConfig:
    """Configuration for a batch job"""
    job_type: BatchJobType
    job_id: str
    input_data: Any
    output_directory: Path
    batch_size: int = 10
    max_retries: int = 3
    retry_delay: int = 5
    model: str = "claude-3-sonnet-20240229"
    max_tokens: int = 4096
    temperature: float = 0.7
    concurrent_requests: int = 5
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BatchJobResult:
    """Result of a batch job"""
    job_id: str
    status: BatchJobStatus
    total_requests: int = 0
    completed_requests: int = 0
    failed_requests: int = 0
    results: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    progress_log: List[str] = field(default_factory=list)

@dataclass
class BatchRequest:
    """Configuration for a single batch request"""
    request_id: str
    job_type: BatchJobType
    input_data: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    custom_id: Optional[str] = None
    prompt: Optional[str] = None
    config: Optional[BatchJobConfig] = None
    attempts: int = 0

class UnifiedBatchProcessor:
    """
    Unified batch processing system for all Governor Generation operations
    """
    
    def __init__(self, base_path: Path = Path(".")):
        """Initialize the unified batch processor"""
        self.base_path = Path(base_path)
        self.jobs_directory = self.base_path / "batch_jobs"
        self.jobs_directory.mkdir(exist_ok=True)
        
        # Initialize Anthropic client
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        
        # Job registry and handlers
        self.active_jobs: Dict[str, BatchJobConfig] = {}
        self.job_handlers: Dict[BatchJobType, Callable] = {
            BatchJobType.STORYLINES: self._create_storyline_requests,
            BatchJobType.GOVERNOR_PROFILES: self._create_governor_profile_requests,
            BatchJobType.KNOWLEDGE_ENTRIES: self._create_knowledge_entry_requests,
            BatchJobType.TRAIT_ASSIGNMENTS: self._create_trait_assignment_requests
        }
        
        logger.info("🚀 Unified Batch Processor initialized")
        logger.info(f"   Jobs directory: {self.jobs_directory}")
        logger.info(f"   Supported job types: {len(self.job_handlers)}")
    
    def create_batch_job(self, config: BatchJobConfig) -> BatchJobResult:
        """Create and submit a new batch job"""
        
        logger.info(f"📦 Creating {config.job_type.value} batch job: {config.job_id}")
        
        # Validate job configuration
        if not self._validate_job_config(config):
            return BatchJobResult(
                job_id=config.job_id,
                status=BatchJobStatus.FAILED,
                error_message="Invalid job configuration"
            )
        
        # Create batch requests
        handler = self.job_handlers.get(config.job_type)
        if not handler:
            return BatchJobResult(
                job_id=config.job_id,
                status=BatchJobStatus.FAILED,
                error_message=f"No handler for job type: {config.job_type.value}"
            )
        
        try:
            batch_requests = handler(config)
            
            # Store job configuration
            self.active_jobs[config.job_id] = config
            
            # Create job result
            result = BatchJobResult(
                job_id=config.job_id,
                status=BatchJobStatus.SUBMITTED,
                total_requests=len(batch_requests),
                start_time=datetime.now()
            )
            
            # Save job state
            self._save_job_state(result)
            
            logger.info(f"✅ Batch job {config.job_id} created with {len(batch_requests)} requests")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to create batch job {config.job_id}: {str(e)}")
            return BatchJobResult(
                job_id=config.job_id,
                status=BatchJobStatus.FAILED,
                error_message=str(e)
            )
    
    def process_batch_job(self, job_id: str) -> BatchJobResult:
        """Process a batch job using concurrent requests"""
        
        logger.info(f"🔄 Processing batch job: {job_id}")
        
        # Load job state
        job_result = self._load_job_state(job_id)
        if not job_result:
            return BatchJobResult(
                job_id=job_id,
                status=BatchJobStatus.FAILED,
                error_message="Job not found"
            )
        
        # Get job configuration
        config = self.active_jobs.get(job_id)
        if not config:
            return BatchJobResult(
                job_id=job_id,
                status=BatchJobStatus.FAILED,
                error_message="Job configuration not found"
            )
        
        # Get batch requests
        handler = self.job_handlers.get(config.job_type)
        if not handler:
            return BatchJobResult(
                job_id=job_id,
                status=BatchJobStatus.FAILED,
                error_message=f"No handler for job type: {config.job_type.value}"
            )
        
        try:
            batch_requests = handler(config)
            
            # Update job status
            job_result.status = BatchJobStatus.PROCESSING
            job_result.total_requests = len(batch_requests)
            self._save_job_state(job_result)
            
            # Process requests concurrently
            results = self._process_concurrent_requests(batch_requests, config, job_result)
            
            # Update final results
            job_result.results = results
            job_result.completed_requests = len([r for r in results.values() if r.get('status') == 'success'])
            job_result.failed_requests = len([r for r in results.values() if r.get('status') == 'error'])
            job_result.status = BatchJobStatus.COMPLETED
            job_result.end_time = datetime.now()
            
            # Save output files
            self._save_batch_output(job_id, config, results)
            
            # Save final state
            self._save_job_state(job_result)
            
            logger.info(f"✅ Batch job {job_id} completed: {job_result.completed_requests} success, {job_result.failed_requests} failed")
            return job_result
            
        except Exception as e:
            logger.error(f"❌ Failed to process batch job {job_id}: {str(e)}")
            job_result.status = BatchJobStatus.FAILED
            job_result.error_message = str(e)
            job_result.end_time = datetime.now()
            self._save_job_state(job_result)
            return job_result
    
    def _process_concurrent_requests(self, batch_requests: List[BatchRequest], config: BatchJobConfig, job_result: BatchJobResult) -> Dict[str, Any]:
        """Process batch requests concurrently"""
        
        results = {}
        
        # Use ThreadPoolExecutor for concurrent requests
        with ThreadPoolExecutor(max_workers=config.concurrent_requests) as executor:
            # Submit all requests
            future_to_request = {
                executor.submit(self._process_request, request, config): request
                for request in batch_requests
            }
            
            # Process completed requests
            for future in as_completed(future_to_request):
                request = future_to_request[future]
                
                try:
                    result = future.result()
                    results[request.custom_id] = result
                    
                    # Update progress
                    job_result.completed_requests = len([r for r in results.values() if r.get('status') == 'success'])
                    job_result.failed_requests = len([r for r in results.values() if r.get('status') == 'error'])
                    
                    progress_msg = f"Progress: {len(results)}/{len(batch_requests)} requests completed"
                    job_result.progress_log.append(progress_msg)
                    logger.info(f"📊 {job_result.job_id}: {progress_msg}")
                    
                    # Save intermediate progress
                    if len(results) % 10 == 0:  # Save every 10 completions
                        self._save_job_state(job_result)
                    
                except Exception as e:
                    logger.error(f"❌ Request {request.custom_id} failed: {str(e)}")
                    results[request.custom_id] = {
                        'status': 'error',
                        'error': str(e),
                        'custom_id': request.custom_id
                    }
        
        return results
    
    def _process_request(self, request: BatchRequest, config: BatchJobConfig) -> Dict[str, Any]:
        """Process a single batch request"""
        try:
            # Increment attempt counter
            request.attempts += 1
            
            # Create messages for the request
            messages = []
            if request.prompt:
                messages.append({"role": "system", "content": request.prompt})
            messages.append({"role": "user", "content": json.dumps(request.input_data)})
            
            # Make API call with type-safe messages
            response = self.client.messages.create(
                model=config.model,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                messages=messages
            )
            
            # Extract content from response
            # Convert all content to string to handle any response type
            content = " ".join(str(message) for message in response.content)
            
            return {
                "status": "success",
                "request_id": request.request_id,
                "response": content,
                "metadata": request.metadata
            }
            
        except Exception as e:
            logger.error(f"❌ Request {request.request_id} failed: {str(e)}")
            
            # Check if we should retry
            if request.attempts < config.max_retries:
                logger.info(f"⏳ Retrying request {request.request_id} in {config.retry_delay} seconds...")
                time.sleep(config.retry_delay)
                return self._process_request(request, config)
            
            return {
                "status": "error",
                "request_id": request.request_id,
                "error": str(e),
                "metadata": request.metadata
            }
    
    def get_job_status(self, job_id: str) -> Optional[BatchJobResult]:
        """Get current status of a batch job"""
        return self._load_job_state(job_id)
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a batch job"""
        
        logger.info(f"🛑 Cancelling batch job: {job_id}")
        
        job_result = self._load_job_state(job_id)
        if not job_result:
            return False
        
        try:
            # Update job status
            job_result.status = BatchJobStatus.CANCELLED
            job_result.end_time = datetime.now()
            self._save_job_state(job_result)
            
            # Remove from active jobs
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
            
            logger.info(f"✅ Job {job_id} cancelled successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to cancel job {job_id}: {str(e)}")
            return False
    
    def list_jobs(self) -> List[BatchJobResult]:
        """List all batch jobs"""
        jobs = []
        
        for job_file in self.jobs_directory.glob("*.json"):
            try:
                job_result = self._load_job_state(job_file.stem)
                if job_result:
                    jobs.append(job_result)
            except Exception as e:
                logger.warning(f"⚠️ Could not load job {job_file.stem}: {str(e)}")
        
        return jobs
    
    # Job-specific request handlers
    def _create_storyline_requests(self, config: BatchJobConfig) -> List[BatchRequest]:
        """Create batch requests for storyline generation"""
        requests = []
        for i, data in enumerate(config.input_data):
            request = BatchRequest(
                request_id=f"{config.job_id}_storyline_{i}",
                job_type=BatchJobType.STORYLINES,
                input_data=data,
                metadata={"index": i}
            )
            requests.append(request)
        return requests
    
    def _create_governor_profile_requests(self, config: BatchJobConfig) -> List[BatchRequest]:
        """Create batch requests for governor profile generation"""
        requests = []
        for i, data in enumerate(config.input_data):
            request = BatchRequest(
                request_id=f"{config.job_id}_governor_{i}",
                job_type=BatchJobType.GOVERNOR_PROFILES,
                input_data=data,
                metadata={"index": i}
            )
            requests.append(request)
        return requests
    
    def _create_knowledge_entry_requests(self, config: BatchJobConfig) -> List[BatchRequest]:
        """Create batch requests for knowledge entry generation"""
        requests = []
        for i, data in enumerate(config.input_data):
            request = BatchRequest(
                request_id=f"{config.job_id}_knowledge_{i}",
                job_type=BatchJobType.KNOWLEDGE_ENTRIES,
                input_data=data,
                metadata={"index": i}
            )
            requests.append(request)
        return requests
    
    def _create_trait_assignment_requests(self, config: BatchJobConfig) -> List[BatchRequest]:
        """Create batch requests for trait assignment generation"""
        requests = []
        for i, data in enumerate(config.input_data):
            request = BatchRequest(
                request_id=f"{config.job_id}_trait_{i}",
                job_type=BatchJobType.TRAIT_ASSIGNMENTS,
                input_data=data,
                metadata={"index": i}
            )
            requests.append(request)
        return requests
    
    # Helper methods for batch operations
    def _validate_job_config(self, config: BatchJobConfig) -> bool:
        """Validate job configuration"""
        try:
            # Basic validation
            if not config.job_id:
                logger.error("Job ID is required")
                return False
            
            if not config.input_data:
                logger.error("Input data is required")
                return False
            
            if config.batch_size <= 0:
                logger.error("Batch size must be positive")
                return False
            
            if config.max_retries < 0:
                logger.error("Max retries cannot be negative")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return False
    
    def _save_job_state(self, job_result: BatchJobResult) -> None:
        """Save job state to disk"""
        try:
            job_file = self.jobs_directory / f"{job_result.job_id}.json"
            
            # Convert to dict for serialization
            job_dict = {
                "job_id": job_result.job_id,
                "status": job_result.status.value,
                "total_requests": job_result.total_requests,
                "completed_requests": job_result.completed_requests,
                "failed_requests": job_result.failed_requests,
                "results": job_result.results,
                "error_message": job_result.error_message,
                "start_time": job_result.start_time.isoformat() if job_result.start_time else None,
                "end_time": job_result.end_time.isoformat() if job_result.end_time else None,
                "progress_log": job_result.progress_log
            }
            
            with open(job_file, 'w') as f:
                json.dump(job_dict, f, indent=2)
                
        except Exception as e:
            logger.error(f"❌ Failed to save job state for {job_result.job_id}: {str(e)}")
    
    def _load_job_state(self, job_id: str) -> Optional[BatchJobResult]:
        """Load job state from disk"""
        try:
            job_file = self.jobs_directory / f"{job_id}.json"
            
            if not job_file.exists():
                return None
            
            with open(job_file, 'r') as f:
                job_dict = json.load(f)
            
            # Convert back to BatchJobResult
            return BatchJobResult(
                job_id=job_dict["job_id"],
                status=BatchJobStatus(job_dict["status"]),
                total_requests=job_dict.get("total_requests", 0),
                completed_requests=job_dict.get("completed_requests", 0),
                failed_requests=job_dict.get("failed_requests", 0),
                results=job_dict.get("results"),
                error_message=job_dict.get("error_message"),
                start_time=datetime.fromisoformat(job_dict["start_time"]) if job_dict.get("start_time") else None,
                end_time=datetime.fromisoformat(job_dict["end_time"]) if job_dict.get("end_time") else None,
                progress_log=job_dict.get("progress_log", [])
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to load job state for {job_id}: {str(e)}")
            return None
    
    def _save_batch_output(self, job_id: str, config: BatchJobConfig, results: Dict[str, Any]) -> None:
        """Save batch results to disk"""
        try:
            output_dir = config.output_directory
            output_dir.mkdir(exist_ok=True)
            
            for custom_id, result in results.items():
                status = result.get('status')
                content = result.get('content')
                raw_content = result.get('raw_content')
                
                if status == 'success':
                    if isinstance(content, dict):
                        filename = f"{custom_id}_content.json"
                        with open(output_dir / filename, 'w') as f:
                            json.dump(content, f)
                    else:
                        filename = f"{custom_id}_content.txt"
                        with open(output_dir / filename, 'w') as f:
                            f.write(content)
                elif status == 'error':
                    filename = f"{custom_id}_error.txt"
                    with open(output_dir / filename, 'w') as f:
                        f.write(f"Error: {raw_content}\n{result['error']}")
                else:
                    filename = f"{custom_id}_unknown_status.txt"
                    with open(output_dir / filename, 'w') as f:
                        f.write(f"Unknown status: {status}\n{raw_content}")
            
            logger.info(f"✅ Batch job {job_id} completed: {len(results)} results saved")
            
        except Exception as e:
            logger.error(f"❌ Failed to save batch output for {job_id}: {str(e)}")

# Convenience functions for common operations
def create_storyline_batch(governor_data: List[Dict[str, Any]], 
                         output_dir: Path = Path("storyline_output"),
                         job_id: Optional[str] = None) -> BatchJobResult:
    """Convenience function to create storyline batch job"""
    
    if job_id is None:
        job_id = f"storyline_batch_{int(time.time())}"
    
    processor = UnifiedBatchProcessor()
    
    config = BatchJobConfig(
        job_type=BatchJobType.STORYLINES,
        job_id=job_id,
        input_data=governor_data,
        output_directory=output_dir,
        metadata={}
    )
    
    return processor.create_batch_job(config)

def monitor_job(job_id: str) -> BatchJobResult:
    """Convenience function to monitor a job"""
    processor = UnifiedBatchProcessor()
    return processor.process_batch_job(job_id)

def list_all_jobs() -> List[BatchJobResult]:
    """Convenience function to list all jobs"""
    processor = UnifiedBatchProcessor()
    return processor.list_jobs()

if __name__ == "__main__":
    # Example usage
    logger.info("🧪 Testing Unified Batch Processor")
    
    # Create a test processor
    processor = UnifiedBatchProcessor()
    
    # List existing jobs
    jobs = processor.list_jobs()
    logger.info(f"📋 Found {len(jobs)} existing jobs")
    
    for job in jobs:
        logger.info(f"   - {job.job_id}: {job.status.value}")
    
    logger.info("✅ Unified Batch Processor test complete") 