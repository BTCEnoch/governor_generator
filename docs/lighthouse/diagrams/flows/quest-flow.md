# Quest System Flow

## Quest Interaction Flow
```mermaid
sequenceDiagram
    participant P as Player
    participant C as Client
    participant Q as Quest System
    participant D as Dialog Engine
    participant K as Knowledge Base
    participant B as Bitcoin Chain

    P->>C: Start Quest Interaction
    C->>Q: Request Available Quests
    Q->>K: Check Knowledge Requirements
    K-->>Q: Return Available Content
    Q-->>C: Return Quest Options
    C-->>P: Display Quest Options

    P->>C: Select Quest
    C->>Q: Start Quest
    Q->>D: Generate Quest Dialog
    D->>K: Fetch Quest Knowledge
    K-->>D: Return Knowledge
    D-->>Q: Return Dialog
    Q->>B: Record Quest Start
    B-->>Q: Confirm Transaction
    Q-->>C: Quest Started
    C-->>P: Display Quest Dialog

    Note over P,B: Quest Progress Loop

    P->>C: Complete Objective
    C->>Q: Update Progress
    Q->>B: Record Progress
    B-->>Q: Confirm Transaction
    Q->>D: Generate Response
    D-->>Q: Return Response
    Q-->>C: Update State
    C-->>P: Show Progress

    Note over P,B: Quest Completion

    P->>C: Complete Final Objective
    C->>Q: Verify Completion
    Q->>B: Record Completion
    B-->>Q: Confirm Transaction
    Q->>K: Unlock New Knowledge
    K-->>Q: Knowledge Updated
    Q-->>C: Quest Complete
    C-->>P: Show Rewards
```

## Quest State Flow
```mermaid
stateDiagram-v2
    [*] --> Available
    Available --> Accepted: Player Accepts
    Accepted --> InProgress: Start Quest
    InProgress --> Failed: Fail Conditions
    InProgress --> Completed: All Objectives Done
    Failed --> Available: Reset
    Completed --> [*]

    state InProgress {
        [*] --> ObjectiveActive
        ObjectiveActive --> ObjectiveComplete: Complete Objective
        ObjectiveComplete --> ObjectiveActive: Next Objective
        ObjectiveComplete --> [*]: All Done
    }
```

## Component Descriptions

### Participants
- **Player**: End user interacting with the system
- **Client**: Local game client handling UI and state
- **Quest System**: Core quest management system
- **Dialog Engine**: Handles NPC interactions and responses
- **Knowledge Base**: Stores and manages game knowledge
- **Bitcoin Chain**: Permanent record of game state

### Key Interactions
1. **Quest Discovery**
   - Player initiates quest interaction
   - System checks requirements
   - Available quests are presented

2. **Quest Initiation**
   - Player selects quest
   - System validates and starts quest
   - Initial dialog is generated
   - State is recorded on-chain

3. **Quest Progress**
   - Player completes objectives
   - Progress is validated and recorded
   - Appropriate responses are generated
   - State is updated on-chain

4. **Quest Completion**
   - Final objective completion
   - System verifies all requirements
   - Records completion on-chain
   - Unlocks new knowledge/content
   - Distributes rewards

### State Transitions
- **Available**: Quest can be started
- **Accepted**: Player has accepted but not started
- **InProgress**: Active quest with objectives
- **Failed**: Failed to meet requirements
- **Completed**: Successfully finished

### On-Chain Integration
- Quest starts are recorded
- Progress is tracked
- Completions are permanent
- Rewards are distributed
- Knowledge unlocks are tracked 

# Quest Flow Sequence Diagram

## Overview
This diagram illustrates the sequence of interactions between system components during quest initiation, progression, and completion.

## Diagram

```mermaid
sequenceDiagram
    participant Player
    participant QuestSystem
    participant Governor
    participant DialogEngine
    participant StateManager
    participant Blockchain
    
    Player->>QuestSystem: Request Available Quests
    QuestSystem->>StateManager: Get Player State
    StateManager-->>QuestSystem: Return State
    QuestSystem->>Governor: Get Available Quests
    Governor-->>QuestSystem: Return Quest List
    QuestSystem-->>Player: Display Available Quests
    
    Player->>QuestSystem: Start Quest
    QuestSystem->>StateManager: Validate Requirements
    StateManager-->>QuestSystem: Requirements Met
    QuestSystem->>DialogEngine: Initialize Quest Dialog
    DialogEngine->>Governor: Get Initial Dialog
    Governor-->>DialogEngine: Return Dialog
    DialogEngine-->>Player: Display Quest Introduction
    
    QuestSystem->>StateManager: Update Quest State
    StateManager->>Blockchain: Submit State Transaction
    Blockchain-->>StateManager: Confirm Transaction
    
    loop Quest Progress
        Player->>QuestSystem: Complete Objective
        QuestSystem->>StateManager: Update Progress
        StateManager->>Blockchain: Submit Progress
        Blockchain-->>StateManager: Confirm Progress
        QuestSystem->>DialogEngine: Get Progress Dialog
        DialogEngine->>Governor: Get Response
        Governor-->>DialogEngine: Return Response
        DialogEngine-->>Player: Display Progress Update
    end
    
    Player->>QuestSystem: Complete Final Objective
    QuestSystem->>StateManager: Validate Completion
    StateManager-->>QuestSystem: Completion Confirmed
    QuestSystem->>DialogEngine: Get Completion Dialog
    DialogEngine->>Governor: Get Final Response
    Governor-->>DialogEngine: Return Response
    DialogEngine-->>Player: Display Quest Completion
    
    QuestSystem->>StateManager: Update Reputation
    StateManager->>Blockchain: Submit Reputation Change
    Blockchain-->>StateManager: Confirm Change
    
    QuestSystem->>StateManager: Distribute Rewards
    StateManager->>Blockchain: Submit Reward Transaction
    Blockchain-->>StateManager: Confirm Rewards
    QuestSystem-->>Player: Display Rewards
```

## Component Descriptions

### Player
- Initiates quest interactions
- Completes objectives
- Receives feedback and rewards

### QuestSystem
- Manages quest availability and progression
- Coordinates between components
- Handles objective completion
- Distributes rewards

### Governor
- Provides quest content
- Generates contextual responses
- Validates quest-specific actions

### DialogEngine
- Manages conversation flow
- Generates appropriate responses
- Handles quest-related dialog

### StateManager
- Maintains game state
- Validates state changes
- Manages state persistence

### Blockchain
- Stores permanent state
- Validates transactions
- Ensures data integrity

## Key Interactions

1. **Quest Discovery**
   - Player requests available quests
   - System checks eligibility
   - Governor provides quest options

2. **Quest Initiation**
   - Player starts quest
   - System validates requirements
   - Dialog engine begins quest narrative

3. **Progress Tracking**
   - Player completes objectives
   - System updates state
   - Blockchain confirms changes

4. **Quest Completion**
   - System validates completion
   - Updates reputation
   - Distributes rewards

## Error Handling

The sequence includes implicit error handling:
- Requirement validation
- State verification
- Transaction confirmation
- Progress validation

## State Management

All state changes are:
1. Validated locally
2. Submitted to blockchain
3. Confirmed before proceeding
4. Synchronized across components 