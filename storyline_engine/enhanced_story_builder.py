#!/usr/bin/env python3
"""
Enhanced Story Builder - Adds more story nodes
Expands the basic 3-node structure to 8-12 nodes
"""

from typing import Dict, List

class EnhancedStoryBuilder:
    """Builds enhanced story trees with more nodes"""
    
    def __init__(self):
        pass
    
    def build_enhanced_story_tree(self, info: Dict) -> Dict:
        """Create enhanced story tree with 8-12 nodes"""
        name = info["name"]
        element = info["element"]
        traditions = info["traditions"]
        
        # Base story structure
        story_tree = {
            "start_node": "introduction",
            "nodes": {}
        }
        
        # Add introduction nodes
        story_tree["nodes"].update(self._create_introduction_nodes(name, element))
        
        # Add teaching nodes
        story_tree["nodes"].update(self._create_teaching_nodes(name, traditions))
        
        # Add challenge nodes
        story_tree["nodes"].update(self._create_challenge_nodes(name, element))
        
        # Add ending nodes
        story_tree["nodes"].update(self._create_ending_nodes(name))
        
        return story_tree
    
    def _create_introduction_nodes(self, name: str, element: str) -> Dict:
        """Create introduction sequence nodes"""
        return {
            "introduction": {
                "type": "dialogue",
                "title": f"Approaching {name}",
                "content": f"You sense the {element}al presence of {name}, the mighty governor. Their aura resonates with ancient wisdom.",
                "choices": ["show_respect", "challenge_directly", "observe_silently"],
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
            },
            "observe_silently": {
                "type": "dialogue",
                "title": "Silent Observation",
                "content": f"{name} notices your silent study. 'Patience shows wisdom,' they remark.",
                "choices": ["ask_for_guidance", "continue_watching"],
                "requirements": {"reputation": 0}
            }
        }
    
    def _create_teaching_nodes(self, name: str, traditions: List[str]) -> Dict:
        """Create teaching sequence nodes"""
        tradition_hint = ""
        if "hermetic_tradition" in [t.lower().replace(" ", "_") for t in traditions]:
            tradition_hint = " The hermetic principles resonate in their words."
        
        return {
            "request_teaching": {
                "type": "dialogue",
                "title": "Seeking Knowledge",
                "content": f"{name} considers your request carefully.{tradition_hint}",
                "choices": ["accept_first_lesson", "ask_about_price"],
                "requirements": {"reputation": 0}
            },
            "accept_first_lesson": {
                "type": "challenge",
                "title": "First Lesson",
                "content": f"{name} begins to speak of ancient mysteries. 'Listen carefully,' they warn.",
                "choices": ["focus_intently", "ask_questions"],
                "requirements": {"reputation": 0}
            },
            "ask_about_price": {
                "type": "dialogue",
                "title": "Understanding the Cost",
                "content": f"{name} speaks of sacrifice and dedication required for true knowledge.",
                "choices": ["accept_terms", "negotiate_terms"],
                "requirements": {"reputation": 0}
            }
        }
    
    def _create_challenge_nodes(self, name: str, element: str) -> Dict:
        """Create challenge sequence nodes"""
        challenge_type = self._get_elemental_challenge(element)
        
        return {
            "accept_trial": {
                "type": "challenge",
                "title": f"The {element.title()}al Trial",
                "content": f"{name} presents you with {challenge_type}. Your resolve will be tested.",
                "choices": ["face_challenge", "prepare_more"],
                "requirements": {"reputation": 5}
            },
            "face_challenge": {
                "type": "challenge",
                "title": "Moment of Truth",
                "content": f"You steel yourself and face {name}'s trial with determination.",
                "choices": ["success_path", "failure_path"],
                "requirements": {"reputation": 5}
            }
        }
    
    def _create_ending_nodes(self, name: str) -> Dict:
        """Create ending sequence nodes"""
        return {
            "success_path": {
                "type": "dialogue",
                "title": "Victory",
                "content": f"{name} nods with approval. 'You have proven yourself worthy.'",
                "choices": ["request_boon", "ask_for_wisdom"],
                "requirements": {"reputation": 10}
            },
            "failure_path": {
                "type": "dialogue",
                "title": "Learning from Defeat",
                "content": f"{name} offers guidance despite your failure. 'Learn from this experience.'",
                "choices": ["accept_guidance", "try_again_later"],
                "requirements": {"reputation": 0}
            }
        }
    
    def _get_elemental_challenge(self, element: str) -> str:
        """Get appropriate challenge based on element"""
        challenges = {
            "fire": "a trial of courage and will",
            "water": "a test of intuition and flow",
            "air": "a puzzle of logic and wit",
            "earth": "a demonstration of patience and strength",
            "unknown": "a mysterious test of character"
        }
        return challenges.get(element, challenges["unknown"])

def test_enhanced_builder():
    """Test the enhanced story builder"""
    try:
        builder = EnhancedStoryBuilder()
        
        test_info = {
            "name": "TEST_GOVERNOR",
            "element": "fire",
            "traditions": ["Hermetic Tradition", "Kabbalah"]
        }
        
        story_tree = builder.build_enhanced_story_tree(test_info)
        
        print(f"✅ Enhanced story tree created")
        print(f"   Nodes: {len(story_tree['nodes'])}")
        print(f"   Start: {story_tree['start_node']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_enhanced_builder() 