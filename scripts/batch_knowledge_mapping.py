"""
Batch process all governors to create their knowledge profiles.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from tqdm import tqdm

from core.governors.traits.knowledge_mapper import KnowledgeMapper, GovernorKnowledge

logger = logging.getLogger(__name__)

def load_governor_index(data_root: Optional[Path] = None) -> Dict[str, int]:
    """Load the governor index mapping names to numbers"""
    try:
        if data_root is None:
            data_root = Path("data")
        
        index_path = data_root / "governors/indexes/governor_number_index.json"
        with open(index_path) as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load governor index: {e}")
        return {}

def save_knowledge_profile(knowledge: GovernorKnowledge, output_dir: Path) -> None:
    """Save a governor's knowledge profile to JSON"""
    try:
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert knowledge to dictionary
        knowledge_dict = {
            "governor_id": knowledge.governor_id,
            "primary_tradition": {
                "tradition_name": knowledge.primary_tradition.tradition_name,
                "core_concepts": knowledge.primary_tradition.core_concepts,
                "practices": knowledge.primary_tradition.practices,
                "correspondences": knowledge.primary_tradition.correspondences,
                "historical_context": knowledge.primary_tradition.historical_context,
                "modern_applications": knowledge.primary_tradition.modern_applications
            },
            "secondary_traditions": [
                {
                    "tradition_name": t.tradition_name,
                    "core_concepts": t.core_concepts,
                    "practices": t.practices,
                    "correspondences": t.correspondences,
                    "historical_context": t.historical_context,
                    "modern_applications": t.modern_applications
                }
                for t in knowledge.secondary_traditions
            ],
            "specialized_domains": knowledge.specialized_domains,
            "teaching_methods": knowledge.teaching_methods,
            "ritual_practices": knowledge.ritual_practices,
            "mystical_correspondences": knowledge.mystical_correspondences
        }
        
        # Save to file
        output_path = output_dir / f"{knowledge.governor_id.lower()}_knowledge.json"
        with open(output_path, "w") as f:
            json.dump(knowledge_dict, f, indent=2)
            
    except Exception as e:
        logger.error(f"Failed to save knowledge profile for {knowledge.governor_id}: {e}")

def process_governors(output_dir: Optional[Path] = None, data_root: Optional[Path] = None) -> None:
    """Process all governors and create their knowledge profiles"""
    try:
        # Set default output directory
        if output_dir is None:
            output_dir = Path("data/knowledge/governor_profiles")
        
        # Load governor index
        governor_index = load_governor_index(data_root)
        if not governor_index:
            logger.error("No governors found in index")
            return
        
        # Initialize knowledge mapper
        mapper = KnowledgeMapper(data_root) if data_root else KnowledgeMapper()
        
        # Process each governor
        logger.info(f"Processing {len(governor_index)} governors...")
        
        for governor_id, governor_number in tqdm(governor_index.items(), desc="Mapping governor knowledge"):
            try:
                # Map governor knowledge
                knowledge = mapper.map_governor_knowledge(governor_id, governor_number)
                if knowledge:
                    # Save knowledge profile
                    save_knowledge_profile(knowledge, output_dir)
                    logger.info(f"Successfully processed {governor_id}")
                else:
                    logger.error(f"Failed to map knowledge for {governor_id}")
                
            except Exception as e:
                logger.error(f"Error processing {governor_id}: {e}")
        
        logger.info("Knowledge mapping complete")
        
    except Exception as e:
        logger.error(f"Failed to process governors: {e}")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/knowledge_mapping.log")
        ]
    )
    
    # Run processing
    process_governors() 