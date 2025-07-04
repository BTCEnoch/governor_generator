#!/usr/bin/env python3
"""
Simple test for the questlines system
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.questlines.questline_builder import QuestlineBuilder
from core.questlines.schemas.questline_schemas import QuestlineType, DifficultyLevel

def test_questline_creation():
    """Test basic questline creation"""
    print("🧪 Testing Questlines System")
    print("=" * 50)
    
    # Sample governor data
    governor_data = {
        'name': 'ABRIOND',
        'element': 'Fire',
        'wisdom_domains': ['Sacred Geometry', 'Ancient Wisdom'],
        'personality_traits': {
            'courage': 8,
            'wisdom': 9,
            'mystery': 7
        }
    }
    
    try:
        # Initialize questline builder
        builder = QuestlineBuilder(governor_data)
        print(f"✅ QuestlineBuilder initialized for {governor_data['name']}")
        
        # Create a wisdom trial questline
        questline = builder.create_questline(
            questline_type=QuestlineType.WISDOM_TRIAL,
            difficulty=DifficultyLevel.APPRENTICE,
            custom_theme="Sacred Fire"
        )
        
        print(f"✅ Created questline: '{questline.title}'")
        print(f"   Type: {questline.type.value}")
        print(f"   Difficulty: {questline.difficulty.value}")
        print(f"   Duration: {questline.estimated_duration} minutes")
        print(f"   Element: {questline.elemental_alignment}")
        print(f"   Creator: {questline.creator_governor}")
        print(f"   Themes: {questline.wisdom_themes}")
        print(f"   Tags: {questline.tags}")
        print(f"   Description: {questline.description}")
        
        # Test different questline types
        print("\n🔍 Testing different questline types:")
        
        questline_types = [
            QuestlineType.ELEMENTAL_JOURNEY,
            QuestlineType.MYSTERY_INVESTIGATION,
            QuestlineType.ARTIFACT_QUEST
        ]
        
        for qtype in questline_types:
            test_questline = builder.create_questline(
                questline_type=qtype,
                difficulty=DifficultyLevel.NOVICE
            )
            print(f"   ✅ {qtype.value}: '{test_questline.title}'")
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_schema_validation():
    """Test schema validation"""
    print("\n🧪 Testing Schema Validation")
    print("=" * 50)
    
    try:
        from core.questlines.schemas.questline_schemas import (
            Questline, QuestlineType, DifficultyLevel
        )
        
        # Test creating a basic questline
        questline = Questline(
            id="test-001",
            creator_governor="TEST_GOVERNOR",
            title="Test Questline",
            description="A test questline for validation",
            type=QuestlineType.WISDOM_TRIAL,
            difficulty=DifficultyLevel.NOVICE,
            estimated_duration=30
        )
        
        print(f"✅ Basic questline created: {questline.title}")
        print(f"   ID: {questline.id}")
        print(f"   Created at: {questline.created_at}")
        
        # Test auto-generated ID
        questline_auto = Questline(
            id="",  # Empty ID should auto-generate
            creator_governor="AUTO_GOVERNOR",
            title="Auto ID Test",
            description="Testing auto-generated ID",
            type=QuestlineType.KNOWLEDGE_SEEKING,
            difficulty=DifficultyLevel.ADEPT,
            estimated_duration=45
        )
        
        print(f"✅ Auto-generated ID: {questline_auto.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Questlines System Tests")
    print("=" * 60)
    
    # Run tests
    test1_result = test_schema_validation()
    test2_result = test_questline_creation()
    
    print("\n📊 Test Results:")
    print(f"   Schema Validation: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"   Questline Creation: {'✅ PASS' if test2_result else '❌ FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 All tests passed! Questlines system is functional.")
    else:
        print("\n❌ Some tests failed. Check the output above.")
        sys.exit(1) 