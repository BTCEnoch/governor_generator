#!/usr/bin/env python3
"""
Test Individual Mystical Systems
Quick verification that all databases work correctly
"""

import sys
from pathlib import Path

# Add the current directory to the path so imports work
sys.path.insert(0, str(Path(__file__).parent))

def test_sefirot_database():
    """Test the Sefirot database"""
    print("🧪 Testing Sefirot Database...")
    
    try:
        from data.sefirot_database import ALL_SEFIROT, get_sefirah_by_position, get_sefirah_by_number
        from schemas.mystical_schemas import SefirotPosition
        
        print(f"✅ Loaded {len(ALL_SEFIROT)} Sefirot")
        
        # Test getting specific Sefirot
        keter = get_sefirah_by_position(SefirotPosition.KETER)
        print(f"✅ Found Keter: {keter.name} ({keter.hebrew_name})")
        
        malkhut = get_sefirah_by_number(10)
        print(f"✅ Found Sefirah #10: {malkhut.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Sefirot test failed: {e}")
        return False

def test_numerology_database():
    """Test the numerology database"""
    print("\n🧪 Testing Numerology Database...")
    
    try:
        from data.numerology_database import LIFE_PATH_NUMBERS, get_numerology_profile, calculate_name_numerology
        
        print(f"✅ Loaded {len(LIFE_PATH_NUMBERS)} Life Path Numbers")
        
        # Test getting specific numbers
        life_path_1 = get_numerology_profile(1)
        print(f"✅ Life Path 1: {life_path_1.positive_traits[0]} leader")
        
        # Test name calculation
        test_name_number = calculate_name_numerology("TEST")
        print(f"✅ Name numerology calculation works: TEST = {test_name_number}")
        
        return True
        
    except Exception as e:
        print(f"❌ Numerology test failed: {e}")
        return False

def test_zodiac_database():
    """Test the zodiac database"""
    print("\n🧪 Testing Zodiac Database...")
    
    try:
        from data.zodiac_database import ALL_ZODIAC_SIGNS, get_zodiac_sign_by_name, get_zodiac_signs_by_element
        from schemas.mystical_schemas import ZodiacElement
        
        print(f"✅ Loaded {len(ALL_ZODIAC_SIGNS)} Zodiac Signs")
        
        # Test getting specific signs
        aries = get_zodiac_sign_by_name("Aries")
        print(f"✅ Found Aries: {aries.symbol} ({aries.dates})")
        
        # Test element grouping
        fire_signs = get_zodiac_signs_by_element(ZodiacElement.FIRE)
        print(f"✅ Found {len(fire_signs)} Fire signs: {[s.name for s in fire_signs]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Zodiac test failed: {e}")
        return False

def test_schema_imports():
    """Test all schema imports work"""
    print("\n🧪 Testing Schema Imports...")
    
    try:
        from schemas.mystical_schemas import (
            Sefirah, SefirotPosition, NumerologyProfile, NumerologySystem,
            ZodiacSign, ZodiacElement, ZodiacModality, CompleteMysticalProfile
        )
        print("✅ All mystical schemas imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema import test failed: {e}")
        return False

def main():
    """Run all individual system tests"""
    print("🔮✨ MYSTICAL SYSTEMS INDIVIDUAL TESTS ✨🔮")
    print("=" * 50)
    
    tests = [
        test_schema_imports,
        test_sefirot_database,
        test_numerology_database,
        test_zodiac_database
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 INDIVIDUAL TESTS: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 ALL INDIVIDUAL SYSTEMS WORKING!")
        print("✅ Ready to create unified mystical profiler")
    else:
        print("❌ Some systems failed. Fix errors before proceeding.")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 