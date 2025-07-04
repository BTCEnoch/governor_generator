#!/usr/bin/env python3
"""
Free Content Consolidator
Consolidates all existing free knowledge content into unified format for governor storylines.
NO APIs REQUIRED - Uses only existing knowledge databases.
"""

import os
import json
from typing import List, Dict, Any
from dataclasses import asdict

# Import existing knowledge databases
from traditions.kabbalah_knowledge_database import get_all_kabbalah_entries
from traditions.hermetic_knowledge_database import get_all_hermetic_entries  
from traditions.golden_dawn_knowledge_database import GOLDEN_DAWN_KNOWLEDGE_ENTRIES
from traditions.enochian_knowledge_database import get_all_enochian_entries

# Import schemas
from core.lighthouse.schemas.knowledge_schemas import KnowledgeEntry

# LOGGING SETUP
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("FreeContentConsolidator")

def consolidate_free_content() -> Dict[str, List[Dict]]:
    """
    Consolidate all existing free knowledge content into unified structure.
    Returns organized knowledge ready for governor storylines.
    """
    logger.info("🏛️ Starting FREE content consolidation...")
    
    consolidated = {
        "kabbalah_tradition": [],
        "hermetic_tradition": [], 
        "golden_dawn": [],
        "enochian": []
    }
    
    # Get all free content
    try:
        # Kabbalah entries
        kabbalah_entries = get_all_kabbalah_entries()
        logger.info(f"📚 Loaded {len(kabbalah_entries)} Kabbalah entries")
        consolidated["kabbalah_tradition"] = [asdict(entry) for entry in kabbalah_entries]
        
        # Hermetic entries  
        hermetic_entries = get_all_hermetic_entries()
        logger.info(f"📚 Loaded {len(hermetic_entries)} Hermetic entries")
        consolidated["hermetic_tradition"] = [asdict(entry) for entry in hermetic_entries]
        
        # Golden Dawn entries
        logger.info(f"📚 Loaded {len(GOLDEN_DAWN_KNOWLEDGE_ENTRIES)} Golden Dawn entries")
        consolidated["golden_dawn"] = [asdict(entry) for entry in GOLDEN_DAWN_KNOWLEDGE_ENTRIES]
        
        # Enochian entries
        enochian_entries = get_all_enochian_entries()
        logger.info(f"📚 Loaded {len(enochian_entries)} Enochian entries")
        consolidated["enochian"] = [asdict(entry) for entry in enochian_entries]
        
    except Exception as e:
        logger.error(f"❌ Error loading knowledge entries: {e}")
        return {}
    
    # Calculate totals
    total_entries = sum(len(entries) for entries in consolidated.values())
    logger.info(f"✅ FREE CONTENT CONSOLIDATED: {total_entries} total entries across 4 traditions")
    
    return consolidated

def save_consolidated_knowledge(filename: str = "free_lighthouse_content.json"):
    """Save consolidated free content to JSON file."""
    consolidated = consolidate_free_content()
    
    if not consolidated:
        logger.error("❌ No content to save")
        return False
        
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(consolidated, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Saved consolidated content to {filename}")
        return True
    except Exception as e:
        logger.error(f"❌ Error saving content: {e}")
        return False

def get_knowledge_for_governor_selection(knowledge_selections: List[str]) -> List[Dict]:
    """
    Get relevant knowledge entries for a governor's knowledge_base_selections.
    This replaces the need for API-based retrieval.
    """
    consolidated = consolidate_free_content()
    relevant_entries = []
    
    for selection in knowledge_selections:
        # Map knowledge selections to traditions
        if "hermetic" in selection.lower() or "principle" in selection.lower():
            relevant_entries.extend(consolidated.get("hermetic_tradition", []))
        elif "kabbalah" in selection.lower() or "tree_of_life" in selection.lower():
            relevant_entries.extend(consolidated.get("kabbalah_tradition", []))
        elif "golden_dawn" in selection.lower() or "ritual" in selection.lower():
            relevant_entries.extend(consolidated.get("golden_dawn", []))
        elif "enochian" in selection.lower() or "angel" in selection.lower():
            relevant_entries.extend(consolidated.get("enochian", []))
    
    # Remove duplicates by ID
    seen_ids = set()
    unique_entries = []
    for entry in relevant_entries:
        if entry['id'] not in seen_ids:
            unique_entries.append(entry)
            seen_ids.add(entry['id'])
    
    logger.info(f"🎯 Found {len(unique_entries)} relevant entries for governor selections")
    return unique_entries

if __name__ == "__main__":
    # Consolidate and save free content
    logger.info("🚀 Running FREE Content Consolidation...")
    save_consolidated_knowledge()
    logger.info("✅ Consolidation complete - ready for governor storylines!") 
