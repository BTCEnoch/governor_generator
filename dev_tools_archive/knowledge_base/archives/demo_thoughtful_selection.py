#!/usr/bin/env python3
"""
Demo: Thoughtful Selection System for Governors
==============================================

This demo shows how the enhanced review system encourages thoughtful
selection based on existing lore and personality traits.
"""

import json
from pathlib import Path
from governor_review_template import GovernorReviewTemplateGenerator

def show_knowledge_base_section_demo():
    """Demonstrate the enhanced knowledge base selection guidance"""
    print("=" * 80)
    print("🏛️ ENHANCED KNOWLEDGE BASE SELECTION DEMO")
    print("=" * 80)
    
    generator = GovernorReviewTemplateGenerator()
    
    # Sample governor profile for context
    sample_profile = {
        "name": "ABRIOND",
        "title": "Governor of Righteous Fury", 
        "aethyr": "ZAA",
        "personality": {
            "virtue": "Courage",
            "flaw": "Impatience", 
            "approach": "Direct Confrontation",
            "tone": "Authoritative",
            "role_archtype": "The Warrior"
        }
    }
    
    current_selections = ["enochian_magic", "norse_traditions", "chaos_magic"]
    
    kb_section = generator.create_knowledge_base_section(current_selections, sample_profile)
    
    print("SAMPLE KNOWLEDGE BASE SELECTION GUIDANCE:")
    print("-" * 50)
    print(kb_section.instruction[:800] + "...")
    print("\n📚 Available traditions (sample):")
    
    for i, (tradition, description) in enumerate(list(kb_section.available_options.items())[:3]):
        print(f"\n{i+1}. {tradition}:")
        print(description[:300] + "...")

def show_personality_trait_section_demo():
    """Demonstrate the enhanced personality trait selection guidance"""
    print("\n" + "=" * 80)
    print("🎭 ENHANCED PERSONALITY TRAIT SELECTION DEMO")
    print("=" * 80)
    
    generator = GovernorReviewTemplateGenerator()
    
    # Sample governor profile for context
    sample_profile = {
        "name": "ABRIOND",
        "title": "Governor of Righteous Fury",
        "aethyr": "ZAA", 
        "personality": {
            "virtue": "Courage",
            "flaw": "Impatience",
            "approach": "Direct Confrontation", 
            "tone": "Authoritative",
            "role_archtype": "The Warrior"
        }
    }
    
    # Demo virtue selection
    virtue_section = generator.create_personality_trait_section("virtues", "Courage", sample_profile)
    
    print("SAMPLE VIRTUE SELECTION GUIDANCE:")
    print("-" * 50)
    print(virtue_section.instruction[:700] + "...")
    
    print("\n⚡ Key Features of Enhanced Selection:")
    print("• Shows current trait definition and AI impact")
    print("• Provides deep consideration questions")
    print("• Shows personality constellation context")
    print("• Encourages authentic self-reflection")
    print("• Emphasizes long-term consequences")

def main():
    """Run the thoughtful selection demo"""
    print("🎯 THOUGHTFUL GOVERNOR SELECTION SYSTEM DEMONSTRATION")
    print("\nKey Improvements:")
    print("✅ Enochian Magic automatically assigned (not selectable)")
    print("✅ Rich tradition descriptions with core wisdom")
    print("✅ Personality-aware selection guidance")
    print("✅ Deep consideration questions")
    print("✅ Synergy analysis with existing traits")
    print("✅ Long-term AI consciousness perspective")
    
    try:
        show_knowledge_base_section_demo()
        show_personality_trait_section_demo()
        
        print("\n" + "=" * 80)
        print("🎉 DEMO COMPLETE - THOUGHTFUL SELECTION SYSTEM READY!")
        print("=" * 80)
        print("\nNext Steps:")
        print("1. Generate review templates for all 91 governors")
        print("2. Create Claude API batch processing system")
        print("3. Process governor responses and update profiles")
        
    except Exception as e:
        print(f"Demo error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 