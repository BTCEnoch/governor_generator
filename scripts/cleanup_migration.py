"""
Cleanup script to consolidate trait and knowledge base definitions
"""

import logging
import shutil
from pathlib import Path
from typing import Dict, List, Set
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cleanup_migration.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TraitCleanupMigrator:
    """Handles consolidation of trait and knowledge base definitions"""
    
    def __init__(self):
        self.workspace_root = Path(__file__).parent.parent
        self.target_traits_dir = self.workspace_root / 'core/governors/traits'
        self.target_knowledge_dir = self.target_traits_dir / 'knowledge_base'
        
        # Source directories to consolidate
        self.source_dirs = {
            'knowledge_base': [
                self.workspace_root / 'knowledge_base',
                self.workspace_root / 'core/lighthouse/traditions',
                self.workspace_root / 'core/knowledge-base'
            ],
            'traits': [
                self.workspace_root / 'data/governors/traits',
                self.workspace_root / 'governor_dossier',
                self.workspace_root / 'data/governors/indexes'
            ]
        }
        
        # Track processed files to avoid duplicates
        self.processed_files: Set[str] = set()
        
    def migrate_all(self):
        """Execute complete migration process"""
        logger.info("Starting trait and knowledge base consolidation...")
        
        # Ensure target directories exist
        self.target_traits_dir.mkdir(parents=True, exist_ok=True)
        self.target_knowledge_dir.mkdir(parents=True, exist_ok=True)
        
        # Migrate knowledge base files
        self._migrate_knowledge_base()
        
        # Migrate trait files
        self._migrate_traits()
        
        # Clean up old directories
        self._cleanup_old_dirs()
        
        logger.info("Migration complete!")
        
    def _migrate_knowledge_base(self):
        """Migrate knowledge base files to consolidated location"""
        logger.info("Migrating knowledge base files...")
        
        for source_dir in self.source_dirs['knowledge_base']:
            if not source_dir.exists():
                continue
                
            for file_path in source_dir.rglob('*'):
                if not file_path.is_file():
                    continue
                    
                # Skip already processed files
                if str(file_path) in self.processed_files:
                    continue
                    
                # Determine target path
                rel_path = file_path.relative_to(source_dir)
                target_path = self.target_knowledge_dir / rel_path
                
                # Create parent directories
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(file_path, target_path)
                logger.info(f"Copied {file_path} -> {target_path}")
                
                self.processed_files.add(str(file_path))
                
    def _migrate_traits(self):
        """Migrate trait files to consolidated location"""
        logger.info("Migrating trait files...")
        
        for source_dir in self.source_dirs['traits']:
            if not source_dir.exists():
                continue
                
            for file_path in source_dir.rglob('*'):
                if not file_path.is_file():
                    continue
                    
                # Skip already processed files
                if str(file_path) in self.processed_files:
                    continue
                    
                # Determine target path
                rel_path = file_path.relative_to(source_dir)
                target_path = self.target_traits_dir / rel_path
                
                # Create parent directories
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(file_path, target_path)
                logger.info(f"Copied {file_path} -> {target_path}")
                
                self.processed_files.add(str(file_path))
                
    def _cleanup_old_dirs(self):
        """Remove old directories after successful migration"""
        logger.info("Cleaning up old directories...")
        
        all_source_dirs = self.source_dirs['knowledge_base'] + self.source_dirs['traits']
        
        for source_dir in all_source_dirs:
            if source_dir.exists():
                shutil.rmtree(source_dir)
                logger.info(f"Removed {source_dir}")

if __name__ == '__main__':
    migrator = TraitCleanupMigrator()
    migrator.migrate_all() 