#!/usr/bin/env python3
"""
Migration script to reorganize knowledge base files into new structure
"""

import shutil
from pathlib import Path
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class KnowledgeBaseMigrator:
    """
    Migrates knowledge base files to new structure
    """
    
    def __init__(self):
        self.old_archives_dir = Path("knowledge_base/archives")
        self.new_base_dir = Path("core/knowledge-base")
        self.backup_dir = Path("knowledge_base/archives_backup")
        
    def migrate(self):
        """
        Perform the migration
        """
        logger.info("🔄 Starting knowledge base migration...")
        
        # Create backup
        self._create_backup()
        
        # Create new directory structure
        self._create_directories()
        
        # Move and consolidate files
        self._migrate_files()
        
        logger.info("✅ Migration complete!")
        
    def _create_backup(self):
        """Create backup of old files"""
        logger.info("📦 Creating backup...")
        
        # Create backup directory
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        self.backup_dir.mkdir(parents=True)
        
        # Copy all files
        for file in self.old_archives_dir.glob("*"):
            shutil.copy2(file, self.backup_dir)
            
        logger.info(f"✅ Backup created in {self.backup_dir}")
        
    def _create_directories(self):
        """Create new directory structure"""
        logger.info("📁 Creating new directory structure...")
        
        directories = [
            self.new_base_dir / "processors",
            self.new_base_dir / "data",
            self.new_base_dir / "indices",
            self.new_base_dir / "utils"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
    def _migrate_files(self):
        """Move and consolidate files"""
        logger.info("📋 Migrating files...")
        
        # Move processor files
        self._migrate_processors()
        
        # Consolidate and move indices
        self._migrate_indices()
        
        # Move utility scripts
        self._migrate_utils()
        
    def _migrate_processors(self):
        """Migrate processor files"""
        logger.info("Moving processor files...")
        
        # List of old processor files to remove
        old_processors = [
            "mystical_traditions_processor.py",
            "mystical_content_extractor.py",
            "knowledge_extractor.py",
            "enhanced_knowledge_extractor.py",
            "complete_concepts_processor.py",
            "legacy_research_processor.py"
        ]
        
        # Remove old processors
        for processor in old_processors:
            file = self.old_archives_dir / processor
            if file.exists():
                file.unlink()
                logger.info(f"Removed {processor}")
                
    def _migrate_indices(self):
        """Consolidate and migrate indices"""
        logger.info("Consolidating indices...")
        
        # List of index files to consolidate
        index_files = [
            "comprehensive_traditions_index.json",
            "unified_knowledge_index.json",
            "tradition_selection_index.json",
            "mystical_traditions_index.json",
            "enhanced_trait_index.json",
            "enhanced_governor_index.json"
        ]
        
        # Consolidate indices
        consolidated_data = {
            "metadata": {
                "consolidated_at": datetime.now().isoformat(),
                "source_files": index_files
            },
            "traditions": {},
            "indices": {
                "concepts": {},
                "traits": {},
                "patterns": {},
                "teachings": {},
                "frameworks": {}
            }
        }
        
        # Process each index file
        for index_file in index_files:
            file_path = self.old_archives_dir / index_file
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Merge data (implement specific merging logic here)
                self._merge_index_data(consolidated_data, data)
                
                # Remove old file
                file_path.unlink()
                logger.info(f"Processed and removed {index_file}")
                
        # Save consolidated index
        output_path = self.new_base_dir / "indices" / "consolidated_index.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(consolidated_data, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Created consolidated index at {output_path}")
        
    def _merge_index_data(self, consolidated: dict, new_data: dict):
        """
        Merge new index data into consolidated data
        
        Args:
            consolidated: The consolidated index data
            new_data: New data to merge in
        """
        # Merge traditions
        if "traditions" in new_data:
            for name, data in new_data["traditions"].items():
                if name not in consolidated["traditions"]:
                    consolidated["traditions"][name] = data
                else:
                    # Update existing tradition data
                    consolidated["traditions"][name].update(data)
                    
        # Merge indices
        if "indices" in new_data:
            for index_type, index_data in new_data["indices"].items():
                if index_type not in consolidated["indices"]:
                    consolidated["indices"][index_type] = {}
                    
                for key, values in index_data.items():
                    if key not in consolidated["indices"][index_type]:
                        consolidated["indices"][index_type][key] = values
                    else:
                        # Combine values, removing duplicates
                        existing = set(consolidated["indices"][index_type][key])
                        existing.update(values)
                        consolidated["indices"][index_type][key] = list(existing)
                        
    def _migrate_utils(self):
        """Migrate utility scripts"""
        logger.info("Moving utility scripts...")
        
        utils = [
            "governor_review_template.py",
            "complete_remaining.py",
            "tradition_audit.py"
        ]
        
        for util in utils:
            src = self.old_archives_dir / util
            if src.exists():
                dst = self.new_base_dir / "utils" / util
                shutil.move(src, dst)
                logger.info(f"Moved {util} to utils directory")
                
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run migration
    migrator = KnowledgeBaseMigrator()
    migrator.migrate() 