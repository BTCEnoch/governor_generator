#!/usr/bin/env python3
"""
Batch Governor Review System
===========================

This system creates and manages batch API requests for all 90 remaining governors
to review their dossiers and confirm their personality traits and knowledge base selections.

Uses Anthropic's batch API to process governors efficiently with proper monitoring.
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import time
import uuid

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

# Import existing governor review system components
from ai_governor_review_system import (
    AIGovernorReviewSystem, 
    GovernorPersona,
    ReviewChoice,
    GovernorReviewSession
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/batch_governor_review.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

@dataclass
class BatchRequest:
    """Represents a single request in the batch."""
    custom_id: str
    governor_name: str
    category: str
    model: str
    max_tokens: int
    prompt: str
    
    def to_anthropic_format(self) -> Dict[str, Any]:
        """Convert to Anthropic batch API format."""
        return {
            "custom_id": self.custom_id,
            "params": {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": self.prompt
                    }
                ]
            }
        }

@dataclass
class BatchJob:
    """Represents a complete batch job."""
    batch_id: str
    job_name: str
    created_at: str
    total_requests: int
    governors: List[str]
    categories: List[str]
    status: str
    batch_response: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "batch_id": self.batch_id,
            "job_name": self.job_name,
            "created_at": self.created_at,
            "total_requests": self.total_requests,
            "governors": self.governors,
            "categories": self.categories,
            "status": self.status,
            "batch_response": self.batch_response
        }

class BatchGovernorReviewSystem:
    """Manages batch processing of governor reviews."""
    
    def __init__(self, 
                 model: str = "claude-3-5-sonnet-20241022",
                 verbose: bool = False,
                 dry_run: bool = False):
        """Initialize the batch processing system."""
        
        self.model = model
        self.verbose = verbose
        self.dry_run = dry_run
        self.logger = logging.getLogger("BatchGovernorReviewSystem")
        
        # Initialize paths
        self.project_root = Path(__file__).parent.parent
        self.batch_jobs_dir = self.project_root / "batch_jobs"
        self.batch_results_dir = self.project_root / "batch_results"
        
        # Create directories
        self.batch_jobs_dir.mkdir(exist_ok=True)
        self.batch_results_dir.mkdir(exist_ok=True)
        
        # Initialize the base review system
        self.review_system = AIGovernorReviewSystem(
            api_provider="anthropic",
            model=model,
            verbose=verbose,
            dry_run=dry_run
        )
        
        # Categories to review for each governor
        self.review_categories = [
            "knowledge_base",
            "virtues_pool",
            "flaws_pool", 
            "approaches",
            "tones",
            "motive_alignment",
            "role_archtypes",
            "orientation_io",
            "polarity_cd",
            "self_regard_options"
        ]
        
        self.logger.info(f"Batch Governor Review System initialized")
        self.logger.info(f"Model: {model}, Dry Run: {dry_run}")
        
        # Initialize API client
        self.anthropic_client = None
        if not self.dry_run:
            self._initialize_api_client()
    
    def _initialize_api_client(self):
        """Initialize the Anthropic API client."""
        try:
            import anthropic
            self.anthropic_client = anthropic.Anthropic()
            self.logger.info("Anthropic API client initialized for batch processing")
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
        except Exception as e:
            self.logger.error(f"Failed to initialize Anthropic client: {e}")
            raise
    
    def get_governors_needing_review(self) -> List[str]:
        """Get list of governors that need review (check individual dossier files)."""
        try:
            # Check individual governor dossier files in governor_output
            governor_output_dir = self.project_root / "governor_output"
            
            if not governor_output_dir.exists():
                self.logger.error("Governor output directory not found")
                return []
            
            governors_needing_review = []
            processed_governors = []
            
            # Get all governor JSON files
            for dossier_file in governor_output_dir.glob("*.json"):
                governor_name = dossier_file.stem  # Filename without .json extension
                
                try:
                    with open(dossier_file, 'r', encoding='utf-8') as f:
                        dossier_data = json.load(f)
                    
                    # Check if governor has been batch reviewed
                    review_metadata = dossier_data.get("review_metadata", {})
                    review_method = review_metadata.get("review_method", "")
                    
                    if review_method == "batch_api_review":
                        processed_governors.append(governor_name)
                    else:
                        governors_needing_review.append(governor_name)
                        
                except Exception as e:
                    self.logger.warning(f"Error reading dossier for {governor_name}: {e}")
                    # Include in needing review if can't read
                    governors_needing_review.append(governor_name)
            
            # Sort for consistent ordering
            governors_needing_review.sort()
            processed_governors.sort()
            
            self.logger.info(f"Found {len(governors_needing_review)} governors needing review")
            self.logger.info(f"Found {len(processed_governors)} already processed governors")
            
            if self.verbose:
                self.logger.info(f"Already processed: {processed_governors}")
                self.logger.info(f"Need processing: {governors_needing_review[:10]}...")  # Show first 10
            
            return governors_needing_review
            
        except Exception as e:
            self.logger.error(f"Error getting governors needing review: {e}")
            return []
    
    def create_batch_requests(self, governors: List[str], categories: Optional[List[str]] = None) -> List[BatchRequest]:
        """Create batch requests for the specified governors and categories."""
        
        if categories is None:
            categories = self.review_categories
            
        batch_requests = []
        failed_requests = []
        
        self.logger.info(f"Creating batch requests for {len(governors)} governors, {len(categories)} categories each")
        
        for governor_name in governors:
            try:
                # Create governor persona
                persona = self.review_system.create_governor_persona(governor_name)
                
                if not persona:
                    self.logger.warning(f"Could not create persona for {governor_name}")
                    failed_requests.append(f"{governor_name} - persona creation failed")
                    continue
                
                # Create request for each category
                for category in categories:
                    try:
                        # Generate prompt for this governor and category
                        prompt = self.review_system.generate_review_prompt(persona, category)
                        
                        # Create custom ID
                        custom_id = f"{governor_name}_{category}_{uuid.uuid4().hex[:8]}"
                        
                        # Determine max tokens based on category
                        max_tokens = 2000 if category == "knowledge_base" else 1000
                        
                        # Create batch request
                        batch_request = BatchRequest(
                            custom_id=custom_id,
                            governor_name=governor_name,
                            category=category,
                            model=self.model,
                            max_tokens=max_tokens,
                            prompt=prompt
                        )
                        
                        batch_requests.append(batch_request)
                        
                        if self.verbose:
                            self.logger.info(f"Created request: {custom_id}")
                            
                    except Exception as e:
                        error_msg = f"{governor_name}_{category} - prompt generation failed: {e}"
                        self.logger.error(error_msg)
                        failed_requests.append(error_msg)
                        
            except Exception as e:
                error_msg = f"{governor_name} - persona creation failed: {e}"
                self.logger.error(error_msg)
                failed_requests.append(error_msg)
        
        self.logger.info(f"Created {len(batch_requests)} batch requests")
        if failed_requests:
            self.logger.warning(f"Failed to create {len(failed_requests)} requests")
            if self.verbose:
                for failure in failed_requests:
                    self.logger.warning(f"  - {failure}")
        
        return batch_requests
    
    def save_batch_requests(self, batch_requests: List[BatchRequest], filename: str) -> bool:
        """Save batch requests to a file in Anthropic format."""
        try:
            # Convert to Anthropic format
            anthropic_requests = [req.to_anthropic_format() for req in batch_requests]
            
            # Save to file
            batch_file = self.batch_jobs_dir / filename
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(anthropic_requests, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved {len(batch_requests)} batch requests to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving batch requests: {e}")
            return False
    
    def submit_batch_job(self, batch_requests: List[BatchRequest], job_name: str) -> Optional[BatchJob]:
        """Submit a batch job to Anthropic."""
        
        if self.dry_run:
            self.logger.info(f"DRY RUN: Would submit batch job with {len(batch_requests)} requests")
            
            # Create mock batch job
            mock_batch_job = BatchJob(
                batch_id=f"mock_batch_{uuid.uuid4().hex[:8]}",
                job_name=job_name,
                created_at=datetime.now().isoformat(),
                total_requests=len(batch_requests),
                governors=[req.governor_name for req in batch_requests],
                categories=[req.category for req in batch_requests],
                status="mock_submitted"
            )
            
            # Save batch job info
            self._save_batch_job_info(mock_batch_job)
            return mock_batch_job
        
        try:
            if not self.anthropic_client:
                self.logger.error("Anthropic client not initialized")
                return None
            
            # Convert to Anthropic format and create Request objects
            from anthropic.types.messages.batch_create_params import Request
            from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
            
            anthropic_requests = []
            for req in batch_requests:
                request_param = Request(
                    custom_id=req.custom_id,
                    params=MessageCreateParamsNonStreaming(
                        model=req.model,
                        max_tokens=req.max_tokens,
                        messages=[
                            {
                                "role": "user",
                                "content": req.prompt
                            }
                        ]
                    )
                )
                anthropic_requests.append(request_param)
            
            self.logger.info(f"Submitting batch job '{job_name}' with {len(batch_requests)} requests")
            
            # Submit to Anthropic
            batch_response = self.anthropic_client.messages.batches.create(
                requests=anthropic_requests
            )
            
            # Create batch job record
            batch_job = BatchJob(
                batch_id=batch_response.id,
                job_name=job_name,
                created_at=datetime.now().isoformat(),
                total_requests=len(batch_requests),
                governors=list(set([req.governor_name for req in batch_requests])),
                categories=list(set([req.category for req in batch_requests])),
                status=batch_response.processing_status,
                batch_response=batch_response.model_dump() if hasattr(batch_response, 'model_dump') else dict(batch_response)
            )
            
            # Save batch job info
            self._save_batch_job_info(batch_job)
            
            self.logger.info(f"Batch job submitted successfully: {batch_job.batch_id}")
            return batch_job
            
        except Exception as e:
            self.logger.error(f"Error submitting batch job: {e}")
            return None
    
    def _save_batch_job_info(self, batch_job: BatchJob) -> bool:
        """Save batch job information to file."""
        try:
            job_file = self.batch_jobs_dir / f"{batch_job.batch_id}.json"
            with open(job_file, 'w', encoding='utf-8') as f:
                json.dump(batch_job.to_dict(), f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved batch job info: {batch_job.batch_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving batch job info: {e}")
            return False
    
    def check_batch_status(self, batch_id: str) -> Optional[str]:
        """Check the status of a batch job."""
        
        if self.dry_run:
            self.logger.info(f"DRY RUN: Would check status of batch {batch_id}")
            return "mock_completed"
        
        try:
            if not self.anthropic_client:
                self.logger.error("Anthropic client not initialized")
                return None
            
            batch_response = self.anthropic_client.messages.batches.retrieve(batch_id)
            status = batch_response.processing_status
            
            self.logger.info(f"Batch {batch_id} status: {status}")
            return status
            
        except Exception as e:
            self.logger.error(f"Error checking batch status: {e}")
            return None
    
    def monitor_batch_job(self, batch_id: str, check_interval: int = 300) -> bool:
        """Monitor a batch job until completion."""
        
        self.logger.info(f"Monitoring batch job {batch_id}, checking every {check_interval} seconds")
        
        while True:
            status = self.check_batch_status(batch_id)
            
            if status is None:
                self.logger.error(f"Failed to check status for batch {batch_id}")
                return False
            
            if status == "completed" or status == "mock_completed":
                self.logger.info(f"Batch job {batch_id} completed successfully!")
                return True
            
            elif status == "failed":
                self.logger.error(f"Batch job {batch_id} failed!")
                return False
            
            elif status in ["in_progress", "processing", "mock_submitted"]:
                self.logger.info(f"Batch job {batch_id} still {status}...")
                
                if not self.dry_run:
                    time.sleep(check_interval)
                else:
                    # In dry run, just simulate completion
                    self.logger.info("DRY RUN: Simulating batch completion")
                    return True
            
            else:
                self.logger.warning(f"Unknown batch status: {status}")
                if not self.dry_run:
                    time.sleep(check_interval)
                else:
                    return True
    
    def create_test_batch(self, num_governors: int = 3) -> List[BatchRequest]:
        """Create a small test batch for validation."""
        
        governors = self.get_governors_needing_review()
        
        if not governors:
            self.logger.error("No governors available for testing")
            return []
        
        # Use first N governors for testing
        test_governors = governors[:num_governors]
        
        # Use subset of categories for testing
        test_categories = ["knowledge_base", "virtues_pool", "tones"]
        
        self.logger.info(f"Creating test batch with {len(test_governors)} governors, {len(test_categories)} categories")
        
        return self.create_batch_requests(test_governors, test_categories)
    
    def prepare_full_batch(self) -> List[BatchRequest]:
        """Prepare the full batch for all governors needing review."""
        
        governors = self.get_governors_needing_review()
        
        if not governors:
            self.logger.error("No governors need review")
            return []
        
        self.logger.info(f"Creating full batch for {len(governors)} governors")
        
        return self.create_batch_requests(governors, self.review_categories)
    
    def get_batch_summary(self, batch_requests: List[BatchRequest]) -> Dict[str, Any]:
        """Get a summary of the batch requests."""
        
        governors = list(set([req.governor_name for req in batch_requests]))
        categories = list(set([req.category for req in batch_requests]))
        
        # Calculate estimated costs (rough estimate)
        total_tokens_estimate = sum([req.max_tokens for req in batch_requests])
        
        return {
            "total_requests": len(batch_requests),
            "unique_governors": len(governors),
            "categories": categories,
            "governor_list": governors,
            "estimated_total_tokens": total_tokens_estimate,
            "estimated_cost_usd": total_tokens_estimate * 0.000003,  # Rough estimate
            "model": self.model
        }
    
    def retrieve_batch_results(self, batch_id: str) -> Optional[List[Dict[str, Any]]]:
        """Retrieve batch results from Anthropic."""
        
        if self.dry_run:
            self.logger.info(f"DRY RUN: Would retrieve results for batch {batch_id}")
            # Return mock results for testing
            return [
                {
                    "custom_id": "PASCOMB_knowledge_base_test",
                    "result": {
                        "type": "succeeded",
                        "message": {
                            "content": [{"text": "SELECTIONS: Hermetic Tradition, Sacred Geometry, Sufi Mysticism, Kabbalah\nREASONING: These traditions align with my water element..."}]
                        }
                    }
                }
            ]
        
        try:
            if not self.anthropic_client:
                self.logger.error("Anthropic client not initialized")
                return None
            
            # Get batch results
            results = []
            for result in self.anthropic_client.messages.batches.results(batch_id):
                results.append(result.model_dump() if hasattr(result, 'model_dump') else dict(result))
            
            self.logger.info(f"Retrieved {len(results)} results for batch {batch_id}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error retrieving batch results: {e}")
            return None
    
    def process_batch_results(self, batch_id: str, results: List[Dict[str, Any]]) -> bool:
        """Process batch results and update individual governor dossiers."""
        
        try:
            # Create results directory structure
            batch_results_dir = self.batch_results_dir / batch_id
            batch_results_dir.mkdir(exist_ok=True)
            
            # Save raw results
            raw_results_file = batch_results_dir / "raw_results.jsonl"
            with open(raw_results_file, 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(json.dumps(result, ensure_ascii=False) + '\n')
            
            self.logger.info(f"Saved raw results to {raw_results_file}")
            
            # Process each result
            successful_updates = 0
            failed_updates = 0
            processing_log = []
            
            for result in results:
                try:
                    # Extract result info
                    custom_id = result.get("custom_id", "")
                    result_data = result.get("result", {})
                    result_type = result_data.get("type", "")
                    
                    if result_type == "succeeded":
                        # Parse custom_id: "GOVERNORNAME_CATEGORY_HASH"
                        parts = custom_id.split("_")
                        if len(parts) >= 2:
                            governor_name = parts[0]
                            category = parts[1]
                            
                            # Get response content
                            message = result_data.get("message", {})
                            content = message.get("content", [])
                            response_text = ""
                            
                            if content and len(content) > 0:
                                response_text = content[0].get("text", "")
                            
                            # Update governor dossier
                            update_success = self._update_governor_dossier(
                                governor_name, category, response_text, batch_id
                            )
                            
                            if update_success:
                                successful_updates += 1
                                self.logger.info(f"Updated {governor_name} - {category}")
                            else:
                                failed_updates += 1
                                self.logger.error(f"Failed to update {governor_name} - {category}")
                            
                            # Log processing details
                            processing_log.append({
                                "custom_id": custom_id,
                                "governor_name": governor_name,
                                "category": category,
                                "result_type": result_type,
                                "update_success": update_success,
                                "response_length": len(response_text)
                            })
                        
                    else:
                        # Handle failed results
                        self.logger.warning(f"Result failed: {custom_id} - {result_type}")
                        processing_log.append({
                            "custom_id": custom_id,
                            "result_type": result_type,
                            "update_success": False,
                            "error": result_data.get("error", "Unknown error")
                        })
                        failed_updates += 1
                        
                except Exception as e:
                    self.logger.error(f"Error processing result {result.get('custom_id', 'unknown')}: {e}")
                    failed_updates += 1
            
            # Save processing summary
            summary = {
                "batch_id": batch_id,
                "processed_at": datetime.now().isoformat(),
                "total_results": len(results),
                "successful_updates": successful_updates,
                "failed_updates": failed_updates,
                "processing_log": processing_log
            }
            
            summary_file = batch_results_dir / "processing_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Batch processing complete: {successful_updates} success, {failed_updates} failed")
            return successful_updates > 0
            
        except Exception as e:
            self.logger.error(f"Error processing batch results: {e}")
            return False
    
    def _update_governor_dossier(self, governor_name: str, category: str, response_text: str, batch_id: str) -> bool:
        """Update individual governor dossier file with clean trait data (no critique)."""
        
        try:
            # Load individual governor dossier
            dossier_file = self.project_root / "governor_output" / f"{governor_name}.json"
            
            if not dossier_file.exists():
                self.logger.error(f"Governor dossier not found: {dossier_file}")
                return False
            
            with open(dossier_file, 'r', encoding='utf-8') as f:
                dossier_data = json.load(f)
            
            # Parse the response to extract clean trait data
            updated_trait = self._parse_response_for_trait(response_text, category)
            
            if not updated_trait:
                self.logger.error(f"Could not parse trait from response for {governor_name} - {category}")
                return False
            
            # Update the appropriate section in dossier
            update_success = self._apply_trait_update(dossier_data, category, updated_trait)
            
            if not update_success:
                self.logger.error(f"Could not apply trait update for {governor_name} - {category}")
                return False
            
            # Add/update review metadata
            if "review_metadata" not in dossier_data:
                dossier_data["review_metadata"] = {}
            
            dossier_data["review_metadata"].update({
                "last_review_date": datetime.now().isoformat(),
                "review_method": "batch_api_review",
                "batch_id": batch_id,
                "reviewed_categories": dossier_data["review_metadata"].get("reviewed_categories", [])
            })
            
            # Add category to reviewed list if not already there
            reviewed_cats = dossier_data["review_metadata"]["reviewed_categories"]
            if category not in reviewed_cats:
                reviewed_cats.append(category)
            
            # Save updated dossier
            with open(dossier_file, 'w', encoding='utf-8') as f:
                json.dump(dossier_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Successfully updated {governor_name} dossier for {category}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating governor dossier: {e}")
            return False
    
    def _parse_response_for_trait(self, response_text: str, category: str) -> Optional[Any]:
        """Parse response text to extract clean trait data without reasoning."""
        
        try:
            if category == "knowledge_base":
                # Look for SELECTIONS: line
                lines = response_text.split('\n')
                for line in lines:
                    if line.strip().startswith("SELECTIONS:"):
                        selections_text = line.replace("SELECTIONS:", "").strip()
                        # Parse comma-separated traditions
                        traditions = [t.strip() for t in selections_text.split(',')]
                        return traditions[:4]  # Ensure only 4 traditions
                        
            elif category in ["virtues_pool", "flaws_pool", "tones", "approaches", 
                             "motive_alignment", "role_archtypes", "orientation_io", 
                             "polarity_cd", "self_regard_options"]:
                # Look for DECISION: line
                lines = response_text.split('\n')
                for line in lines:
                    if line.strip().startswith("DECISION:"):
                        decision_text = line.replace("DECISION:", "").strip()
                        
                        if decision_text.startswith("CONFIRM"):
                            # Extract current trait name after CONFIRM
                            parts = decision_text.split()
                            if len(parts) > 1:
                                return " ".join(parts[1:])
                        elif decision_text.startswith("CHANGE to"):
                            # Extract new trait name after "CHANGE to"
                            new_trait = decision_text.replace("CHANGE to", "").strip()
                            return new_trait
                        else:
                            # Direct trait name
                            return decision_text
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error parsing response for {category}: {e}")
            return None
    
    def _apply_trait_update(self, dossier_data: Dict[str, Any], category: str, trait_value: Any) -> bool:
        """Apply trait update to dossier data structure."""
        
        try:
            if category == "knowledge_base":
                # Update knowledge_base section
                if "knowledge_base" not in dossier_data:
                    dossier_data["knowledge_base"] = {}
                dossier_data["knowledge_base"]["chosen_traditions"] = trait_value
                
            elif category == "virtues_pool":
                # Update personality.virtues (assuming single virtue for now)
                if "personality" not in dossier_data:
                    dossier_data["personality"] = {}
                if isinstance(trait_value, str):
                    dossier_data["personality"]["virtue"] = trait_value
                    
            elif category == "flaws_pool":
                # Update personality.flaws (assuming single flaw for now)
                if "personality" not in dossier_data:
                    dossier_data["personality"] = {}
                if isinstance(trait_value, str):
                    dossier_data["personality"]["flaw"] = trait_value
                    
            elif category == "tones":
                if "personality" not in dossier_data:
                    dossier_data["personality"] = {}
                dossier_data["personality"]["tone"] = trait_value
                
            elif category == "approaches":
                if "personality" not in dossier_data:
                    dossier_data["personality"] = {}
                dossier_data["personality"]["approach"] = trait_value
                
            elif category == "motive_alignment":
                if "personality" not in dossier_data:
                    dossier_data["personality"] = {}
                dossier_data["personality"]["motive_alignment"] = trait_value
                
            elif category == "role_archtypes":
                if "personality" not in dossier_data:
                    dossier_data["personality"] = {}
                dossier_data["personality"]["role_archtype"] = trait_value
                
            elif category == "orientation_io":
                if "personality" not in dossier_data:
                    dossier_data["personality"] = {}
                dossier_data["personality"]["orientation_io"] = trait_value
                
            elif category == "polarity_cd":
                if "personality" not in dossier_data:
                    dossier_data["personality"] = {}
                dossier_data["personality"]["polarity_cd"] = trait_value
                
            elif category == "self_regard_options":
                if "personality" not in dossier_data:
                    dossier_data["personality"] = {}
                dossier_data["personality"]["self_regard"] = trait_value
                
            else:
                self.logger.warning(f"Unknown category for trait update: {category}")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying trait update for {category}: {e}")
            return False

def main():
    """Main function to run the batch governor review system."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch Governor Review System")
    parser.add_argument("--dry-run", action="store_true", help="Run in dry-run mode")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--test", action="store_true", help="Run test batch (3 governors)")
    parser.add_argument("--create-batch", action="store_true", help="Create batch requests")
    parser.add_argument("--submit-batch", type=str, help="Submit batch from file")
    parser.add_argument("--monitor-batch", type=str, help="Monitor batch by ID")
    parser.add_argument("--process-results", type=str, help="Process results from batch ID")
    parser.add_argument("--model", type=str, default="claude-3-5-sonnet-20241022", help="Model to use")
    
    args = parser.parse_args()
    
    # Initialize system
    system = BatchGovernorReviewSystem(
        model=args.model,
        verbose=args.verbose,
        dry_run=args.dry_run
    )
    
    try:
        if args.test:
            # Test run with 3 governors
            print("🧪 Creating test batch...")
            batch_requests = system.create_test_batch(3)
            
            if batch_requests:
                summary = system.get_batch_summary(batch_requests)
                print(f"✅ Test batch created: {summary}")
                
                # Save test batch
                system.save_batch_requests(batch_requests, "test_batch.json")
                print("📁 Test batch saved to test_batch.json")
            else:
                print("❌ Failed to create test batch")
        
        elif args.create_batch:
            # Create full batch
            print("📝 Creating full batch for all governors...")
            batch_requests = system.prepare_full_batch()
            
            if batch_requests:
                summary = system.get_batch_summary(batch_requests)
                print(f"✅ Full batch created: {summary}")
                
                # Save full batch
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"governor_batch_{timestamp}.json"
                system.save_batch_requests(batch_requests, filename)
                print(f"📁 Full batch saved to {filename}")
                
                # Show readiness checklist
                print("\n🚀 BATCH READINESS CHECKLIST:")
                print(f"   ✅ Total requests: {summary['total_requests']}")
                print(f"   ✅ Governors to process: {summary['unique_governors']}")
                print(f"   ✅ Categories per governor: {len(summary['categories'])}")
                print(f"   ✅ Estimated cost: ${summary['estimated_cost_usd']:.2f}")
                print(f"   ✅ Model: {summary['model']}")
                print(f"   ✅ Batch file: {filename}")
                print("\n🎯 Ready to submit!")
                
            else:
                print("❌ Failed to create full batch")
        
        elif args.submit_batch:
            # Submit batch from file
            print(f"🚀 Submitting batch from {args.submit_batch}...")
            
            # Load batch requests
            batch_file = system.batch_jobs_dir / args.submit_batch
            if batch_file.exists():
                with open(batch_file, 'r', encoding='utf-8') as f:
                    batch_data = json.load(f)
                
                # Submit batch
                job_name = f"governor_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                batch_job = system.submit_batch_job(batch_data, job_name)
                
                if batch_job:
                    print(f"✅ Batch submitted: {batch_job.batch_id}")
                    print(f"📊 Job name: {batch_job.job_name}")
                    print(f"🔄 Status: {batch_job.status}")
                    
                    # Start monitoring
                    if not args.dry_run:
                        print("🔍 Starting monitoring...")
                        system.monitor_batch_job(batch_job.batch_id)
                else:
                    print("❌ Failed to submit batch")
            else:
                print(f"❌ Batch file not found: {args.submit_batch}")
        
        elif args.monitor_batch:
            # Monitor existing batch
            print(f"🔍 Monitoring batch {args.monitor_batch}...")
            success = system.monitor_batch_job(args.monitor_batch)
            
            if success:
                print("✅ Batch completed successfully!")
                
                # Automatically process results if batch completed
                print("📊 Processing batch results...")
                results = system.retrieve_batch_results(args.monitor_batch)
                if results:
                    process_success = system.process_batch_results(args.monitor_batch, results)
                    if process_success:
                        print("✅ Governor dossiers updated successfully!")
                    else:
                        print("❌ Failed to process some results")
                else:
                    print("❌ Failed to retrieve batch results")
            else:
                print("❌ Batch failed or monitoring error")
        
        elif args.process_results:
            # Process results from completed batch
            print(f"📊 Processing results from batch {args.process_results}...")
            results = system.retrieve_batch_results(args.process_results)
            
            if results:
                success = system.process_batch_results(args.process_results, results)
                if success:
                    print("✅ Governor dossiers updated successfully!")
                    print(f"📁 Results saved to batch_results/{args.process_results}/")
                else:
                    print("❌ Failed to process batch results")
            else:
                print("❌ Failed to retrieve batch results")
        
        else:
            # Default: show status
            governors = system.get_governors_needing_review()
            print(f"📊 Status: {len(governors)} governors need review")
            print("Use --help for available commands")
    
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 