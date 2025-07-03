#!/usr/bin/env python3
"""
Complete Tarot System Launcher
Demonstrates all functionality of the tarot integration system
"""

import sys
from pathlib import Path

# Add tarot_system to path
sys.path.append(str(Path(__file__).parent))

from game.tarot_game_interface import TarotGameInterface
from assignment.batch_governor_assignment import BatchGovernorTarotAssignment
from integration.storyline_enhancer import GovernorStorylineEnhancer

def main():
    print("🔮✨ GOVERNOR GENERATION TAROT SYSTEM ✨🔮")
    print("=" * 50)
    print("1. 🎯 Assign Tarot to All 91 Governors")
    print("2. 🎴 Play Interactive Tarot Game")
    print("3. 📚 Generate Enhanced Storylines")
    print("4. 🧪 Test System Components")
    print("5. 🚪 Exit")
    
    while True:
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            print("\n🎯 STARTING BATCH TAROT ASSIGNMENT...")
            assigner = BatchGovernorTarotAssignment()
            assigner.assign_all_governors()
            
        elif choice == "2":
            print("\n🎴 LAUNCHING INTERACTIVE TAROT GAME...")
            game = TarotGameInterface()
            game.start_game_session()
            
        elif choice == "3":
            print("\n📚 GENERATING ENHANCED STORYLINES...")
            enhancer = GovernorStorylineEnhancer()
            # Example with first governor
            governor_files = list(Path("governor_output").glob("*.json"))
            if governor_files:
                first_governor = governor_files[0].stem
                enhanced = enhancer.enhance_governor_storyline(first_governor)
                print(f"✅ Enhanced storyline for {first_governor}")
            else:
                print("❌ No governor files found")
                
        elif choice == "4":
            print("\n🧪 RUNNING SYSTEM TESTS...")
            test_system_components()
            
        elif choice == "5":
            print("🌟 May the cards guide your path! Farewell! 🌟")
            break
            
        else:
            print("❌ Please enter a valid choice (1-5)")

def test_system_components():
    """Test all system components"""
    from utils.tarot_utils import TarotDatabase
    from game.tarot_game_engine import TarotGameEngine
    
    print("Testing Tarot Database...")
    db = TarotDatabase()
    print(f"✅ Loaded {len(db.cards_by_id)} tarot cards")
    
    print("Testing Game Engine...")
    engine = TarotGameEngine()
    reading = engine.create_three_card_reading("Test question")
    print(f"✅ Generated reading with {len(reading.cards_drawn)} cards")
    
    print("✅ All system components working!")

if __name__ == "__main__":
    main()
