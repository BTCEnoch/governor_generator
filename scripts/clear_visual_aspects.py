"""Script to clear visual aspects fields from all governors."""

import json
import os
from pathlib import Path

# Empty visual aspects template with truly empty values
EMPTY_VISUAL_ASPECTS = {
    "form": {
        "name": "",
        "description": ""
    },
    "color": "",
    "geometry": {
        "patterns": [],
        "complexity": None
    },
    "environment": {
        "effect_type": None,
        "radius": None,
        "intensity": None
    },
    "time_variations": None,
    "energy_signature": None,
    "symbol_set": None,
    "light_shadow": None,
    "special_properties": []
}

def clear_visual_aspects():
    """Clear visual aspects from all governor dossiers while preserving other traits."""
    dossier_dir = Path("governor_dossier")
    count = 0
    
    # Process all .json files in the governor_dossier directory
    for file_path in dossier_dir.glob("*.json"):
        if file_path.name.startswith("visual_aspects"):
            continue
            
        try:
            # Load governor data
            with open(file_path, 'r', encoding='utf-8') as f:
                governor_data = json.load(f)
                
            # Update visual aspects to empty template
            governor_data["visual_aspects"] = EMPTY_VISUAL_ASPECTS.copy()
                
            # Save updated governor data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(governor_data, f, indent=2)
                
            count += 1
            print(f"Cleared visual aspects for {file_path.name}")
                
        except Exception as e:
            print(f"Error processing {file_path.name}: {str(e)}")
            
    print(f"\nSuccessfully cleared visual aspects for {count} governors")

if __name__ == "__main__":
    clear_visual_aspects() 