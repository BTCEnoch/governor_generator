#!/usr/bin/env python3
"""
🏛️ ENOCHIAN GOVERNOR GENERATION - FINAL SYNTAX FIXER
Fix remaining bracket mismatches and orphaned parentheses in core files
"""

import os
import re
import ast
from datetime import datetime
from typing import List, Tuple

def log_operation(message):
    """Log operation with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_core_files_only():
    """Get only core project files, excluding backups and archives"""
    core_files = []
    for root, dirs, files in os.walk("."):
        # Skip backup and archive directories
        skip_dirs = {
            '.git', '__pycache__', '.pytest_cache', 'venv', 'env', '.env', 'node_modules',
            'reorganization_backup', 'dev_tools_archive', 'import_backup', 'knowledge_base'
        }
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                # Skip if it's in any backup directory
                if not any(skip in file_path for skip in ['backup', 'archive']):
                    core_files.append(file_path)
    
    return core_files

def analyze_bracket_mismatches(content: str) -> List[Tuple[int, str]]:
    """Analyze bracket mismatches in content"""
    lines = content.split('\n')
    issues = []
    
    for i, line in enumerate(lines, 1):
        # Check for common bracket issues
        if '(' in line and ')' in line:
            open_count = line.count('(')
            close_count = line.count(')')
            if open_count != close_count:
                issues.append((i, f"Parentheses mismatch: {open_count} open, {close_count} close"))
        
        if '[' in line and ']' in line:
            open_count = line.count('[')
            close_count = line.count(']')
            if open_count != close_count:
                issues.append((i, f"Square bracket mismatch: {open_count} open, {close_count} close"))
        
        # Check for orphaned brackets at start of line
        if re.match(r'^\s*[\)\]]+\s*$', line):
            issues.append((i, "Orphaned closing brackets"))
        
        # Check for orphaned commas with brackets
        if re.match(r'^\s*,\s*[\)\]]+\s*$', line):
            issues.append((i, "Orphaned comma with closing brackets"))
    
    return issues

def fix_bracket_mismatches(file_path: str) -> int:
    """Fix bracket mismatches in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_made = 0
        lines = content.split('\n')
        
        # Track bracket state across lines
        paren_stack = []
        bracket_stack = []
        fixed_lines = []
        
        for i, line in enumerate(lines):
            original_line = line
            
            # Remove orphaned closing brackets at start of line
            if re.match(r'^\s*[\)\]]+\s*$', line):
                line = ''
                fixes_made += 1
                log_operation(f"   🔧 Removed orphaned brackets on line {i+1}")
            
            # Remove orphaned commas with brackets
            elif re.match(r'^\s*,\s*[\)\]]+\s*$', line):
                line = ''
                fixes_made += 1
                log_operation(f"   🔧 Removed orphaned comma+brackets on line {i+1}")
            
            # Fix lines that end with orphaned opening brackets
            elif re.search(r'[\(\[]\s*$', line) and not re.search(r'=\s*[\(\[]\s*$', line):
                # Check if next line starts with closing bracket
                if i + 1 < len(lines) and re.match(r'^\s*[\)\]]+', lines[i + 1]):
                    line = re.sub(r'[\(\[]\s*$', '', line)
                    fixes_made += 1
                    log_operation(f"   🔧 Removed orphaned opening brackets on line {i+1}")
            
            # Fix specific patterns in knowledge database files
            if 'knowledge_database.py' in file_path:
                # Fix KnowledgeEntry construction issues
                if 'KnowledgeEntry(' in line and line.count('(') > line.count(')'):
                    # Check if this is a multi-line KnowledgeEntry
                    if i + 1 < len(lines) and 'id=' in lines[i + 1]:
                        # This is likely correct, leave as is
                        pass
                    else:
                        # Close the parenthesis
                        line = line + ')'
                        fixes_made += 1
                        log_operation(f"   🔧 Closed KnowledgeEntry parenthesis on line {i+1}")
            
            fixed_lines.append(line)
        
        # Reconstruct content
        content = '\n'.join(fixed_lines)
        
        # Clean up multiple empty lines
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return fixes_made
        
        return 0
    except Exception as e:
        log_operation(f"   ❌ Error fixing {file_path}: {e}")
        return 0

def fix_specific_lighthouse_files():
    """Fix specific issues in lighthouse tradition files"""
    lighthouse_files = [
        'core/lighthouse/traditions/enochian_knowledge_database.py',
        'core/lighthouse/traditions/golden_dawn_knowledge_database.py',
        'core/lighthouse/traditions/hermetic_knowledge_database.py',
        'core/lighthouse/traditions/kabbalah_knowledge_database.py',
        'core/lighthouse/traditions/unified_knowledge_retriever.py'
    ]
    
    total_fixes = 0
    
    for file_path in lighthouse_files:
        if os.path.exists(file_path):
            log_operation(f"🔧 Fixing specific issues in {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                fixes_made = 0
                
                # Fix common patterns in knowledge database files
                patterns_to_fix = [
                    # Fix mismatched KnowledgeEntry brackets
                    (r'KnowledgeEntry\(\s*\n\s*id=', r'KnowledgeEntry(\n        id='),
                    (r'KnowledgeEntry\(\s*\n\s*\n\s*id=', r'KnowledgeEntry(\n        id='),
                    
                    # Fix orphaned closing brackets after list items
                    (r',\s*\n\s*\]\s*\n\s*\)', r'\n    )'),
                    
                    # Fix double closing brackets
                    (r'\]\s*\n\s*\]\s*\n\s*\)', r']\n    )'),
                    
                    # Fix orphaned function calls
                    (r'^\s*\)\s*$', ''),
                    
                    # Clean up empty lines in data structures
                    (r'\[\s*\n\s*\n\s*\]', '[]'),
                    
                    # Fix malformed imports
                    (r'from\s+import\s+', 'from . import '),
                ]
                
                for pattern, replacement in patterns_to_fix:
                    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                    if new_content != content:
                        fixes_made += 1
                        content = new_content
                
                # Manual fixes for specific files
                if 'unified_knowledge_retriever.py' in file_path:
                    # Fix the invalid syntax issue
                    content = re.sub(r'^\s*from\s+import\s*$', '', content, flags=re.MULTILINE)
                    content = re.sub(r'^\s*import\s*$', '', content, flags=re.MULTILINE)
                    fixes_made += 1
                
                # Only write if changes were made
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    total_fixes += fixes_made
                    log_operation(f"   ✅ Fixed {fixes_made} issues in {file_path}")
                
            except Exception as e:
                log_operation(f"   ❌ Error fixing {file_path}: {e}")
    
    return total_fixes

def validate_syntax(file_path: str) -> Tuple[bool, str]:
    """Validate syntax of a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        ast.parse(content)
        return True, ""
    except SyntaxError as e:
        return False, f"Syntax error on line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Parse error: {e}"

def comprehensive_final_fix():
    """Perform comprehensive final fix on all core files"""
    log_operation("🔍 Getting core project files (excluding backups/archives)...")
    
    core_files = get_core_files_only()
    log_operation(f"   Found {len(core_files)} core Python files")
    
    # First, fix specific lighthouse issues
    log_operation("🏛️ Fixing specific lighthouse tradition files...")
    lighthouse_fixes = fix_specific_lighthouse_files()
    log_operation(f"   Made {lighthouse_fixes} lighthouse-specific fixes")
    
    # Then fix general bracket mismatches
    log_operation("🔧 Fixing bracket mismatches in all core files...")
    
    files_with_errors = []
    total_fixes = 0
    files_fixed = 0
    
    # First pass: identify files with syntax errors
    for file_path in core_files:
        is_valid, error = validate_syntax(file_path)
        if not is_valid:
            files_with_errors.append((file_path, error))
    
    log_operation(f"   Found {len(files_with_errors)} core files with syntax errors")
    
    # Second pass: fix the errors
    for file_path, error in files_with_errors:
        fixes_made = fix_bracket_mismatches(file_path)
        if fixes_made > 0:
            files_fixed += 1
            total_fixes += fixes_made
            log_operation(f"   ✅ Fixed {fixes_made} issues in {file_path}")
            
            # Validate the fix
            is_valid, new_error = validate_syntax(file_path)
            if is_valid:
                log_operation(f"   ✓ Syntax now valid: {file_path}")
            else:
                log_operation(f"   ⚠️ Still has issues: {file_path}")
                log_operation(f"     Error: {new_error}")
    
    return files_fixed, total_fixes + lighthouse_fixes

def final_validation():
    """Final validation of all core files"""
    log_operation("🔍 Final validation of all core files...")
    
    core_files = get_core_files_only()
    validation_errors = []
    
    for file_path in core_files:
        is_valid, error = validate_syntax(file_path)
        if not is_valid:
            validation_errors.append(f"{file_path}: {error}")
    
    if validation_errors:
        log_operation(f"⚠️  {len(validation_errors)} core files still have syntax errors:")
        for error in validation_errors:
            log_operation(f"     - {error}")
    else:
        log_operation("✅ All core files have valid syntax!")
    
    return len(validation_errors)

def main():
    """Main function"""
    log_operation("🏛️ ENOCHIAN GOVERNOR GENERATION - FINAL SYNTAX FIXER")
    log_operation("=" * 65)
    
    try:
        files_fixed, total_fixes = comprehensive_final_fix()
        remaining_errors = final_validation()
        
        log_operation("📋 FINAL SYNTAX FIXING SUMMARY:")
        log_operation(f"   Core files fixed: {files_fixed}")
        log_operation(f"   Total fixes made: {total_fixes}")
        log_operation(f"   Remaining core file errors: {remaining_errors}")
        
        if remaining_errors == 0:
            log_operation("🎉 ALL CORE FILES NOW HAVE VALID SYNTAX!")
        else:
            log_operation("⚠️  Some core files still need manual review")
            
    except Exception as e:
        log_operation(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 