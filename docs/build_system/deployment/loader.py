"""
Unified trait loading system for governors.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

from .schemas.trait_schemas import (
    GovernorTraits,
    CanonicalTraits,
    EnhancedTraits,
    MysticalTraits,
    PersonalityTraits,
    VisualTraits,
    ElementType,
    AlignmentType
)

logger = logging.getLogger(__name__)

class TraitLoader:
    """Unified system for loading all governor traits"""
    
    def __init__(self, data_root: Path = Path("data/governors/traits")):
        """Initialize the trait loader"""
        self.data_root = data_root
        self.canonical_path = data_root / "canonical"
        self.enhanced_path = data_root / "enhanced"
        self.mystical_path = data_root / "mystical"
        self.personality_path = data_root / "personality"
        self.visual_path = data_root / "visual"
        
        # Ensure directories exist
        for path in [self.canonical_path, self.enhanced_path, 
                    self.mystical_path, self.personality_path,
                    self.visual_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def load_all_traits(self, governor_id: str, governor_number: int) -> Optional[GovernorTraits]:
        """Load all traits for a governor"""
        try:
            # Load canonical traits
            canonical = self._load_canonical_traits(governor_id)
            if not canonical:
                logger.error(f"Failed to load canonical traits for {governor_id}")
                return None
                
            # Load enhanced traits
            enhanced = self._load_enhanced_traits(governor_id)
            if not enhanced:
                logger.error(f"Failed to load enhanced traits for {governor_id}")
                return None
                
            # Load mystical traits
            mystical = self._load_mystical_traits(governor_id)
            if not mystical:
                logger.error(f"Failed to load mystical traits for {governor_id}")
                return None
                
            # Load personality traits
            personality = self._load_personality_traits(governor_id)
            if not personality:
                logger.error(f"Failed to load personality traits for {governor_id}")
                return None
                
            # Load visual traits
            visual = self._load_visual_traits(governor_id)
            if not visual:
                logger.error(f"Failed to load visual traits for {governor_id}")
                return None
                
            # Create unified traits
            traits = GovernorTraits(
                governor_id=governor_id,
                governor_number=governor_number,
                canonical=canonical,
                enhanced=enhanced,
                mystical=mystical,
                personality=personality,
                visual=visual,
                last_updated=datetime.utcnow().isoformat()
            )
            
            return traits
            
        except Exception as e:
            logger.error(f"Error loading traits for {governor_id}: {e}")
            return None
    
    def _load_canonical_traits(self, governor_id: str) -> Optional[CanonicalTraits]:
        """Load canonical traits from JSON"""
        try:
            file_path = self.canonical_path / f"{governor_id.lower()}_canonical.json"
            if not file_path.exists():
                return None
                
            with open(file_path) as f:
                data = json.load(f)
                return CanonicalTraits(**data)
                
        except Exception as e:
            logger.error(f"Error loading canonical traits: {e}")
            return None
    
    def _load_enhanced_traits(self, governor_id: str) -> Optional[Dict[str, EnhancedTraits]]:
        """Load enhanced trait definitions"""
        try:
            file_path = self.enhanced_path / f"{governor_id.lower()}_enhanced.json"
            if not file_path.exists():
                return None
                
            with open(file_path) as f:
                data = json.load(f)
                return {name: EnhancedTraits(**traits) for name, traits in data.items()}
                
        except Exception as e:
            logger.error(f"Error loading enhanced traits: {e}")
            return None
    
    def _load_mystical_traits(self, governor_id: str) -> Optional[MysticalTraits]:
        """Load mystical traits"""
        try:
            file_path = self.mystical_path / f"{governor_id.lower()}_mystical.json"
            if not file_path.exists():
                return None
                
            with open(file_path) as f:
                data = json.load(f)
                # Convert string to enum
                data["element"] = ElementType(data["element"])
                data["alignment"] = AlignmentType(data["alignment"])
                return MysticalTraits(**data)
                
        except Exception as e:
            logger.error(f"Error loading mystical traits: {e}")
            return None
    
    def _load_personality_traits(self, governor_id: str) -> Optional[PersonalityTraits]:
        """Load personality traits"""
        try:
            file_path = self.personality_path / f"{governor_id.lower()}_personality.json"
            if not file_path.exists():
                return None
                
            with open(file_path) as f:
                data = json.load(f)
                return PersonalityTraits(**data)
                
        except Exception as e:
            logger.error(f"Error loading personality traits: {e}")
            return None
    
    def _load_visual_traits(self, governor_id: str) -> Optional[VisualTraits]:
        """Load visual traits"""
        try:
            file_path = self.visual_path / f"{governor_id.lower()}_visual.json"
            if not file_path.exists():
                return None
                
            with open(file_path) as f:
                data = json.load(f)
                return VisualTraits(**data)
                
        except Exception as e:
            logger.error(f"Error loading visual traits: {e}")
            return None 