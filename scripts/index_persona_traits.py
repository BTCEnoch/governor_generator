#!/usr/bin/env python3
"""
Persona Traits Indexer
Processes all governor dossiers to build a comprehensive index of persona traits
with support for hierarchical relationships and trait compatibility rules
"""

import json
import os
from pathlib import Path
import logging
from typing import Dict, List, Set, Optional

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Enhanced definitions with hierarchical relationships
TRAIT_HIERARCHY = {
    "role_archetype": {
        "messenger": ["herald", "harbinger"],
        "wisdom_keeper": ["oracle", "chronicler", "archivist"],
        "protector": ["guardian", "warden", "protector"],
        "teacher": ["guide", "master", "high_priestess"],
        "creator": ["alchemist", "artificer", "weaver"],
        "transformer": ["catalyst", "liberator", "provocateur"],
        "observer": ["mirror", "judge"]
    }
}

# Trait compatibility rules
INCOMPATIBLE_TRAITS = {
    "alignments": [
        {"lawful_good", "chaotic_neutral"},
        {"true_neutral", "lawful_good"},
        {"neutral_evil", "lawful_good"}
    ],
    "approaches": [
        {"deceiving", "direct"},
        {"judging", "empathizing"}
    ]
}

# Enhanced quality context with more nuanced definitions
QUALITY_CONTEXT = {
    "good": {
        "approach": "Masterful application bringing consistent positive outcomes",
        "tone": "Perfectly balanced expression enhancing divine communication"
    },
    "average": {
        "approach": "Competent but occasionally inconsistent application",
        "tone": "Functional but sometimes lacking in subtlety or depth"
    },
    "bad": {
        "approach": "Problematic application often leading to unintended consequences",
        "tone": "Disruptive or ineffective expression hindering divine connection"
    }
}

# Base definitions for all trait types
BASE_DEFINITIONS = {
    "role_archetype": {
        "herald": "Divine messenger who announces celestial decrees and prophecies",
        "oracle": "Channel of divine wisdom and prophetic insights",
        "guardian": "Protector of sacred knowledge and divine boundaries",
        "guide": "Spiritual mentor who leads souls through mystical realms",
        "alchemist": "Master of divine transformation and spiritual refinement",
        "artificer": "Creator of sacred tools and mystical artifacts",
        "catalyst": "Initiator of spiritual transformation and growth",
        "chronicler": "Keeper of divine records and celestial histories",
        "harbinger": "Announcer of significant spiritual changes",
        "judge": "Arbiter of divine law and cosmic justice",
        "liberator": "Breaker of spiritual bonds and limitations",
        "master": "Expert in specific domains of divine knowledge",
        "mirror": "Reflector of divine truth and self-knowledge",
        "protector": "Guardian of sacred beings and divine essence",
        "provocateur": "Challenger of spiritual complacency",
        "warden": "Keeper of divine boundaries and sacred spaces",
        "weaver": "Creator of spiritual connections and divine patterns",
        "high_priestess": "Channel of divine mysteries and sacred wisdom",
        "archivist": "Preserver of divine knowledge and sacred records"
    },
    "alignment": {
        "lawful_good": "Upholds divine order for the benefit of all",
        "lawful_neutral": "Maintains cosmic law without bias",
        "neutral_good": "Promotes harmony while remaining flexible",
        "true_neutral": "Maintains perfect balance in all things",
        "chaotic_good": "Creates positive change through divine inspiration",
        "chaotic_neutral": "Embodies divine unpredictability",
        "neutral_evil": "Serves self-interest over divine purpose"
    },
    "orientation": {
        "balanced": "Maintains harmony between inner and outer realms",
        "inward_focused": "Concentrates on internal spiritual development",
        "outward_focused": "Directs energy toward external manifestation"
    },
    "polarity": {
        "balanced_flux": "Harmonious flow between different states of being",
        "constructive": "Builds and strengthens divine connections",
        "destructive": "Breaks down barriers to spiritual growth"
    },
    "approach": {
        "challenging": "Tests and pushes boundaries of understanding",
        "comforting": "Provides solace and spiritual support",
        "deceiving": "Uses misdirection for higher purpose",
        "demonstrating": "Shows through direct example",
        "empathizing": "Connects through shared understanding",
        "encouraging": "Motivates spiritual growth",
        "guiding": "Leads the way on spiritual paths",
        "inspiring": "Awakens divine potential",
        "judging": "Evaluates according to divine law",
        "mediating": "Balances opposing forces",
        "mirroring": "Reflects truth back to the seeker",
        "naming": "Defines and categorizes divine aspects",
        "negotiating": "Finds harmony between different paths",
        "observing": "Watches and learns from divine patterns",
        "prophesying": "Reveals future possibilities",
        "teaching": "Imparts divine wisdom"
    },
    "tone": {
        "analytical": "Systematic examination of divine principles",
        "stern": "Strict adherence to divine law",
        "direct": "Clear and straightforward divine communication",
        "mysterious": "Veiled in divine mystery",
        "nurturing": "Supportive of spiritual growth",
        "playful": "Lightens the path with divine joy"
    },
    "virtue": {
        "vision": "Divine foresight and prophetic insight",
        "prudence": "Wise judgment in divine matters",
        "discernment": "Ability to perceive divine truth",
        "wisdom": "Deep understanding of divine principles",
        "patience": "Steadfast endurance in divine work",
        "courage": "Strength to face divine challenges"
    },
    "flaw": {
        "obsession": "Excessive focus on specific divine aspects",
        "rigidity": "Inflexible adherence to divine patterns",
        "aloofness": "Detachment from earthly concerns",
        "pride": "Overconfidence in divine connection",
        "doubt": "Uncertainty in divine purpose",
        "fear": "Hesitation before divine mysteries"
    }
}

def get_trait_hierarchy(trait_name: str) -> Optional[str]:
    """Get the hierarchical category for a trait"""
    for category, hierarchy in TRAIT_HIERARCHY.items():
        for parent, children in hierarchy.items():
            if trait_name.lower() in children:
                return parent
    return None

def validate_trait_compatibility(traits: Dict[str, List[dict]]) -> List[str]:
    """Validate trait combinations and return any conflicts"""
    conflicts = []
    
    for category, incompatible_sets in INCOMPATIBLE_TRAITS.items():
        if category not in traits:
            continue
            
        current_traits = {t["name"].lower() for t in traits[category]}
        for incompatible_set in incompatible_sets:
            if len(incompatible_set & current_traits) > 1:
                conflicts.append(
                    f"Incompatible {category}: {', '.join(incompatible_set & current_traits)}"
                )
    
    return conflicts

def parse_variant_info(name: str) -> tuple[str, List[str]]:
    """Parse a trait name into base name and nested variant information"""
    base_name = name.split("(")[0].strip()
    variants = []
    
    # Extract all nested variants
    start = 0
    depth = 0
    variant = ""
    
    for i, char in enumerate(name):
        if char == "(":
            if depth == 0:
                start = i + 1
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                variant = name[start:i].strip()
                if variant:
                    variants.append(variant)
    
    return base_name, variants

def merge_duplicate_traits(entries: Dict[str, List[dict]]) -> Dict[str, List[dict]]:
    """Merge duplicate traits with different qualities and handle nested variants"""
    for category in entries:
        if category not in ["approaches", "tones"]:
            continue
            
        # Group by base name
        grouped = {}
        for entry in entries[category]:
            base_name, variants = parse_variant_info(entry["name"])
            if base_name not in grouped:
                grouped[base_name] = []
            entry["variants"] = variants
            grouped[base_name].append(entry)
        
        # Merge entries with same base name
        merged = []
        for base_name, variants in grouped.items():
            # Sort by quality (bad -> average -> good)
            quality_order = {"bad": 0, "average": 1, "good": 2}
            variants.sort(key=lambda x: quality_order[x["quality"]])
            
            # Keep only one entry per quality
            seen_qualities = set()
            for variant in variants:
                if variant["quality"] not in seen_qualities:
                    # Update ID to include quality and variants
                    variant_suffix = "_".join(v.lower().replace(" ", "_") for v in variant["variants"])
                    variant["id"] = f"{variant['id']}_{variant['quality']}"
                    if variant_suffix:
                        variant["id"] = f"{variant['id']}_{variant_suffix}"
                    
                    # Update definition with quality context and variants
                    base_def = BASE_DEFINITIONS.get(category.rstrip("s"), {}).get(
                        base_name.lower().replace(" ", "_").replace("-", "_"), ""
                    )
                    
                    if base_def:
                        quality_context = QUALITY_CONTEXT[variant["quality"]][category.rstrip("s")]
                        variant["definition"] = f"{base_def} - {quality_context}"
                        if variant["variants"]:
                            variant_desc = " and ".join(variant["variants"])
                            variant["definition"] = f"{variant['definition']} (Specifically: {variant_desc})"
                    else:
                        # If no base definition, use the name as a fallback
                        quality_context = QUALITY_CONTEXT[variant["quality"]][category.rstrip("s")]
                        variant["definition"] = f"{base_name} - {quality_context}"
                        if variant["variants"]:
                            variant_desc = " and ".join(variant["variants"])
                            variant["definition"] = f"{variant['definition']} (Specifically: {variant_desc})"
                    
                    merged.append(variant)
                    seen_qualities.add(variant["quality"])
        
        entries[category] = merged
    
    return entries

def deduplicate_entries(entries: Dict[str, List[dict]]) -> Dict[str, List[dict]]:
    """Deduplicate entries while preserving definitions and handling hierarchical relationships"""
    for category in entries:
        # Group by ID
        grouped = {}
        for entry in entries[category]:
            entry_id = entry["id"]
            if entry_id not in grouped:
                base_name, variants = parse_variant_info(entry["name"])
                
                if category in ["approaches", "tones"]:
                    # Handle approaches and tones with quality levels
                    base_def = BASE_DEFINITIONS.get(category.rstrip("s"), {}).get(
                        base_name.lower().replace(" ", "_").replace("-", "_"), ""
                    )
                    quality_context = QUALITY_CONTEXT[entry["quality"]][category.rstrip("s")]
                    
                    if base_def:
                        entry["definition"] = f"{base_def} - {quality_context}"
                    else:
                        entry["definition"] = f"{base_name} - {quality_context}"
                        
                    if variants:
                        variant_desc = " and ".join(variants)
                        entry["definition"] = f"{entry['definition']} (Specifically: {variant_desc})"
                else:
                    # Handle other traits with hierarchical relationships
                    base_def = BASE_DEFINITIONS.get(category.rstrip("s"), {}).get(
                        base_name.lower().replace(" ", "_").replace("-", "_"), ""
                    )
                    
                    if category == "role_archetypes":
                        hierarchy = get_trait_hierarchy(base_name.lower())
                        hierarchy_prefix = f"[{hierarchy}] " if hierarchy else ""
                        base_def = f"{hierarchy_prefix}{base_def}" if base_def else base_def
                    
                    if variants:
                        variant_desc = " and ".join(variants)
                        entry["definition"] = f"{base_def} - Specifically: {variant_desc}" if base_def else f"{base_name} - {variant_desc}"
                    else:
                        entry["definition"] = base_def or f"{base_name}"
                
                grouped[entry_id] = entry
        
        # Convert back to list
        entries[category] = list(grouped.values())
    
    return entries

def get_trait_definition(name: str, category: str, variant_info: str = "", quality: Optional[str] = None) -> str:
    """Get appropriate definition for a trait based on its type, context, and hierarchy"""
    # Parse base name and any nested variants from the name itself
    base_name, variants = parse_variant_info(name)
    
    # Add any additional variant info to the variants list
    if variant_info and variant_info not in variants:
        variants.append(variant_info)
    
    # Convert category to lookup key
    lookup_category = category.rstrip("s")  # Remove trailing 's'
    lookup_name = base_name.lower().replace(" ", "_").replace("-", "_")
    
    # Get hierarchical information for role archetypes
    hierarchy_prefix = ""
    if lookup_category == "role_archetype":
        hierarchy = get_trait_hierarchy(lookup_name)
        hierarchy_prefix = f"[{hierarchy}] " if hierarchy else ""
    
    # Get base definition
    base_def = BASE_DEFINITIONS.get(lookup_category, {}).get(lookup_name, "")
    
    # Build the complete definition
    if base_def:
        # Start with hierarchy prefix if applicable
        definition = f"{hierarchy_prefix}{base_def}"
        
        # Add quality context for approaches and tones
        if quality and lookup_category in ["approach", "tone"]:
            quality_context = QUALITY_CONTEXT[quality][lookup_category]
            definition = f"{definition} - {quality_context}"
        
        # Add variant information if present
        if variants:
            variant_desc = " and ".join(variants)
            definition = f"{definition} (Specifically: {variant_desc})"
    else:
        # Fallback definition if no base definition exists
        definition = base_name
        if quality and lookup_category in ["approach", "tone"]:
            quality_context = QUALITY_CONTEXT[quality][lookup_category]
            definition = f"{definition} - {quality_context}"
        if variants:
            variant_desc = " and ".join(variants)
            definition = f"{definition} (Specifically: {variant_desc})"
    
    return definition or "Definition pending"

def load_json(file_path):
    """Load JSON file safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading {file_path}: {e}")
        return None

def extract_traits_from_dossier(data):
    """Extract traits from a dossier's persona data"""
    traits = {
        "role_archetypes": [],
        "alignments": [],
        "orientations": [],
        "polarities": [],
        "approaches": [],
        "tones": [],
        "virtues": [],
        "flaws": []
    }
    
    if not data.get("persona"):
        return traits
        
    persona = data["persona"]
    polar_traits = persona.get("polar_traits", {})
    
    # Extract role archetype
    if role := polar_traits.get("role_archetype"):
        traits["role_archetypes"].append({
            "id": role.lower().replace(" ", "_"),
            "name": role,
            "category": "role_archetypes"
        })
    
    # Extract alignment
    if alignment := polar_traits.get("motive_alignment"):
        traits["alignments"].append({
            "id": alignment.lower().replace(" ", "_"),
            "name": alignment,
            "category": "alignments"
        })
    
    # Extract orientation
    if orientation := polar_traits.get("orientation"):
        traits["orientations"].append({
            "id": orientation.lower().replace(" ", "_"),
            "name": orientation,
            "category": "orientations"
        })
    
    # Extract polarity
    if polarity := polar_traits.get("polarity"):
        traits["polarities"].append({
            "id": polarity.lower().replace(" ", "_"),
            "name": polarity,
            "category": "polarities"
        })
    
    # Extract virtues
    for virtue in polar_traits.get("virtues", []):
        traits["virtues"].append({
            "id": virtue.lower().replace(" ", "_"),
            "name": virtue,
            "category": "virtues"
        })
    
    # Extract flaws
    for flaw in polar_traits.get("flaws", []):
        traits["flaws"].append({
            "id": flaw.lower().replace(" ", "_"),
            "name": flaw,
            "category": "flaws"
        })
    
    # Extract approaches with qualities
    approaches = persona.get("approaches", {})
    for quality, approach in approaches.items():
        if approach:
            base_id = approach.lower().replace(" ", "_").replace("-", "_")
            if "(" in approach:
                base_name = approach.split("(")[0].strip()
                variant_info = approach[approach.find("(")+1:approach.find(")")]
                trait_id = f"{base_name.lower().replace(' ', '_')}_{variant_info.lower().replace(' ', '_')}_{quality}"
            else:
                trait_id = f"{base_id}_{quality}"
            traits["approaches"].append({
                "id": trait_id,
                "name": approach,
                "category": "approaches",
                "quality": quality
            })
    
    # Extract tones with qualities
    tones = persona.get("tones", {})
    for quality, tone in tones.items():
        if tone:
            base_id = tone.lower().replace(" ", "_").replace("-", "_")
            if "(" in tone:
                base_name = tone.split("(")[0].strip()
                variant_info = tone[tone.find("(")+1:tone.find(")")]
                trait_id = f"{base_name.lower().replace(' ', '_')}_{variant_info.lower().replace(' ', '_')}_{quality}"
            else:
                trait_id = f"{base_id}_{quality}"
            traits["tones"].append({
                "id": trait_id,
                "name": tone,
                "category": "tones",
                "quality": quality
            })
    
    return traits

def process_dossiers(dossier_dir, output_file):
    """Process all dossiers and update the persona traits index"""
    # Initialize traits index
    traits_index = {
        "schema_version": "1.0.0",
        "last_updated": "2025-07-04T22:07:00.000Z",
        "entries": {
            "role_archetypes": [],
            "alignments": [],
            "orientations": [],
            "polarities": [],
            "approaches": [],
            "tones": [],
            "virtues": [],
            "flaws": []
        }
    }
    
    # Process each dossier
    for file_name in os.listdir(dossier_dir):
        if not file_name.endswith(".json"):
            continue
            
        file_path = os.path.join(dossier_dir, file_name)
        logging.info(f"Processing {file_path}")
        
        # Load dossier data
        data = load_json(file_path)
        if not data:
            continue
            
        # Extract traits from dossier
        traits = extract_traits_from_dossier(data)
        
        # Add traits to index
        for category in traits:
            traits_index["entries"][category].extend(traits[category])
    
    # Merge duplicate traits with different qualities
    traits_index["entries"] = merge_duplicate_traits(traits_index["entries"])
    
    # Deduplicate entries and add definitions
    traits_index["entries"] = deduplicate_entries(traits_index["entries"])
    
    # Validate trait compatibility
    conflicts = validate_trait_compatibility(traits_index["entries"])
    if conflicts:
        logging.warning("Trait compatibility conflicts detected:")
        for conflict in conflicts:
            logging.warning(conflict)
    
    # Save updated index
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(traits_index, f, indent=2)
        logging.info(f"Updated traits index saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving traits index: {e}")

if __name__ == "__main__":
    dossier_dir = "governor_dossier"
    output_file = "core/governors/traits/persona/persona_traits.json"
    process_dossiers(dossier_dir, output_file) 