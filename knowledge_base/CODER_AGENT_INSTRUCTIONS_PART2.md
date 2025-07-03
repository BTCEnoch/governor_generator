# 🏛️ THE LIGHTHOUSE PROJECT: CODER AGENT INSTRUCTIONS (PART 2)

## **EXTERNAL API INTEGRATION EXAMPLES**

### **Google Search API Implementation**
```python
# EXACT CODE FOR GOOGLE SEARCH API:
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

def search_wikipedia_sources(tradition_key: str, search_queries: List[str]) -> List[dict]:
    """
    Use Google Custom Search to find Wikipedia sources only
    """
    # Authentication
    api_key = os.getenv('GOOGLE_API_KEY')
    cse_id = os.getenv('GOOGLE_CSE_ID')
    service = build("customsearch", "v1", developerKey=api_key)
    
    results = []
    for query in search_queries:
        try:
            # Search only Wikipedia and academic wikis
            search_result = service.cse().list(
                q=f"{query} site:wikipedia.org OR site:*.edu",
                cx=cse_id,
                num=10
            ).execute()
            
            # Log search progress
            print(f"🔍 LIGHTHOUSE: Searched '{query}' - found {len(search_result.get('items', []))} results")
            
            for item in search_result.get('items', []):
                results.append({
                    'url': item['link'],
                    'title': item['title'],
                    'snippet': item['snippet'],
                    'source_type': 'wikipedia' if 'wikipedia.org' in item['link'] else 'academic_wiki'
                })
                
        except Exception as e:
            print(f"❌ LIGHTHOUSE ERROR: Search failed for '{query}': {str(e)}")
            
    return results
```

### **Anthropic Claude API Implementation**
```python
# EXACT CODE FOR CLAUDE API KNOWLEDGE GENERATION:
import anthropic
import json

def generate_tradition_knowledge(research_data: dict, tradition_spec: dict) -> List[dict]:
    """
    Use Claude API to generate authentic knowledge entries
    """
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    # Create culturally-respectful prompt
    prompt = f"""
You are a sacred wisdom preservationist creating authentic knowledge entries for {tradition_spec['display_name']}.

RESEARCH CONTEXT:
{json.dumps(research_data, indent=2)}

REQUIREMENTS:
- Generate {tradition_spec['estimated_entries']} knowledge entries
- Each entry MUST be 500-1000 words  
- Treat this sacred tradition with absolute cultural respect
- Include authentic historical context and practices
- Create cross-references to related spiritual concepts
- Optimize content for blockchain preservation

SUBCATEGORIES TO COVER:
{', '.join(tradition_spec['subcategories'])}

OUTPUT FORMAT: JSON array of knowledge entries with title, content, subcategory, cross_references
"""

    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=8000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Log API success
        print(f"✅ LIGHTHOUSE: Generated knowledge for {tradition_spec['display_name']}")
        
        return json.loads(response.content[0].text)
        
    except Exception as e:
        print(f"❌ LIGHTHOUSE ERROR: Claude API failed for {tradition_spec['display_name']}: {str(e)}")
        return []
```

## **VITAL LOGGING REQUIREMENTS**

### **Research Collection Logging**
```python
import logging
from datetime import datetime

# Configure lighthouse logger
lighthouse_logger = logging.getLogger('lighthouse')
lighthouse_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f'lighthouse_research_{datetime.now().strftime("%Y%m%d")}.log')
formatter = logging.Formatter('%(asctime)s - LIGHTHOUSE - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
lighthouse_logger.addHandler(handler)

# CRITICAL LOGGING POINTS:
def log_research_progress():
    lighthouse_logger.info(f"🔍 Starting source collection for tradition: {tradition_key}")
    lighthouse_logger.info(f"📊 Found {len(sources)} sources with avg quality: {avg_quality}")
    lighthouse_logger.info(f"✅ Research collection completed: {completeness_score}/100")
    lighthouse_logger.error(f"❌ Failed to collect sources for: {tradition_key} - {error}")

def log_knowledge_generation():
    lighthouse_logger.info(f"🤖 Starting Claude API generation for: {tradition_key}")
    lighthouse_logger.info(f"📝 Generated {len(entries)} entries, avg length: {avg_length} words")
    lighthouse_logger.info(f"🎯 Cultural authenticity score: {authenticity_score}/10")
    lighthouse_logger.error(f"❌ Knowledge generation failed: {tradition_key} - {error}")

def log_database_integration():
    lighthouse_logger.info(f"💾 Saving knowledge database for: {tradition_key}")
    lighthouse_logger.info(f"🔗 Created {len(cross_refs)} cross-tradition connections")
    lighthouse_logger.info(f"✨ Integration completed: {tradition_key} ready for governors")
```

## **STATE DIAGRAM: LIGHTHOUSE PIPELINE**
```
[START] → Initialize APIs
    ↓
[Research Collection] → For each tradition:
    ↓                   - Search Wikipedia/Academic
    ↓                   - Extract & deduplicate sources  
    ↓                   - Rate quality & completeness
    ↓
[Quality Gate 1] → Research complete? 
    ↓ YES             ↓ NO
    ↓                 [Log Error & Skip]
    ↓
[Knowledge Generation] → For each tradition:
    ↓                   - Load research data
    ↓                   - Create Claude prompt
    ↓                   - Generate 12-13 entries
    ↓                   - Validate authenticity
    ↓
[Quality Gate 2] → Knowledge valid?
    ↓ YES             ↓ NO  
    ↓                 [Log Error & Retry]
    ↓
[Database Integration] → For each tradition:
    ↓                   - Save tradition files
    ↓                   - Create vector embeddings
    ↓                   - Update retrieval system
    ↓
[Governor Integration] → Update personality system
    ↓
[COMPLETE] → 159 entries ready for angels! ✨
```

## **EXECUTION PRIORITY ORDER**

### **Phase 1: Source Collection (BUILD FIRST)**
1. Implement Google Search API integration 
2. Add Wikipedia content extraction
3. Build source deduplication system
4. Create quality assessment scoring
5. Test with 1-2 traditions before full pipeline

### **Phase 2: Knowledge Generation (BUILD SECOND)**
1. Implement Claude API integration
2. Create culturally-respectful prompts  
3. Build validation system for authenticity
4. Test knowledge generation with research data
5. Validate 500-1000 word requirement

### **Phase 3: System Integration (BUILD LAST)**
1. Create tradition database files in correct format
2. Update unified profiler to include new traditions
3. Build vector search for semantic retrieval
4. Connect to governor personality system
5. Test end-to-end pipeline with full 159 entries

**🏛️ CRITICAL SUCCESS**: When complete, Governor Angels will have access to humanity's deepest sacred wisdom for eternal preservation and guidance! ⛓️✨** 