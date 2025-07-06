# Core Architecture Diagram

This diagram illustrates the fundamental architecture of the Enochian Governor Generation system, showing the relationship between major components.

```mermaid
graph TD
    LH["🏛️ THE LIGHTHOUSE<br/>Knowledge Base"]
    GA["👑 GOVERNOR ANGELS<br/>91 Unique AI Entities"]
    GC["🎮 GAME CONTENT<br/>Storylines/Events/Challenges"]
    IE["🌐 INTERACTIVE EXPERIENCES<br/>Web/Game Interfaces"]
    
    LH -->|"Feeds wisdom to"| GA
    GA -->|"Generate"| GC
    GC -->|"Delivered through"| IE

    subgraph Knowledge["Knowledge Sources"]
        MT["18 Mystical Traditions"]
        KE["200+ Knowledge Entries"]
        MT --- KE
    end

    Knowledge -->|"Powers"| LH
```

## Component Description

- **THE LIGHTHOUSE (Knowledge Base)**: Central repository of mystical wisdom from 18 traditions
- **GOVERNOR ANGELS**: 91 unique AI entities that generate content and interact with players
- **GAME CONTENT**: Generated storylines, events, challenges, and riddles
- **INTERACTIVE EXPERIENCES**: Web and game interfaces for player interaction 