#!/usr/bin/env python3
"""
Tradition Organization Script
Moves governor archive files into proper knowledge base structure
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, Any
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Mapping of traditions to their categories
TRADITION_CATEGORIES = {
    'eastern': ['taoism', 'kuji_kiri', 'i_ching'],
    'western': ['hermetic_philosophy', 'kabbalistic_mysticism', 'golden_dawn', 'thelema'],
    'ancient': ['egyptian_magic', 'norse_traditions', 'celtic_druidic', 'classical_philosophy'],
    'esoteric': ['enochian_magic', 'tarot_knowledge', 'sacred_geometry', 'gnostic_traditions'],
    'modern': ['chaos_magic', 'quantum_physics'],
    'universal': []  # Will be created but no direct mappings
}

def ensure_directory(path: Path) -> None:
    """Ensure directory exists, create if not"""
    if not path.exists():
        path.mkdir(parents=True)
        logging.info(f"Created directory: {path}")

def extract_concepts(data: Dict[str, Any]) -> list:
    """Extract concepts from governor archive format"""
    logging.debug("Extracting concepts...")
    concepts = []
    
    # Extract from key concepts
    for concept in data.get("key_concepts", []):
        logging.debug(f"Processing concept: {concept}")
        if isinstance(concept, dict):
            concept_entry = {
                "id": concept["name"].lower().replace(" ", "_").replace("(", "").replace(")", ""),
                "name": concept["name"],
                "category": "core_concept",
                "definition": concept.get("core_principle", ""),
                "attributes": {
                    "wisdom": concept.get("practical_wisdom", ""),
                    "trigger": concept.get("interaction_triggers", []),
                    "quote": concept.get("wisdom_quotes", []),
                    "personality_influence": concept.get("personality_influence", ""),
                    "decision_making_style": concept.get("decision_making_style", ""),
                    "communication_approach": concept.get("communication_approach", ""),
                    "conflict_resolution": concept.get("conflict_resolution", ""),
                    "growth_potential": concept.get("growth_potential", "")
                },
                "correspondences": [],
                "sources": [concept.get("source_tradition", "")]
            }
            concepts.append(concept_entry)
    
    # Extract from wisdom teachings
    for wisdom in data.get("wisdom_teachings", []):
        if wisdom:  # Skip empty strings
            logging.debug(f"Processing wisdom teaching: {wisdom}")
            wisdom_entry = {
                "id": wisdom.lower().replace(" ", "_").replace("(", "").replace(")", ""),
                "name": wisdom,
                "category": "wisdom_teaching",
                "definition": data.get("overview", ""),
                "attributes": {
                    "governor_essence": data.get("governor_essence", ""),
                    "growth_paths": data.get("growth_paths", []),
                    "ethical_principles": data.get("ethical_principles", [])
                },
                "correspondences": [],
                "sources": []
            }
            concepts.append(wisdom_entry)
    
    return concepts

def extract_practices(data: Dict[str, Any]) -> list:
    """Extract practices from governor archive format"""
    logging.debug("Extracting practices...")
    practices = []
    
    # Extract from interaction patterns
    for pattern in data.get("interaction_patterns", []):
        if pattern:  # Skip empty strings
            logging.debug(f"Processing interaction pattern: {pattern}")
            practice_entry = {
                "id": pattern.lower().replace(" ", "_").replace("(", "").replace(")", ""),
                "name": pattern,
                "category": "interaction_pattern",
                "definition": "",
                "methods": data.get("communication_styles", []),
                "requirements": {
                    "tools": [],
                    "preparations": data.get("ethical_principles", [])
                },
                "stages": data.get("growth_paths", [])
            }
            practices.append(practice_entry)
    
    # Extract from decision frameworks
    for framework in data.get("decision_frameworks", []):
        if framework:  # Skip empty strings
            logging.debug(f"Processing decision framework: {framework}")
            framework_entry = {
                "id": framework.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("?", ""),
                "name": framework,
                "category": "decision_framework",
                "definition": data.get("overview", ""),
                "methods": data.get("ethical_principles", []),
                "requirements": {
                    "tools": [],
                    "preparations": data.get("power_dynamics", [])
                },
                "stages": data.get("relationship_approaches", [])
            }
            practices.append(framework_entry)
    
    return practices

def extract_figures(data: Dict[str, Any]) -> list:
    """Extract figures from governor archive format"""
    logging.debug("Extracting figures...")
    figures = []
    
    # Create a figure entry for the tradition itself
    figure_entry = {
        "id": data["tradition_name"].lower(),
        "name": data["display_name"],
        "category": "tradition_archetype",
        "definition": data.get("overview", ""),
        "dates": {},
        "roles": data.get("power_dynamics", []),
        "contributions": data.get("wisdom_teachings", []),
        "key_works": [],
        "attributes": {
            "governor_essence": data.get("governor_essence", ""),
            "conflict_styles": data.get("conflict_styles", []),
            "communication_styles": data.get("communication_styles", []),
            "relationship_approaches": data.get("relationship_approaches", [])
        }
    }
    figures.append(figure_entry)
    
    return figures

def extract_correspondences(data: Dict[str, Any]) -> list:
    """Extract correspondences from governor archive format"""
    logging.debug("Extracting correspondences...")
    correspondences = []
    
    # Extract from personality traits
    for trait in data.get("personality_traits", []):
        if trait:  # Skip empty strings
            logging.debug(f"Processing personality trait: {trait}")
            corr_entry = {
                "id": trait.lower().replace(" ", "_").replace("-", "_"),
                "name": trait,
                "category": "personality_correspondence",
                "definition": data.get("governor_essence", ""),
                "attributes": {
                    "growth_paths": data.get("growth_paths", []),
                    "ethical_principles": data.get("ethical_principles", []),
                    "power_dynamics": data.get("power_dynamics", []),
                    "conflict_styles": data.get("conflict_styles", [])
                },
                "related_concepts": [concept["name"] for concept in data.get("key_concepts", []) if isinstance(concept, dict)],
                "sources": []
            }
            correspondences.append(corr_entry)
    
    return correspondences

def process_archive_file(src_file: Path, tradition_name: str, base_dir: Path) -> None:
    """Process a single governor archive file and organize its contents"""
    logging.info(f"\nProcessing {tradition_name}...")
    
    try:
        # Find category for tradition
        category = next(
            (cat for cat, traditions in TRADITION_CATEGORIES.items() 
             if tradition_name.replace('_magic', '').replace('_knowledge', '') in traditions),
            'universal'
        )
        logging.debug(f"Found category {category} for tradition {tradition_name}")
        
        # Create tradition directory
        tradition_dir = base_dir / category / tradition_name
        ensure_directory(tradition_dir)
        
        logging.debug(f"Reading archive file: {src_file}")
        with open(src_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract components
        concepts = {
            "schema_version": "1.0.0",
            "last_updated": data.get("extraction_timestamp", "2025-07-04T22:07:00.000Z"),
            "entries": extract_concepts(data)
        }
        
        practices = {
            "schema_version": "1.0.0",
            "last_updated": data.get("extraction_timestamp", "2025-07-04T22:07:00.000Z"),
            "entries": extract_practices(data)
        }
        
        figures = {
            "schema_version": "1.0.0",
            "last_updated": data.get("extraction_timestamp", "2025-07-04T22:07:00.000Z"),
            "entries": extract_figures(data)
        }
        
        correspondences = {
            "schema_version": "1.0.0",
            "last_updated": data.get("extraction_timestamp", "2025-07-04T22:07:00.000Z"),
            "entries": extract_correspondences(data)
        }
        
        # Save all files
        logging.debug("Saving extracted data to files...")
        with open(tradition_dir / "concepts.json", 'w', encoding='utf-8') as f:
            json.dump(concepts, f, indent=2)
            
        with open(tradition_dir / "practices.json", 'w', encoding='utf-8') as f:
            json.dump(practices, f, indent=2)
            
        with open(tradition_dir / "figures.json", 'w', encoding='utf-8') as f:
            json.dump(figures, f, indent=2)
            
        with open(tradition_dir / "correspondences.json", 'w', encoding='utf-8') as f:
            json.dump(correspondences, f, indent=2)
            
        logging.info(f"✅ Successfully processed {tradition_name}")
        
    except Exception as e:
        logging.error(f"❌ Error processing {tradition_name}: {str(e)}", exc_info=True)

def main():
    """Main organization function"""
    logging.info("Starting tradition organization...")
    
    # Setup paths
    src_dir = Path("data/knowledge/archives/governor_archives")
    base_dir = Path("core/governors/traits/knowledge_base")
    
    logging.info(f"Source directory: {src_dir}")
    logging.info(f"Base directory: {base_dir}")
    
    # Create category directories
    for category in TRADITION_CATEGORIES:
        ensure_directory(base_dir / category)
    
    # Clean up any duplicate or incorrect directories
    if (base_dir / "traditions").exists():
        shutil.rmtree(base_dir / "traditions")
    if (base_dir / "western" / "golden_dawn_magic").exists():
        shutil.rmtree(base_dir / "western" / "golden_dawn_magic")
    
    # Process each archive file
    archive_files = list(src_dir.glob("*_governor_archive.json"))
    logging.info(f"Found {len(archive_files)} archive files to process")
    
    for src_file in archive_files:
        tradition_name = src_file.stem.replace("_governor_archive", "")
        # Fix tradition names
        if tradition_name == "enochian_magic":
            tradition_name = "enochian_magic"  # Keep the full name
        process_archive_file(src_file, tradition_name, base_dir)
        
    logging.info("\n🎉 Tradition organization complete!")

if __name__ == "__main__":
    main() 