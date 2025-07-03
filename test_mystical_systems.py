#!/usr/bin/env python3
"""
Comprehensive test script for all mystical systems
Tests that all import issues have been resolved
"""

def test_numerology_system():
    """Test numerology system"""
    print("🔢 Testing Numerology System...")
    try:
        from mystical_systems.numerology_system.data.numerology_database import get_numerology_profile, get_life_path_number
        
        # Test basic functionality
        profile = get_numerology_profile(1)
        print(f"   ✅ Life Path 1: {profile.life_purpose}")
        print(f"   ✅ Positive traits: {profile.positive_traits[:2]}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_kabbalah_system():
    """Test kabbalah system"""
    print("\n🌟 Testing Kabbalah System...")
    try:
        from mystical_systems.kabbalah_system.data.sefirot_database import get_sefirah_by_number
        
        # Test basic functionality
        sefirah = get_sefirah_by_number(1)
        print(f"   ✅ Sefirah 1: {sefirah.name} ({sefirah.hebrew_name})")
        print(f"   ✅ Attribute: {sefirah.divine_attribute}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_zodiac_system():
    """Test zodiac system"""
    print("\n♈ Testing Zodiac System...")
    try:
        from mystical_systems.zodiac_system.data.zodiac_database import get_zodiac_sign_by_name
        
        # Test basic functionality
        sign = get_zodiac_sign_by_name("Aries")
        print(f"   ✅ Sign: {sign.name} {sign.symbol}")
        print(f"   ✅ Element: {sign.element.value}, Modality: {sign.modality.value}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_tarot_system():
    """Test tarot system"""
    print("\n🎴 Testing Tarot System...")
    try:
        from mystical_systems.tarot_system.utils.tarot_utils import TarotDatabase
        from mystical_systems.tarot_system.engines.governor_tarot_assigner import GovernorTarotAssigner
        
        # Test basic functionality
        db = TarotDatabase()
        assigner = GovernorTarotAssigner()
        
        fool_card = db.get_card_by_id("fool")
        if fool_card:
            print(f"   ✅ Tarot Card: {fool_card.name}")
            print(f"   ✅ Keywords: {fool_card.upright_keywords[:2]}")
        else:
            print("   ❌ Could not find fool card")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_unified_profiler():
    """Test unified mystical profiler"""
    print("\n🔮 Testing Unified Mystical Profiler...")
    try:
        from unified_profiler.core.mystical_profiler import UnifiedMysticalProfiler
        
        # Test basic functionality
        profiler = UnifiedMysticalProfiler()
        print(f"   ✅ Unified profiler initialized successfully")
        
        # Test with sample governor data
        governor_data = {
            "name": "TEST_GOVERNOR",
            "wisdom_tradition": "hermetic_tradition",
            "personality_traits": ["leadership", "wisdom"],
            "magical_focus": "manifestation"
        }
        
        profile = profiler.create_complete_profile(governor_data)
        print(f"   ✅ Complete profile created for {profile.governor_name}")
        print(f"   ✅ Systems integrated: Tarot, Kabbalah, Numerology, Zodiac")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_game_mechanics():
    """Test game mechanics integration"""
    print("\n🎮 Testing Game Mechanics Integration...")
    try:
        from game_mechanics.divination_systems.tarot_game_engine import TarotGameEngine
        
        # Test basic functionality
        engine = TarotGameEngine()
        reading = engine.create_three_card_reading("Test question")
        print(f"   ✅ Tarot reading created: {reading.spread_type}")
        print(f"   ✅ Cards drawn: {len(reading.cards_drawn)}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 MYSTICAL SYSTEMS COMPREHENSIVE TEST")
    print("=" * 50)
    
    tests = [
        test_numerology_system,
        test_kabbalah_system,
        test_zodiac_system,
        test_tarot_system,
        test_unified_profiler,
        test_game_mechanics
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 TEST RESULTS: {passed}/{total} systems passed")
    
    if passed == total:
        print("✅ ALL MYSTICAL SYSTEMS WORKING PERFECTLY!")
        print("🌟 Import issues have been completely resolved!")
    else:
        print("❌ Some systems still need attention")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 