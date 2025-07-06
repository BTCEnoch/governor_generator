#!/usr/bin/env python3
"""
Test script for Universal Unicode Cleaner
Demonstrates cleaning capabilities across different file types.
"""

import os
import json
import tempfile
import shutil
from pathlib import Path
from master_unicode_cleaner import MasterUnicodeCleaner

def create_test_files(test_dir: Path) -> dict:
    """Create test files with Unicode characters for testing."""
    test_files = {}
    
    # Test JSON file
    json_content = {
        "name": "Café Mystique",
        "description": "A magical café with 🧙‍♂️ wizards and ✨ sparkles",
        "price": "€15.50",
        "rating": "\u2605\u2605\u2605\u2605\u2606",
        "quote": "\u201cAmazing experience\u201d",
        "special_chars": "\u03b1 \u03b2 \u03b3 \u03b4 \u03b5 \u2014 \u2013 \u2026 \u00bd \u00be"
    }
    json_file = test_dir / "test.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_content, f, indent=2, ensure_ascii=False)
    test_files['json'] = json_file
    
    # Test Python file
    python_content = '''#!/usr/bin/env python3
"""
Test Python file with Unicode characters
"""

def café_function():
    """Function with Unicode in docstring: ✨"""
    message = "Hello 🌍 World!"
    price = "€25.99"
    rating = "★★★★★"
    return f"Café rating: {rating}, Price: {price}"

# Greek letters in comments: α β γ δ
# Smart quotes: "Hello" and 'World'
# Special dashes: – and —
# Mathematical: ± × ÷ ≈
'''
    python_file = test_dir / "test.py"
    with open(python_file, 'w', encoding='utf-8') as f:
        f.write(python_content)
    test_files['python'] = python_file
    
    # Test Markdown file
    markdown_content = '''# Test Markdown File

This is a test file with Unicode characters:

## Features
- Smart quotes: "Hello" and 'World'
- Emojis: 🎭 🔮 ⚡ 🌟
- Mathematical symbols: ± × ÷ ≈ ∞
- Greek letters: α β γ δ ε
- Currency: €25.99, £19.99, ¥1500
- Accented characters: café, naïve, résumé

## Special Characters
- Em dash: —
- En dash: –
- Ellipsis: …
- Fractions: ½ ¾ ⅓ ⅔

> "This is a blockquote with special characters"
'''
    markdown_file = test_dir / "test.md"
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    test_files['markdown'] = markdown_file
    
    # Test YAML file
    yaml_content = '''---
name: "Café Configuration"
description: "A magical configuration 🧙‍♂️"
settings:
  price: "€15.50"
  rating: "★★★★☆"
  special_chars: "α β γ δ ε — – … ½ ¾"
  quotes: "Smart quotes test"
  emojis: "🎭 🔮 ⚡ 🌟"
'''
    yaml_file = test_dir / "test.yaml"
    with open(yaml_file, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    test_files['yaml'] = yaml_file
    
    # Test CSV file
    csv_content = '''Name,Description,Price,Rating
"Café Mystique","Magical café with 🧙‍♂️ wizards","€15.50","★★★★☆"
"Naïve Restaurant","French cuisine with résumé","£25.99","★★★★★"
"Alpha Café","Greek themed: α β γ δ","¥1500","★★★☆☆"
'''
    csv_file = test_dir / "test.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    test_files['csv'] = csv_file
    
    return test_files

def test_universal_cleaner():
    """Test the universal Unicode cleaner."""
    print("🧪 Testing Universal Unicode Cleaner")
    print("=" * 50)
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir)
        
        # Create test files
        print("📁 Creating test files with Unicode characters...")
        test_files = create_test_files(test_dir)
        
        # Initialize cleaner
        cleaner = MasterUnicodeCleaner(str(test_dir))
        
        # Display files before cleaning
        print(f"\n📋 Created {len(test_files)} test files:")
        for file_type, file_path in test_files.items():
            print(f"  • {file_type}: {file_path.name}")
        
        # Run the cleaner
        print("\n🔧 Running Universal Unicode Cleaner...")
        stats = cleaner.clean_all_text_files(create_backups=True)
        
        # Display results
        print(f"\n📊 Cleaning Results:")
        print(f"  • Files processed: {stats['files_processed']}")
        print(f"  • Files cleaned: {stats['files_cleaned']}")
        print(f"  • Files skipped: {stats['files_skipped']}")
        print(f"  • Unicode characters replaced: {stats['unicode_chars_replaced']:,}")
        print(f"  • Processing time: {stats['processing_time']}")
        
        # Show file type breakdown
        if stats['file_types_processed']:
            print(f"\n📁 File types processed:")
            for file_type, count in stats['file_types_processed'].items():
                print(f"  • {file_type}: {count} files")
        
        # Verify files are still valid
        print(f"\n✅ Verification:")
        
        # Check JSON
        try:
            with open(test_files['json'], 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"  • JSON file: Valid structure ✓")
        except Exception as e:
            print(f"  • JSON file: Invalid structure ✗ ({e})")
        
        # Check Python syntax
        try:
            with open(test_files['python'], 'r', encoding='utf-8') as f:
                python_code = f.read()
            compile(python_code, str(test_files['python']), 'exec')
            print(f"  • Python file: Valid syntax ✓")
        except Exception as e:
            print(f"  • Python file: Invalid syntax ✗ ({e})")
        
        # Show sample cleaned content
        print(f"\n📄 Sample cleaned content (JSON):")
        with open(test_files['json'], 'r', encoding='utf-8') as f:
            sample_content = f.read()
        print(sample_content[:300] + "..." if len(sample_content) > 300 else sample_content)
        
        # Check backup files
        backup_files = list(test_dir.rglob('*_unicode_backup'))
        print(f"\n💾 Backup files created: {len(backup_files)}")
        for backup in backup_files:
            print(f"  • {backup.name}")
        
        print(f"\n🎉 Test completed successfully!")
        
        # Show cleaning effectiveness
        if stats['unicode_chars_replaced'] > 0:
            print(f"✨ Successfully replaced {stats['unicode_chars_replaced']} Unicode characters")
            print(f"📁 All {stats['files_cleaned']} files are now ASCII-safe")
        else:
            print("ℹ️ No Unicode characters found to replace")

if __name__ == "__main__":
    test_universal_cleaner() 