#!/usr/bin/env python3
"""
Simple test for the game assets system
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_asset_schemas():
    """Test basic asset schema creation"""
    print("🧪 Testing Asset Schemas")
    print("=" * 50)
    
    try:
        from core.game_assets.schemas.asset_schemas import (
            GameAsset, AssetType, AssetRarity, ElementalAffinity,
            AssetSource, AssetEffect, PlayerAssetInventory
        )
        
        # Test creating a basic asset
        asset = GameAsset(
            id="test-artifact-001",
            name="Test Artifact",
            description="A test artifact for validation",
            type=AssetType.ARTIFACT,
            rarity=AssetRarity.RARE,
            elemental_affinity=ElementalAffinity.FIRE,
            base_value=500
        )
        
        print(f"✅ Basic asset created: {asset.name}")
        print(f"   ID: {asset.id}")
        print(f"   Type: {asset.type.value}")
        print(f"   Rarity: {asset.rarity.value}")
        print(f"   Element: {asset.elemental_affinity.value if asset.elemental_affinity else 'None'}")
        print(f"   Value: {asset.base_value}")
        
        # Test asset effect
        effect = AssetEffect(
            type="stat_boost",
            name="Fire Resistance",
            description="Provides resistance to fire damage",
            magnitude=0.5
        )
        
        asset.effects.append(effect)
        print(f"   Effects: {len(asset.effects)} effect(s)")
        
        # Test player inventory
        inventory = PlayerAssetInventory(player_id="test_player")
        inventory.add_asset(asset.id, 1)
        inventory.add_tokens("Wisdom", 100)
        
        print(f"✅ Player inventory created")
        print(f"   Assets: {len(inventory.assets)}")
        print(f"   Tokens: {inventory.tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_artifact_manager():
    """Test artifact manager functionality"""
    print("\n🧪 Testing Artifact Manager")
    print("=" * 50)
    
    try:
        from core.game_assets.artifact_manager import ArtifactManager
        from core.game_assets.schemas.asset_schemas import AssetRarity, ElementalAffinity
        
        # Initialize artifact manager
        manager = ArtifactManager()
        print("✅ ArtifactManager initialized")
        
        # Test basic artifact creation
        artifact = manager.create_artifact(
            rarity=AssetRarity.EPIC,
            elemental_affinity=ElementalAffinity.FIRE
        )
        
        print(f"✅ Created artifact: '{artifact.name}'")
        print(f"   Rarity: {artifact.rarity.value if artifact.rarity else 'None'}")
        print(f"   Element: {artifact.elemental_affinity.value if artifact.elemental_affinity else 'None'}")
        print(f"   Value: {artifact.base_value}")
        print(f"   Effects: {len(artifact.effects)}")
        print(f"   Requirements: {len(artifact.requirements)}")
        print(f"   Tags: {artifact.tags}")
        print(f"   Description: {artifact.description}")
        
        # Test governor-themed artifact
        governor_data = {
            'name': 'ABRIOND',
            'element': 'Fire',
            'wisdom_domains': ['Sacred Geometry'],
            'personality_traits': {'courage': 8}
        }
        
        governor_artifact = manager.create_artifact_for_governor(
            governor_data=governor_data,
            rarity=AssetRarity.LEGENDARY
        )
        
        print(f"\n✅ Created governor artifact: '{governor_artifact.name}'")
        print(f"   Creator: {governor_artifact.created_by_governor}")
        print(f"   Element: {governor_artifact.elemental_affinity.value if governor_artifact.elemental_affinity else 'None'}")
        print(f"   Lore: {governor_artifact.lore_text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Artifact manager test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Game Assets System Tests")
    print("=" * 60)
    
    # Run tests
    test1_result = test_asset_schemas()
    test2_result = test_artifact_manager()
    
    print("\n📊 Test Results:")
    print(f"   Asset Schemas: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"   Artifact Manager: {'✅ PASS' if test2_result else '❌ FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 All tests passed! Game Assets system is functional.")
    else:
        print("\n❌ Some tests failed. Check the output above.")
        sys.exit(1) 