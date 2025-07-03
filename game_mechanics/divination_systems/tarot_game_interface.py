from game_mechanics.divination_systems.tarot_game_engine import TarotGameEngine
from mystical_systems.tarot_system.schemas.tarot_schemas import TarotReading

class TarotGameInterface:
    def __init__(self):
        self.engine = TarotGameEngine()
        self.reading_history = []
    
    def start_game_session(self):
        """Start interactive tarot game session"""
        print("🔮✨ WELCOME TO THE MYSTICAL TAROT ORACLE ✨🔮")
        print("=" * 50)
        print("The cards are ready to reveal the mysteries of your path...")
        print()
        
        while True:
            self._show_main_menu()
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                self._three_card_reading_session()
            elif choice == "2":
                self._celtic_cross_reading_session()
            elif choice == "3":
                self._show_reading_history()
            elif choice == "4":
                print("🌟 May the wisdom of the cards guide your journey. Farewell! 🌟")
                break
            else:
                print("❌ Please enter a valid choice (1-4)")
    
    def _show_main_menu(self):
        """Display main game menu"""
        print("\n🎴 TAROT ORACLE MENU 🎴")
        print("1. 🌟 Three-Card Reading (Past, Present, Future)")
        print("2. ⭐ Celtic Cross Reading (Complete 10-card spread)")
        print("3. 📚 View Reading History")
        print("4. 🚪 Exit Oracle")
        print()
    
    def _three_card_reading_session(self):
        """Conduct three-card reading session"""
        print("\n🌟 THREE-CARD READING SESSION 🌟")
        print("This reading reveals your Past, Present, and Future.")
        print()
        
        question = input("💭 Ask a question or press Enter for general reading: ").strip()
        print("\n🔮 Shuffling the cosmic deck...")
        print("✨ Drawing your cards...")
        
        question_to_pass = question if question else None
        reading = self.engine.create_three_card_reading(question_to_pass)
        self._display_reading(reading)
        self.reading_history.append(reading)
        
        input("\nPress Enter to return to main menu...")
    
    def _celtic_cross_reading_session(self):
        """Conduct Celtic Cross reading session"""
        print("\n⭐ CELTIC CROSS READING SESSION ⭐")
        print("This is the most comprehensive 10-card reading.")
        print()
        
        question = input("💭 Ask a question or press Enter for general reading: ").strip()
        print("\n🔮 Shuffling the cosmic deck...")
        print("✨ Drawing your 10 sacred cards...")
        
        question_to_pass = question if question else None
        reading = self.engine.create_celtic_cross_reading(question_to_pass)
        self._display_reading(reading)
        self.reading_history.append(reading)
        
        input("\nPress Enter to return to main menu...")
    
    def _display_reading(self, reading: TarotReading):
        """Display a tarot reading beautifully"""
        print("\n" + "="*60)
        print(reading.interpretation)
        print("\n🎯 KEY THEMES:")
        for theme in reading.themes:
            print(f"   • {theme}")
        
        print(f"\n💡 ORACLE'S ADVICE:\n{reading.advice}")
        print("="*60)
    
    def _show_reading_history(self):
        """Show previous readings"""
        if not self.reading_history:
            print("\n📚 No readings in history yet.")
            return
        
        print(f"\n📚 READING HISTORY ({len(self.reading_history)} readings)")
        print("-" * 40)
        
        for i, reading in enumerate(self.reading_history, 1):
            cards_summary = ", ".join([f"{card.name} ({pos.value})" for card, pos in reading.cards_drawn[:3]])
            print(f"{i}. {reading.spread_type.title()} - {reading.timestamp[:10]}")
            print(f"   Cards: {cards_summary}")
            print(f"   Themes: {', '.join(reading.themes[:2])}")
            print()
