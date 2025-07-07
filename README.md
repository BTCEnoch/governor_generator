# 🏛️ Enochian Governor Generation System

## Overview

The Enochian Governor Generation system is a sophisticated AI-powered game engine that creates mystical storylines, challenges, and interactive experiences using authentic sacred wisdom from 18 mystical traditions. The system runs entirely on Bitcoin L1 without web dependencies, using Ordinals and TAP protocols for immutable content storage.

## Core Features

1. **👑 Governor Angels (91 Unique AI Entities)**
   - Unique personality traits and specializations
   - Authentic Enochian names and lore
   - Dynamic interaction patterns
   - Mystical knowledge integration

2. **🏛️ The Lighthouse (Knowledge Base)**
   - 18 mystical traditions
   - Verified sacred wisdom
   - Cross-referenced knowledge entries
   - Cultural authenticity preservation

3. **🎮 Quest System**
   - Dynamic storyline generation
   - Progressive difficulty scaling
   - Multiple challenge types:
     - Rituals
     - Puzzles
     - Riddles
     - Wisdom trials
   - Energy-based progression
   - Achievement tracking

4. **⛓️ Bitcoin L1 Integration**
   - Ordinals for content storage
   - TAP protocol implementation
   - Immutable game state
   - On-chain achievements
   - Zero web dependencies

## Project Structure

```
governor_generator/
├── core/                   # Core system components
│   ├── governors/         # Governor generation & profiles
│   ├── lighthouse/        # Knowledge base & wisdom retrieval
│   ├── questlines/        # Quest & challenge system
│   └── utils/            # Shared utilities
├── engines/              # Processing engines
│   ├── mystical_systems/ # Tarot, Kabbalah, etc.
│   ├── storyline_generation/ # Dynamic narratives
│   └── trait_generation/ # Governor traits
├── data/                # Data and resources
│   ├── canon/          # Sacred source materials
│   ├── governors/      # Governor profiles & indexes
│   ├── knowledge/      # Wisdom traditions
│   └── questlines/     # Quest templates
└── tests/              # Comprehensive test suite
```

## Setup & Development

### Prerequisites
- Python 3.9+
- Bitcoin Core (for TAP protocol)
- PowerShell (Windows) or Bash (Unix)

### Environment Setup

```powershell
# Clone repository
git clone <repository_url>
cd governor_generator

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Unix

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Create `.env` file in project root:
```env
# Anthropic API Configuration
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_MODEL=claude-3-opus-20240229
ANTHROPIC_MAX_TOKENS=4096
ANTHROPIC_TEMPERATURE=0.7

# Batch Processing
BATCH_SIZE=10
BATCH_DELAY=1
```

### Running Tests

```powershell
# Full test suite
python -m pytest

# Specific components
python -m pytest tests/core/questlines/
python -m pytest tests/engines/mystical_systems/
```

## Development Standards

### Code Quality
- PEP 8 compliance
- Type hints required
- Comprehensive docstrings
- Error handling & logging
- Performance optimization

### Testing Requirements
- Unit tests for all components
- Integration tests for systems
- Cultural accuracy validation
- Performance benchmarks
- Edge case coverage

### Documentation
- Clear function documentation
- Architecture diagrams
- Implementation guides
- Change tracking
- Cultural context notes

## Quest System Architecture

### Components
1. **Quest Template Manager**
   - Template generation
   - Difficulty scaling
   - Challenge type management
   - Reward calculation

2. **Story Tree**
   - Branching narratives
   - State management
   - Progress tracking
   - Achievement system

3. **State Manager**
   - Runtime state handling
   - Progress persistence
   - Challenge tracking
   - Energy management

4. **Reward System**
   - On-chain achievements
   - Wisdom token distribution
   - Reputation tracking
   - Energy refunds

## Cultural Respect Guidelines

1. **Source Material**
   - Academic verification
   - Cultural context preservation
   - Historical accuracy
   - Respectful presentation

2. **Content Generation**
   - Authentic representation
   - Cultural sensitivity
   - Educational value
   - Spiritual integrity

## Contributing

1. Fork repository
2. Create feature branch
3. Implement changes with tests
4. Submit pull request
5. Ensure cultural respect

## License

This project is licensed under the MIT License.

---

**🏛️ Preserving humanity's sacred wisdom for eternity through innovative technology and respectful implementation. ⛓️✨**

## API Key Setup

1. Create a `.env` file in the project root with the following content:
```env
# Anthropic API Configuration
ANTHROPIC_API_KEY=your_api_key_here

# API Settings
ANTHROPIC_MODEL=claude-3-opus-20240229
ANTHROPIC_MAX_TOKENS=4096
ANTHROPIC_TEMPERATURE=0.7

# Batch Processing Settings
BATCH_SIZE=10
BATCH_DELAY=1  # Delay between batches in seconds
```

2. Replace `your_api_key_here` with your actual Anthropic API key