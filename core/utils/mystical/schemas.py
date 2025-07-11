"""
Common schemas for mystical systems
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

class MysticalSystemConfig(BaseModel):
    """Configuration for mystical systems"""
    system_id: str = Field(..., description="Unique identifier for the mystical system")
    name: str = Field(..., description="Human-readable name of the system")
    description: str = Field(..., description="Description of the system's purpose and capabilities")
    version: str = Field(..., description="System version number")
    capabilities: List[str] = Field(default_factory=list, description="List of system capabilities")
    bitcoin_integration: Dict[str, Any] = Field(
        default_factory=dict,
        description="Bitcoin integration settings"
    )

class BitcoinIntegrationConfig(BaseModel):
    """Bitcoin integration configuration"""
    use_ordinals: bool = Field(default=True, description="Whether to use ordinals for randomness")
    use_inscriptions: bool = Field(default=True, description="Whether to use inscriptions for data storage")
    network: str = Field(default="mainnet", description="Bitcoin network to use")
    min_confirmations: int = Field(default=1, description="Minimum confirmations for Bitcoin transactions")

class MysticalCorrespondence(BaseModel):
    """Mystical correspondence between entities"""
    source_id: str = Field(..., description="Source entity ID")
    target_id: str = Field(..., description="Target entity ID")
    correspondence_type: str = Field(..., description="Type of correspondence")
    strength: float = Field(default=1.0, description="Strength of correspondence (0.0 to 1.0)")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Additional attributes")

class MysticalReading(BaseModel):
    """Result of a mystical system reading"""
    reading_id: str = Field(..., description="Unique identifier for the reading")
    system_id: str = Field(..., description="ID of the system that performed the reading")
    timestamp: str = Field(..., description="ISO timestamp of the reading")
    input_data: Dict[str, Any] = Field(..., description="Input data used for the reading")
    results: Dict[str, Any] = Field(..., description="Reading results")
    bitcoin_data: Optional[Dict[str, Any]] = Field(None, description="Associated Bitcoin data")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

@dataclass
class ValidationError:
    """Validation error details"""
    field: str
    error: str
    context: Optional[Dict[str, Any]] = None

@dataclass
class SystemValidation:
    """System validation result"""
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict) 