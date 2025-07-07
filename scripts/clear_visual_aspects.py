"""Script to clear visual aspects fields from all governors."""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Add project root to PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.utils.custom_logging.custom_logger import setup_logger

# Setup logging
logger = setup_logger(__name__)

def create_empty_visual_aspects(governor_id: str) -> Dict[str, Any]:
    """Create empty visual aspects structure.
    
    Args:
        governor_id: ID of the governor
        
    Returns:
        Empty visual aspects structure
    """
    return {
        "governor_id": governor_id,
        "name": governor_id,
        "dimensional_manifestation": {
            "base_form": "",
            "form_description": "",
            "dimensional_variations": {
                "etheric": "",
                "astral": "",
                "mental": "",
                "causal": ""
            },
            "transition_effects": "",
            "constant_elements": []
        },
        "color_scheme": "",
        "geometry_patterns": [],
        "environmental_effects": {
            "primary_effect": "",
            "radius": "",
            "duration": "",
            "intensity": "",
            "secondary_effects": []
        },
        "time_variations": {
            "astrological_influences": [],
            "cycle_description": "",
            "peak_manifestation": "",
            "dormant_manifestation": ""
        },
        "energy_signature": {
            "frequency": "",
            "polarity": "",
            "intensity": "",
            "special_properties": []
        },
        "symbol_set": {
            "sigils": [],
            "emblems": [],
            "seals": [],
            "scripts": []
        },
        "light_shadow": {
            "light_expression": "",
            "shadow_interaction": "",
            "balance_point": "",
            "special_effects": []
        },
        "scale_description": "",
        "scale_variations": {
            "physical": "",
            "etheric": "",
            "astral": "",
            "mental": ""
        },
        "special_properties": [],
        "manifestation_triggers": [],
        "observer_effects": ""
    }

def clear_governor_visual_aspects(governor_file: Path) -> None:
    """Clear visual aspects for a single governor.
    
    Args:
        governor_file: Path to governor JSON file
    """
    logger.info(f"Processing {governor_file.name}")
    
    # Load governor data
    with governor_file.open('r', encoding='utf-8') as f:
        governor_data = json.load(f)
        
    # Create empty visual aspects
    governor_id = governor_data.get("governor_id") or governor_file.stem
    governor_data["visual_aspects"] = create_empty_visual_aspects(governor_id)
    
    # Save updated governor data
    with governor_file.open('w', encoding='utf-8') as f:
        json.dump(governor_data, f, indent=2)
        
    logger.info(f"Cleared visual aspects for {governor_file.name}")

def clear_all_governors(governors_dir: Path) -> None:
    """Clear visual aspects for all governors.
    
    Args:
        governors_dir: Directory containing governor files
    """
    logger.info("Starting visual aspects clearing process")
    
    # Process each governor file
    governor_files = list(governors_dir.glob("*.json"))
    total_governors = len(governor_files)
    
    logger.info(f"Found {total_governors} governors to process")
    
    for governor_file in governor_files:
        try:
            clear_governor_visual_aspects(governor_file)
        except Exception as e:
            logger.error(f"Error processing {governor_file.name}: {str(e)}")
            
    logger.info("Visual aspects clearing process complete")

def main():
    """Run the visual aspects clearing process."""
    try:
        # Get project root directory
        project_root = Path(__file__).parent.parent
        
        # Get governors directory
        governors_dir = project_root / "governor_dossier"
        if not governors_dir.exists():
            raise FileNotFoundError("Governor dossier directory not found")
            
        # Create backup directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = project_root / "backups" / f"governors_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup current governors
        logger.info("Creating backup of governor files")
        for governor_file in governors_dir.glob("*.json"):
            backup_file = backup_dir / governor_file.name
            backup_file.write_bytes(governor_file.read_bytes())
            
        # Clear visual aspects
        clear_all_governors(governors_dir)
        
        logger.info("Process completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Error clearing visual aspects: {str(e)}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main()) 