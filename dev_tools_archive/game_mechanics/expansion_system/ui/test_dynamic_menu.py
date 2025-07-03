#!/usr/bin/env python3
"""
Dynamic Expansion Menu System Demo
==================================

Demonstrates the Dynamic Expansion Menu System with various scenarios
including discovery, loading, failures, and real-time updates.
"""

import time
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from .dynamic_menu import DynamicExpansionMenu, MenuItemState, ExpansionCategory


def print_menu_status(menu_summary: Dict[str, Any]) -> None:
    """Print formatted menu status"""
    print("\n" + "="*60)
    print("DYNAMIC EXPANSION MENU STATUS")
    print("="*60)
    
    # Overall stats
    stats = menu_summary['overall_stats']
    print(f"Total Expansions: {stats['total_expansions']}")
    print(f"Available: {stats['available_expansions']}")
    print(f"Loading: {stats['loading_expansions']}")
    print(f"Failed: {stats['failed_expansions']}")
    print()
    
    # Category details
    for category_name, category_data in menu_summary['categories'].items():
        print(f"📁 {category_data['display_name']}")
        print(f"   {category_data['description']}")
        print(f"   Status: {category_data['availability']}")
        print(f"   Loading: {category_data['is_loading']}")
        print(f"   Stats: {category_data['stats']}")
        
        # Show first few items
        items = category_data['items']
        if items:
            print("   Items:")
            for item in items[:3]:  # Show first 3 items
                print(f"     • {item['display_name']}")
                print(f"       {item['description']}")
            
            if len(items) > 3:
                print(f"     ... and {len(items) - 3} more items")
        print()


def demo_menu_updates():
    """Demonstrate dynamic menu updates"""
    
    # Menu update callback
    def on_menu_update(menu_summary: Dict[str, Any]):
        """Handle menu updates"""
        print(f"\n🔄 Menu Update Triggered - {menu_summary['overall_stats']['total_expansions']} expansions")
        
        # Show brief status
        if menu_summary['is_loading']:
            print("   ⏳ Loading in progress...")
        if menu_summary['has_failed']:
            print("   ❌ Some expansions failed to load")
        if menu_summary['has_available']:
            print("   ✅ Expansions available for use")
    
    # Initialize menu
    print("🚀 Initializing Dynamic Expansion Menu System")
    menu = DynamicExpansionMenu(update_callback=on_menu_update)
    
    # Create default categories
    print("📂 Creating default categories with sample data")
    menu.create_default_categories()
    
    # Show initial status
    print_menu_status(menu.get_menu_summary())
    
    # Simulate real-time updates
    print("\n🔄 Simulating Real-Time Updates")
    
    # Add a new expansion
    print("  ➕ Adding new expansion...")
    menu.add_expansion_item(
        expansion_id="custom_sigil_1",
        name="Custom Sigil Generator",
        category=ExpansionCategory.CUSTOM,
        description="Generate personalized sigils",
        state=MenuItemState.DISCOVERING,
        version="2.0",
        author="MysticDev",
        size_estimate=2048,
        is_premium=True
    )
    
    time.sleep(1)
    
    # Update expansion state
    print("  ✅ Marking expansion as available...")
    menu.update_expansion_state("custom_sigil_1", MenuItemState.AVAILABLE)
    
    time.sleep(1)
    
    # Simulate loading process
    print("  ⏳ Simulating loading process...")
    menu.update_expansion_state("custom_sigil_1", MenuItemState.LOADING)
    
    time.sleep(2)
    
    # Mark as failed
    print("  ❌ Simulating loading failure...")
    menu.update_expansion_state("custom_sigil_1", MenuItemState.FAILED)
    
    time.sleep(1)
    
    # Retry failed expansion
    print("  🔄 Retrying failed expansion...")
    success = menu.retry_failed_expansion("custom_sigil_1")
    print(f"     Retry initiated: {success}")
    
    time.sleep(1)
    
    # Mark as available
    print("  ✅ Retry successful!")
    menu.update_expansion_state("custom_sigil_1", MenuItemState.AVAILABLE)
    
    # Show final status
    print_menu_status(menu.get_menu_summary())
    
    return menu


def demo_menu_features():
    """Demonstrate various menu features"""
    
    print("\n🛠️  Testing Menu Features")
    menu = DynamicExpansionMenu()
    menu.create_default_categories()
    
    # Test category filtering
    print("📁 Testing Category Filtering")
    ars_goetia_expansions = menu.get_available_expansions(ExpansionCategory.ARS_GOETIA)
    print(f"   Found {len(ars_goetia_expansions)} Ars Goetia expansions")
    
    # Test failed expansion management
    print("❌ Testing Failed Expansion Management")
    
    # Add a failed expansion
    menu.add_expansion_item(
        expansion_id="broken_expansion",
        name="Broken Test Expansion",
        category=ExpansionCategory.CUSTOM,
        description="This expansion will fail",
        state=MenuItemState.FAILED
    )
    
    failed_expansions = menu.get_failed_expansions()
    print(f"   Found {len(failed_expansions)} failed expansions")
    
    # Test retry functionality
    print("🔄 Testing Retry Functionality")
    for i in range(5):  # Try to exceed retry limit
        success = menu.retry_failed_expansion("broken_expansion")
        print(f"   Retry attempt {i+1}: {'Success' if success else 'Failed (max retries)'}")
        if not success:
            break
    
    # Test category discovery
    print("🔍 Testing Category Discovery")
    
    # Add new category with expansions
    custom_expansions = [
        {'name': 'Planetary Seals', 'description': 'Seals of the seven planets'},
        {'name': 'Elemental Invocations', 'description': 'Calls to the four elements'},
        {'name': 'Angelic Scripts', 'description': 'Sacred angelic writing systems'}
    ]
    
    menu.mark_category_loading(ExpansionCategory.CUSTOM, True)
    time.sleep(1)
    
    menu.simulate_expansion_discovery(ExpansionCategory.CUSTOM, custom_expansions)
    
    # Show category data
    category_data = menu.get_category_data(ExpansionCategory.CUSTOM)
    if category_data:
        print(f"   Custom category: {category_data.availability.value}")
        print(f"   Items: {len(category_data.items)}")
        print(f"   Stats: {category_data.progress_stats}")
    
    # Test state persistence
    print("💾 Testing State Persistence")
    
    # Export state
    exported_state = menu.export_menu_state()
    print(f"   Exported state with {len(exported_state['categories'])} categories")
    
    # Create new menu and import state
    new_menu = DynamicExpansionMenu()
    new_menu.import_menu_state(exported_state)
    
    new_summary = new_menu.get_menu_summary()
    print(f"   Imported state with {new_summary['overall_stats']['total_expansions']} expansions")
    
    print("\n✅ All menu features tested successfully!")


if __name__ == "__main__":
    print("🎮 Dynamic Expansion Menu System Demo")
    print("=====================================")
    
    try:
        # Run demos
        print("\n🎯 Demo 1: Real-Time Menu Updates")
        demo_menu = demo_menu_updates()
        
        print("\n🎯 Demo 2: Advanced Menu Features")
        demo_menu_features()
        
        print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        raise 