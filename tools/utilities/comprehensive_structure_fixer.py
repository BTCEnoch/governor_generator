#!/usr/bin/env python3
"""
🏛️ ENOCHIAN GOVERNOR GENERATION - COMPREHENSIVE STRUCTURE FIXER
Fix all structural issues in knowledge database files
"""

import os
import re
from datetime import datetime

def log_operation(message):
    """Log operation with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def fix_knowledge_database_structure(file_path):
    """Fix the structure of a knowledge database file"""
    if not os.path.exists(file_path):
        return False
    
    log_operation(f"🔧 Fixing structure of {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the main list structure
        # 1. Ensure the opening list bracket is properly placed
        content = re.sub(r'^(\s*)(def\s+\w+.*?:\s*\n\s*"""[^"]*"""\s*\n)', r'\1\2\1return [', content, flags=re.MULTILINE | re.DOTALL)
        
        # 2. Fix KnowledgeEntry closures - ensure each KnowledgeEntry is properly closed
        content = re.sub(
            r'(\s+quality=ContentQuality\.HIGH)\s*\n\s*\n\s*(KnowledgeEntry\(|#|\]|$)',
            r'\1\n    ),\n\n    \2',
            content,
            flags=re.MULTILINE
        )
        
        # 3. Fix the end of function - ensure proper list closure
        content = re.sub(
            r'(\s+quality=ContentQuality\.HIGH)\s*\n\s*$',
            r'\1\n    )\n]',
            content,
            flags=re.MULTILINE
        )
        
        # 4. Fix any remaining structural issues
        content = re.sub(r'\n\s*\n\s*\n\s*\)', r'\n    )', content)
        content = re.sub(r'\]\s*\n\s*\n\s*def', r']\n\ndef', content)
        
        # 5. Clean up any double list closures
        content = re.sub(r'\]\s*\n\s*\]', r']', content)
        
        # 6. Ensure proper spacing
        content = re.sub(r'\n\n\n+', r'\n\n', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            log_operation(f"   ✅ Fixed structure of {file_path}")
            return True
        
        return False
    
    except Exception as e:
        log_operation(f"   ❌ Error fixing {file_path}: {e}")
        return False

def fix_unified_knowledge_retriever():
    """Fix the unified knowledge retriever imports"""
    file_path = 'core/lighthouse/traditions/unified_knowledge_retriever.py'
    
    if not os.path.exists(file_path):
        return False
    
    log_operation(f"🔧 Fixing {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Rewrite the import section completely
        new_imports = '''from typing import Dict, List, Optional
from core.lighthouse.schemas.knowledge_schemas import KnowledgeEntry, ProcessedTradition, KnowledgeType

# Import all tradition databases
from .enochian_knowledge_database import (
    create_enochian_tradition, get_enochian_entry_by_id, 
    search_enochian_by_tag, get_all_enochian_entries
)
from .hermetic_knowledge_database import (
    create_hermetic_tradition, get_hermetic_entry_by_id,
    search_hermetic_by_tag, get_all_hermetic_entries, get_seven_principles
)
from .kabbalah_knowledge_database import (
    create_kabbalah_tradition, get_kabbalah_entry_by_id,
    search_kabbalah_by_tag, get_all_kabbalah_entries, get_ten_sefirot
)
'''
        
        # Replace the problematic import section
        content = re.sub(
            r'from (?:schemas\.knowledge_schemas|core\.lighthouse\.schemas\.knowledge_schemas).*?from \.kabbalah_knowledge_database import[^)]*\)',
            new_imports,
            content,
            flags=re.DOTALL
        )
        
        # Fix the incomplete list comprehension
        content = re.sub(
            r'if "angel" in entry\.tags or "key" in entry\.tags\s*\n\s*\n\s*return foundational',
            r'if "angel" in entry.tags or "key" in entry.tags]\n\n        return foundational',
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        log_operation(f"   ✅ Fixed {file_path}")
        return True
        
    except Exception as e:
        log_operation(f"   ❌ Error fixing {file_path}: {e}")
        return False

def fix_utility_script_logging():
    """Fix the logging configuration in utility scripts"""
    files_to_fix = [
        'tools/utilities/scripts/ai_governor_review_system.py',
        'tools/utilities/scripts/batch_governor_review.py',
        'tools/utilities/scripts/production_readiness_assessment.py'
    ]
    
    fixes_made = 0
    
    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            continue
        
        log_operation(f"🔧 Fixing logging in {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix logging configuration
            content = re.sub(
                r'(logging\.basicConfig\(\s*level=logging\.INFO,\s*format=\'[^\']*\',\s*handlers=\[\s*logging\.FileHandler\([^)]*\),\s*logging\.StreamHandler\(\)\s*)\n',
                r'\1\n    ]\n)\n',
                content,
                flags=re.MULTILINE
            )
            
            # Fix other structural issues
            content = re.sub(r'sys\.path\.append\(str\(Path\(__file__\)\.parent\.parent\.parent\)\)', r'sys.path.append(str(Path(__file__).parent.parent.parent))', content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            fixes_made += 1
            log_operation(f"   ✅ Fixed {file_path}")
            
        except Exception as e:
            log_operation(f"   ❌ Error fixing {file_path}: {e}")
    
    return fixes_made

def main():
    """Main function"""
    log_operation("🏛️ ENOCHIAN GOVERNOR GENERATION - COMPREHENSIVE STRUCTURE FIXER")
    log_operation("=" * 75)
    
    total_fixes = 0
    
    # Fix knowledge database files
    knowledge_files = [
        'core/lighthouse/traditions/enochian_knowledge_database.py',
        'core/lighthouse/traditions/golden_dawn_knowledge_database.py',
        'core/lighthouse/traditions/hermetic_knowledge_database.py',
        'core/lighthouse/traditions/kabbalah_knowledge_database.py'
    ]
    
    for file_path in knowledge_files:
        if fix_knowledge_database_structure(file_path):
            total_fixes += 1
    
    # Fix unified knowledge retriever
    if fix_unified_knowledge_retriever():
        total_fixes += 1
    
    # Fix utility scripts
    total_fixes += fix_utility_script_logging()
    
    log_operation(f"✅ Comprehensive structure fixing completed!")
    log_operation(f"   Total files fixed: {total_fixes}")
    
    return total_fixes

if __name__ == "__main__":
    exit(main()) 
