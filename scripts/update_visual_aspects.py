"""
Script to update governor dossiers with consistent visual_aspects structure
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_visual_aspects(visual_aspects_dir: Path, governor_id: str) -> Dict[str, Any]:
    """Load visual aspects from JSON file"""
    visual_file = visual_aspects_dir / f"{governor_id}_visual.json"
    if not visual_file.exists():
        raise FileNotFoundError(f"Visual aspects not found for {governor_id}")
        
    with open(visual_file, 'r') as f:
        return json.load(f)

def update_dossier(dossier_file: Path, visual_aspects: Dict[str, Any]) -> None:
    """Update dossier with consistent visual_aspects structure"""
    with open(dossier_file, 'r') as f:
        dossier = json.load(f)
        
    # Update visual_aspects section
    dossier['visual_aspects'] = visual_aspects
    
    # Write updated dossier
    with open(dossier_file, 'w') as f:
        json.dump(dossier, f, indent=2)

def main():
    """Main function"""
    try:
        dossier_dir = Path('governor_dossier')
        visual_aspects_dir = dossier_dir / 'visual_aspects'
        
        # Process each governor dossier
        for dossier_file in dossier_dir.glob('*.json'):
            if dossier_file.stem in ['visual_aspects_generation_results']:
                continue
                
            try:
                governor_id = dossier_file.stem
                logger.info(f"Processing {governor_id}")
                
                # Load visual aspects
                visual_aspects = load_visual_aspects(visual_aspects_dir, governor_id)
                
                # Update dossier
                update_dossier(dossier_file, visual_aspects)
                logger.info(f"Updated {governor_id}")
                
            except Exception as e:
                logger.error(f"Failed to process {dossier_file.name}: {e}")
                
    except Exception as e:
        logger.error(f"Script failed: {e}")
        raise

if __name__ == '__main__':
    main() 