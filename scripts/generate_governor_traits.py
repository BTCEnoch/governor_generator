#!/usr/bin/env python3
"""
CLI script for generating governor traits.
"""

import argparse
import json
from pathlib import Path
import sys
from typing import Optional, Dict

from core.governors.traits.generator import TraitGenerator
from core.utils.custom_logging import setup_logger

logger = setup_logger(__name__)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate traits for Enochian Governors"
    )
    
    parser.add_argument(
        "governor_id",
        help="Unique identifier for the governor"
    )
    
    parser.add_argument(
        "governor_number",
        type=int,
        help="Governor's numerical designation (1-91)"
    )
    
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/traits"),
        help="Directory containing trait data files"
    )
    
    parser.add_argument(
        "--seed-file",
        type=Path,
        help="Optional JSON file with seed data"
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (default: governor_id.json)"
    )
    
    return parser.parse_args()

def load_seed_data(seed_file: Optional[Path]) -> Optional[Dict]:
    """Load seed data from JSON file"""
    if not seed_file:
        return None
        
    if not seed_file.exists():
        logger.error(f"Seed file not found: {seed_file}")
        sys.exit(1)
        
    try:
        with open(seed_file) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in seed file: {e}")
        sys.exit(1)

def main():
    """Main entry point"""
    args = parse_args()
    
    # Validate governor number
    if not 1 <= args.governor_number <= 91:
        logger.error("Governor number must be between 1 and 91")
        sys.exit(1)
    
    # Load seed data if provided
    seed_data = load_seed_data(args.seed_file)
    
    try:
        # Initialize generator
        generator = TraitGenerator(args.data_dir)
        
        # Generate traits
        logger.info(f"Generating traits for Governor {args.governor_number}")
        traits = generator.generate_governor_traits(
            governor_id=args.governor_id,
            governor_number=args.governor_number,
            seed_data=seed_data
        )
        
        # Determine output path
        output_path = args.output or Path(f"{args.governor_id}.json")
        
        # Save traits
        with open(output_path, 'w') as f:
            json.dump({
                "governor_id": traits.governor_id,
                "governor_number": traits.governor_number,
                "canonical": {
                    "name": traits.canonical.name,
                    "aethyr": traits.canonical.aethyr,
                    "aethyr_number": traits.canonical.aethyr_number,
                    "region": traits.canonical.region,
                    "correspondence": traits.canonical.correspondence,
                    "personality": traits.canonical.personality,
                    "domain": traits.canonical.domain,
                    "visual_motif": traits.canonical.visual_motif,
                    "letter_influence": traits.canonical.letter_influence
                },
                "enhanced": {
                    name: {
                        "trait_name": trait.trait_name,
                        "definition": trait.definition,
                        "source": trait.source,
                        "correspondences": trait.correspondences,
                        "practical_application": trait.practical_application
                    }
                    for name, trait in traits.enhanced.items()
                },
                "mystical": {
                    "element": traits.mystical.element.value,
                    "alignment": traits.mystical.alignment.value,
                    "zodiac": traits.mystical.zodiac,
                    "tarot": traits.mystical.tarot,
                    "sephirot": traits.mystical.sephirot,
                    "angel": traits.mystical.angel,
                    "number": traits.mystical.number
                },
                "personality": {
                    "archetype": traits.personality.archetype,
                    "primary_traits": traits.personality.primary_traits,
                    "secondary_traits": traits.personality.secondary_traits,
                    "teaching_style": traits.personality.teaching_style,
                    "approach": traits.personality.approach,
                    "tone": traits.personality.tone
                },
                "visual": {
                    "form_type": traits.visual.form_type,
                    "color_scheme": traits.visual.color_scheme,
                    "sacred_geometry": traits.visual.sacred_geometry,
                    "manifestation": traits.visual.manifestation,
                    "effects": traits.visual.effects
                },
                "version": traits.version,
                "last_updated": traits.last_updated
            }, f, indent=2)
            
        logger.info(f"✨ Traits saved to {output_path}")
        
    except Exception as e:
        logger.error(f"Error generating traits: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 