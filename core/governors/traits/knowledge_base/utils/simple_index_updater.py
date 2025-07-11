#!/usr/bin/env python3
"""
Simple Canonical Index Updater
Updates canon_sources_index.json with working curated sources
"""

import json
import logging
from pathlib import Path
import shutil
from datetime import datetime
from typing import List, Dict
import sys

# Add project root to Python path for proper imports
project_root = Path(__file__).parent.parent.parent
# )  # Removed during reorganization

# Import our components - updated paths for current structure
try:
    # Try current knowledge_base structure first
    from data.knowledge.data.curated_sources import CURATED_SOURCES
    print("✅ Using knowledge_base structure")
except ImportError:
    try:
        # Future lighthouse_core structure (migration-ready code)
        from lighthouse_core.data.curated_sources import CURATED_SOURCES  # type: ignore
        print("✅ Using lighthouse_core structure")
    except ImportError:
        # Create fallback data if neither exists
        print("⚠️  No curated sources found, using fallback")
        CURATED_SOURCES = {
            "kabbalah": {},
            "hermetic_tradition": {},
            "enochian_magic": {}
        }

class SimpleIndexUpdater:
    """Simple updater for canonical sources index"""
    
    def __init__(self, canon_path: str = "canon/canon_sources_index.json"):
        self.canon_path = Path(canon_path)
        # Create backup directory in current knowledge_base structure
        self.backup_dir = Path("knowledge_base/data/index_backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("SimpleIndexUpdater")
        
        # Initialize without processor for now to avoid import issues
        self.logger.info("🔧 Simple Index Updater initialized")
    
    def update_tradition_with_curated_sources(self, tradition_name: str) -> bool:
        """
        Update a single tradition with curated sources
        """
        self.logger.info(f"🔄 Updating {tradition_name} with curated sources")
        
        # Check if we have curated sources for this tradition
        if tradition_name not in CURATED_SOURCES:
            self.logger.warning(f"⚠️  No curated sources available for {tradition_name}")
            return False
        
        try:
            # Create backup
            self._create_backup()
            
            # Load current index
            if not self.canon_path.exists():
                self.logger.error(f"❌ Canon file not found: {self.canon_path}")
                return False
                
            with open(self.canon_path, 'r', encoding='utf-8') as f:
                canon_data = json.load(f)
            
            # Get curated URLs for this tradition
            curated_urls = self._get_curated_urls_for_tradition(tradition_name)
            
            if not curated_urls:
                self.logger.warning(f"⚠️  No curated URLs found for {tradition_name}")
                return False
            
            # Update the tradition's links
            if tradition_name in canon_data['canon_sources_index']['traditions']:
                old_links = canon_data['canon_sources_index']['traditions'][tradition_name]['links']
                canon_data['canon_sources_index']['traditions'][tradition_name]['links'] = curated_urls
                
                # Add update metadata
                canon_data['canon_sources_index']['traditions'][tradition_name]['last_updated'] = datetime.now().isoformat()
                canon_data['canon_sources_index']['traditions'][tradition_name]['previous_links_count'] = len(old_links)
                canon_data['canon_sources_index']['traditions'][tradition_name]['updated_links_count'] = len(curated_urls)
                canon_data['canon_sources_index']['traditions'][tradition_name]['update_source'] = "curated_sources"
                
                # Save updated index
                with open(self.canon_path, 'w', encoding='utf-8') as f:
                    json.dump(canon_data, f, indent=2, ensure_ascii=False)
                
                self.logger.info(f"✅ Updated {tradition_name}: {len(old_links)} -> {len(curated_urls)} URLs")
                self.logger.info(f"📋 New URLs: {curated_urls}")
                return True
            else:
                self.logger.error(f"❌ Tradition {tradition_name} not found in index")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Failed to update {tradition_name}: {e}")
            return False
    
    def _get_curated_urls_for_tradition(self, tradition: str) -> List[str]:
        """Extract just the URLs from curated sources for a tradition"""
        urls = []
        
        curated_data = CURATED_SOURCES.get(tradition, {})
        for source_type, sources in curated_data.items():
            if isinstance(sources, list):
                for source in sources:
                    if isinstance(source, dict) and "url" in source:
                        urls.append(source["url"])
                    elif isinstance(source, str):
                        urls.append(source)
        
        return urls
    
    def _create_backup(self) -> Path:
        """Create a backup of the current canonical index"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f"canon_sources_backup_{timestamp}.json"
        
        if self.canon_path.exists():
            shutil.copy2(self.canon_path, backup_path)
            self.logger.info(f"📋 Created backup: {backup_path}")
        
        return backup_path
    
    def show_current_vs_curated_comparison(self, tradition: str) -> None:
        """Show comparison between current URLs and available curated sources"""
        
        print(f"\n📊 COMPARISON FOR {tradition.upper()}")
        print("=" * 50)
        
        try:
            # Load current index
            if not self.canon_path.exists():
                print(f"❌ Canon file not found: {self.canon_path}")
                return
                
            with open(self.canon_path, 'r', encoding='utf-8') as f:
                canon_data = json.load(f)
            
            current_urls = canon_data['canon_sources_index']['traditions'].get(tradition, {}).get('links', [])
            curated_urls = self._get_curated_urls_for_tradition(tradition)
            
            print(f"📂 CURRENT URLs ({len(current_urls)}):")
            for i, url in enumerate(current_urls, 1):
                print(f"   {i}. {url}")
            
            print(f"\n🎯 CURATED URLs ({len(curated_urls)}):")
            for i, url in enumerate(curated_urls, 1):
                print(f"   {i}. {url}")
            
            print(f"\n📈 IMPROVEMENT:")
            print(f"   Current: {len(current_urls)} URLs")
            print(f"   Curated: {len(curated_urls)} URLs")
            print(f"   Change: {len(curated_urls) - len(current_urls):+d} URLs")
            
        except Exception as e:
            print(f"❌ Error comparing: {e}")

def main():
    """Test the simple index updater"""
    
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    updater = SimpleIndexUpdater()
    
    # Test traditions that have curated sources
    test_traditions = ["kabbalah", "hermetic_tradition", "enochian_magic"]
    
    print("🔧 SIMPLE INDEX UPDATER TEST")
    print("=" * 50)
    
    for tradition in test_traditions:
        # Show comparison first
        updater.show_current_vs_curated_comparison(tradition)
        
        # Ask if user wants to update (simulated yes for testing)
        print(f"\n❓ Update {tradition} with curated sources? (This is a test run)")
        print("   Note: This will modify your canonical index file!")
    
    print(f"\n💡 To actually update, call:")
    print(f"   updater.update_tradition_with_curated_sources('tradition_name')")

if __name__ == "__main__":
    main() 