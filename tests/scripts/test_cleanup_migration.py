"""
Tests for the cleanup migration script
"""

import pytest
import shutil
from pathlib import Path
import json

from scripts.cleanup_migration import TraitCleanupMigrator

@pytest.fixture
def test_workspace(tmp_path):
    """Create a test workspace with dummy files"""
    # Create source directories
    knowledge_base = tmp_path / 'knowledge_base'
    lighthouse = tmp_path / 'core/lighthouse/traditions'
    core_knowledge = tmp_path / 'core/knowledge-base'
    gov_traits = tmp_path / 'data/governors/traits'
    gov_dossier = tmp_path / 'governor_dossier'
    gov_indexes = tmp_path / 'data/governors/indexes'
    
    # Create test files
    for dir_path in [knowledge_base, lighthouse, core_knowledge, 
                    gov_traits, gov_dossier, gov_indexes]:
        dir_path.mkdir(parents=True)
        (dir_path / 'test.json').write_text('{"test": "data"}')
        (dir_path / 'subdir').mkdir()
        (dir_path / 'subdir/test2.json').write_text('{"test2": "data"}')
    
    return tmp_path

@pytest.fixture
def migrator(monkeypatch, test_workspace):
    """Create a migrator instance with mocked workspace root"""
    migrator = TraitCleanupMigrator()
    monkeypatch.setattr(migrator, 'workspace_root', test_workspace)
    return migrator

def test_directories_created(migrator):
    """Test that target directories are created"""
    migrator.migrate_all()
    
    assert migrator.target_traits_dir.exists()
    assert migrator.target_knowledge_dir.exists()

def test_files_migrated(migrator):
    """Test that files are migrated correctly"""
    migrator.migrate_all()
    
    # Check knowledge base files
    assert (migrator.target_knowledge_dir / 'test.json').exists()
    assert (migrator.target_knowledge_dir / 'subdir/test2.json').exists()
    
    # Check trait files
    assert (migrator.target_traits_dir / 'test.json').exists()
    assert (migrator.target_traits_dir / 'subdir/test2.json').exists()

def test_old_directories_removed(migrator):
    """Test that old directories are removed"""
    migrator.migrate_all()
    
    # Check knowledge base directories are removed
    assert not (migrator.workspace_root / 'knowledge_base').exists()
    assert not (migrator.workspace_root / 'core/lighthouse/traditions').exists()
    assert not (migrator.workspace_root / 'core/knowledge-base').exists()
    
    # Check trait directories are removed
    assert not (migrator.workspace_root / 'data/governors/traits').exists()
    assert not (migrator.workspace_root / 'governor_dossier').exists()
    assert not (migrator.workspace_root / 'data/governors/indexes').exists()

def test_duplicate_files_handled(migrator):
    """Test that duplicate files are handled correctly"""
    # Create duplicate files
    for source_dir in migrator.source_dirs['knowledge_base']:
        source_dir.mkdir(parents=True, exist_ok=True)
        (source_dir / 'duplicate.json').write_text('{"test": "data"}')
    
    migrator.migrate_all()
    
    # Only one copy should exist in target
    duplicate_files = list(migrator.target_knowledge_dir.rglob('duplicate.json'))
    assert len(duplicate_files) == 1

def test_file_content_preserved(migrator):
    """Test that file content is preserved during migration"""
    test_data = {'test': 'complex data', 'nested': {'value': 123}}
    test_file = migrator.workspace_root / 'knowledge_base/test_content.json'
    test_file.parent.mkdir(parents=True)
    test_file.write_text(json.dumps(test_data))
    
    migrator.migrate_all()
    
    migrated_file = migrator.target_knowledge_dir / 'test_content.json'
    assert migrated_file.exists()
    assert json.loads(migrated_file.read_text()) == test_data 