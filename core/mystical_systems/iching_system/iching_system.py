"""
I Ching System Implementation with Bitcoin Integration
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, cast
from pydantic import ValidationError

from core.utils.mystical import BitcoinIntegration, BitcoinMysticalSystem, MysticalAttribute, ValidationResult
from core.utils.mystical.wikipedia_integration import WikipediaIChing
from core.utils.custom_logging import setup_logger
from .schemas import (
    IChingHexagram,
    IChingProfile,
    IChingSystemConfig,
    HexagramLine,
    LineChange
)
from .data.hexagram_database import get_hexagram_data

logger = setup_logger("iching_system")

class IChingSystem(BitcoinMysticalSystem):
    """Bitcoin-integrated I Ching system implementation"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the I Ching system with Bitcoin integration"""
        if config is None:
            config = IChingSystemConfig().model_dump()
        validated_config = IChingSystemConfig(**config)
        super().__init__("iching", validated_config.model_dump())
        self.bitcoin = BitcoinIntegration(config.get("bitcoin_integration"))
        self.wikipedia = WikipediaIChing()
        self.logger = setup_logger("iching_system")
        self.logger.info("Initialized Bitcoin-integrated IChingSystem")
            
    async def __aenter__(self):
        """Async context manager entry"""
        await self.wikipedia.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.wikipedia.__aexit__(exc_type, exc_val, exc_tb)
            
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            "system_id": "iching_system_v1",
            "name": "I Ching System",
            "description": "A Bitcoin-integrated I Ching system for divination and mystical analysis",
            "version": "1.0.0",
            "capabilities": [
                "hexagram_generation",
                "bitcoin_integration",
                "governor_resonance",
                "mystical_correspondences"
            ],
            "supported_inputs": [
                "question",
                "seed",
                "txid",
                "ordinal_id",
                "inscription_id"
            ],
            "supported_outputs": [
                "iching_profile",
                "hexagram_resonances",
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
        if "question" not in data and "seed" not in data:
            errors.append("Either question or seed must be provided")
            
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
        
    def _generate_line(self, seed: str) -> Tuple[int, LineChange]:
        """Generate a single I Ching line using Bitcoin entropy"""
        value = self.bitcoin.generate_number(seed, 6, 9)
        
        if value == 6:
            return (0, LineChange.YIN_TO_YANG)
        elif value == 7:
            return (0, LineChange.STABLE_YIN)
        elif value == 8:
            return (1, LineChange.STABLE_YANG)
        else:  # value == 9
            return (1, LineChange.YANG_TO_YIN)
            
    def _generate_hexagram(self, seed: str) -> Tuple[List[int], List[LineChange]]:
        """Generate a complete hexagram using Bitcoin entropy"""
        lines = []
        changes = []
        
        for i in range(6):
            line_value, change_type = self._generate_line(f"{seed}_line_{i}")
            lines.append(line_value)
            changes.append(change_type)
            
        return lines, changes
        
    def _lines_to_number(self, lines: List[int]) -> int:
        """Convert binary line values to hexagram number (1-64)"""
        binary_str = "".join(str(x) for x in reversed(lines))
        return int(binary_str, 2) + 1
        
    async def generate_profile(self, data: Dict[str, Any]) -> IChingProfile:
        """Generate Bitcoin-integrated I Ching profile"""
        logger.info("Generating I Ching profile")
        
        try:
            # Validate input
            validation = self.validate_input(data)
            if not validation.is_valid:
                raise ValueError(f"Invalid input data: {validation.errors}")
                
            # Get seed from question or provided seed
            seed = data.get("seed", data["question"])
            
            # Generate initial hexagram
            lines, changes = self._generate_hexagram(seed)
            initial_number = self._lines_to_number(lines)
            
            # Get hexagram data
            initial_data = await self.wikipedia.get_hexagram_data(initial_number)
            if initial_data is None:
                initial_data = get_hexagram_data(initial_number)
            if initial_data is None:
                raise ValueError(f"No data found for hexagram {initial_number}")
            
            # Create initial hexagram lines
            hexagram_lines = []
            changing_line_indices = []
            for i, (line, change) in enumerate(zip(lines, changes), 1):
                is_changing = change in [LineChange.YIN_TO_YANG, LineChange.YANG_TO_YIN]
                if is_changing:
                    changing_line_indices.append(i)
                    
                line_meanings = initial_data.get("line_meanings", {})
                meaning = line_meanings.get(str(i)) if isinstance(line_meanings, dict) else None
                    
                hexagram_lines.append(HexagramLine(
                    position=i,
                    value=6 if change == LineChange.YIN_TO_YANG else
                          7 if change == LineChange.STABLE_YIN else
                          8 if change == LineChange.STABLE_YANG else 9,
                    is_changing=is_changing,
                    change_type=change,
                    meaning=meaning
                ))
                
            # Create initial hexagram
            initial_hexagram = IChingHexagram(
                number=initial_number,
                binary="".join(str(x) for x in lines),
                unicode_char=initial_data.get("unicode", "?"),
                name=initial_data.get("name", f"Hexagram {initial_number}"),
                description=initial_data.get("description", ""),
                judgment=initial_data.get("judgment", ""),
                image=initial_data.get("image", ""),
                lines=hexagram_lines,
                changing_lines=changing_line_indices
            )
            
            # Calculate transformed hexagram if there are changes
            transformed_hexagram = None
            if changing_line_indices:
                transformed_lines = [
                    1 - line if change in [LineChange.YIN_TO_YANG, LineChange.YANG_TO_YIN] else line
                    for line, change in zip(lines, changes)
                ]
                transformed_number = self._lines_to_number(transformed_lines)
                transformed_data = await self.wikipedia.get_hexagram_data(transformed_number)
                if transformed_data is None:
                    transformed_data = get_hexagram_data(transformed_number)
                if transformed_data is None:
                    raise ValueError(f"No data found for hexagram {transformed_number}")
                
                transformed_hexagram = IChingHexagram(
                    number=transformed_number,
                    binary="".join(str(x) for x in transformed_lines),
                    unicode_char=transformed_data.get("unicode", "?"),
                    name=transformed_data.get("name", f"Hexagram {transformed_number}"),
                    description=transformed_data.get("description", ""),
                    judgment=transformed_data.get("judgment", ""),
                    image=transformed_data.get("image", ""),
                    lines=[],  # No line details needed for transformed hexagram
                    changing_lines=[]
                )
            
            # Get Bitcoin-influenced scores if available
            txid = data.get("txid")
            if txid and self.config.get("use_bitcoin_influence", True):
                bitcoin_attributes = self.derive_mystical_attributes(txid)
                bitcoin_resonance = bitcoin_attributes[0].value if bitcoin_attributes else None
                chain_harmony = bitcoin_attributes[1].value if len(bitcoin_attributes) > 1 else None
                # Convert MysticalAttributes to dicts for profile
                attribute_dicts = [
                    {"name": attr.name, "value": str(attr.value), "description": attr.description}
                    for attr in bitcoin_attributes
                ]
            else:
                bitcoin_resonance = None
                chain_harmony = None
                attribute_dicts = []
                
            # Create profile
            profile = IChingProfile(
                id=f"iching_reading_{datetime.now().isoformat()}",
                name=f"I Ching Reading for {data.get('question', 'Unknown Query')}",
                initial_hexagram=initial_hexagram,
                transformed_hexagram=transformed_hexagram,
                changing_line_meanings=[
                    line_meanings.get(str(i), "") if isinstance(line_meanings := initial_data.get("line_meanings", {}), dict) else ""
                    for i in changing_line_indices
                ],
                bitcoin_resonance=bitcoin_resonance,
                chain_harmony=chain_harmony,
                governor_resonances={},  # To be implemented
                attributes=attribute_dicts,
                metadata={
                    "question": data.get("question", ""),
                    "seed": seed,
                    "timestamp": datetime.now().isoformat(),
                    "method": "bitcoin_entropy"
                }
            )
            
            return profile
            
        except Exception as e:
            logger.error(f"Error generating profile: {e}")
            raise 

    def calculate_correspondences(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate mystical correspondences for the I Ching reading"""
        correspondences = []
        
        # Add hexagram-based correspondences
        if "initial_hexagram" in data:
            hexagram = data["initial_hexagram"]
            correspondences.append({
                "type": "hexagram_number",
                "value": hexagram["number"],
                "description": f"Primary hexagram number {hexagram['number']}"
            })
            
            # Add trigram correspondences
            upper_trigram = hexagram["binary"][:3]
            lower_trigram = hexagram["binary"][3:]
            correspondences.extend([
                {
                    "type": "upper_trigram",
                    "value": upper_trigram,
                    "description": f"Upper trigram pattern: {upper_trigram}"
                },
                {
                    "type": "lower_trigram",
                    "value": lower_trigram,
                    "description": f"Lower trigram pattern: {lower_trigram}"
                }
            ])
            
        # Add transformation correspondences
        if "transformed_hexagram" in data:
            transformed = data["transformed_hexagram"]
            correspondences.append({
                "type": "transformed_hexagram",
                "value": transformed["number"],
                "description": f"Transformed hexagram number {transformed['number']}"
            })
            
        # Add changing line correspondences
        if "changing_lines" in data:
            changing_lines = data["changing_lines"]
            correspondences.append({
                "type": "changing_lines",
                "value": len(changing_lines),
                "description": f"Number of changing lines: {len(changing_lines)}"
            })
            
        return correspondences
        
    def format_output(self, profile: IChingProfile) -> Dict[str, Any]:
        """Format the I Ching profile for output"""
        return {
            "reading_id": profile.id,
            "name": profile.name,
            "initial_hexagram": {
                "number": profile.initial_hexagram.number,
                "name": profile.initial_hexagram.name,
                "unicode": profile.initial_hexagram.unicode_char,
                "binary": profile.initial_hexagram.binary,
                "description": profile.initial_hexagram.description,
                "judgment": profile.initial_hexagram.judgment,
                "image": profile.initial_hexagram.image,
                "lines": [
                    {
                        "position": line.position,
                        "value": line.value,
                        "is_changing": line.is_changing,
                        "change_type": line.change_type.value,
                        "meaning": line.meaning
                    }
                    for line in profile.initial_hexagram.lines
                ],
                "changing_lines": profile.initial_hexagram.changing_lines
            },
            "transformed_hexagram": {
                "number": profile.transformed_hexagram.number,
                "name": profile.transformed_hexagram.name,
                "unicode": profile.transformed_hexagram.unicode_char,
                "binary": profile.transformed_hexagram.binary,
                "description": profile.transformed_hexagram.description,
                "judgment": profile.transformed_hexagram.judgment,
                "image": profile.transformed_hexagram.image
            } if profile.transformed_hexagram else None,
            "changing_line_meanings": profile.changing_line_meanings,
            "bitcoin_resonance": profile.bitcoin_resonance,
            "chain_harmony": profile.chain_harmony,
            "governor_resonances": profile.governor_resonances,
            "attributes": [
                {
                    "name": attr["name"],
                    "value": attr["value"],
                    "description": attr["description"]
                }
                for attr in profile.attributes
            ],
            "metadata": profile.metadata
        } 