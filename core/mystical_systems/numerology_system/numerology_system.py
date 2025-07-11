"""
Numerology System Implementation with Bitcoin Integration
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import ValidationError

from core.utils.mystical.base import BitcoinMysticalSystem, MysticalAttribute, ValidationResult
from core.utils.mystical import BitcoinIntegration
from core.utils.custom_logging import setup_logger
from .schemas import NumerologySystem as NumerologyType, NumerologyProfile, NumerologySystemConfig
from .data.numerology_database import (
    calculate_life_path_number,
    calculate_destiny_number,
    calculate_soul_urge_number,
    calculate_personality_number,
    calculate_birth_day_number,
    calculate_current_year_number
)

logger = setup_logger("numerology_system")

class NumerologySystem(BitcoinMysticalSystem):
    """Bitcoin-integrated numerology system implementation"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the numerology system with optional configuration"""
        try:
            config_dict = config or {}
            validated_config = NumerologySystemConfig(**config_dict)
            super().__init__("numerology", validated_config.dict())
            self.bitcoin = BitcoinIntegration(config_dict.get("bitcoin_integration"))
            self.system_type = validated_config.system_type
            logger.info(f"Initialized Bitcoin-integrated NumerologySystem ({self.system_type})")
        except ValidationError as e:
            logger.error(f"Failed to initialize NumerologySystem: {e}")
            raise
            
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            "system_id": "numerology_system_v1",
            "name": "Numerology System",
            "description": "A Bitcoin-integrated numerology system for mystical analysis",
            "version": "1.0.0",
            "system_type": self.system_type,
            "capabilities": [
                "life_path_analysis",
                "destiny_calculation",
                "soul_urge_analysis",
                "bitcoin_integration",
                "mystical_correspondences"
            ],
            "supported_inputs": [
                "name",
                "birthdate",
                "txid",
                "ordinal_id",
                "inscription_id"
            ],
            "supported_outputs": [
                "numerology_profile",
                "mystical_attributes",
                "bitcoin_resonances"
            ]
        }
        
    def validate_input(self, data: Any) -> ValidationResult:
        """Validate input data"""
        logger.info("Validating input data")
        errors = []
        
        if not isinstance(data, dict):
            return ValidationResult(
                is_valid=False,
                data=data,
                errors=["Input must be a dictionary"]
            )
            
        # Check required fields
        required_fields = ["name", "birthdate"]
        for field in required_fields:
            if field not in data:
                errors.append(f"{field} must be provided")
                
        # Validate birthdate format
        if "birthdate" in data:
            try:
                datetime.strptime(data["birthdate"], "%Y-%m-%d")
            except ValueError:
                errors.append("Birthdate must be in YYYY-MM-DD format")
                
        # Validate Bitcoin-related fields
        if "txid" in data:
            if not self.bitcoin.validate_bitcoin_data(txid=data["txid"]):
                errors.append("Invalid Bitcoin transaction ID")
                
        if "ordinal_id" in data:
            if not self.bitcoin.validate_bitcoin_data(ordinal_id=data["ordinal_id"]):
                errors.append("Invalid ordinal ID")
                
        if "inscription_id" in data:
            if not self.bitcoin.validate_bitcoin_data(inscription_id=data["inscription_id"]):
                errors.append("Invalid inscription ID")
                
        return ValidationResult(
            is_valid=len(errors) == 0,
            data=data,
            errors=errors if errors else None
        )
        
    def format_output(self, result: NumerologyProfile) -> Dict[str, Any]:
        """Format output data"""
        logger.info("Formatting numerology profile output")
        try:
            return result.dict()
        except Exception as e:
            logger.error(f"Error formatting output: {e}")
            return {}
            
    def calculate_correspondences(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate mystical correspondences including Bitcoin resonances"""
        logger.info("Calculating numerology correspondences")
        correspondences = {}
        
        try:
            # Calculate core numbers
            correspondences["life_path_number"] = calculate_life_path_number(
                data["birthdate"],
                system=self.system_type
            )
            correspondences["destiny_number"] = calculate_destiny_number(
                data["name"],
                system=self.system_type
            )
            correspondences["soul_urge_number"] = calculate_soul_urge_number(
                data["name"],
                system=self.system_type
            )
            correspondences["personality_number"] = calculate_personality_number(
                data["name"],
                system=self.system_type
            )
            correspondences["birth_day_number"] = calculate_birth_day_number(
                data["birthdate"],
                system=self.system_type
            )
            correspondences["current_year_number"] = calculate_current_year_number(
                data["birthdate"],
                system=self.system_type
            )
            
            # Get Bitcoin-influenced scores if available
            txid = data.get("txid")
            if txid and self.config.get("use_bitcoin_influence", True):
                bitcoin_attributes = self.derive_mystical_attributes(txid)
                correspondences["bitcoin_resonance"] = bitcoin_attributes[0].value if bitcoin_attributes else None
                correspondences["chain_harmony"] = bitcoin_attributes[1].value if len(bitcoin_attributes) > 1 else None
                
            logger.info("Successfully calculated correspondences")
            return correspondences
            
        except Exception as e:
            logger.error(f"Error calculating correspondences: {e}")
            return {}
            
    def generate_profile(self, data: Dict[str, Any]) -> NumerologyProfile:
        """Generate Bitcoin-integrated numerology profile"""
        logger.info("Generating numerology profile")
        
        try:
            # Validate input
            validation = self.validate_input(data)
            if not validation.is_valid:
                raise ValueError(f"Invalid input data: {validation.errors or []}")
                
            # Calculate correspondences
            correspondences = self.calculate_correspondences(data)
            if not correspondences:
                raise ValueError("Failed to calculate correspondences")
                
            # Create profile
            profile = NumerologyProfile(
                name=data["name"],
                birthdate=data["birthdate"],
                life_path_number=correspondences["life_path_number"],
                destiny_number=correspondences["destiny_number"],
                soul_urge_number=correspondences["soul_urge_number"],
                personality_number=correspondences["personality_number"],
                birth_day_number=correspondences["birth_day_number"],
                current_year_number=correspondences["current_year_number"],
                bitcoin_resonance=correspondences.get("bitcoin_resonance"),
                chain_harmony=correspondences.get("chain_harmony")
            )
            
            # Add Bitcoin-derived attributes if available
            txid = data.get("txid")
            if txid and self.config.get("use_bitcoin_influence", True):
                profile.attributes.extend(self.derive_mystical_attributes(txid))
                
            # Add ordinal attributes if available
            ordinal_id = data.get("ordinal_id")
            if ordinal_id:
                self.bind_to_ordinal(ordinal_id)
                profile.metadata["ordinal_data"] = self.ordinal_data
                
            # Add inscription attributes if available
            inscription_id = data.get("inscription_id")
            if inscription_id:
                self.bind_to_inscription(inscription_id)
                profile.metadata["inscription_data"] = self.inscription_data
                
            # Generate art if configured
            if self.config.get("generate_art", False):
                art_data = self.generate_art(correspondences)
                if art_data:
                    profile.metadata["art_data"] = art_data
                    
            return profile
            
        except Exception as e:
            logger.error(f"Failed to generate profile: {e}")
            raise 