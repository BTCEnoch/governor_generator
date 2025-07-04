#!/usr/bin/env python3
"""
🏛️ ENOCHIAN GOVERNOR GENERATION - COMPREHENSIVE IMPORT FIXER
Fix all broken import paths after project reorganization
"""

import os
import re
import ast
import sys
from pathlib import Path
from datetime import datetime
import json

def log_operation(message):
    """Log operation with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_comprehensive_import_mappings():
    """Get comprehensive mapping of old import paths to new paths"""
    return {
        # Original locations → New locations
        
        # Clean governor profiles
        "clean_governor_profiles": "data.governors.profiles",
        "from clean_governor_profiles": "from data.governors.profiles",
        
        # Governor indexes
        "governor_indexes": "data.governors.indexes",
        "from governor_indexes": "from data.governors.indexes",
        
        # Personality seeds
        "personality_seeds": "data.governors.seeds",
        "from personality_seeds": "from data.governors.seeds",
        
        # Canon materials
        "canon": "data.canon",
        "from canon": "from data.canon",
        
        # Knowledge base and lighthouse
        "knowledge_base": "core.lighthouse",
        "from knowledge_base": "from core.lighthouse",
        "core.lighthouse.schemas": "core.lighthouse.schemas",
        "core.lighthouse.retrievers": "core.lighthouse.retrievers",
        "core.lighthouse.traditions": "core.lighthouse.traditions",
        "core.lighthouse.utils": "core.lighthouse.utils",
        "core.lighthouse.data": "data.knowledge.data",
        "core.lighthouse.generated": "data.knowledge.generated",
        "core.lighthouse.links": "data.knowledge.links",
        "core.lighthouse.archives": "data.knowledge.archives",
        
        # Storyline engine
        "storyline_engine": "engines.storyline_generation",
        "from storyline_engine": "from engines.storyline_generation",
        "engines.storyline_generation.schemas": "engines.storyline_generation.schemas",
        "engines.storyline_generation.dev_tools": "engines.storyline_generation.dev_tools",
        
        # Mystical systems
        "mystical_systems": "engines.mystical_systems",
        "from mystical_systems": "from engines.mystical_systems",
        "engines.mystical_systems.tarot_system": "engines.engines.mystical_systems.tarot_system",
        "engines.mystical_systems.kabbalah_system": "engines.engines.mystical_systems.kabbalah_system",
        "engines.mystical_systems.numerology_system": "engines.engines.mystical_systems.numerology_system",
        "engines.mystical_systems.zodiac_system": "engines.engines.mystical_systems.zodiac_system",
        
        # Unified profiler
        "unified_profiler": "core.governors.profiler",
        "from unified_profiler": "from core.governors.profiler",
        "core.governors.profiler.core": "core.governors.profiler.core",
        "core.governors.profiler.interfaces": "core.governors.profiler.interfaces",
        "core.governors.profiler.schemas": "core.governors.profiler.schemas",
        
        # Game mechanics
        "game_mechanics": "tools.game_mechanics",
        "from game_mechanics": "from tools.game_mechanics",
        "tools.game_mechanics.dialog_system": "tools.game_mechanics.dialog_system",
        "tools.game_mechanics.expansion_system": "tools.game_mechanics.expansion_system",
        "tools.game_mechanics.divination_systems": "tools.game_mechanics.divination_systems",
        
        # Integration layer
        "integration_layer": "engines.batch_processing",
        "from integration_layer": "from engines.batch_processing",
        "engines.batch_processing.coordinators": "engines.batch_processing.coordinators",
        
        # Scripts
        "scripts": "tools.utilities",
        "from scripts": "from tools.utilities",
        
        # CLI
        "cli": "tools.cli",
        "from cli": "from tools.cli",
        
        # Tests
        "tests": "tools.validation",
        "from tests": "from tools.validation",
        
        # Trac build
        "trac_build": "build_system.trac_build",
        "from trac_build": "from build_system.trac_build",
        
        # Pack assets
        "pack": "core.game_assets.pack",
        "from pack": "from core.game_assets.pack",
        
        # JSON cleaner
        "json_cleaner": "tools.utilities.json_cleaner",
        "from json_cleaner": "from tools.utilities.json_cleaner",
        
        # Batch jobs
        "batch_jobs": "engines.batch_processing.jobs",
        "from batch_jobs": "from engines.batch_processing.jobs",
        
        # Logs
        "logs": "tools.utilities.logs",
        "from logs": "from tools.utilities.logs",
        
        # Governor output
        "governor_output": "data.governors.output",
        "from governor_output": "from data.governors.output",
        
        # Validation output
        "validation_output": "tools.validation.output",
        "from validation_output": "from tools.validation.output",
        
        # Storyline output
        "storyline_output": "engines.storyline_generation.output",
        "from storyline_output": "from engines.storyline_generation.output",
        
        # Specific file mappings for common patterns
        "from lighthouse_research_index": "from core.lighthouse.lighthouse_research_index",
        "from run_lighthouse_research": "from core.lighthouse.run_lighthouse_research",
        "from wiki_api_extractor": "from core.lighthouse.wiki_api_extractor",
        "from knowledge_entry_generator": "from core.lighthouse.knowledge_entry_generator",
        "from mystical_cli": "from tools.tools.cli.mystical_cli",
        
        # Governor specific imports
        "from governor_engine": "from engines.storyline_generation.governor_engine",
        "from enhanced_story_builder": "from engines.storyline_generation.enhanced_story_builder",
        "from canonical_loader": "from engines.storyline_generation.canonical_loader",
        "from batch_storyline_generator": "from engines.storyline_generation.batch_storyline_generator",
        
        # Tarot system imports
        "from tarot_system": "from engines.engines.mystical_systems.tarot_system",
        "from tarot_cards_database": "from engines.mystical_systems.tarot_system.data.tarot_cards_database",
        
        # Profiler imports
        "from mystical_profiler": "from core.governors.profiler.core.mystical_profiler",
        "from system_registry": "from core.governors.profiler.core.system_registry",
        
        # Schema imports
        "from governor_input_schema": "from engines.storyline_generation.schemas.governor_input_schema",
        "from storyline_output_schema": "from engines.storyline_generation.schemas.storyline_output_schema",
        "from mystical_schemas": "from core.governors.profiler.schemas.mystical_schemas",
        "from knowledge_schemas": "from core.lighthouse.schemas.knowledge_schemas",
        "from discovery_schemas": "from core.lighthouse.schemas.discovery_schemas",
        
        # Batch processing
        "from batch_governor_assignment": "from engines.batch_processing.coordinators.batch_governor_assignment",
        
        # Dialog system
        "from core_structures": "from tools.game_mechanics.dialog_system.core_structures",
        "from behavioral_filter": "from tools.game_mechanics.dialog_system.behavioral_filter",
        "from intent_classifier": "from tools.game_mechanics.dialog_system.intent_classifier",
        "from nlu_engine": "from tools.game_mechanics.dialog_system.nlu_engine",
        
        # Expansion system
        "from dynamic_menu": "from tools.game_mechanics.expansion_system.ui.dynamic_menu",
        "from error_recovery": "from tools.game_mechanics.expansion_system.ui.error_recovery",
        
        # Divination systems
        "from tarot_game_engine": "from tools.game_mechanics.divination_systems.tarot_game_engine",
        "from tarot_game_interface": "from tools.game_mechanics.divination_systems.tarot_game_interface",
    }

def find_all_python_files(root_dir="."):
    """Find all Python files in the project"""
    python_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv', 'env', '.env', 'node_modules'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    return python_files

def analyze_imports(file_path):
    """Analyze imports in a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to find imports
        tree = ast.parse(content)
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imports.append(f"from {module} import {', '.join(alias.name for alias in node.names)}")
        
        return imports, content
    except Exception as e:
        log_operation(f"   ❌ Error analyzing {file_path}: {e}")
        return [], ""

def fix_imports_in_file(file_path, import_mappings):
    """Fix imports in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_made = 0
        
        # Fix import statements
        for old_pattern, new_pattern in import_mappings.items():
            # Handle different import patterns
            patterns = [
                # Direct imports: import module
                (rf'\bimport\s+{re.escape(old_pattern)}(?=\s|$|\.)', f'import {new_pattern}'),
                # From imports: from module import ...
                (rf'\bfrom\s+{re.escape(old_pattern)}(?=\s|$|\.)', f'from {new_pattern}'),
                # Module references in imports
                (rf'\b{re.escape(old_pattern)}\.', f'{new_pattern}.'),
            ]
            
            for pattern, replacement in patterns:
                new_content = re.sub(pattern, replacement, content)
                if new_content != content:
                    fixes_made += len(re.findall(pattern, content))
                    content = new_content
        
        # Remove sys.path manipulations
        sys_path_patterns = [
            r'sys\.path\.append\([^)]+\)\n?',
            r'sys\.path\.insert\([^)]+\)\n?',
            r'import sys\n(?=.*sys\.path)',
            r'            r'        ]
        
        for pattern in sys_path_patterns:
            new_content = re.sub(pattern, '', content, flags=re.MULTILINE)
            if new_content != content:
                fixes_made += 1
                content = new_content
        
        # Clean up extra newlines
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return fixes_made
        
        return 0
    except Exception as e:
        log_operation(f"   ❌ Error fixing imports in {file_path}: {e}")
        return 0

def scan_and_fix_imports():
    """Scan all Python files and fix import statements"""
    log_operation("🔍 Scanning for all Python files...")
    
    python_files = find_all_python_files()
    log_operation(f"   Found {len(python_files)} Python files")
    
    import_mappings = get_comprehensive_import_mappings()
    log_operation(f"   Using {len(import_mappings)} import mappings")
    
    total_fixes = 0
    files_modified = 0
    
    log_operation("🔧 Fixing imports in all files...")
    
    for file_path in python_files:
        fixes_made = fix_imports_in_file(file_path, import_mappings)
        if fixes_made > 0:
            files_modified += 1
            total_fixes += fixes_made
            log_operation(f"   ✅ Fixed {fixes_made} imports in {file_path}")
    
    log_operation(f"✅ Import fixing completed!")
    log_operation(f"   📊 Files modified: {files_modified}")
    log_operation(f"   📊 Total fixes made: {total_fixes}")
    
    return files_modified, total_fixes

def validate_imports():
    """Validate that imports are working correctly"""
    log_operation("🔍 Validating import fixes...")
    
    python_files = find_all_python_files()
    validation_errors = []
    
    for file_path in python_files:
        try:
            # Try to parse the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            ast.parse(content)
            
        except SyntaxError as e:
            validation_errors.append(f"Syntax error in {file_path}: {e}")
        except Exception as e:
            validation_errors.append(f"Error parsing {file_path}: {e}")
    
    if validation_errors:
        log_operation(f"⚠️  Found {len(validation_errors)} validation errors:")
        for error in validation_errors[:10]:  # Show first 10 errors
            log_operation(f"     - {error}")
        if len(validation_errors) > 10:
            log_operation(f"     ... and {len(validation_errors) - 10} more errors")
    else:
        log_operation("✅ All import fixes validated successfully!")
    
    return len(validation_errors)

def main():
    """Main function"""
    log_operation("🏛️ ENOCHIAN GOVERNOR GENERATION - COMPREHENSIVE IMPORT FIXER")
    log_operation("=" * 70)
    
    try:
        files_modified, total_fixes = scan_and_fix_imports()
        validation_errors = validate_imports()
        
        log_operation("📋 IMPORT FIXING SUMMARY:")
        log_operation(f"   Files modified: {files_modified}")
        log_operation(f"   Total fixes made: {total_fixes}")
        log_operation(f"   Validation errors: {validation_errors}")
        
        if validation_errors == 0:
            log_operation("🎉 All import paths have been successfully fixed!")
        else:
            log_operation("⚠️  Some validation errors remain - manual review needed")
            
    except Exception as e:
        log_operation(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 
