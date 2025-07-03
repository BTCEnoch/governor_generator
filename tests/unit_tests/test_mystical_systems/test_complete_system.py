#!/usr/bin/env python3
"""
Test Complete Unified Mystical System
Quick verification that the full system works
"""

import sys
from pathlib import Path

# Add the current directory to the path so imports work
sys.path.insert(0, str(Path(__file__).parent))

def test_complete_system():
    """Test the complete unified mystical profiler"""
    print("🔮✨ COMPLETE MYSTICAL SYSTEM TEST ✨🔮")
    print("=" * 50)
    
    try:
        from assignment.mystical_profiler import UnifiedMysticalProfiler
        
        # Create profiler
        profiler = UnifiedMysticalProfiler()
        print("✅ Unified Mystical Profiler created")
        
        # Test with sample governor data
        sample_governor = {
            'name': 'TESTIARCH',
            'wisdom_tradition': 'hermetic_tradition',
            'domains': ['TRANSFORMATION', 'KNOWLEDGE'],
            'traits': ['scholarly', 'transformative', 'wise'],
            'flaws': ['perfectionist', 'aloof']
        }
        
        # Create complete profile
        complete_profile = profiler.create_complete_profile(sample_governor)
        print("✅ Complete mystical profile created")
        
        # Display results
        print(f"\n🎯 PROFILE FOR: {complete_profile.governor_name}")
        print(f"🎴 TAROT: {complete_profile.tarot_profile.primary_card.name}")
        print(f"🌳 SEFIROT: {complete_profile.sefirot_influences[0].name}")
        print(f"🔢 NUMEROLOGY: Life Path {complete_profile.numerology_profile.life_path_number}")
        print(f"⭐ ZODIAC: {complete_profile.zodiac_sign.name} ({complete_profile.zodiac_sign.element.value})")
        
        print(f"\n📊 UNIFIED THEMES: {len(complete_profile.unified_storyline_themes)} themes")
        for theme in complete_profile.unified_storyline_themes[:5]:
            print(f"  • {theme}")
        
        print(f"\n⚖️ ELEMENTAL BALANCE:")
        for element, value in complete_profile.elemental_balance.items():
            if value > 0:
                print(f"  • {element.title()}: {value:.1f}")
        
        print(f"\n🪐 PLANETARY INFLUENCES: {', '.join(complete_profile.planetary_influences)}")
        
        print(f"\n🎭 ARCHETYPAL THEMES:")
        for archetype in complete_profile.archetypal_themes:
            print(f"  • {archetype}")
        
        print("\n" + "=" * 50)
        print("🎉 COMPLETE UNIFIED SYSTEM WORKING!")
        print("✅ All mystical systems integrated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Complete system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_system()
    sys.exit(0 if success else 1) 