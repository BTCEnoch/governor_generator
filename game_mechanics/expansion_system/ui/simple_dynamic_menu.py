#!/usr/bin/env python3
"""
Simplified Dynamic Expansion Menu System
=======================================

A working version without complex callbacks or logging that might cause timeouts.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from .progressive_loading import ExpansionCategory


class MenuItemState(Enum):
    """States for individual menu items"""
    AVAILABLE = "available"
    LOADING = "loading" 
    FAILED = "failed"
    DISCOVERING = "discovering"
    LOCKED = "locked"


@dataclass
class SimpleExpansionItem:
    """Simplified expansion menu item"""
    expansion_id: str
    name: str
    category: ExpansionCategory
    description: str
    state: MenuItemState = MenuItemState.AVAILABLE
    version: str = "1.0"
    
    @property
    def display_name(self) -> str:
        """Get formatted display name with state indicator"""
        indicators = {
            MenuItemState.AVAILABLE: "✅",
            MenuItemState.LOADING: "⏳",
            MenuItemState.FAILED: "❌", 
            MenuItemState.DISCOVERING: "🔍",
            MenuItemState.LOCKED: "🔒"
        }
        indicator = indicators.get(self.state, "❓")
        return f"{indicator} {self.name}"


class SimpleDynamicMenu:
    """
    Simplified dynamic expansion menu system.
    
    Provides basic menu functionality without complex callbacks or logging.
    """
    
    def __init__(self):
        """Initialize simple dynamic menu"""
        self.categories: Dict[ExpansionCategory, Dict[str, Any]] = {}
        self.expansion_items: Dict[str, SimpleExpansionItem] = {}
        self.menu_stats = {
            'total_expansions': 0,
            'available_expansions': 0,
            'failed_expansions': 0
        }
    
    def add_category(self, category: ExpansionCategory, display_name: str, description: str) -> None:
        """Add a menu category"""
        self.categories[category] = {
            'display_name': display_name,
            'description': description,
            'items': []
        }
    
    def add_expansion_item(self, expansion_id: str, name: str, category: ExpansionCategory,
                          description: str, state: MenuItemState = MenuItemState.AVAILABLE) -> None:
        """Add an expansion item to the menu"""
        item = SimpleExpansionItem(
            expansion_id=expansion_id,
            name=name,
            category=category,
            description=description,
            state=state
        )
        
        self.expansion_items[expansion_id] = item
        
        # Add to category
        if category not in self.categories:
            self.add_category(category, category.value.replace('_', ' ').title(), f'{category.value} expansions')
        
        self.categories[category]['items'].append(item)
        self._update_stats()
    
    def update_expansion_state(self, expansion_id: str, new_state: MenuItemState) -> None:
        """Update the state of an expansion item"""
        if expansion_id in self.expansion_items:
            self.expansion_items[expansion_id].state = new_state
            self._update_stats()
    
    def get_available_expansions(self, category: Optional[ExpansionCategory] = None) -> List[SimpleExpansionItem]:
        """Get list of available expansions"""
        items = self.expansion_items.values()
        
        if category:
            items = [item for item in items if item.category == category]
        
        return [item for item in items if item.state == MenuItemState.AVAILABLE]
    
    def get_menu_summary(self) -> Dict[str, Any]:
        """Get comprehensive menu summary"""
        category_summaries = {}
        
        for category, data in self.categories.items():
            category_summaries[category.value] = {
                'display_name': data['display_name'],
                'description': data['description'],
                'item_count': len(data['items']),
                'items': [
                    {
                        'id': item.expansion_id,
                        'name': item.name,
                        'display_name': item.display_name,
                        'state': item.state.value,
                        'description': item.description
                    }
                    for item in data['items']
                ]
            }
        
        return {
            'categories': category_summaries,
            'stats': self.menu_stats
        }
    
    def create_sample_data(self) -> None:
        """Create sample expansion data"""
        # Create categories with sample expansions
        sample_data = {
            ExpansionCategory.ARS_GOETIA: {
                'display_name': 'Ars Goetia',
                'description': 'Demonic entities and their sigils',
                'expansions': [
                    {'name': 'Baal', 'description': 'First duke of Hell'},
                    {'name': 'Paimon', 'description': 'Great king of the western winds'}
                ]
            },
            ExpansionCategory.ARCHANGELS: {
                'display_name': 'Archangels',
                'description': 'Divine messengers and their powers',
                'expansions': [
                    {'name': 'Michael', 'description': 'Guardian of the divine throne'},
                    {'name': 'Gabriel', 'description': 'Messenger of God'}
                ]
            },
            ExpansionCategory.CUSTOM: {
                'display_name': 'Custom',
                'description': 'User-created expansions',
                'expansions': [
                    {'name': 'Test Expansion', 'description': 'A test expansion'}
                ]
            }
        }
        
        # Populate menu with sample data
        for category, cat_data in sample_data.items():
            self.add_category(category, cat_data['display_name'], cat_data['description'])
            
            for expansion in cat_data['expansions']:
                expansion_id = f"{category.value}_{expansion['name'].lower().replace(' ', '_')}"
                self.add_expansion_item(
                    expansion_id=expansion_id,
                    name=expansion['name'],
                    category=category,
                    description=expansion['description'],
                    state=MenuItemState.AVAILABLE
                )
    
    def _update_stats(self) -> None:
        """Update internal statistics"""
        total = len(self.expansion_items)
        available = sum(1 for item in self.expansion_items.values() 
                       if item.state == MenuItemState.AVAILABLE)
        failed = sum(1 for item in self.expansion_items.values() 
                    if item.state == MenuItemState.FAILED)
        
        self.menu_stats = {
            'total_expansions': total,
            'available_expansions': available,
            'failed_expansions': failed
        }


# Test function
def test_simple_menu():
    """Test the simplified menu system"""
    print("🚀 Testing Simplified Dynamic Menu System")
    
    # Create menu
    menu = SimpleDynamicMenu()
    print("✅ Menu created successfully")
    
    # Add sample data
    menu.create_sample_data()
    print("✅ Sample data added successfully")
    
    # Get summary
    summary = menu.get_menu_summary()
    print(f"✅ Menu summary: {summary['stats']['total_expansions']} total expansions")
    
    # Test category filtering
    available_custom = menu.get_available_expansions(ExpansionCategory.CUSTOM)
    print(f"✅ Found {len(available_custom)} available custom expansions")
    
    print("🎉 Simplified menu system test completed successfully!")
    return menu


if __name__ == "__main__":
    test_simple_menu() 