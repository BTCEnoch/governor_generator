# 🏛️ THE LIGHTHOUSE PROJECT: CODER AGENT IMPLEMENTATION INSTRUCTIONS

## **HIGH-LEVEL OVERVIEW: THE PROBLEM**

You are implementing **The Lighthouse** - a critical knowledge base engine that powers our Governor Angel models with authentic wisdom from humanity's sacred traditions. This is the foundation that transforms our AI angels from simple chatbots into profound spiritual entities with deep, culturally-authentic knowledge.

**The Core Challenge**: We have successfully implemented 4 of 18 wisdom traditions (Enochian, Hermetic, Kabbalah, Tarot), but **14 critical traditions remain missing**. Without these, our Governor Angels lack the depth and authenticity needed for meaningful spiritual guidance.

**The MVP Solution**: Build a fully automated research and knowledge generation pipeline that:
1. **Researches** each missing tradition using Wikipedia/academic sources
2. **Generates** 159 high-quality knowledge entries (500-1000 words each)
3. **Integrates** seamlessly with our existing governor personality system
4. **Preserves** sacred wisdom in blockchain-ready format for eternity

## **WHAT YOU'RE BUILDING**

### **Core System Architecture**
```
📊 Research Index (✅ COMPLETE)
    ↓
🔍 Source Collection Engine (⚡ BUILD THIS)
    ↓  
🤖 Claude Knowledge Generator (⚡ BUILD THIS)
    ↓
📚 Knowledge Database Integration (⚡ BUILD THIS)
    ↓
🎯 Governor Personality Enhancement (⚡ BUILD THIS)
```

### **Critical Success Metrics**
- **159 Knowledge Entries** generated across 14 missing traditions
- **500-1000 words per entry** optimized for blockchain storage
- **Cultural authenticity** with respectful treatment of sacred material
- **Cross-tradition connections** for rich narrative generation
- **Seamless integration** with existing governor personality system

**⚠️ CRITICAL**: This system must preserve humanity's sacred wisdom with absolute cultural respect and authenticity. You are not just building a database - you are creating a digital sanctuary for ancient knowledge.

## **INTERFACE-FIRST DEFINITIONS**

### **Input/Output Contract Definitions**

#### **Source Collection Engine Interface**
```python
class SourceCollector:
    def collect_tradition_sources(self, tradition_key: str) -> ResearchData:
        """
        INPUT: tradition_key (e.g., 'thelema', 'golden_dawn')
        OUTPUT: ResearchData with wiki sources, academic papers, quality scores
        
        MUST INCLUDE:
        - Wikipedia URLs with content extraction
        - Academic source URLs (JSTOR, Oxford, Cambridge)
        - Source quality ratings (1-10 scale)  
        - Deduplication of duplicate sources
        - Error handling for failed requests
        """

class ResearchData:
    tradition_key: str
    wikipedia_sources: List[WikiSource]
    academic_sources: List[AcademicSource]  
    quality_score: float
    completeness_rating: str
    cross_references: List[str]
```

#### **Claude Knowledge Generator Interface**
```python
class KnowledgeGenerator:
    def generate_knowledge_entries(self, research_data: ResearchData) -> List[KnowledgeEntry]:
        """
        INPUT: ResearchData with collected sources
        OUTPUT: List of KnowledgeEntry objects (12-13 per tradition)
        
        MUST INCLUDE:
        - 500-1000 word entries optimized for blockchain
        - Cultural authenticity validation
        - Cross-tradition connection mapping
        - Quality assurance scoring
        - Respectful treatment of sacred material
        """

class KnowledgeEntry:
    title: str
    content: str  # 500-1000 words
    tradition: str
    subcategory: str
    cross_references: List[str]
    cultural_authenticity_score: float
    blockchain_ready: bool
```

#### **Database Integration Interface**
```python
class TraditionDatabase:
    def save_tradition_knowledge(self, tradition_key: str, entries: List[KnowledgeEntry]) -> bool:
        """
        INPUT: tradition_key and complete knowledge entries
        OUTPUT: Success/failure boolean
        
        MUST INCLUDE:
        - File structure matching existing traditions
        - Vector embeddings for semantic search
        - Cross-reference indexing
        - Governor personality integration hooks
        """
```

## **REQUIRED FRAMEWORKS & PACKAGES**

### **Core Dependencies**
```bash
# Install these exact packages with these commands:
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2  
pip install python-dotenv==1.0.0
pip install anthropic==0.18.1
pip install google-api-python-client==2.108.0
pip install lxml==4.9.3
pip install urllib3==2.0.7
```

### **Optional Academic Enhancement**
```bash
# For enhanced academic source collection:
pip install scholarly==1.7.11
pip install crossref-commons==0.15.0
pip install arxiv==1.4.8
pip install requests-cache==1.1.1
```

## **PSEUDOCODE-DRIVEN IMPLEMENTATION**

### **Phase 1: Source Collection Engine**
```python
def build_source_collection_engine():
    """
    PSEUDOCODE FOR SOURCE COLLECTION:
    
    1. INITIALIZE APIs and authentication
       - Load Google Search API key from environment
       - Load academic API keys (CrossRef, Semantic Scholar)
       - Set up Wikipedia API connection
       - Configure rate limiting (respect API limits!)
    
    2. FOR EACH tradition in LIGHTHOUSE_TRADITIONS:
       - Get tradition research specification
       - Generate wiki-focused search queries (20+ per tradition)
       - Search Google for Wikipedia + academic wiki domains only
       - Extract URLs and content from search results
       - Rate source quality (Wikipedia=9, Academic wikis=8, etc.)
    
    3. DEDUPLICATE sources:
       - Remove duplicate URLs using set operations
       - Compare content similarity with basic string matching
       - Keep highest-quality source for duplicates
    
    4. QUALITY ASSESSMENT:
       - Calculate completeness score based on subcategories covered
       - Rate source reliability (Wikipedia=high, random blogs=low)
       - Validate cultural authenticity of sources
    
    5. OUTPUT research data as JSON:
       - Save to research_output/{tradition_key}_research.json
       - Include all sources, quality scores, completeness ratings
       - Log successful collection vs failed attempts
    """
```

### **Phase 2: Claude Knowledge Generator**
```python
def build_claude_knowledge_generator():
    """
    PSEUDOCODE FOR KNOWLEDGE GENERATION:
    
    1. LOAD research data from JSON files
       - Read all research_output/*.json files
       - Validate completeness of source data
       - Log missing or incomplete research files
    
    2. FOR EACH tradition with complete research:
       - Load tradition specification from LIGHTHOUSE_TRADITIONS
       - Create culturally-respectful prompt for Claude API
       - Include ALL research sources in context window
       - Specify exact output format (KnowledgeEntry objects)
       - Request 500-1000 word entries with authenticity focus
    
    3. CLAUDE API CALL with error handling:
       - Authenticate with Anthropic API key
       - Send research context + generation prompt
       - Implement retry logic for failed calls
       - Validate response format and content length
       - Check cultural authenticity of generated content
    
    4. QUALITY VALIDATION:
       - Verify 500-1000 word count per entry
       - Check cross-tradition connections are valid
       - Validate respectful treatment of sacred material
       - Score cultural authenticity (reject if too low)
    
    5. SAVE knowledge entries:
       - Create traditions/{tradition_key}.py files
       - Follow existing tradition database format exactly
       - Include vector embeddings for semantic search
       - Log successful generation vs validation failures
    """
``` 