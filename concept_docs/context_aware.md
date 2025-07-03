# Context-Aware Dialog Engine Architecture
## On-Chain Story Game Dialog System

### Overview
This document outlines the architecture for a Context-Aware Dialog Engine designed for on-chain story games with 91 Enochian Governors. The system combines structured state machines with lightweight language processing to achieve context-awareness and high variability under strict on-chain constraints.

## Core Architecture Components

### 1. State Machine & Story Graph
Each governor encounter is modeled as a directed graph of dialogue **nodes** (states) with conditional branches:

- **Node Structure**: Each node contains narrative snippets or NPC speech
- **Transitions**: Depend on player input or game state  
- **Context Maintenance**: Current node + game state stored on-chain
- **Branching Logic**: Reputation levels, items, secrets gate certain branches
- **Memory System**: Dialog remembers past events by progressing through nodes and flags

**Example Flow:**
```
Introduction Node → [Player Choice] → Riddle Node OR Ritual Node
                                   ↓
                            [Reputation Check] → Advanced Content
```

### 2. On-Chain Dialog Library
All dialogue text and lore stored immutably as ordinal inscriptions on Bitcoin:

- **Compressed Storage**: Text chunks compressed and stored per governor
- **Reference System**: Game stores IDs/indices to on-chain dialogues
- **High Variability**: Multiple response variants for any situation
- **Entropy-Based Selection**: Block hash/nonce selects from response variants
- **Data-Driven Model**: No hard-coded text in logic

**Storage Pattern:**
```
Governor_ID → Dialog_Library → {
  "intro_responses": ["response_1", "response_2", "response_3"],
  "success_praise": ["praise_1", "praise_2", "praise_3"],
  "failure_hints": ["hint_1", "hint_2", "hint_3"]
}
```

### 3. Deterministic Small Models
Two-phase interaction process for flexible input handling:

#### Phase 1: Natural Language Understanding (NLU)
- **Input Classification**: Maps open-ended input to semantic categories
- **Intent Detection**: "riddle_answer", "formal_greeting", "off_topic", etc.
- **Lightweight Processing**: Rule-based classifier or tiny neural network
- **Deterministic Output**: Same input → same classification across all peers

#### Phase 2: State Update
- **Transition Logic**: Based on intent + current node/state
- **Response Selection**: Choose from pre-written variants
- **Consensus**: All peers reach same outcome deterministically

**Processing Pipeline:**
```
Player Input → NLU Classification → Intent Category → State Machine → Response Selection
```

## Natural Language Processing Components

### 1. Token Matching & Regex
- **Keyword Detection**: Simple pattern matching for specific answers
- **Pattern Libraries**: Stored on-chain as part of puzzle data
- **Variation Handling**: Multiple acceptable forms per answer
- **Performance**: Fast, zero-compute-cost processing

### 2. Word Embeddings for Similarity
- **Vector Comparison**: Small pre-trained embedding model
- **Similarity Threshold**: Cosine similarity for concept matching
- **Local Processing**: 50-100 dimensional embeddings
- **Consensus**: Identical embedding lookups across peers

### 3. Lightweight Classification Models
- **Compressed Neural Networks**: Small transformer or LSTM
- **Domain-Specific**: Fine-tuned on fantasy/occult dialog
- **Output Categories**: Limited set of intent labels
- **On-Chain Storage**: Model weights in inscription chunks

### 4. Deterministic Parsing
- **Formal Language**: Mini-grammar for ritual phrases
- **Structure Validation**: Parser checks input format
- **DSL Integration**: Domain-specific language for magical responses
- **Consistency**: Same parser results across all nodes

## Governor Preference Encoding

### 1. Profile Key-Value Pairs
Compact storage of governor preferences:

```json
{
  "tone": "SOLEMN_CRYPTIC",
  "puzzle_style": "METAPHOR", 
  "greeting_preference": "FORMAL",
  "response_style": "RIDDLES",
  "triggers": ["RITUAL_GESTURE", "SACRED_KNOWLEDGE"]
}
```

### 2. Parameterized Language Models
- **Persona Vectors**: Precomputed embeddings from profile traits
- **Context Integration**: Governor preferences fed to NLU model
- **Efficient Processing**: Numeric parameters vs. text prompts
- **Runtime Adaptation**: Model adjusts to governor's style

### 3. Compact Data Structures
- **Token Libraries**: Mini-ontology of player actions
- **Lookup Tables**: Governor preferences as set membership
- **Trait Mapping**: Link personality traits to behaviors
- **O(1) Performance**: Instant preference checking

### 4. Persona Trait Referencing
Leverage existing governor traits for dialog behavior:

```python
if "patient" in governor.traits:
    allow_partial_answers = True
if "meticulous" in governor.traits:
    require_exact_answers = True
if governor.mood == "stern":
    use_curt_responses = True
```

## Fallback Strategies

### 1. Metaphor & Analogy Recognition
- **Symbolic Interpretation**: Check for metaphorical equivalents
- **Concept Matching**: Embedding similarity for figurative language
- **Partial Credit**: Acknowledge metaphors with appropriate responses
- **Creative Encouragement**: Don't penalize symbolic thinking

### 2. Keyword-Based Hints
- **Partial Triggers**: Scan for relevant keywords in failed attempts
- **Progressive Hints**: Guide players toward complete answers
- **Token Checking**: Simple keyword presence detection
- **Interactive Feedback**: Dynamic responses to partial correctness

### 3. Intent Classification & Slot Filling
Categorize unmatched input by general intent:

- **Questions**: "I pose the questions here, Seeker"
- **Greetings**: "Pleasantries won't earn you secrets"
- **Nonsense**: "Your words stray from the matter at hand"
- **Insults**: Reputation penalty + angry response
- **Offerings**: Extract item slot, check against desired tribute

### 4. Branched Failure Outcomes
- **Tiered Responses**: First failure → hint, repeated failures → clearer clues
- **Progressive Revelation**: Gradual unveiling of answers
- **State Tracking**: Failure counters trigger different responses
- **Player Assistance**: Prevent permanent puzzle blocking

### 5. Default Safe Response
- **Catch-All**: Generic response for truly unexpected input
- **Character Voice**: Governor-specific default lines
- **Immersion Maintenance**: Avoid awkward silence
- **Player Feedback**: Signal that input wasn't understood

## Dialog Logic Models

### Governor Interaction Types

#### 1. Riddle Keeper (Puzzle Challenge)
```python
def riddle_keeper_logic(player_input, expected_answer):
    if exact_match(player_input, expected_answer):
        return success_response(), +2_rep
    elif semantic_similarity(player_input, expected_answer) > 0.8:
        return partial_success(), +1_rep
    elif contains_keywords(player_input, expected_answer):
        return hint_response(), 0_rep
    else:
        return failure_response(), 0_rep
```

#### 2. Ceremonial Governor (Ritual Greeting)
```python
def ceremonial_logic(player_input, required_formality):
    formality_score = analyze_formality(player_input)
    if formality_score >= required_formality and contains_title(player_input):
        return pleased_response(), +1_rep
    elif is_disrespectful(player_input):
        return rebuke_response(), -1_rep
    else:
        return neutral_response(), 0_rep
```

#### 3. Archetypal Mirror (Tone Matching)
```python
def mirror_logic(player_input, governor_style):
    player_style = analyze_tone(player_input)
    style_match = calculate_style_similarity(player_style, governor_style)
    
    if style_match > 0.9:
        return enthusiastic_response(), +2_rep
    elif style_match > 0.6:
        return approving_response(), +1_rep
    elif is_offensive_mismatch(player_style, governor_style):
        return offended_response(), -1_rep
    else:
        return neutral_response(), 0_rep
```

#### 4. Secret Keeper (Knowledge Check)
```python
def secret_keeper_logic(player_input, required_secret):
    if contains_secret(player_input, required_secret):
        return reveal_lore(), +3_rep
    else:
        return deny_knowledge(), 0_rep
```

#### 5. Tribute Taker (Offering Exchange)
```python
def tribute_logic(player_input, player_inventory, desired_offering):
    offered_item = extract_offering(player_input)
    if offered_item == desired_offering and has_item(player_inventory, offered_item):
        return ritual_success(), +2_rep, consume_item(offered_item)
    elif is_trivial_offering(offered_item):
        return scoff_response(), -1_rep  # if repeated
    else:
        return refuse_response(), 0_rep
```

## Reputation System Integration

### Scoring Mechanics
- **Small Increments**: 1-3 points per interaction
- **Bounded Growth**: Daily interaction limits prevent grinding
- **Meaningful Penalties**: Rare but impactful reputation losses
- **Progressive Unlocks**: New content at reputation thresholds

### Reputation Effects
```python
reputation_thresholds = {
    0: "basic_interactions",
    5: "intermediate_puzzles", 
    10: "true_name_revelation",
    15: "secret_knowledge_sharing",
    20: "advanced_rituals"
}
```

## Technical Implementation

### Data Structures
```python
class DialogNode:
    id: str
    content: List[str]  # Multiple response variants
    transitions: Dict[str, str]  # intent -> next_node_id
    requirements: Dict[str, Any]  # reputation, items, flags
    
class GovernorProfile:
    preferences: Dict[str, str]
    traits: List[str]
    interaction_models: List[str]
    reputation_thresholds: Dict[int, str]

class PlayerState:
    current_node: str
    reputation: Dict[str, int]  # governor_id -> rep_score
    inventory: List[str]
    flags: Set[str]  # story progression flags
```

### Processing Pipeline
```python
def process_interaction(player_input, governor_id, player_state):
    # 1. Load governor profile and current dialog node
    governor = load_governor_profile(governor_id)
    current_node = load_dialog_node(player_state.current_node)
    
    # 2. NLU Processing
    intent = classify_intent(player_input, governor.preferences)
    
    # 3. State Machine Transition
    next_node_id = current_node.transitions.get(intent)
    if not next_node_id:
        return handle_fallback(player_input, governor, current_node)
    
    # 4. Check Requirements
    next_node = load_dialog_node(next_node_id)
    if not meets_requirements(next_node.requirements, player_state):
        return insufficient_requirements_response()
    
    # 5. Generate Response
    response_variant = select_response_variant(next_node.content)
    reputation_change = calculate_reputation_change(intent, governor)
    
    # 6. Update State
    player_state.current_node = next_node_id
    player_state.reputation[governor_id] += reputation_change
    
    return response_variant, reputation_change
```

## Implementation Phases

### Phase 1: Core Infrastructure
- [ ] Dialog node data structures
- [ ] Basic state machine implementation
- [ ] On-chain storage schemas
- [ ] Governor profile system

### Phase 2: NLU Components  
- [ ] Token matching system
- [ ] Embedding similarity calculator
- [ ] Intent classification model
- [ ] Deterministic parsing rules

### Phase 3: Dialog Logic Models
- [ ] Riddle keeper implementation
- [ ] Ceremonial governor logic
- [ ] Archetypal mirror system
- [ ] Secret keeper mechanics
- [ ] Tribute taker functionality

### Phase 4: Fallback Systems
- [ ] Metaphor recognition
- [ ] Keyword-based hints
- [ ] Intent classification fallbacks
- [ ] Default response handlers

### Phase 5: Integration & Testing
- [ ] Reputation system integration
- [ ] On-chain data validation
- [ ] Cross-governor quest linking
- [ ] Performance optimization

This architecture provides a robust foundation for creating rich, context-aware dialog interactions while maintaining the constraints necessary for on-chain consensus and minimal compute requirements. 