"""
Script to generate visual aspects for all Enochian Governors
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import asdict

from core.governors.visual_aspects.generator import (
    GovernorTraits,
    VisualAspectGenerator
)
from core.governors.visual_aspects.schemas.visual_aspect_schema import (
    AspectScale,
    AspectDimension,
    AspectMotion,
    ColorDefinition,
    PatternDefinition,
    VisualAspect
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_governor_data() -> List[Dict[str, Any]]:
    """Load governor data from archives"""
    governors = []
    archives_dir = Path("data/knowledge/archives/governor_archives")
    
    if not archives_dir.exists():
        raise FileNotFoundError(f"Governor archives directory not found: {archives_dir}")
        
    for file in archives_dir.glob("*.json"):
        try:
            with open(file) as f:
                data = json.load(f)
                governors.append(data)
        except Exception as e:
            logger.error(f"Failed to load governor data from {file}: {str(e)}")
            continue
            
    return governors

def extract_governor_traits(data: Dict[str, Any]) -> GovernorTraits:
    """Extract relevant traits from governor data"""
    return GovernorTraits(
        name=data["name"],
        aethyrs=data.get("aethyrs", []),
        elements=data.get("elements", []),
        traditions=data.get("traditions", []),
        personality_traits=data.get("personality_traits", []),
        mystical_domains=data.get("mystical_domains", [])
    )

def serialize_aspect(aspect: VisualAspect) -> Dict[str, Any]:
    """Serialize a visual aspect to JSON-compatible format"""
    aspect_dict = asdict(aspect)
    
    # Convert enums to strings
    aspect_dict["scale"] = aspect.scale.name
    aspect_dict["dimensions"] = [d.name for d in aspect.dimensions]
    aspect_dict["motions"] = [m.name for m in aspect.motions]
    
    # Convert forms
    if aspect.primary_form:
        aspect_dict["primary_form"] = {
            "name": aspect.primary_form.name,
            "base_type": aspect.primary_form.base_type.name,
            "description": aspect.primary_form.description,
            "valid_interactions": [i.name for i in aspect.primary_form.valid_interactions],
            "tradition_origins": aspect.primary_form.tradition_origins,
            "elemental_affinities": aspect.primary_form.elemental_affinities,
            "aethyr_resonance": aspect.primary_form.aethyr_resonance
        }
    
    if aspect.secondary_form:
        aspect_dict["secondary_form"] = {
            "name": aspect.secondary_form.name,
            "base_type": aspect.secondary_form.base_type.name,
            "description": aspect.secondary_form.description,
            "valid_interactions": [i.name for i in aspect.secondary_form.valid_interactions],
            "tradition_origins": aspect.secondary_form.tradition_origins,
            "elemental_affinities": aspect.secondary_form.elemental_affinities,
            "aethyr_resonance": aspect.secondary_form.aethyr_resonance
        }
    
    return aspect_dict

def save_visual_aspects(aspects: Dict[str, VisualAspect]):
    """Save generated visual aspects to files"""
    output_dir = Path("governor_dossier/visual_aspects")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for name, aspect in aspects.items():
        try:
            output_file = output_dir / f"{name}_visual.json"
            with open(output_file, "w") as f:
                json.dump(serialize_aspect(aspect), f, indent=2)
            logger.info(f"Saved visual aspect for {name} to {output_file}")
        except Exception as e:
            logger.error(f"Failed to save visual aspect for {name}: {str(e)}")

def main():
    """Main execution function"""
    try:
        # Load governor data
        logger.info("Loading governor data...")
        governor_data = load_governor_data()
        logger.info(f"Loaded data for {len(governor_data)} governors")
        
        # Extract traits
        logger.info("Extracting governor traits...")
        governor_traits = [extract_governor_traits(data) for data in governor_data]
        
        # Initialize generator
        generator = VisualAspectGenerator()
        
        # Generate aspects
        logger.info("Generating visual aspects...")
        aspects = generator.generate_aspects_batch(governor_traits)
        logger.info(f"Generated {len(aspects)} visual aspects")
        
        # Save results
        logger.info("Saving visual aspects...")
        save_visual_aspects(aspects)
        logger.info("Visual aspect generation complete")
        
    except Exception as e:
        logger.error(f"Failed to generate visual aspects: {str(e)}")
        raise

if __name__ == "__main__":
    main() 