# The Lighthouse System Documentation

## Overview
The Lighthouse is the core knowledge and interaction engine powering the Enochian Governor system. It serves as both a repository of mystical wisdom and an intelligent dialog management system that enables meaningful interactions with the 91 Governors.

## Core Components
1. [Knowledge Base Architecture](./knowledge-base/README.md)
2. [Dialog Engine](./dialog-engine/README.md)
3. [Game Loop Manager](./game-loops/README.md)
4. [Implementation Strategy](./implementation/README.md)

## System Architecture
The Lighthouse system is built on three primary pillars:
- **On-Chain Storage**: All knowledge and dialog content is stored immutably on Bitcoin via Ordinal inscriptions
- **P2P Network**: Distributed access and validation through the Trac network
- **TAP Protocol**: Smart contract integration for game mechanics and state management

## Directory Structure
```
lighthouse/
├── knowledge-base/       # Knowledge storage and retrieval system
├── dialog-engine/       # Governor interaction and response generation
├── game-loops/         # Core game mechanics and loops
└── implementation/     # Technical implementation details
```

## Getting Started
- See [Quick Start Guide](./quick-start.md) for development setup
- Review [Architecture Overview](./architecture.md) for system design
- Check [Integration Guide](./integration.md) for connecting to existing systems

## Development Guidelines
1. All content must be blockchain-ready (optimized for on-chain storage)
2. Follow the deterministic dialog generation patterns
3. Maintain cross-reference integrity in the knowledge base
4. Ensure all state changes are TAP-compatible

## Key Features
- Immutable knowledge storage
- Deterministic dialog generation
- State-driven interactions
- Cross-referenced wisdom traditions
- Reputation-gated content access
- Intelligent response selection

## Technical Stack
- TypeScript/Python for core systems
- Bitcoin Ordinals for content storage
- TAP Protocol for smart contracts
- Trac P2P for network layer 