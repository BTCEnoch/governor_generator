#!/usr/bin/env python3
"""
Tradition Audit Script
Identifies duplicates, missing traditions, and cleanup needed
"""

import json
from pathlib import Path

class TraditionAuditor:
    """Audit traditions for duplicates and missing items"""
    
    def __init__(self):
        self.links_dir = Path("../links")
        self.archives_dir = Path("governor_archives")
        
        # Expected traditions based on user's knowledge databases and existing research
        self.expected_traditions = {
            # Core mystical traditions from knowledge databases
            'enochian_magic': 'From @enochian_knowledge_database.py',
            'golden_dawn': 'From @golden_dawn_knowledge_database.py', 
            'hermetic_philosophy': 'From @hermetic_knowledge_database.py',
            'kabbalistic_mysticism': 'From @kabbalah_knowledge_database.py',
            
            # Original research traditions
            'celtic_druidic': 'Original research tradition',
            'chaos_magic': 'Original research tradition',
            'classical_philosophy': 'Original research tradition', 
            'egyptian_magic': 'Original research tradition',
            'gnostic_traditions': 'Original research tradition',
            'i_ching': 'Original research tradition',
            'kuji_kiri': 'Original research tradition',
            'norse_traditions': 'Original research tradition',
            'sacred_geometry': 'Original research tradition',
            'sufi_mysticism': 'Original research tradition',
            'taoism': 'Original research tradition',
            'tarot_knowledge': 'Original research tradition',
            'thelema': 'Original research tradition'
        }
    
    def audit_research_files(self):
        """Audit research files for duplicates and issues"""
        print("🔍 RESEARCH FILES AUDIT")
        print("=" * 50)
        
        research_files = list(self.links_dir.glob("research_*.json"))
        found_traditions = {}
        duplicates = []
        
        for file in research_files:
            tradition_name = file.stem.replace('research_', '')
            if tradition_name in found_traditions:
                duplicates.append({
                    'tradition': tradition_name,
                    'files': [found_traditions[tradition_name], str(file)]
                })
            found_traditions[tradition_name] = str(file)
        
        print(f"📁 Found {len(research_files)} research files")
        print(f"🎯 Found {len(found_traditions)} unique traditions")
        
        if duplicates:
            print(f"⚠️  DUPLICATES FOUND: {len(duplicates)}")
            for dup in duplicates:
                print(f"     🔄 {dup['tradition']}:")
                for file in dup['files']:
                    size = Path(file).stat().st_size
                    print(f"        - {Path(file).name} ({size} bytes)")
        else:
            print("✅ No duplicates in research files")
        
        return found_traditions, duplicates
    
    def audit_archives(self):
        """Audit archive files"""
        print()
        print("🔍 ARCHIVE FILES AUDIT") 
        print("=" * 50)
        
        archive_files = list(self.archives_dir.glob("*_governor_archive.json"))
        found_archives = {}
        quality_stats = {"ENHANCED": 0, "BASIC": 0, "UNKNOWN": 0}
        
        for file in archive_files:
            tradition_name = file.stem.replace('_governor_archive', '')
            found_archives[tradition_name] = str(file)
            
            # Check quality
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                quality = data.get('quality_rating', 'UNKNOWN')
                concept_count = len(data.get('key_concepts', []))
                quality_stats[quality] += 1
                
                print(f"     📄 {tradition_name}: {quality} quality ({concept_count} concepts)")
            except:
                print(f"     ❌ {tradition_name}: Error reading file")
                quality_stats["UNKNOWN"] += 1
        
        print(f"📊 Archive Quality Summary:")
        for quality, count in quality_stats.items():
            print(f"     {quality}: {count} traditions")
        
        return found_archives
    
    def find_missing_traditions(self, found_traditions):
        """Find missing traditions"""
        print()
        print("🔍 MISSING TRADITIONS CHECK")
        print("=" * 50)
        
        missing = []
        for expected, source in self.expected_traditions.items():
            if expected not in found_traditions:
                missing.append({'tradition': expected, 'source': source})
        
        if missing:
            print(f"❌ MISSING: {len(missing)} traditions")
            for item in missing:
                print(f"     - {item['tradition']} ({item['source']})")
        else:
            print("✅ All expected traditions found")
        
        return missing
    
    def generate_cleanup_plan(self, duplicates, missing):
        """Generate cleanup recommendations"""
        print()
        print("🛠️  CLEANUP RECOMMENDATIONS")
        print("=" * 50)
        
        if duplicates:
            print("🔄 DUPLICATE CLEANUP:")
            for dup in duplicates:
                print(f"   {dup['tradition']}:")
                files_info = []
                for file_path in dup['files']:
                    path = Path(file_path)
                    size = path.stat().st_size
                    files_info.append((file_path, size))
                
                # Recommend keeping the larger file (likely has more content)
                files_info.sort(key=lambda x: x[1], reverse=True)
                print(f"     ✅ KEEP: {Path(files_info[0][0]).name} ({files_info[0][1]} bytes)")
                for file_path, size in files_info[1:]:
                    print(f"     ❌ DELETE: {Path(file_path).name} ({size} bytes)")
        
        if missing:
            print("📝 MISSING TRADITIONS TO CREATE:")
            for item in missing:
                print(f"   - Create research_{item['tradition']}.json")
        
        print()
        print("🎯 NEXT STEPS:")
        print("   1. Remove duplicate research files")
        print("   2. Create missing research files") 
        print("   3. Re-run comprehensive processing")
        print("   4. Verify all traditions have ENHANCED quality")

if __name__ == "__main__":
    auditor = TraditionAuditor()
    
    print("🏛️ MYSTICAL TRADITIONS AUDIT")
    print("=" * 80)
    
    found_traditions, duplicates = auditor.audit_research_files()
    found_archives = auditor.audit_archives() 
    missing = auditor.find_missing_traditions(found_traditions)
    
    auditor.generate_cleanup_plan(duplicates, missing)
    
    print()
    print("📋 AUDIT COMPLETE!")
    print("🎯 Use recommendations above to clean up the tradition system") 