#!/usr/bin/env python3
"""
🏛️ ENOCHIAN GOVERNOR GENERATION - TARGETED SYNTAX FIXER
Fix specific syntax issues in the remaining 8 files
"""

import os
import re
from datetime import datetime

def log_operation(message):
    """Log operation with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def fix_knowledge_database_files():
    """Fix specific issues in knowledge database files"""
    files_to_fix = [
        'core/lighthouse/traditions/enochian_knowledge_database.py',
        'core/lighthouse/traditions/golden_dawn_knowledge_database.py',
        'core/lighthouse/traditions/hermetic_knowledge_database.py',
        'core/lighthouse/traditions/kabbalah_knowledge_database.py'
    ]
    
    total_fixes = 0
    
    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            continue
            
        log_operation(f"🔧 Fixing {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            fixes_made = 0
            
            # Fix missing closing parentheses for KnowledgeEntry
            # Pattern: quality=ContentQuality.HIGH followed by newline without closing )
            content = re.sub(
                r'(quality=ContentQuality\.HIGH)\s*\n(\s*)(\w)',
                r'\1\n\2)\n\n\2\3',
                content
            )
            if content != original_content:
                fixes_made += 1
                log_operation(f"   ✅ Fixed KnowledgeEntry closing parenthesis")
            
            # Fix patterns where lists end without proper closing
            content = re.sub(
                r',\s*\n\s*quality=ContentQuality\.HIGH\s*\n\s*([A-Z])',
                r',\n        quality=ContentQuality.HIGH\n    )\n\n    \1',
                content
            )
            
            # Fix missing commas before quality statements
            content = re.sub(
                r'source_url="[^"]*"\s*\n\s*quality=ContentQuality\.HIGH',
                r'source_url=\g<0>,\n        quality=ContentQuality.HIGH',
                content
            )
            
            # Only write if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                total_fixes += fixes_made
                log_operation(f"   ✅ Fixed {file_path}")
        
        except Exception as e:
            log_operation(f"   ❌ Error fixing {file_path}: {e}")
    
    return total_fixes

def fix_unified_knowledge_retriever():
    """Fix specific issues in unified_knowledge_retriever.py"""
    file_path = 'core/lighthouse/traditions/unified_knowledge_retriever.py'
    
    if not os.path.exists(file_path):
        return 0
    
    log_operation(f"🔧 Fixing {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the malformed import statements
        # Pattern: from .module import (function, function, ...
        # Missing closing parentheses
        
        # Fix enochian imports
        content = re.sub(
            r'from \.enochian_knowledge_database import \(\s*create_enochian_tradition, get_enochian_entry_by_id,\s*search_enochian_by_tag, get_all_enochian_entries\s*$',
            r'from .enochian_knowledge_database import (\n    create_enochian_tradition, get_enochian_entry_by_id,\n    search_enochian_by_tag, get_all_enochian_entries\n)',
            content,
            flags=re.MULTILINE
        )
        
        # Fix hermetic imports
        content = re.sub(
            r'from \.hermetic_knowledge_database import \(\s*create_hermetic_tradition, get_hermetic_entry_by_id,\s*search_hermetic_by_tag, get_all_hermetic_entries, get_seven_principles\s*$',
            r'from .hermetic_knowledge_database import (\n    create_hermetic_tradition, get_hermetic_entry_by_id,\n    search_hermetic_by_tag, get_all_hermetic_entries, get_seven_principles\n)',
            content,
            flags=re.MULTILINE
        )
        
        # Fix kabbalah imports
        content = re.sub(
            r'from \.kabbalah_knowledge_database import \(\s*create_kabbalah_tradition, get_kabbalah_entry_by_id,\s*search_kabbalah_by_tag, get_all_kabbalah_entries, get_ten_sefirot\s*$',
            r'from .kabbalah_knowledge_database import (\n    create_kabbalah_tradition, get_kabbalah_entry_by_id,\n    search_kabbalah_by_tag, get_all_kabbalah_entries, get_ten_sefirot\n)',
            content,
            flags=re.MULTILINE
        )
        
        # Fix any remaining broken lines
        content = re.sub(r'if "angel" in entry\.tags or "key" in entry\.tags\s*$', 
                        r'if "angel" in entry.tags or "key" in entry.tags]', 
                        content, flags=re.MULTILINE)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            log_operation(f"   ✅ Fixed {file_path}")
            return 1
        
        return 0
    
    except Exception as e:
        log_operation(f"   ❌ Error fixing {file_path}: {e}")
        return 0

def fix_utility_scripts():
    """Fix specific issues in utility scripts"""
    files_to_fix = [
        'tools/utilities/scripts/ai_governor_review_system.py',
        'tools/utilities/scripts/batch_governor_review.py',
        'tools/utilities/scripts/production_readiness_assessment.py'
    ]
    
    total_fixes = 0
    
    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            continue
            
        log_operation(f"🔧 Fixing {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix missing closing bracket in logging configuration
            content = re.sub(
                r'logging\.StreamHandler\(\)\s*$',
                r'logging.StreamHandler()\n    ]',
                content,
                flags=re.MULTILINE
            )
            
            # Fix orphaned import statements
            content = re.sub(
                r'\.parent\.parent\)\s*$',
                r'.parent.parent)',
                content,
                flags=re.MULTILINE
            )
            
            # Fix malformed list endings
            content = re.sub(
                r'"[^"]*\.json"\s*$',
                r'\g<0>]',
                content,
                flags=re.MULTILINE
            )
            
            # Only write if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                total_fixes += 1
                log_operation(f"   ✅ Fixed {file_path}")
        
        except Exception as e:
            log_operation(f"   ❌ Error fixing {file_path}: {e}")
    
    return total_fixes

def manual_fix_specific_lines():
    """Manually fix the specific line issues identified"""
    fixes_made = 0
    
    # Fix enochian_knowledge_database.py line 42 area
    file_path = 'core/lighthouse/traditions/enochian_knowledge_database.py'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Look for the problematic area around line 42
        for i, line in enumerate(lines):
            if 'quality=ContentQuality.HIGH' in line and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not next_line.startswith(')') and not next_line.startswith('#'):
                    # Insert closing parenthesis
                    lines.insert(i + 1, '    )\n\n')
                    fixes_made += 1
                    break
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    # Fix unified_knowledge_retriever.py import issues
    file_path = 'core/lighthouse/traditions/unified_knowledge_retriever.py'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the specific import lines manually
        new_content = content.replace(
            'from .enochian_knowledge_database import (\n    create_enochian_tradition, get_enochian_entry_by_id, \n    search_enochian_by_tag, get_all_enochian_entries\nfrom .hermetic_knowledge_database import (',
            'from .enochian_knowledge_database import (\n    create_enochian_tradition, get_enochian_entry_by_id, \n    search_enochian_by_tag, get_all_enochian_entries\n)\nfrom .hermetic_knowledge_database import ('
        )
        
        new_content = new_content.replace(
            'from .hermetic_knowledge_database import (\n    create_hermetic_tradition, get_hermetic_entry_by_id,\n    search_hermetic_by_tag, get_all_hermetic_entries, get_seven_principles\nfrom .kabbalah_knowledge_database import (',
            'from .hermetic_knowledge_database import (\n    create_hermetic_tradition, get_hermetic_entry_by_id,\n    search_hermetic_by_tag, get_all_hermetic_entries, get_seven_principles\n)\nfrom .kabbalah_knowledge_database import ('
        )
        
        new_content = new_content.replace(
            'from .kabbalah_knowledge_database import (\n    create_kabbalah_tradition, get_kabbalah_entry_by_id,\n    search_kabbalah_by_tag, get_all_kabbalah_entries, get_ten_sefirot',
            'from .kabbalah_knowledge_database import (\n    create_kabbalah_tradition, get_kabbalah_entry_by_id,\n    search_kabbalah_by_tag, get_all_kabbalah_entries, get_ten_sefirot\n)'
        )
        
        # Fix the incomplete list comprehension
        new_content = new_content.replace(
            'if "angel" in entry.tags or "key" in entry.tags\n\n        ',
            'if "angel" in entry.tags or "key" in entry.tags]\n\n        '
        )
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixes_made += 1
    
    # Fix ai_governor_review_system.py logging issue
    file_path = 'tools/utilities/scripts/ai_governor_review_system.py'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the logging handlers issue
        new_content = content.replace(
            "        logging.StreamHandler()\n\n@dataclass",
            "        logging.StreamHandler()\n    ]\n)\n\n@dataclass"
        )
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixes_made += 1
    
    return fixes_made

def main():
    """Main function"""
    log_operation("🏛️ ENOCHIAN GOVERNOR GENERATION - TARGETED SYNTAX FIXER")
    log_operation("=" * 70)
    
    try:
        total_fixes = 0
        
        # Fix knowledge database files
        log_operation("🔧 Fixing knowledge database files...")
        total_fixes += fix_knowledge_database_files()
        
        # Fix unified knowledge retriever
        log_operation("🔧 Fixing unified knowledge retriever...")
        total_fixes += fix_unified_knowledge_retriever()
        
        # Fix utility scripts
        log_operation("🔧 Fixing utility scripts...")
        total_fixes += fix_utility_scripts()
        
        # Manual fixes for specific line issues
        log_operation("🔧 Applying manual fixes...")
        total_fixes += manual_fix_specific_lines()
        
        log_operation(f"✅ Targeted syntax fixing completed!")
        log_operation(f"   Total fixes made: {total_fixes}")
        
        return total_fixes
        
    except Exception as e:
        log_operation(f"❌ Error: {e}")
        return 0

if __name__ == "__main__":
    exit(main()) 