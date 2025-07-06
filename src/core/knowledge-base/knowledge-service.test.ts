import { KnowledgeService } from './knowledge-service';
import { Logger, LogLevel } from '../utils/logger';
import { KnowledgeEntry, ValidationErrorCode } from './types';

describe('KnowledgeService', () => {
  let service: KnowledgeService;
  let logger: Logger;

  beforeEach(() => {
    logger = new Logger('test', LogLevel.DEBUG);
    service = new KnowledgeService(logger);
  });

  const createValidEntry = (): KnowledgeEntry => ({
    id: 'test-1',
    tradition: 'enochian',
    title: 'Test Entry',
    content: 'This is a test entry with sufficient words to meet the minimum requirement. '.repeat(50), // 600 words
    tags: ['test', 'enochian', 'magic'],
    references: [
      {
        source: 'Test Source',
        type: 'academic',
        citation: 'Test Citation'
      }
    ],
    crossReferences: [],
    lastModified: Date.now(),
    version: 1
  });

  describe('addEntry', () => {
    it('should successfully add a valid entry', async () => {
      const entry = createValidEntry();
      const result = await service.addEntry(entry);
      
      expect(result.isValid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should reject entry with insufficient content', async () => {
      const entry = {
        ...createValidEntry(),
        content: 'Too short'
      };
      const result = await service.addEntry(entry);

      expect(result.isValid).toBe(false);
      expect(result.errors[0].code).toBe(ValidationErrorCode.CONTENT_LENGTH);
    });

    it('should reject entry with insufficient tags', async () => {
      const entry = {
        ...createValidEntry(),
        content: 'This is a test entry with sufficient words to meet the minimum requirement. '.repeat(50),
        tags: ['test']
      };
      const result = await service.addEntry(entry);

      expect(result.isValid).toBe(false);
      expect(result.errors[0].code).toBe(ValidationErrorCode.INSUFFICIENT_TAGS);
    });

    it('should reject entry with invalid references', async () => {
      const entry = {
        ...createValidEntry(),
        content: 'This is a test entry with sufficient words to meet the minimum requirement. '.repeat(50),
        references: [{ type: 'academic' } as any]
      };
      const result = await service.addEntry(entry);

      expect(result.isValid).toBe(false);
      expect(result.errors[0].code).toBe(ValidationErrorCode.INVALID_REFERENCE);
    });
  });

  describe('search', () => {
    beforeEach(async () => {
      // Add test entries
      await service.addEntry({
        ...createValidEntry(),
        id: 'entry-1',
        tradition: 'kabbalah',
        tags: ['test', 'kabbalah', 'tree-of-life']
      });

      await service.addEntry({
        ...createValidEntry(),
        id: 'entry-2',
        tradition: 'kabbalah',
        tags: ['test', 'kabbalah', 'sefirot']
      });
    });

    it('should filter by tradition', async () => {
      const result = await service.search({ tradition: 'kabbalah' });
      
      expect(result.entries).toHaveLength(2);
      expect(result.entries[0].id).toBe('entry-1');
      expect(result.entries[1].id).toBe('entry-2');
    });

    it('should filter by tags', async () => {
      const result = await service.search({
        tags: ['kabbalah', 'tree-of-life']
      });
      
      expect(result.entries).toHaveLength(1);
      expect(result.entries[0].id).toBe('entry-1');
    });

    it('should paginate results', async () => {
      const result = await service.search({
        offset: 1,
        limit: 1
      });
      
      expect(result.entries).toHaveLength(1);
      expect(result.total).toBe(2);
      expect(result.hasMore).toBe(false);
    });

    it('should exclude content when not requested', async () => {
      const result = await service.search({
        includeContent: false
      });
      
      expect(result.entries[0].content).toBe('');
      expect(result.entries[1].content).toBe('');
    });
  });

  describe('getStats', () => {
    beforeEach(async () => {
      // Add test entries
      await service.addEntry({
        ...createValidEntry(),
        id: 'stats-1',
        tradition: 'kabbalah',
        tags: ['test', 'kabbalah', 'tree-of-life']
      });

      await service.addEntry({
        ...createValidEntry(),
        id: 'stats-2',
        tradition: 'kabbalah',
        tags: ['test', 'kabbalah', 'sefirot']
      });

      await service.addEntry({
        ...createValidEntry(),
        id: 'stats-3',
        tradition: 'enochian',
        tags: ['test', 'enochian', 'magic']
      });
    });

    it('should calculate correct statistics', async () => {
      const stats = await service.getStats();
      
      expect(stats.totalEntries).toBe(3);
      expect(stats.entriesByTradition.get('kabbalah')).toBe(2);
      expect(stats.entriesByTradition.get('enochian')).toBe(1);
      expect(stats.totalTags).toBe(6); // unique tags
    });

    it('should identify popular tags', async () => {
      const stats = await service.getStats();
      
      expect(stats.popularTags[0].tag).toBe('test'); // most common tag
      expect(stats.popularTags[0].count).toBe(3); // appears in all entries
      expect(stats.popularTags[1].tag).toBe('kabbalah'); // second most common
      expect(stats.popularTags[1].count).toBe(2);
    });
  });
}); 