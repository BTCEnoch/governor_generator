"""
Enochian Magic System Implementation with Bitcoin Integration
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, cast
from pydantic import ValidationError

from core.utils.mystical.base import (
    BitcoinMysticalSystem,
    MysticalAttribute,
    ValidationResult as BaseValidationResult
)
from core.utils.mystical.bitcoin_integration import BitcoinIntegration
from core.utils.bitcoin.art_generation import BitcoinArtGenerator
from core.utils.custom_logging import setup_logger

from .schemas import (
    EnochianLetter,
    AethyrProfile,
    EnochianTable,
    RitualPattern,
    GovernorRelationship,
    EnochianSystemConfig,
    Direction
)
from .data.enochian_database import (
    get_enochian_alphabet,
    get_aethyr_data,
    get_watchtower_table,
    get_ritual_correspondences
)
from .ritual_mechanics.ritual_engine import RitualEngine
from .ritual_mechanics.schemas import (
    RitualPoint,
    ValidationResult as RitualValidationResult
)
from .relationships.relationship_engine import RelationshipEngine

logger = setup_logger("enochian_system")

def convert_validation_result(result: RitualValidationResult) -> BaseValidationResult:
    """Convert RitualValidationResult to BaseValidationResult"""
    return BaseValidationResult(
        data=result.data,
        is_valid=result.is_valid,
        errors=result.errors
    )

class EnochianSystem(BitcoinMysticalSystem):
    """Bitcoin-integrated Enochian magic system implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the Enochian system"""
        try:
            # Validate config
            validated_config = EnochianSystemConfig(**config)
            
            # Initialize components
            self.ritual_engine = RitualEngine(
                config={
                    "min_power": validated_config.min_power,
                    "max_power": validated_config.max_power,
                    "resonance_threshold": validated_config.resonance_threshold,
                    "governor_influence": validated_config.governor_influence,
                    "ritual_points_required": validated_config.ritual_points_required
                }
            )
            
            # Initialize other components
            self.relationship_engine = RelationshipEngine(
                config=EnochianSystemConfig(**validated_config.dict())
            )
            
            # Load data
            self.aethyrs = self._load_aethyrs()
            self.governors = self._load_governors()
            
            self.logger.info(
                f"Initialized EnochianSystem with config: {validated_config}"
            )
            
        except Exception as e:
            self.logger.error(f"Error initializing EnochianSystem: {str(e)}")
            raise
        
        self.bitcoin = BitcoinIntegration(config.get("bitcoin_integration"))
        self.art_generator = BitcoinArtGenerator()
        self.logger = logger
        
        # Load system data
        self.alphabet = get_enochian_alphabet()
        self.aethyrs = get_aethyr_data()
        self.tables = {
            direction: get_watchtower_table(direction)
            for direction in Direction
        }
        
        # Initialize ritual engine with Bitcoin integration
        self.ritual_engine = RitualEngine(config=validated_config.dict())
        
        self.logger.info("Initialized Bitcoin-integrated EnochianSystem")

    def _load_aethyrs(self) -> List[AethyrProfile]:
        """Load all Aethyr data"""
        return get_aethyr_data()

    def _load_governors(self) -> List[str]:
        """Load all Governor names"""
        governors = []
        for aethyr in self.aethyrs:
            governors.extend(aethyr.governors)
        return governors

    def get_system_info(self) -> Dict[str, Any]:
        """Get information about the Enochian system"""
        return {
            "name": "Enochian Magic System",
            "version": "1.0.0",
            "description": (
                "A Bitcoin-integrated Enochian magic system for working with "
                "letters, Aethyrs, and Governor relationships."
            ),
            "capabilities": [
                "Letter and word generation",
                "Aethyr scrying mechanics",
                "Governor relationship mapping",
                "Ritual validation",
                "Sigil art generation"
            ],
            "requirements": [
                "Bitcoin integration for entropy",
                "Sacred geometry support",
                "Governor resonance"
            ],
            "author": "Enochian Cyphers",
            "documentation_url": "https://docs.enochiancyphers.com/enochian"
        }

    async def validate_input(self, input_data: Dict[str, Any]) -> BaseValidationResult:
        """Validate input data for Enochian operations"""
        try:
            validation_data = {"input": input_data}
            
            if "power_level" in input_data:
                power = input_data["power_level"]
                if not isinstance(power, int) or power < 1 or power > 10:
                    return BaseValidationResult(
                        data=validation_data,
                        is_valid=False,
                        errors=["Power level must be an integer between 1 and 10"]
                    )
            
            if "aethyr" in input_data:
                aethyr = input_data["aethyr"]
                valid_aethyrs = [a.name for a in self.aethyrs]
                if not isinstance(aethyr, str) or aethyr not in valid_aethyrs:
                    return BaseValidationResult(
                        data=validation_data,
                        is_valid=False,
                        errors=["Invalid Aethyr specified"]
                    )
            
            if "governor" in input_data:
                governor = input_data["governor"]
                valid_governors = []
                for aethyr in self.aethyrs:
                    valid_governors.extend(aethyr.governors)
                if not isinstance(governor, str) or governor not in valid_governors:
                    return BaseValidationResult(
                        data=validation_data,
                        is_valid=False,
                        errors=["Invalid Governor specified"]
                    )
            
            if "ritual_points" in input_data:
                points = input_data["ritual_points"]
                if not isinstance(points, list):
                    return BaseValidationResult(
                        data=validation_data,
                        is_valid=False,
                        errors=["Ritual points must be a list"]
                    )
                try:
                    ritual_points = [RitualPoint(**p) for p in points]
                    validation = await self.ritual_engine.validate_ritual_points(
                        [p.dict() for p in ritual_points]
                    )
                    if not validation.is_valid:
                        return convert_validation_result(validation)
                except ValidationError as e:
                    return BaseValidationResult(
                        data=validation_data,
                        is_valid=False,
                        errors=[str(e)]
                    )
            
            return BaseValidationResult(data=validation_data, is_valid=True, errors=[])
            
        except Exception as e:
            return BaseValidationResult(
                data={"error": str(e)},
                is_valid=False,
                errors=[f"Validation error: {str(e)}"]
            )

    def format_output(self, output_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format Enochian output data"""
        try:
            # Add letter descriptions
            if "letters" in output_data:
                letters = []
                for letter in output_data["letters"]:
                    letter_obj = next(
                        (l for l in self.alphabet if l.name == letter),
                        None
                    )
                    if letter_obj:
                        letters.append(letter_obj.model_dump())
                output_data["letter_data"] = letters
            
            # Add Aethyr descriptions
            if "aethyr" in output_data:
                aethyr_obj = next(
                    (a for a in self.aethyrs if a.name == output_data["aethyr"]),
                    None
                )
                if aethyr_obj:
                    output_data["aethyr_data"] = aethyr_obj.model_dump()
            
            # Add Governor correspondences
            if "governor" in output_data:
                correspondences = get_ritual_correspondences(output_data["governor"])
                output_data["governor_data"] = correspondences
            
            # Add ritual results
            if "ritual_results" in output_data:
                results = output_data["ritual_results"]
                if "resonance" in results:
                    resonance = results["resonance"]
                    output_data["ritual_results"]["resonance_data"] = {
                        "level": resonance.resonance_level,
                        "patterns": [p.model_dump() for p in resonance.energy_patterns],
                        "verification": resonance.bitcoin_verification
                    }
            
            return output_data
            
        except Exception as e:
            self.logger.error(f"Error formatting output: {str(e)}")
            return output_data

    async def calculate_correspondences(self, data: Dict[str, Any]) -> List[MysticalAttribute]:
        """Calculate mystical correspondences for Enochian data"""
        correspondences = []
        
        try:
            # Add letter-based correspondences
            if "letters" in data:
                for letter in data["letters"]:
                    letter_obj = next(
                        (l for l in self.alphabet if l.name == letter),
                        None
                    )
                    if letter_obj:
                        correspondences.append(
                            MysticalAttribute(
                                name=f"letter_{letter_obj.name.lower()}",
                                value=letter_obj.power_level / 10,
                                description=f"Letter power: {letter_obj.name}"
                            )
                        )
            
            # Add Aethyr-based correspondences
            if "aethyr" in data:
                aethyr_obj = next(
                    (a for a in self.aethyrs if a.name == data["aethyr"]),
                    None
                )
                if aethyr_obj:
                    correspondences.append(
                        MysticalAttribute(
                            name=f"aethyr_{aethyr_obj.name.lower()}",
                            value=aethyr_obj.number / 30,
                            description=f"Aethyr resonance: {aethyr_obj.name}"
                        )
                    )
            
            # Add ritual-based correspondences
            if "ritual_points" in data:
                points = [RitualPoint(**p) for p in data["ritual_points"]]
                pattern = await self.ritual_engine.match_ritual_pattern(points)
                if pattern:
                    correspondences.append(
                        MysticalAttribute(
                            name=f"pattern_{pattern.pattern_type}",
                            value=pattern.total_energy / 10,
                            description=f"Ritual pattern: {pattern.pattern_type}"
                        )
                    )
            
            return correspondences
            
        except Exception as e:
            self.logger.error(f"Error calculating correspondences: {str(e)}")
            return []

    async def generate_reading(
        self,
        txid: Optional[str] = None,
        power_level: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate an Enochian reading using Bitcoin entropy"""
        try:
            # Use Bitcoin transaction for entropy
            entropy = await self.bitcoin.get_entropy(txid) if txid else None
            
            # Set power level
            power = power_level or 5  # Default to medium power
            
            # Select Aethyr based on entropy
            aethyr_index = int(entropy[:8], 16) % len(self.aethyrs) if entropy else 0
            aethyr = self.aethyrs[aethyr_index]
            
            # Generate ritual points
            points = []
            for i in range(3):  # Minimum points for a pattern
                x = float(int(entropy[8+i*8:16+i*8], 16)) / 2**32 if entropy else 0.5
                y = float(int(entropy[16+i*8:24+i*8], 16)) / 2**32 if entropy else 0.5
                points.append(
                    RitualPoint(
                        x=x,
                        y=y,
                        energy_level=power / 10,
                        element=aethyr.correspondence,
                        aethyr_resonance=aethyr.name
                    )
                )
            
            # Calculate resonance
            pattern = await self.ritual_engine.match_ritual_pattern(points)
            
            return {
                "aethyr": aethyr.name,
                "power_level": power,
                "ritual_points": [p.dict() for p in points],
                "ritual_results": {
                    "resonance": pattern
                },
                "bitcoin_data": {
                    "txid": txid,
                    "entropy": entropy
                } if txid else None
            }
            
        except Exception as e:
            self.logger.error(f"Error generating reading: {str(e)}")
            raise

    async def generate_art(
        self,
        reading: Dict[str, Any],
        output_path: str
    ) -> str:
        """Generate ritual art based on reading"""
        try:
            # Extract ritual points
            points = [
                RitualPoint(**p)
                for p in reading.get("ritual_points", [])
            ]
            
            # Get pattern for art generation
            pattern = await self.ritual_engine.match_ritual_pattern(points)
            
            # Generate art using Bitcoin entropy
            art_path = await self.art_generator.generate_ritual_art(
                points=[(p.x, p.y) for p in points],
                energy_levels=[p.energy_level for p in points],
                pattern_type=pattern.pattern_type if pattern else "default",
                output_path=output_path,
                entropy=pattern.bitcoin_entropy if pattern else ""
            )
            
            return art_path
            
        except Exception as e:
            self.logger.error(f"Error generating art: {str(e)}")
            raise

    async def get_all_aethyrs(self) -> List[AethyrProfile]:
        """Get all available Aethyrs"""
        return self.aethyrs

    async def get_aethyr(self, name: str) -> Optional[AethyrProfile]:
        """Get a specific Aethyr by name"""
        return next(
            (aethyr for aethyr in self.aethyrs if aethyr.name == name),
            None
        )

    async def generate_ritual_art(
        self,
        profile_data: Dict[str, Any],
        output_path: str
    ) -> str:
        """Generate ritual art for a relationship profile"""
        try:
            # Extract points and energy levels
            points = []
            energy_levels = []
            
            # Get points from connections
            for conn in profile_data.get("connections", []):
                points.append((conn["source_x"], conn["source_y"]))
                points.append((conn["target_x"], conn["target_y"]))
                energy_levels.extend([conn["strength"], conn["strength"]])
            
            # Get points from patterns
            for pattern in profile_data.get("patterns", []):
                for gov in pattern["governors"]:
                    gov_data = profile_data["visualization"]["nodes"].get(gov, {})
                    if gov_data:
                        points.append((gov_data["x"], gov_data["y"]))
                        energy_levels.append(pattern["intensity"])
            
            # Generate art
            return await self.art_generator.generate_ritual_art(
                points=points,
                energy_levels=energy_levels,
                pattern_type="relationship",
                output_path=output_path,
                entropy=profile_data.get("bitcoin_block_hash", "")
            )
            
        except Exception as e:
            self.logger.error(f"Error generating ritual art: {str(e)}")
            raise

    async def validate_ritual_pattern(
        self,
        points: List[Dict[str, float]],
        reading: Dict[str, Any]
    ) -> bool:
        """Validate a ritual pattern against a reading"""
        try:
            # Convert points to RitualPoint objects
            ritual_points = []
            for p in points:
                ritual_points.append(
                    RitualPoint(
                        x=p["x"],
                        y=p["y"],
                        energy_level=p.get("energy", 0.5),
                        element=reading.get("aethyr_data", {}).get("correspondence", "air"),
                        aethyr_resonance=str(reading.get("aethyr", ""))  # Convert to string
                    )
                )
            
            # Validate points
            validation = await self.ritual_engine.validate_ritual_points(
                [p.dict() for p in ritual_points]
            )
            
            if not validation.is_valid:
                self.logger.warning(
                    "Ritual pattern validation failed: %s",
                    validation.errors
                )
                return False
            
            # Match pattern
            pattern = await self.ritual_engine.match_ritual_pattern(ritual_points)
            
            # Check if pattern matches reading
            reading_pattern = reading.get("ritual_results", {}).get(
                "resonance", {}
            ).get("pattern_type", "")
            
            if not reading_pattern:
                return True  # No pattern to match against
            
            return pattern.pattern_type == reading_pattern if pattern else False
            
        except Exception as e:
            self.logger.error(f"Error validating ritual pattern: {str(e)}")
            return False 