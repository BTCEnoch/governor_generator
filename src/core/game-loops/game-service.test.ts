import { GameService } from './game-service';
import { Logger, LogLevel } from '../utils/logger';
import { DialogService } from '../dialog-engine/dialog-service';
import { KnowledgeService } from '../knowledge-base/knowledge-service';
import { InventoryItem, QuestState, RitualState, WorldEvent } from './types';

describe('GameService', () => {
  let service: GameService;
  let logger: Logger;
  let dialogService: DialogService;
  let knowledgeService: KnowledgeService;

  beforeEach(() => {
    logger = new Logger('test', LogLevel.DEBUG);
    knowledgeService = new KnowledgeService(logger);
    dialogService = new DialogService(logger, knowledgeService);
    service = new GameService(logger, dialogService, knowledgeService);
  });

  describe('createGame', () => {
    it('should create a new game with initial state', async () => {
      const state = await service.createGame('player-1', 'Test Player');

      expect(state.id).toBe('game_player-1');
      expect(state.player.name).toBe('Test Player');
      expect(state.player.level).toBe(1);
      expect(state.player.energy).toBe(100);
      expect(state.activeQuests).toHaveLength(0);
      expect(state.activeRituals).toHaveLength(0);
    });
  });

  describe('loadGame', () => {
    it('should load an existing game', async () => {
      const state = await service.createGame('player-1', 'Test Player');
      const loaded = await service.loadGame(state.id);

      expect(loaded).toBeDefined();
      expect(loaded.id).toBe(state.id);
    });

    it('should throw error for non-existent game', async () => {
      await expect(service.loadGame('invalid-id')).rejects.toThrow('Game invalid-id not found');
    });
  });

  describe('startQuest', () => {
    it('should start a new quest', async () => {
      const state = await service.createGame('player-1', 'Test Player');
      const quest = await service.startQuest(state.id, 'quest-1');

      expect(quest.id).toBe('quest-1');
      expect(quest.stage).toBe(0);
      expect(quest.progress).toBe(0);
    });
  });

  describe('startRitual', () => {
    it('should start a new ritual', async () => {
      const state = await service.createGame('player-1', 'Test Player');
      const ritual = await service.startRitual(state.id, 'ritual-1');

      expect(ritual.id).toBe('ritual-1');
      expect(ritual.stage).toBe(0);
      expect(ritual.type).toBe('invocation');
    });
  });

  describe('updateQuestProgress', () => {
    let gameId: string;
    let quest: QuestState;

    beforeEach(async () => {
      const state = await service.createGame('player-1', 'Test Player');
      gameId = state.id;
      quest = await service.startQuest(gameId, 'quest-1');
      quest.objectives = [
        {
          id: 'obj-1',
          description: 'Test objective',
          type: 'collect_item',
          target: 10,
          progress: 0,
          completed: false
        }
      ];
    });

    it('should update objective progress', async () => {
      const updated = await service.updateQuestProgress(gameId, 'quest-1', 'obj-1', 5);
      expect(updated.objectives[0].progress).toBe(5);
      expect(updated.objectives[0].completed).toBe(false);
    });

    it('should complete objective when target is reached', async () => {
      const updated = await service.updateQuestProgress(gameId, 'quest-1', 'obj-1', 10);
      expect(updated.objectives[0].progress).toBe(10);
      expect(updated.objectives[0].completed).toBe(true);
    });

    it('should throw error for non-existent quest', async () => {
      await expect(
        service.updateQuestProgress(gameId, 'invalid-quest', 'obj-1', 5)
      ).rejects.toThrow('Quest invalid-quest not found');
    });
  });

  describe('updateRitualProgress', () => {
    let gameId: string;
    let ritual: RitualState;

    beforeEach(async () => {
      const state = await service.createGame('player-1', 'Test Player');
      gameId = state.id;
      ritual = await service.startRitual(gameId, 'ritual-1');
      ritual.components = [
        {
          id: 'comp-1',
          type: 'item',
          value: '',
          consumed: true
        }
      ];
    });

    it('should update component value', async () => {
      const updated = await service.updateRitualProgress(gameId, 'ritual-1', 'comp-1', 'test-item');
      expect(updated.components[0].value).toBe('test-item');
    });

    it('should throw error for non-existent ritual', async () => {
      await expect(
        service.updateRitualProgress(gameId, 'invalid-ritual', 'comp-1', 'test-item')
      ).rejects.toThrow('Ritual invalid-ritual not found');
    });
  });

  describe('inventory management', () => {
    let gameId: string;

    beforeEach(async () => {
      const state = await service.createGame('player-1', 'Test Player');
      gameId = state.id;
    });

    it('should add item to inventory', async () => {
      const item: InventoryItem = {
        id: 'item-1',
        type: 'ritual_component',
        name: 'Test Item',
        description: 'A test item',
        rarity: 'common',
        properties: {},
        stackable: true,
        quantity: 1,
        acquiredAt: Date.now()
      };

      await service.addInventoryItem(gameId, item);
      const state = await service.loadGame(gameId);
      expect(state.player.inventory.items).toHaveLength(1);
      expect(state.player.inventory.items[0].id).toBe('item-1');
    });

    it('should remove item from inventory', async () => {
      const item: InventoryItem = {
        id: 'item-1',
        type: 'ritual_component',
        name: 'Test Item',
        description: 'A test item',
        rarity: 'common',
        properties: {},
        stackable: true,
        quantity: 1,
        acquiredAt: Date.now()
      };

      await service.addInventoryItem(gameId, item);
      await service.removeInventoryItem(gameId, 'item-1');
      const state = await service.loadGame(gameId);
      expect(state.player.inventory.items).toHaveLength(0);
    });

    it('should throw error when inventory is full', async () => {
      const state = await service.loadGame(gameId);
      state.player.inventory.capacity = 1;

      const item: InventoryItem = {
        id: 'item-1',
        type: 'ritual_component',
        name: 'Test Item',
        description: 'A test item',
        rarity: 'common',
        properties: {},
        stackable: false,
        quantity: 1,
        acquiredAt: Date.now()
      };

      await service.addInventoryItem(gameId, item);
      await expect(service.addInventoryItem(gameId, {
        ...item,
        id: 'item-2'
      })).rejects.toThrow('Inventory is full');
    });
  });

  describe('world events', () => {
    let gameId: string;

    beforeEach(async () => {
      const state = await service.createGame('player-1', 'Test Player');
      gameId = state.id;
    });

    it('should add world event', async () => {
      const event: WorldEvent = {
        id: 'event-1',
        type: 'ritual',
        source: 'test',
        timestamp: Date.now(),
        effects: [
          {
            type: 'energy_cost',
            value: 10,
            duration: 3600000,
            startedAt: Date.now()
          }
        ]
      };

      await service.addWorldEvent(gameId, event);
      const state = await service.loadGame(gameId);
      expect(state.worldState.events).toHaveLength(1);
      expect(state.worldState.activeEffects).toHaveLength(1);
    });

    it('should update world cycle after 24 hours', async () => {
      const state = await service.loadGame(gameId);
      state.worldState.time = Date.now() - (25 * 60 * 60 * 1000); // 25 hours ago

      const event: WorldEvent = {
        id: 'event-1',
        type: 'ritual',
        source: 'test',
        timestamp: Date.now(),
        effects: []
      };

      await service.addWorldEvent(gameId, event);
      const updated = await service.loadGame(gameId);
      expect(updated.worldState.cycle).toBe(1);
    });
  });

  describe('getGameStats', () => {
    it('should return player stats', async () => {
      const state = await service.createGame('player-1', 'Test Player');
      const stats = await service.getGameStats(state.id);

      expect(stats).toBeDefined();
      expect(stats.questsCompleted).toBe(0);
      expect(stats.ritualsPerformed).toBe(0);
      expect(stats.itemsCollected).toBe(0);
    });
  });
}); 