# Knowledge Base Technical Specification

## Overview
The Lighthouse Knowledge Base is the core data repository for the Enochian Governor Generation system. It stores and manages mystical wisdom from 18 traditions, providing the foundation for governor personalities and game content.

## Data Structure

### Knowledge Entry Schema
```typescript
interface KnowledgeEntry {
  id: string;                    // Unique identifier
  tradition: TraditionType;      // One of 18 mystical traditions
  title: string;                 // Entry title (max 100 chars)
  content: string;               // Main content (500-1000 words)
  tags: string[];                // Categorization tags
  references: Reference[];       // Source citations
  crossReferences: string[];     // IDs of related entries
  lastModified: number;          // Unix timestamp
  version: number;               // Entry version
  blockchainMetadata?: {        // Optional blockchain storage info
    inscriptionId?: string;     // Bitcoin inscription ID if stored
    transactionId?: string;     // Bitcoin transaction ID
    blockHeight?: number;       // Block where data was inscribed
  }
}

interface Reference {
  source: string;               // Source title/name
  type: 'academic' | 'primary' | 'historical';
  citation: string;            // Formatted citation
  url?: string;               // Optional URL for digital sources
}

type TraditionType = 
  | 'enochian'
  | 'kabbalah'
  | 'hermeticism'
  | 'alchemy'
  | 'tarot'
  | 'astrology'
  | 'numerology'
  | 'gematria'
  | 'sacred_geometry'
  | 'egyptian'
  | 'greek'
  | 'celtic'
  | 'norse'
  | 'vedic'
  | 'buddhist'
  | 'taoism'
  | 'sufism'
  | 'shamanic';
```

### Validation Rules
1. Content length must be 500-1000 words
2. Each entry must have at least 2 tags
3. Cross-references must point to valid entry IDs
4. References must include at least one primary source
5. Titles must be unique within a tradition
6. Content must pass cultural sensitivity check

## Storage and Compression

### Compression Strategy
1. Text content uses DEFLATE algorithm
2. JSON structure preserved for query efficiency
3. Binary compression for non-text assets
4. Chunking threshold: 100KB per block

### Blockchain Storage
1. Content split into 100KB chunks
2. Each chunk inscribed as separate ordinal
3. Manifest tracks chunk ordering
4. Content hash stored with each chunk
5. TAP protocol references for game integration

## Search and Retrieval

### Index Structure
```typescript
interface KnowledgeIndex {
  byTradition: Map<TraditionType, string[]>;  // Tradition -> Entry IDs
  byTag: Map<string, string[]>;               // Tag -> Entry IDs
  byReference: Map<string, string[]>;         // Source -> Entry IDs
  crossRefGraph: Map<string, string[]>;       // Entry ID -> Related IDs
}
```

### Search Optimization
1. In-memory tag index
2. Pre-computed cross-reference graph
3. Cached frequent queries
4. Vector embeddings for semantic search
5. Incremental index updates

## Cross-Referencing System

### Reference Types
1. Direct references (explicit links)
2. Semantic connections (AI-detected)
3. Shared symbolism
4. Historical connections
5. Practical applications

### Validation Process
1. Check reference existence
2. Verify tradition compatibility
3. Validate semantic relevance
4. Update cross-reference graph
5. Maintain reference integrity

## API Interface

### Query Methods
```typescript
interface KnowledgeBaseAPI {
  // Basic CRUD
  getEntry(id: string): Promise<KnowledgeEntry>;
  addEntry(entry: KnowledgeEntry): Promise<string>;
  updateEntry(id: string, entry: Partial<KnowledgeEntry>): Promise<void>;
  deleteEntry(id: string): Promise<void>;

  // Search and Discovery
  searchByTradition(tradition: TraditionType): Promise<KnowledgeEntry[]>;
  searchByTags(tags: string[]): Promise<KnowledgeEntry[]>;
  findRelated(id: string): Promise<KnowledgeEntry[]>;
  semanticSearch(query: string): Promise<KnowledgeEntry[]>;

  // Blockchain Integration
  inscribeEntry(id: string): Promise<string>;  // Returns inscription ID
  verifyInscription(id: string): Promise<boolean>;
  syncFromChain(): Promise<void>;
}
```

## Error Handling

### Error Types
```typescript
enum KnowledgeBaseError {
  INVALID_ENTRY = 'INVALID_ENTRY',
  DUPLICATE_TITLE = 'DUPLICATE_TITLE',
  REFERENCE_NOT_FOUND = 'REFERENCE_NOT_FOUND',
  INSCRIPTION_FAILED = 'INSCRIPTION_FAILED',
  SYNC_ERROR = 'SYNC_ERROR',
  VALIDATION_ERROR = 'VALIDATION_ERROR'
}
```

### Recovery Procedures
1. Automatic retry for failed inscriptions
2. Local backup before chain operations
3. Conflict resolution for concurrent updates
4. Validation state recovery
5. Index rebuild capability

## Performance Requirements

### Response Times
- Read operations: < 100ms
- Write operations: < 500ms
- Search operations: < 200ms
- Blockchain ops: < 5s

### Scalability Targets
- Support 10,000+ entries
- Handle 100+ concurrent users
- Maintain 99.9% uptime
- Max 1GB local cache size
- 5MB max entry size

## Security Measures

### Data Integrity
1. SHA-256 hashing for entries
2. Digital signatures for updates
3. Blockchain verification
4. Audit trail logging
5. Version control

### Access Control
1. Read-only public access
2. Signed updates only
3. Multi-sig for critical changes
4. Rate limiting
5. DOS protection

## Testing Strategy

### Test Categories
1. Unit tests for CRUD operations
2. Integration tests for search
3. Blockchain sync tests
4. Performance benchmarks
5. Security penetration tests

### Test Coverage Requirements
- 95% code coverage
- All error paths tested
- Load testing to 2x scale
- Cross-platform verification
- Blockchain testnet validation 