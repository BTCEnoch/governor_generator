#!/usr/bin/env python3
"""
Simple Review Test - Show Enhanced Output
========================================

This script demonstrates the enhanced change summary output that shows exactly 
what was changed in a governor's profile during the review process.
"""

import json
from pathlib import Path

def show_change_summary():
    """Show the enhanced change summary for OCCODON."""
    
    # Load the latest review session
    review_sessions_dir = Path("review_sessions")
    latest_session_file = None
    
    # Find the most recent OCCODON session
    for session_file in review_sessions_dir.glob("OCCODON_*.json"):
        if latest_session_file is None or session_file.stat().st_mtime > latest_session_file.stat().st_mtime:
            latest_session_file = session_file
    
    if not latest_session_file:
        print("❌ No OCCODON review sessions found")
        return
    
    # Load session data
    with open(latest_session_file, 'r', encoding='utf-8') as f:
        session_data = json.load(f)
    
    governor_name = session_data["governor_name"]
    profile_updates = session_data["final_profile_updates"]
    kb_selections = profile_updates.get("knowledge_base_selections", [])
    personality_updates = profile_updates.get("personality", {})
    
    # Display enhanced summary
    print(f"🎉 Review completed for {governor_name}!")
    print(f"📚 Knowledge Base: {len(kb_selections)} traditions selected")
    print(f"🎭 Personality: {len(personality_updates)} traits confirmed")
    
    print(f"\n📝 CHANGES MADE TO {governor_name}'S PROFILE:")
    print("=" * 70)
    
    # Knowledge base changes
    if kb_selections:
        print("📚 KNOWLEDGE BASE SELECTIONS:")
        for i, tradition in enumerate(kb_selections, 1):
            tradition_display = tradition.replace("_", " ").title()
            if tradition == "enochian_magic":
                print(f"  {i}. {tradition_display} (Mandatory)")
            else:
                print(f"  {i}. {tradition_display}")
    
    # Personality trait changes
    if personality_updates:
        print("\n🎭 PERSONALITY TRAITS:")
        trait_labels = {
            "virtue": "Virtue",
            "flaw": "Flaw",
            "approach": "Approach", 
            "tone": "Tone",
            "motive_alignment": "Alignment",
            "role_archtype": "Role",
            "orientation_io": "Orientation",
            "polarity_cd": "Polarity",
            "self_regard": "Self-Regard"
        }
        
        for field, value in personality_updates.items():
            label = trait_labels.get(field, field.title())
            print(f"  • {label}: {value}")
    
    # Review metadata
    print(f"\n📋 REVIEW METADATA:")
    print(f"  • Review Date: {profile_updates['review_metadata']['last_review_date']}")
    print(f"  • Review Method: {profile_updates['review_metadata']['review_method']}")
    print(f"  • Sections Reviewed: {profile_updates['review_metadata']['total_sections_reviewed']}")
    
    # File locations
    print(f"\n💾 FILES UPDATED:")
    print(f"  • Profile: canon/canon_governor_profiles.json (OCCODON's section)")
    print(f"  • Review Session: {latest_session_file}")
    print(f"  • Profile Backup: profile_backups/OCCODON_backup_*.json")
    
    print("=" * 70)
    print("\n✨ OCCODON has successfully reviewed and updated their profile!")
    print("📖 All reasoning and selections have been recorded for future reference.")

if __name__ == "__main__":
    show_change_summary() 