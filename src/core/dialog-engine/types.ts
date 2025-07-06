import { BlockchainMetadata } from '../blockchain/types';

export interface DialogContext {
  governorId: string;
  playerState: PlayerState;
  sessionId: string;
  timestamp: number;
  previousMessages: DialogMessage[];
  activeQuests: string[];
  unlockedContent: string[];
}

export interface PlayerState {
  id: string;
  reputation: number;
  energy: number;
  completedQuests: string[];
  inventory: InventoryItem[];
  skills: Map<string, number>;
  lastInteraction: number;
}

export interface InventoryItem {
  id: string;
  type: 'artifact' | 'ritual_item' | 'knowledge_fragment';
  name: string;
  description: string;
  properties: Record<string, any>;
  acquiredAt: number;
  blockchainMetadata?: BlockchainMetadata;
}

export interface DialogMessage {
  id: string;
  role: 'governor' | 'player';
  content: string;
  intent?: DialogIntent;
  sentiment?: DialogSentiment;
  timestamp: number;
  metadata?: {
    questProgress?: QuestProgress;
    reputationChange?: number;
    energyCost?: number;
    rewards?: InventoryItem[];
  };
}

export interface DialogIntent {
  primary: string;
  confidence: number;
  secondary?: string[];
  entities?: Record<string, string>;
}

export interface DialogSentiment {
  score: number; // -1 to 1
  aspects: {
    respect: number;
    wisdom: number;
    devotion: number;
  };
}

export interface QuestProgress {
  questId: string;
  stage: number;
  completed: boolean;
  requirements: {
    items?: string[];
    skills?: Record<string, number>;
    reputation?: number;
  };
}

export interface DialogResponse {
  message: DialogMessage;
  stateChanges: {
    reputationDelta?: number;
    energyDelta?: number;
    addedItems?: InventoryItem[];
    removedItems?: string[];
    questUpdates?: QuestProgress[];
    unlockedContent?: string[];
  };
}

export interface DialogOptions {
  maxResponseLength?: number;
  includeMetadata?: boolean;
  forceIntent?: string;
  contextWindow?: number;
  temperature?: number;
}

export interface IntentClassification {
  intent: DialogIntent;
  sentiment: DialogSentiment;
  confidence: number;
}

export interface ResponseGeneration {
  content: string;
  metadata: {
    generationStats: {
      promptTokens: number;
      completionTokens: number;
      totalTokens: number;
      generationTime: number;
    };
    alternatives?: string[];
  };
}

export interface DialogStats {
  totalSessions: number;
  activeUsers: number;
  averageSessionLength: number;
  popularIntents: Array<{
    intent: string;
    count: number;
  }>;
  questCompletion: Record<string, number>;
  averageReputation: number;
  topRewards: Array<{
    item: string;
    count: number;
  }>;
} 