# Questline Engine Architecture

## Core Design Philosophy

The questline engine is designed as a **fully on-chain, Bitcoin L1-native narrative system**. Each of the 91 Governors exists as an immutable inscription with dynamic state managed through TAP Protocol tokens. The entire system operates without any web dependencies or external services.

## Key Components

### 1. Governor Inscriptions & TAP Tokens
- **Immutable Core**: Each Governor inscribed as permanent Bitcoin Ordinal
- **Dynamic State**: TAP tokens track interaction state and progression
- **Self-Contained Logic**: All game rules encoded in inscription JavaScript
- **Local Processing**: All AI/narrative generation runs on client device

### 2. Reputation-Based Progression
- **0-25 Rep**: Basic introductions and tests
- **26-50 Rep**: Deeper mysteries and subtle Voidmaker hints
- **51-75 Rep**: Direct cosmic concepts and branching quests
- **76-100 Rep**: Full secrets and Voidmaker puzzle pieces
- **All progression stored in TAP tokens**

### 3. Non-Linear Narrative Structure
- **Aethyr-Based Exploration**: 30 dimensional realms as inscribed content
- **Cross-Governor Interactions**: Coordinated through TAP Protocol
- **Dynamic Questlines**: 20-35 narrative nodes per Governor inscription
- **Branching Choices**: State changes via TAP token evolution

## Technical Implementation

### Governor Inscription Structure
```typescript
interface GovernorInscription {
  id: string;
  name: string;
  aethyr: string;
  element: ElementType;
  personality: PersonalityTraits;
  canonicalData: CanonicalData;
  traitChoices: TraitChoices;
  
  // Self-contained game logic
  narrativeEngine: {
    generateResponse: (input: string, state: TAPTokenState) => NarrativeResponse;
    processAction: (action: PlayerAction, state: TAPTokenState) => StateUpdate;
  };
}
```

### TAP Protocol State Management
```typescript
interface GovernorTAPToken {
  tokenId: string;
  governorId: string;
  currentState: {
    reputation: number;
    unlockedNodes: string[];
    completedQuests: string[];
    activeEffects: Effect[];
  };
  
  // Evolution rules encoded in token
  evolve(action: PlayerAction): StateTransition;
  validate(newState: Partial<GovernorState>): boolean;
}
```

## On-Chain Knowledge Integration

### Inscribed Knowledge Base
All knowledge is stored as Bitcoin inscriptions:

```typescript
interface KnowledgeInscription {
  id: string;
  tradition: MysticalTradition;
  content: string;
  accessLevel: number; // Reputation required
  references: string[]; // Other inscription IDs
}

// No external queries - all knowledge pre-inscribed
class LocalKnowledgeAccess {
  async queryKnowledge(params: QueryParams): Promise<KnowledgeFragment[]> {
    return this.searchLocalInscriptions(params);
  }
}
```

### Governor Knowledge Access
Each Governor accesses knowledge through inscription references:

```typescript
class InscribedGovernor {
  // Knowledge is referenced by inscription IDs
  specializedKnowledge: string[]; // Inscription IDs
  
  async accessKnowledge(
    topic: string,
    playerState: TAPTokenState
  ): Promise<string[]> {
    const accessible = this.specializedKnowledge.filter(id => 
      this.canAccess(id, playerState.reputation)
    );
    return this.fetchInscriptionContent(accessible);
  }
}
```

## Decentralized Infrastructure

### Pure Bitcoin L1 Storage
All content exists as Ordinal inscriptions:

```typescript
interface QuestlineInscription {
  type: 'governor-profile' | 'narrative-node' | 'lore-fragment';
  governorId: string;
  content: string; // No encryption - fully on-chain
  dependencies: string[]; // Other inscription IDs
  version: number;
}
```

### TAP Protocol Game State
All mutable state managed through TAP:

```typescript
interface PlayerTAPToken {
  tokenId: string;
  playerId: string;
  gameState: {
    aethyrsUnlocked: string[];
    voidmakerAwareness: number;
    codexEntries: string[];
    activeQuests: QuestReference[];
  };
  
  // State transitions through TAP
  evolve(action: GameAction): StateTransition;
}
```

### P2P Coordination
Pure peer-to-peer using Hyperswarm DHT:

```typescript
interface P2PCoordination {
  // Discover peers through DHT
  async findPeers(): Promise<PeerConnection[]>;
  
  // Validate and sync TAP token states
  async syncState(peerId: string): Promise<void>;
  
  // Broadcast game actions
  async broadcastAction(action: GameAction): Promise<void>;
}
```

### Zero-Infrastructure Operation
The system operates entirely on Bitcoin L1:

- **All Content**: Stored as Ordinal inscriptions
- **All State**: Managed through TAP tokens
- **All Processing**: Runs locally on player devices
- **All Networking**: Pure P2P through Hyperswarm
- **No External Dependencies**: Everything on Bitcoin

## Narrative Generation

### Local Processing Engine
All narrative generation runs on the client:

```typescript
class LocalNarrativeEngine {
  constructor(
    governorInscription: GovernorInscription,
    playerToken: PlayerTAPToken
  ) {
    this.governor = governorInscription;
    this.state = playerToken;
  }
  
  async generateResponse(input: string): Promise<NarrativeResponse> {
    // Use inscribed personality and knowledge
    const context = this.buildContext(this.state);
    return this.governor.narrativeEngine.generateResponse(input, context);
  }
}
```

### Inscribed Content Structure
Narrative content pre-inscribed and referenced:

```typescript
interface NarrativeNodeInscription {
  id: string;
  type: 'dialogue' | 'quest' | 'revelation' | 'test';
  content: string;
  choices: {
    text: string;
    nextNodeId: string;
    requirements: TAPRequirement[];
  }[];
  reputationGate: number;
}
```

### State Transitions
All state changes through TAP evolution:

```typescript
interface NarrativeStateChange {
  type: 'QUEST_COMPLETE' | 'CHOICE_MADE' | 'ITEM_FOUND';
  data: any;
  
  // Evolve relevant TAP tokens
  async apply(playerToken: PlayerTAPToken): Promise<void> {
    const transition = await playerToken.evolve(this);
    await this.broadcastToNetwork(transition);
  }
}
```

## Implementation Strategy

### Phase 1: Bitcoin Foundation (Months 1-2)
- Implement inscription structure for Governors
- Create TAP token templates
- Build local narrative processing
- Establish P2P networking base

### Phase 2: Content Inscription (Months 3-4)
- Inscribe all Governor content
- Create knowledge base inscriptions
- Build narrative node network
- Implement content validation

### Phase 3: TAP Integration (Months 5-6)
- Implement token evolution rules
- Build state transition system
- Create validation logic
- Test network consensus

### Phase 4: P2P Completion (Months 7-8)
- Complete Hyperswarm integration
- Implement state synchronization
- Build action broadcasting
- Test full system operation

### Success Metrics
- **Zero External Calls**: No web requests or external services
- **Full Decentralization**: Everything on Bitcoin L1
- **Local Processing**: All computation on client
- **P2P Consensus**: Clean state synchronization
- **Network Resilience**: Operates offline after initial sync

### Risk Mitigation
- **Size Optimization**: Efficient inscription batching
- **State Consistency**: Robust TAP validation
- **Network Efficiency**: Smart P2P protocols
- **Client Performance**: Optimized local processing
- **Bitcoin Costs**: Strategic inscription planning
