#!/usr/bin/env python3
"""
Enhanced Element Detector - Better elemental nature detection
Analyzes multiple governor data sources to determine elemental affinity
"""

from typing import Dict, List, Optional, Tuple

class EnhancedElementDetector:
    """Detects elemental nature from governor data"""
    
    def __init__(self):
        # Element keywords for detection
        self.element_keywords = {
            "fire": [
                "fire", "flame", "heat", "burn", "ignite", "blaze", "ember", "forge", 
                "passion", "rage", "anger", "red", "crimson", "solar", "sun"
            ],
            "water": [
                "water", "flow", "stream", "ocean", "sea", "wave", "tide", "fluid",
                "emotion", "intuition", "blue", "silver", "lunar", "moon", "deep"
            ],
            "air": [
                "air", "wind", "breath", "sky", "cloud", "storm", "thought", "mind",
                "intellect", "yellow", "gold", "swift", "light", "knowledge"
            ],
            "earth": [
                "earth", "stone", "rock", "mountain", "solid", "stable", "ground",
                "practical", "endurance", "green", "brown", "steady", "strong"
            ]
        }
        
        # Watchtower correspondences
        self.watchtower_elements = {
            "east": "air",
            "south": "fire", 
            "west": "water",
            "north": "earth"
        }
    
    def detect_element(self, governor_data: Dict) -> Tuple[str, float]:
        """Detect element with confidence score"""
        scores = {"fire": 0, "water": 0, "air": 0, "earth": 0}
        
        # Check elemental essence block (Q6)
        essence_score = self._analyze_elemental_essence(governor_data, scores)
        
        # Check personality traits (Q11-Q15)
        personality_score = self._analyze_personality(governor_data, scores)
        
        # Check teaching style (Q16-Q20)
        teaching_score = self._analyze_teaching_style(governor_data, scores)
        
        # Check aethyr description (Q3) for watchtower hints
        aethyr_score = self._analyze_aethyr_connection(governor_data, scores)
        
        # Find highest scoring element
        best_element = max(scores.items(), key=lambda x: x[1])
        
        total_possible = essence_score + personality_score + teaching_score + aethyr_score
        confidence = best_element[1] / max(total_possible, 1)
        
        return best_element[0], confidence
    
    def _analyze_elemental_essence(self, governor_data: Dict, scores: Dict) -> float:
        """Analyze B_elemental_essence block"""
        blocks = governor_data.get("blocks", {})
        elemental_block = blocks.get("B_elemental_essence", {})
        
        if not isinstance(elemental_block, dict):
            return 0
        
        text_to_analyze = ""
        for q_num in ["6", "7", "8", "9", "10"]:  # Q6-Q10
            if q_num in elemental_block:
                text_to_analyze += str(elemental_block[q_num]).lower() + " "
        
        if not text_to_analyze:
            return 0
        
        # Score based on keyword matches (weighted higher for elemental block)
        max_score = 0
        for element, keywords in self.element_keywords.items():
            element_score = sum(3 for keyword in keywords if keyword in text_to_analyze)
            scores[element] += element_score
            max_score = max(max_score, element_score)
        
        return max_score
    
    def _analyze_personality(self, governor_data: Dict, scores: Dict) -> float:
        """Analyze personality blocks for elemental traits"""
        blocks = governor_data.get("blocks", {})
        personality_block = blocks.get("C_personality", {})
        
        if not isinstance(personality_block, dict):
            return 0
        
        text_to_analyze = ""
        for q_num in ["11", "12", "13", "14", "15"]:  # Q11-Q15
            if q_num in personality_block:
                text_to_analyze += str(personality_block[q_num]).lower() + " "
        
        if not text_to_analyze:
            return 0
        
        max_score = 0
        for element, keywords in self.element_keywords.items():
            element_score = sum(2 for keyword in keywords if keyword in text_to_analyze)
            scores[element] += element_score
            max_score = max(max_score, element_score)
        
        return max_score
    
    def _analyze_teaching_style(self, governor_data: Dict, scores: Dict) -> float:
        """Analyze teaching and lesson blocks"""
        blocks = governor_data.get("blocks", {})
        lesson_block = blocks.get("D_core_lesson", {})
        
        if not isinstance(lesson_block, dict):
            return 0
        
        text_to_analyze = ""
        for q_num in ["16", "17", "18", "19", "20"]:  # Q16-Q20
            if q_num in lesson_block:
                text_to_analyze += str(lesson_block[q_num]).lower() + " "
        
        if not text_to_analyze:
            return 0
        
        max_score = 0
        for element, keywords in self.element_keywords.items():
            element_score = sum(1 for keyword in keywords if keyword in text_to_analyze)
            scores[element] += element_score
            max_score = max(max_score, element_score)
        
        return max_score
    
    def _analyze_aethyr_connection(self, governor_data: Dict, scores: Dict) -> float:
        """Analyze Aethyr description for watchtower connections"""
        blocks = governor_data.get("blocks", {})
        identity_block = blocks.get("A_identity_origin", {})
        
        if not isinstance(identity_block, dict) or "3" not in identity_block:
            return 0
        
        aethyr_description = str(identity_block["3"]).lower()
        
        # Check for directional/watchtower hints
        for direction, element in self.watchtower_elements.items():
            if direction in aethyr_description:
                scores[element] += 2
                return 2
        
        return 0
    
    def get_element_description(self, element: str) -> str:
        """Get descriptive text for element"""
        descriptions = {
            "fire": "fiery and passionate",
            "water": "flowing and intuitive", 
            "air": "swift and intellectual",
            "earth": "grounded and steadfast",
            "unknown": "mysterious and balanced"
        }
        return descriptions.get(element, descriptions["unknown"])

def test_enhanced_detector():
    """Test the enhanced element detector"""
    try:
        detector = EnhancedElementDetector()
        
        # Test data
        test_data = {
            "blocks": {
                "B_elemental_essence": {
                    "6": "Flames dance around me, burning with fierce passion and solar energy"
                },
                "C_personality": {
                    "11": "Courage, determination, fiery will"
                }
            }
        }
        
        element, confidence = detector.detect_element(test_data)
        description = detector.get_element_description(element)
        
        print(f"✅ Element detection working")
        print(f"   Detected: {element} (confidence: {confidence:.2f})")
        print(f"   Description: {description}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_enhanced_detector() 