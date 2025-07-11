"""Schema definitions for Enochian Governor relationships"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class EnochianLetterType(str, Enum):
    """Types of Enochian letters"""
    REGULAR = "regular"
    ELEMENTAL = "elemental"
    SPECIAL = "special"
    KING = "king"
    SENIOR = "senior"

class Direction(str, Enum):
    """Cardinal and ordinal directions"""
    NORTH = "north"
    NORTHEAST = "northeast"
    EAST = "east"
    SOUTHEAST = "southeast"
    SOUTH = "south"
    SOUTHWEST = "southwest"
    WEST = "west"
    NORTHWEST = "northwest"

class RitualPoint(BaseModel):
    """A point in ritual space"""
    x: float = Field(ge=0.0, le=1.0, description="X coordinate (0-1)")
    y: float = Field(ge=0.0, le=1.0, description="Y coordinate (0-1)")
    energy_level: float = Field(ge=0.0, le=1.0, description="Energy level (0-1)")
    element: str = Field(description="Associated element")
    governor_influence: Optional[str] = Field(default=None, description="Influencing Governor")
    aethyr_resonance: str = Field(description="Resonating Aethyr")

class RitualPattern(BaseModel):
    """A pattern formed by ritual points"""
    points: List[RitualPoint] = Field(description="Points forming the pattern")
    pattern_type: str = Field(description="Type of pattern")
    total_energy: float = Field(ge=0.0, description="Total energy of the pattern")
    elements: List[str] = Field(description="Elements involved")
    governors: List[str] = Field(description="Governors involved")
    aethyrs: List[str] = Field(description="Aethyrs involved")
    bitcoin_entropy: str = Field(description="Bitcoin entropy used for validation")

class EnochianLetter(BaseModel):
    """An Enochian letter with its properties"""
    name: str = Field(description="Letter name")
    glyph: str = Field(description="Visual representation")
    type: EnochianLetterType = Field(description="Type of letter")
    numeric_value: int = Field(ge=1, description="Numeric value")
    element: str = Field(description="Associated element")
    power_level: int = Field(ge=1, le=10, description="Power level 1-10")

class EnochianTable(BaseModel):
    """An Enochian Watchtower table"""
    direction: Direction = Field(description="Cardinal direction")
    element: str = Field(description="Associated element")
    king_name: str = Field(description="Name of the King")
    senior_names: List[str] = Field(description="Names of the Seniors")
    kerubic_angels: List[str] = Field(description="Kerubic angel names")
    servient_angels: List[str] = Field(description="Servient angel names")
    grid: List[List[str]] = Field(description="Letter grid")

class GovernorRelationship(BaseModel):
    """Relationship between Governors"""
    source_governor: str = Field(description="Source Governor name")
    target_governor: str = Field(description="Target Governor name")
    relationship_type: str = Field(description="Type of relationship")
    strength: float = Field(ge=0.0, le=1.0, description="Relationship strength")
    description: Optional[str] = Field(default=None, description="Description")
    aethyr_connection: Optional[str] = Field(default=None, description="Connecting Aethyr")

class AethyrProfile(BaseModel):
    """Profile of an Enochian Aethyr"""
    name: str
    number: int
    governors: List[str]
    correspondence: str
    description: str
    ritual_requirements: List[str] = Field(default_factory=list)
    power_centers: List[Dict[str, float]] = Field(default_factory=list)
    influence: float = Field(ge=0, le=1)

class EnochianSystemConfig(BaseModel):
    """Configuration for the Enochian system"""
    output_dir: str = Field(default="./output")
    visualization_cache_ttl: int = Field(default=3600)  # 1 hour in seconds
    bitcoin_node_url: Optional[str] = None
    log_level: str = Field(default="INFO")
    max_cache_size: int = Field(default=1000)  # Maximum number of cached items
    cache_cleanup_interval: int = Field(default=86400)  # 24 hours in seconds

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
    """Types of interactions between Governors"""
    TEACHING = "TEACHING"
    EMPOWERMENT = "EMPOWERMENT"
    TRANSFORMATION = "TRANSFORMATION"
    OPPOSITION = "OPPOSITION"
    SYNTHESIS = "SYNTHESIS"

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

    class Config:
        """Pydantic configuration"""
        arbitrary_types_allowed = True
        validate_assignment = True
        allow_population_by_field_name = True
        extra = "forbid"

    def __getitem__(self, key: str) -> Any:
        """Support dictionary-like access to properties"""
        if key == "color":
            return {
                "r": self.color.r,
                "g": self.color.g,
                "b": self.color.b
            }
        elif key == "glow" and self.glow:
            return {
                "radius": self.glow.radius,
                "color": {
                    "r": self.glow.color.r,
                    "g": self.glow.color.g,
                    "b": self.glow.color.b
                },
                "intensity": self.glow.intensity
            }
        elif key == "border" and self.border:
            return {
                "width": self.border.width,
                "style": self.border.style,
                "color": {
                    "r": self.border.color.r,
                    "g": self.border.color.g,
                    "b": self.border.color.b
                }
            }
        elif key == "shape" and self.shape:
            return {
                "type": self.shape.type,
                "sides": self.shape.sides,
                "rotation": self.shape.rotation
            }
        elif key == "opacity":
            return self.opacity
        else:
            raise KeyError(f"Unknown property: {key}")

    def __setitem__(self, key: str, value: Any) -> None:
        """Support dictionary-like property updates"""
        if key == "color":
            self.color = ColorRGB(**value)
        elif key == "glow":
            self.glow = GlowEffect(**value) if value else None
        elif key == "border":
            self.border = BorderStyle(**value) if value else None
        elif key == "shape":
            self.shape = ShapeProperties(**value) if value else None
        elif key == "opacity":
            self.opacity = float(value)
        else:
            raise KeyError(f"Unknown property: {key}")

    def __contains__(self, key: str) -> bool:
        """Support 'in' operator"""
        return key in {"color", "opacity", "glow", "border", "shape"}

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {
            "color": {
                "r": self.color.r,
                "g": self.color.g,
                "b": self.color.b
            },
            "opacity": self.opacity
        }
        if self.glow:
            result["glow"] = {
                "radius": self.glow.radius,
                "color": {
                    "r": self.glow.color.r,
                    "g": self.glow.color.g,
                    "b": self.glow.color.b
                },
                "intensity": self.glow.intensity
            }
        if self.border:
            result["border"] = {
                "width": self.border.width,
                "style": self.border.style,
                "color": {
                    "r": self.border.color.r,
                    "g": self.border.color.g,
                    "b": self.border.color.b
                }
            }
        if self.shape:
            result["shape"] = {
                "type": self.shape.type,
                "sides": self.shape.sides,
                "rotation": self.shape.rotation
            }
        return result

class GovernorConnection(BaseModel):
    """Connection between two Governors"""
    source_governor: str
    target_governor: str
    connection_type: ConnectionType
    strength: float = Field(ge=0, le=1)
    attributes: List[str] = Field(default_factory=list)
    bitcoin_verification: Optional[str] = None

class ResonancePattern(BaseModel):
    """Pattern of resonance between Governors"""
    governors: List[str]
    pattern_type: ResonanceType
    intensity: float = Field(ge=0, le=1)
    entropy: Optional[str] = None

    class Config:
        """Pydantic configuration"""
        arbitrary_types_allowed = True
        validate_assignment = True
        allow_population_by_field_name = True
        extra = "forbid"

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {
            "governors": self.governors,
            "pattern_type": self.pattern_type.value,
            "intensity": self.intensity
        }
        if self.entropy:
            result["entropy"] = self.entropy
        return result

class InteractionRule(BaseModel):
    """Rule for Governor interactions"""
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

    class Config:
        """Pydantic configuration"""
        arbitrary_types_allowed = True
        validate_assignment = True
        allow_population_by_field_name = True
        extra = "forbid"

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "governor": self.governor,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "power": self.power
        }

class RelationshipVisualizationCluster(BaseModel):
    """Cluster in the relationship visualization"""
    governors: List[str]
    type: str
    intensity: float = Field(ge=0, le=1)
    visuals: Optional[VisualProperties] = None

    class Config:
        """Pydantic configuration"""
        arbitrary_types_allowed = True
        validate_assignment = True
        allow_population_by_field_name = True
        extra = "forbid"

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {
            "governors": self.governors,
            "type": self.type,
            "intensity": self.intensity
        }
        if self.visuals:
            result["visuals"] = self.visuals.dict()
        return result

class RelationshipVisualization(BaseModel):
    """Visualization of Governor relationships"""
    nodes: List[RelationshipVisualizationNode]
    edges: List[Dict[str, Any]]
    clusters: List[RelationshipVisualizationCluster]
    entropy: str

    class Config:
        """Pydantic configuration"""
        arbitrary_types_allowed = True
        validate_assignment = True
        allow_population_by_field_name = True
        extra = "forbid"

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "nodes": [node.dict() for node in self.nodes],
            "edges": self.edges,
            "clusters": [cluster.dict() for cluster in self.clusters],
            "entropy": self.entropy
        }

class RelationshipProfile(BaseModel):
    """Complete profile of Governor relationships"""
    governors: List[str] = Field(default_factory=list)
    connections: List[GovernorConnection] = Field(default_factory=list)
    resonance_patterns: List[ResonancePattern] = Field(default_factory=list)
    interaction_rules: List[InteractionRule] = Field(default_factory=list)
    visualization: Optional[RelationshipVisualization] = None
    bitcoin_block_hash: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration"""
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        validate_assignment = True
        allow_population_by_field_name = True
        extra = "forbid"

class ValidationResult(BaseModel):
    """Result of a validation check"""
    is_valid: bool
    errors: List[str]
    data: Optional[Dict[str, Any]] = None 