#!/usr/bin/env python3
"""
Simple test script for persona extractor
"""

import sys
from pathlib import Path
sys.path.append(str(Path("storyline_engine")))

try:
    print("🧪 Testing imports...")
    from core_loader import CoreDataLoader
    print("✅ CoreDataLoader imported")
    
    from persona_extractor import PersonaExtractor
    print("✅ PersonaExtractor imported")
    
    print("🧪 Testing core loader...")
    loader = CoreDataLoader()
    available = loader.list_available_governors()
    print(f"📊 Found {len(available)} governors")
    
    if available:
        test_gov = available[0]
        print(f"🧪 Loading {test_gov}...")
        
        profile = loader.load_enhanced_governor(test_gov)
        print(f"✅ Loaded {profile.governor_name}")
        print(f"   Traditions: {len(profile.knowledge_base_selections.chosen_traditions)}")
        print(f"   Voidmaker blocks: {len(profile.voidmaker_expansion)}")
        
        print("🧪 Testing persona extraction...")
        extractor = PersonaExtractor()
        persona = extractor.extract_persona(test_gov)
        
        print(f"✅ Extracted persona for {persona.governor_name}")
        print(f"   Tone: {persona.tone}")
        print(f"   Traits: {persona.traits}")
        
    else:
        print("❌ No governors found")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 