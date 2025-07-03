#!/usr/bin/env python3
"""
Dynamic Expansion Menu System
============================

Provides real-time menu updates when expansions load, with category-based
organization and availability indicators for the expansion system.
"""

import time
import logging
from typing import Dict, List, Optional, Callable, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from .progressive_loading import ExpansionCategory, LoadingState

logger = logging.getLogger(__name__)


class MenuItemState(Enum):
    """States for individual menu items"""
    AVAILABLE = "available"
    LOADING = "loading" 
    FAILED = "failed"
    DISCOVERING = "discovering"
    LOCKED = "locked"
    CORRUPTED = "corrupted"


class MenuAvailability(Enum):
    """Overall availability states for menu categories"""
    ALL_AVAILABLE = "all_available"
    PARTIALLY_AVAILABLE = "partially_available"
    NONE_AVAILABLE = "none_available"
    LOADING = "loading"
    ERROR = "error"


@dataclass
class ExpansionMenuItem:
    """Single expansion menu item with state and metadata"""
    expansion_id: str
    name: str
    category: ExpansionCategory
    description: str
    state: MenuItemState = MenuItemState.DISCOVERING
    inscription_id: Optional[str] = None
    version: str = "1.0"
    author: Optional[str] = None
    size_estimate: int = 0  # bytes
    last_updated: float = field(default_factory=time.time)
    requirements: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    is_premium: bool = False
    preview_image: Optional[str] = None
    
    @property
    def is_available(self) -> bool:
        """Check if expansion is available for loading"""
        return self.state == MenuItemState.AVAILABLE
    
    @property
    def display_name(self) -> str:
        """Get formatted display name with state indicator"""
        state_indicators = {
            MenuItemState.AVAILABLE: "✅",
            MenuItemState.LOADING: "⏳",
            MenuItemState.FAILED: "❌", 
            MenuItemState.DISCOVERING: "🔍",
            MenuItemState.LOCKED: "🔒",
            MenuItemState.CORRUPTED: "⚠️"
        }
        indicator = state_indicators.get(self.state, "❓")
        return f"{indicator} {self.name}"


@dataclass
class CategoryMenuData:
    """Menu data for a specific expansion category"""
    category: ExpansionCategory
    display_name: str
    description: str
    items: List[ExpansionMenuItem] = field(default_factory=list)
    is_loading: bool = False
    is_discovered: bool = False
    failed_count: int = 0
    discovery_timestamp: Optional[float] = None
    
    @property
    def availability(self) -> MenuAvailability:
        """Get overall availability for this category"""
        if not self.items:
            return MenuAvailability.NONE_AVAILABLE if self.is_discovered else MenuAvailability.LOADING
        
        available_count = sum(1 for item in self.items if item.is_available)
        total_count = len(self.items)
        
        if self.is_loading:
            return MenuAvailability.LOADING
        elif available_count == total_count:
            return MenuAvailability.ALL_AVAILABLE
        elif available_count > 0:
            return MenuAvailability.PARTIALLY_AVAILABLE
        else:
            return MenuAvailability.NONE_AVAILABLE
    
    @property
    def progress_stats(self) -> Dict[str, int]:
        """Get progress statistics for this category"""
        total = len(self.items)
        available = sum(1 for item in self.items if item.state == MenuItemState.AVAILABLE)
        loading = sum(1 for item in self.items if item.state == MenuItemState.LOADING)
        failed = sum(1 for item in self.items if item.state == MenuItemState.FAILED)
        
        return {
            'total': total,
            'available': available,
            'loading': loading,
            'failed': failed,
            'discovering': total - available - loading - failed
        }


class DynamicExpansionMenu:
    """
    Dynamic expansion menu system with real-time updates.
    
    Manages expansion discovery, categorization, and availability
    indicators with live updates as expansions are discovered and loaded.
    """
    
    def __init__(self, update_callback: Optional[Callable[[Dict[str, Any]], None]] = None):
        """
        Initialize dynamic expansion menu.
        
        Args:
            update_callback: Function called when menu state changes
        """
        self.update_callback = update_callback
        
        # Menu state
        self.categories: Dict[ExpansionCategory, CategoryMenuData] = {}
        self.expansion_items: Dict[str, ExpansionMenuItem] = {}
        self.menu_state = {
            'last_update': time.time(),
            'total_expansions': 0,
            'available_expansions': 0,
            'loading_expansions': 0,
            'failed_expansions': 0
        }
        
        # Discovery tracking
        self.discovery_queue: Set[str] = set()
        self.failed_discoveries: Dict[str, int] = {}  # expansion_id -> retry_count
        
        logger.info("DynamicExpansionMenu initialized")
    
    def initialize_categories(self, category_configs: Dict[ExpansionCategory, Dict[str, str]]) -> None:
        """
        Initialize menu categories with metadata.
        
        Args:
            category_configs: Dictionary mapping categories to their display info
        """
        for category, config in category_configs.items():
            self.categories[category] = CategoryMenuData(
                category=category,
                display_name=config.get('display_name', category.value.replace('_', ' ').title()),
                description=config.get('description', f'Expansions for {category.value}')
            )
        
        logger.info(f"Initialized {len(self.categories)} menu categories")
        self._update_menu_state()


    def add_expansion_item(self, expansion_id: str, name: str, category: ExpansionCategory,
                          description: str, **kwargs) -> None:
        """
        Add an expansion item to the menu.
        
        Args:
            expansion_id: Unique identifier
            name: Display name
            category: Expansion category 
            description: Item description
            **kwargs: Additional item properties
        """
        # Create menu item
        item = ExpansionMenuItem(
            expansion_id=expansion_id,
            name=name,
            category=category,
            description=description,
            **kwargs
        )
        
        # Add to tracking
        self.expansion_items[expansion_id] = item
        
        # Add to category
        if category not in self.categories:
            # Auto-create category if not exists
            self.categories[category] = CategoryMenuData(
                category=category,
                display_name=category.value.replace('_', ' ').title(),
                description=f'Expansions for {category.value}'
            )
        
        self.categories[category].items.append(item)
        
        logger.debug(f"Added expansion item: {expansion_id} to {category.value}")
        self._update_menu_state()
    
    def update_expansion_state(self, expansion_id: str, new_state: MenuItemState,
                             **kwargs) -> None:
        """
        Update the state of a specific expansion item.
        
        Args:
            expansion_id: Expansion to update
            new_state: New state for the expansion
            **kwargs: Additional properties to update
        """
        if expansion_id not in self.expansion_items:
            logger.warning(f"Attempted to update unknown expansion: {expansion_id}")
            return
        
        item = self.expansion_items[expansion_id]
        old_state = item.state
        item.state = new_state
        
        # Update additional properties
        for key, value in kwargs.items():
            if hasattr(item, key):
                setattr(item, key, value)
        
        logger.debug(f"Updated expansion {expansion_id}: {old_state.value} -> {new_state.value}")
        self._update_menu_state()
    
    def mark_category_loading(self, category: ExpansionCategory, is_loading: bool = True) -> None:
        """Mark a category as loading or not loading"""
        if category in self.categories:
            self.categories[category].is_loading = is_loading
            if is_loading:
                self.categories[category].discovery_timestamp = time.time()
            
            logger.debug(f"Category {category.value} loading state: {is_loading}")
            self._update_menu_state()
    
    def mark_category_discovered(self, category: ExpansionCategory) -> None:
        """Mark a category as discovered (finished scanning for expansions)"""
        if category in self.categories:
            self.categories[category].is_discovered = True
            self.categories[category].is_loading = False
            
            logger.info(f"Category {category.value} discovery completed")
            self._update_menu_state()
    
    def get_category_data(self, category: ExpansionCategory) -> Optional[CategoryMenuData]:
        """Get menu data for a specific category"""
        return self.categories.get(category)
    
    def get_available_expansions(self, category: Optional[ExpansionCategory] = None) -> List[ExpansionMenuItem]:
        """
        Get list of available expansions, optionally filtered by category.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of available expansion items
        """
        items = self.expansion_items.values()
        
        if category:
            items = [item for item in items if item.category == category]
        
        return [item for item in items if item.is_available]
    
    def get_failed_expansions(self) -> List[ExpansionMenuItem]:
        """Get list of failed expansions for retry interface"""
        return [item for item in self.expansion_items.values() 
                if item.state == MenuItemState.FAILED]
    
    def retry_failed_expansion(self, expansion_id: str) -> bool:
        """
        Retry a failed expansion discovery/loading.
        
        Args:
            expansion_id: Expansion to retry
            
        Returns:
            True if retry was initiated, False if max retries exceeded
        """
        if expansion_id not in self.expansion_items:
            return False
        
        retry_count = self.failed_discoveries.get(expansion_id, 0)
        if retry_count >= 3:
            logger.warning(f"Max retries exceeded for expansion: {expansion_id}")
            return False
        
        # Update retry count and state
        self.failed_discoveries[expansion_id] = retry_count + 1
        self.update_expansion_state(expansion_id, MenuItemState.DISCOVERING)
        
        logger.info(f"Retrying expansion {expansion_id} (attempt {retry_count + 1}/3)")
        return True
    
    def get_menu_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive menu summary for UI display.
        
        Returns:
            Dictionary with menu state and statistics
        """
        category_summaries = {}
        
        for category, data in self.categories.items():
            stats = data.progress_stats
            category_summaries[category.value] = {
                'display_name': data.display_name,
                'description': data.description,
                'availability': data.availability.value,
                'is_loading': data.is_loading,
                'is_discovered': data.is_discovered,
                'stats': stats,
                'items': [
                    {
                        'id': item.expansion_id,
                        'name': item.name,
                        'display_name': item.display_name,
                        'state': item.state.value,
                        'description': item.description,
                        'version': item.version,
                        'size_estimate': item.size_estimate,
                        'is_premium': item.is_premium
                    }
                    for item in data.items
                ]
            }
        
        return {
            'categories': category_summaries,
            'overall_stats': self.menu_state,
            'has_available': self.menu_state['available_expansions'] > 0,
            'has_failed': self.menu_state['failed_expansions'] > 0,
            'is_loading': self.menu_state['loading_expansions'] > 0
        }
    
    def _update_menu_state(self) -> None:
        """Update internal menu state and trigger callback"""
        # Calculate overall statistics
        total = len(self.expansion_items)
        available = sum(1 for item in self.expansion_items.values() 
                       if item.state == MenuItemState.AVAILABLE)
        loading = sum(1 for item in self.expansion_items.values() 
                     if item.state == MenuItemState.LOADING)
        failed = sum(1 for item in self.expansion_items.values() 
                    if item.state == MenuItemState.FAILED)
        
        # Update menu state
        self.menu_state.update({
            'last_update': time.time(),
            'total_expansions': total,
            'available_expansions': available,
            'loading_expansions': loading,
            'failed_expansions': failed
        })
        
        # Trigger callback if provided (safely)
        if self.update_callback:
            try:
                # Create a simplified summary to avoid infinite recursion
                simple_summary = {
                    'overall_stats': self.menu_state.copy(),
                    'category_count': len(self.categories),
                    'has_available': available > 0,
                    'has_failed': failed > 0,
                    'is_loading': loading > 0
                }
                self.update_callback(simple_summary)
            except Exception as e:
                logger.error(f"Error in menu update callback: {e}")
    
    def start_discovery(self, category: Optional[ExpansionCategory] = None) -> None:
        """
        Start discovery process for expansions.
        
        Args:
            category: Optional category to discover, None for all categories
        """
        categories_to_discover = [category] if category else list(self.categories.keys())
        
        for cat in categories_to_discover:
            if cat in self.categories:
                self.mark_category_loading(cat, True)
                
                # Mock discovery simulation (in real implementation, this would be async)
                logger.info(f"Starting discovery for category: {cat.value}")
                
                # Add to discovery queue
                self.discovery_queue.add(cat.value)
        
        logger.info(f"Started discovery for {len(categories_to_discover)} categories")
    
    def simulate_expansion_discovery(self, category: ExpansionCategory, 
                                   expansion_configs: List[Dict[str, Any]]) -> None:
        """
        Simulate discovering expansions for a category.
        
        Args:
            category: Category to populate
            expansion_configs: List of expansion configurations
        """
        logger.info(f"Simulating discovery of {len(expansion_configs)} expansions for {category.value}")
        
        for config in expansion_configs:
            # Add expansion item
            expansion_id = config.get('id', f"{category.value}_{config['name'].lower().replace(' ', '_')}")
            
            self.add_expansion_item(
                expansion_id=expansion_id,
                name=config['name'],
                category=category,
                description=config.get('description', f'{config["name"]} expansion'),
                state=MenuItemState.DISCOVERING,
                version=config.get('version', '1.0'),
                author=config.get('author', 'Unknown'),
                size_estimate=config.get('size_estimate', 1024),
                is_premium=config.get('is_premium', False),
                requirements=config.get('requirements', []),
                dependencies=config.get('dependencies', [])
            )
            
            # Simulate discovery process (deterministic for testing)
            # Most expansions are available, with occasional failures
            if config['name'] in ['Broken Test', 'Corrupted']:
                discovery_result = MenuItemState.FAILED
            else:
                discovery_result = MenuItemState.AVAILABLE
            
            self.update_expansion_state(expansion_id, discovery_result)
        
        # Mark category as discovered
        self.mark_category_discovered(category)
    
    def integrate_with_progressive_loader(self, progressive_loader) -> None:
        """
        Integrate with progressive loading system for seamless updates.
        
        Args:
            progressive_loader: Progressive loading instance
        """
        logger.info("Integrating with progressive loading system")
        
        # Set up event handlers for progressive loader updates
        def on_loading_started(expansion_id: str):
            """Handle when progressive loader starts loading an expansion"""
            if expansion_id in self.expansion_items:
                self.update_expansion_state(expansion_id, MenuItemState.LOADING)
        
        def on_loading_completed(expansion_id: str, success: bool):
            """Handle when progressive loader completes loading"""
            if expansion_id in self.expansion_items:
                new_state = MenuItemState.AVAILABLE if success else MenuItemState.FAILED
                self.update_expansion_state(expansion_id, new_state)
        
        def on_loading_failed(expansion_id: str, error: str):
            """Handle when progressive loader fails"""
            if expansion_id in self.expansion_items:
                self.update_expansion_state(
                    expansion_id, 
                    MenuItemState.FAILED,
                    error_message=error
                )
        
        # Register callbacks with progressive loader
        if hasattr(progressive_loader, 'add_callback'):
            progressive_loader.add_callback('loading_started', on_loading_started)
            progressive_loader.add_callback('loading_completed', on_loading_completed)
            progressive_loader.add_callback('loading_failed', on_loading_failed)
    
    def create_default_categories(self) -> None:
        """Create default expansion categories with sample data"""
        default_categories = {
            ExpansionCategory.ARS_GOETIA: {
                'display_name': 'Ars Goetia',
                'description': 'Demonic entities and their sigils'
            },
            ExpansionCategory.ARCHANGELS: {
                'display_name': 'Archangels',
                'description': 'Divine messengers and their powers'
            },
            ExpansionCategory.ENOCHIAN_KEYS: {
                'display_name': 'Enochian Keys',
                'description': 'Sacred calls and invocations'
            },
            ExpansionCategory.WATCHTOWERS: {
                'display_name': 'Watchtowers',
                'description': 'Elemental watchtowers and their guardians'
            },
            ExpansionCategory.AETHYRS: {
                'display_name': 'Aethyrs',
                'description': 'Ethereal realms and their mysteries'
            },
            ExpansionCategory.CUSTOM: {
                'display_name': 'Custom',
                'description': 'User-created expansions'
            }
        }
        
        self.initialize_categories(default_categories)
        
        # Add sample expansions for demonstration
        sample_expansions = {
            ExpansionCategory.ARS_GOETIA: [
                {'name': 'Baal', 'description': 'First duke of Hell'},
                {'name': 'Paimon', 'description': 'Great king of the western winds'},
                {'name': 'Beleth', 'description': 'Mighty and terrible king'}
            ],
            ExpansionCategory.ARCHANGELS: [
                {'name': 'Michael', 'description': 'Guardian of the divine throne'},
                {'name': 'Gabriel', 'description': 'Messenger of God'},
                {'name': 'Raphael', 'description': 'Healer of the earth'}
            ],
            ExpansionCategory.ENOCHIAN_KEYS: [
                {'name': 'First Key', 'description': 'The key of divine authority'},
                {'name': 'Second Key', 'description': 'The key of elemental balance'}
            ]
        }
        
        # Populate with sample data
        for category, expansions in sample_expansions.items():
            self.simulate_expansion_discovery(category, expansions)
        
        logger.info("Created default categories with sample expansions")
    
    def export_menu_state(self) -> Dict[str, Any]:
        """Export complete menu state for persistence"""
        return {
            'categories': {
                cat.value: {
                    'display_name': data.display_name,
                    'description': data.description,
                    'is_discovered': data.is_discovered,
                    'discovery_timestamp': data.discovery_timestamp,
                    'items': [
                        {
                            'expansion_id': item.expansion_id,
                            'name': item.name,
                            'category': item.category.value,
                            'description': item.description,
                            'state': item.state.value,
                            'version': item.version,
                            'author': item.author,
                            'size_estimate': item.size_estimate,
                            'requirements': item.requirements,
                            'dependencies': item.dependencies,
                            'is_premium': item.is_premium
                        }
                        for item in data.items
                    ]
                }
                for cat, data in self.categories.items()
            },
            'menu_state': self.menu_state,
            'failed_discoveries': self.failed_discoveries
        }
    
    def import_menu_state(self, state_data: Dict[str, Any]) -> None:
        """Import menu state from persistence"""
        logger.info("Importing menu state from persistence")
        
        # Clear existing state
        self.categories.clear()
        self.expansion_items.clear()
        
        # Import categories and items
        for cat_value, cat_data in state_data.get('categories', {}).items():
            try:
                category = ExpansionCategory(cat_value)
                
                # Create category
                self.categories[category] = CategoryMenuData(
                    category=category,
                    display_name=cat_data['display_name'],
                    description=cat_data['description'],
                    is_discovered=cat_data.get('is_discovered', False),
                    discovery_timestamp=cat_data.get('discovery_timestamp')
                )
                
                # Import items
                for item_data in cat_data.get('items', []):
                    item = ExpansionMenuItem(
                        expansion_id=item_data['expansion_id'],
                        name=item_data['name'],
                        category=category,
                        description=item_data['description'],
                        state=MenuItemState(item_data['state']),
                        version=item_data.get('version', '1.0'),
                        author=item_data.get('author'),
                        size_estimate=item_data.get('size_estimate', 0),
                        requirements=item_data.get('requirements', []),
                        dependencies=item_data.get('dependencies', []),
                        is_premium=item_data.get('is_premium', False)
                    )
                    
                    self.expansion_items[item.expansion_id] = item
                    self.categories[category].items.append(item)
                    
            except (ValueError, KeyError) as e:
                logger.error(f"Error importing category {cat_value}: {e}")
        
        # Import other state
        self.menu_state = state_data.get('menu_state', self.menu_state)
        self.failed_discoveries = state_data.get('failed_discoveries', {})
        
        logger.info(f"Imported menu state with {len(self.expansion_items)} expansions")
        self._update_menu_state() 