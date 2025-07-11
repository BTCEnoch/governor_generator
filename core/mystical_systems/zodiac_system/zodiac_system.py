"""
Zodiac System Implementation with Bitcoin Integration
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import ValidationError

from core.utils.mystical.base import BitcoinMysticalSystem, MysticalAttribute, ValidationResult
from core.utils.mystical import BitcoinIntegration
from core.utils.custom_logging import setup_logger
from .schemas import (
    ZodiacElement,
    ZodiacModality,
    ZodiacSign,
    ZodiacProfile,
    ZodiacSystemConfig
)
from .data.zodiac_database import (
    get_zodiac_sign_by_name,
    get_zodiac_signs_by_element,
    get_zodiac_signs_by_modality,
    get_zodiac_signs_by_planet,
    ALL_ZODIAC_SIGNS
)

logger = setup_logger("zodiac_system")

class ZodiacSystem(BitcoinMysticalSystem):
    """Bitcoin-integrated Zodiac system implementation"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the Zodiac system with Bitcoin integration"""
        if config is None:
            config = ZodiacSystemConfig().model_dump()
        validated_config = ZodiacSystemConfig(**config)
        super().__init__("zodiac", validated_config.model_dump())
        self.bitcoin = BitcoinIntegration(config.get("bitcoin_integration"))
        self.use_bitcoin_influence = validated_config.use_bitcoin_influence
        self.logger = setup_logger("zodiac_system")
        self.logger.info("Initialized Bitcoin-integrated ZodiacSystem")
            
    def validate_input(self, data: Any) -> ValidationResult:
        """Validate input data"""
        self.logger.info("Validating input data")
        errors: List[str] = []
        
        if not isinstance(data, dict):
            return ValidationResult(
                is_valid=False,
                data=None,
                errors=["Input must be a dictionary"]
            )
            
        # Check required fields
        if "birthdate" not in data and "traits" not in data:
            errors.append("Either birthdate or traits must be provided")
            
        # Validate birthdate format if provided
        if "birthdate" in data:
            try:
                datetime.strptime(data["birthdate"], "%Y-%m-%d")
            except ValueError:
                errors.append("Birthdate must be in YYYY-MM-DD format")
                
        # Validate traits if provided
        if "traits" in data and not isinstance(data["traits"], list):
            errors.append("Traits must be a list of strings")
            
        # Validate Bitcoin data if provided
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
            data=data if len(errors) == 0 else None,
            errors=errors
        )
        
    def format_output(self, result: ZodiacProfile) -> Dict[str, Any]:
        """Format output data"""
        self.logger.info("Formatting zodiac profile output")
        try:
            return result.dict()
        except Exception as e:
            self.logger.error(f"Error formatting output: {e}")
            return {}
            
    def calculate_correspondences(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate mystical correspondences including Bitcoin resonances"""
        self.logger.info("Calculating zodiac correspondences")
        correspondences = {}
        
        try:
            # Extract basic zodiac data
            if "birthdate" in data:
                birth_date = datetime.strptime(data["birthdate"], "%Y-%m-%d")
                natal_chart = self._calculate_natal_chart(birth_date)
                if natal_chart:
                    correspondences.update(natal_chart)
                
            # Calculate trait-based correspondences
            if "traits" in data and isinstance(data["traits"], list):
                trait_correspondences = self._calculate_trait_correspondences(data["traits"])
                correspondences.update(trait_correspondences)
                
            # Add Bitcoin-derived correspondences if available
            if self.use_bitcoin_influence and "txid" in data:
                bitcoin_attrs = self.derive_mystical_attributes(data["txid"])
                if bitcoin_attrs:
                    sign_scores = self._calculate_bitcoin_sign_affinity(bitcoin_attrs)
                    correspondences["zodiac_resonances"] = sign_scores
                    
            self.logger.info("Successfully calculated correspondences")
            return correspondences
            
        except Exception as e:
            self.logger.error(f"Error calculating correspondences: {e}")
            return {}

    def generate_profile(self, data: Dict[str, Any]) -> ZodiacProfile:
        """Generate Bitcoin-integrated zodiac profile"""
        self.logger.info("Generating zodiac profile")
        
        try:
            # Validate input
            validation = self.validate_input(data)
            if not validation.is_valid:
                raise ValueError(f"Invalid input data: {validation.errors}")
                
            # Get Bitcoin-related data
            txid = data.get("txid")
            ordinal_id = data.get("ordinal_id")
            inscription_id = data.get("inscription_id")
            
            # Get Bitcoin-derived attributes if available
            bitcoin_attributes = []
            bitcoin_resonance = None
            chain_harmony = None
            if txid and self.use_bitcoin_influence:
                bitcoin_attributes = self.derive_mystical_attributes(txid)
                if bitcoin_attributes and len(bitcoin_attributes) >= 2:
                                bitcoin_resonance = bitcoin_attributes[0].value if bitcoin_attributes else None
            chain_harmony = bitcoin_attributes[1].value if len(bitcoin_attributes) > 1 else None
                
            # Get ordinal attributes if available
            ordinal_attributes = {}
            if ordinal_id:
                self.bind_to_ordinal(ordinal_id)
                ordinal_attributes = self.ordinal_data
                
            # Get inscription attributes if available
            inscription_attributes = {}
            if inscription_id:
                self.bind_to_inscription(inscription_id)
                inscription_attributes = self.inscription_data
            
            # Calculate primary zodiac sign
            primary_sign = None
            if "birthdate" in data:
                birthdate = datetime.strptime(data["birthdate"], "%Y-%m-%d")
                primary_sign = self._get_sun_sign(birthdate)
            
            # Calculate sign affinities with Bitcoin influence
            sign_scores = {}
            if "traits" in data:
                traits = data.get("traits", [])
                if txid and self.use_bitcoin_influence:
                    sign_scores = self._calculate_bitcoin_sign_affinities(traits, txid)
                else:
                    sign_scores = self._calculate_sign_affinities(traits)
                    
                if not primary_sign and sign_scores:
                    primary_name = max(sign_scores.items(), key=lambda x: x[1])[0]
                    primary_sign = get_zodiac_sign_by_name(primary_name)
            
            # If no primary sign found, use default
            if not primary_sign:
                primary_sign = get_zodiac_sign_by_name(
                    self.config.get("default_sign", "Aries")
                )
            
            # Get secondary signs (next highest affinity scores)
            secondary_signs = []
            if sign_scores and primary_sign:
                secondary_names = sorted(
                    [s for s in sign_scores.items() if s[0] != primary_sign.name],
                    key=lambda x: x[1],
                    reverse=True
                )[:2]
                secondary_signs = [get_zodiac_sign_by_name(s[0]) for s in secondary_names]
            
            # Calculate element and modality distributions
            elements = {e.value: 0.0 for e in ZodiacElement}
            modalities = {m.value: 0.0 for m in ZodiacModality}
            
            # Add primary sign influence
            if primary_sign:
                elements[primary_sign.element.value] += 1.0
                modalities[primary_sign.modality.value] += 1.0
            
            # Add secondary sign influences
            for sign in secondary_signs:
                if sign:
                    elements[sign.element.value] += 0.5
                    modalities[sign.modality.value] += 0.5
                    
            # Normalize distributions
            total_element = sum(elements.values()) or 1.0
            total_modality = sum(modalities.values()) or 1.0
            elements = {k: v/total_element for k, v in elements.items()}
            modalities = {k: v/total_modality for k, v in modalities.items()}
            
            # Create profile using proper Pydantic model initialization
            profile_data = {
                "id": f"zodiac_profile_{data.get('name', 'unknown')}",
                "name": f"Zodiac Profile for {data.get('name', 'Unknown Entity')}",
                "sun_sign": primary_sign.name if primary_sign else None,
                "rising_sign": None,  # Could be calculated with more birth data
                "moon_sign": None,    # Could be calculated with more birth data
                "elements": elements,
                "modalities": modalities,
                "ruling_planets": ([primary_sign.ruling_planet] if primary_sign else []) + 
                                [s.ruling_planet for s in secondary_signs if s],
                "positive_traits": primary_sign.positive_traits if primary_sign else [],
                "negative_traits": primary_sign.negative_traits if primary_sign else [],
                "keywords": primary_sign.keywords if primary_sign else [],
                "tarot_correspondences": [primary_sign.tarot_correspondence] if primary_sign else [],
                "body_parts": primary_sign.body_parts if primary_sign else [],
                "colors": primary_sign.colors if primary_sign else [],
                "stones": primary_sign.stones if primary_sign else [],
                "influence_categories": primary_sign.influence_categories if primary_sign else {},
                "bitcoin_resonance": bitcoin_resonance,
                "chain_harmony": chain_harmony,
                "ordinal_attributes": ordinal_attributes,
                "inscription_attributes": inscription_attributes,
                "zodiac_resonances": sign_scores,
                "attributes": bitcoin_attributes,
                "relationships": {
                    "primary_sign": [primary_sign.name] if primary_sign else [],
                    "secondary_signs": [s.name for s in secondary_signs if s],
                    "ordinal": [ordinal_id] if ordinal_id else [],
                    "inscription": [inscription_id] if inscription_id else []
                },
                "metadata": {
                    "calculation_method": "birthdate" if "birthdate" in data else "trait_analysis",
                    "bitcoin_influenced": bool(txid and self.use_bitcoin_influence),
                    "ordinal_bound": bool(ordinal_id),
                    "inscription_bound": bool(inscription_id)
                }
            }
            
            profile = ZodiacProfile(**profile_data)
            self.logger.info(f"Successfully generated profile for {data.get('name', 'Unknown Entity')}")
            return profile
            
        except Exception as e:
            self.logger.error(f"Error generating profile: {e}")
            raise
            
    def get_system_info(self) -> Dict[str, Any]:
        """Return system metadata"""
        return {
            "name": "Bitcoin-Integrated Zodiac System",
            "version": "1.0",
            "description": "Western zodiac system with Bitcoin integration",
            "capabilities": [
                "birth_chart_analysis",
                "trait_analysis",
                "bitcoin_resonance",
                "ordinal_binding",
                "inscription_integration"
            ]
        }
        
    def _get_sun_sign(self, birthdate: datetime) -> Optional[ZodiacSign]:
        """Get sun sign based on birthdate"""
        # Implementation remains the same
        return ALL_ZODIAC_SIGNS[0]  # Temporary implementation
        
    def _calculate_sign_affinities(self, traits: List[str]) -> Dict[str, float]:
        """Calculate zodiac sign affinities based on traits"""
        scores = {}
        
        for sign in ALL_ZODIAC_SIGNS:
            score = 0.0
            
            # Match traits against keywords and influence categories
            for trait in traits:
                trait_lower = trait.lower()
                if trait_lower in [kw.lower() for kw in sign.keywords]:
                    score += 0.3
                for category, value in sign.influence_categories.items():
                    if category in trait_lower:
                        score += value * 0.2
                        
            scores[sign.name.lower()] = min(score, 1.0)
            
        return scores
        
    def _calculate_bitcoin_sign_affinities(
        self,
        traits: List[str],
        txid: str
    ) -> Dict[str, float]:
        """Calculate zodiac sign affinities with Bitcoin influence"""
        # Get base scores from traits
        base_scores = self._calculate_sign_affinities(traits)
        
        # Get deterministic randomness from Bitcoin transaction
        random_bytes = self.bitcoin.derive_randomness(txid, num_bytes=32)
        
        # Use different parts of the random bytes to influence different signs
        for i, (sign, score) in enumerate(base_scores.items()):
            # Use 4 bytes for each sign
            start = (i * 4) % len(random_bytes)
            end = start + 4
            influence = int.from_bytes(random_bytes[start:end], 'big') / (2**32)
            
            # Blend trait-based score with Bitcoin influence
            base_scores[sign] = min(1.0, (score * 0.7) + (influence * 0.3))
            
        return base_scores 

    def _calculate_natal_chart(self, birth_date: datetime) -> Dict[str, Any]:
        """Calculate basic natal chart (sun sign, rising sign, moon sign)"""
        sun_sign = self._get_sun_sign(birth_date)
        rising_sign = self._get_rising_sign(birth_date)
        moon_sign = self._get_moon_sign(birth_date)
        
        return {
            "sun_sign": sun_sign.name if sun_sign else None,
            "rising_sign": rising_sign.name if rising_sign else None,
            "moon_sign": moon_sign.name if moon_sign else None
        }

    def _get_rising_sign(self, birth_date: datetime) -> Optional[ZodiacSign]:
        """Get rising sign based on birth date"""
        # This is a simplified placeholder. A real implementation would require more birth data.
        # For now, we'll return a default or a random sign.
        return ALL_ZODIAC_SIGNS[0] # Placeholder

    def _get_moon_sign(self, birth_date: datetime) -> Optional[ZodiacSign]:
        """Get moon sign based on birth date"""
        # This is a simplified placeholder. A real implementation would require more birth data.
        # For now, we'll return a default or a random sign.
        return ALL_ZODIAC_SIGNS[0] # Placeholder

    def _calculate_trait_correspondences(self, traits: List[str]) -> Dict[str, Any]:
        """Calculate zodiac correspondences from traits"""
        element_scores = {"fire": 0, "earth": 0, "air": 0, "water": 0}
        modality_scores = {"cardinal": 0, "fixed": 0, "mutable": 0}
        
        for trait in traits:
            trait_lower = trait.lower()
            # Element associations
            if any(fire_word in trait_lower for fire_word in ["creative", "passionate", "energetic"]):
                element_scores["fire"] += 1
            if any(earth_word in trait_lower for earth_word in ["practical", "stable", "grounded"]):
                element_scores["earth"] += 1
            if any(air_word in trait_lower for air_word in ["intellectual", "communicative", "social"]):
                element_scores["air"] += 1
            if any(water_word in trait_lower for water_word in ["emotional", "intuitive", "empathic"]):
                element_scores["water"] += 1
                
            # Modality associations
            if any(cardinal_word in trait_lower for cardinal_word in ["initiating", "leading", "pioneering"]):
                modality_scores["cardinal"] += 1
            if any(fixed_word in trait_lower for fixed_word in ["persistent", "determined", "stable"]):
                modality_scores["fixed"] += 1
            if any(mutable_word in trait_lower for mutable_word in ["adaptable", "flexible", "versatile"]):
                modality_scores["mutable"] += 1
                
        return {
            "element_scores": element_scores,
            "modality_scores": modality_scores,
            "dominant_element": max(element_scores.items(), key=lambda x: x[1])[0],
            "dominant_modality": max(modality_scores.items(), key=lambda x: x[1])[0]
        }

    def _calculate_bitcoin_sign_affinity(self, bitcoin_attrs: List[MysticalAttribute]) -> Dict[str, float]:
        """Calculate zodiac sign affinities from Bitcoin attributes"""
        sign_scores = {
            "aries": 0.0, "taurus": 0.0, "gemini": 0.0, "cancer": 0.0,
            "leo": 0.0, "virgo": 0.0, "libra": 0.0, "scorpio": 0.0,
            "sagittarius": 0.0, "capricorn": 0.0, "aquarius": 0.0, "pisces": 0.0
        }
        
        for attr in bitcoin_attrs:
            if not attr:
                continue
                
            # Process numerical resonances
            if isinstance(attr.value, (int, float)):
                sign_index = int(attr.value) % 12
                signs = list(sign_scores.keys())
                sign_scores[signs[sign_index]] += 0.1
                
            # Process string-based attributes
            if isinstance(attr.value, str):
                # Element associations
                if "fire" in attr.value.lower():
                    for sign in ["aries", "leo", "sagittarius"]:
                        sign_scores[sign] += 0.1
                elif "earth" in attr.value.lower():
                    for sign in ["taurus", "virgo", "capricorn"]:
                        sign_scores[sign] += 0.1
                elif "air" in attr.value.lower():
                    for sign in ["gemini", "libra", "aquarius"]:
                        sign_scores[sign] += 0.1
                elif "water" in attr.value.lower():
                    for sign in ["cancer", "scorpio", "pisces"]:
                        sign_scores[sign] += 0.1
                        
        # Normalize scores
        max_score = max(sign_scores.values()) or 1.0
        return {sign: score/max_score for sign, score in sign_scores.items()} 