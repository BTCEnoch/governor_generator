#!/usr/bin/env python3
"""
Import Updater Script
====================

Updates all import statements after project reorganization.
Handles path changes and removes sys.path manipulations.

Usage:
    python scripts/update_imports.py --scan
    python scripts/update_imports.py --update
    python scripts/update_imports.py --validate
"""

import os
import re
import sys
import ast
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
import argparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ImportUpdater")

class ImportUpdater:
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root if project_root is not None else Path.cwd()
        
        # Import path mappings (old -> new)
        self.path_mappings = {
            # Knowledge base mappings
            'core.lighthouse.traditions': 'core.lighthouse.traditions',
            'core.lighthouse.retrievers': 'core.lighthouse.retrievers',
            'core.lighthouse.schemas': 'core.lighthouse.schemas',
            'core.lighthouse.data': 'data.knowledge.data',
            'core.lighthouse.archives': 'data.knowledge.archives',
            'core.lighthouse.links': 'data.knowledge.links',
            'core.lighthouse.generated': 'data.knowledge.generated',
            
            # Unified profiler mappings
            'unified_profiler': 'core.governors.profiler',
            'core.governors.profiler.core': 'core.governors.profiler.core',
            'core.governors.profiler.interfaces': 'core.governors.profiler.interfaces',
            'core.governors.profiler.schemas': 'core.governors.profiler.schemas',
            
            # Mystical systems mappings
            'mystical_systems': 'engines.mystical_systems',
            'engines.mystical_systems.tarot_system': 'engines.engines.mystical_systems.tarot_system',
            'engines.mystical_systems.kabbalah_system': 'engines.engines.mystical_systems.kabbalah_system',
            'engines.mystical_systems.numerology_system': 'engines.engines.mystical_systems.numerology_system',
            'engines.mystical_systems.zodiac_system': 'engines.engines.mystical_systems.zodiac_system',
            
            # Storyline engine mappings
            'storyline_engine': 'engines.storyline_generation',
            'engines.storyline_generation.schemas': 'engines.storyline_generation.schemas',
            
            # Integration layer mappings
            'integration_layer': 'engines.batch_processing',
            'engines.batch_processing.coordinators': 'engines.batch_processing.coordinators',
            
            # Game mechanics mappings
            'game_mechanics': 'tools.game_mechanics',
            'tools.game_mechanics.dialog_system': 'tools.game_mechanics.dialog_system',
            'tools.game_mechanics.divination_systems': 'tools.game_mechanics.divination_systems',
            
            # CLI mappings
            'cli': 'tools.cli',
            
            # Scripts mappings
            'scripts': 'tools.utilities',
            
            # Tests mappings
            'tests': 'tools.validation',
            
            # Trac build mappings
            'trac_build': 'build_system.trac_build',
            
            # Data mappings
            'clean_governor_profiles': 'data.governors.profiles',
            'governor_indexes': 'data.governors.indexes',
            'personality_seeds': 'data.governors.seeds',
            'canon': 'data.canon',
            'pack': 'core.game_assets.pack'
        }
        
        # Patterns to remove
        self.patterns_to_remove = [
            r'sys\.path\.append\(.*?\)',
            r'import\s+sys\s*\n.*?sys\.path\.append\(.*?\)',
            r'from\s+pathlib\s+import\s+Path\s*\n.*?sys\.path\.append\(.*?\)',
        ]
        
        # Files to update
        self.python_files = []
        self.scan_results = {}
        
    def find_python_files(self) -> List[Path]:
        """Find all Python files in the project"""
        python_files = []
        
        # Search in new structure directories
        search_dirs = [
            'data', 'core', 'engines', 'build_system', 'tools'
        ]
        
        for search_dir in search_dirs:
            search_path = self.project_root / search_dir
            if search_path.exists():
                for py_file in search_path.rglob('*.py'):
                    python_files.append(py_file)
                    
        return python_files
        
    def scan_imports(self) -> Dict[str, List[str]]:
        """Scan all Python files for imports that need updating"""
        logger.info("Scanning Python files for imports...")
        
        self.python_files = self.find_python_files()
        scan_results = {}
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                imports_to_update = []
                
                # Check for imports that need updating
                for old_path, new_path in self.path_mappings.items():
                    # Check for "import old_path" or "from old_path import ..."
                    import_patterns = [
                        rf'import\s+{re.escape(old_path)}',
                        rf'from\s+{re.escape(old_path)}\s+import',
                        rf'from\s+{re.escape(old_path)}\.[\w\.]+\s+import'
                    ]
                    
                    for pattern in import_patterns:
                        matches = re.findall(pattern, content)
                        if matches:
                            imports_to_update.extend(matches)
                            
                # Check for sys.path manipulations
                for pattern in self.patterns_to_remove:
                    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
                    if matches:
                        imports_to_update.extend([f"REMOVE: {match}" for match in matches])
                        
                if imports_to_update:
                    scan_results[str(py_file)] = imports_to_update
                    logger.info(f"Found {len(imports_to_update)} imports to update in {py_file}")
                    
            except Exception as e:
                logger.error(f"Failed to scan {py_file}: {e}")
                
        self.scan_results = scan_results
        return scan_results
        
    def update_file_imports(self, file_path: Path) -> bool:
        """Update imports in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            # Update import paths
            for old_path, new_path in self.path_mappings.items():
                # Update "import old_path" to "import new_path"
                content = re.sub(
                    rf'\bimport\s+{re.escape(old_path)}\b',
                    f'import {new_path}',
                    content
                )
                
                # Update "from old_path import ..." to "from new_path import ..."
                content = re.sub(
                    rf'\bfrom\s+{re.escape(old_path)}\s+import',
                    f'from {new_path} import',
                    content
                )
                
                # Update "from old_path.submodule import ..." to "from new_path.submodule import ..."
                content = re.sub(
                    rf'\bfrom\s+{re.escape(old_path)}\.([\w\.]+)\s+import',
                    rf'from {new_path}.\1 import',
                    content
                )
                
            # Remove sys.path manipulations
            for pattern in self.patterns_to_remove:
                content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
                
            # Clean up extra whitespace
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            
            # Write back if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"Updated imports in {file_path}")
                return True
            else:
                logger.info(f"No changes needed in {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to update {file_path}: {e}")
            return False
            
    def update_all_imports(self) -> Dict[str, bool]:
        """Update imports in all Python files"""
        logger.info("Updating imports in all Python files...")
        
        results = {}
        
        for py_file in self.python_files:
            success = self.update_file_imports(py_file)
            results[str(py_file)] = success
            
        return results
        
    def validate_imports(self) -> Dict[str, List[str]]:
        """Validate that all imports are working"""
        logger.info("Validating imports...")
        
        validation_results = {}
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Try to parse the file
                try:
                    ast.parse(content)
                    logger.info(f"✅ {py_file} - syntax OK")
                except SyntaxError as e:
                    validation_results[str(py_file)] = [f"Syntax error: {e}"]
                    logger.error(f"❌ {py_file} - syntax error: {e}")
                    
            except Exception as e:
                validation_results[str(py_file)] = [f"Read error: {e}"]
                logger.error(f"❌ {py_file} - read error: {e}")
                
        return validation_results
        
    def generate_report(self) -> str:
        """Generate a report of the import updates"""
        report = []
        report.append("# Import Update Report")
        report.append(f"Generated: {Path(__file__).name}")
        report.append("")
        
        if self.scan_results:
            report.append("## Files with imports to update:")
            for file_path, imports in self.scan_results.items():
                report.append(f"### {file_path}")
                for imp in imports:
                    report.append(f"- {imp}")
                report.append("")
                
        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='Update imports after reorganization')
    parser.add_argument('--scan', action='store_true', help='Scan for imports to update')
    parser.add_argument('--update', action='store_true', help='Update all imports')
    parser.add_argument('--validate', action='store_true', help='Validate imports')
    parser.add_argument('--project-root', type=Path, default=Path.cwd(),
                       help='Project root directory')
    
    args = parser.parse_args()
    
    updater = ImportUpdater(args.project_root)
    
    if args.scan:
        results = updater.scan_imports()
        print(updater.generate_report())
        
    elif args.update:
        updater.find_python_files()
        results = updater.update_all_imports()
        print(f"Updated {sum(results.values())} files")
        
    elif args.validate:
        updater.find_python_files()
        results = updater.validate_imports()
        if results:
            print(f"Found issues in {len(results)} files")
            for file_path, issues in results.items():
                print(f"{file_path}: {', '.join(issues)}")
        else:
            print("All imports validated successfully!")
            
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 
