"""
Batch Visual Aspects Generator

This script generates visual aspects profiles for all governors and updates their dossiers.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import anthropic
from dotenv import load_dotenv

from core.governors.profiler.interview.visual_aspects_interview import VisualAspectsInterviewer
from core.utils.custom_logging.custom_logger import setup_logger
from core.utils.common.progress import ProgressTracker

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)

class BatchVisualAspectsGenerator:
    """Generates visual aspects for all governors"""
    
    def __init__(self, governors_dir: str = "governor_dossier"):
        self.governors_dir = Path(governors_dir)
        self.progress: Optional[ProgressTracker] = None
        
        # Initialize Anthropic client
        self.client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
        
    def run(self):
        """Run the batch generation process"""
        logger.info("Starting batch visual aspects generation")
        
        # Get all governor files
        governor_files = [f for f in self.governors_dir.glob("*.json") 
                         if f.stem != "visual_aspects_generation_results"]
        
        successful = 0
        failed = 0
        
        for idx, governor_file in enumerate(governor_files, 1):
            logger.info(f"Processing governor {idx}/{len(governor_files)}: {governor_file.stem}")
            
            try:
                result = self.generate_visual_aspects(governor_file)
                if result:
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                logger.error(f"Error processing {governor_file.stem}: {str(e)}")
                failed += 1
                
        logger.info(f"Completed processing {len(governor_files)} governors")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")

    def generate_visual_aspects(self, governor_file: Path) -> Optional[Dict[str, Any]]:
        """Generate visual aspects for a single governor"""
        try:
            # Get governor ID from filename
            governor_id = governor_file.stem
            
            # Load governor data
            governor_data = self.load_governor_data(governor_file)
            
            # Add governor ID if missing
            if "governor_id" not in governor_data:
                governor_data["governor_id"] = governor_id
                
            governor_info = self.extract_governor_info(governor_data)
            
            # Create interviewer and generate profile
            interviewer = VisualAspectsInterviewer(
                governor_id=governor_id,
                governor_name=governor_info["governor_name"] or governor_id,
                governor_traits=governor_info["governor_traits"],
                aethyr_level=governor_info["aethyr_level"],
                mystical_correspondences=governor_info["mystical_correspondences"]
            )
            
            # Generate visual profile
            visual_profile = interviewer.generate_visual_profile()
            
            # Convert to dict and update governor data
            governor_data["visual_aspects"] = visual_profile.to_dict()
            self.save_governor_data(governor_file, governor_data)
            
            return governor_data
            
        except Exception as e:
            logger.error(f"Error generating visual aspects for {governor_file.stem}: {str(e)}")
            return None

    def load_governor_data(self, governor_file: Path) -> Dict[str, Any]:
        """Load governor data from file"""
        with open(governor_file, 'r') as f:
            return json.load(f)
            
    def save_governor_data(self, governor_file: Path, data: Dict[str, Any]):
        """Save updated governor data to file"""
        with open(governor_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    def extract_governor_info(self, governor_data: Dict) -> Dict[str, Any]:
        """Extract required info for visual aspects generation"""
        persona = governor_data.get("persona", {})
        return {
            "governor_id": governor_data.get("governor_id"),
            "governor_name": governor_data.get("name"),
            "governor_traits": {
                "polar_traits": persona.get("polar_traits", {}),
                "approaches": persona.get("approaches", {}),
                "tones": persona.get("tones", {})
            },
            "aethyr_level": self._get_aethyr_level(governor_data.get("aethyr", "LIL")),
            "mystical_correspondences": {
                "element": governor_data.get("element"),
                "archetypal": governor_data.get("archetypal_correspondences", {})
            }
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

if __name__ == "__main__":
    generator = BatchVisualAspectsGenerator()
    generator.run() 