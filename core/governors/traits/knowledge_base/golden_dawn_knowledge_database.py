#!/usr/bin/env python3
"""
Golden Dawn Knowledge Database
Comprehensive database of Golden Dawn magical concepts, rituals, and correspondences
Based on curated sources from canon/canon_sources_index.json
"""

from typing import List, Dict
import json
from pathlib import Path

from core.lighthouse.schemas.knowledge_schemas import KnowledgeEntry, KnowledgeType, ContentQuality, ProcessedTradition

# LOGGING SETUP (VITAL for debugging)
import logging
logger = logging.getLogger("KnowledgeDB.GoldenDawn")

def load_consolidated_data() -> Dict:
    """Load the consolidated Golden Dawn data from JSON file"""
    consolidated_path = Path(__file__).parent / "consolidated" / "golden_dawn.json"
    if not consolidated_path.exists():
        raise FileNotFoundError(f"Consolidated data file not found at {consolidated_path}")
    
    with open(consolidated_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        logger.info(f"Loaded Golden Dawn consolidated data: {len(data.get('key_concepts', []))} concepts")
        return data

def convert_to_knowledge_entry(concept: Dict, tradition_data: Dict) -> KnowledgeEntry:
    """Convert a concept from consolidated data into a KnowledgeEntry"""
    return KnowledgeEntry(
        id=f"golden_dawn_{concept['name'].lower().replace(' ', '_')}",
        tradition="golden_dawn",
        title=concept['name'],
        summary=concept['principle'],
        full_content=f"""{concept['wisdom']}

Key Attributes:
- Principle: {concept['principle']}
- Wisdom: {concept['wisdom']}
- Application Trigger: {concept['trigger']}
- Key Quote: "{concept['quote']}"

This concept is fundamental to Golden Dawn practice and governance.""",
        knowledge_type=KnowledgeType.SYSTEM,
        tags=[t.lower().replace(' ', '_') for t in concept['name'].split()],
        related_concepts=[],  # To be populated from relationships
        source_url="https://hermetic.com/golden-dawn/",
        confidence_score=0.95,
        quality=ContentQuality.HIGH if tradition_data['quality_rating'] == "ENHANCED" else ContentQuality.MEDIUM
    )

def create_golden_dawn_tradition() -> ProcessedTradition:
    """Create a ProcessedTradition instance from consolidated Golden Dawn data"""
    data = load_consolidated_data()
    
    # Convert concepts to KnowledgeEntries
    entries = [convert_to_knowledge_entry(concept, data) for concept in data['key_concepts']]
    
    logger.info(f"Created {len(entries)} Golden Dawn knowledge entries")
    
    # Organize entries by type
    principles = []
    practices = []
    systems = []
    concepts = entries  # For now, all entries are concepts
    
    return ProcessedTradition(
        name="golden_dawn",
        description=data['overview'],
        total_entries=len(entries),
        principles=principles,
        practices=practices,
        systems=systems,
        concepts=concepts
    )

def get_all_entries() -> List[KnowledgeEntry]:
    """Return all Golden Dawn knowledge entries"""
    tradition = create_golden_dawn_tradition()
    return tradition.get_all_entries()

def get_entry_by_id(entry_id: str) -> KnowledgeEntry:
    """Get a specific Golden Dawn knowledge entry by ID"""
    entries = get_all_entries()
    for entry in entries:
        if entry.id == entry_id:
            return entry
    raise KeyError(f"No Golden Dawn entry found with ID: {entry_id}")

# Initialize logging
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)


