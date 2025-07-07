#!/usr/bin/env python3
"""
Convert existing visual aspects data to Bitcoin L1 optimized format.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

from core.game_assets.visual_aspects.bitcoin_optimized import (
    generate_visual_traits, expand_visual_traits
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VisualAspectsConverter:
    """Convert visual aspects to Bitcoin L1 format"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.governors_dir = data_dir / "governors"
        self.output_dir = data_dir / "bitcoin_optimized"
        self.output_dir.mkdir(exist_ok=True)
        
    def convert_all_governors(self):
        """Convert all governor visual aspects"""
        logger.info("Starting visual aspects conversion")
        
        # Get all governor files
        governor_files = list(self.governors_dir.glob("*.json"))
        logger.info(f"Found {len(governor_files)} governor files")
        
        successful = 0
        failed = 0
        bitcoin_data = {
            "version": "1.0.0",
            "timestamp": "",
            "governors": {}
        }
        
        for idx, governor_file in enumerate(governor_files, 1):
            logger.info(f"Processing {idx}/{len(governor_files)}: {governor_file.stem}")
            
            try:
                # Load governor data
                with open(governor_file) as f:
                    governor_data = json.load(f)
                
                # Extract required info
                governor_info = self._extract_governor_info(governor_data)
                
                # Generate Bitcoin format
                binary_traits = generate_visual_traits(
                    governor_info["name"],
                    governor_info["aethyr_level"],
                    governor_info["element"]
                )
                
                # Expand for verification
                expanded = expand_visual_traits(binary_traits)
                
                # Store result
                bitcoin_data["governors"][governor_file.stem] = {
                    "binary_traits": binary_traits.hex(),
                    "expanded": expanded
                }
                
                successful += 1
                
            except Exception as e:
                logger.error(f"Failed to convert {governor_file.stem}: {str(e)}")
                failed += 1
        
        # Save results
        self._save_results(bitcoin_data, successful, failed)
        
    def _extract_governor_info(self, data: Dict) -> Dict[str, Any]:
        """Extract required info from governor data"""
        return {
            "name": data.get("name", ""),
            "aethyr_level": self._get_aethyr_level(data.get("aethyr", "LIL")),
            "element": data.get("element", "Spirit")
        }
        
    def _get_aethyr_level(self, aethyr: str) -> int:
        """Convert aethyr name to numeric level (1-30)"""
        aethyrs = ["LIL", "ARN", "ZOM", "PAZ", "LIT", "MAZ", "DEO", "ZID", "ZIP", 
                   "ZAX", "ICH", "LOE", "IKH", "VTA", "OXO", "LEA", "TAN", "ZEN", 
                   "POP", "KHR", "ASP", "LIN", "TOR", "NIA", "UTI", "DES", "ZAA", 
                   "BAG", "RII", "TEX"]
        try:
            return len(aethyrs) - aethyrs.index(aethyr)
        except ValueError:
            return 1  # Default to highest aethyr if not found
            
    def _save_results(self, bitcoin_data: Dict, successful: int, failed: int):
        """Save conversion results"""
        # Save full data
        output_file = self.output_dir / "visual_aspects_bitcoin.json"
        with open(output_file, "w") as f:
            json.dump(bitcoin_data, f, indent=2)
            
        # Save stats
        stats = {
            "total_governors": successful + failed,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / (successful + failed)) * 100
        }
        
        stats_file = self.output_dir / "conversion_stats.json"
        with open(stats_file, "w") as f:
            json.dump(stats, f, indent=2)
            
        logger.info(f"Conversion complete. Success: {successful}, Failed: {failed}")
        logger.info(f"Results saved to {self.output_dir}")

def main():
    """Main entry point"""
    try:
        # Get data directory
        data_dir = Path(__file__).parent.parent / "data"
        
        # Create converter
        converter = VisualAspectsConverter(data_dir)
        
        # Run conversion
        converter.convert_all_governors()
        
    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 