"""
Game Asset Schemas
Data structures for artifacts, rewards, and tokenomics
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Literal, Union
from enum import Enum
import uuid
from datetime import datetime

class AssetType(Enum):
    """Types of game assets"""
    ARTIFACT = "artifact"
    CONSUMABLE = "consumable"
    CURRENCY = "currency"
    KNOWLEDGE = "knowledge"
    POWER = "power"
    TOKEN = "token"
    BADGE = "badge"
    BLESSING = "blessing"

class AssetRarity(Enum):
    """Rarity levels for assets"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"
    DIVINE = "divine"

class ElementalAffinity(Enum):
    """Elemental affinities for assets"""
    FIRE = "fire"
    WATER = "water"
    AIR = "air"
    EARTH = "earth"
    SPIRIT = "spirit"
    VOID = "void"
    BALANCE = "balance"

class AssetSource(Enum):
    """How an asset can be obtained"""
    QUESTLINE_REWARD = "questline_reward"
    GOVERNOR_GIFT = "governor_gift"
    RITUAL_COMPLETION = "ritual_completion"
    KNOWLEDGE_MASTERY = "knowledge_mastery"
    ELEMENTAL_TRIAL = "elemental_trial"
    MYSTERY_SOLVED = "mystery_solved"
    TRANSFORMATION = "transformation"
    DISCOVERY = "discovery"

@dataclass
class AssetEffect:
    """Effects that an asset can provide"""
    type: Literal["stat_boost", "ability_grant", "protection", "enhancement", "unlock"]
    name: str
    description: str
    magnitude: float
    duration: Optional[int] = None  # minutes, None for permanent
    conditions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AssetRequirement:
    """Requirements to use or obtain an asset"""
    type: Literal["level", "element", "knowledge", "achievement", "governor_favor"]
    value: Union[str, int, float]
    description: str

@dataclass
class GameAsset:
    """Base game asset - artifacts, consumables, etc."""
    id: str
    name: str
    description: str
    type: AssetType
    rarity: AssetRarity
    
    # Properties
    elemental_affinity: Optional[ElementalAffinity] = None
    effects: List[AssetEffect] = field(default_factory=list)
    requirements: List[AssetRequirement] = field(default_factory=list)
    
    # Acquisition
    sources: List[AssetSource] = field(default_factory=list)
    created_by_governor: Optional[str] = None
    creation_questline: Optional[str] = None
    
    # Economics
    base_value: int = 100
    trade_value: Optional[int] = None
    is_tradeable: bool = True
    is_consumable: bool = False
    max_stack: int = 1
    
    # Metadata
    lore_text: str = ""
    flavor_text: str = ""
    image_url: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Generate ID if not provided"""
        if not self.id:
            self.id = str(uuid.uuid4())

@dataclass
class TokenomicsConfig:
    """Configuration for token economics"""
    # Base token parameters
    base_token_name: str = "Wisdom"
    base_token_symbol: str = "WIS"
    base_token_decimals: int = 8
    
    # Reward rates (tokens per action)
    questline_completion_base: int = 100
    encounter_completion_base: int = 10
    knowledge_mastery_base: int = 50
    governor_interaction_base: int = 25
    
    # Difficulty multipliers
    difficulty_multipliers: Dict[str, float] = field(default_factory=lambda: {
        "novice": 1.0,
        "apprentice": 1.5,
        "adept": 2.0,
        "master": 3.0,
        "grandmaster": 5.0
    })
    
    # Rarity multipliers for rewards
    rarity_multipliers: Dict[str, float] = field(default_factory=lambda: {
        "common": 1.0,
        "uncommon": 2.0,
        "rare": 5.0,
        "epic": 10.0,
        "legendary": 25.0,
        "mythic": 50.0,
        "divine": 100.0
    })
    
    # Token sinks (what consumes tokens)
    token_sinks: Dict[str, int] = field(default_factory=lambda: {
        "hint_request": 10,
        "retry_encounter": 5,
        "skip_requirement": 50,
        "boost_reward": 25,
        "artifact_enhancement": 100
    })

@dataclass
class PlayerAssetInventory:
    """Player's asset inventory"""
    player_id: str
    assets: Dict[str, int] = field(default_factory=dict)  # asset_id -> quantity
    tokens: Dict[str, int] = field(default_factory=dict)  # token_type -> amount
    
    # Statistics
    total_assets_acquired: int = 0
    total_tokens_earned: int = 0
    total_tokens_spent: int = 0
    rarest_asset_owned: Optional[AssetRarity] = None
    
    # Metadata
    last_updated: datetime = field(default_factory=datetime.now)
    achievements: List[str] = field(default_factory=list)
    
    def add_asset(self, asset_id: str, quantity: int = 1):
        """Add asset to inventory"""
        if asset_id in self.assets:
            self.assets[asset_id] += quantity
        else:
            self.assets[asset_id] = quantity
        self.total_assets_acquired += quantity
        self.last_updated = datetime.now()
    
    def remove_asset(self, asset_id: str, quantity: int = 1) -> bool:
        """Remove asset from inventory, returns True if successful"""
        if asset_id in self.assets and self.assets[asset_id] >= quantity:
            self.assets[asset_id] -= quantity
            if self.assets[asset_id] == 0:
                del self.assets[asset_id]
            self.last_updated = datetime.now()
            return True
        return False
    
    def add_tokens(self, token_type: str, amount: int):
        """Add tokens to inventory"""
        if token_type in self.tokens:
            self.tokens[token_type] += amount
        else:
            self.tokens[token_type] = amount
        self.total_tokens_earned += amount
        self.last_updated = datetime.now()
    
    def spend_tokens(self, token_type: str, amount: int) -> bool:
        """Spend tokens, returns True if successful"""
        if token_type in self.tokens and self.tokens[token_type] >= amount:
            self.tokens[token_type] -= amount
            self.total_tokens_spent += amount
            self.last_updated = datetime.now()
            return True
        return False

@dataclass
class AssetTemplate:
    """Template for generating assets"""
    type: AssetType
    rarity: AssetRarity
    name_patterns: List[str]
    description_patterns: List[str]
    effect_templates: List[Dict[str, Any]]
    elemental_affinities: List[ElementalAffinity]
    source_weights: Dict[AssetSource, float]  # Probability weights
    base_value_range: tuple[int, int]
    tags: List[str] = field(default_factory=list) 