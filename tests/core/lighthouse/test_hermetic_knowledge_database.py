#!/usr/bin/env python3
"""
Tests for the Hermetic Tradition Knowledge Database
"""

import pytest
from pathlib import Path

from core.lighthouse.schemas.knowledge_schemas import (
    KnowledgeEntry,
    ProcessedTradition,
    KnowledgeType,
    ContentQuality
)

from core.governors.traits.knowledge_base.hermetic_knowledge_database import (
    load_hermetic_data,
    get_hermetic_entry_by_id,
    get_all_hermetic_entries,
    get_seven_principles,
    search_hermetic_by_tag,
    create_hermetic_tradition
)

def test_load_hermetic_data():
    """Test loading Hermetic tradition data"""
    data = load_hermetic_data()
    assert data is not None
    assert isinstance(data, dict)
    assert "core_principles" in data
    assert "core_concepts" in data
    assert "practices" in data
    assert len(data["core_principles"]) == 7  # Seven Hermetic Principles

def test_get_hermetic_entry_by_id():
    """Test retrieving specific Hermetic entries"""
    # Test getting a principle
    entry = get_hermetic_entry_by_id("hermetic_principle_mentalism")
    assert entry is not None
    assert isinstance(entry, KnowledgeEntry)
    assert entry.id == "hermetic_principle_mentalism"
    assert entry.tradition == "hermetic_tradition"
    assert entry.knowledge_type == KnowledgeType.PRINCIPLE
    
    # Test getting a concept
    entry = get_hermetic_entry_by_id("hermetic_emerald_tablet")
    assert entry is not None
    assert isinstance(entry, KnowledgeEntry)
    assert entry.id == "hermetic_emerald_tablet"
    assert entry.knowledge_type == KnowledgeType.CONCEPT
    
    # Test non-existent entry
    entry = get_hermetic_entry_by_id("non_existent_entry")
    assert entry is None

def test_get_all_hermetic_entries():
    """Test retrieving all Hermetic entries"""
    entries = get_all_hermetic_entries()
    assert entries is not None
    assert isinstance(entries, list)
    assert len(entries) > 0
    assert all(isinstance(e, KnowledgeEntry) for e in entries)
    assert all(e.tradition == "hermetic_tradition" for e in entries)

def test_get_seven_principles():
    """Test retrieving the Seven Hermetic Principles"""
    principles = get_seven_principles()
    assert principles is not None
    assert isinstance(principles, list)
    assert len(principles) == 7
    assert all(isinstance(p, KnowledgeEntry) for p in principles)
    assert all(p.knowledge_type == KnowledgeType.PRINCIPLE for p in principles)
    assert all(p.id.startswith("hermetic_principle_") for p in principles)

def test_search_hermetic_by_tag():
    """Test searching Hermetic entries by tag"""
    # Test with existing tag
    entries = search_hermetic_by_tag("alchemy")
    assert entries is not None
    assert isinstance(entries, list)
    assert len(entries) > 0
    assert all(isinstance(e, KnowledgeEntry) for e in entries)
    assert all("alchemy" in e.tags for e in entries)
    
    # Test with non-existent tag
    entries = search_hermetic_by_tag("non_existent_tag")
    assert entries == []

def test_create_hermetic_tradition():
    """Test creating complete Hermetic tradition database"""
    tradition = create_hermetic_tradition()
    assert tradition is not None
    assert isinstance(tradition, ProcessedTradition)
    assert tradition.name == "hermetic_tradition"
    assert len(tradition.principles) == 7  # Seven Hermetic Principles
    assert len(tradition.concepts) > 0
    assert len(tradition.practices) > 0
    assert tradition.total_entries == len(tradition.principles) + len(tradition.concepts) + len(tradition.practices) 