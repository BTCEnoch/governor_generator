#!/usr/bin/env python3
"""
Trait Index Manager
==================

Unified system for loading and managing all governor trait indexes.
Consolidates the duplicate trait loading logic from multiple components.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import time
import importlib
import sys

@dataclass
class TraitLoadResult:
    """Result of trait loading operation."""
    success: bool
    trait_count: int
    categories_loaded: List[str]
    errors: List[str]
    load_time_ms: float

class TraitIndexManager:
    """Centralized manager for all governor trait indexes."""
    
    # Standard trait files that should be loaded
    STANDARD_TRAIT_FILES = [
        "virtues_pool.json",
        "flaws_pool.json", 
        "approaches.json",
        "tones.json",
        "motive_alignment.json",
        "role_archetypes.json",
        "orientation_io.json",
        "polarity_cd.json",
        "self_regard_options.json"
    ]
    
    # Mystical system files that should be loaded from Python modules
    MYSTICAL_SYSTEM_FILES = [
        "engines.mystical_systems.tarot_system.data.tarot_cards_database",
        "engines.mystical_systems.kabbalah_system.data.sefirot_database", 
        "engines.mystical_systems.zodiac_system.data.zodiac_database"
    ]
    
    def __init__(self, 
                 trait_indexes_dir: Optional[Path] = None,
                 cache_enabled: bool = True,
                 logger: Optional[logging.Logger] = None):
        """Initialize the trait index manager.
        
        Args:
            trait_indexes_dir: Path to trait indexes directory (auto-detected if None)
            cache_enabled: Whether to cache loaded traits in memory
            logger: Logger instance (creates default if None)
        """
        
        # Set up paths
        if trait_indexes_dir:
            self.trait_indexes_dir = Path(trait_indexes_dir)
        else:
            # Auto-detect from project structure
            self.trait_indexes_dir = self._find_trait_indexes_dir()
        
        # Set up logging
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        
        # Cache settings
        self.cache_enabled = cache_enabled
        self._trait_cache: Dict[str, Any] = {}
        self._cache_timestamp: Optional[float] = None
        
        # Validate setup
        if not self.trait_indexes_dir.exists():
            raise FileNotFoundError(f"Trait indexes directory not found: {self.trait_indexes_dir}")
        
        self.logger.info(f"TraitIndexManager initialized with directory: {self.trait_indexes_dir}")
    
    def _find_trait_indexes_dir(self) -> Path:
        """Auto-detect the trait indexes directory from project structure."""
        
        # Start from current file location and work up
        current_dir = Path(__file__).parent
        
        # Common possible paths relative to project root
        possible_paths = [
            "data/governors/indexes",
            "governor_indexes", 
            "indexes"
        ]
        
        # Search up the directory tree
        for _ in range(5):  # Max 5 levels up
            for possible_path in possible_paths:
                candidate = current_dir / possible_path
                if candidate.exists() and (candidate / "motive_alignment.json").exists():
                    return candidate
            current_dir = current_dir.parent
        
        # Fallback to default
        return Path(__file__).parent.parent.parent.parent / "data" / "governors" / "indexes"
    
    def _load_mystical_system_data(self, module_path: str) -> Dict[str, Any]:
        """Load mystical system data from a Python module.
        
        Args:
            module_path: Dot-separated module path (e.g., 'engines.mystical_systems.tarot_system.data.tarot_cards_database')
            
        Returns:
            Dictionary containing extracted mystical system data
        """
        try:
            # Import the module
            module = importlib.import_module(module_path)
            
            # Extract data based on module type
            if 'tarot_cards_database' in module_path:
                return self._extract_tarot_data(module)
            elif 'sefirot_database' in module_path:
                return self._extract_sefirot_data(module)
            elif 'zodiac_database' in module_path:
                return self._extract_zodiac_data(module)
            else:
                self.logger.warning(f"Unknown mystical system module: {module_path}")
                return {}
                
        except Exception as e:
            self.logger.error(f"Error loading mystical system module {module_path}: {e}")
            return {}
    
    def _extract_tarot_data(self, module) -> Dict[str, Any]:
        """Extract tarot card data from the tarot module."""
        tarot_data = {}
        
        # Get all tarot card collections
        if hasattr(module, 'MAJOR_ARCANA'):
            tarot_data['major_arcana'] = [
                {
                    'id': card.id,
                    'name': card.name,
                    'suit': card.suit.value if hasattr(card.suit, 'value') else str(card.suit),
                    'number': card.number,
                    'upright_keywords': card.upright_keywords,
                    'reversed_keywords': card.reversed_keywords,
                    'upright_meaning': card.upright_meaning,
                    'reversed_meaning': card.reversed_meaning,
                    'element': card.element,
                    'influence_categories': card.influence_categories
                }
                for card in module.MAJOR_ARCANA
            ]
        
        # Get minor arcana if available
        for suit_name in ['WANDS_SUIT', 'CUPS_SUIT', 'SWORDS_SUIT', 'PENTACLES_SUIT']:
            if hasattr(module, suit_name):
                suit_data = getattr(module, suit_name)
                tarot_data[suit_name.lower()] = [
                    {
                        'id': card.id,
                        'name': card.name,
                        'suit': card.suit.value if hasattr(card.suit, 'value') else str(card.suit),
                        'number': card.number,
                        'upright_keywords': card.upright_keywords,
                        'reversed_keywords': card.reversed_keywords,
                        'upright_meaning': card.upright_meaning,
                        'reversed_meaning': card.reversed_meaning,
                        'element': card.element,
                        'influence_categories': card.influence_categories
                    }
                    for card in suit_data
                ]
        
        return tarot_data
    
    def _extract_sefirot_data(self, module) -> Dict[str, Any]:
        """Extract sefirot data from the kabbalah module."""
        sefirot_data = {}
        
        if hasattr(module, 'ALL_SEFIROT'):
            sefirot_data['all_sefirot'] = [
                {
                    'position': sefirah.position.value if hasattr(sefirah.position, 'value') else str(sefirah.position),
                    'name': sefirah.name,
                    'hebrew_name': sefirah.hebrew_name,
                    'number': sefirah.number,
                    'divine_attribute': sefirah.divine_attribute,
                    'human_attribute': sefirah.human_attribute,
                    'spiritual_meaning': sefirah.spiritual_meaning,
                    'practical_meaning': sefirah.practical_meaning,
                    'shadow_aspect': sefirah.shadow_aspect,
                    'element': sefirah.element,
                    'planet': sefirah.planet,
                    'influence_categories': sefirah.influence_categories
                }
                for sefirah in module.ALL_SEFIROT
            ]
        
        return sefirot_data
    
    def _extract_zodiac_data(self, module) -> Dict[str, Any]:
        """Extract zodiac data from the zodiac module."""
        zodiac_data = {}
        
        # Use ALL_ZODIAC_SIGNS first (contains all 12 signs)
        all_signs = []
        if hasattr(module, 'ALL_ZODIAC_SIGNS'):
            all_signs = getattr(module, 'ALL_ZODIAC_SIGNS')
        else:
            # Fallback to combining parts if ALL_ZODIAC_SIGNS doesn't exist
            for collection_name in ['ZODIAC_SIGNS_PART1', 'ZODIAC_SIGNS_PART2']:
                if hasattr(module, collection_name):
                    collection = getattr(module, collection_name)
                    all_signs.extend(collection)
        
        if all_signs:
            zodiac_data['all_signs'] = [
                {
                    'name': sign.name,
                    'symbol': sign.symbol,
                    'dates': sign.dates,
                    'element': sign.element.value if hasattr(sign.element, 'value') else str(sign.element),
                    'modality': sign.modality.value if hasattr(sign.modality, 'value') else str(sign.modality),
                    'ruling_planet': sign.ruling_planet,
                    'positive_traits': sign.positive_traits,
                    'negative_traits': sign.negative_traits,
                    'keywords': sign.keywords,
                    'tarot_correspondence': sign.tarot_correspondence,
                    'body_parts': sign.body_parts,
                    'colors': sign.colors,
                    'stones': sign.stones,
                    'influence_categories': sign.influence_categories
                }
                for sign in all_signs
            ]
        
        return zodiac_data
    
    def load_all_traits(self, force_reload: bool = False) -> TraitLoadResult:
        """Load all standard trait indexes.
        
        Args:
            force_reload: Force reload even if cached data exists
            
        Returns:
            TraitLoadResult with loading statistics and any errors
        """
        
        start_time = time.time()
        
        # Check cache first
        if not force_reload and self.cache_enabled and self._trait_cache and self._cache_timestamp:
            cache_age = time.time() - self._cache_timestamp
            if cache_age < 300:  # 5 minutes cache
                self.logger.debug("Using cached trait data")
                return TraitLoadResult(
                    success=True,
                    trait_count=sum(len(traits) if isinstance(traits, (list, dict)) else 1 
                                  for traits in self._trait_cache.values()),
                    categories_loaded=list(self._trait_cache.keys()),
                    errors=[],
                    load_time_ms=(time.time() - start_time) * 1000
                )
        
        # Load fresh data
        trait_data = {}
        errors = []
        categories_loaded = []
        
        # Load standard JSON trait files
        for filename in self.STANDARD_TRAIT_FILES:
            try:
                filepath = self.trait_indexes_dir / filename
                
                if not filepath.exists():
                    error_msg = f"Trait file not found: {filename}"
                    errors.append(error_msg)
                    self.logger.warning(error_msg)
                    continue
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Store with clean category name (remove .json)
                category_name = filename.replace('.json', '')
                trait_data[category_name] = data
                categories_loaded.append(category_name)
                
                self.logger.debug(f"Loaded trait category: {category_name}")
                
            except Exception as e:
                error_msg = f"Error loading {filename}: {str(e)}"
                errors.append(error_msg)
                self.logger.error(error_msg)
        
        # Load mystical system data from Python modules
        for module_path in self.MYSTICAL_SYSTEM_FILES:
            try:
                mystical_data = self._load_mystical_system_data(module_path)
                
                if mystical_data:
                    # Extract system name from module path
                    if 'tarot_cards_database' in module_path:
                        system_name = 'tarot_cards'
                    elif 'sefirot_database' in module_path:
                        system_name = 'sefirot' 
                    elif 'zodiac_database' in module_path:
                        system_name = 'zodiac_signs'
                    else:
                        system_name = module_path.split('.')[-2].replace('_database', '').replace('_data', '')
                    
                    trait_data[system_name] = mystical_data
                    categories_loaded.append(system_name)
                    
                    self.logger.debug(f"Loaded mystical system: {system_name}")
                else:
                    error_msg = f"No data loaded from mystical system: {module_path}"
                    errors.append(error_msg)
                    self.logger.warning(error_msg)
                    
            except Exception as e:
                error_msg = f"Error loading mystical system {module_path}: {str(e)}"
                errors.append(error_msg)
                self.logger.error(error_msg)
        
        # Update cache
        if self.cache_enabled:
            self._trait_cache = trait_data
            self._cache_timestamp = time.time()
        
        # Calculate statistics
        trait_count = sum(
            len(traits) if isinstance(traits, (list, dict)) else 1 
            for traits in trait_data.values()
        )
        
        load_time_ms = (time.time() - start_time) * 1000
        success = len(categories_loaded) > 0
        
        result = TraitLoadResult(
            success=success,
            trait_count=trait_count,
            categories_loaded=categories_loaded,
            errors=errors,
            load_time_ms=load_time_ms
        )
        
        self.logger.info(f"Loaded {len(categories_loaded)} trait categories "
                        f"({trait_count} total traits) in {load_time_ms:.1f}ms")
        
        if errors:
            self.logger.warning(f"Encountered {len(errors)} errors during loading")
        
        return result
    
    def get_trait_data(self, category: str) -> Optional[Any]:
        """Get trait data for a specific category.
        
        Args:
            category: Category name (e.g., 'virtues_pool', 'motive_alignment')
            
        Returns:
            Trait data for the category, or None if not found
        """
        
        # Ensure data is loaded
        if not self._trait_cache:
            result = self.load_all_traits()
            if not result.success:
                return None
        
        return self._trait_cache.get(category)
    
    def get_all_trait_data(self) -> Dict[str, Any]:
        """Get all loaded trait data.
        
        Returns:
            Dictionary mapping category names to their trait data
        """
        
        # Ensure data is loaded
        if not self._trait_cache:
            result = self.load_all_traits()
            if not result.success:
                return {}
        
        return self._trait_cache.copy()
    
    def get_available_categories(self) -> List[str]:
        """Get list of available trait categories.
        
        Returns:
            List of category names that have been successfully loaded
        """
        
        if not self._trait_cache:
            self.load_all_traits()
        
        return list(self._trait_cache.keys())
    
    def validate_trait_files(self) -> Dict[str, bool]:
        """Validate that all expected trait files exist and are readable.
        
        Returns:
            Dictionary mapping filenames to their validity status
        """
        
        validation_results = {}
        
        for filename in self.STANDARD_TRAIT_FILES:
            filepath = self.trait_indexes_dir / filename
            
            try:
                if not filepath.exists():
                    validation_results[filename] = False
                    continue
                
                # Try to parse JSON
                with open(filepath, 'r', encoding='utf-8') as f:
                    json.load(f)
                
                validation_results[filename] = True
                
            except Exception as e:
                validation_results[filename] = False
                self.logger.error(f"Validation failed for {filename}: {e}")
        
        return validation_results
    
    def clear_cache(self):
        """Clear the cached trait data."""
        self._trait_cache.clear()
        self._cache_timestamp = None
        self.logger.debug("Trait cache cleared")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about the current cache state.
        
        Returns:
            Dictionary with cache statistics
        """
        
        return {
            "cache_enabled": self.cache_enabled,
            "cached_categories": len(self._trait_cache),
            "cache_timestamp": self._cache_timestamp,
            "cache_age_seconds": (time.time() - self._cache_timestamp) if self._cache_timestamp else None
        } 