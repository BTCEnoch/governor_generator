import { 
  KnowledgeEntry, 
  KnowledgeIndex, 
  SearchOptions, 
  SearchResult, 
  ValidationResult,
  ValidationError,
  ValidationErrorCode,
  KnowledgeStats,
  Reference,
  TraditionType
} from './types';

import { Logger } from '../utils/logger';

export class KnowledgeService {
  private entries: Map<string, KnowledgeEntry>;
  private index: KnowledgeIndex;
  private logger: Logger;

  constructor(logger: Logger) {
    this.entries = new Map();
    this.index = {
      byTradition: new Map(),
      byTag: new Map(),
      byReference: new Map(),
      crossRefGraph: new Map()
    };
    this.logger = logger;
  }

  private validateEntry(entry: KnowledgeEntry): ValidationResult {
    const errors: ValidationError[] = [];
    
    // Check content length (500-1000 words)
    const wordCount = entry.content.split(/\s+/).length;
    if (wordCount < 500 || wordCount > 1000) {
      errors.push({
        field: 'content',
        message: `Content must be between 500-1000 words. Current: ${wordCount}`,
        code: ValidationErrorCode.CONTENT_LENGTH
      });
    }

    // Check tags (minimum 3)
    if (!entry.tags || entry.tags.length < 3) {
      errors.push({
        field: 'tags',
        message: 'Entry must have at least 3 tags',
        code: ValidationErrorCode.INSUFFICIENT_TAGS
      });
    }

    // Validate references
    if (!entry.references || !entry.references.every(this.isValidReference)) {
      errors.push({
        field: 'references',
        message: 'Each reference must have source and citation',
        code: ValidationErrorCode.INVALID_REFERENCE
      });
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  private isValidReference(ref: Reference): boolean {
    return Boolean(ref.source && ref.citation);
  }

  private updateIndices(entry: KnowledgeEntry): void {
    // Update tradition index
    let traditionEntries = this.index.byTradition.get(entry.tradition) || [];
    traditionEntries = [...traditionEntries, entry.id];
    this.index.byTradition.set(entry.tradition, traditionEntries);

    // Update tag index
    entry.tags.forEach(tag => {
      let tagEntries = this.index.byTag.get(tag) || [];
      tagEntries = [...tagEntries, entry.id];
      this.index.byTag.set(tag, tagEntries);
    });

    // Update reference index
    entry.references.forEach(ref => {
      let refEntries = this.index.byReference.get(ref.source) || [];
      refEntries = [...refEntries, entry.id];
      this.index.byReference.set(ref.source, refEntries);
    });

    // Update cross-reference graph
    entry.crossReferences.forEach(crossRef => {
      let crossRefs = this.index.crossRefGraph.get(entry.id) || [];
      crossRefs = [...crossRefs, crossRef];
      this.index.crossRefGraph.set(entry.id, crossRefs);
    });
  }

  async addEntry(entry: KnowledgeEntry): Promise<ValidationResult> {
    this.logger.info(`Adding knowledge entry: ${entry.id}`);
    
    // Validate entry
    const validation = this.validateEntry(entry);
    if (!validation.isValid) {
      this.logger.error(`Validation failed for entry ${entry.id}`, validation.errors);
      return validation;
    }

    // Add to entries map
    this.entries.set(entry.id, entry);

    // Update indices
    this.updateIndices(entry);

    return validation;
  }

  async search(options: SearchOptions): Promise<SearchResult> {
    this.logger.info('Performing knowledge search', options);

    let matchingIds = new Set<string>();

    // Filter by tradition
    if (options.tradition) {
      const traditionEntries = this.index.byTradition.get(options.tradition) || [];
      matchingIds = new Set(traditionEntries);
    }

    // Filter by tags
    if (options.tags && options.tags.length > 0) {
      const tagEntries = options.tags.map(tag => this.index.byTag.get(tag) || []);
      const tagMatches = tagEntries.reduce((acc, curr) => {
        return acc.filter(id => curr.includes(id));
      }, Array.from(matchingIds.size ? matchingIds : this.entries.keys()));
      matchingIds = new Set(tagMatches);
    }

    // If no filters applied, use all entries
    if (!options.tradition && (!options.tags || options.tags.length === 0)) {
      matchingIds = new Set(Array.from(this.entries.keys()));
    }

    // Convert to array and sort by ID for consistent ordering
    let entries = Array.from(matchingIds)
      .sort()
      .map(id => this.entries.get(id))
      .filter(Boolean) as KnowledgeEntry[];

    const total = entries.length;
    
    // Apply pagination
    if (typeof options.offset === 'number' && typeof options.limit === 'number') {
      entries = entries.slice(options.offset, options.offset + options.limit);
    }

    // Remove content if not requested
    if (options.includeContent === false) {
      entries = entries.map(entry => ({
        ...entry,
        content: ''
      }));
    }

    return {
      entries,
      total,
      hasMore: total > (options.offset || 0) + entries.length
    };
  }

  async getStats(): Promise<KnowledgeStats> {
    const totalEntries = this.entries.size;
    const entriesByTradition = new Map<TraditionType, number>();
    const tagCounts = new Map<string, number>();

    // Calculate tradition counts and tag frequencies
    for (const entry of this.entries.values()) {
      // Count by tradition
      const traditionCount = entriesByTradition.get(entry.tradition) || 0;
      entriesByTradition.set(entry.tradition, traditionCount + 1);

      // Count tags
      entry.tags.forEach(tag => {
        const tagCount = tagCounts.get(tag) || 0;
        tagCounts.set(tag, tagCount + 1);
      });
    }

    // Sort tags by frequency
    const popularTags = Array.from(tagCounts.entries())
      .map(([tag, count]) => ({ tag, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10);

    return {
      totalEntries,
      entriesByTradition,
      totalTags: tagCounts.size,
      popularTags
    };
  }
} 