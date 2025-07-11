#!/usr/bin/env python3
"""
Sacred Geometry Reading Generator CLI

This script generates sacred geometry readings with Bitcoin integration.
"""

import argparse
import asyncio
import json
import os
from datetime import datetime
from typing import Optional

from core.mystical_systems.sacred_geometry_system import SacredGeometrySystem
from core.mystical_systems.sacred_geometry_system.schemas import SacredGeometrySystemConfig
from core.utils.custom_logging import setup_logger

logger = setup_logger("sacred_geometry_cli")

def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate sacred geometry readings with Bitcoin integration"
    )
    
    parser.add_argument(
        "--complexity",
        type=int,
        choices=range(1, 11),
        help="Reading complexity (1-10)"
    )
    
    parser.add_argument(
        "--txid",
        type=str,
        help="Optional Bitcoin transaction ID for entropy"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="sacred_geometry_reading.json",
        help="Output file path for the reading (default: sacred_geometry_reading.json)"
    )
    
    parser.add_argument(
        "--art-output",
        type=str,
        help="Optional output path for generated sacred geometry art"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Optional path to configuration JSON file"
    )
    
    return parser.parse_args()

def load_config(config_path: Optional[str] = None) -> dict:
    """Load system configuration"""
    if config_path and os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
    else:
        config = {
            "min_complexity": 1,
            "max_complexity": 10,
            "resonance_threshold": 0.7,
            "power_scale": 100,
            "ritual_points_required": 3
        }
    
    return config

def save_reading(reading: dict, output_path: str):
    """Save reading to JSON file"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(reading, f, indent=2)
    
    logger.info(f"Saved reading to {output_path}")

async def main():
    """Main CLI function"""
    args = parse_args()
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        # Initialize system
        system = SacredGeometrySystem(config)
        logger.info("Initialized Sacred Geometry system")
        
        # Generate reading
        profile = await system.generate_profile(
            txid=args.txid,
            complexity=args.complexity
        )
        
        # Format output
        reading = system.format_output(profile)
        
        # Save reading
        save_reading(reading, args.output)
        
        # Generate art if requested
        if args.art_output:
            art_path = await system.generate_art(profile, args.art_output)
            logger.info(f"Generated sacred geometry art: {art_path}")
        
        logger.info("Sacred geometry reading generation complete")
        
    except Exception as e:
        logger.error(f"Error generating reading: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 