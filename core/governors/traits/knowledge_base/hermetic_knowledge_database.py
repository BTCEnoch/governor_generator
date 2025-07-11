#!/usr/bin/env python3
"""
Hermetic Tradition Knowledge Database
Loads and processes Hermetic tradition data from consolidated JSON format
"""

import os
from pathlib import Path
from typing import List, Dict, Optional

from core.lighthouse.schemas.knowledge_schemas import (
    KnowledgeEntry, 
    ProcessedTradition,
    KnowledgeType,
    ContentQuality
)

from core.utils.common.file_ops import safe_json_read
from core.utils.custom_logging import custom_logger

logger = custom_logger.setup_logger(__name__)

HERMETIC_JSON_PATH = Path("data/knowledge/archives/governor_archives/hermetic_tradition.json")

def load_hermetic_data() -> Dict:
    """Load the consolidated Hermetic tradition data"""
    try:
        data = safe_json_read(HERMETIC_JSON_PATH)
        if data is None:
            logger.error("❌ Failed to load Hermetic tradition data: File could not be read")
            return {}
            
        logger.info(f"✅ Loaded Hermetic tradition data: {len(data.get('core_principles', [])) + len(data.get('core_concepts', [])) + len(data.get('practices', []))} total entries")
        return data
    except Exception as e:
        logger.error(f"❌ Failed to load Hermetic tradition data: {e}")
        return {}

def create_knowledge_entry(entry_data: Dict) -> KnowledgeEntry:
    """Convert JSON entry data to KnowledgeEntry object"""
    return KnowledgeEntry(
        id=entry_data["id"],
        tradition="hermetic_tradition",
        title=entry_data["title"],
        summary=entry_data["summary"],
        full_content=entry_data["content"],
        tags=entry_data["tags"],
        related_concepts=entry_data.get("related_concepts", []),
        source_url=entry_data.get("source_url", ""),
        confidence_score=0.9,
        quality=ContentQuality.HIGH if entry_data.get("quality") == "HIGH" else ContentQuality.MEDIUM,
        knowledge_type=KnowledgeType.PRINCIPLE if entry_data["id"].startswith("hermetic_principle_") else KnowledgeType.CONCEPT
    )

def get_hermetic_entry_by_id(entry_id: str) -> Optional[KnowledgeEntry]:
    """Retrieve a specific Hermetic knowledge entry by ID"""
    data = load_hermetic_data()
    
    # Search in all sections
    for section in ["core_principles", "core_concepts", "practices"]:
        for entry in data.get(section, []):
            if entry["id"] == entry_id:
                return create_knowledge_entry(entry)
    
    return None

def get_all_hermetic_entries() -> List[KnowledgeEntry]:
    """Get all Hermetic tradition knowledge entries"""
    data = load_hermetic_data()
    entries = []
    
    # Combine entries from all sections
    for section in ["core_principles", "core_concepts", "practices"]:
        entries.extend([create_knowledge_entry(entry) for entry in data.get(section, [])])
    
    return entries

def get_seven_principles() -> List[KnowledgeEntry]:
    """Get the Seven Hermetic Principles entries"""
    data = load_hermetic_data()
    return [create_knowledge_entry(entry) for entry in data.get("core_principles", [])]

def search_hermetic_by_tag(tag: str) -> List[KnowledgeEntry]:
    """Search for Hermetic entries by tag"""
    entries = get_all_hermetic_entries()
    return [entry for entry in entries if tag in entry.tags]

def create_hermetic_tradition() -> ProcessedTradition:
    """Create the complete Hermetic tradition database"""
    data = load_hermetic_data()
    
    all_entries = get_all_hermetic_entries()
    
    # Categorize entries
    principles = [e for e in all_entries if e.id.startswith("hermetic_principle_")]
    concepts = [e for e in all_entries if e.id.startswith("hermetic_") and not e.id.startswith("hermetic_principle_")]
    practices = [e for e in all_entries if not e.id.startswith("hermetic_")]
    
    # Get cross-references
    cross_references = data.get("cross_references", {})
    
    return ProcessedTradition(
        name="hermetic_tradition",
        description="The philosophical and magical tradition attributed to Hermes Trismegistus, synthesizing Egyptian wisdom, Greek philosophy, and practical alchemy.",
        total_entries=len(all_entries),
        principles=principles,
        concepts=concepts,
        practices=practices,
        cross_references=cross_references
    ) 
