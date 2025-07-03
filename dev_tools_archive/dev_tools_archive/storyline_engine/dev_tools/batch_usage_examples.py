#!/usr/bin/env python3
"""
Batch Usage Examples - How to use the batch storyline generator
"""

import logging
from pathlib import Path
from batch_storyline_generator import BatchStorylineGenerator

def example_1_test_batch():
    """Example 1: Test with a small batch of governors"""
    logging.basicConfig(level=logging.INFO)
    
    generator = BatchStorylineGenerator()
    
    # Test with just 3 governors first
    test_governors = ["ABRIOND", "VALGARS", "OCCODON"]
    
    print("🧪 Testing batch generation with 3 governors...")
    success = generator.generate_all_storylines(test_governors)
    
    if success:
        print("✅ Test batch completed successfully!")
    else:
        print("❌ Test batch failed!")

def example_2_all_governors():
    """Example 2: Generate storylines for all 91 governors"""
    logging.basicConfig(level=logging.INFO)
    
    generator = BatchStorylineGenerator()
    
    # Generate for all governors (None = all governors)
    print("🚀 Starting full batch generation for all 91 governors...")
    success = generator.generate_all_storylines()
    
    if success:
        print("🎉 All governor storylines generated!")
    else:
        print("❌ Batch generation failed!")

def example_3_chunked_processing():
    """Example 3: Process governors in chunks for better control"""
    logging.basicConfig(level=logging.INFO)
    
    generator = BatchStorylineGenerator()
    
    # Get all governor names
    governor_files = list(generator.governor_path.glob("*.json"))
    all_governors = [f.stem for f in governor_files]
    
    # Process in chunks of 20
    chunk_size = 20
    chunks = [all_governors[i:i + chunk_size] for i in range(0, len(all_governors), chunk_size)]
    
    print(f"📦 Processing {len(all_governors)} governors in {len(chunks)} chunks...")
    
    for i, chunk in enumerate(chunks):
        print(f"🔄 Processing chunk {i+1}/{len(chunks)}: {len(chunk)} governors")
        
        success = generator.generate_all_storylines(chunk)
        
        if success:
            print(f"✅ Chunk {i+1} completed successfully!")
        else:
            print(f"❌ Chunk {i+1} failed!")

def example_4_monitor_only():
    """Example 4: Monitor an existing batch by ID"""
    logging.basicConfig(level=logging.INFO)
    
    generator = BatchStorylineGenerator()
    
    # If you have a batch ID from a previous run
    batch_id = "your_batch_id_here"  # Replace with actual batch ID
    
    print(f"👀 Monitoring existing batch: {batch_id}")
    
    # Monitor the batch
    batch_status = generator.monitor_batch(batch_id)
    
    if batch_status.processing_status == "ended":
        # Retrieve and save results
        results = generator.retrieve_results(batch_id)
        success = generator.save_batch_results(results)
        
        if success:
            print("✅ Batch results saved successfully!")
        else:
            print("❌ Failed to save batch results!")

def example_5_specific_elements():
    """Example 5: Generate storylines for governors with specific elements"""
    logging.basicConfig(level=logging.INFO)
    
    generator = BatchStorylineGenerator()
    
    # Define governors by element (example categorization)
    fire_governors = ["VALGARS", "DOAGNIS", "ZAMFRES"]
    water_governors = ["ABRIOND", "DIALOIA", "PACASNA"] 
    air_governors = ["OCCODON", "THOTANP", "NOCAMAL"]
    earth_governors = ["POTHNIR", "SAMAPHA", "VIROOLI"]
    
    # Process fire governors first
    print("🔥 Processing Fire Governors...")
    success = generator.generate_all_storylines(fire_governors)
    
    if success:
        print("✅ Fire governors completed!")
        
        # Then process water governors
        print("🌊 Processing Water Governors...")
        success = generator.generate_all_storylines(water_governors)
        
        if success:
            print("✅ Water governors completed!")

if __name__ == "__main__":
    print("📚 Batch Storyline Generator Examples")
    print("=" * 50)
    
    print("\n1. Test Batch (3 governors)")
    example_1_test_batch()
    
    print("\n2. Full Batch (all governors)")
    # example_2_all_governors()  # Uncomment to run
    
    print("\n3. Chunked Processing")
    # example_3_chunked_processing()  # Uncomment to run
    
    print("\n4. Monitor Existing Batch")
    # example_4_monitor_only()  # Uncomment to run
    
    print("\n5. Element-Specific Processing")
    # example_5_specific_elements()  # Uncomment to run 