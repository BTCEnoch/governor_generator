# Dialog System Flow

## Dialog Interaction Flow
```mermaid
sequenceDiagram
    participant P as Player
    participant C as Client
    participant D as Dialog Engine
    participant K as Knowledge Base
    participant G as Governor Profile
    participant S as State Manager
    participant B as Bitcoin Chain

    P->>C: Initiate Dialog
    C->>D: Request Dialog Start
    D->>G: Load Governor Profile
    G-->>D: Return Profile
    D->>K: Fetch Relevant Knowledge
    K-->>D: Return Knowledge
    D->>S: Get Current State
    S-->>D: Return State
    D-->>C: Initial Dialog
    C-->>P: Display Dialog

    Note over P,B: Dialog Loop

    P->>C: Choose Response
    C->>D: Process Response
    D->>K: Check Knowledge Requirements
    K-->>D: Knowledge Status
    D->>G: Generate Governor Response
    G-->>D: Response Content
    D->>S: Update State
    S->>B: Record State Change
    B-->>S: Confirm Transaction
    S-->>D: State Updated
    D-->>C: Next Dialog
    C-->>P: Show Response

    Note over P,B: Knowledge Unlock

    P->>C: Reach Knowledge Threshold
    C->>D: Check Progress
    D->>K: Unlock New Content
    K->>B: Record Unlock
    B-->>K: Confirm Transaction
    K-->>D: Content Available
    D-->>C: Update Available Knowledge
    C-->>P: Show New Content
```

## Dialog State Flow
```mermaid
stateDiagram-v2
    [*] --> Initial
    Initial --> Active: Start Dialog
    Active --> Knowledge: Knowledge Check
    Knowledge --> Response: Generate Response
    Response --> Active: Continue Dialog
    Active --> Complete: End Dialog
    Complete --> [*]

    state Active {
        [*] --> ProcessInput
        ProcessInput --> GenerateResponse
        GenerateResponse --> UpdateState
        UpdateState --> [*]
    }

    state Knowledge {
        [*] --> CheckRequirements
        CheckRequirements --> FetchContent
        FetchContent --> ValidateAccess
        ValidateAccess --> [*]
    }
```

## Component Descriptions

### Participants
- **Player**: End user interacting with the system
- **Client**: Local game client handling UI
- **Dialog Engine**: Core conversation management
- **Knowledge Base**: Content and wisdom storage
- **Governor Profile**: Governor personality and traits
- **State Manager**: Game state tracking
- **Bitcoin Chain**: Permanent record storage

### Key Interactions
1. **Dialog Initiation**
   - Player starts conversation
   - System loads governor profile
   - Relevant knowledge is fetched
   - Current state is checked
   - Initial dialog is presented

2. **Response Processing**
   - Player chooses response
   - System processes choice
   - Knowledge requirements checked
   - Governor response generated
   - State updated and recorded
   - Next dialog presented

3. **Knowledge Unlocking**
   - Progress threshold reached
   - New content unlocked
   - Unlock recorded on-chain
   - Content made available
   - Player notified

### State Transitions
- **Initial**: Starting state
- **Active**: Ongoing dialog
- **Knowledge**: Content checks
- **Response**: Response generation
- **Complete**: Dialog end

### On-Chain Integration
- Dialog progress recorded
- Knowledge unlocks tracked
- State changes permanent
- Progress verifiable
- Content accessibility managed

# Dialog Flow Sequence Diagram

## Overview
This diagram illustrates the sequence of interactions between system components during dialog generation and processing.

## Diagram

```mermaid
sequenceDiagram
    participant Player
    participant DialogEngine
    participant Governor
    participant StateManager
    participant KnowledgeBase
    participant Blockchain
    
    Player->>DialogEngine: Initiate Dialog
    DialogEngine->>StateManager: Get Dialog Context
    StateManager-->>DialogEngine: Return Context
    DialogEngine->>Governor: Get Initial Response
    Governor->>KnowledgeBase: Query Relevant Knowledge
    KnowledgeBase-->>Governor: Return Knowledge
    Governor-->>DialogEngine: Generate Response
    DialogEngine-->>Player: Display Response
    
    loop Dialog Exchange
        Player->>DialogEngine: Send Input
        DialogEngine->>DialogEngine: Classify Intent
        DialogEngine->>StateManager: Get Updated Context
        StateManager-->>DialogEngine: Return Context
        
        alt Quest Related
            DialogEngine->>Governor: Get Quest Dialog
            Governor->>KnowledgeBase: Query Quest Knowledge
            KnowledgeBase-->>Governor: Return Knowledge
            Governor-->>DialogEngine: Generate Quest Response
            
        else Lore Related
            DialogEngine->>KnowledgeBase: Direct Knowledge Query
            KnowledgeBase-->>DialogEngine: Return Lore
            DialogEngine->>Governor: Format Lore Response
            Governor-->>DialogEngine: Return Formatted Response
            
        else General Conversation
            DialogEngine->>Governor: Get Contextual Response
            Governor-->>DialogEngine: Generate Response
        end
        
        DialogEngine->>StateManager: Update Dialog History
        StateManager->>Blockchain: Submit Dialog State
        Blockchain-->>StateManager: Confirm State
        DialogEngine-->>Player: Display Response
    end
    
    Player->>DialogEngine: End Dialog
    DialogEngine->>StateManager: Save Final State
    StateManager->>Blockchain: Submit Final State
    Blockchain-->>StateManager: Confirm State
    DialogEngine->>Governor: Update Relationship
    Governor->>StateManager: Update Reputation
    StateManager->>Blockchain: Submit Reputation Change
    Blockchain-->>StateManager: Confirm Change
    DialogEngine-->>Player: Display Dialog Summary
```

## Component Descriptions

### Player
- Initiates conversations
- Provides input/responses
- Receives governor responses
- Makes dialog choices

### DialogEngine
- Manages conversation flow
- Classifies player intent
- Coordinates responses
- Maintains dialog context

### Governor
- Provides personality-driven responses
- Accesses relevant knowledge
- Maintains conversation coherence
- Tracks relationship development

### StateManager
- Maintains dialog state
- Tracks conversation history
- Manages reputation changes
- Ensures state persistence

### KnowledgeBase
- Stores mystical knowledge
- Provides lore responses
- Supports quest information
- Maintains cross-references

### Blockchain
- Stores permanent dialog records
- Validates state changes
- Ensures data integrity
- Tracks reputation changes

## Key Interactions

1. **Dialog Initiation**
   - Player starts conversation
   - System establishes context
   - Governor prepares initial response

2. **Intent Classification**
   - System analyzes player input
   - Determines response type
   - Routes to appropriate handler

3. **Response Generation**
   - Governor accesses knowledge
   - Applies personality traits
   - Generates contextual response

4. **State Management**
   - Dialog history is recorded
   - State changes are validated
   - Blockchain confirms changes

## Dialog Categories

### Quest Dialog
- Objective-related responses
- Progress updates
- Reward information
- Quest guidance

### Lore Dialog
- Mystical knowledge sharing
- Tradition explanations
- Historical context
- Symbolic meanings

### General Dialog
- Personality-driven responses
- Relationship building
- Casual conversation
- Character development

## Error Handling

The sequence includes handling for:
- Invalid inputs
- Context mismatches
- Knowledge gaps
- State conflicts
- Network issues

## State Persistence

All dialog interactions are:
1. Validated for context
2. Recorded in history
3. Persisted to blockchain
4. Available for future reference 