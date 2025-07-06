import {
  GameState,
  PlayerState,
  QuestState,
  RitualState,
  WorldState,
  WorldEvent,
  WorldEffect,
  InventoryItem,
  PlayerStats
} from './types';

import { Logger } from '../utils/logger';
import { DialogService } from '../dialog-engine/dialog-service';
import { KnowledgeService } from '../knowledge-base/knowledge-service';

export class GameService {
  private games: Map<string, GameState>;
  private logger: Logger;
  private dialogService: DialogService;
  private knowledgeService: KnowledgeService;

  constructor(
    logger: Logger,
    dialogService: DialogService,
    knowledgeService: KnowledgeService
  ) {
    this.games = new Map();
    this.logger = logger;
    this.dialogService = dialogService;
    this.knowledgeService = knowledgeService;
  }

  private createInitialState(playerId: string, playerName: string): GameState {
    const playerState: PlayerState = {
      id: playerId,
      name: playerName,
      level: 1,
      experience: 0,
      energy: 100,
      maxEnergy: 100,
      energyRegenRate: 1,
      lastEnergyRegen: Date.now(),
      reputation: {
        total: 0,
        byGovernor: new Map()
      },
      inventory: {
        items: [],
        capacity: 50,
        categories: new Map()
      },
      skills: {
        levels: new Map(),
        experience: new Map(),
        masteryLevels: new Map()
      },
      achievements: [],
      stats: {
        questsCompleted: 0,
        ritualsPerformed: 0,
        itemsCollected: 0,
        dialoguesHad: 0,
        timeSpent: 0,
        energySpent: 0,
        reputationGained: 0
      },
      lastAction: Date.now()
    };

    const worldState: WorldState = {
      time: Date.now(),
      cycle: 0,
      events: [],
      activeEffects: [],
      governors: new Map()
    };

    return {
      id: `game_${playerId}`,
      player: playerState,
      activeQuests: [],
      completedQuests: [],
      activeRituals: [],
      worldState,
      lastUpdate: Date.now()
    };
  }

  private validateGameState(state: GameState): boolean {
    return Boolean(
      state &&
      state.id &&
      state.player &&
      Array.isArray(state.activeQuests) &&
      Array.isArray(state.completedQuests) &&
      Array.isArray(state.activeRituals) &&
      state.worldState
    );
  }

  private async updateGameState(state: GameState): Promise<void> {
    const now = Date.now();

    // Update energy
    const energyRegenCycles = Math.floor(
      (now - state.player.lastEnergyRegen) / (60 * 1000) // 1 minute cycles
    );
    if (energyRegenCycles > 0) {
      state.player.energy = Math.min(
        state.player.maxEnergy,
        state.player.energy + (energyRegenCycles * state.player.energyRegenRate)
      );
      state.player.lastEnergyRegen = now;
    }

    // Update world effects
    state.worldState.activeEffects = state.worldState.activeEffects.filter(effect => {
      return now - effect.startedAt < effect.duration;
    });

    // Update quests
    state.activeQuests = state.activeQuests.filter(quest => {
      if (quest.expiresAt && now > quest.expiresAt) {
        this.logger.info(`Quest ${quest.id} expired`);
        return false;
      }
      return true;
    });

    // Update rituals
    state.activeRituals = state.activeRituals.filter(ritual => {
      if (ritual.expiresAt && now > ritual.expiresAt) {
        this.logger.info(`Ritual ${ritual.id} expired`);
        return false;
      }
      return true;
    });

    state.lastUpdate = now;
  }

  async createGame(playerId: string, playerName: string): Promise<GameState> {
    this.logger.info(`Creating new game for player ${playerId}`);
    
    const state = this.createInitialState(playerId, playerName);
    this.games.set(state.id, state);
    
    return state;
  }

  async loadGame(gameId: string): Promise<GameState> {
    const state = this.games.get(gameId);
    if (!state) {
      throw new Error(`Game ${gameId} not found`);
    }

    if (!this.validateGameState(state)) {
      throw new Error(`Invalid game state for ${gameId}`);
    }

    await this.updateGameState(state);
    return state;
  }

  async startQuest(gameId: string, questId: string): Promise<QuestState> {
    const state = await this.loadGame(gameId);
    
    // TODO: Load quest template from knowledge base
    const quest: QuestState = {
      id: questId,
      name: "Test Quest",
      description: "A test quest",
      type: 'side',
      stage: 0,
      progress: 0,
      requirements: [],
      objectives: [],
      rewards: [],
      governor: 'gov-1',
      startedAt: Date.now()
    };

    state.activeQuests.push(quest);
    return quest;
  }

  async startRitual(gameId: string, ritualId: string): Promise<RitualState> {
    const state = await this.loadGame(gameId);
    
    // TODO: Load ritual template from knowledge base
    const ritual: RitualState = {
      id: ritualId,
      name: "Test Ritual",
      description: "A test ritual",
      type: 'invocation',
      stage: 0,
      components: [],
      requirements: [],
      effects: [],
      governor: 'gov-1',
      startedAt: Date.now()
    };

    state.activeRituals.push(ritual);
    return ritual;
  }

  async updateQuestProgress(
    gameId: string,
    questId: string,
    objectiveId: string,
    progress: number
  ): Promise<QuestState> {
    const state = await this.loadGame(gameId);
    const quest = state.activeQuests.find(q => q.id === questId);
    
    if (!quest) {
      throw new Error(`Quest ${questId} not found`);
    }

    const objective = quest.objectives.find(o => o.id === objectiveId);
    if (!objective) {
      throw new Error(`Objective ${objectiveId} not found in quest ${questId}`);
    }

    objective.progress = Math.min(progress, objective.target as number);
    objective.completed = objective.progress >= (objective.target as number);

    // Update overall quest progress
    const totalProgress = quest.objectives.reduce((sum, obj) => {
      if (obj.optional) return sum;
      return sum + (obj.completed ? 1 : 0);
    }, 0);

    const requiredObjectives = quest.objectives.filter(obj => !obj.optional).length;
    quest.progress = (totalProgress / requiredObjectives) * 100;

    if (quest.progress >= 100) {
      quest.completedAt = Date.now();
      state.completedQuests.push(quest);
      state.activeQuests = state.activeQuests.filter(q => q.id !== questId);
      
      // Update player stats
      state.player.stats.questsCompleted++;
    }

    return quest;
  }

  async updateRitualProgress(
    gameId: string,
    ritualId: string,
    componentId: string,
    value: number | string
  ): Promise<RitualState> {
    const state = await this.loadGame(gameId);
    const ritual = state.activeRituals.find(r => r.id === ritualId);
    
    if (!ritual) {
      throw new Error(`Ritual ${ritualId} not found`);
    }

    const component = ritual.components.find(c => c.id === componentId);
    if (!component) {
      throw new Error(`Component ${componentId} not found in ritual ${ritualId}`);
    }

    component.value = value;
    
    // Check if all required components are satisfied
    const allComponentsSatisfied = ritual.components
      .filter(c => !c.optional)
      .every(c => Boolean(c.value));

    if (allComponentsSatisfied) {
      ritual.completedAt = Date.now();
      
      // Apply ritual effects
      for (const effect of ritual.effects) {
        const worldEffect: WorldEffect = {
          type: 'ritual_power',
          value: effect.value,
          duration: effect.duration || 0,
          startedAt: Date.now()
        };
        state.worldState.activeEffects.push(worldEffect);
      }

      // Update player stats
      state.player.stats.ritualsPerformed++;
    }

    return ritual;
  }

  async addInventoryItem(gameId: string, item: InventoryItem): Promise<void> {
    const state = await this.loadGame(gameId);
    
    // Check capacity
    const currentCount = state.player.inventory.items.reduce((sum, item) => {
      return sum + (item.stackable ? 1 : item.quantity);
    }, 0);

    if (currentCount >= state.player.inventory.capacity) {
      throw new Error('Inventory is full');
    }

    // Update category counts
    const categoryCount = state.player.inventory.categories.get(item.type) || 0;
    state.player.inventory.categories.set(item.type, categoryCount + 1);

    // Add item
    state.player.inventory.items.push(item);

    // Update player stats
    state.player.stats.itemsCollected++;
  }

  async removeInventoryItem(gameId: string, itemId: string): Promise<void> {
    const state = await this.loadGame(gameId);
    const item = state.player.inventory.items.find(i => i.id === itemId);
    
    if (!item) {
      throw new Error(`Item ${itemId} not found in inventory`);
    }

    // Update category counts
    const categoryCount = state.player.inventory.categories.get(item.type) || 0;
    if (categoryCount > 1) {
      state.player.inventory.categories.set(item.type, categoryCount - 1);
    } else {
      state.player.inventory.categories.delete(item.type);
    }

    // Remove item
    state.player.inventory.items = state.player.inventory.items.filter(i => i.id !== itemId);
  }

  async addWorldEvent(gameId: string, event: WorldEvent): Promise<void> {
    const state = await this.loadGame(gameId);
    
    state.worldState.events.push(event);

    // Apply immediate effects
    for (const effect of event.effects) {
      state.worldState.activeEffects.push(effect);
    }

    // Update world cycle if needed
    const hoursSinceLastCycle = (Date.now() - state.worldState.time) / (60 * 60 * 1000);
    if (hoursSinceLastCycle >= 24) {
      state.worldState.cycle++;
      state.worldState.time = Date.now();
    }
  }

  async getGameStats(gameId: string): Promise<PlayerStats> {
    const state = await this.loadGame(gameId);
    return state.player.stats;
  }
} 