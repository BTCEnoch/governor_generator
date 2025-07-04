#!/usr/bin/env python3
"""
Batch Retry Handler - Handles retry logic and failure recovery for batch operations
Provides resilient batch processing with smart retry mechanisms
"""

import time
import logging
from typing import Dict, List, Optional, Callable, Any
from pathlib import Path
import json

class BatchRetryHandler:
    """Handles retry logic and failure recovery for batch operations"""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 30.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.failed_requests = {}
        self.partial_results = {}
        
        logging.info(f"🔄 Batch retry handler initialized (max_retries: {max_retries})")
    
    def execute_with_retry(self, operation: Callable, operation_name: str, *args, **kwargs) -> Any:
        """Execute an operation with exponential backoff retry"""
        
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    delay = self.base_delay * (2 ** (attempt - 1))  # Exponential backoff
                    logging.info(f"🔄 Retrying {operation_name} (attempt {attempt + 1}/{self.max_retries + 1}) after {delay}s delay")
                    time.sleep(delay)
                
                result = operation(*args, **kwargs)
                
                if attempt > 0:
                    logging.info(f"✅ {operation_name} succeeded on retry attempt {attempt + 1}")
                
                return result
                
            except Exception as e:
                last_exception = e
                logging.warning(f"⚠️ {operation_name} failed on attempt {attempt + 1}: {str(e)}")
                
                if attempt == self.max_retries:
                    logging.error(f"❌ {operation_name} failed after {self.max_retries + 1} attempts")
                    break
        
        # Ensure we always have an exception to raise
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError(f"Operation {operation_name} failed with no exception details")
    
    def handle_batch_failure(self, batch_id: str, failed_requests: List[str]) -> Dict[str, Any]:
        """Handle partial batch failure and prepare for retry"""
        
        logging.info(f"🚨 Handling batch failure for batch: {batch_id}")
        logging.info(f"   Failed requests: {len(failed_requests)}")
        
        # Store failed requests for retry
        if batch_id not in self.failed_requests:
            self.failed_requests[batch_id] = []
        
        self.failed_requests[batch_id].extend(failed_requests)
        
        # Prepare recovery strategy
        recovery_strategy = {
            "batch_id": batch_id,
            "failed_count": len(failed_requests),
            "retry_candidates": failed_requests,
            "recovery_action": "create_retry_batch",
            "priority": "high" if len(failed_requests) > 10 else "normal"
        }
        
        logging.info(f"🔧 Recovery strategy prepared: {recovery_strategy['recovery_action']}")
        
        return recovery_strategy
    
    def create_retry_batch(self, original_requests: List[Dict], failed_governor_names: List[str]) -> List[Dict]:
        """Create a new batch with only the failed requests"""
        
        retry_requests = []
        
        for request in original_requests:
            # Extract governor name from custom_id
            custom_id = request.get("custom_id", "")
            governor_name = custom_id.replace("storyline-", "")
            
            if governor_name in failed_governor_names:
                # Create new request with modified custom_id for tracking
                retry_request = request.copy()
                retry_request["custom_id"] = f"{custom_id}-retry"
                retry_requests.append(retry_request)
        
        logging.info(f"🔄 Created retry batch with {len(retry_requests)} requests")
        
        return retry_requests
    
    def save_partial_results(self, batch_id: str, successful_results: Dict[str, Dict], 
                            output_path: Path) -> bool:
        """Save partial results from a failed batch"""
        
        if not successful_results:
            logging.warning("⚠️ No successful results to save")
            return False
        
        # Create partial results directory
        partial_dir = output_path / "partial_results"
        partial_dir.mkdir(exist_ok=True)
        
        # Save individual successful results
        saved_count = 0
        
        for governor_name, storyline_data in successful_results.items():
            if "error" not in storyline_data:
                partial_file = partial_dir / f"{governor_name}_partial.json"
                
                try:
                    with open(partial_file, 'w', encoding='utf-8') as f:
                        json.dump(storyline_data, f, indent=2, ensure_ascii=False)
                    
                    saved_count += 1
                    logging.info(f"💾 Saved partial result for {governor_name}")
                    
                except Exception as e:
                    logging.error(f"❌ Failed to save partial result for {governor_name}: {e}")
        
        # Save batch metadata
        metadata = {
            "batch_id": batch_id,
            "partial_results_count": saved_count,
            "failed_governors": [name for name, data in successful_results.items() if "error" in data],
            "timestamp": time.time()
        }
        
        metadata_file = partial_dir / f"batch_{batch_id}_metadata.json"
        
        try:
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"❌ Failed to save batch metadata: {e}")
        
        logging.info(f"💾 Saved {saved_count} partial results from batch {batch_id}")
        return saved_count > 0
    
    def recover_partial_results(self, output_path: Path) -> Dict[str, Dict]:
        """Recover previously saved partial results"""
        
        partial_dir = output_path / "partial_results"
        
        if not partial_dir.exists():
            logging.info("ℹ️ No partial results directory found")
            return {}
        
        recovered_results = {}
        partial_files = list(partial_dir.glob("*_partial.json"))
        
        for partial_file in partial_files:
            governor_name = partial_file.stem.replace("_partial", "")
            
            try:
                with open(partial_file, 'r', encoding='utf-8') as f:
                    storyline_data = json.load(f)
                
                recovered_results[governor_name] = storyline_data
                logging.info(f"🔄 Recovered partial result for {governor_name}")
                
            except Exception as e:
                logging.error(f"❌ Failed to recover partial result for {governor_name}: {e}")
        
        if recovered_results:
            logging.info(f"🔄 Recovered {len(recovered_results)} partial results")
        
        return recovered_results
    
    def cleanup_partial_results(self, output_path: Path, governor_names: List[str]) -> None:
        """Clean up partial results after successful completion"""
        
        partial_dir = output_path / "partial_results"
        
        if not partial_dir.exists():
            return
        
        cleaned_count = 0
        
        for governor_name in governor_names:
            partial_file = partial_dir / f"{governor_name}_partial.json"
            
            if partial_file.exists():
                try:
                    partial_file.unlink()
                    cleaned_count += 1
                except Exception as e:
                    logging.warning(f"⚠️ Failed to clean up partial file for {governor_name}: {e}")
        
        if cleaned_count > 0:
            logging.info(f"🧹 Cleaned up {cleaned_count} partial result files")
    
    def get_retry_statistics(self) -> Dict[str, Any]:
        """Get statistics about retry operations"""
        
        total_failed_requests = sum(len(requests) for requests in self.failed_requests.values())
        
        return {
            "failed_batches": len(self.failed_requests),
            "total_failed_requests": total_failed_requests,
            "partial_results_saved": len(self.partial_results),
            "retry_handler_active": True
        }

def test_retry_handler():
    """Test the retry handler functionality"""
    
    logging.basicConfig(level=logging.INFO)
    
    handler = BatchRetryHandler(max_retries=2, base_delay=1.0)
    
    # Test successful operation
    def successful_operation():
        return "success"
    
    result = handler.execute_with_retry(successful_operation, "test_operation")
    print(f"✅ Successful operation result: {result}")
    
    # Test failing operation
    def failing_operation():
        raise Exception("Test failure")
    
    try:
        handler.execute_with_retry(failing_operation, "failing_test")
    except Exception as e:
        print(f"✅ Failing operation handled correctly: {e}")
    
    print("🎉 Retry handler test completed!")

if __name__ == "__main__":
    test_retry_handler() 