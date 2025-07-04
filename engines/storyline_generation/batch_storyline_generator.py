#!/usr/bin/env python3
"""
Batch Storyline Generator - Uses Anthropic Batch API for parallel processing
Processes multiple governors simultaneously for efficient storyline generation
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import anthropic
import logging
import time

# Import validation schemas
try:
    from engines.storyline_generation.schemas.governor_input_schema import GovernorInputValidator
    from engines.storyline_generation.schemas.storyline_output_schema import StorylineOutputValidator
    VALIDATION_AVAILABLE = True
except ImportError:
    logging.warning("⚠️ Validation schemas not available - running without validation")
    VALIDATION_AVAILABLE = False

class BatchStorylineGenerator:
    """Generates storylines for multiple governors using batch API"""
    
    def __init__(self, base_path: Path = Path(".")):
        self.base_path = Path(base_path)
        self.governor_path = self.base_path / "governor_output"
        self.output_path = self.base_path / "storyline_output_v3_batch"
        
        # Create output directory
        self.output_path.mkdir(exist_ok=True)
        
        # Initialize Anthropic client
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        
        # Initialize validators if available
        self.input_validator = None
        self.output_validator = None
        
        if VALIDATION_AVAILABLE:
            self.input_validator = GovernorInputValidator()
            self.output_validator = StorylineOutputValidator()
            logging.info("✅ Validation schemas loaded")
        
        logging.info("🚀 Batch Storyline Generator initialized")
        logging.info(f"   Output: {self.output_path}")
        logging.info(f"   Validation: {'Enabled' if VALIDATION_AVAILABLE else 'Disabled'}")
    
    def create_batch_requests(self, governor_names: Optional[List[str]] = None) -> List[Dict]:
        """Create batch requests for multiple governors"""
        
        if governor_names is None:
            # Get all governor files
            governor_files = list(self.governor_path.glob("*.json"))
            governor_names = [f.stem for f in governor_files]
        
        batch_requests = []
        
        for governor_name in governor_names:
            # Load governor data
            governor_data = self._load_governor_data(governor_name)
            if not governor_data:
                logging.warning(f"⚠️ Could not load data for {governor_name}")
                continue
            
            # Create the detailed prompt for this governor
            prompt = self._create_governor_prompt(governor_name, governor_data)
            
            batch_request = {
                "custom_id": f"storyline-{governor_name}",
                "params": {
                    "model": "claude-3-5-sonnet-20241022",
                    "max_tokens": 8000,  # Large enough for rich storylines
                    "messages": [
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ]
                }
            }
            
            batch_requests.append(batch_request)
        
        logging.info(f"📦 Created {len(batch_requests)} batch requests")
        return batch_requests
    
    def _create_governor_prompt(self, governor_name: str, governor_data: Dict) -> str:
        """Create detailed prompt for rich storyline generation"""
        
        # Extract key data for the prompt
        identity = self._extract_identity_summary(governor_data)
        wisdom_traditions = governor_data.get("knowledge_base_selections", {})
        voidmaker_summary = self._extract_voidmaker_summary(governor_data)
        
        prompt = f"""
# Rich Storyline Generation for Governor {governor_name}

You are tasked with creating a RICH, specification-compliant storyline for Governor {governor_name} following the exact requirements:

## Governor Profile Summary:
**Name:** {governor_name}
**Identity:** {identity.get('name_pronunciation', 'Unknown')}
**Home Aethyr:** {identity.get('home_aethyr', 'Unknown')}
**Cosmic Mandate:** {identity.get('cosmic_mandate', 'Unknown')}

**Wisdom Traditions:** {wisdom_traditions.get('chosen_traditions', [])}
**Tradition Count:** {len(wisdom_traditions.get('chosen_traditions', []))}

**Voidmaker Questions:** {voidmaker_summary.get('total_questions', 0)}
**Voidmaker Themes:** {voidmaker_summary.get('themes', [])}

## REQUIREMENTS:
1. Generate 20-35 rich story nodes (NOT template content)
2. Implement 4-tier reputation system (0-25, 26-50, 51-75, 76-100)
3. Use actual Q&A responses for personality-driven dialogue
4. Integrate voidmaker content across reputation tiers
5. Include canonical accuracy (Aethyrs, elements, traditions)

## Full Governor Data:
```json
{json.dumps(governor_data, indent=2)}
```

## TASK:
Create a complete rich storyline JSON that follows the storyline_template.md schema with:
- Rich personality integration from actual responses
- Reputation-gated voidmaker reveals
- 20-35 narrative nodes with branching choices
- Game mechanics integration (energy costs, cooldowns, rewards)
- Canonical accuracy validation

Return ONLY the complete JSON storyline structure.
"""
        
        return prompt
    
    def submit_batch(self, batch_requests: List[Dict]) -> str:
        """Submit batch requests and return batch ID"""
        
        logging.info(f"📤 Submitting batch with {len(batch_requests)} requests")
        
        message_batch = self.client.messages.batches.create(
            requests=batch_requests  # type: ignore
        )
        
        batch_id = message_batch.id
        logging.info(f"✅ Batch submitted successfully: {batch_id}")
        return batch_id
    
    def monitor_batch(self, batch_id: str) -> Any:
        """Monitor batch progress and return when complete"""
        
        logging.info(f"👀 Monitoring batch: {batch_id}")
        
        while True:
            batch_status = self.client.messages.batches.retrieve(batch_id)
            
            status = batch_status.processing_status
            
            # Safe attribute access for request counts
            completed = 0
            total = 0
            if hasattr(batch_status, 'request_counts') and batch_status.request_counts:
                completed = getattr(batch_status.request_counts, 'completed', 0)
                total = getattr(batch_status.request_counts, 'total', 0)
            
            logging.info(f"📊 Batch status: {status} ({completed}/{total} completed)")
            
            if status == "ended":
                logging.info("✅ Batch processing completed!")
                return batch_status
            elif status == "failed":
                logging.error("❌ Batch processing failed!")
                return batch_status
            
            # Wait 30 seconds before checking again
            time.sleep(30)
    
    def retrieve_results(self, batch_id: str) -> Dict[str, Dict]:
        """Retrieve and process batch results"""
        
        logging.info(f"📥 Retrieving results for batch: {batch_id}")
        
        results = {}
        
        # Get batch results
        batch_results = self.client.messages.batches.results(batch_id)
        
        for result in batch_results:
            custom_id = result.custom_id
            governor_name = custom_id.replace("storyline-", "")
            
            if result.result.type == "succeeded":
                try:
                    # Parse the JSON response - safely extract text content
                    content_blocks = result.result.message.content
                    storyline_content = ""
                    
                    for block in content_blocks:
                        # Use getattr for safe attribute access
                        text_content = getattr(block, 'text', None)
                        if text_content:
                            storyline_content += text_content
                        else:
                            # Try alternative content attribute
                            alt_content = getattr(block, 'content', None)
                            if alt_content:
                                storyline_content += str(alt_content)
                    
                    if not storyline_content:
                        raise ValueError("No text content found in response")
                        
                    storyline_json = json.loads(storyline_content)
                    
                    # Validate output if validator available
                    if self.output_validator:
                        is_valid, errors = self.output_validator.validate_storyline_data(storyline_json)
                        if not is_valid:
                            logging.error(f"❌ Storyline validation failed for {governor_name}:")
                            for error in errors[:3]:  # Show first 3 errors
                                logging.error(f"   - {error}")
                            results[governor_name] = {"error": "Output validation failed", "validation_errors": errors}
                        else:
                            logging.info(f"✅ Storyline validation passed for {governor_name}")
                            results[governor_name] = storyline_json
                    else:
                        results[governor_name] = storyline_json
                    
                    logging.info(f"✅ Successfully processed storyline for {governor_name}")
                    
                except json.JSONDecodeError as e:
                    logging.error(f"❌ JSON parsing failed for {governor_name}: {e}")
                    results[governor_name] = {"error": "JSON parsing failed"}
                    
            else:
                logging.error(f"❌ Request failed for {governor_name}: {result.result}")
                results[governor_name] = {"error": "Request failed"}
        
        success_count = sum(1 for r in results.values() if "error" not in r)
        logging.info(f"📈 Retrieved {success_count}/{len(results)} successful storylines")
        
        return results
    
    def save_batch_results(self, results: Dict[str, Dict]) -> bool:
        """Save all batch results to files"""
        
        logging.info(f"💾 Saving {len(results)} storyline results")
        
        success_count = 0
        
        for governor_name, storyline_data in results.items():
            if "error" in storyline_data:
                logging.warning(f"⚠️ Skipping {governor_name} due to error: {storyline_data['error']}")
                continue
            
            # Save individual storyline file
            output_file = self.output_path / f"{governor_name}_rich_v3.json"
            
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(storyline_data, f, indent=2, ensure_ascii=False)
                
                success_count += 1
                logging.info(f"✅ Saved storyline for {governor_name}")
                
            except Exception as e:
                logging.error(f"❌ Failed to save {governor_name}: {e}")
        
        logging.info(f"🎯 Successfully saved {success_count}/{len(results)} storylines")
        return success_count > 0
    
    def generate_all_storylines(self, governor_names: Optional[List[str]] = None) -> bool:
        """Complete end-to-end batch storyline generation"""
        
        logging.info("🚀 Starting complete batch storyline generation")
        
        try:
            # Create batch requests
            batch_requests = self.create_batch_requests(governor_names)
            if not batch_requests:
                logging.error("❌ No valid batch requests created")
                return False
            
            # Submit batch
            batch_id = self.submit_batch(batch_requests)
            
            # Monitor until completion
            batch_status = self.monitor_batch(batch_id)
            
            if batch_status.processing_status != "ended":
                logging.error("❌ Batch did not complete successfully")
                return False
            
            # Retrieve results
            results = self.retrieve_results(batch_id)
            
            # Save results
            success = self.save_batch_results(results)
            
            if success:
                logging.info("🎉 Batch storyline generation completed successfully!")
                return True
            else:
                logging.error("❌ Failed to save batch results")
                return False
                
        except Exception as e:
            logging.error(f"❌ Batch generation failed: {e}")
            return False
    
    def _load_governor_data(self, governor_name: str) -> Optional[Dict]:
        """Load governor data safely with validation"""
        governor_file = self.governor_path / f"{governor_name}.json"
        
        if not governor_file.exists():
            logging.warning(f"❌ Governor file not found: {governor_name}")
            return None
        
        try:
            with open(governor_file, 'r', encoding='utf-8') as f:
                governor_data = json.load(f)
            
            # Validate input data if validator available
            if self.input_validator:
                is_valid, errors = self.input_validator.validate_governor_data(governor_data)
                if not is_valid:
                    logging.error(f"❌ Governor data validation failed for {governor_name}:")
                    for error in errors[:3]:  # Show first 3 errors
                        logging.error(f"   - {error}")
                    return None
                else:
                    logging.info(f"✅ Governor data validation passed for {governor_name}")
            
            return governor_data
            
        except Exception as e:
            logging.error(f"❌ Failed to load governor data for {governor_name}: {e}")
            return None
    
    def _extract_identity_summary(self, governor_data: Dict) -> Dict:
        """Extract identity summary for prompt"""
        blocks = governor_data.get("blocks", {})
        identity_block = blocks.get("A_identity_origin", {}).get("questions", {})
        
        return {
            "name_pronunciation": identity_block.get("1", {}).get("answer", ""),
            "home_aethyr": identity_block.get("3", {}).get("answer", ""),
            "cosmic_mandate": identity_block.get("5", {}).get("answer", "")
        }
    
    def _extract_voidmaker_summary(self, governor_data: Dict) -> Dict:
        """Extract voidmaker summary for prompt"""
        voidmaker = governor_data.get("voidmaker_expansion", {})
        
        total_questions = 0
        themes = set()
        
        for block_name, block_data in voidmaker.items():
            if isinstance(block_data, dict) and "questions" in block_data:
                questions = block_data["questions"]
                total_questions += len(questions)
                
                # Extract themes from answers
                for q_data in questions.values():
                    if isinstance(q_data, dict) and "answer" in q_data:
                        answer = q_data["answer"].lower()
                        if "geometric" in answer:
                            themes.add("geometric")
                        if "hermetic" in answer:
                            themes.add("hermetic")
                        if "unity" in answer:
                            themes.add("unity")
        
        return {
            "total_questions": total_questions,
            "themes": list(themes)
        }

def main():
    """Run batch storyline generation"""
    logging.basicConfig(level=logging.INFO)
    
    generator = BatchStorylineGenerator()
    
    # Generate for specific governors (or None for all)
    test_governors = ["ABRIOND", "VALGARS", "OCCODON"]  # Start with a few for testing
    
    success = generator.generate_all_storylines(test_governors)
    
    if success:
        print("🎉 Batch storyline generation completed!")
    else:
        print("❌ Batch storyline generation failed!")

if __name__ == "__main__":
    main() 
