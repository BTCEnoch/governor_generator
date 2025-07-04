#!/usr/bin/env python3
"""
Example usage of the unicode_cleaner utility module.

This script demonstrates various ways to use the unicode_cleaner functions
to clean Unicode characters from JSON data.
"""

import json
from unicode_cleaner import (
    clean_json_data, 
    clean_text, 
    clean_json_file, 
    clean_json_string,
    validate_json_safety,
    get_unicode_characters,
    add_custom_replacement
)


def example_clean_text():
    """Example of cleaning individual text strings."""
    print("=== Cleaning Individual Text Strings ===")
    
    # Sample text with Unicode characters
    sample_text = "🧙‍♂️ Mystical text with • bullets and — dashes"
    print(f"Original: {sample_text}")
    
    cleaned = clean_text(sample_text)
    print(f"Cleaned:  {cleaned}")
    print()


def example_clean_json_data():
    """Example of cleaning JSON data objects."""
    print("=== Cleaning JSON Data Objects ===")
    
    # Sample JSON data with Unicode characters
    sample_data = {
        "title": "🧙‍♂️ Mystical Guide",
        "description": "A guide with • bullet points and — dashes",
        "tags": ["mystical", "•", "🎭"],
        "metadata": {
            "author": "Author Name",
            "symbols": ["•", "—", "…"]
        }
    }
    
    print("Original JSON data:")
    print(json.dumps(sample_data, indent=2))
    print()
    
    cleaned_data = clean_json_data(sample_data)
    print("Cleaned JSON data:")
    print(json.dumps(cleaned_data, indent=2))
    print()


def example_clean_json_string():
    """Example of cleaning JSON strings."""
    print("=== Cleaning JSON Strings ===")
    
    json_string = '''
    {
        "message": "🧙‍♂️ Hello world with • bullets",
        "items": ["item1", "•", "item2"]
    }
    '''
    
    print("Original JSON string:")
    print(json_string)
    print()
    
    cleaned_string = clean_json_string(json_string)
    print("Cleaned JSON string:")
    print(cleaned_string)
    print()


def example_validate_json_safety():
    """Example of validating JSON safety."""
    print("=== Validating JSON Safety ===")
    
    # Safe JSON data
    safe_data = {
        "title": "Safe Title",
        "description": "Safe description with no Unicode"
    }
    
    # Unsafe JSON data
    unsafe_data = {
        "title": "🧙‍♂️ Unsafe Title",
        "description": "Description with • bullets and — dashes"
    }
    
    # Validate safe data
    safe_result = validate_json_safety(safe_data)
    print("Safe data validation:")
    print(f"  Is safe: {safe_result['is_safe']}")
    print(f"  Total issues: {safe_result['total_issues']}")
    print()
    
    # Validate unsafe data
    unsafe_result = validate_json_safety(unsafe_data)
    print("Unsafe data validation:")
    print(f"  Is safe: {unsafe_result['is_safe']}")
    print(f"  Total issues: {unsafe_result['total_issues']}")
    if unsafe_result['issues']:
        print("  Issues found:")
        for issue in unsafe_result['issues']:
            print(f"    - Path: {issue['path']}")
            print(f"      Unicode chars: {issue['unicode_chars']}")
            print(f"      Sample: {issue['sample_text']}")
    print()


def example_custom_replacements():
    """Example of adding custom Unicode replacements."""
    print("=== Custom Unicode Replacements ===")
    
    # Add a custom replacement
    add_custom_replacement('🌟', '[STAR]')
    add_custom_replacement('🔥', '[FIRE]')
    
    sample_text = "🌟 Star and 🔥 fire symbols"
    print(f"Original: {sample_text}")
    
    cleaned = clean_text(sample_text)
    print(f"Cleaned:  {cleaned}")
    print()


def example_find_unicode_characters():
    """Example of finding Unicode characters in text."""
    print("=== Finding Unicode Characters ===")
    
    sample_text = "🧙‍♂️ Text with • bullets, — dashes, and 🎭 symbols"
    unicode_chars = get_unicode_characters(sample_text)
    
    print(f"Text: {sample_text}")
    print(f"Unicode characters found: {unicode_chars}")
    print(f"Character codes: {[ord(char) for char in unicode_chars]}")
    print()


def main():
    """Run all examples."""
    print("Unicode Cleaner Utility Examples")
    print("=" * 50)
    print()
    
    example_clean_text()
    example_clean_json_data()
    example_clean_json_string()
    example_validate_json_safety()
    example_custom_replacements()
    example_find_unicode_characters()
    
    print("All examples completed!")


if __name__ == "__main__":
    main() 