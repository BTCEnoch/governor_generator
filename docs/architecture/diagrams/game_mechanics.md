# Game Mechanics and Interaction Flow

This diagram illustrates how player actions, game systems, and governor responses interact within the game.

```mermaid
graph TD
    subgraph Player["Player Interaction"]
        Act["Actions"]
        Rep["Reputation"]
        Eng["Energy"]
        Inv["Inventory"]
    end

    subgraph GameSystems["Game Systems"]
        Tar["Tarot System"]
        Div["Divination"]
        Rit["Rituals"]
        Que["Quests"]
    end

    subgraph Governor["Governor Response"]
        Dia["Dialogue"]
        Rew["Rewards"]
        Chl["Challenges"]
        Pro["Progression"]
    end

    Act -->|"influences"| Rep
    Act -->|"consumes"| Eng
    Act -->|"uses"| Inv
    
    Act -->|"triggers"| GameSystems
    GameSystems -->|"generates"| Governor
    Governor -->|"affects"| Player
```

## System Components

### Player Interaction
- **Actions**: Player-initiated activities
- **Reputation**: Standing with governors
- **Energy**: Resource for actions
- **Inventory**: Collected items and artifacts

### Game Systems
- **Tarot System**: Card-based mechanics
- **Divination**: Mystical insight mechanics
- **Rituals**: Ceremonial actions
- **Quests**: Structured challenges

### Governor Response
- **Dialogue**: Interactive conversations
- **Rewards**: Achievement benefits
- **Challenges**: Tests and trials
- **Progression**: Advancement tracking

## Interaction Flow
1. Player initiates actions using energy and inventory items
2. Actions influence reputation and trigger game systems
3. Game systems generate appropriate governor responses
4. Governor responses affect player state and progression 