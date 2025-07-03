#!/usr/bin/env python3
"""
Enhanced Generator V2 - Combines improvements
Uses enhanced story builder and element detector with working generator
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add current directory for imports
sys.path.append(str(Path(__file__).parent))

from enhanced_story_builder import EnhancedStoryBuilder
from enhanced_element_detector import EnhancedElementDetector

class EnhancedGeneratorV2:
    """Enhanced storyline generator with improved features"""
    
    def __init__(self, base_path: Path = Path(".")):
        self.base_path = Path(base_path)
        self.governor_path = self.base_path / "governor_output"
        self.output_path = self.base_path / "storyline_output_v2"
        
        # Create output directory
        self.output_path.mkdir(exist_ok=True)
        
        # Initialize enhanced components
        self.story_builder = EnhancedStoryBuilder()
        self.element_detector = EnhancedElementDetector()
        
        print(f"🏗️ Enhanced Generator V2 initialized")
        print(f"   Output: {self.output_path}")
    
    def load_governor_data(self, governor_name: str) -> Optional[Dict]:
        """Load governor data safely"""
        governor_file = self.governor_path / f"{governor_name}.json"
        
        if not governor_file.exists():
            return None
        
        try:
            with open(governor_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    def extract_enhanced_info(self, governor_data: Dict) -> Dict:
        """Extract enhanced information using new detectors and profile data"""
        info = {
            "name": governor_data.get("governor_name", "Unknown"),
            "number": governor_data.get("governor_number", 0),
            "traditions": [],
            "element": "unknown",
            "element_confidence": 0.0,
            "teaching": "balanced",
            "profile_element": None,
            "aethyr": None,
            "tarot": None,
            "voidmaker_themes": [],
            "voidmaker_question_count": 0
        }
        
        # Extract traditions and knowledge base
        kb_selections = governor_data.get("knowledge_base_selections", {})
        if isinstance(kb_selections, dict):
            info["traditions"] = kb_selections.get("chosen_traditions", [])
            info["reasoning"] = kb_selections.get("reasoning", "")
        
        # Extract profile data directly
        profile = governor_data.get("profile", {})
        if isinstance(profile, dict):
            info["profile_element"] = profile.get("element", "").lower()
            info["aethyr"] = profile.get("aethyr", "")
            if "archetypal" in profile:
                info["tarot"] = profile["archetypal"].get("tarot", "")
        
        # Use enhanced element detection or fallback to profile
        try:
            element, confidence = self.element_detector.detect_element(governor_data)
            info["element"] = element
            info["element_confidence"] = confidence
        except Exception:
            # Fallback to profile element
            if info["profile_element"]:
                info["element"] = info["profile_element"]
                info["element_confidence"] = 0.8  # High confidence for profile data
        
        # Extract voidmaker expansion info
        voidmaker = governor_data.get("voidmaker_expansion", {})
        if isinstance(voidmaker, dict):
            info["voidmaker_question_count"] = sum(
                len(block.get("questions", {})) if isinstance(block, dict) else 0 
                for block in voidmaker.values()
            )
            
            # Extract themes from all voidmaker content
            themes = set()
            for block_data in voidmaker.values():
                if isinstance(block_data, dict):
                    for q_data in block_data.values():
                        if isinstance(q_data, dict) and "answer" in q_data:
                            answer = q_data["answer"].lower()
                            # Extract key thematic words
                            if "geometric" in answer or "sacred geometry" in answer:
                                themes.add("geometric")
                            if "hermetic" in answer:
                                themes.add("hermetic")
                            if "kabbal" in answer:
                                themes.add("kabbalistic")
                            if "unity" in answer or "unified" in answer:
                                themes.add("unity")
                            if "reality" in answer or "dimension" in answer:
                                themes.add("reality_manipulation")
            
            info["voidmaker_themes"] = list(themes)
        
        return info
    
    def create_enhanced_storyline(self, governor_name: str) -> Optional[Dict]:
        """Create enhanced storyline with improved features"""
        
        # Load governor data
        gov_data = self.load_governor_data(governor_name)
        if not gov_data:
            return None
        
        # Extract enhanced info
        info = self.extract_enhanced_info(gov_data)
        
        # Create enhanced storyline structure
        storyline = {
            "governor_id": governor_name,
            "version": "2.0",
            "generator": "enhanced_hybrid_v2",
            "metadata": {
                "governor_name": info["name"],
                "governor_number": info["number"],
                "primary_element": info["element"],
                "element_confidence": info["element_confidence"],
                "tradition_count": len(info["traditions"]),
                "selected_traditions": info["traditions"]
            },
            "persona": {
                "tone": self._determine_enhanced_tone(info),
                "traits": self._determine_enhanced_traits(info),
                "power_level": "formidable_approachable",
                "teaching_style": self._determine_teaching_style(info)
            },
            "voidmaker_integration": self._create_voidmaker_integration(gov_data, info),
            "story_tree": self.story_builder.build_enhanced_story_tree(info),
            "utilities": self._suggest_enhanced_utilities(info),
            "cross_governor_arcs": []
        }
        
        return storyline
    
    def _determine_enhanced_tone(self, info: Dict) -> str:
        """Enhanced tone determination"""
        element = info["element"]
        confidence = info["element_confidence"]
        tradition_count = len(info["traditions"])
        
        # Base tone on element with confidence weighting
        if confidence > 0.6:  # High confidence
            if element == "fire":
                return "fierce_passionate" if tradition_count >= 3 else "direct_powerful"
            elif element == "water":
                return "flowing_intuitive" if tradition_count >= 3 else "emotional_deep"
            elif element == "air":
                return "intellectual_precise" if tradition_count >= 3 else "quick_analytical"
            elif element == "earth":
                return "grounded_practical" if tradition_count >= 3 else "steady_reliable"
        
        # Default balanced tone for low confidence
        return "balanced_authority"
    
    def _determine_enhanced_traits(self, info: Dict) -> List[str]:
        """Enhanced trait determination"""
        traits = []
        
        # Add elemental trait with confidence
        element = info["element"]
        confidence = info["element_confidence"]
        
        if element != "unknown" and confidence > 0.4:
            element_desc = self.element_detector.get_element_description(element)
            traits.append(f"{element}_elemental")
        
        # Add tradition depth trait
        tradition_count = len(info["traditions"])
        if tradition_count >= 4:
            traits.append("tradition_master")
        elif tradition_count >= 2:
            traits.append("tradition_rich")
        else:
            traits.append("tradition_focused")
        
        # Add specific tradition traits
        traditions = [t.lower().replace(" ", "_") for t in info["traditions"]]
        if "hermetic_tradition" in traditions:
            traits.append("hermetic_wisdom")
        if "kabbalah" in traditions:
            traits.append("kabbalistic_depth")
        if "sacred_geometry" in traditions:
            traits.append("geometric_precision")
        
        return traits[:4]
    
    def _determine_teaching_style(self, info: Dict) -> str:
        """Determine teaching style based on element and traditions"""
        element = info["element"]
        
        if element == "fire":
            return "direct_challenging"
        elif element == "water":
            return "intuitive_flowing"
        elif element == "air":
            return "intellectual_testing"
        elif element == "earth":
            return "patient_methodical"
        else:
            return "balanced_testing"
    
    def _suggest_enhanced_utilities(self, info: Dict) -> List[str]:
        """Enhanced utility suggestions"""
        utilities = ["enhanced_dialogue", "reputation_tracking", "voidmaker_integration"]
        
        element = info["element"]
        confidence = info["element_confidence"]
        
        if confidence > 0.5:  # Only add element-specific if confident
            if element == "fire":
                utilities.extend(["combat_trial", "courage_test"])
            elif element == "water":
                utilities.extend(["wisdom_puzzle", "intuition_challenge"])
            elif element == "air":
                utilities.extend(["riddle_challenge", "logic_test"])
            elif element == "earth":
                utilities.extend(["patience_test", "endurance_trial"])
        
        return utilities
    
    def _create_voidmaker_integration(self, governor_data: Dict, info: Dict) -> Dict:
        """Create rich voidmaker integration based on actual expansion data"""
        voidmaker = governor_data.get("voidmaker_expansion", {})
        
        integration = {
            "cosmic_awareness": {"enabled": False, "questions": [], "themes": []},
            "reality_influence": {"enabled": False, "questions": [], "themes": []},
            "integration_unity": {"enabled": False, "questions": [], "themes": []}
        }
        
        # Extract actual voidmaker content by block
        for block_name, block_data in voidmaker.items():
            if not isinstance(block_data, dict):
                continue
                
            # Map block names to integration tiers
            tier_name = None
            if "cosmic_awareness" in block_name:
                tier_name = "cosmic_awareness"
            elif "reality_influence" in block_name:
                tier_name = "reality_influence"
            elif "integration_unity" in block_name:
                tier_name = "integration_unity"
            
            if tier_name and tier_name in integration:
                integration[tier_name]["enabled"] = True
                
                # Extract question/answer pairs
                questions = []
                themes = set()
                
                for q_num, q_data in block_data.items():
                    if isinstance(q_data, dict) and "question" in q_data and "answer" in q_data:
                        questions.append({
                            "number": q_num,
                            "question": q_data["question"][:100] + "..." if len(q_data["question"]) > 100 else q_data["question"],
                            "themes": self._extract_question_themes(q_data["answer"])
                        })
                        
                        # Extract themes from answer
                        answer = q_data["answer"].lower()
                        if "reality" in answer or "simulation" in answer:
                            themes.add("reality_manipulation")
                        if "consciousness" in answer or "awareness" in answer:
                            themes.add("consciousness_expansion")
                        if "unity" in answer or "one" in answer:
                            themes.add("unity_dissolution")
                        if "geometric" in answer or "sacred" in answer:
                            themes.add("sacred_mathematics")
                
                integration[tier_name]["questions"] = questions[:5]  # Limit to 5 sample questions
                integration[tier_name]["themes"] = list(themes)
        
        # Add overall statistics
        integration["statistics"] = {
            "total_questions": info["voidmaker_question_count"],
            "enabled_tiers": sum(1 for tier in integration.values() if isinstance(tier, dict) and tier.get("enabled")),
            "primary_themes": info["voidmaker_themes"]
        }
        
        return integration
    
    def _extract_question_themes(self, answer: str) -> List[str]:
        """Extract themes from a single voidmaker answer"""
        themes = []
        answer_lower = answer.lower()
        
        theme_keywords = {
            "metaphysical": ["reality", "existence", "being", "consciousness"],
            "geometric": ["geometric", "sacred", "pattern", "mathematical"],
            "mystical": ["mystical", "divine", "sacred", "transcendent"],
            "philosophical": ["truth", "wisdom", "understanding", "knowledge"]
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in answer_lower for keyword in keywords):
                themes.append(theme)
        
        return themes[:3]  # Limit to 3 themes per question
    
    def save_enhanced_storyline(self, storyline: Dict, governor_name: str) -> bool:
        """Save enhanced storyline"""
        output_file = self.output_path / f"{governor_name}_enhanced_v2.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(storyline, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def generate_enhanced_single(self, governor_name: str) -> bool:
        """Generate enhanced storyline for single governor"""
        print(f"🎭 Generating enhanced storyline for {governor_name}...")
        
        storyline = self.create_enhanced_storyline(governor_name)
        if not storyline:
            print(f"❌ Failed to create storyline for {governor_name}")
            return False
        
        if self.save_enhanced_storyline(storyline, governor_name):
            nodes = len(storyline["story_tree"]["nodes"])
            element = storyline["metadata"]["primary_element"]
            confidence = storyline["metadata"]["element_confidence"]
            print(f"✅ Generated enhanced storyline for {governor_name}")
            print(f"   Nodes: {nodes}, Element: {element} ({confidence:.2f})")
            return True
        else:
            return False

def test_enhanced_v2():
    """Test enhanced generator V2"""
    try:
        print("🧪 Testing Enhanced Generator V2...")
        
        generator = EnhancedGeneratorV2()
        
        # Find available governors
        if generator.governor_path.exists():
            governor_files = list(generator.governor_path.glob("*.json"))
            if governor_files:
                test_gov = governor_files[0].stem
                success = generator.generate_enhanced_single(test_gov)
                
                if success:
                    print("✅ Enhanced V2 test passed")
                    return True
        
        print("❌ Test failed - no governors found")
        return False
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    test_enhanced_v2() 