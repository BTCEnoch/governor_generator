#!/usr/bin/env python3
"""
Simple Storyline Template Generator
Creates basic JSON structure for governor storylines
"""

import json
from typing import Dict, List

class BasicStorylineTemplate:
    """Creates basic storyline templates"""
    
    def __init__(self):
        pass
    
    def create_template(self, governor_name: str) -> Dict:
        """Create basic storyline template"""
        
        template = {
            "governor_id": governor_name,
            "version": "1.0",
            "persona": {
                "tone": "balanced_authority",
                "traits": ["elemental", "tradition_focused"],
                "power_level": "formidable_approachable",
                "teaching_style": "balanced_testing"
            },
            "story_tree": {
                "nodes": {},
                "start_node": "introduction"
            },
            "voidmaker_integration": {
                "tier_0_25": {"enabled": True, "style": "traditional_only"},
                "tier_26_50": {"enabled": True, "style": "subtle_hints"},
                "tier_51_75": {"enabled": True, "style": "direct_concepts"},
                "tier_76_100": {"enabled": True, "style": "full_awareness"}
            },
            "utilities": [],
            "cross_governor_arcs": []
        }
        
        # Add basic story nodes
        template["story_tree"]["nodes"] = {
            "introduction": {
                "type": "dialogue",
                "title": f"Meeting {governor_name}",
                "content": f"You approach the mighty governor {governor_name}...",
                "choices": ["begin_teaching", "ask_about_power"],
                "requirements": {"reputation": 0}
            },
            "begin_teaching": {
                "type": "challenge",
                "title": "First Teaching",
                "content": "The governor presents their first lesson...",
                "choices": ["accept_challenge", "decline_respectfully"],
                "requirements": {"reputation": 0}
            },
            "ask_about_power": {
                "type": "dialogue",
                "title": "Understanding Power",
                "content": "The governor speaks of the nature of true power...",
                "choices": ["listen_carefully", "challenge_wisdom"],
                "requirements": {"reputation": 0}
            }
        }
        
        return template
    
    def save_template(self, template: Dict, output_path: str) -> bool:
        """Save template to JSON file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving template: {e}")
            return False

def test_template_generator():
    """Simple test"""
    try:
        generator = BasicStorylineTemplate()
        template = generator.create_template("TEST_GOVERNOR")
        
        print("✅ Created basic template")
        print(f"   Nodes: {len(template['story_tree']['nodes'])}")
        print(f"   Voidmaker tiers: {len(template['voidmaker_integration'])}")
        
        # Test saving
        if generator.save_template(template, "test_storyline.json"):
            print("✅ Template saved successfully")
            
            # Clean up
            import os
            os.remove("test_storyline.json")
            print("✅ Test file cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_template_generator() 