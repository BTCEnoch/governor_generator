#!/usr/bin/env python3
"""
Enochian Magic Knowledge Database
Comprehensive database of Enochian magical concepts, Angels, Keys, and Aethyrs
Based on curated sources from Sacred Texts, Hermetic Library, and Archive.org
"""

from typing import List, Dict
import json
from pathlib import Path

from core.lighthouse.schemas.knowledge_schemas import KnowledgeEntry, KnowledgeType, ContentQuality, ProcessedTradition

def load_consolidated_data() -> Dict:
    """Load the consolidated Enochian data from JSON file"""
    consolidated_path = Path(__file__).parent / "consolidated" / "enochian_magic.json"
    if not consolidated_path.exists():
        raise FileNotFoundError(f"Consolidated data file not found at {consolidated_path}")
    
    with open(consolidated_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def convert_to_knowledge_entry(concept_data: Dict) -> KnowledgeEntry:
    """Convert consolidated JSON data to KnowledgeEntry format"""
    return KnowledgeEntry(
        id=concept_data["name"].lower().replace(" ", "_"),
        tradition="enochian_magic",
        title=concept_data["name"],
        summary=concept_data["core_principle"],
        full_content=concept_data["practical_wisdom"],
        knowledge_type=KnowledgeType.CONCEPT,
        tags=concept_data.get("interaction_triggers", []),
        related_concepts=[],  # Will be populated from relationships
        source_url="",  # Add source URL if available
        confidence_score=0.9,  # Default high confidence for consolidated data
        quality=ContentQuality.HIGH
    )

def create_enochian_tradition() -> ProcessedTradition:
    """Create the Enochian tradition from consolidated data"""
    consolidated_data = load_consolidated_data()
    
    entries = []
    
    # Convert key concepts to KnowledgeEntry format
    for concept in consolidated_data.get("key_concepts", []):
        entry = convert_to_knowledge_entry(concept)
        entries.append(entry)
    
    # Add personality traits
    for trait in consolidated_data.get("personality_traits", []):
        entries.append(KnowledgeEntry(
            id=f"trait_{trait}",
            tradition="enochian_magic",
            title=trait.capitalize(),
            summary=f"Enochian Magic personality trait: {trait}",
            full_content="",
            knowledge_type=KnowledgeType.CONCEPT,  # Using CONCEPT since TRAIT is not defined
            tags=["personality", "trait"],
            related_concepts=[],
            confidence_score=0.9,
            quality=ContentQuality.HIGH
        ))
    
    # Categorize entries by type
    principles = []
    practices = []
    systems = []
    concepts = entries  # All entries are concepts for now
    
    return ProcessedTradition(
        name="Enochian Magic",
        description="The complete system of Enochian magic as received by John Dee and Edward Kelley",
        total_entries=len(entries),
        principles=principles,
        practices=practices,
        systems=systems,
        concepts=concepts
    )

def get_enochian_entry_by_id(entry_id: str) -> KnowledgeEntry:
    """Retrieve a specific Enochian entry by ID"""
    tradition = create_enochian_tradition()
    for entry in tradition.get_all_entries():
        if entry.id == entry_id:
            return entry
    raise KeyError(f"Entry {entry_id} not found")

def search_enochian_by_tag(tag: str) -> List[KnowledgeEntry]:
    """Search Enochian entries by tag"""
    tradition = create_enochian_tradition()
    return [entry for entry in tradition.get_all_entries() if tag in entry.tags]

def get_all_enochian_entries() -> List[KnowledgeEntry]:
    """Get all Enochian entries"""
    tradition = create_enochian_tradition()
    return tradition.get_all_entries() 
