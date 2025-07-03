#!/usr/bin/env python3
"""
Test script to verify validation integration works
"""

import logging

def test_integration():
    """Test the validation integration"""
    
    logging.basicConfig(level=logging.INFO)
    
    try:
        print("🧪 Testing batch generator with validation integration...")
        
        from batch_storyline_generator import BatchStorylineGenerator
        
        generator = BatchStorylineGenerator()
        print("✅ Batch generator initialized successfully")
        
        # Test loading a governor file with validation
        test_governor = "ABRIOND"
        governor_data = generator._load_governor_data(test_governor)
        
        if governor_data:
            print(f"✅ Governor data loaded and validated for {test_governor}")
        else:
            print(f"❌ Failed to load governor data for {test_governor}")
        
        print("🎉 Validation integration test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_integration()
    exit(0 if success else 1) 