import json
import os
from pathlib import Path
from typing import Dict, List, Any, Set

# Expected governor names (91 total)
EXPECTED_GOVERNORS = {
    'ABRIOND', 'ADVORPT', 'AMBRIOL', 'ANDISPI', 'ASPIAON', 'AXXIARG', 'AYDROPT',
    'CALZIRG', 'CHASLPO', 'CHIRZPA', 'COMANAN', 'CRALPIR', 'CRPANIB', 'CUCARPT',
    'DIALOIA', 'DOAGNIS', 'DOANZIN', 'DOCEPAX', 'DOXMAEL', 'GECAOND', 'GEDOONS',
    'GEMNIMB', 'GENADOL', 'GMTZIAM', 'LAPARIN', 'LAVACON', 'LAZDIXI', 'LAZHIIM',
    'LEXARPH', 'MATHVLA', 'MIRZIND', 'MOLPAND', 'NABAOMI', 'NIGRANA', 'NOCAMAL',
    'NOTIABI', 'OBUAORS', 'OCCODON', 'ODDIORG', 'ODRAXTI', 'OMAGRAP', 'ONIZIMP',
    'OPMACAS', 'ORANCIR', 'OSIDAIA', 'OXLOPAR', 'PABNIXP', 'PACASNA', 'PARAOAN',
    'PARZIBA', 'PASCOMB', 'POCISNI', 'PONODOL', 'POPHAND', 'POTHNIR', 'PRISTAC',
    'RANGLAM', 'RONOOMB', 'SAMAPHA', 'SAXTOMP', 'SAZIAMI', 'SIGMORF', 'SOAGEEL',
    'SOCHIAL', 'TABITOM', 'TAHAMDO', 'TAOAGLA', 'TAPAMAL', 'TASTOZO', 'TEDOOND',
    'THOTANP', 'TIARPAX', 'TOANTOM', 'TOCARZI', 'TODNAON', 'TORZOXI', 'TOTOCAN',
    'USNARDA', 'VALGARS', 'VASTRIM', 'VAUAAMP', 'VIROOLI', 'VIVIPOS', 'VIXPALG',
    'VOANAMB', 'YALPAMB', 'ZAFASAI', 'ZAMFRES', 'ZAXANIN', 'ZILDRON', 'ZIRZIRD'
}

# Expected empty visual aspects structure
EMPTY_VISUAL_ASPECTS = {
    "form": {
        "name": "Unknown",
        "description": "Undefined form"
    },
    "color": "",
    "geometry": {
        "patterns": [],
        "complexity": 0
    },
    "environment": {
        "effect_type": 0,
        "radius": 0,
        "intensity": 0
    },
    "time_variations": 0,
    "energy_signature": 0,
    "symbol_set": 0,
    "light_shadow": 0,
    "special_properties": []
}

def load_trait_definitions() -> Dict[str, Any]:
    """Load all trait definitions from indexes."""
    indexes_dir = Path("data/governors/indexes")
    definitions = {}
    
    # Load all JSON files from indexes
    for json_file in indexes_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                definitions[json_file.stem] = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load {json_file.name}: {str(e)}")
            
    return definitions

def validate_visual_aspects(visual_aspects: Dict[str, Any], governor_name: str) -> List[str]:
    """Validate that visual aspects are properly empty."""
    errors = []
    
    if visual_aspects != EMPTY_VISUAL_ASPECTS:
        errors.append(f"{governor_name}: Visual aspects are not properly empty")
        
    return errors

def validate_persona_traits(persona: Dict[str, Any], governor_name: str, trait_defs: Dict[str, Any]) -> List[str]:
    """Validate persona traits against definitions."""
    errors = []
    
    # Required persona fields
    required_fields = {
        "name", "title", "element", "aethyr", "essence", "angelic_role",
        "knowledge_base", "archetypal_correspondences", "polar_traits",
        "approaches", "tones"
    }
    
    # Check required fields exist
    for field in required_fields:
        if field not in persona:
            errors.append(f"{governor_name}: Missing required persona field '{field}'")
            
    # Validate knowledge base
    if "knowledge_base" in persona:
        if not isinstance(persona["knowledge_base"], list):
            errors.append(f"{governor_name}: knowledge_base must be a list")
        elif len(persona["knowledge_base"]) < 1:
            errors.append(f"{governor_name}: knowledge_base cannot be empty")
            
    # Validate archetypal correspondences
    if "archetypal_correspondences" in persona:
        required_correspondences = {"tarot", "sephirot", "zodiac_sign", "zodiac_angel", "numerology"}
        for field in required_correspondences:
            if field not in persona["archetypal_correspondences"]:
                errors.append(f"{governor_name}: Missing archetypal correspondence '{field}'")
                
    # Validate polar traits
    if "polar_traits" in persona:
        required_polar = {
            "baseline_approach", "baseline_tone", "motive_alignment",
            "role_archetype", "orientation", "polarity", "self_regard",
            "virtues", "flaws"
        }
        for field in required_polar:
            if field not in persona["polar_traits"]:
                errors.append(f"{governor_name}: Missing polar trait '{field}'")
                
        # Validate virtues and flaws are lists
        if "virtues" in persona["polar_traits"]:
            if not isinstance(persona["polar_traits"]["virtues"], list):
                errors.append(f"{governor_name}: virtues must be a list")
            elif len(persona["polar_traits"]["virtues"]) < 1:
                errors.append(f"{governor_name}: virtues cannot be empty")
                
        if "flaws" in persona["polar_traits"]:
            if not isinstance(persona["polar_traits"]["flaws"], list):
                errors.append(f"{governor_name}: flaws must be a list")
            elif len(persona["polar_traits"]["flaws"]) < 1:
                errors.append(f"{governor_name}: flaws cannot be empty")
                
    return errors

def validate_governor(governor_data: Dict[str, Any], governor_name: str, trait_defs: Dict[str, Any]) -> List[str]:
    """Validate a single governor's structure and traits."""
    errors = []
    
    # Required top-level fields
    required_fields = {"governor_name", "governor_id", "persona", "visual_aspects"}
    for field in required_fields:
        if field not in governor_data:
            errors.append(f"{governor_name}: Missing required field '{field}'")
            
    # Validate governor name matches
    if governor_data.get("governor_name") != governor_name:
        errors.append(f"{governor_name}: governor_name mismatch")
        
    if governor_data.get("governor_id") != governor_name:
        errors.append(f"{governor_name}: governor_id mismatch")
        
    # Validate visual aspects
    if "visual_aspects" in governor_data:
        errors.extend(validate_visual_aspects(governor_data["visual_aspects"], governor_name))
        
    # Validate persona traits
    if "persona" in governor_data:
        errors.extend(validate_persona_traits(governor_data["persona"], governor_name, trait_defs))
        
    return errors

def validate_all_governors():
    """Validate all governors in the dossier."""
    print("Starting governor validation...")
    
    # Load trait definitions
    trait_defs = load_trait_definitions()
    print(f"Loaded {len(trait_defs)} trait definition files")
    
    # Get all governor files
    dossier_dir = Path("governor_dossier")
    found_governors = set()
    all_errors = []
    
    # Process each governor file
    for file_path in dossier_dir.glob("*.json"):
        if file_path.name.startswith("visual_aspects"):
            continue
            
        governor_name = file_path.stem
        found_governors.add(governor_name)
        
        try:
            # Load governor data
            with open(file_path, 'r', encoding='utf-8') as f:
                governor_data = json.load(f)
                
            # Validate governor
            errors = validate_governor(governor_data, governor_name, trait_defs)
            if errors:
                all_errors.extend(errors)
                
        except Exception as e:
            all_errors.append(f"Error processing {governor_name}: {str(e)}")
            
    # Check for missing governors
    missing_governors = EXPECTED_GOVERNORS - found_governors
    if missing_governors:
        all_errors.append(f"Missing governors: {', '.join(sorted(missing_governors))}")
        
    # Check for unexpected governors
    unexpected_governors = found_governors - EXPECTED_GOVERNORS
    if unexpected_governors:
        all_errors.append(f"Unexpected governors: {', '.join(sorted(unexpected_governors))}")
        
    # Print results
    print(f"\nValidation complete!")
    print(f"Found {len(found_governors)} governors")
    print(f"Expected {len(EXPECTED_GOVERNORS)} governors")
    
    if all_errors:
        print("\nErrors found:")
        for error in all_errors:
            print(f"- {error}")
    else:
        print("\nNo errors found! All governors are valid.")

if __name__ == "__main__":
    validate_all_governors() 