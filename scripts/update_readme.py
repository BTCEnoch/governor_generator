#!/usr/bin/env python3
"""
README Update Script
Helps systematically update the README.md with new clean architecture
"""

import os
from pathlib import Path
from datetime import datetime

class ReadmeUpdater:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.readme_path = self.root_dir / "README.md"
        self.backup_path = self.root_dir / f"README_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        # New architecture structure
        self.new_structure = {
            "core/": "Active core systems (lighthouse, governors, questlines, game_assets)",
            "engines/": "Active processing engines (storyline_generation, mystical_systems, batch_processing, trait_generation)",
            "data/": "Active data storage (governors, knowledge, questlines, canon)",
            "tools/": "Active development tools (cli, game_mechanics, utilities, validation)",
            "build_system/": "Build and deployment systems (contracts, deployment, trac_build)",
            "docs/": "Documentation and architecture guides"
        }
        
        # Files to highlight in new structure
        self.key_files = {
            "core/lighthouse/": "Knowledge base and retrieval systems",
            "engines/storyline_generation/": "Active storyline generation engine",
            "data/governors/profiles/": "91 Governor profiles (ABRIOND.json, etc.)",
            "data/knowledge/": "Processed knowledge base",
            "tools/cli/mystical_cli.py": "Command-line interface",
            "build_system/trac_build/": "Trac systems architecture"
        }

    def create_backup(self):
        """Create backup of current README"""
        if self.readme_path.exists():
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(self.backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Backup created: {self.backup_path.name}")
            return True
        return False

    def get_section_boundaries(self):
        """Identify major sections that need updating"""
        sections = {
            "project_overview": (1, 50),
            "architecture": (200, 400), 
            "quick_start": (401, 600),
            "developer_guide": (601, 750),
            "file_structure": (751, 829)
        }
        return sections

    def generate_new_architecture_section(self):
        """Generate new architecture documentation"""
        return f"""## 🏗️ **CLEAN PROJECT ARCHITECTURE** (Updated {datetime.now().strftime('%Y-%m-%d')})

### **✅ REORGANIZED STRUCTURE - All Backup Files Removed**
After comprehensive cleanup, the project now uses a clean, production-ready structure:

```
governor_generator/
├── core/                           # 🎯 ACTIVE CORE SYSTEMS
│   ├── lighthouse/                 # Knowledge base and retrieval
│   ├── governors/                  # Governor processing systems  
│   ├── questlines/                 # Quest and storyline logic
│   └── game_assets/                # Game data and assets
│
├── engines/                        # ⚡ ACTIVE PROCESSING ENGINES  
│   ├── storyline_generation/       # Main storyline engine
│   ├── mystical_systems/           # Tarot, kabbalah, numerology
│   ├── batch_processing/           # Batch job coordination
│   └── trait_generation/           # Personality trait systems
│
├── data/                           # 📊 ACTIVE DATA STORAGE
│   ├── governors/profiles/         # 91 Governor JSON files
│   ├── knowledge/                  # Processed knowledge base
│   ├── questlines/                 # Generated questlines
│   └── canon/                      # Source materials
│
├── tools/                          # 🛠️ ACTIVE DEVELOPMENT TOOLS
│   ├── cli/                        # Command-line interfaces
│   ├── game_mechanics/             # Game systems and UI
│   ├── utilities/                  # Helper scripts and tools
│   └── validation/                 # Testing and validation
│
├── build_system/                   # 🚀 BUILD & DEPLOYMENT
│   ├── contracts/                  # Smart contracts
│   ├── deployment/                 # Deployment scripts
│   └── trac_build/                 # Trac systems architecture
│
├── docs/                           # 📚 DOCUMENTATION
│   ├── api/                        # API documentation
│   ├── architecture/               # Architecture guides
│   └── game_design/                # Game design documents
│
└── scripts/                        # 🔧 UTILITY SCRIPTS
    └── update_readme.py            # This file!
```

### **🧹 CLEANUP COMPLETED - Space Recovered: ~41-46 MB**
- ❌ **Removed**: `reorganization_backup/` (35.4 MB)
- ❌ **Removed**: `dev_tools_archive/` (old development tools)  
- ❌ **Removed**: All backup directories and temporary files
- ❌ **Removed**: 22 `__pycache__` directories
- ✅ **Result**: Clean, organized, production-ready codebase
"""

if __name__ == "__main__":
    updater = ReadmeUpdater()
    
    print("📚 README Update Helper")
    print("=" * 50)
    print("1. create_backup() - Backup current README")
    print("2. get_section_boundaries() - Identify sections to update")  
    print("3. generate_new_architecture_section() - New architecture docs")
    print("\nUse this in interactive Python or import functions as needed") 