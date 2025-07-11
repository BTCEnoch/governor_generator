"""
Schema definitions for Enochian Governor relationships
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class ColorRGB(BaseModel):
    """RGB color values"""
    r: int = Field(ge=0, le=255)
    g: int = Field(ge=0, le=255)
    b: int = Field(ge=0, le=255)

class GlowEffect(BaseModel):
    """Glow effect properties"""
    radius: float = Field(ge=0)
    color: ColorRGB
    intensity: float = Field(ge=0, le=1)

class BorderStyle(BaseModel):
    """Border style properties"""
    width: float = Field(ge=0)
    style: str
    color: ColorRGB

class ShapeProperties(BaseModel):
    """Shape properties"""
    type: str
    sides: int = Field(ge=3)
    rotation: float = Field(ge=0, lt=360)

class VisualProperties(BaseModel):
    """Visual properties for clusters"""
    color: ColorRGB
    opacity: float = Field(ge=0, le=1)
    glow: Optional[GlowEffect] = None
    border: Optional[BorderStyle] = None
    shape: Optional[ShapeProperties] = None

class ConnectionType(str, Enum):
    """Types of connections between Governors"""
    DIRECT = "DIRECT"
    RESONANT = "RESONANT"
    COMPLEMENTARY = "COMPLEMENTARY"
    OPPOSING = "OPPOSING"
    AETHYRIC = "AETHYRIC"
    ELEMENTAL = "ELEMENTAL"

class ResonanceType(str, Enum):
    """Types of resonance patterns"""
    HARMONIC = "HARMONIC"
    AMPLIFYING = "AMPLIFYING"
    NEUTRAL = "NEUTRAL"
    DAMPENING = "DAMPENING"
    DISSONANT = "DISSONANT"

class InteractionType(str, Enum):
    """Types of Governor interactions"""
    TEACHING = "TEACHING"
    EMPOWERMENT = "EMPOWERMENT"
    TRANSFORMATION = "TRANSFORMATION"
    OPPOSITION = "OPPOSITION"
    SYNTHESIS = "SYNTHESIS"

class ValidationResult(BaseModel):
    """Validation result with data and messages"""
    data: Dict[str, Any] = Field(default_factory=dict)
    is_valid: bool
    errors: Optional[List[str]] = None
    message: Optional[str] = None

class GovernorConnection(BaseModel):
    """Connection between two Governors"""
    source_governor: str
    target_governor: str
    connection_type: ConnectionType
    strength: float
    shared_attributes: List[str]
    bitcoin_verification: str

class ResonancePattern(BaseModel):
    """Resonance pattern between Governors"""
    governors: List[str]
    pattern_type: ResonanceType
    intensity: float
    bitcoin_entropy: str

class InteractionRule(BaseModel):
    """Rule governing Governor interactions"""
    rule_type: InteractionType
    conditions: Dict[str, float]
    effects: Dict[str, float]
    priority: int
    description: str

class RelationshipVisualizationNode(BaseModel):
    """Node in the relationship visualization"""
    governor: str
    x: float
    y: float
    z: float
    power: float

class RelationshipVisualizationCluster(BaseModel):
    """Cluster in the relationship visualization"""
    governors: List[str]
    type: str
    intensity: float
    visuals: Optional[VisualProperties] = None

class RelationshipVisualization(BaseModel):
    """Visualization of governor relationships"""
    nodes: List[RelationshipVisualizationNode]
    edges: List[Dict[str, float]]
    clusters: List[RelationshipVisualizationCluster]
    dimensions: int = Field(default=2)
    entropy: str

class RelationshipProfile(BaseModel):
    """Complete Governor relationship profile"""
    connections: List[GovernorConnection]
    resonance_patterns: List[ResonancePattern]
    interaction_rules: List[InteractionRule]
    visualization: RelationshipVisualization
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    bitcoin_block_hash: str 