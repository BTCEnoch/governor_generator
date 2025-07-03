#!/usr/bin/env python3
"""
Test script to verify the tarot system components work together
"""

import sys
from pathlib import Path

# Add the current directory to the path so imports work
sys.path.insert(0, str(Path(__file__).parent))

def test_tarot_database():
    """Test the tarot database loads correctly"""
    print("🧪 Testing Tarot Database...")
    
    try:
        from utils.tarot_utils import TarotDatabase
        
        db = TarotDatabase()
        print(f"✅ Loaded {len(db.cards_by_id)} tarot cards")
        
        # Test getting a specific card
        fool_card = db.get_card_by_id("fool")
        if fool_card:
            print(f"✅ Found card: {fool_card.name}")
        else:
            print("❌ Could not find The Fool card")
            
        # Test getting major arcana
        major_arcana = db.get_major_arcana()
        print(f"✅ Found {len(major_arcana)} Major Arcana cards")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_game_engine():
    """Test the game engine"""
    print("\n🧪 Testing Game Engine...")
    
    try:
        from game.tarot_game_engine import TarotGameEngine
        
        engine = TarotGameEngine()
        print("✅ Game engine initialized")
        
        # Test three-card reading
        reading = engine.create_three_card_reading("Test question")
        print(f"✅ Generated three-card reading with {len(reading.cards_drawn)} cards")
        print(f"   Themes: {reading.themes[:3]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Game engine test failed: {e}")
        return False

def test_governor_assigner():
    """Test the governor tarot assigner"""
    print("\n🧪 Testing Governor Assigner...")
    
    try:
        from assignment.governor_tarot_assigner import GovernorTarotAssigner
        
        assigner = GovernorTarotAssigner()
        print("✅ Assigner initialized")
        
        # Test with sample governor data
        sample_governor = {
            "name": "Test Governor",
            "wisdom_tradition": "hermetic_tradition",
            "personality_traits": ["leadership", "creativity"],
            "magical_focus": "manifestation"
        }
        
        profile = assigner.assign_tarot_to_governor(sample_governor)
        print(f"✅ Assigned tarot profile to {profile.governor_name}")
        print(f"   Primary card: {profile.primary_card.name}")
        print(f"   Secondary cards: {[card.name for card in profile.secondary_cards]}")
        print(f"   Shadow card: {profile.shadow_card.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Governor assigner test failed: {e}")
        return False

def test_schemas():
    """Test the schema imports"""
    print("\n🧪 Testing Schemas...")
    
    try:
        from schemas.tarot_schemas import TarotCard, TarotSuit, CardPosition, GovernorTarotProfile, TarotReading
        print("✅ All schemas imported successfully")
        
        # Test creating a simple card
        test_card = TarotCard(
            id="test_card",
            name="Test Card",
            suit=TarotSuit.WANDS,
            number=1,
            wikipedia_url="https://test.com",
            upright_keywords=["test"],
            reversed_keywords=["reversed test"],
            upright_meaning="Test meaning",
            reversed_meaning="Reversed test meaning"
        )
        print(f"✅ Created test card: {test_card.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔮✨ TAROT SYSTEM COMPONENT TESTS ✨🔮")
    print("=" * 50)
    
    tests = [
        test_schemas,
        test_tarot_database,
        test_game_engine,
        test_governor_assigner
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The tarot system is ready to use.")
        print("\nTo run the full system:")
        print("  python launch_tarot_system.py")
    else:
        print("❌ Some tests failed. Check the error messages above.")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 