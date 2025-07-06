"""
Governor Batch Processor
Specialized implementation of UnifiedBatchProcessor for governor profile generation
"""

from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime

from core.utils.batch.unified_processor import UnifiedBatchProcessor, BatchConfig
from core.governors.profiler.schemas.mystical_schemas import GovernorProfileSchema
from core.governors.profiler.core.mystical_profiler import MysticalProfiler

logger = logging.getLogger(__name__)

class GovernorBatchProcessor(UnifiedBatchProcessor):
    """
    Batch processor for generating governor profiles
    """
    
    def __init__(self, config: Optional[BatchConfig] = None):
        super().__init__(config or BatchConfig(
            max_retries=3,
            retry_delay=2.0,
            batch_size=10,  # Process governors in smaller batches
            parallel=True,
            validation_schema=GovernorProfileSchema
        ))
        self.profiler = MysticalProfiler()
        
    async def _process_item(self, governor_data: Dict) -> Dict:
        """
        Process a single governor's data to generate their profile
        
        Args:
            governor_data: Raw governor data including name, number, etc.
            
        Returns:
            Dict containing the processed governor profile
        """
        logger.info(f"Processing governor {governor_data.get('name', 'UNKNOWN')}")
        
        try:
            # Generate profile using mystical profiler
            profile = await self.profiler.generate_profile(governor_data)
            
            # Validate the generated profile
            if not self._validate_profile(profile):
                raise ValueError("Generated profile failed validation")
                
            # Add metadata
            profile["metadata"] = {
                "generated_at": datetime.now().isoformat(),
                "version": "2.0",
                "processor": "unified"
            }
            
            logger.info(f"Successfully generated profile for {governor_data.get('name')}")
            return {
                "status": "success",
                "profile": profile,
                "governor_id": governor_data.get("number")
            }
            
        except Exception as e:
            logger.error(f"Error generating profile for {governor_data.get('name')}: {e}")
            raise
            
    def _validate_profile(self, profile: Dict) -> bool:
        """
        Additional validation specific to governor profiles
        
        Args:
            profile: The generated governor profile
            
        Returns:
            bool indicating if profile is valid
        """
        try:
            # Check required sections
            required_sections = [
                "traits",
                "personality",
                "specializations",
                "approaches"
            ]
            
            for section in required_sections:
                if section not in profile:
                    logger.error(f"Missing required section: {section}")
                    return False
                    
            # Validate trait consistency
            if not self._validate_trait_consistency(profile):
                return False
                
            # Validate mystical alignments
            if not self._validate_mystical_alignments(profile):
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error in profile validation: {e}")
            return False
            
    def _validate_trait_consistency(self, profile: Dict) -> bool:
        """
        Ensure traits are consistent with governor's archetype
        """
        try:
            archetype = profile.get("archetype", {}).get("primary")
            traits = profile.get("traits", [])
            
            # TODO: Implement archetype-trait consistency rules
            # For now, just check if traits exist
            return bool(traits)
            
        except Exception as e:
            logger.error(f"Error validating trait consistency: {e}")
            return False
            
    def _validate_mystical_alignments(self, profile: Dict) -> bool:
        """
        Validate mystical alignments and correspondences
        """
        try:
            alignments = profile.get("mystical_alignments", {})
            
            required_alignments = [
                "element",
                "aethyr",
                "direction"
            ]
            
            # Check if all required alignments are present
            for alignment in required_alignments:
                if alignment not in alignments:
                    logger.error(f"Missing required mystical alignment: {alignment}")
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Error validating mystical alignments: {e}")
            return False
            
    async def process_governors(self, governor_data_list: list) -> Dict:
        """
        Process a list of governors and generate their profiles
        
        Args:
            governor_data_list: List of raw governor data
            
        Returns:
            Dict containing results and statistics
        """
        logger.info(f"Starting batch processing of {len(governor_data_list)} governors")
        
        result = await self.process_batch(governor_data_list)
        
        # Compile statistics
        stats = {
            "total_governors": len(governor_data_list),
            "successful": len(result.successful),
            "failed": len(result.failed),
            "processing_time": (result.end_time - result.start_time).total_seconds(),
            "retries": result.stats.get("retries", 0),
            "validation_errors": result.stats.get("validation_errors", 0)
        }
        
        logger.info(f"Completed governor batch processing: {stats}")
        
        return {
            "successful_profiles": result.successful,
            "failed_governors": result.failed,
            "stats": stats
        } 