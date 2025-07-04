#!/usr/bin/env python3
"""
Import Path Updater Script
========================

Updates import statements throughout the codebase to match the new directory structure.
Handles sys.path manipulation removal and import validation.

Usage:
    python scripts/update_imports.py --mode scan
    python scripts/update_imports.py --mode update
    python scripts/update_imports.py --mode validate
"""

import os
import re
import ast
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ImportUpdater")

class ImportUpdater:
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root if project_root is not None else Path.cwd()
        self.backup_dir = self.project_root / "import_backup"
        self.report_file = self.project_root / "import_update_report.json"
        
        # Import path mappings based on directory reorganization
        self.import_mappings = {
            # Data imports
            'clean_governor_profiles': 'data.governors.profiles',
            'governor_indexes': 'data.governors.indexes',
            'personality_seeds': 'data.governors.seeds',
            'canon': 'data.canon',
            
            # Knowledge base imports
            'core.lighthouse.archives.governor_archives': 'data.knowledge.archives',
            'core.lighthouse.archives.personality_seeds': 'data.knowledge.seeds',
            'core.lighthouse.links': 'data.knowledge.links',
            'core.lighthouse.data': 'data.knowledge.data',
            'core.lighthouse.generated': 'data.knowledge.generated',
            'core.lighthouse.traditions': 'core.lighthouse.traditions',
            'core.lighthouse.retrievers': 'core.lighthouse.retrievers',
            'core.lighthouse.schemas': 'core.lighthouse.schemas',
            'knowledge_base': 'core.lighthouse',
            
            # Engine imports
            'mystical_systems': 'engines.mystical_systems',
            'storyline_engine': 'engines.storyline_generation',
            'unified_profiler': 'core.governors.profiler',
            'integration_layer': 'engines.batch_processing',
            
            # Build system imports
            'trac_build': 'build_system.trac_build',
            
            # Tools imports
            'cli': 'tools.cli',
            'scripts': 'tools.utilities',
            'tests': 'tools.validation',
            'game_mechanics': 'tools.game_mechanics',
            
            # Game assets
            'pack': 'core.game_assets.pack',
        }
        
        # Files to process
        self.python_files = []
        self.scan_results = {
            'files_scanned': 0,
            'imports_found': 0,
            'imports_to_update': [],
            'sys_path_manipulations': [],
            'circular_imports': [],
            'errors': []
        }
        
    def find_python_files(self) -> List[Path]:
        """Find all Python files in the project"""
        python_files = []
        
        # Search in all directories
        for root, dirs, files in os.walk(self.project_root):
            # Skip hidden directories, __pycache__, and backup directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and 'backup' not in d.lower()]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
                    
        return python_files
        
    def parse_imports(self, file_path: Path) -> List[Dict]:
        """Parse imports from a Python file"""
        imports = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse with AST
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({
                            'type': 'import',
                            'module': alias.name,
                            'alias': alias.asname,
                            'line': node.lineno
                        })
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append({
                            'type': 'from_import',
                            'module': node.module,
                            'names': [alias.name for alias in node.names],
                            'line': node.lineno
                        })
                        
        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
            self.scan_results['errors'].append(f"Parse error in {file_path}: {e}")
            
        return imports
        
    def find_sys_path_manipulations(self, file_path: Path) -> List[Dict]:
        """Find sys.path manipulation statements"""
        sys_path_lines = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                if 'sys.path' in line and ('append' in line or 'insert' in line):
                    sys_path_lines.append({
                        'file': file_path,
                        'line': i,
                        'content': line.strip()
                    })
                    
        except Exception as e:
            logger.error(f"Failed to scan sys.path in {file_path}: {e}")
            
        return sys_path_lines
        
    def scan_imports(self) -> None:
        """Scan all Python files for imports that need updating"""
        logger.info("Scanning for imports to update...")
        
        self.python_files = self.find_python_files()
        logger.info(f"Found {len(self.python_files)} Python files")
        
        for file_path in self.python_files:
            self.scan_results['files_scanned'] += 1
            
            # Parse imports
            imports = self.parse_imports(file_path)
            self.scan_results['imports_found'] += len(imports)
            
            # Check for imports that need updating
            for import_info in imports:
                module = import_info['module']
                
                # Check if this import needs updating
                for old_path, new_path in self.import_mappings.items():
                    if module == old_path or module.startswith(old_path + '.'):
                        # Calculate new module path
                        new_module = module.replace(old_path, new_path, 1)
                        
                        self.scan_results['imports_to_update'].append({
                            'file': str(file_path),
                            'line': import_info['line'],
                            'old_module': module,
                            'new_module': new_module,
                            'type': import_info['type']
                        })
                        
            # Find sys.path manipulations
            sys_path_lines = self.find_sys_path_manipulations(file_path)
            self.scan_results['sys_path_manipulations'].extend(sys_path_lines)
            
        logger.info(f"Scan complete: {self.scan_results['imports_found']} imports found, "
                   f"{len(self.scan_results['imports_to_update'])} need updating")
                   
    def update_imports(self) -> None:
        """Update import statements in files"""
        logger.info("Updating import statements...")
        
        # Create backup
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)
            
        files_to_update = set()
        for import_info in self.scan_results['imports_to_update']:
            files_to_update.add(import_info['file'])
            
        for file_path_str in files_to_update:
            file_path = Path(file_path_str)
            
            # Create backup
            backup_path = self.backup_dir / file_path.name
            backup_path.write_text(file_path.read_text(encoding='utf-8'), encoding='utf-8')
            
            # Update file
            self.update_file_imports(file_path)
            
        logger.info(f"Updated imports in {len(files_to_update)} files")
        
    def update_file_imports(self, file_path: Path) -> None:
        """Update imports in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            # Update imports
            for import_info in self.scan_results['imports_to_update']:
                if import_info['file'] == str(file_path):
                    old_module = import_info['old_module']
                    new_module = import_info['new_module']
                    
                    # Replace import statements
                    if import_info['type'] == 'import':
                        content = re.sub(
                            rf'\bimport\s+{re.escape(old_module)}\b',
                            f'import {new_module}',
                            content
                        )
                    elif import_info['type'] == 'from_import':
                        content = re.sub(
                            rf'\bfrom\s+{re.escape(old_module)}\s+import\b',
                            f'from {new_module} import',
                            content
                        )
                        
            # Remove sys.path manipulations
            for sys_path_info in self.scan_results['sys_path_manipulations']:
                if sys_path_info['file'] == file_path:
                    # Comment out sys.path lines
                    line_content = sys_path_info['content']
                    content = content.replace(line_content, f'# {line_content}  # Removed during reorganization')
                    
            # Write updated content
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"Updated imports in {file_path}")
                
        except Exception as e:
            logger.error(f"Failed to update {file_path}: {e}")
            self.scan_results['errors'].append(f"Update error in {file_path}: {e}")
            
    def validate_imports(self) -> None:
        """Validate that updated imports work"""
        logger.info("Validating updated imports...")
        
        validation_errors = []
        
        for file_path in self.python_files:
            try:
                # Try to compile the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                ast.parse(content)
                logger.debug(f"Validated {file_path}")
                
            except SyntaxError as e:
                validation_errors.append(f"Syntax error in {file_path}: {e}")
                logger.error(f"Syntax error in {file_path}: {e}")
            except Exception as e:
                validation_errors.append(f"Validation error in {file_path}: {e}")
                logger.error(f"Validation error in {file_path}: {e}")
                
        if validation_errors:
            logger.error(f"Found {len(validation_errors)} validation errors")
            for error in validation_errors:
                logger.error(error)
        else:
            logger.info("All files validated successfully")
            
    def generate_report(self) -> None:
        """Generate detailed report of import updates"""
        import json
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'files_scanned': self.scan_results['files_scanned'],
                'imports_found': self.scan_results['imports_found'],
                'imports_updated': len(self.scan_results['imports_to_update']),
                'sys_path_removed': len(self.scan_results['sys_path_manipulations']),
                'errors': len(self.scan_results['errors'])
            },
            'details': self.scan_results
        }
        
        with open(self.report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        logger.info(f"Report generated: {self.report_file}")
        
    def run(self, mode: str) -> None:
        """Run the import updater in specified mode"""
        if mode == 'scan':
            self.scan_imports()
            self.generate_report()
        elif mode == 'update':
            self.scan_imports()
            self.update_imports()
            self.generate_report()
        elif mode == 'validate':
            self.validate_imports()
        else:
            logger.error(f"Unknown mode: {mode}")

def main():
    parser = argparse.ArgumentParser(description='Update import statements for reorganized project')
    parser.add_argument('--mode', choices=['scan', 'update', 'validate'], required=True,
                       help='Mode to run: scan, update, or validate')
    parser.add_argument('--project-root', type=Path, default=Path.cwd(),
                       help='Project root directory')
    
    args = parser.parse_args()
    
    updater = ImportUpdater(args.project_root)
    updater.run(args.mode)

if __name__ == "__main__":
    main() 