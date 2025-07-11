#!/usr/bin/env python3
"""
I Ching Reading Generator CLI

This script provides a command-line interface for generating I Ching readings
using the Bitcoin-integrated I Ching system.
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

from core.mystical_systems.iching_system import IChingSystem
from core.utils.custom_logging import setup_logger

logger = setup_logger("iching_cli")

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate I Ching readings using Bitcoin-integrated divination"
    )
    
    parser.add_argument(
        "-q", "--question",
        help="Question or topic for the reading",
        type=str,
        required=True
    )
    
    parser.add_argument(
        "-s", "--seed",
        help="Optional seed for deterministic generation",
        type=str,
        default=None
    )
    
    parser.add_argument(
        "-t", "--txid",
        help="Optional Bitcoin transaction ID for resonance",
        type=str,
        default=None
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Optional JSON file to save the reading",
        type=str,
        default=None
    )
    
    parser.add_argument(
        "--pretty",
        help="Pretty-print the output",
        action="store_true"
    )
    
    return parser.parse_args()

def format_reading_output(profile_data):
    """Format the reading output for display"""
    initial = profile_data["initial_hexagram"]
    transformed = profile_data.get("transformed_hexagram")
    
    output = []
    output.extend([
        "\n=== I CHING READING ===\n",
        f"Question: {profile_data['metadata']['question']}\n",
        f"\nInitial Hexagram: {initial['unicode']} - {initial['name']} (#{initial['number']})",
        f"\nJudgment: {initial['judgment']}",
        f"\nImage: {initial['image']}",
        "\nLines:"
    ])
    
    for line in initial["lines"]:
        line_str = f"  Line {line['position']}: "
        if line['is_changing']:
            line_str += "[CHANGING] "
        line_str += "Yang" if line["value"] in [8, 9] else "Yin"
        if line["meaning"]:
            line_str += f" - {line['meaning']}"
        output.append(line_str)
        
    if transformed:
        output.extend([
            f"\nTransformed Hexagram: {transformed['unicode']} - {transformed['name']} (#{transformed['number']})",
            f"\nJudgment: {transformed['judgment']}",
            f"\nImage: {transformed['image']}"
        ])
        
    if profile_data["bitcoin_resonance"] is not None:
        output.extend([
            "\nBitcoin Resonances:",
            f"  Resonance: {profile_data['bitcoin_resonance']:.2f}",
            f"  Chain Harmony: {profile_data['chain_harmony']:.2f}"
        ])
        
    output.extend([
        "\nAttributes:"
    ])
    for attr in profile_data["attributes"]:
        output.append(f"  {attr['name']}: {attr['value']} - {attr['description']}")
        
    return "\n".join(output)

async def main():
    """Main CLI function"""
    args = parse_args()
    
    try:
        # Prepare input data
        data = {
            "question": args.question
        }
        if args.seed:
            data["seed"] = args.seed
        if args.txid:
            data["txid"] = args.txid
            
        # Generate reading
        async with IChingSystem() as system:
            profile = await system.generate_profile(data)
            output_data = system.format_output(profile)
            
        # Display reading
        if args.pretty:
            print(format_reading_output(output_data))
        else:
            json.dump(output_data, sys.stdout, indent=2 if args.pretty else None)
            print()  # Add newline
            
        # Save to file if requested
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2)
            logger.info(f"Reading saved to {output_path}")
            
    except Exception as e:
        logger.error(f"Error generating reading: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 