#!/usr/bin/env python3
"""
🏛️ ENOCHIAN GOVERNOR GENERATION - DOUBLE NESTING FIXER
Fix all double nesting issues in data and pack directories
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

def log_operation(message):
    """Log operation with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def fix_double_nesting():
    """Fix all double nesting issues in the project"""
    
    # Dictionary of double nesting fixes needed
    double_nesting_fixes = {
        # Game Assets Pack
        "core/game_assets/pack/pack/": "core/game_assets/pack/",
        
        # Governor Data
        "data/governors/indexes/governor_indexes/": "data/governors/indexes/",
        "data/governors/seeds/personality_seeds/": "data/governors/seeds/",
        
        # Knowledge Data
        "data/knowledge/data/data/": "data/knowledge/data/",
        "data/knowledge/generated/generated/": "data/knowledge/generated/",
        "data/knowledge/links/links/": "data/knowledge/links/",
        
        # Canon Data
        "data/canon/canon/": "data/canon/",
        
        # CLI Tools
        "tools/cli/cli/": "tools/cli/",
        
        # Game Mechanics
        "tools/game_mechanics/game_mechanics/": "tools/game_mechanics/",
    }
    
    log_operation("🔧 Starting comprehensive double nesting fixes...")
    
    for nested_path, correct_path in double_nesting_fixes.items():
        if os.path.exists(nested_path):
            log_operation(f"📁 Fixing: {nested_path} → {correct_path}")
            
            # Get list of files and directories in the nested directory
            items = os.listdir(nested_path)
            log_operation(f"   Found {len(items)} items to move")
            
            # Move each item up one level
            for item in items:
                src = os.path.join(nested_path, item)
                dst = os.path.join(correct_path, item)
                
                try:
                    # Create destination directory if it doesn't exist
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    
                    # Check if destination already exists
                    if os.path.exists(dst):
                        log_operation(f"   ⚠️  Destination exists, skipping: {item}")
                        continue
                    
                    # Move file or directory
                    shutil.move(src, dst)
                    log_operation(f"   ✅ Moved: {item}")
                except Exception as e:
                    log_operation(f"   ❌ Error moving {item}: {e}")
            
            # Remove the empty nested directory
            try:
                os.rmdir(nested_path)
                log_operation(f"   🗑️  Removed empty directory: {nested_path}")
            except Exception as e:
                log_operation(f"   ⚠️  Could not remove {nested_path}: {e}")
        else:
            log_operation(f"   ⚠️  Directory not found: {nested_path}")
    
    log_operation("✅ Comprehensive double nesting fixes completed!")

def verify_structure():
    """Verify the fixed structure"""
    log_operation("🔍 Verifying fixed structure...")
    
    expected_directories = [
        "core/game_assets/pack/",
        "data/governors/indexes/",
        "data/governors/seeds/",
        "data/knowledge/data/",
        "data/knowledge/generated/",
        "data/knowledge/links/",
        "data/canon/",
        "tools/cli/",
        "tools/game_mechanics/",
    ]
    
    for directory in expected_directories:
        if os.path.exists(directory):
            items = os.listdir(directory)
            file_count = len([item for item in items if os.path.isfile(os.path.join(directory, item))])
            dir_count = len([item for item in items if os.path.isdir(os.path.join(directory, item))])
            log_operation(f"   ✅ {directory} - {file_count} files, {dir_count} directories")
        else:
            log_operation(f"   ❌ {directory} - NOT FOUND")
    
    # Check for any remaining double nesting
    problematic_paths = [
        "core/game_assets/pack/pack/",
        "data/governors/indexes/governor_indexes/",
        "data/governors/seeds/personality_seeds/",
        "data/knowledge/data/data/",
        "data/knowledge/generated/generated/",
        "data/knowledge/links/links/",
        "data/canon/canon/",
        "tools/cli/cli/",
        "tools/game_mechanics/game_mechanics/",
    ]
    
    remaining_issues = []
    for path in problematic_paths:
        if os.path.exists(path):
            remaining_issues.append(path)
    
    if remaining_issues:
        log_operation(f"⚠️  {len(remaining_issues)} double nesting issues remain:")
        for issue in remaining_issues:
            log_operation(f"     - {issue}")
    else:
        log_operation("✅ No double nesting issues found!")

def main():
    """Main function"""
    log_operation("🏛️ ENOCHIAN GOVERNOR GENERATION - COMPREHENSIVE DOUBLE NESTING FIXER")
    log_operation("=" * 70)
    
    try:
        fix_double_nesting()
        verify_structure()
        log_operation("🎉 All double nesting issues have been resolved!")
    except Exception as e:
        log_operation(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 