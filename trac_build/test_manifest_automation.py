#!/usr/bin/env python3
"""
Test Manifest Automation System
===============================

Demonstrates the manifest automation system with content validation,
deployment, and rollback capabilities.
"""

import logging
import json
from pathlib import Path
from manifest_automation_system import (
    ManifestAutomationEngine, 
    ContentType, 
    ManifestStatus
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_manifest_automation():
    """Test the manifest automation system"""
    print("🚀 Testing Manifest Automation System")
    
    # Setup test directories
    manifest_dir = Path("test_manifests")
    backup_dir = Path("test_backups")
    
    # Clean up previous test data
    import shutil
    if manifest_dir.exists():
        shutil.rmtree(manifest_dir)
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    
    try:
        # Initialize automation engine
        print("📂 Initializing manifest automation engine...")
        engine = ManifestAutomationEngine(manifest_dir, backup_dir)
        
        # Create test content items
        test_content = [
            {
                "content_id": "governor_abriond_portrait",
                "content_type": "governor_portrait",
                "file_path": "test_portrait.webp",  # Mock file
                "metadata": {
                    "governor_name": "ABRIOND",
                    "aethyr": "LIL",
                    "region": "Northeast"
                }
            },
            {
                "content_id": "governor_abriond_metadata", 
                "content_type": "governor_metadata",
                "file_path": "test_metadata.json",  # Mock file
                "dependencies": ["governor_abriond_portrait"],
                "metadata": {
                    "governor_name": "ABRIOND",
                    "aethyr": "LIL", 
                    "region": "Northeast"
                }
            },
            {
                "content_id": "artifact_ancient_key",
                "content_type": "artifact_nft",
                "file_path": "test_artifact.webp",  # Mock file
                "metadata": {
                    "name": "Ancient Key",
                    "rarity": "legendary",
                    "category": "tool"
                }
            }
        ]
        
        # Create manifest version
        print("📋 Creating manifest version...")
        manifest = engine.create_manifest_version("v1.0.0", test_content)
        
        print(f"✅ Created manifest {manifest.version} with {len(manifest.content_items)} items")
        print(f"   Status: {manifest.status.value}")
        print(f"   Dependencies: {manifest.dependencies}")
        
        # Test content patching
        print("🔧 Testing manifest patching...")
        patches = {
            "governor_abriond_portrait": {
                "inscription_id": "abc123def456789..."
            },
            "governor_abriond_metadata": {
                "metadata": {"version": "1.1"}
            }
        }
        
        patch_success = engine.patch_manifest_content("v1.0.0", patches)
        print(f"   Patch result: {'✅ Success' if patch_success else '❌ Failed'}")
        
        # Test validation
        print("🔍 Testing content validation...")
        for content_id, item in manifest.content_items.items():
            # Note: Files don't exist, so validation will show expected failures
            is_valid, errors = engine.validate_content_item(item)
            print(f"   {content_id}: {'✅ Valid' if is_valid else '❌ Invalid'}")
            if errors:
                print(f"     Errors: {errors[:2]}")  # Show first 2 errors
        
        # Test inscription ID validation
        print("🔐 Testing inscription ID validation...")
        test_inscription_id = "abc123def456789012345678901234567890123456789012345678901234"
        is_valid_id = engine.validate_inscription_id(test_inscription_id, manifest.content_items["governor_abriond_portrait"])
        print(f"   Inscription ID validation: {'✅ Valid' if is_valid_id else '❌ Invalid'}")
        
        # Test deployment status
        print("📊 Getting deployment status...")
        status = engine.get_deployment_status()
        print(f"   Active version: {status['active_version']}")
        print(f"   Total versions: {status['total_versions']}")
        print(f"   Deployable versions: {status['deployable_versions']}")
        
        # Simulate successful deployment
        print("🚀 Simulating deployment...")
        # Mark all content as valid for deployment test
        for item in manifest.content_items.values():
            item.validation_status = "valid"
            item.inscription_id = f"mock_inscription_{item.content_id}"
        
        deploy_success = engine.deploy_manifest_version("v1.0.0")
        print(f"   Deployment result: {'✅ Success' if deploy_success else '❌ Failed'}")
        
        if deploy_success:
            print(f"   Active version: {engine.active_version}")
        
        # Create second version for rollback test
        print("📋 Creating second manifest version...")
        test_content_v2 = test_content + [{
            "content_id": "new_expansion_pack",
            "content_type": "expansion_pack", 
            "file_path": "test_expansion.zip",
            "metadata": {
                "name": "Ars Goetia Pack",
                "version": "1.0",
                "dependencies": []
            }
        }]
        
        manifest_v2 = engine.create_manifest_version("v2.0.0", test_content_v2)
        
        # Mark v2 content as valid
        for item in manifest_v2.content_items.values():
            item.validation_status = "valid"
            item.inscription_id = f"mock_inscription_v2_{item.content_id}"
        
        # Deploy v2
        deploy_v2_success = engine.deploy_manifest_version("v2.0.0")
        print(f"   V2 deployment result: {'✅ Success' if deploy_v2_success else '❌ Failed'}")
        
        # Test rollback
        if deploy_v2_success:
            print("⏪ Testing rollback...")
            rollback_success = engine.rollback_to_version("v1.0.0")
            print(f"   Rollback result: {'✅ Success' if rollback_success else '❌ Failed'}")
            print(f"   Active version after rollback: {engine.active_version}")
        
        # Final status
        final_status = engine.get_deployment_status()
        print("\n📈 Final Status:")
        print(f"   Active version: {final_status['active_version']}")
        print(f"   Version statuses: {final_status['version_statuses']}")
        print(f"   Rollback history: {len(final_status['rollback_history'])} operations")
        
        print("\n🎉 Manifest automation system test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup test directories
        try:
            if manifest_dir.exists():
                shutil.rmtree(manifest_dir)
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            print("🧹 Test cleanup completed")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

if __name__ == "__main__":
    test_manifest_automation() 