"""
Test script for visual aspect generation of a single governor.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any
import logging
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from core.game_assets.visual_aspects.bitcoin_optimized import VisualAspectBatchProcessor
from core.utils.custom_logging import get_batch_logger

class DateTimeEncoder(json.JSONEncoder):
    """Handle datetime serialization"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Set up logging
logger = get_batch_logger("visual_test")
logger.setLevel(logging.INFO)

# Test governor data
TEST_GOVERNOR = {
    "name": "ADVORPT",  # Using a known governor name
    "aethyr": 3,        # Higher aethyr for more complex patterns
    "element": "Fire"   # Element for specific trait mapping
}

async def test_single_governor() -> None:
    """Test visual aspect generation for a single governor"""
    try:
        # Initialize processor with config
        processor = VisualAspectBatchProcessor(
            VisualAspectBatchProcessor.create_batch_config()
        )
        
        logger.info(f"Starting visual aspect test for governor: {TEST_GOVERNOR['name']}")
        logger.info(f"Input data: {json.dumps(TEST_GOVERNOR, indent=2)}")
        
        # Process single governor
        results = await processor.process_batch([TEST_GOVERNOR])
        
        # Convert results to dict and serialize
        results_dict = {
            "successful": results.successful if hasattr(results, 'successful') else [],
            "failed": results.failed if hasattr(results, 'failed') else [],
            "stats": results.stats if hasattr(results, 'stats') else {},
            "total_processed": results.total_processed if hasattr(results, 'total_processed') else 0
        }
        logger.info(f"Raw results: {json.dumps(results_dict, indent=2, cls=DateTimeEncoder)}")
        
        if not results.successful:
            logger.error("❌ Visual aspect generation failed!")
            if results.failed:
                logger.error(f"Failed items: {json.dumps(results.failed, indent=2)}")
            if hasattr(results, 'stats'):
                logger.error(f"Stats: {json.dumps(results.stats, indent=2, cls=DateTimeEncoder)}")
            return
            
        # Get the successful result
        result = results.successful[0]
        
        # Save output for inspection
        output_dir = Path("test_output")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"visual_test_{TEST_GOVERNOR['name']}_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2, cls=DateTimeEncoder)
            
        logger.info(f"✅ Test completed successfully!")
        logger.info(f"Results saved to: {output_file}")
        
        # Display key information
        logger.info("\nVisual Aspect Summary:")
        logger.info("-" * 40)
        logger.info(f"Governor: {result['governor_id']}")
        logger.info(f"Binary Size: {len(bytes.fromhex(result['binary_traits']))} bytes")
        
        # Display expanded traits summary
        expanded = result['expanded_traits']
        logger.info("\nExpanded Traits:")
        logger.info("-" * 40)
        for key, value in expanded.items():
            if isinstance(value, dict):
                logger.info(f"{key}:")
                for subkey, subval in value.items():
                    logger.info(f"  {subkey}: {subval}")
            else:
                logger.info(f"{key}: {value}")
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    asyncio.run(test_single_governor()) 