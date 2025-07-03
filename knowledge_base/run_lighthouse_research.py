#!/usr/bin/env python3
"""
🏛️ LIGHTHOUSE RESEARCH EXECUTION SCRIPT

Simple script to run the Lighthouse research automation system.
This demonstrates how to use the research orchestration for The Lighthouse project.
"""

import asyncio
import os
from lighthouse_research_index import (
    execute_lighthouse_research_pipeline,
    print_tradition_source_index,
    LighthouseResearchOrchestrator,
    ClaudeAPIIntegration,
    LIGHTHOUSE_TRADITIONS
)

def print_usage_instructions():
    """
    Print instructions for using the Lighthouse research system
    """
    print("\n🏛️ THE LIGHTHOUSE RESEARCH AUTOMATION SYSTEM")
    print("=" * 60)
    print("\nThis system automates research collection for all 14 missing wisdom traditions.")
    print("It integrates Google Search API, Academic API, and wiki parsing.")
    print("\n📋 RESEARCH BLOCKS:")
    print("   Block 1: Critical Foundations (Golden Dawn, Thelema, Egyptian Magic)")
    print("   Block 2: Eastern Wisdom (Taoism, I-Ching, Kuji-kiri)")  
    print("   Block 3: Classical & Gnostic (Classical Philosophy, Gnostic Traditions)")
    print("   Block 4: Divination & Sacred (Tarot Knowledge, Sacred Geometry)")
    print("   Block 5: Modern & Experimental (Chaos Magic, Norse Traditions)")
    print("   Block 6: Mystical Traditions (Sufi Mysticism, Celtic Druidic)")
    
    print("\n🔧 SETUP REQUIRED:")
    print("   1. Set GOOGLE_SEARCH_API_KEY environment variable")
    print("   2. SEMANTIC_SCHOLAR_API - Uses free Semantic Scholar API (no key needed)") 
    print("   3. Set ANTHROPIC_API_KEY for Claude integration")
    
    print("\n🚀 USAGE:")
    print("   python run_lighthouse_research.py --mode [demo|research|full]")
    print("   python run_lighthouse_research.py --tradition [tradition_name]")
    print("   python run_lighthouse_research.py --block [block_id]")

async def demo_mode():
    """
    Demonstration mode - shows what the system will do without API calls
    """
    print("\n🎭 DEMO MODE: Lighthouse Research Preview")
    print("-" * 50)
    
    # Show tradition source index
    print_tradition_source_index()
    
    # Initialize demo orchestrator with Semantic Scholar
    orchestrator = LighthouseResearchOrchestrator(
        google_api_key="demo_google_key",
        use_semantic_scholar=True
    )
    
    # Show research blocks
    blocks = orchestrator.get_research_blocks()
    
    print(f"\n📋 Research blocks created: {len(blocks)}")
    for block in blocks:
        print(f"   {block['block_id']}: {block['focus']}")
        print(f"      Traditions: {', '.join(block['traditions'])}")
        print(f"      Priority: {block['priority']}")
        print()

async def research_single_tradition(tradition_name: str):
    """
    Research a single tradition for testing
    """
    if tradition_name not in LIGHTHOUSE_TRADITIONS:
        print(f"❌ Unknown tradition: {tradition_name}")
        print(f"Available: {', '.join(LIGHTHOUSE_TRADITIONS.keys())}")
        return
    
    print(f"\n🔍 RESEARCHING SINGLE TRADITION: {tradition_name}")
    print("-" * 50)
    
    # Get API keys from environment
    google_key = os.getenv("GOOGLE_SEARCH_API_KEY", "demo_key")
    
    orchestrator = LighthouseResearchOrchestrator(google_key, use_semantic_scholar=True)
    
    # Generate search queries for this tradition
    queries = orchestrator.generate_enhanced_search_queries(tradition_name)
    
    tradition_data = LIGHTHOUSE_TRADITIONS[tradition_name]
    print(f"\n📚 {tradition_data.display_name}")
    print(f"Priority: {tradition_data.priority.value}")
    print(f"Complexity: {tradition_data.complexity.value}")
    print(f"Estimated Entries: {tradition_data.estimated_entries}")
    
    print(f"\n🔍 Generated {len(queries)} search queries:")
    for i, query in enumerate(queries[:10], 1):
        print(f"   {i:2d}. {query}")
    
    print(f"\n📖 Primary Sources ({len(tradition_data.primary_sources)}):")
    for source in tradition_data.primary_sources:
        print(f"   • {source.title}")
        print(f"     {source.url}")
        print(f"     Quality: {source.quality} | Type: {source.type}")
        print()

async def full_research_pipeline():
    """
    Execute the complete research pipeline with real API calls
    """
    print("\n🚀 FULL RESEARCH PIPELINE EXECUTION")
    print("-" * 50)
    
    # Check for required API keys (Semantic Scholar is free, no key needed)
    required_keys = ["GOOGLE_SEARCH_API_KEY", "ANTHROPIC_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f"❌ Missing required environment variables: {', '.join(missing_keys)}")
        print("Please set these before running the full pipeline.")
        print("Note: Semantic Scholar API is free and requires no API key!")
        return
    
    # Execute complete pipeline
    results, summary = await execute_lighthouse_research_pipeline()
    
    print("\n✅ RESEARCH PIPELINE COMPLETE!")
    print(f"   Traditions researched: {summary['total_traditions_researched']}")
    print(f"   Sources collected: {summary['total_sources_collected']}")
    print(f"   Knowledge entries needed: {summary['estimated_knowledge_entries']}")
    
    # Show next steps
    print("\n📝 NEXT STEPS:")
    print("   1. Review generated JSON files in knowledge_base/")
    print("   2. Use Claude API to generate knowledge entries")
    print("   3. Create tradition database files")
    print("   4. Integrate with unified knowledge retriever")

if __name__ == "__main__":
    import sys
    
    # Simple argument parsing
    if len(sys.argv) == 1:
        print_usage_instructions()
        sys.exit(0)
    
    mode = "demo"
    tradition = None
    
    # Parse arguments
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg.startswith("--mode="):
            mode = arg.split("=")[1]
        elif arg.startswith("--tradition="):
            tradition = arg.split("=")[1]
        elif arg == "--mode" and i < len(sys.argv) - 1:
            mode = sys.argv[i + 1]
        elif arg == "--tradition" and i < len(sys.argv) - 1:
            tradition = sys.argv[i + 1]
    
    # Execute based on mode
    if mode == "demo":
        asyncio.run(demo_mode())
    elif mode == "research" and tradition:
        asyncio.run(research_single_tradition(tradition))
    elif mode == "full":
        asyncio.run(full_research_pipeline())
    else:
        print("❌ Invalid arguments. Use --mode=demo, --mode=full, or --mode=research --tradition=tradition_name")
        print_usage_instructions() 