# Dependency Mapping & Implementation Guide

## Current Import Dependency Analysis

### 🔍 **Current Import Patterns Found**

#### **1. Heavy sys.path Manipulation**
```python
# Pattern used in 20+ files:
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
```

#### **2. Cross-System Dependencies**
```python
# storyline_engine → knowledge_base
from knowledge_base.traditions.unified_knowledge_retriever import UnifiedKnowledgeRetriever
from knowledge_base.retrievers.focused_mystical_retriever import FocusedMysticalRetriever

# unified_profiler → mystical_systems  
from mystical_systems.tarot_system.engines.governor_tarot_assigner import GovernorTarotAssigner
from mystical_systems.kabbalah_system.data.sefirot_database import ALL_SEFIROT

# mystical_systems → unified_profiler
from unified_profiler.interfaces.base_system import BaseMysticalSystem, MysticalProfile

# scripts → everything
from storyline_engine.canonical_trait_registry import CanonicalTraitRegistry
from knowledge_base.traditions.unified_knowledge_retriever import UnifiedKnowledgeRetriever
```

### 📊 **Current Dependency Graph**

```
ROOT LEVEL IMPORTS:
├── scripts/ → storyline_engine/, knowledge_base/, mystical_systems/, unified_profiler/
├── tests/ → game_mechanics/, mystical_systems/
├── storyline_engine/ → knowledge_base/
├── unified_profiler/ → mystical_systems/
├── mystical_systems/ → unified_profiler/
├── knowledge_base/ → (standalone - good!)
├── integration_layer/ → (everything)
└── cli/ → mystical_systems/

PROBLEMATIC CIRCULAR IMPORTS:
unified_profiler/ ←→ mystical_systems/
```

## New Import Structure After Reorganization

### 🏗️ **New Dependency Hierarchy**

```
LAYER 1: data/ (no code dependencies)
├── data/governors/
├── data/canon/  
├── data/knowledge/
└── data/questlines/

LAYER 2: core/ (minimal cross-dependencies)
├── core/lighthouse/ (imports from data/knowledge/)
├── core/governors/ (imports from data/governors/, data/canon/)
├── core/questlines/ (imports from data/questlines/)
└── core/game_assets/ (imports from data/)

LAYER 3: engines/ (imports from core/ and data/)
├── engines/mystical_systems/ (imports from core/)
├── engines/trait_generation/ (imports from data/governors/, core/governors/)
├── engines/storyline_generation/ (imports from core/lighthouse/, core/governors/)
└── engines/batch_processing/ (imports from all engines/)

LAYER 4: build_system/ (imports from core/ and engines/)
├── build_system/trac_build/
├── build_system/contracts/
└── build_system/deployment/

LAYER 5: tools/ (imports from all layers as needed)
├── tools/cli/
├── tools/validation/
└── tools/utilities/
```

### 🔧 **New Import Patterns**

#### **1. Clean Data Access Pattern**
```python
# All data access goes through standardized loaders
from data.governors.governor_loader import GovernorLoader
from data.canon.canon_loader import CanonLoader
from data.knowledge.knowledge_loader import KnowledgeLoader
from data.questlines.questline_loader import QuestlineLoader

# No direct JSON file access
# No sys.path manipulation needed
```

#### **2. Core Service Pattern**
```python
# Core services are imported cleanly
from core.lighthouse.lighthouse_service import LighthouseService
from core.governors.governor_service import GovernorService
from core.questlines.questline_service import QuestlineService
from core.game_assets.asset_service import AssetService

# Services manage their own data dependencies
# No cross-core imports
```

#### **3. Engine Integration Pattern**
```python
# Engines import from core and data only
from core.lighthouse.lighthouse_service import LighthouseService
from core.governors.governor_service import GovernorService
from data.governors.governor_loader import GovernorLoader

# Engines use dependency injection
class StorylineEngine:
    def __init__(self, lighthouse_service, governor_service):
        self.lighthouse = lighthouse_service
        self.governors = governor_service
```

#### **4. Tool Access Pattern**
```python
# Tools can access any layer through registry
from tools.utilities.system_registry import SystemRegistry

# Registry provides clean access to all services
registry = SystemRegistry()
lighthouse = registry.get_service('lighthouse')
governors = registry.get_service('governors')
```

### 🧩 **Interface Definitions**

#### **Base Service Interface**
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseService(ABC):
    """Base interface all services must implement"""
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize service with configuration"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get service status and health"""
        pass
    
    @abstractmethod
    def shutdown(self) -> bool:
        """Clean shutdown of service"""
        pass
```

#### **Data Loader Interface**
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path

class BaseLoader(ABC):
    """Base interface all data loaders must implement"""
    
    @abstractmethod
    def load_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Load single item by ID"""
        pass
    
    @abstractmethod
    def load_all(self) -> List[Dict[str, Any]]:
        """Load all items"""
        pass
    
    @abstractmethod
    def search(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search items by criteria"""
        pass
```

## Implementation Plan

### 📋 **Phase 1: Create New Directory Structure**

#### **Step 1.1: Create Base Directories**
```bash
# Create main structure
mkdir -p data/governors data/canon data/knowledge data/questlines
mkdir -p core/lighthouse core/governors core/questlines core/game_assets
mkdir -p engines/mystical_systems engines/trait_generation engines/storyline_generation engines/batch_processing
mkdir -p build_system/trac_build build_system/contracts build_system/deployment
mkdir -p tools/cli tools/validation tools/utilities
mkdir -p docs/architecture docs/game_design docs/api
```

#### **Step 1.2: Create __init__.py Files**
```python
# Create package structure
touch data/__init__.py
touch core/__init__.py
touch engines/__init__.py
touch build_system/__init__.py
touch tools/__init__.py
touch docs/__init__.py

# Create subdirectory __init__.py files
find data core engines build_system tools -type d -exec touch {}/__init__.py \;
```

### 📋 **Phase 2: Move Data Files**

#### **Step 2.1: Move Governor Data**
```bash
# Move governor profiles to data/governors/
mv clean_governor_profiles/* data/governors/
mv governor_indexes/* data/governors/
mv personality_seeds/* data/governors/
```

#### **Step 2.2: Move Canon Data**
```bash
# Move canon files to data/canon/
mv canon/* data/canon/
```

#### **Step 2.3: Move Knowledge Data**
```bash
# Move knowledge base data to data/knowledge/
mv knowledge_base/archives/governor_archives/* data/knowledge/
mv knowledge_base/archives/personality_seeds/* data/knowledge/
mv knowledge_base/links/* data/knowledge/
mv knowledge_base/data/* data/knowledge/
```

### 📋 **Phase 3: Create Data Loaders**

#### **Step 3.1: Governor Loader**
```python
# data/governors/governor_loader.py
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import logging

logger = logging.getLogger(__name__)

class GovernorLoader:
    def __init__(self, data_path: Path = None):
        self.data_path = data_path or Path(__file__).parent
        self.profiles_path = self.data_path
        self.indexes_path = self.data_path
        
    def load_by_id(self, governor_id: str) -> Optional[Dict[str, Any]]:
        """Load governor profile by ID"""
        profile_file = self.profiles_path / f"{governor_id}.json"
        if profile_file.exists():
            with open(profile_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
        
    def load_all(self) -> List[Dict[str, Any]]:
        """Load all governor profiles"""
        profiles = []
        for profile_file in self.profiles_path.glob("*.json"):
            if profile_file.stem not in ['trait_choice_questions_catalog', 'canonical_traits']:
                try:
                    with open(profile_file, 'r', encoding='utf-8') as f:
                        profile = json.load(f)
                        profiles.append(profile)
                except Exception as e:
                    logger.warning(f"Failed to load {profile_file}: {e}")
        return profiles
        
    def search(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search governors by criteria"""
        all_profiles = self.load_all()
        results = []
        
        for profile in all_profiles:
            match = True
            for key, value in query.items():
                if key not in profile or profile[key] != value:
                    match = False
                    break
            if match:
                results.append(profile)
                
        return results
```

#### **Step 3.2: Canon Loader**
```python
# data/canon/canon_loader.py
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import logging

logger = logging.getLogger(__name__)

class CanonLoader:
    def __init__(self, data_path: Path = None):
        self.data_path = data_path or Path(__file__).parent
        
    def load_by_id(self, canon_id: str) -> Optional[Dict[str, Any]]:
        """Load canon entry by ID"""
        # Check various canon files
        canon_files = ['91_governors_canon.json', 'canon_governor_profiles.json', 'canon_sources.json']
        
        for canon_file in canon_files:
            file_path = self.data_path / canon_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if canon_id in data:
                            return data[canon_id]
                except Exception as e:
                    logger.warning(f"Failed to load {file_path}: {e}")
        return None
``` 