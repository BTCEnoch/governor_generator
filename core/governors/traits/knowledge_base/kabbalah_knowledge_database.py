#!/usr/bin/env python3
"""
Kabbalah Knowledge Database
Comprehensive database of Kabbalistic concepts, Tree of Life, and mystical practices
Based on curated sources from Sacred Texts, Sefaria, and Wikipedia
"""

from typing import List, Dict
import json
from pathlib import Path
import logging

from core.lighthouse.schemas.knowledge_schemas import KnowledgeEntry, KnowledgeType, ContentQuality, ProcessedTradition

# LOGGING SETUP (VITAL for debugging)
logger = logging.getLogger("KnowledgeDB.Kabbalah")

def load_consolidated_data() -> Dict:
    """Load the consolidated Kabbalah data from JSON file"""
    consolidated_path = Path(__file__).parent / "consolidated" / "kabbalah.json"
    if not consolidated_path.exists():
        raise FileNotFoundError(f"Consolidated data file not found at {consolidated_path}")
    
    with open(consolidated_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        logger.info(f"Loaded Kabbalah data with {len(data['core_concepts'])} core concepts")
        return data

def convert_to_knowledge_entry(concept_data: Dict) -> KnowledgeEntry:
    """Convert a concept from the consolidated format to a KnowledgeEntry"""
    return KnowledgeEntry(
        id=concept_data['id'],
        tradition="kabbalah",
        title=concept_data['title'],
        summary=concept_data['summary'],
        full_content=concept_data['full_content'],
        knowledge_type=getattr(KnowledgeType, concept_data['knowledge_type']),
        tags=concept_data['tags'],
        related_concepts=concept_data.get('related_concepts', []),
        source_url=concept_data.get('source_url', ''),
        confidence_score=concept_data.get('confidence_score', 0.0),
        quality=getattr(ContentQuality, concept_data['quality'])
    )

def create_kabbalah_tradition() -> ProcessedTradition:
    """Create a ProcessedTradition instance for Kabbalah"""
    data = load_consolidated_data()
    
    # Convert all concepts and practices to KnowledgeEntry objects
    entries = []
    for concept in data['core_concepts']:
        entries.append(convert_to_knowledge_entry(concept))
    for practice in data['practices']:
        entries.append(convert_to_knowledge_entry(practice))
    
    logger.info(f"Created Kabbalah tradition with {len(entries)} total entries")
    
    # Categorize entries by type
    principles = [e for e in entries if e.knowledge_type == KnowledgeType.PRINCIPLE]
    practices = [e for e in entries if e.knowledge_type == KnowledgeType.PRACTICE]
    systems = [e for e in entries if e.knowledge_type == KnowledgeType.SYSTEM]
    concepts = [e for e in entries if e.knowledge_type == KnowledgeType.CONCEPT]
    
    return ProcessedTradition(
        name="Kabbalah",
        description=data['description'],
        total_entries=len(entries),
        principles=principles,
        practices=practices,
        systems=systems,
        concepts=concepts,
        cross_references=data.get('correspondences', {})
    )

def get_all_entries() -> List[KnowledgeEntry]:
    """Get all Kabbalah knowledge entries"""
    tradition = create_kabbalah_tradition()
    return tradition.get_all_entries()

def get_entry_by_id(entry_id: str) -> KnowledgeEntry:
    """Get a specific entry by ID"""
    tradition = create_kabbalah_tradition()
    for entry in tradition.get_all_entries():
        if entry.id == entry_id:
            return entry
    raise KeyError(f"No entry found with ID: {entry_id}")

def get_entries_by_tag(tag: str) -> List[KnowledgeEntry]:
    """Get all entries with a specific tag"""
    tradition = create_kabbalah_tradition()
    return [entry for entry in tradition.get_all_entries() if tag in entry.tags]

def get_entries_by_type(knowledge_type: KnowledgeType) -> List[KnowledgeEntry]:
    """Get all entries of a specific type"""
    tradition = create_kabbalah_tradition()
    return [entry for entry in tradition.get_all_entries() if entry.knowledge_type == knowledge_type]

def get_correspondences() -> Dict:
    """Get all Kabbalistic correspondences"""
    data = load_consolidated_data()
    return data.get('correspondences', {})

def get_sefirot_data() -> List[Dict]:
    """Get detailed Sefirot data including influence categories"""
    data = load_consolidated_data()
    return [concept['sefirot_data'] for concept in data['core_concepts'] 
            if 'sefirot_data' in concept] 
