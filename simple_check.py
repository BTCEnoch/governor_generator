#!/usr/bin/env python3
"""Simple file check"""

import json
import os

print("🔍 SIMPLE INVENTORY CHECK")
print("=" * 30)

# Check 1: Canon file
if os.path.exists("canon/canon_sources_index.json"):
    with open("canon/canon_sources_index.json", "r") as f:
        canon_data = json.load(f)
    traditions = len(canon_data["canon_sources_index"]["traditions"])
    print(f"✅ Canon file found: {traditions} traditions")
else:
    print("❌ Canon file missing!")

# Check 2: Games file  
if os.path.exists("games_with_angels.md"):
    with open("games_with_angels.md", "r") as f:
        content = f.read()
    lines = len(content.split('\n'))
    print(f"✅ Games file found: {lines} lines")
else:
    print("❌ Games file missing!")

# Check 3: Knowledge base
kb_path = "knowledge_base/data"
if os.path.exists(kb_path):
    kb_files = [f for f in os.listdir(kb_path) if f.endswith('_knowledge_database.py')]
    print(f"✅ Knowledge base found: {len(kb_files)} databases")
else:
    print("❌ Knowledge base missing!")

# Check 4: Tarot system
tarot_path = "knowledge_base/data/tarot_system"
if os.path.exists(tarot_path):
    tarot_files = len([f for f in os.listdir(tarot_path) if f.endswith('.py')])
    print(f"✅ Tarot system found: {tarot_files} files")
else:
    print("❌ Tarot system missing!")

print("\n📋 QUICK GAPS:")
print("• Need to separate mixed systems")
print("• Need to implement game mechanics")  
print("• Need unified profiler architecture")
print("• Need enhancement layers") 