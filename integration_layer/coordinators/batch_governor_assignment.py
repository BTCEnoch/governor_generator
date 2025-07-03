import json
import sys
import os
from pathlib import Path

# Add project root to Python path for proper imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Import from mystical systems according to new architecture
from mystical_systems.tarot_system.engines.governor_tarot_assigner import GovernorTarotAssigner
from mystical_systems.tarot_system.schemas.tarot_schemas import GovernorTarotProfile

class BatchGovernorTarotAssignment:
    def __init__(self):
        self.assigner = GovernorTarotAssigner()
        self.governors_path = Path("governor_output")
        # Update path to match new mystical systems architecture
        self.tarot_output_path = Path("mystical_systems/tarot_system/data/governor_tarot_profiles")
        self.tarot_output_path.mkdir(parents=True, exist_ok=True)
    
    def assign_all_governors(self):
        """Process all 91 governors and assign tarot influences"""
        
        print("🔮 STARTING BATCH TAROT ASSIGNMENT FOR 91 GOVERNORS")
        print("=" * 60)
        
        governor_files = list(self.governors_path.glob("*.json"))
        success_count = 0
        
        for governor_file in governor_files:
            try:
                # Load governor data
                with open(governor_file, 'r', encoding='utf-8') as f:
                    governor_data = json.load(f)
                
                # Assign tarot profile
                tarot_profile = self.assigner.assign_tarot_to_governor(governor_data)
                
                # Save tarot profile
                output_file = self.tarot_output_path / f"{governor_file.stem}_tarot.json"
                self._save_tarot_profile(tarot_profile, output_file)
                
                print(f"✅ {governor_file.stem}: {tarot_profile.primary_card.name} (Primary)")
                success_count += 1
                
            except Exception as e:
                print(f"❌ Failed to process {governor_file.stem}: {e}")
        
        print(f"\n🎯 BATCH ASSIGNMENT COMPLETE: {success_count}/{len(governor_files)} governors")
        self._generate_summary_report(success_count, len(governor_files))
    
    def _save_tarot_profile(self, profile: GovernorTarotProfile, output_file: Path):
        """Save tarot profile to JSON"""
        profile_data = {
            "governor_name": profile.governor_name,
            "primary_card": {
                "id": profile.primary_card.id,
                "name": profile.primary_card.name,
                "suit": profile.primary_card.suit.value,
                "meaning": profile.primary_card.upright_meaning
            },
            "secondary_cards": [
                {
                    "id": card.id,
                    "name": card.name, 
                    "suit": card.suit.value,
                    "influence": card.upright_keywords[:3]
                }
                for card in profile.secondary_cards
            ],
            "shadow_card": {
                "id": profile.shadow_card.id,
                "name": profile.shadow_card.name,
                "challenge": profile.shadow_card.reversed_meaning
            },
            "personality_modifiers": profile.personality_modifiers,
            "storyline_themes": profile.storyline_themes,
            "magical_affinities": profile.magical_affinities
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, indent=2, ensure_ascii=False)

    def _generate_summary_report(self, success_count: int, total_count: int):
        """Generate a summary report of the batch assignment"""
        print(f"\n📊 TAROT ASSIGNMENT SUMMARY REPORT")
        print("=" * 50)
        print(f"Total Governors Processed: {total_count}")
        print(f"Successful Assignments: {success_count}")
        print(f"Failed Assignments: {total_count - success_count}")
        print(f"Success Rate: {(success_count/total_count*100):.1f}%")
        
        if success_count > 0:
            print(f"\n✨ Tarot profiles saved to: {self.tarot_output_path}")
            print("🎴 Each governor now has tarot influences for enhanced storylines!")
        else:
            print("\n❌ No successful assignments. Check governor files and tarot database.")
