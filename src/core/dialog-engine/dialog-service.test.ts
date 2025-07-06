import { DialogService } from './dialog-service';
import { Logger, LogLevel } from '../utils/logger';
import { KnowledgeService } from '../knowledge-base/knowledge-service';
import { DialogContext, PlayerState } from './types';

describe('DialogService', () => {
  let service: DialogService;
  let logger: Logger;
  let knowledgeService: KnowledgeService;

  beforeEach(() => {
    logger = new Logger('test', LogLevel.DEBUG);
    knowledgeService = new KnowledgeService(logger);
    service = new DialogService(logger, knowledgeService);
  });

  const createMockContext = (): DialogContext => {
    const playerState: PlayerState = {
      id: 'player-1',
      reputation: 50,
      energy: 100,
      completedQuests: [],
      inventory: [],
      skills: new Map(),
      lastInteraction: Date.now()
    };

    return {
      governorId: 'gov-1',
      playerState,
      sessionId: 'session-1',
      timestamp: Date.now(),
      previousMessages: [],
      activeQuests: [],
      unlockedContent: []
    };
  };

  describe('processMessage', () => {
    it('should process a message and return a valid response', async () => {
      const context = createMockContext();
      const message = "Tell me about the Enochian Governors";

      const response = await service.processMessage(message, context);

      expect(response.message).toBeDefined();
      expect(response.message.content).toBeTruthy();
      expect(response.message.role).toBe('governor');
      expect(response.message.intent).toBeDefined();
      expect(response.message.sentiment).toBeDefined();
      expect(response.stateChanges).toBeDefined();
    });

    it('should update the session context', async () => {
      const context = createMockContext();
      const message = "Tell me about sacred wisdom";

      await service.processMessage(message, context);

      expect(context.previousMessages).toHaveLength(2); // Player message + Governor response
      expect(context.previousMessages[0].role).toBe('player');
      expect(context.previousMessages[1].role).toBe('governor');
    });

    it('should reject invalid context', async () => {
      const invalidContext = {
        // Missing required fields
        sessionId: 'session-1',
        timestamp: Date.now()
      } as unknown as DialogContext;

      await expect(
        service.processMessage("Hello", invalidContext)
      ).rejects.toThrow('Invalid dialog context');
    });

    it('should include state changes in response', async () => {
      const context = createMockContext();
      const message = "I seek to learn";

      const response = await service.processMessage(message, context);

      expect(response.stateChanges.reputationDelta).toBeDefined();
      expect(response.stateChanges.energyDelta).toBeDefined();
      expect(Array.isArray(response.stateChanges.questUpdates)).toBe(true);
    });
  });

  describe('getStats', () => {
    beforeEach(async () => {
      // Add some test sessions
      const context1 = createMockContext();
      const context2 = createMockContext();
      context2.sessionId = 'session-2';
      context2.playerState.id = 'player-2';

      await service.processMessage("Tell me about magic", context1);
      await service.processMessage("What are the mysteries?", context2);
    });

    it('should calculate correct session statistics', async () => {
      const stats = await service.getStats();

      expect(stats.totalSessions).toBe(2);
      expect(stats.activeUsers).toBe(2);
      expect(stats.averageSessionLength).toBe(2); // 2 messages per session
    });

    it('should identify popular intents', async () => {
      const stats = await service.getStats();

      expect(stats.popularIntents).toHaveLength(1); // Only one intent type in mock data
      expect(stats.popularIntents[0].intent).toBe('query_knowledge');
      expect(stats.popularIntents[0].count).toBe(2);
    });

    it('should track quest completion', async () => {
      const context = createMockContext();
      context.playerState.completedQuests = ['quest-1', 'quest-2'];
      await service.processMessage("I completed the quest", context);

      const stats = await service.getStats();
      expect(Object.keys(stats.questCompletion)).toHaveLength(2);
    });

    it('should calculate average reputation', async () => {
      const stats = await service.getStats();
      expect(stats.averageReputation).toBe(50); // Default reputation in mock data
    });
  });
}); 