# TAP Protocol Architecture Diagrams

## System Overview

```mermaid
graph TB
    subgraph "Bitcoin L1"
        BTC["Bitcoin Network"]
        TAP["TAP Protocol Layer"]
        TRAC["TRAC Indexer"]
    end

    subgraph "Token Layer"
        HT["Hypertokens"]
        GT["Governor Tokens"]
        AT["Artifact Tokens"]
        WT["Wisdom Tokens"]
    end

    subgraph "Game Layer"
        QS["Quest System"]
        PS["Player State"]
        GS["Governor State"]
    end

    BTC --> TAP
    TAP --> HT
    TAP --> GT
    TAP --> AT
    TAP --> WT
    
    HT --> QS
    HT --> PS
    HT --> GS
    
    TRAC --> |"Index"| TAP
    TRAC --> |"Monitor"| HT
```

## Token State Transitions

```mermaid
stateDiagram-v2
    [*] --> Inactive
    Inactive --> Active: Governor Activation
    Active --> InProgress: Player Starts
    InProgress --> Completed: Success
    InProgress --> Failed: Failure
    Failed --> Retry: Governor Allows
    Retry --> InProgress: Player Restarts
    Completed --> [*]
```

## Data Flow Architecture

```mermaid
flowchart TD
    subgraph "Bitcoin L1 Operations"
        L1["Bitcoin L1"] --> TAP["TAP Protocol"]
        TAP --> TI["TRAC Indexer"]
    end

    subgraph "Token Management"
        TI --> TokenOps["Token Operations"]
        TokenOps --> StateUpdate["State Updates"]
        TokenOps --> EventEmit["Event Emission"]
    end

    subgraph "Game Logic"
        StateUpdate --> QuestLogic["Quest Logic"]
        StateUpdate --> WisdomLogic["Wisdom System"]
        StateUpdate --> ArtifactLogic["Artifact System"]
    end

    subgraph "Player Interaction"
        QuestLogic --> PlayerState["Player State"]
        WisdomLogic --> PlayerState
        ArtifactLogic --> PlayerState
    end

    PlayerState --> TokenOps
```

## Governor Permission Model

```mermaid
graph TD
    subgraph "Governor Permissions"
        GP["Governor Profile"] --> QP["Quest Permissions"]
        GP --> WP["Wisdom Permissions"]
        GP --> AP["Artifact Permissions"]
    end

    subgraph "Quest Management"
        QP --> |"Can Create"| QC["Create Quest"]
        QP --> |"Can Modify"| QM["Modify Inactive"]
        QP --> |"Can Review"| QR["Review Completion"]
    end

    subgraph "Wisdom System"
        WP --> |"Can Teach"| WT["Teach Wisdom"]
        WP --> |"Can Verify"| WV["Verify Mastery"]
        WP --> |"Can Grant"| WG["Grant Tokens"]
    end

    subgraph "Artifact Control"
        AP --> |"Can Create"| AC["Create Artifact"]
        AP --> |"Can Bind"| AB["Bind to Player"]
        AP --> |"Can Activate"| AA["Activate Powers"]
    end
```

## Storage Architecture

```mermaid
graph LR
    subgraph "L1 Storage"
        L1S["L1 Storage"] --> QD["Quest Data<br/>1024 bytes"]
        L1S --> WD["Wisdom Data<br/>512 bytes"]
        L1S --> AD["Artifact Data<br/>768 bytes"]
    end

    subgraph "TRAC Index"
        TI["TRAC Index"] --> QI["Quest Index"]
        TI --> WI["Wisdom Index"]
        TI --> AI["Artifact Index"]
    end

    QD --> |"Index"| QI
    WD --> |"Index"| WI
    AD --> |"Index"| AI
```

## Rate Limiting System

```mermaid
graph TD
    subgraph "Block Limits"
        BL["Block Processing"] --> QL["Quest Limit<br/>10 per block"]
        BL --> WL["Wisdom Limit<br/>20 per block"]
        BL --> AL["Artifact Limit<br/>100 per day"]
    end

    subgraph "Transaction Limits"
        TL["Transaction"] --> SC["State Changes<br/>Max 5"]
        TL --> TT["Token Transfers<br/>Max 3"]
        TL --> EV["Events<br/>Max 10"]
    end

    subgraph "Validation"
        QL --> VS["Validation System"]
        WL --> VS
        AL --> VS
        SC --> VS
        TT --> VS
        EV --> VS
    end
``` 