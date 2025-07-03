#!/usr/bin/env python3
"""
Simple Storyline Generator - Working Version
Combines governor data with basic storyline templates
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

# Set up basic logging
logging.basicConfig(level=logging.WARNING)  # Reduce noise

class SimpleStorylineGenerator:
    """Simple working storyline generator"""
    
    def __init__(self, base_path: Path = Path(".")):
        self.base_path = Path(base_path)
        self.governor_path = self.base_path / "governor_output"
        self.output_path = self.base_path / "storyline_output"
        
        # Create output directory if it doesn't exist
        self.output_path.mkdir(exist_ok=True)
        
        print(f"🏗️ Generator initialized")
        print(f"   Governor path: {self.governor_path}")
        print(f"   Output path: {self.output_path}")
    
    def list_governors(self) -> List[str]:
        """Get list of available governors"""
        if not self.governor_path.exists():
            return []
        
        governor_files = list(self.governor_path.glob("*.json"))
        return [f.stem for f in governor_files]
    
    def load_governor_data(self, governor_name: str) -> Optional[Dict]:
        """Load governor data safely"""
        governor_file = self.governor_path / f"{governor_name}.json"
        
        if not governor_file.exists():
            print(f"❌ Governor file not found: {governor_name}")
            return None
        
        try:
            with open(governor_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"❌ Error loading {governor_name}: {e}")
            return None
    
    def extract_basic_info(self, governor_data: Dict) -> Dict:
        """Extract basic information from governor data"""
        info = {
            "name": governor_data.get("governor_name", "Unknown"),
            "number": governor_data.get("governor_number", 0),
            "traditions": [],
            "element": "unknown",
            "teaching": "balanced"
        }
        
        # Extract traditions
        kb_selections = governor_data.get("knowledge_base_selections", {})
        if isinstance(kb_selections, dict):
            info["traditions"] = kb_selections.get("chosen_traditions", [])
        
        # Extract elemental nature from blocks
        blocks = governor_data.get("blocks", {})
        if isinstance(blocks, dict):
            elemental_block = blocks.get("B_elemental_essence", {})
            if isinstance(elemental_block, dict) and "6" in elemental_block:
                element_text = str(elemental_block["6"]).lower()
                for element in ["fire", "water", "air", "earth"]:
                    if element in element_text:
                        info["element"] = element
                        break
        
        return info
    
    def create_storyline(self, governor_name: str) -> Optional[Dict]:
        """Create storyline for a governor"""
        
        # Load governor data
        gov_data = self.load_governor_data(governor_name)
        if not gov_data:
            return None
        
        # Extract basic info
        info = self.extract_basic_info(gov_data)
        
        # Create storyline structure
        storyline = {
            "governor_id": governor_name,
            "version": "1.0",
            "generator": "simple_hybrid",
            "metadata": {
                "governor_name": info["name"],
                "governor_number": info["number"],
                "primary_element": info["element"],
                "tradition_count": len(info["traditions"]),
                "selected_traditions": info["traditions"]
            },
            "persona": {
                "tone": self._determine_tone(info),
                "traits": self._determine_traits(info),
                "power_level": "formidable_approachable",
                "teaching_style": info["teaching"]
            },
            "voidmaker_integration": {
                "tier_0_25": {"enabled": True, "style": "traditional_only"},
                "tier_26_50": {"enabled": True, "style": "subtle_cosmic_hints"},
                "tier_51_75": {"enabled": True, "style": "direct_concepts"},
                "tier_76_100": {"enabled": True, "style": "full_awareness_unnamed"}
            },
            "story_tree": self._create_basic_story_tree(info),
            "utilities": self._suggest_utilities(info),
            "cross_governor_arcs": []
        }
        
        return storyline
    
    def _determine_tone(self, info: Dict) -> str:
        """Determine tone based on element and traditions"""
        element = info["element"]
        tradition_count = len(info["traditions"])
        
        if element == "fire":
            return "fierce_passionate" if tradition_count >= 3 else "direct_powerful"
        elif element == "water":
            return "flowing_intuitive" if tradition_count >= 3 else "emotional_deep"
        elif element == "air":
            return "intellectual_precise" if tradition_count >= 3 else "quick_analytical"
        elif element == "earth":
            return "grounded_practical" if tradition_count >= 3 else "steady_reliable"
        else:
            return "balanced_authority"
    
    def _determine_traits(self, info: Dict) -> List[str]:
        """Determine traits based on governor info"""
        traits = []
        
        # Add elemental trait
        if info["element"] != "unknown":
            traits.append(f"{info['element']}_elemental")
        
        # Add tradition depth trait
        tradition_count = len(info["traditions"])
        if tradition_count >= 4:
            traits.append("tradition_master")
        elif tradition_count >= 2:
            traits.append("tradition_rich")
        else:
            traits.append("tradition_focused")
        
        # Add wisdom traditions
        traditions = info["traditions"]
        if "Hermetic Tradition" in traditions:
            traits.append("hermetic_wisdom")
        if "Kabbalah" in traditions:
            traits.append("kabbalistic_depth")
          
        return traits[:4]  # Limit to 4 key traits
    
    def _create_basic_story_tree(self, info: Dict) -> Dict:
        """Create basic story tree structure"""
        name = info["name"]
        element = info["element"]
        
        return {
            "start_node": "introduction",
            "nodes": {
                "introduction": {
                    "type": "dialogue",
                    "title": f"Approaching {name}",
                    "content": f"You sense the {element}al presence of {name}, the mighty governor. Their aura resonates with ancient wisdom.",
                    "choices": ["show_respect", "challenge_directly"],
                    "requirements": {"reputation": 0}
                },
                "show_respect": {
                    "type": "dialogue", 
                    "title": "Respectful Greeting",
                    "content": f"{name} acknowledges your respectful approach with a nod of approval.",
                    "choices": ["request_teaching", "ask_about_domain"],
                    "requirements": {"reputation": 0}
                },
                "challenge_directly": {
                    "type": "challenge",
                    "title": "Bold Challenge",
                    "content": f"{name}'s eyes flash with interest at your boldness. 'Prove your worth,' they command.",
                    "choices": ["accept_trial", "withdraw_respectfully"],
                    "requirements": {"reputation": 5}
                }
            }
        }
    
    def _suggest_utilities(self, info: Dict) -> List[str]:
        """Suggest utilities based on governor info"""
        utilities = ["basic_dialogue", "reputation_tracking"]
        
        element = info["element"]
        if element == "fire":
            utilities.append("combat_trial")
        elif element == "water":
            utilities.append("wisdom_puzzle")
        elif element == "air":
            utilities.append("riddle_challenge")
        elif element == "earth":
            utilities.append("patience_test")
        
        return utilities
    
    def save_storyline(self, storyline: Dict, governor_name: str) -> bool:
        """Save storyline to output directory"""
        output_file = self.output_path / f"{governor_name}_storyline.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(storyline, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving storyline for {governor_name}: {e}")
            return False
    
    def generate_single(self, governor_name: str) -> bool:
        """Generate storyline for single governor"""
        print(f"🎭 Generating storyline for {governor_name}...")
        
        storyline = self.create_storyline(governor_name)
        if not storyline:
            print(f"❌ Failed to create storyline for {governor_name}")
            return False
        
        if self.save_storyline(storyline, governor_name):
            print(f"✅ Generated storyline for {governor_name}")
            return True
        else:
            return False
    
    def generate_batch(self, limit: Optional[int] = None) -> Dict[str, int]:
        """Generate storylines for multiple governors"""
        governors = self.list_governors()
        
        if limit:
            governors = governors[:limit]
        
        results = {"success": 0, "failed": 0}
        
        print(f"🚀 Generating storylines for {len(governors)} governors...")
        
        for gov_name in governors:
            if self.generate_single(gov_name):
                results["success"] += 1
            else:
                results["failed"] += 1
        
        print(f"📊 Batch complete: {results['success']} success, {results['failed']} failed")
        return results

def test_simple_generator():
    """Test the simple generator"""
    try:
        print("🧪 Testing Simple Storyline Generator...")
        
        generator = SimpleStorylineGenerator()
        governors = generator.list_governors()
        
        print(f"📊 Found {len(governors)} governors")
        
        if governors:
            # Test with first governor
            test_gov = governors[0]
            success = generator.generate_single(test_gov)
            
            if success:
                print("✅ Single generation test passed")
                
                # Test batch with limit of 3
                results = generator.generate_batch(limit=3)
                if results["success"] > 0:
                    print("✅ Batch generation test passed")
                    return True
            
        print("❌ Tests failed")
        return False
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple_generator() 