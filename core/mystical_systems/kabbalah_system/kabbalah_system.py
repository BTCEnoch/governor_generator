"""
Kabbalah System Implementation with Bitcoin Integration
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from pydantic import ValidationError, BaseModel

from core.utils.mystical.base import BitcoinMysticalSystem, MysticalAttribute, ValidationResult
from core.utils.mystical import BitcoinIntegration
from core.utils.custom_logging import setup_logger
from .schemas import (
    SefirotPosition,
    Sefirah,
    KabbalahProfile,
    KabbalahSystemConfig
)
from .data.sefirot_database import (
    get_sefirah_by_position,
    get_sefirah_by_number,
    get_sefirot_by_element,
    get_sefirot_by_planet,
    ALL_SEFIROT
)

logger = setup_logger("kabbalah_system")

class KabbalahSystem(BitcoinMysticalSystem):
    """Bitcoin-integrated Kabbalah system implementation"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the Kabbalah system with Bitcoin integration"""
        if config is None:
            config = KabbalahSystemConfig().model_dump()
        validated_config = KabbalahSystemConfig(**config)
        super().__init__("kabbalah", validated_config.model_dump())
        self.bitcoin = BitcoinIntegration(config.get("bitcoin_integration"))
        self.logger = setup_logger("kabbalah_system")
        self.logger.info("Initialized Bitcoin-integrated KabbalahSystem")
            
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            "system_id": "kabbalah_system_v1",
            "name": "Kabbalah System",
            "description": "A Bitcoin-integrated Kabbalah system for mystical analysis and divination",
            "version": "1.0.0",
            "capabilities": [
                "sefirot_analysis",
                "bitcoin_integration",
                "trait_analysis",
                "mystical_correspondences"
            ],
            "supported_inputs": [
                "traits",
                "txid",
                "ordinal_id",
                "inscription_id"
            ],
            "supported_outputs": [
                "kabbalah_profile",
                "sefirot_resonances",
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
        if "traits" not in data:
            errors.append("Traits must be provided")
            
        # Validate traits format
        if "traits" in data and not isinstance(data["traits"], list):
            errors.append("Traits must be a list of strings")
            
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
        
    def format_output(self, result: KabbalahProfile) -> Dict[str, Any]:
        """Format output data"""
        logger.info("Formatting Kabbalah profile output")
        try:
            return result.dict()
        except Exception as e:
            logger.error(f"Error formatting output: {e}")
            return {}
            
    def calculate_correspondences(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate mystical correspondences including Bitcoin resonances"""
        logger.info("Calculating Kabbalah correspondences")
        correspondences = {}
        
        try:
            # Get Bitcoin-influenced scores if available
            txid = data.get("txid")
            if txid and self.config.get("use_bitcoin_influence", True):
                sefirot_scores = self._calculate_bitcoin_sefirot_affinities(
                    data.get("traits", []),
                    txid
                )
                bitcoin_attributes = self.derive_mystical_attributes(txid)
                correspondences["bitcoin_resonance"] = bitcoin_attributes[0].value
                correspondences["chain_harmony"] = bitcoin_attributes[1].value
            else:
                sefirot_scores = self._calculate_sefirot_affinities(data.get("traits", []))
            
            # Get primary and secondary sefirot
            primary_sefirah = max(sefirot_scores.items(), key=lambda x: x[1])[0]
            secondary_sefirot = sorted(
                [s for s in sefirot_scores.items() if s[0] != primary_sefirah],
                key=lambda x: x[1],
                reverse=True
            )[:2]
            
            # Get sefirah details
            primary = get_sefirah_by_position(SefirotPosition[primary_sefirah.upper()])
            if not primary:
                logger.error(f"Primary Sefirah not found: {primary_sefirah}")
                return {}
                
            correspondences["primary_sefirah"] = primary_sefirah
            correspondences["secondary_sefirot"] = [s[0] for s in secondary_sefirot]
            correspondences["divine_attribute"] = primary.divine_attribute
            correspondences["human_attribute"] = primary.human_attribute
            correspondences["element"] = primary.element
            correspondences["planet"] = primary.planet
            correspondences["sefirot_resonances"] = sefirot_scores
            
            logger.info("Successfully calculated correspondences")
            return correspondences
            
        except Exception as e:
            logger.error(f"Error calculating correspondences: {e}")
            return {}
            
    def generate_profile(self, data: Dict[str, Any]) -> KabbalahProfile:
        """Generate Bitcoin-integrated Kabbalah profile"""
        logger.info("Generating Kabbalah profile")
        
        try:
            # Validate input
            validation = self.validate_input(data)
            if not validation.is_valid:
                raise ValueError(f"Invalid input data: {validation.errors or []}")
                
            # Get Bitcoin-related data
            txid = data.get("txid")
            ordinal_id = data.get("ordinal_id")
            inscription_id = data.get("inscription_id")
            
            # Get Bitcoin-derived attributes if available
            if txid and self.config.get("use_bitcoin_influence", True):
                bitcoin_attributes = self.derive_mystical_attributes(txid)
                if len(bitcoin_attributes) >= 2:
                    bitcoin_resonance = bitcoin_attributes[0].value
                    chain_harmony = bitcoin_attributes[1].value
                else:
                    bitcoin_resonance = None
                    chain_harmony = None
                    bitcoin_attributes = []
            else:
                bitcoin_resonance = None
                chain_harmony = None
                bitcoin_attributes = []
                
            # Get ordinal attributes if available
            if ordinal_id:
                self.bind_to_ordinal(ordinal_id)
                ordinal_attributes = self.ordinal_data
            else:
                ordinal_attributes = {}
                
            # Get inscription attributes if available
            if inscription_id:
                self.bind_to_inscription(inscription_id)
                inscription_attributes = self.inscription_data
            else:
                inscription_attributes = {}
            
            # Calculate sefirot affinities with Bitcoin influence
            traits = data.get("traits", [])
            if txid and self.config.get("use_bitcoin_influence", True):
                sefirot_scores = self._calculate_bitcoin_sefirot_affinities(traits, txid)
            else:
                sefirot_scores = self._calculate_sefirot_affinities(traits)
            
            # Get primary and secondary sefirot
            primary_sefirah = max(sefirot_scores.items(), key=lambda x: x[1])[0]
            secondary_sefirot = sorted(
                [s for s in sefirot_scores.items() if s[0] != primary_sefirah],
                key=lambda x: x[1],
                reverse=True
            )[:2]
            
            # Get sefirah details
            primary = get_sefirah_by_position(SefirotPosition[primary_sefirah.upper()])
            if not primary:
                logger.error(f"Primary Sefirah not found: {primary_sefirah}")
                raise ValueError(f"Primary Sefirah not found: {primary_sefirah}")
                
            secondaries = []
            for s in secondary_sefirot:
                secondary = get_sefirah_by_position(SefirotPosition[s[0].upper()])
                if secondary:
                    secondaries.append(secondary)
                else:
                    logger.warning(f"Secondary Sefirah not found: {s[0]}")
            
            # Create profile data
            profile_data = {
                "id": f"kabbalah_profile_{data.get('name', 'unknown')}",
                "name": f"Kabbalah Profile for {data.get('name', 'Unknown Entity')}",
                "primary_sefirah": primary_sefirah,
                "secondary_sefirot": [s[0] for s in secondary_sefirot],
                "divine_attributes": [primary.divine_attribute] + [s.divine_attribute for s in secondaries],
                "human_attributes": [primary.human_attribute] + [s.human_attribute for s in secondaries],
                "spiritual_meanings": [primary.spiritual_meaning] + [s.spiritual_meaning for s in secondaries],
                "practical_meanings": [primary.practical_meaning] + [s.practical_meaning for s in secondaries],
                "shadow_aspects": [primary.shadow_aspect] + [s.shadow_aspect for s in secondaries],
                "elements": [primary.element] + [s.element for s in secondaries],
                "planets": [primary.planet] + [s.planet for s in secondaries],
                "influence_categories": primary.influence_categories,
                "bitcoin_resonance": bitcoin_resonance,
                "chain_harmony": chain_harmony,
                "ordinal_attributes": ordinal_attributes,
                "inscription_attributes": inscription_attributes,
                "sefirot_resonances": sefirot_scores,
                "attributes": [
                    MysticalAttribute(
                        name="primary_sefirah",
                        value=primary_sefirah,
                        description=f"Primary Sefirah: {primary.divine_attribute}"
                    ),
                    MysticalAttribute(
                        name="element",
                        value=primary.element,
                        description=f"Primary element from {primary_sefirah}"
                    ),
                    MysticalAttribute(
                        name="planet",
                        value=primary.planet,
                        description=f"Primary planet from {primary_sefirah}"
                    )
                ] + (bitcoin_attributes if txid else []),
                "relationships": {
                    "primary_sefirah": [primary_sefirah],
                    "secondary_sefirot": [s[0] for s in secondary_sefirot],
                    "ordinal": [ordinal_id] if ordinal_id else [],
                    "inscription": [inscription_id] if inscription_id else []
                },
                "metadata": {
                    "calculation_method": "trait_analysis",
                    "bitcoin_influenced": bool(txid and self.config.get("use_bitcoin_influence", True)),
                    "ordinal_bound": bool(ordinal_id),
                    "inscription_bound": bool(inscription_id)
                }
            }
            
            # Create and validate profile
            profile = KabbalahProfile(**profile_data)
            logger.info(f"Successfully generated profile for {data.get('name', 'Unknown Entity')}")
            return profile
            
        except Exception as e:
            logger.error(f"Error generating profile: {e}")
            raise
            
    def _calculate_sefirot_affinities(self, traits: List[str]) -> Dict[str, float]:
        """Calculate Sefirot affinities based on traits"""
        scores = {}
        
        for sefirah in ALL_SEFIROT:
            score = 0.0
            
            # Match traits against keywords and influence categories
            for trait in traits:
                trait_lower = trait.lower()
                if trait_lower in [kw.lower() for kw in sefirah.keywords]:
                    score += 0.3
                for category, value in sefirah.influence_categories.items():
                    if category in trait_lower:
                        score += value * 0.2
                        
            scores[sefirah.position.value] = min(score, 1.0)
            
        return scores
        
    def _calculate_bitcoin_sefirot_affinities(
        self,
        traits: List[str],
        txid: str
    ) -> Dict[str, float]:
        """Calculate Sefirot affinities with Bitcoin influence"""
        # Get base scores from traits
        base_scores = self._calculate_sefirot_affinities(traits)
        
        # Get deterministic randomness from Bitcoin transaction
        random_bytes = self.bitcoin.derive_randomness(txid, num_bytes=32)
        
        # Use different parts of the random bytes to influence different sefirot
        for i, (sefirah, score) in enumerate(base_scores.items()):
            # Use 4 bytes for each sefirah
            start = (i * 4) % len(random_bytes)
            end = start + 4
            influence = int.from_bytes(random_bytes[start:end], 'big') / (2**32)
            
            # Blend trait-based score with Bitcoin influence
            base_scores[sefirah] = min(1.0, (score * 0.7) + (influence * 0.3))
            
        return base_scores 