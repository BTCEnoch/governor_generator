#!/usr/bin/env python3
"""
Unified Knowledge Retriever System
Central system for accessing and searching across all wisdom tradition databases
"""

from typing import List, Dict, Optional, Union

import os

from typing import Dict, List, Optional
from core.lighthouse.schemas.knowledge_schemas import KnowledgeEntry, ProcessedTradition, KnowledgeType

# Import all tradition databases
from .enochian_knowledge_database import (
    create_enochian_tradition, get_enochian_entry_by_id, 
    search_enochian_by_tag, get_all_enochian_entries

from .hermetic_knowledge_database import (
    create_hermetic_tradition, get_hermetic_entry_by_id,
    search_hermetic_by_tag, get_all_hermetic_entries, get_seven_principles

from .kabbalah_knowledge_database import (
    create_kabbalah_tradition, get_kabbalah_entry_by_id,
    search_kabbalah_by_tag, get_all_kabbalah_entries, get_ten_sefirot

:
        # Initialize all tradition databases
        self.enochian_tradition = create_enochian_tradition()
        self.hermetic_tradition = create_hermetic_tradition()
        self.kabbalah_tradition = create_kabbalah_tradition()
        
        # Create unified index
        self.all_traditions = {
            "enochian_magic": self.enochian_tradition,
            "hermetic_tradition": self.hermetic_tradition,
            "kabbalah": self.kabbalah_tradition
        }
        
        # Create unified entry index
        self._create_unified_index()
    
    def _create_unified_index(self):
        """Create unified index of all knowledge entries"""
        self.all_entries = {}
        self.entries_by_tradition = {}
        self.entries_by_type = {}
        self.entries_by_tag = {}
        
        # Index all entries
        for tradition_name, tradition in self.all_traditions.items():
            self.entries_by_tradition[tradition_name] = tradition.get_all_entries()
            
            for entry in tradition.get_all_entries():
                # Add to main index
                self.all_entries[entry.id] = entry
                
                # Index by type
                if entry.knowledge_type not in self.entries_by_type:
                    self.entries_by_type[entry.knowledge_type] = []
                self.entries_by_type[entry.knowledge_type].append(entry)
                
                # Index by tags
                for tag in entry.tags:
                    if tag not in self.entries_by_tag:
                        self.entries_by_tag[tag] = []
                    self.entries_by_tag[tag].append(entry)
    
    def get_tradition_overview(self) -> Dict[str, Dict]:
        """Get overview of all traditions"""
        overview = {}
        for name, tradition in self.all_traditions.items():
            overview[name] = {
                "name": tradition.name,
                "description": tradition.description,
                "total_entries": tradition.total_entries,
                "principles": len(tradition.principles),
                "practices": len(tradition.practices),
                "systems": len(tradition.systems),
                "concepts": len(tradition.concepts)
            }
        return overview
    
    def get_entry_by_id(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """Get any knowledge entry by ID across all traditions"""
        return self.all_entries.get(entry_id)
    
    def search_by_tradition(self, tradition: str) -> List[KnowledgeEntry]:
        """Get all entries from a specific tradition"""
        return self.entries_by_tradition.get(tradition, [])
    
    def search_by_type(self, knowledge_type: KnowledgeType) -> List[KnowledgeEntry]:
        """Search entries by knowledge type across all traditions"""
        return self.entries_by_type.get(knowledge_type, [])
    
    def search_by_tag(self, tag: str) -> List[KnowledgeEntry]:
        """Search entries by tag across all traditions"""
        results = []
        for tradition_name in self.all_traditions.keys():
            if tradition_name == "enochian_magic":
                results.extend(search_enochian_by_tag(tag))
            elif tradition_name == "hermetic_tradition":
                results.extend(search_hermetic_by_tag(tag))
            elif tradition_name == "kabbalah":
                results.extend(search_kabbalah_by_tag(tag))
        return results
    
    def search_by_keywords(self, keywords: List[str]) -> List[KnowledgeEntry]:
        """Search entries by keywords in title, summary, or content"""
        results = []
        keywords_lower = [kw.lower() for kw in keywords]
        
        for entry in self.all_entries.values():
            # Check title, summary, and content
            searchable_text = (
                entry.title.lower() + " " + 
                entry.summary.lower() + " " + 
                entry.full_content.lower()
            
            # Check if any keyword appears in the text
            for keyword in keywords_lower:
                if keyword in searchable_text:
                    if entry not in results:
                        results.append(entry)
                    break
        
        return results
    
    def get_cross_tradition_connections(self, entry_id: str) -> List[KnowledgeEntry]:
        """Find entries from other traditions that share concepts or tags"""
        entry = self.get_entry_by_id(entry_id)
        if not entry:
            return []
        
        connections = []
        entry_tradition = entry.tradition
        
        # Search for shared tags in other traditions
        for tag in entry.tags:
            related_entries = self.search_by_tag(tag)
            for related_entry in related_entries:
                if (related_entry.tradition != entry_tradition and 
                    related_entry not in connections):
                    connections.append(related_entry)
        
        # Search for shared concepts
        for concept in entry.related_concepts:
            keyword_matches = self.search_by_keywords([concept])
            for match in keyword_matches:
                if (match.tradition != entry_tradition and 
                    match not in connections):
                    connections.append(match)
        
        return connections
    
    def get_foundational_knowledge(self) -> Dict[str, List[KnowledgeEntry]]:
        """Get foundational knowledge from each tradition"""
        foundational = {}
        
        # Hermetic: The Seven Principles
        foundational["hermetic_principles"] = get_seven_principles()
        
        # Kabbalah: The Ten Sefirot
        foundational["kabbalah_sefirot"] = get_ten_sefirot()
        
        # Enochian: Core Angels and Keys
        foundational["enochian_core"] = [
            entry for entry in get_all_enochian_entries() 
            if "angel" in entry.tags or "key" in entry.tags]
        return foundational
    
    def get_tradition_stats(self) -> Dict[str, int]:
        """Get statistics across all traditions"""
        stats = {
            "total_entries": len(self.all_entries),
            "total_traditions": len(self.all_traditions),
            "principles": len(self.entries_by_type.get(KnowledgeType.PRINCIPLE, [])),
            "practices": len(self.entries_by_type.get(KnowledgeType.PRACTICE, [])),
            "systems": len(self.entries_by_type.get(KnowledgeType.SYSTEM, [])),
            "concepts": len(self.entries_by_type.get(KnowledgeType.CONCEPT, [])),
            "unique_tags": len(self.entries_by_tag)
        }
        return stats
    
    def export_tradition_summary(self, tradition_name: str) -> Dict:
        """Export complete summary of a tradition"""
        if tradition_name not in self.all_traditions:
            return {}
        
        tradition = self.all_traditions[tradition_name]
        return tradition.to_dict()

# Global instance for easy access
unified_knowledge = UnifiedKnowledgeRetriever()

# Convenience functions
def get_knowledge_overview():
    """Get overview of all knowledge traditions"""
    return unified_knowledge.get_tradition_overview()

def search_all_traditions(query: str) -> List[KnowledgeEntry]:
    """Search across all traditions by keyword"""
    return unified_knowledge.search_by_keywords([query])

def get_foundational_teachings() -> Dict[str, List[KnowledgeEntry]]:
    """Get foundational teachings from all traditions"""
    return unified_knowledge.get_foundational_knowledge() 
