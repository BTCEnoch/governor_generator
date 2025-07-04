#!/usr/bin/env python3
"""
🏛️ ENOCHIAN GOVERNOR GENERATION - SYNTAX ERROR FIXER
Fix orphaned parentheses and other syntax errors left by import fixing
"""

import os
import re
import ast
from datetime import datetime

def log_operation(message):
    """Log operation with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

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

def fix_orphaned_parentheses(file_path):
    """Fix orphaned parentheses in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_made = 0
        
        # Common patterns to fix
        patterns_to_fix = [
            # Orphaned parentheses from sys.path statements
            (r'^, [\'"][^\'")]*[\'"]?\)\)\s*$', ''),  # Lines like ", 'traditions'))"
            (r'^, [\'"][^\'")]*[\'"]?\)\s*$', ''),    # Lines like ", 'traditions')"
            (r'^\s*,\s*[\'"][^\'")]*[\'"]?\)\s*$', ''),  # Lines like "    , 'traditions')"
            
            # Empty sys.path related lines
            (r'^# Add path for imports\s*$', ''),
            (r'^# Add project root to path\s*$', ''),
            (r'^# Add parent directory to path\s*$', ''),
            
            # Orphaned import statements
            (r'^\s*import\s+sys\s*$(?!\n.*sys\.)', ''),  # Remove standalone 'import sys' if sys not used
            
            # Fix double newlines
            (r'\n\n\n+', '\n\n'),
        ]
        
        for pattern, replacement in patterns_to_fix:
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            if new_content != content:
                fixes_made += 1
                content = new_content
        
        # Clean up any remaining orphaned lines
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Skip lines that are just orphaned parentheses or commas
            if re.match(r'^\s*[,)]+\s*$', line):
                fixes_made += 1
                continue
            cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return fixes_made
        
        return 0
    except Exception as e:
        log_operation(f"   ❌ Error fixing {file_path}: {e}")
        return 0

def validate_python_syntax(file_path):
    """Check if a Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Parse error: {e}"

def fix_all_syntax_errors():
    """Fix syntax errors in all Python files"""
    log_operation("🔍 Scanning for Python files with syntax errors...")
    
    python_files = find_all_python_files()
    files_with_errors = []
    
    # First pass: identify files with syntax errors
    for file_path in python_files:
        is_valid, error = validate_python_syntax(file_path)
        if not is_valid:
            files_with_errors.append((file_path, error))
    
    log_operation(f"   Found {len(files_with_errors)} files with syntax errors")
    
    if not files_with_errors:
        log_operation("✅ No syntax errors found!")
        return 0, 0
    
    # Second pass: fix the errors
    total_fixes = 0
    files_fixed = 0
    
    for file_path, error in files_with_errors:
        fixes_made = fix_orphaned_parentheses(file_path)
        if fixes_made > 0:
            files_fixed += 1
            total_fixes += fixes_made
            log_operation(f"   ✅ Fixed {fixes_made} syntax issues in {file_path}")
            
            # Validate the fix
            is_valid, new_error = validate_python_syntax(file_path)
            if is_valid:
                log_operation(f"   ✓ Syntax now valid: {file_path}")
            else:
                log_operation(f"   ⚠️ Still has issues: {file_path} - {new_error}")
    
    return files_fixed, total_fixes

def final_validation():
    """Final validation of all Python files"""
    log_operation("🔍 Final validation of all Python files...")
    
    python_files = find_all_python_files()
    validation_errors = []
    
    for file_path in python_files:
        is_valid, error = validate_python_syntax(file_path)
        if not is_valid:
            validation_errors.append(f"{file_path}: {error}")
    
    if validation_errors:
        log_operation(f"⚠️  {len(validation_errors)} files still have syntax errors:")
        for error in validation_errors[:10]:  # Show first 10
            log_operation(f"     - {error}")
        if len(validation_errors) > 10:
            log_operation(f"     ... and {len(validation_errors) - 10} more errors")
    else:
        log_operation("✅ All Python files have valid syntax!")
    
    return len(validation_errors)

def main():
    """Main function"""
    log_operation("🏛️ ENOCHIAN GOVERNOR GENERATION - SYNTAX ERROR FIXER")
    log_operation("=" * 65)
    
    try:
        files_fixed, total_fixes = fix_all_syntax_errors()
        remaining_errors = final_validation()
        
        log_operation("📋 SYNTAX FIXING SUMMARY:")
        log_operation(f"   Files fixed: {files_fixed}")
        log_operation(f"   Total fixes made: {total_fixes}")
        log_operation(f"   Remaining errors: {remaining_errors}")
        
        if remaining_errors == 0:
            log_operation("🎉 All syntax errors have been fixed!")
        else:
            log_operation("⚠️  Some syntax errors remain - may need manual review")
            
    except Exception as e:
        log_operation(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 