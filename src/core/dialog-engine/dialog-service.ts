import {
  DialogContext,
  DialogMessage,
  DialogResponse,
  DialogOptions,
  IntentClassification,
  ResponseGeneration,
  DialogStats,
  PlayerState
} from './types';

import { Logger } from '../utils/logger';
import { KnowledgeService } from '../knowledge-base/knowledge-service';

export class DialogService {
  private sessions: Map<string, DialogContext>;
  private logger: Logger;
  private knowledgeService: KnowledgeService;

  constructor(logger: Logger, knowledgeService: KnowledgeService) {
    this.sessions = new Map();
    this.logger = logger;
    this.knowledgeService = knowledgeService;
  }

  private async classifyIntent(message: string, _context: DialogContext): Promise<IntentClassification> {
    this.logger.info(`Classifying intent for message: ${message.substring(0, 50)}...`);

    // TODO: Implement intent classification using an LLM
    // For now, return mock data
    return {
      intent: {
        primary: 'query_knowledge',
        confidence: 0.85,
        secondary: ['express_interest', 'seek_guidance'],
        entities: {
          topic: 'enochian_magic',
          subtopic: 'governors'
        }
      },
      sentiment: {
        score: 0.7,
        aspects: {
          respect: 0.8,
          wisdom: 0.6,
          devotion: 0.7
        }
      },
      confidence: 0.85
    };
  }

  private async generateResponse(
    intent: IntentClassification,
    _context: DialogContext,
    _options: DialogOptions = {}
  ): Promise<ResponseGeneration> {
    this.logger.info(`Generating response for intent: ${intent.intent.primary}`);

    // TODO: Implement response generation using an LLM
    // For now, return mock data
    return {
      content: "I sense your genuine interest in understanding the deeper mysteries. Let me share with you some wisdom about the Enochian Governors...",
      metadata: {
        generationStats: {
          promptTokens: 150,
          completionTokens: 50,
          totalTokens: 200,
          generationTime: 500
        }
      }
    };
  }

  private async updatePlayerState(
    state: PlayerState,
    response: DialogResponse
  ): Promise<PlayerState> {
    const {
      reputationDelta = 0,
      energyDelta = 0,
      addedItems = [],
      removedItems = [],
      questUpdates = []
    } = response.stateChanges;

    // Update basic stats
    state.reputation = Math.max(0, Math.min(100, state.reputation + reputationDelta));
    state.energy = Math.max(0, Math.min(100, state.energy + energyDelta));
    state.lastInteraction = Date.now();

    // Update inventory
    state.inventory = [
      ...state.inventory.filter(item => !removedItems.includes(item.id)),
      ...addedItems
    ];

    // Update quests
    const completedQuests = questUpdates
      .filter(update => update.completed)
      .map(update => update.questId);
    
    state.completedQuests = [...new Set([...state.completedQuests, ...completedQuests])];

    return state;
  }

  private validateContext(context: DialogContext): boolean {
    return Boolean(
      context &&
      context.governorId &&
      context.playerState &&
      context.sessionId &&
      Array.isArray(context.previousMessages)
    );
  }

  async processMessage(
    message: string,
    context: DialogContext,
    options: DialogOptions = {}
  ): Promise<DialogResponse> {
    if (!this.validateContext(context)) {
      throw new Error('Invalid dialog context');
    }

    this.logger.info(`Processing message for session ${context.sessionId}`);

    // Classify intent
    const classification = await this.classifyIntent(message, context);

    // Generate response
    const generation = await this.generateResponse(classification, context, options);

    // Create message
    const dialogMessage: DialogMessage = {
      id: `msg_${Date.now()}`,
      role: 'governor',
      content: generation.content,
      intent: classification.intent,
      sentiment: classification.sentiment,
      timestamp: Date.now()
    };

    // Create response with state changes
    const response: DialogResponse = {
      message: dialogMessage,
      stateChanges: {
        reputationDelta: 1, // Mock value
        energyDelta: -5, // Mock value
        questUpdates: [] // Mock value
      }
    };

    // Update session
    context.previousMessages.push({
      id: `msg_${Date.now()}_player`,
      role: 'player',
      content: message,
      timestamp: Date.now()
    });
    context.previousMessages.push(dialogMessage);

    // Store updated context
    this.sessions.set(context.sessionId, context);

    return response;
  }

  async getStats(): Promise<DialogStats> {
    const stats: DialogStats = {
      totalSessions: this.sessions.size,
      activeUsers: Array.from(this.sessions.values())
        .filter(ctx => Date.now() - ctx.playerState.lastInteraction < 3600000)
        .length,
      averageSessionLength: 0,
      popularIntents: [],
      questCompletion: {},
      averageReputation: 0,
      topRewards: []
    };

    let totalMessages = 0;
    const intentCounts = new Map<string, number>();
    const questCounts = new Map<string, number>();
    const rewardCounts = new Map<string, number>();
    let reputationSum = 0;

    // Analyze all sessions
    for (const context of this.sessions.values()) {
      totalMessages += context.previousMessages.length;
      reputationSum += context.playerState.reputation;

      // Count intents
      context.previousMessages
        .filter(msg => msg.intent)
        .forEach(msg => {
          const count = intentCounts.get(msg.intent!.primary) || 0;
          intentCounts.set(msg.intent!.primary, count + 1);
        });

      // Count completed quests
      context.playerState.completedQuests.forEach(questId => {
        const count = questCounts.get(questId) || 0;
        questCounts.set(questId, count + 1);
      });

      // Count rewards
      context.playerState.inventory.forEach(item => {
        const count = rewardCounts.get(item.id) || 0;
        rewardCounts.set(item.id, count + 1);
      });
    }

    // Calculate averages and sort collections
    stats.averageSessionLength = totalMessages / Math.max(1, this.sessions.size);
    stats.averageReputation = reputationSum / Math.max(1, this.sessions.size);

    // Sort and limit collections
    stats.popularIntents = Array.from(intentCounts.entries())
      .map(([intent, count]) => ({ intent, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10);

    stats.questCompletion = Object.fromEntries(questCounts);

    stats.topRewards = Array.from(rewardCounts.entries())
      .map(([item, count]) => ({ item, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10);

    return stats;
  }
} 