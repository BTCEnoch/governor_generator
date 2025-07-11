"""
Base classes for mystical systems with Bitcoin integration
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

from ..custom_logging import setup_logger
from ..bitcoin.art_generation import BitcoinArtGenerator

class ValidationResult(BaseModel):
    """Result of data validation"""
    is_valid: bool = Field(..., description="Whether the validation passed")
    data: Any = Field(..., description="The validated data")
    errors: Optional[List[str]] = Field(default=None, description="List of validation errors")

class MysticalAttribute(BaseModel):
    """Attribute for mystical entities"""
    name: str = Field(..., description="Name of the attribute")
    value: Any = Field(..., description="Value of the attribute")
    description: str = Field(..., description="Description of the attribute")

class MysticalEntity(BaseModel):
    """Base class for mystical entities"""
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Entity name")
    attributes: List[MysticalAttribute] = Field(default_factory=list, description="Entity attributes")
    relationships: Dict[str, List[str]] = Field(default_factory=dict, description="Related entity IDs")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class BitcoinMysticalSystem(ABC):
    """Base class for Bitcoin-integrated mystical systems"""
    
    def __init__(self, system_id: str, config: Optional[Dict[str, Any]] = None):
        self.id = system_id
        self.config = config if config is not None else {}
        self.logger = setup_logger(f"mystical_{system_id}")
        self.ordinal_data = {}
        self.inscription_data = {}
        art_config = self.config.get("art_generation", {}) if self.config else {}
        self.art_generator = BitcoinArtGenerator(art_config)
        
    @abstractmethod
    def validate_input(self, data: Any) -> ValidationResult:
        """Validate input data"""
        pass
        
    @abstractmethod
    def format_output(self, result: Any) -> Any:
        """Format output data"""
        pass
        
    @abstractmethod
    def calculate_correspondences(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate mystical correspondences"""
        pass

    def derive_mystical_attributes(self, txid: str) -> List[MysticalAttribute]:
        """Derive mystical attributes from Bitcoin transaction"""
        self.logger.info(f"Deriving mystical attributes from txid: {txid}")
        # Implementation will vary by system
        return []

    def bind_to_ordinal(self, ordinal_id: str) -> None:
        """Bind system to Bitcoin ordinal"""
        self.logger.info(f"Binding to ordinal: {ordinal_id}")
        # Implementation will vary by system
        pass

    def bind_to_inscription(self, inscription_id: str) -> None:
        """Bind system to Bitcoin inscription"""
        self.logger.info(f"Binding to inscription: {inscription_id}")
        # Implementation will vary by system
        pass

    def generate_art(self, data: Dict[str, Any]) -> str:
        """Generate Bitcoin-influenced art"""
        self.logger.info("Generating mystical art")
        try:
            art_config = self.config.get("art_generation", {}) if self.config else {}
            return self.art_generator.generate(
                system_id=self.id,
                mystical_data=data,
                config=art_config
            )
        except Exception as e:
            self.logger.error(f"Art generation failed: {e}")
            return ""

    @abstractmethod
    def get_system_info(self) -> Dict[str, Any]:
        """Return system metadata"""
        pass 