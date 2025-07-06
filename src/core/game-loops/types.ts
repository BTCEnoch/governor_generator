import { BlockchainMetadata } from '../blockchain/types';
import { DialogContext } from '../dialog-engine/types';

export interface GameState {
  id: string;
  player: PlayerState;
  activeQuests: QuestState[];
  completedQuests: QuestState[];
  activeRituals: RitualState[];
  worldState: WorldState;
  blockchainMetadata?: BlockchainMetadata;
  lastUpdate: number;
}

export interface PlayerState {
  id: string;
  name: string;
  level: number;
  experience: number;
  energy: number;
  maxEnergy: number;
  energyRegenRate: number;
  lastEnergyRegen: number;
  reputation: {
    total: number;
    byGovernor: Map<string, number>;
  };
  inventory: InventoryState;
  skills: SkillState;
  achievements: Achievement[];
  stats: PlayerStats;
  lastAction: number;
}

export interface InventoryState {
  items: InventoryItem[];
  capacity: number;
  categories: Map<string, number>; // Category -> count
}

export interface InventoryItem {
  id: string;
  type: ItemType;
  name: string;
  description: string;
  rarity: ItemRarity;
  properties: ItemProperties;
  stackable: boolean;
  quantity: number;
  acquiredAt: number;
  blockchainMetadata?: BlockchainMetadata;
}

export type ItemType = 
  | 'ritual_component'
  | 'artifact'
  | 'knowledge_fragment'
  | 'consumable'
  | 'key_item';

export type ItemRarity = 
  | 'common'
  | 'uncommon'
  | 'rare'
  | 'epic'
  | 'legendary'
  | 'mythical';

export interface ItemProperties {
  effects?: ItemEffect[];
  requirements?: ItemRequirement[];
  durability?: number;
  maxDurability?: number;
  cooldown?: number;
  lastUsed?: number;
  charges?: number;
  maxCharges?: number;
}

export interface ItemEffect {
  type: EffectType;
  value: number;
  duration?: number;
  conditions?: EffectCondition[];
}

export type EffectType =
  | 'energy_restore'
  | 'energy_regen'
  | 'reputation_boost'
  | 'skill_boost'
  | 'ritual_power'
  | 'quest_progress';

export interface EffectCondition {
  type: 'skill_level' | 'reputation' | 'quest_stage' | 'time_of_day';
  requirement: number | string;
}

export interface ItemRequirement {
  type: 'skill_level' | 'reputation' | 'quest_completion';
  value: number | string;
}

export interface SkillState {
  levels: Map<string, number>;
  experience: Map<string, number>;
  masteryLevels: Map<string, number>;
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  progress: number;
  completed: boolean;
  completedAt?: number;
  rewards?: AchievementReward[];
}

export interface AchievementReward {
  type: 'item' | 'skill_experience' | 'reputation' | 'energy';
  value: number | string;
  quantity?: number;
}

export interface PlayerStats {
  questsCompleted: number;
  ritualsPerformed: number;
  itemsCollected: number;
  dialoguesHad: number;
  timeSpent: number;
  energySpent: number;
  reputationGained: number;
}

export interface QuestState {
  id: string;
  name: string;
  description: string;
  type: QuestType;
  stage: number;
  progress: number;
  requirements: QuestRequirement[];
  objectives: QuestObjective[];
  rewards: QuestReward[];
  governor: string;
  startedAt: number;
  completedAt?: number;
  expiresAt?: number;
  blockchainMetadata?: BlockchainMetadata;
}

export type QuestType =
  | 'main'
  | 'side'
  | 'daily'
  | 'repeatable'
  | 'hidden'
  | 'achievement';

export interface QuestRequirement {
  type: 'level' | 'skill' | 'reputation' | 'item' | 'quest';
  value: number | string;
  operator?: 'eq' | 'gt' | 'gte' | 'lt' | 'lte';
}

export interface QuestObjective {
  id: string;
  description: string;
  type: ObjectiveType;
  target: string | number;
  progress: number;
  completed: boolean;
  optional?: boolean;
  hidden?: boolean;
}

export type ObjectiveType =
  | 'collect_item'
  | 'perform_ritual'
  | 'gain_reputation'
  | 'learn_skill'
  | 'visit_location'
  | 'complete_dialogue';

export interface QuestReward {
  type: 'item' | 'skill_experience' | 'reputation' | 'energy';
  value: number | string;
  quantity?: number;
}

export interface RitualState {
  id: string;
  name: string;
  description: string;
  type: RitualType;
  stage: number;
  components: RitualComponent[];
  requirements: RitualRequirement[];
  effects: RitualEffect[];
  governor: string;
  startedAt: number;
  completedAt?: number;
  expiresAt?: number;
  blockchainMetadata?: BlockchainMetadata;
}

export type RitualType =
  | 'invocation'
  | 'binding'
  | 'transformation'
  | 'protection'
  | 'divination';

export interface RitualComponent {
  id: string;
  type: 'item' | 'energy' | 'skill' | 'time';
  value: number | string;
  consumed: boolean;
  optional?: boolean;
}

export interface RitualRequirement {
  type: 'skill_level' | 'reputation' | 'time_of_day' | 'location';
  value: number | string;
}

export interface RitualEffect {
  type: EffectType;
  value: number;
  duration?: number;
  conditions?: EffectCondition[];
}

export interface WorldState {
  time: number;
  cycle: number;
  events: WorldEvent[];
  activeEffects: WorldEffect[];
  governors: Map<string, GovernorState>;
}

export interface WorldEvent {
  id: string;
  type: 'ritual' | 'quest' | 'governor' | 'player';
  source: string;
  timestamp: number;
  effects: WorldEffect[];
}

export interface WorldEffect {
  type: 'energy_cost' | 'reputation_modifier' | 'skill_gain' | 'ritual_power';
  value: number;
  duration: number;
  startedAt: number;
}

export interface GovernorState {
  id: string;
  name: string;
  domain: string;
  influence: number;
  activeQuests: string[];
  activeRituals: string[];
  dialogContext: DialogContext;
} 