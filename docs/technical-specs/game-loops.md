# Game Loops Technical Specification

## Overview
The Game Loops system manages the core gameplay cycles, quest progression, and reward mechanisms in the Enochian Governor system. It coordinates player actions, governor interactions, and blockchain state management.

## Core Game Loops

### Quest Loop
```typescript
interface QuestLoop {
  state: QuestState;
  progression: QuestProgression;
  rewards: RewardSystem;
  validation: QuestValidator;
}

interface QuestState {
  activeQuests: Map<string, QuestProgress>;
  completedQuests: string[];
  failedQuests: string[];
  questChains: Map<string, string[]>;
  unlockConditions: Map<string, Condition[]>;
}

interface QuestProgress {
  questId: string;
  stage: number;
  objectives: ObjectiveProgress[];
  timeStarted: number;
  lastUpdated: number;
  governorId: string;
  reputationTier: number;
}

interface ObjectiveProgress {
  id: string;
  type: ObjectiveType;
  progress: number;
  target: number;
  completed: boolean;
  rewards: Reward[];
}
```

### Reputation Loop
```typescript
interface ReputationLoop {
  state: ReputationState;
  progression: ReputationProgression;
  unlocks: UnlockSystem;
}

interface ReputationState {
  governorScores: Map<string, number>;
  tierUnlocks: Map<number, string[]>;
  reputationHistory: ReputationEvent[];
  globalReputation: number;
}

interface ReputationEvent {
  governorId: string;
  change: number;
  reason: string;
  timestamp: number;
  questId?: string;
}
```

### Energy Loop
```typescript
interface EnergyLoop {
  state: EnergyState;
  management: EnergyManager;
  regeneration: RegenerationSystem;
}

interface EnergyState {
  current: number;
  max: number;
  regenerationRate: number;
  lastRegeneration: number;
  modifiers: EnergyModifier[];
}

interface EnergyModifier {
  type: ModifierType;
  value: number;
  duration: number;
  source: string;
}
```

## State Management

### Game State
```typescript
interface GameState {
  player: PlayerState;
  world: WorldState;
  blockchain: BlockchainState;
}

interface PlayerState {
  quests: QuestState;
  reputation: ReputationState;
  energy: EnergyState;
  inventory: InventoryState;
  knowledge: KnowledgeState;
  achievements: AchievementState;
}

interface WorldState {
  time: number;
  activeEvents: GameEvent[];
  governorStates: Map<string, GovernorState>;
  environmentalEffects: Effect[];
}

interface BlockchainState {
  lastSync: number;
  pendingTransactions: Transaction[];
  confirmedStates: StateHash[];
  ordinalRefs: Map<string, string>;
}
```

### State Transitions
```typescript
interface StateTransition {
  from: GameState;
  to: GameState;
  changes: StateChange[];
  validation: TransitionValidation;
}

interface StateChange {
  type: ChangeType;
  path: string[];
  oldValue: any;
  newValue: any;
  reason: string;
}

interface TransitionValidation {
  validateTransition(
    from: GameState,
    to: GameState
  ): Promise<ValidationResult>;
  
  rollbackTransition(
    change: StateChange
  ): Promise<void>;
}
```

## Quest System

### Quest Definition
```typescript
interface Quest {
  id: string;
  governorId: string;
  title: string;
  description: string;
  type: QuestType;
  tier: number;
  stages: QuestStage[];
  requirements: QuestRequirement[];
  rewards: QuestReward[];
}

interface QuestStage {
  id: string;
  objectives: Objective[];
  dialog: DialogTree;
  completion: CompletionCriteria;
  stageRewards: Reward[];
}

interface Objective {
  type: ObjectiveType;
  target: number;
  description: string;
  optional: boolean;
  timeLimit?: number;
}
```

### Quest Progression
```typescript
interface QuestProgression {
  // Stage management
  startQuest(questId: string): Promise<void>;
  advanceStage(questId: string): Promise<void>;
  completeQuest(questId: string): Promise<void>;
  failQuest(questId: string): Promise<void>;
  
  // Progress tracking
  updateProgress(
    questId: string,
    objectiveId: string,
    progress: number
  ): Promise<void>;
  
  // State queries
  getQuestProgress(questId: string): QuestProgress;
  getAvailableQuests(): Quest[];
  getCompletedQuests(): string[];
}
```

## Reward System

### Reward Types
```typescript
interface Reward {
  type: RewardType;
  value: number | string;
  metadata?: any;
}

type RewardType =
  | 'reputation'
  | 'energy'
  | 'item'
  | 'knowledge'
  | 'achievement'
  | 'token';

interface RewardDistribution {
  distributeReward(
    reward: Reward,
    player: PlayerState
  ): Promise<void>;
  
  validateReward(
    reward: Reward,
    context: GameState
  ): Promise<boolean>;
}
```

### Achievement System
```typescript
interface Achievement {
  id: string;
  title: string;
  description: string;
  criteria: AchievementCriteria[];
  rewards: Reward[];
  secret: boolean;
}

interface AchievementProgress {
  achieved: boolean;
  progress: number;
  timestamp?: number;
  criteria: Map<string, boolean>;
}
```

## Blockchain Integration

### State Persistence
```typescript
interface BlockchainPersistence {
  // State management
  saveState(state: GameState): Promise<string>;
  loadState(hash: string): Promise<GameState>;
  
  // Transaction handling
  submitTransaction(tx: GameTransaction): Promise<string>;
  confirmTransaction(txId: string): Promise<void>;
  
  // Sync management
  syncState(): Promise<void>;
  validateChainState(): Promise<boolean>;
}
```

### Transaction Types
```typescript
interface GameTransaction {
  type: TransactionType;
  payload: any;
  timestamp: number;
  signature: string;
  nonce: number;
}

type TransactionType =
  | 'quest_progress'
  | 'reputation_change'
  | 'energy_update'
  | 'item_transfer'
  | 'state_update';
```

## Performance Requirements

### Response Times
- Quest updates: < 200ms
- State transitions: < 100ms
- Reward distribution: < 150ms
- Blockchain ops: < 5s

### Resource Usage
- Memory: < 512MB
- CPU: < 30%
- Storage: < 1GB
- Network: < 2MB/s

## Error Handling

### Error Types
```typescript
enum GameLoopError {
  INVALID_STATE = 'INVALID_STATE',
  QUEST_ERROR = 'QUEST_ERROR',
  REWARD_ERROR = 'REWARD_ERROR',
  BLOCKCHAIN_ERROR = 'BLOCKCHAIN_ERROR',
  SYNC_ERROR = 'SYNC_ERROR'
}
```

### Recovery Procedures
1. State rollback
2. Transaction retry
3. Sync recovery
4. Error compensation
5. Player notification

## Testing Requirements

### Test Categories
1. Loop integration tests
2. State transition tests
3. Reward distribution tests
4. Blockchain sync tests
5. Performance benchmarks

### Coverage Requirements
- Code coverage: 95%
- State transitions: 100%
- Error paths: 100%
- Blockchain ops: 100%
- Performance targets: 95%

## Security Measures

### State Protection
1. Transition validation
2. State encryption
3. Signature verification
4. Rate limiting
5. Anti-cheat measures

### Transaction Security
1. Nonce validation
2. Double-spend prevention
3. Reward verification
4. State consistency checks
5. Audit logging

## Monitoring System

### Metrics
1. Loop execution times
2. State transition rates
3. Reward distribution stats
4. Blockchain sync status
5. Error frequencies

### Alerts
1. State corruption
2. Sync failures
3. Performance degradation
4. Security violations
5. Critical errors

## Documentation Requirements

### API Documentation
1. Loop interfaces
2. State management
3. Transaction types
4. Error handling
5. Integration points

### System Documentation
1. Architecture overview
2. Component interaction
3. State flow diagrams
4. Recovery procedures
5. Maintenance guides 