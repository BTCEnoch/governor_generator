#!/usr/bin/env python3
"""
Project Reorganization Script
============================

Systematically reorganizes the Governor Generator project into the new structure.
Handles file moves, import updates, and dependency management.

Usage:
    python scripts/reorganize_project.py --phase 1
    python scripts/reorganize_project.py --phase 2
    python scripts/reorganize_project.py --phase 3
    python scripts/reorganize_project.py --phase 4
"""

import os
import sys
import shutil
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ProjectReorganizer")

class ProjectReorganizer:
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root if project_root is not None else Path.cwd()
        self.backup_dir = self.project_root / "reorganization_backup"
        self.progress_file = self.project_root / "reorganization_progress.json"
        
        # Directory mappings
        self.directory_mappings = {
            # Data directories
            'clean_governor_profiles': 'data/governors/profiles',
            'governor_indexes': 'data/governors/indexes', 
            'personality_seeds': 'data/governors/seeds',
            'canon': 'data/canon',
            'knowledge_base/archives/governor_archives': 'data/knowledge/archives',
            'knowledge_base/archives/personality_seeds': 'data/knowledge/seeds',
            'knowledge_base/links': 'data/knowledge/links',
            'knowledge_base/data': 'data/knowledge/data',
            'knowledge_base/generated': 'data/knowledge/generated',
            
            # Core directories  
            'knowledge_base/traditions': 'core/lighthouse/traditions',
            'knowledge_base/retrievers': 'core/lighthouse/retrievers',
            'knowledge_base/schemas': 'core/lighthouse/schemas',
            'unified_profiler': 'core/governors/profiler',
            'pack': 'core/game_assets/pack',
            
            # Engine directories
            'mystical_systems': 'engines/mystical_systems',
            'storyline_engine': 'engines/storyline_generation',
            'integration_layer': 'engines/batch_processing',
            
            # Build system directories
            'trac_build': 'build_system/trac_build',
            
            # Tools directories
            'cli': 'tools/cli',
            'scripts': 'tools/utilities',
            'tests': 'tools/validation',
            'game_mechanics': 'tools/game_mechanics'
        }
        
        # Progress tracking
        self.progress = self.load_progress()
        
    def load_progress(self) -> Dict:
        """Load reorganization progress"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            'phase': 0,
            'completed_steps': [],
            'failed_steps': [],
            'timestamp': datetime.now().isoformat()
        }
        
    def save_progress(self) -> None:
        """Save reorganization progress"""
        self.progress['timestamp'] = datetime.now().isoformat()
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
            
    def create_backup(self) -> None:
        """Create backup of current state"""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"project_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        logger.info(f"Creating backup at {backup_path}")
        
        # Copy key directories
        key_dirs = [
            'clean_governor_profiles', 'governor_indexes', 'personality_seeds',
            'canon', 'knowledge_base', 'mystical_systems', 'storyline_engine',
            'unified_profiler', 'scripts', 'tests', 'cli', 'game_mechanics'
        ]
        
        for dir_name in key_dirs:
            src_path = self.project_root / dir_name
            if src_path.exists():
                dst_path = backup_path / dir_name
                shutil.copytree(src_path, dst_path)
                logger.info(f"Backed up {dir_name}")
                
    def create_new_structure(self) -> None:
        """Create new directory structure"""
        logger.info("Creating new directory structure...")
        
        # Main directories
        main_dirs = [
            'data/governors/profiles', 'data/governors/indexes', 'data/governors/seeds',
            'data/canon', 'data/knowledge/archives', 'data/knowledge/seeds',
            'data/knowledge/links', 'data/knowledge/data', 'data/knowledge/generated',
            'data/questlines',
            
            'core/lighthouse/traditions', 'core/lighthouse/retrievers', 'core/lighthouse/schemas',
            'core/governors/profiler', 'core/governors/services',
            'core/questlines', 'core/game_assets/pack',
            
            'engines/mystical_systems', 'engines/trait_generation', 
            'engines/storyline_generation', 'engines/batch_processing',
            
            'build_system/trac_build', 'build_system/contracts', 'build_system/deployment',
            
            'tools/cli', 'tools/validation', 'tools/utilities', 'tools/game_mechanics',
            
            'docs/architecture', 'docs/game_design', 'docs/api'
        ]
        
        for dir_path in main_dirs:
            full_path = self.project_root / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {dir_path}")
            
        # Create __init__.py files
        self.create_init_files()
        
    def create_init_files(self) -> None:
        """Create __init__.py files for new package structure"""
        logger.info("Creating __init__.py files...")
        
        # Find all directories and create __init__.py
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            
            # Skip hidden directories and old structure
            if any(part.startswith('.') for part in root_path.parts):
                continue
                
            # Only create __init__.py in new structure directories
            rel_path = root_path.relative_to(self.project_root)
            if any(str(rel_path).startswith(prefix) for prefix in ['data', 'core', 'engines', 'build_system', 'tools', 'docs']):
                init_file = root_path / '__init__.py'
                if not init_file.exists():
                    init_file.touch()
                    logger.info(f"Created __init__.py in {rel_path}")
                    
    def move_files(self) -> None:
        """Move files according to directory mappings"""
        logger.info("Moving files to new structure...")
        
        for old_path, new_path in self.directory_mappings.items():
            src = self.project_root / old_path
            dst = self.project_root / new_path
            
            if src.exists() and src.is_dir():
                try:
                    # Ensure destination parent exists
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Move contents rather than the directory itself
                    if dst.exists():
                        # Merge directories
                        for item in src.iterdir():
                            item_dst = dst / item.name
                            if item.is_dir():
                                shutil.copytree(item, item_dst, dirs_exist_ok=True)
                            else:
                                shutil.copy2(item, item_dst)
                    else:
                        shutil.move(str(src), str(dst))
                    
                    logger.info(f"Moved {old_path} -> {new_path}")
                    
                except Exception as e:
                    logger.error(f"Failed to move {old_path} -> {new_path}: {e}")
                    self.progress['failed_steps'].append(f"move_{old_path}")
                    
    def run_phase(self, phase: int) -> None:
        """Run specific reorganization phase"""
        logger.info(f"Starting Phase {phase}")
        
        if phase == 1:
            self.run_phase_1()
        elif phase == 2:
            self.run_phase_2()
        elif phase == 3:
            self.run_phase_3()
        elif phase == 4:
            self.run_phase_4()
        else:
            logger.error(f"Unknown phase: {phase}")
            
    def run_phase_1(self) -> None:
        """Phase 1: Create backup and new structure"""
        logger.info("Phase 1: Creating backup and new directory structure")
        
        try:
            self.create_backup()
            self.create_new_structure()
            
            self.progress['phase'] = 1
            self.progress['completed_steps'].append('phase_1')
            self.save_progress()
            
            logger.info("Phase 1 completed successfully")
            
        except Exception as e:
            logger.error(f"Phase 1 failed: {e}")
            self.progress['failed_steps'].append('phase_1')
            self.save_progress()
            
    def run_phase_2(self) -> None:
        """Phase 2: Move data files"""
        logger.info("Phase 2: Moving data files")
        
        try:
            # Move data directories first
            data_mappings = {k: v for k, v in self.directory_mappings.items() 
                           if v.startswith('data/')}
            
            for old_path, new_path in data_mappings.items():
                src = self.project_root / old_path
                dst = self.project_root / new_path
                
                if src.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                    logger.info(f"Moved {old_path} -> {new_path}")
                    
            self.progress['phase'] = 2
            self.progress['completed_steps'].append('phase_2')
            self.save_progress()
            
            logger.info("Phase 2 completed successfully")
            
        except Exception as e:
            logger.error(f"Phase 2 failed: {e}")
            self.progress['failed_steps'].append('phase_2')
            self.save_progress()
            
    def run_phase_3(self) -> None:
        """Phase 3: Move core and engine files"""
        logger.info("Phase 3: Moving core and engine files")
        
        try:
            # Move core and engine directories
            core_engine_mappings = {k: v for k, v in self.directory_mappings.items() 
                                  if v.startswith('core/') or v.startswith('engines/')}
            
            for old_path, new_path in core_engine_mappings.items():
                src = self.project_root / old_path
                dst = self.project_root / new_path
                
                if src.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                    logger.info(f"Moved {old_path} -> {new_path}")
                    
            self.progress['phase'] = 3
            self.progress['completed_steps'].append('phase_3')
            self.save_progress()
            
            logger.info("Phase 3 completed successfully")
            
        except Exception as e:
            logger.error(f"Phase 3 failed: {e}")
            self.progress['failed_steps'].append('phase_3')
            self.save_progress()
            
    def run_phase_4(self) -> None:
        """Phase 4: Move build system and tools"""
        logger.info("Phase 4: Moving build system and tools")
        
        try:
            # Move remaining directories
            remaining_mappings = {k: v for k, v in self.directory_mappings.items() 
                                if v.startswith('build_system/') or v.startswith('tools/')}
            
            for old_path, new_path in remaining_mappings.items():
                src = self.project_root / old_path
                dst = self.project_root / new_path
                
                if src.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                    logger.info(f"Moved {old_path} -> {new_path}")
                    
            self.progress['phase'] = 4
            self.progress['completed_steps'].append('phase_4')
            self.save_progress()
            
            logger.info("Phase 4 completed successfully")
            
        except Exception as e:
            logger.error(f"Phase 4 failed: {e}")
            self.progress['failed_steps'].append('phase_4')
            self.save_progress()

def main():
    parser = argparse.ArgumentParser(description='Reorganize Governor Generator project')
    parser.add_argument('--phase', type=int, required=True, choices=[1, 2, 3, 4],
                       help='Phase to run (1-4)')
    parser.add_argument('--project-root', type=Path, default=Path.cwd(),
                       help='Project root directory')
    
    args = parser.parse_args()
    
    reorganizer = ProjectReorganizer(args.project_root)
    reorganizer.run_phase(args.phase)

if __name__ == "__main__":
    main() 