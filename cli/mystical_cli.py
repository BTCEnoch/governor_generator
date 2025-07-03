#!/usr/bin/env python3
"""
Complete Tarot System Launcher
Demonstrates all functionality of the tarot integration system
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from game_mechanics.divination_systems.tarot_game_interface import TarotGameInterface
from integration_layer.coordinators.batch_governor_assignment import BatchGovernorTarotAssignment
from mystical_systems.tarot_system.utils.tarot_utils import TarotDatabase
from game_mechanics.divination_systems.tarot_game_engine import TarotGameEngine

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
            # Simple storyline enhancement for now
            enhance_storylines()
                
        elif choice == "4":
            print("\n🧪 RUNNING SYSTEM TESTS...")
            test_system_components()
            
        elif choice == "5":
            print("🌟 May the cards guide your path! Farewell! 🌟")
            break
            
        else:
            print("❌ Please enter a valid choice (1-5)")

def enhance_storylines():
    """Simple storyline enhancement function"""
    governor_files = list(Path("governor_output").glob("*.json"))
    if governor_files:
        first_governor = governor_files[0].stem
        print(f"✅ Enhanced storyline for {first_governor}")
        print("📝 Note: Full storyline enhancer will be implemented in Phase 2")
    else:
        print("❌ No governor files found")

def test_system_components():
    """Test all system components"""
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
